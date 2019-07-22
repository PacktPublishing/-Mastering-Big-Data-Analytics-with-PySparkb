# -Mastering-Big-Data-Analytics-with-PySpark-V-

Mastering Big Data Analytics with PySpark, published by Packt

## To build this image

```docker build --rm -f "Dockerfile" -t mastering_pyspark_ml:latest```

## To run this image

```docker run  -v /path/to/mastering_pyspark_ml/repo/notebooks:/home/jovyan/mastering_pyspark_ml -p 8888:8888 -p 4040:4040 -p 4041:4041 -p 4042:4042 -p 4043:4043 -p 4044:4044 -p 4045:4045 -p 4046:4046 -p 4047:4047 -p 4048:4048 -p 4049:4049 --name mastering_pyspark_ml mastering_pyspark_ml```

## To open Jupyter lab once docker image is running

[http://localhost:8888/lab](http://localhost:8888/lab?token=masteringpysparkml)
