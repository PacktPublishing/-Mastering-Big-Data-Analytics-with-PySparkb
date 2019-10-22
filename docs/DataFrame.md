# DataFrame Class Methods




## Transformations

### ``agg``

Type:
Transformation

Description:
 Aggregate on the entire :class:`DataFrame` without groups
(shorthand for ``df.groupBy.agg()``).

>>> df.agg({"age": "max"}).collect()
`[Row(max(age)=5)]`
>>> from pyspark.sql import functions as F
>>> df.agg(F.min(df.age)).collect()
`[Row(min(age)=2)]`

.. versionadded:: 1.3

### ``alias``

Type:
Transformation

Description:
Returns a new :class:`DataFrame` with an alias set.

:param alias: string, an alias name to be set for the DataFrame.

>>> from pyspark.sql.functions import *
>>> df_as1 = df.alias("df_as1")
>>> df_as2 = df.alias("df_as2")
>>> joined_df = df_as1.join(df_as2, col("df_as1.name") == col("df_as2.name"), 'inner')
>>> joined_df.select("df_as1.name", "df_as2.name", "df_as2.age").collect()
[Row(name='Bob', name='Bob', age=5), Row(name='Alice', name='Alice', age=2)]

.. versionadded:: 1.3

### ``coalesce``

Type:
Transformation

Description:

Returns a new :class:`DataFrame` that has exactly `numPartitions` partitions.

:param numPartitions: int, to specify the target number of partitions

Similar to coalesce defined on an :class:`RDD`, this operation results in a
narrow dependency, e.g. if you go from 1000 partitions to 100 partitions,
there will not be a shuffle, instead each of the 100 new partitions will
claim 10 of the current partitions. If a larger number of partitions is requested,
it will stay at the current number of partitions.

However, if you're doing a drastic coalesce, e.g. to numPartitions = 1,
this may result in your computation taking place on fewer nodes than
you like (e.g. one node in the case of numPartitions = 1). To avoid this,
you can call repartition(). This will add a shuffle step, but means the
current upstream partitions will be executed in parallel (per whatever
the current partitioning is).

>>> df.coalesce(1).rdd.getNumPartitions()
1

.. versionadded:: 1.4

### ``colRegex``

Type:
Transformation

Description:

Selects column based on the column name specified as a regex and returns it
as :class:`Column`.

:param colName: string, column name specified as a regex.

>>> df = spark.createDataFrame([("a", 1), ("b", 2), ("c",  3)], ["Col1", "Col2"])
>>> df.select(df.colRegex("`(Col1)?+.+`")).show()
+----+
|Col2|
+----+
|   1|
|   2|
|   3|
+----+

.. versionadded:: 2.3

## Basic Functions

### ``cache``

Description:
Persists the :class:`DataFrame` with the default storage level (C{MEMORY_AND_DISK}).

.. note:: The default storage level has changed to C{MEMORY_AND_DISK} to match Scala in 2.0.

.. versionadded:: 1.3

### ``checkpoint``

Description:
Returns a checkpointed version of this Dataset. Checkpointing can be used to truncate the
logical plan of this DataFrame, which is especially useful in iterative algorithms where the
plan may grow exponentially. It will be saved to files inside the checkpoint
directory set with L{SparkContext.setCheckpointDir()}.

:param eager: Whether to checkpoint this DataFrame immediately

.. note:: Experimental

.. versionadded:: 2.1


## Actions





### ``approxQuantile``

Description:
Calculates the approximate quantiles of numerical columns of a
DataFrame.

The result of this algorithm has the following deterministic bound:
If the DataFrame has N elements and if we request the quantile at
probability `p` up to error `err`, then the algorithm will return
a sample `x` from the DataFrame so that the *exact* rank of `x` is
close to (p * N). More precisely,

  floor((p - err) * N) <= rank(x) <= ceil((p + err) * N).

This method implements a variation of the Greenwald-Khanna
algorithm (with some speed optimizations). The algorithm was first
present in [[http://dx.doi.org/10.1145/375663.375670
Space-efficient Online Computation of Quantile Summaries]]
by Greenwald and Khanna.

Note that null values will be ignored in numerical columns before calculation.
For columns only containing null values, an empty list is returned.

:param col: str, list.
  Can be a single column name, or a list of names for multiple columns.
:param probabilities: a list of quantile probabilities
  Each number must belong to [0, 1].
  For example 0 is the minimum, 0.5 is the median, 1 is the maximum.
:param relativeError:  The relative target precision to achieve
  (>= 0). If set to zero, the exact quantiles are computed, which
  could be very expensive. Note that values greater than 1 are
  accepted but give the same result as 1.
:return:  the approximate quantiles at the given probabilities. If
  the input `col` is a string, the output is a list of floats. If the
  input `col` is a list or tuple of strings, the output is also a
  list, but each element in it is a list of floats, i.e., the output
  is a list of list of floats.

.. versionchanged:: 2.2
   Added support for multiple columns.

.. versionadded:: 2.0








### ``collect``

Type:
Action

Description:
Returns all the records as a list of :class:`Row`.

>>> df.collect()
[Row(age=2, name='Alice'), Row(age=5, name='Bob')]

.. versionadded:: 1.3

### ``columns``

Description:
Returns all column names as a list.

>>> df.columns
['age', 'name']

.. versionadded:: 1.3

### ``corr``

Description:

Calculates the correlation of two columns of a DataFrame as a double value.
Currently only supports the Pearson Correlation Coefficient.
:func:`DataFrame.corr` and :func:`DataFrameStatFunctions.corr` are aliases of each other.

:param col1: The name of the first column
:param col2: The name of the second column
:param method: The correlation method. Currently only supports "pearson"

.. versionadded:: 1.4

### ``count``

Type:
Action

Description:
Returns the number of rows in this :class:`DataFrame`.

>>> df.count()
2

.. versionadded:: 1.3

### ``cov``

Description:

Calculate the sample covariance for the given columns, specified by their names, as a
double value. :func:`DataFrame.cov` and :func:`DataFrameStatFunctions.cov` are aliases.

:param col1: The name of the first column
:param col2: The name of the second column

.. versionadded:: 1.4

### ``createGlobalTempView``

Description:
Creates a global temporary view with this DataFrame.

The lifetime of this temporary view is tied to this Spark application.
throws :class:`TempTableAlreadyExistsException`, if the view name already exists in the
catalog.

>>> df.createGlobalTempView("people")
>>> df2 = spark.sql("select * from global_temp.people")
>>> sorted(df.collect()) == sorted(df2.collect())
True
>>> df.createGlobalTempView("people")  # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
...
AnalysisException: u"Temporary table 'people' already exists;"
>>> spark.catalog.dropGlobalTempView("people")

.. versionadded:: 2.1

### ``createOrReplaceGlobalTempView``

Description:
Creates or replaces a global temporary view using the given name.

The lifetime of this temporary view is tied to this Spark application.

>>> df.createOrReplaceGlobalTempView("people")
>>> df2 = df.filter(df.age > 3)
>>> df2.createOrReplaceGlobalTempView("people")
>>> df3 = spark.sql("select * from global_temp.people")
>>> sorted(df3.collect()) == sorted(df2.collect())
True
>>> spark.catalog.dropGlobalTempView("people")

.. versionadded:: 2.2

### ``createOrReplaceTempView``

Description:
Creates or replaces a local temporary view with this DataFrame.

The lifetime of this temporary table is tied to the :class:`SparkSession`
that was used to create this :class:`DataFrame`.

>>> df.createOrReplaceTempView("people")
>>> df2 = df.filter(df.age > 3)
>>> df2.createOrReplaceTempView("people")
>>> df3 = spark.sql("select * from people")
>>> sorted(df3.collect()) == sorted(df2.collect())
True
>>> spark.catalog.dropTempView("people")

.. versionadded:: 2.0

### ``createTempView``

Description:
Creates a local temporary view with this DataFrame.

The lifetime of this temporary table is tied to the :class:`SparkSession`
that was used to create this :class:`DataFrame`.
throws :class:`TempTableAlreadyExistsException`, if the view name already exists in the
catalog.

>>> df.createTempView("people")
>>> df2 = spark.sql("select * from people")
>>> sorted(df.collect()) == sorted(df2.collect())
True
>>> df.createTempView("people")  # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
...
AnalysisException: u"Temporary table 'people' already exists;"
>>> spark.catalog.dropTempView("people")

.. versionadded:: 2.0

### ``crossJoin``

Type:
Transformation

Description:
Returns the cartesian product with another :class:`DataFrame`.

:param other: Right side of the cartesian product.

>>> df.select("age", "name").collect()
[Row(age=2, name='Alice'), Row(age=5, name='Bob')]
>>> df2.select("name", "height").collect()
[Row(name='Tom', height=80), Row(name='Bob', height=85)]
>>> df.crossJoin(df2.select("height")).select("age", "name", "height").collect()
[Row(age=2, name='Alice', height=80), Row(age=2, name='Alice', height=85),
 Row(age=5, name='Bob', height=80), Row(age=5, name='Bob', height=85)]

.. versionadded:: 2.1

### ``crosstab``

Description:

Computes a pair-wise frequency table of the given columns. Also known as a contingency
table. The number of distinct values for each column should be less than 1e4. At most 1e6
non-zero pair frequencies will be returned.
The first column of each row will be the distinct values of `col1` and the column names
will be the distinct values of `col2`. The name of the first column will be `$col1_$col2`.
Pairs that have no occurrences will have zero as their counts.
:func:`DataFrame.crosstab` and :func:`DataFrameStatFunctions.crosstab` are aliases.

:param col1: The name of the first column. Distinct items will make the first item of
each row.
:param col2: The name of the second column. Distinct items will make the column names
of the DataFrame.

.. versionadded:: 1.4

### ``cube``

Type:
Transformation

Description:
Create a multi-dimensional cube for the current :class:`DataFrame` using
the specified columns, so we can run aggregation on them.

>>> df.cube("name", df.age).count().orderBy("name", "age").show()
+-----+----+-----+
| name| age|count|
+-----+----+-----+
| null|null|2|
| null|   2|1|
| null|   5|1|
|Alice|null|1|
|Alice|   2|1|
|  Bob|null|1|
|  Bob|   5|1|
+-----+----+-----+

.. versionadded:: 1.4

### ``describe``

Type:
Action

Description:
Computes basic statistics for numeric and string columns.

This include count, mean, stddev, min, and max. If no columns are
given, this function computes statistics for all numerical or string columns.

.. note:: This function is meant for exploratory data analysis, as we make no
guarantee about the backward compatibility of the schema of the resulting DataFrame.

>>> df.describe(['age']).show()
+-------+------------------+
|summary|   age|
+-------+------------------+
|  count| 2|
|   mean|   3.5|
| stddev|2.1213203435596424|
|min| 2|
|max| 5|
+-------+------------------+
>>> df.describe().show()
+-------+------------------+-----+
|summary|   age| name|
+-------+------------------+-----+
|  count| 2|2|
|   mean|   3.5| null|
| stddev|2.1213203435596424| null|
|min| 2|Alice|
|max| 5|  Bob|
+-------+------------------+-----+

Use summary for expanded statistics and control over which statistics to compute.

.. versionadded:: 1.3.1

### ``distinct``

Type:
Transformation

Description:
Returns a new :class:`DataFrame` containing the distinct rows in this :class:`DataFrame`.

>>> df.distinct().count()
2

.. versionadded:: 1.3

### ``drop``

Type:
Transformation

Description:
Returns a new :class:`DataFrame` that drops the specified column.
This is a no-op if schema doesn't contain the given column name(s).

:param cols: a string name of the column to drop, or a
:class:`Column` to drop, or a list of string name of the columns to drop.

>>> df.drop('age').collect()
[Row(name='Alice'), Row(name='Bob')]

>>> df.drop(df.age).collect()
[Row(name='Alice'), Row(name='Bob')]

>>> df.join(df2, df.name == df2.name, 'inner').drop(df.name).collect()
[Row(age=5, height=85, name='Bob')]

>>> df.join(df2, df.name == df2.name, 'inner').drop(df2.name).collect()
[Row(age=5, name='Bob', height=85)]

>>> df.join(df2, 'name', 'inner').drop('age', 'height').collect()
[Row(name='Bob')]

.. versionadded:: 1.4

### ``dropDuplicates``

Type:
Transformation

Description:
Return a new :class:`DataFrame` with duplicate rows removed,
optionally only considering certain columns.

For a static batch :class:`DataFrame`, it just drops duplicate rows. For a streaming
:class:`DataFrame`, it will keep all data across triggers as intermediate state to drop
duplicates rows. You can use :func:`withWatermark` to limit how late the duplicate data can
be and system will accordingly limit the state. In addition, too late data older than
watermark will be dropped to avoid any possibility of duplicates.

:func:`drop_duplicates` is an alias for :func:`dropDuplicates`.

>>> from pyspark.sql import Row
>>> df = sc.parallelize([ \
... Row(name='Alice', age=5, height=80), \
... Row(name='Alice', age=5, height=80), \
... Row(name='Alice', age=10, height=80)]).toDF()
>>> df.dropDuplicates().show()
+---+------+-----+
|age|height| name|
+---+------+-----+
|  5|80|Alice|
| 10|80|Alice|
+---+------+-----+

>>> df.dropDuplicates(['name', 'height']).show()
+---+------+-----+
|age|height| name|
+---+------+-----+
|  5|80|Alice|
+---+------+-----+

.. versionadded:: 1.4

### ``drop_duplicates``

Description:
:func:`drop_duplicates` is an alias for :func:`dropDuplicates`.

.. versionadded:: 1.4

### ``dropna``

Description:
Returns a new :class:`DataFrame` omitting rows with null values.
:func:`DataFrame.dropna` and :func:`DataFrameNaFunctions.drop` are aliases of each other.

:param how: 'any' or 'all'.
If 'any', drop a row if it contains any nulls.
If 'all', drop a row only if all its values are null.
:param thresh: int, default None
If specified, drop rows that have less than `thresh` non-null values.
This overwrites the `how` parameter.
:param subset: optional list of column names to consider.

>>> df4.na.drop().show()
+---+------+-----+
|age|height| name|
+---+------+-----+
| 10|80|Alice|
+---+------+-----+

.. versionadded:: 1.3.1

### ``dtypes``

Description:
Returns all column names and their data types as a list.

>>> df.dtypes
[('age', 'int'), ('name', 'string')]

.. versionadded:: 1.3

### ``exceptAll``

Type:
Transformation

Description:
Return a new :class:`DataFrame` containing rows in this :class:`DataFrame` but
not in another :class:`DataFrame` while preserving duplicates.

This is equivalent to `EXCEPT ALL` in SQL.

>>> df1 = spark.createDataFrame(
... [("a", 1), ("a", 1), ("a", 1), ("a", 2), ("b",  3), ("c", 4)], ["C1", "C2"])
>>> df2 = spark.createDataFrame([("a", 1), ("b", 3)], ["C1", "C2"])

>>> df1.exceptAll(df2).show()
+---+---+
| C1| C2|
+---+---+
|  a|  1|
|  a|  1|
|  a|  2|
|  c|  4|
+---+---+

Also as standard in SQL, this function resolves columns by position (not by name).

.. versionadded:: 2.4

### ``explain``

Description:
Prints the (logical and physical) plans to the console for debugging purpose.

:param extended: boolean, default ``False``. If ``False``, prints only the physical plan.

>>> df.explain()
== Physical Plan ==
Scan ExistingRDD[age#0,name#1]

>>> df.explain(True)
== Parsed Logical Plan ==
...
== Analyzed Logical Plan ==
...
== Optimized Logical Plan ==
...
== Physical Plan ==
...

.. versionadded:: 1.3

### ``fillna``

Description:
Replace null values, alias for ``na.fill()``.
:func:`DataFrame.fillna` and :func:`DataFrameNaFunctions.fill` are aliases of each other.

:param value: int, long, float, string, bool or dict.
Value to replace null values with.
If the value is a dict, then `subset` is ignored and `value` must be a mapping
from column name (string) to replacement value. The replacement value must be
an int, long, float, boolean, or string.
:param subset: optional list of column names to consider.
Columns specified in subset that do not have matching data type are ignored.
For example, if `value` is a string, and subset contains a non-string column,
then the non-string column is simply ignored.

>>> df4.na.fill(50).show()
+---+------+-----+
|age|height| name|
+---+------+-----+
| 10|80|Alice|
|  5|50|  Bob|
| 50|50|  Tom|
| 50|50| null|
+---+------+-----+

>>> df5.na.fill(False).show()
+----+-------+-----+
| age|   name|  spy|
+----+-------+-----+
|  10|  Alice|false|
|   5|Bob|false|
|null|Mallory| true|
+----+-------+-----+

>>> df4.na.fill({'age': 50, 'name': 'unknown'}).show()
+---+------+-------+
|age|height|   name|
+---+------+-------+
| 10|80|  Alice|
|  5|  null|Bob|
| 50|  null|Tom|
| 50|  null|unknown|
+---+------+-------+

.. versionadded:: 1.3.1

### ``filter``

Type:
Transformation

Description:
Filters rows using the given condition.

:func:`where` is an alias for :func:`filter`.

:param condition: a :class:`Column` of :class:`types.BooleanType`
or a string of SQL expression.

>>> df.filter(df.age > 3).collect()
[Row(age=5, name='Bob')]
>>> df.where(df.age == 2).collect()
[Row(age=2, name='Alice')]

>>> df.filter("age > 3").collect()
[Row(age=5, name='Bob')]
>>> df.where("age = 2").collect()
[Row(age=2, name='Alice')]

.. versionadded:: 1.3

### ``first``

Type:
Action

Description:
Returns the first row as a :class:`Row`.

>>> df.first()
Row(age=2, name='Alice')

.. versionadded:: 1.3

### ``foreach``

Type:
Action

Description:
Applies the ``f`` function to all :class:`Row` of this :class:`DataFrame`.

This is a shorthand for ``df.rdd.foreach()``.

>>> def f(person):
... print(person.name)
>>> df.foreach(f)

.. versionadded:: 1.3

### ``foreachPartition``

Type:
Action

Description:
Applies the ``f`` function to each partition of this :class:`DataFrame`.

This a shorthand for ``df.rdd.foreachPartition()``.

>>> def f(people):
... for person in people:
... print(person.name)
>>> df.foreachPartition(f)

.. versionadded:: 1.3

### ``freqItems``

Description:

Finding frequent items for columns, possibly with false positives. Using the
frequent element count algorithm described in
"http://dx.doi.org/10.1145/762471.762473, proposed by Karp, Schenker, and Papadimitriou".
:func:`DataFrame.freqItems` and :func:`DataFrameStatFunctions.freqItems` are aliases.

.. note:: This function is meant for exploratory data analysis, as we make no
guarantee about the backward compatibility of the schema of the resulting DataFrame.

:param cols: Names of the columns to calculate frequent items for as a list or tuple of
strings.
:param support: The frequency with which to consider an item 'frequent'. Default is 1%.
The support must be greater than 1e-4.

.. versionadded:: 1.4

### ``groupBy``

Type:
Transformation

Description:
Groups the :class:`DataFrame` using the specified columns,
so we can run aggregation on them. See :class:`GroupedData`
for all the available aggregate functions.

:func:`groupby` is an alias for :func:`groupBy`.

:param cols: list of columns to group by.
Each element should be a column name (string) or an expression (:class:`Column`).

```python
>>> df.groupBy().avg().collect()
[Row(avg(age)=3.5)]
>>> sorted(df.groupBy('name').agg({'age': 'mean'}).collect())
[Row(name='Alice', avg(age)=2.0), Row(name='Bob', avg(age)=5.0)]
>>> sorted(df.groupBy(df.name).avg().collect())
[Row(name='Alice', avg(age)=2.0), Row(name='Bob', avg(age)=5.0)]
>>> sorted(df.groupBy(['name', df.age]).count().collect())
[Row(name='Alice', age=2, count=1), Row(name='Bob', age=5, count=1)]
```

.. versionadded:: 1.3

### ``groupby``

Type:
Transformation

Description:
:func:`groupby` is an alias for :func:`groupBy`.

.. versionadded:: 1.4

### ``head``

Type:
Action

Description:
Returns the first ``n`` rows.

.. note:: This method should only be used if the resulting array is expected
to be small, as all the data is loaded into the driver's memory.

:param n: int, default 1. Number of rows to return.
:return: If n is greater than 1, return a list of :class:`Row`.
If n is 1, return a single Row.

>>> df.head()
Row(age=2, name='Alice')
>>> df.head(1)
[Row(age=2, name='Alice')]

.. versionadded:: 1.3

### ``hint``

Description:
Specifies some hint on the current DataFrame.

:param name: A name of the hint.
:param parameters: Optional parameters.
:return: :class:`DataFrame`

>>> df.join(df2.hint("broadcast"), "name").show()
+----+---+------+
|name|age|height|
+----+---+------+
| Bob|  5|85|
+----+---+------+

.. versionadded:: 2.2

### ``intersect``

Type:
Transformation

Description:
 Return a new :class:`DataFrame` containing rows only in
both this frame and another frame.

This is equivalent to `INTERSECT` in SQL.

.. versionadded:: 1.3

### ``intersectAll``

Type:
Transformation

Description:
 Return a new :class:`DataFrame` containing rows in both this dataframe and other
dataframe while preserving duplicates.

This is equivalent to `INTERSECT ALL` in SQL.
>>> df1 = spark.createDataFrame([("a", 1), ("a", 1), ("b", 3), ("c", 4)], ["C1", "C2"])
>>> df2 = spark.createDataFrame([("a", 1), ("a", 1), ("b", 3)], ["C1", "C2"])

>>> df1.intersectAll(df2).sort("C1", "C2").show()
+---+---+
| C1| C2|
+---+---+
|  a|  1|
|  a|  1|
|  b|  3|
+---+---+

Also as standard in SQL, this function resolves columns by position (not by name).

.. versionadded:: 2.4

### ``isLocal``

Description:
Returns ``True`` if the :func:`collect` and :func:`take` methods can be run locally
(without any Spark executors).

.. versionadded:: 1.3

### ``isStreaming``

Description:
Returns true if this :class:`Dataset` contains one or more sources that continuously
return data as it arrives. A :class:`Dataset` that reads data from a streaming source
must be executed as a :class:`StreamingQuery` using the :func:`start` method in
:class:`DataStreamWriter`.  Methods that return a single answer, (e.g., :func:`count` or
:func:`collect`) will throw an :class:`AnalysisException` when there is a streaming
source present.

.. note:: Evolving

.. versionadded:: 2.0

### ``join``

Type:
Transformation

Description:
Joins with another :class:`DataFrame`, using the given join expression.

:param other: Right side of the join
:param on: a string for the join column name, a list of column names,
a join expression (Column), or a list of Columns.
If `on` is a string or a list of strings indicating the name of the join column(s),
the column(s) must exist on both sides, and this performs an equi-join.
:param how: str, default ``inner``. Must be one of: ``inner``, ``cross``, ``outer``,
``full``, ``full_outer``, ``left``, ``left_outer``, ``right``, ``right_outer``,
``left_semi``, and ``left_anti``.

The following performs a full outer join between ``df1`` and ``df2``.

>>> df.join(df2, df.name == df2.name, 'outer').select(df.name, df2.height).collect()
[Row(name=None, height=80), Row(name='Bob', height=85), Row(name='Alice', height=None)]

>>> df.join(df2, 'name', 'outer').select('name', 'height').collect()
[Row(name='Tom', height=80), Row(name='Bob', height=85), Row(name='Alice', height=None)]

>>> cond = [df.name == df3.name, df.age == df3.age]
>>> df.join(df3, cond, 'outer').select(df.name, df3.age).collect()
[Row(name='Alice', age=2), Row(name='Bob', age=5)]

>>> df.join(df2, 'name').select(df.name, df2.height).collect()
[Row(name='Bob', height=85)]

>>> df.join(df4, ['name', 'age']).select(df.name, df.age).collect()
[Row(name='Bob', age=5)]

.. versionadded:: 1.3

### ``limit``

Type:
Transformation

Description:
Limits the result count to the number specified.

>>> df.limit(1).collect()
[Row(age=2, name='Alice')]
>>> df.limit(0).collect()
[]

.. versionadded:: 1.3

### ``localCheckpoint``

Description:
Returns a locally checkpointed version of this Dataset. Checkpointing can be used to
truncate the logical plan of this DataFrame, which is especially useful in iterative
algorithms where the plan may grow exponentially. Local checkpoints are stored in the
executors using the caching subsystem and therefore they are not reliable.

:param eager: Whether to checkpoint this DataFrame immediately

.. note:: Experimental

.. versionadded:: 2.3

### ``na``

Type:
Transformation

Description:
Returns a :class:`DataFrameNaFunctions` for handling missing values.

.. versionadded:: 1.3.1

### ``orderBy``

Type:
Transformation

Description:
Returns a new :class:`DataFrame` sorted by the specified column(s).

:param cols: list of :class:`Column` or column names to sort by.
:param ascending: boolean or list of boolean (default True).
Sort ascending vs. descending. Specify list for multiple sort orders.
If a list is specified, length of the list must equal length of the `cols`.

>>> df.sort(df.age.desc()).collect()
[Row(age=5, name='Bob'), Row(age=2, name='Alice')]
>>> df.sort("age", ascending=False).collect()
[Row(age=5, name='Bob'), Row(age=2, name='Alice')]
>>> df.orderBy(df.age.desc()).collect()
[Row(age=5, name='Bob'), Row(age=2, name='Alice')]
>>> from pyspark.sql.functions import *
>>> df.sort(asc("age")).collect()
[Row(age=2, name='Alice'), Row(age=5, name='Bob')]
>>> df.orderBy(desc("age"), "name").collect()
[Row(age=5, name='Bob'), Row(age=2, name='Alice')]
>>> df.orderBy(["age", "name"], ascending=[0, 1]).collect()
[Row(age=5, name='Bob'), Row(age=2, name='Alice')]

.. versionadded:: 1.3

### ``persist``

Description:
Sets the storage level to persist the contents of the :class:`DataFrame` across
operations after the first time it is computed. This can only be used to assign
a new storage level if the :class:`DataFrame` does not have a storage level set yet.
If no storage level is specified defaults to (C{MEMORY_AND_DISK}).

.. note:: The default storage level has changed to C{MEMORY_AND_DISK} to match Scala in 2.0.

.. versionadded:: 1.3

### ``printSchema``

Description:
Prints out the schema in the tree format.

>>> df.printSchema()
root
 |-- age: integer (nullable = true)
 |-- name: string (nullable = true)
<BLANKLINE>

.. versionadded:: 1.3

### ``randomSplit``

Type:
Transformation

Description:
Randomly splits this :class:`DataFrame` with the provided weights.

:param weights: list of doubles as weights with which to split the DataFrame. Weights will
be normalized if they don't sum up to 1.0.
:param seed: The seed for sampling.

>>> splits = df4.randomSplit([1.0, 2.0], 24)
>>> splits[0].count()
1

>>> splits[1].count()
3

.. versionadded:: 1.4

### ``rdd``

Description:
Returns the content as an :class:`pyspark.RDD` of :class:`Row`.

.. versionadded:: 1.3

### ``registerTempTable``

Description:
Registers this DataFrame as a temporary table using the given name.

The lifetime of this temporary table is tied to the :class:`SparkSession`
that was used to create this :class:`DataFrame`.

>>> df.registerTempTable("people")
>>> df2 = spark.sql("select * from people")
>>> sorted(df.collect()) == sorted(df2.collect())
True
>>> spark.catalog.dropTempView("people")

.. note:: Deprecated in 2.0, use createOrReplaceTempView instead.

.. versionadded:: 1.3

### ``repartition``

Type:
Transformation

Description:

Returns a new :class:`DataFrame` partitioned by the given partitioning expressions. The
resulting DataFrame is hash partitioned.

:param numPartitions:
can be an int to specify the target number of partitions or a Column.
If it is a Column, it will be used as the first partitioning column. If not specified,
the default number of partitions is used.

.. versionchanged:: 1.6
   Added optional arguments to specify the partitioning columns. Also made numPartitions
   optional if partitioning columns are specified.

>>> df.repartition(10).rdd.getNumPartitions()
10
>>> data = df.union(df).repartition("age")
>>> data.show()
+---+-----+
|age| name|
+---+-----+
|  5|  Bob|
|  5|  Bob|
|  2|Alice|
|  2|Alice|
+---+-----+
>>> data = data.repartition(7, "age")
>>> data.show()
+---+-----+
|age| name|
+---+-----+
|  2|Alice|
|  5|  Bob|
|  2|Alice|
|  5|  Bob|
+---+-----+
>>> data.rdd.getNumPartitions()
7
>>> data = data.repartition("name", "age")
>>> data.show()
+---+-----+
|age| name|
+---+-----+
|  5|  Bob|
|  5|  Bob|
|  2|Alice|
|  2|Alice|
+---+-----+

.. versionadded:: 1.3

### ``repartitionByRange``

Type:
Transformation

Description:
Returns a new :class:`DataFrame` partitioned by the given partitioning expressions. The
resulting DataFrame is range partitioned.

:param numPartitions:
can be an int to specify the target number of partitions or a Column.
If it is a Column, it will be used as the first partitioning column. If not specified,
the default number of partitions is used.

At least one partition-by expression must be specified.
When no explicit sort order is specified, "ascending nulls first" is assumed.

>>> df.repartitionByRange(2, "age").rdd.getNumPartitions()
2
>>> df.show()
+---+-----+
|age| name|
+---+-----+
|  2|Alice|
|  5|  Bob|
+---+-----+
>>> df.repartitionByRange(1, "age").rdd.getNumPartitions()
1
>>> data = df.repartitionByRange("age")
>>> df.show()
+---+-----+
|age| name|
+---+-----+
|  2|Alice|
|  5|  Bob|
+---+-----+

.. versionadded:: 2.4.0

### ``replace``

Description:
Returns a new :class:`DataFrame` replacing a value with another value.
:func:`DataFrame.replace` and :func:`DataFrameNaFunctions.replace` are
aliases of each other.
Values to_replace and value must have the same type and can only be numerics, booleans,
or strings. Value can have None. When replacing, the new value will be cast
to the type of the existing column.
For numeric replacements all values to be replaced should have unique
floating point representation. In case of conflicts (for example with `{42: -1, 42.0: 1}`)
and arbitrary replacement will be used.

:param to_replace: bool, int, long, float, string, list or dict.
Value to be replaced.
If the value is a dict, then `value` is ignored or can be omitted, and `to_replace`
must be a mapping between a value and a replacement.
:param value: bool, int, long, float, string, list or None.
The replacement value must be a bool, int, long, float, string or None. If `value` is a
list, `value` should be of the same length and type as `to_replace`.
If `value` is a scalar and `to_replace` is a sequence, then `value` is
used as a replacement for each item in `to_replace`.
:param subset: optional list of column names to consider.
Columns specified in subset that do not have matching data type are ignored.
For example, if `value` is a string, and subset contains a non-string column,
then the non-string column is simply ignored.

>>> df4.na.replace(10, 20).show()
+----+------+-----+
| age|height| name|
+----+------+-----+
|  20|80|Alice|
|   5|  null|  Bob|
|null|  null|  Tom|
|null|  null| null|
+----+------+-----+

>>> df4.na.replace('Alice', None).show()
+----+------+----+
| age|height|name|
+----+------+----+
|  10|80|null|
|   5|  null| Bob|
|null|  null| Tom|
|null|  null|null|
+----+------+----+

>>> df4.na.replace({'Alice': None}).show()
+----+------+----+
| age|height|name|
+----+------+----+
|  10|80|null|
|   5|  null| Bob|
|null|  null| Tom|
|null|  null|null|
+----+------+----+

>>> df4.na.replace(['Alice', 'Bob'], ['A', 'B'], 'name').show()
+----+------+----+
| age|height|name|
+----+------+----+
|  10|80|   A|
|   5|  null|   B|
|null|  null| Tom|
|null|  null|null|
+----+------+----+

.. versionadded:: 1.4

### ``rollup``

Type:
Transformation

Description:

Create a multi-dimensional rollup for the current :class:`DataFrame` using
the specified columns, so we can run aggregation on them.

>>> df.rollup("name", df.age).count().orderBy("name", "age").show()
+-----+----+-----+
| name| age|count|
+-----+----+-----+
| null|null|2|
|Alice|null|1|
|Alice|   2|1|
|  Bob|null|1|
|  Bob|   5|1|
+-----+----+-----+

.. versionadded:: 1.4

### ``sample``

Type:
Transformation

Description:
Returns a sampled subset of this :class:`DataFrame`.

:param withReplacement: Sample with replacement or not (default False).
:param fraction: Fraction of rows to generate, range [0.0, 1.0].
:param seed: Seed for sampling (default a random seed).

.. note:: This is not guaranteed to provide exactly the fraction specified of the total
count of the given :class:`DataFrame`.

.. note:: `fraction` is required and, `withReplacement` and `seed` are optional.

>>> df = spark.range(10)
>>> df.sample(0.5, 3).count()
4
>>> df.sample(fraction=0.5, seed=3).count()
4
>>> df.sample(withReplacement=True, fraction=0.5, seed=3).count()
1
>>> df.sample(1.0).count()
10
>>> df.sample(fraction=1.0).count()
10
>>> df.sample(False, fraction=1.0).count()
10

.. versionadded:: 1.3

### ``sampleBy``

Description:

Returns a stratified sample without replacement based on the
fraction given on each stratum.

:param col: column that defines strata
:param fractions:
sampling fraction for each stratum. If a stratum is not
specified, we treat its fraction as zero.
:param seed: random seed
:return: a new DataFrame that represents the stratified sample

>>> from pyspark.sql.functions import col
>>> dataset = sqlContext.range(0, 100).select((col("id") % 3).alias("key"))
>>> sampled = dataset.sampleBy("key", fractions={0: 0.1, 1: 0.2}, seed=0)
>>> sampled.groupBy("key").count().orderBy("key").show()
+---+-----+
|key|count|
+---+-----+
|  0|5|
|  1|9|
+---+-----+

.. versionadded:: 1.5

### ``schema``

Description:
Returns the schema of this :class:`DataFrame` as a :class:`pyspark.sql.types.StructType`.

>>> df.schema
StructType(List(StructField(age,IntegerType,true),StructField(name,StringType,true)))

.. versionadded:: 1.3

### ``select``

Type:
Transformation

Description:
Projects a set of expressions and returns a new :class:`DataFrame`.

:param cols: list of column names (string) or expressions (:class:`Column`).
If one of the column names is '*', that column is expanded to include all columns
in the current DataFrame.

>>> df.select('*').collect()
[Row(age=2, name='Alice'), Row(age=5, name='Bob')]
>>> df.select('name', 'age').collect()
[Row(name='Alice', age=2), Row(name='Bob', age=5)]
>>> df.select(df.name, (df.age + 10).alias('age')).collect()
[Row(name='Alice', age=12), Row(name='Bob', age=15)]

.. versionadded:: 1.3

### ``selectExpr``

Type:
Transformation

Description:
Projects a set of SQL expressions and returns a new :class:`DataFrame`.

This is a variant of :func:`select` that accepts SQL expressions.

>>> df.selectExpr("age * 2", "abs(age)").collect()
[Row((age * 2)=4, abs(age)=2), Row((age * 2)=10, abs(age)=5)]

.. versionadded:: 1.3

### ``show``

Type:
Action

Description:
Prints the first ``n`` rows to the console.

:param n: Number of rows to show.
:param truncate: If set to True, truncate strings longer than 20 chars by default.
If set to a number greater than one, truncates long strings to length ``truncate``
and align cells right.
:param vertical: If set to True, print output rows vertically (one line
per column value).

>>> df
DataFrame[age: int, name: string]
>>> df.show()
+---+-----+
|age| name|
+---+-----+
|  2|Alice|
|  5|  Bob|
+---+-----+
>>> df.show(truncate=3)
+---+----+
|age|name|
+---+----+
|  2| Ali|
|  5| Bob|
+---+----+
>>> df.show(vertical=True)
-RECORD 0-----
 age  | 2
 name | Alice
-RECORD 1-----
 age  | 5
 name | Bob

.. versionadded:: 1.3

### ``sort``

Type:
Transformation

Description:
Returns a new :class:`DataFrame` sorted by the specified column(s).

:param cols: list of :class:`Column` or column names to sort by.
:param ascending: boolean or list of boolean (default True).
Sort ascending vs. descending. Specify list for multiple sort orders.
If a list is specified, length of the list must equal length of the `cols`.

>>> df.sort(df.age.desc()).collect()
[Row(age=5, name='Bob'), Row(age=2, name='Alice')]
>>> df.sort("age", ascending=False).collect()
[Row(age=5, name='Bob'), Row(age=2, name='Alice')]
>>> df.orderBy(df.age.desc()).collect()
[Row(age=5, name='Bob'), Row(age=2, name='Alice')]
>>> from pyspark.sql.functions import *
>>> df.sort(asc("age")).collect()
[Row(age=2, name='Alice'), Row(age=5, name='Bob')]
>>> df.orderBy(desc("age"), "name").collect()
[Row(age=5, name='Bob'), Row(age=2, name='Alice')]
>>> df.orderBy(["age", "name"], ascending=[0, 1]).collect()
[Row(age=5, name='Bob'), Row(age=2, name='Alice')]

.. versionadded:: 1.3

### ``sortWithinPartitions``

Type:
Transformation

Description:
Returns a new :class:`DataFrame` with each partition sorted by the specified column(s).

:param cols: list of :class:`Column` or column names to sort by.
:param ascending: boolean or list of boolean (default True).
Sort ascending vs. descending. Specify list for multiple sort orders.
If a list is specified, length of the list must equal length of the `cols`.

>>> df.sortWithinPartitions("age", ascending=False).show()
+---+-----+
|age| name|
+---+-----+
|  2|Alice|
|  5|  Bob|
+---+-----+

.. versionadded:: 1.6

### ``stat``

Type:
Transformation

Description:
Returns a :class:`DataFrameStatFunctions` for statistic functions.

.. versionadded:: 1.4

### ``storageLevel``

Description:
Get the :class:`DataFrame`'s current storage level.

>>> df.storageLevel
StorageLevel(False, False, False, False, 1)
>>> df.cache().storageLevel
StorageLevel(True, True, False, True, 1)
>>> df2.persist(StorageLevel.DISK_ONLY_2).storageLevel
StorageLevel(True, False, False, False, 2)

.. versionadded:: 2.1

### ``subtract``

Description:
 Return a new :class:`DataFrame` containing rows in this frame
but not in another frame.

This is equivalent to `EXCEPT DISTINCT` in SQL.

.. versionadded:: 1.3

### ``summary``

Type:
Action

Description:
Computes specified statistics for numeric and string columns. Available statistics are:
- count
- mean
- stddev
- min
- max
- arbitrary approximate percentiles specified as a percentage (eg, 75%)

If no statistics are given, this function computes count, mean, stddev, min,
approximate quartiles (percentiles at 25%, 50%, and 75%), and max.

.. note:: This function is meant for exploratory data analysis, as we make no
guarantee about the backward compatibility of the schema of the resulting DataFrame.

>>> df.summary().show()
+-------+------------------+-----+
|summary|   age| name|
+-------+------------------+-----+
|  count| 2|2|
|   mean|   3.5| null|
| stddev|2.1213203435596424| null|
|min| 2|Alice|
|25%| 2| null|
|50%| 2| null|
|75%| 5| null|
|max| 5|  Bob|
+-------+------------------+-----+

>>> df.summary("count", "min", "25%", "75%", "max").show()
+-------+---+-----+
|summary|age| name|
+-------+---+-----+
|  count|  2|2|
|min|  2|Alice|
|25%|  2| null|
|75%|  5| null|
|max|  5|  Bob|
+-------+---+-----+

To do a summary for specific columns first select them:

>>> df.select("age", "name").summary("count").show()
+-------+---+----+
|summary|age|name|
+-------+---+----+
|  count|  2|   2|
+-------+---+----+

See also describe for basic statistics.

.. versionadded:: 2.3.0

### ``take``

Type:
Action

Description:
Returns the first ``num`` rows as a :class:`list` of :class:`Row`.

>>> df.take(2)
[Row(age=2, name='Alice'), Row(age=5, name='Bob')]

.. versionadded:: 1.3

### ``toDF``

Description:
Returns a new class:`DataFrame` that with new specified column names

:param cols: list of new column names (string)

>>> df.toDF('f1', 'f2').collect()
[Row(f1=2, f2='Alice'), Row(f1=5, f2='Bob')]


### ``toJSON``

Description:
Converts a :class:`DataFrame` into a :class:`RDD` of string.

Each row is turned into a JSON document as one element in the returned RDD.

>>> df.toJSON().first()
'{"age":2,"name":"Alice"}'

.. versionadded:: 1.3

### ``toLocalIterator``

Type:
Action

Description:

Returns an iterator that contains all of the rows in this :class:`DataFrame`.
The iterator will consume as much memory as the largest partition in this DataFrame.

>>> list(df.toLocalIterator())
[Row(age=2, name='Alice'), Row(age=5, name='Bob')]

.. versionadded:: 2.0

### ``toPandas``

Description:

Returns the contents of this :class:`DataFrame` as Pandas ``pandas.DataFrame``.

This is only available if Pandas is installed and available.

.. note:: This method should only be used if the resulting Pandas's DataFrame is expected
to be small, as all the data is loaded into the driver's memory.

.. note:: Usage with spark.sql.execution.arrow.enabled=True is experimental.

>>> df.toPandas()  # doctest: +SKIP
   age   name
02  Alice
15Bob

.. versionadded:: 1.3

### ``union``

Type:
Transformation

Description:
 Return a new :class:`DataFrame` containing union of rows in this and another frame.

This is equivalent to `UNION ALL` in SQL. To do a SQL-style set union
(that does deduplication of elements), use this function followed by :func:`distinct`.

Also as standard in SQL, this function resolves columns by position (not by name).

.. versionadded:: 2.0

### ``unionAll``

Type:
Transformation

Description:
 Return a new :class:`DataFrame` containing union of rows in this and another frame.

This is equivalent to `UNION ALL` in SQL. To do a SQL-style set union
(that does deduplication of elements), use this function followed by :func:`distinct`.

Also as standard in SQL, this function resolves columns by position (not by name).

.. note:: Deprecated in 2.0, use :func:`union` instead.

.. versionadded:: 1.3

### ``unionByName``

Type:
Transformation

Description:
 Returns a new :class:`DataFrame` containing union of rows in this and another frame.

This is different from both `UNION ALL` and `UNION DISTINCT` in SQL. To do a SQL-style set
union (that does deduplication of elements), use this function followed by :func:`distinct`.

The difference between this function and :func:`union` is that this function
resolves columns by name (not by position):

>>> df1 = spark.createDataFrame([[1, 2, 3]], ["col0", "col1", "col2"])
>>> df2 = spark.createDataFrame([[4, 5, 6]], ["col1", "col2", "col0"])
>>> df1.unionByName(df2).show()
+----+----+----+
|col0|col1|col2|
+----+----+----+
|   1|   2|   3|
|   6|   4|   5|
+----+----+----+

.. versionadded:: 2.3

### ``unpersist``

Description:
Marks the :class:`DataFrame` as non-persistent, and remove all blocks for it from
memory and disk.

.. note:: `blocking` default has changed to False to match Scala in 2.0.

.. versionadded:: 1.3

### ``where``

Type:
Transformation

Description:
:func:`where` is an alias for :func:`filter`.

.. versionadded:: 1.3

### ``withColumn``

Type:
Transformation

Description:
Returns a new :class:`DataFrame` by adding a column or replacing the
existing column that has the same name.

The column expression must be an expression over this DataFrame; attempting to add
a column from some other dataframe will raise an error.

:param colName: string, name of the new column.
:param col: a :class:`Column` expression for the new column.

>>> df.withColumn('age2', df.age + 2).collect()
[Row(age=2, name='Alice', age2=4), Row(age=5, name='Bob', age2=7)]

.. versionadded:: 1.3

### ``withColumnRenamed``

Type:
Transformation

Description:
Returns a new :class:`DataFrame` by renaming an existing column.
This is a no-op if schema doesn't contain the given column name.

:param existing: string, name of the existing column to rename.
:param new: string, new name of the column.

>>> df.withColumnRenamed('age', 'age2').collect()
[Row(age2=2, name='Alice'), Row(age2=5, name='Bob')]

.. versionadded:: 1.3

### ``withWatermark``

Description:
Defines an event time watermark for this :class:`DataFrame`. A watermark tracks a point
in time before which we assume no more late data is going to arrive.

Spark will use this watermark for several purposes:
  - To know when a given time window aggregation can be finalized and thus can be emitted
when using output modes that do not allow updates.

  - To minimize the amount of state that we need to keep for on-going aggregations.

The current watermark is computed by looking at the `MAX(eventTime)` seen across
all of the partitions in the query minus a user specified `delayThreshold`.  Due to the cost
of coordinating this value across partitions, the actual watermark used is only guaranteed
to be at least `delayThreshold` behind the actual event time.  In some cases we may still
process records that arrive more than `delayThreshold` late.

:param eventTime: the name of the column that contains the event time of the row.
:param delayThreshold: the minimum delay to wait to data to arrive late, relative to the
latest record that has been processed in the form of an interval
(e.g. "1 minute" or "5 hours").

.. note:: Evolving

>>> sdf.select('name', sdf.time.cast('timestamp')).withWatermark('time', '10 minutes')
DataFrame[name: string, time: timestamp]

.. versionadded:: 2.1

### ``write``

Description:

Interface for saving the content of the non-streaming :class:`DataFrame` out into external
storage.

:return: :class:`DataFrameWriter`

.. versionadded:: 1.4

### ``writeStream``

Description:

Interface for saving the content of the streaming :class:`DataFrame` out into external
storage.

.. note:: Evolving.

:return: :class:`DataStreamWriter`

.. versionadded:: 2.0
