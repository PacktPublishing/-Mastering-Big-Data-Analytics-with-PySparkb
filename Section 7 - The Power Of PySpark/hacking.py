from pyspark.sql import DataFrame


def available_class_methods(cls):
    _methods = {
        # Key: name of the Class Method
        k:
        # Value: docstring belonging to the Class Method, formatted for readability
        "\n".join(
            "".join(getattr(DataFrame, k).__doc__).replace("    ", "").split("\n")
        )
        # Iterator
        for k in dict(cls.__dict__)
        if "__" not in k
    }
    return _methods


dataframe_methods_raw = available_class_methods(DataFrame)
dataframe_methods = list(dataframe_methods_raw.keys())
dataframe_methods.sort()

print("# DataFrame Class Methods")

for x in dataframe_methods:
    print()
    print("## ``" + x + "``")
    print()
    print("Description:")
    print(dataframe_methods_raw[x])
