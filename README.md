# Mastering Big Data Analytics with PySpark

This repository contains the courseware belonging to the course __Mastering Big Data 
 Analytics with PySpark__.   
- Published by:  Packt Publishing
- Author: [Danny Meijer](https://www.linkedin.com/in/dannydatascientist)

Follow the instructions below to download the data belonging to the course as well as 
 setting up your interactive development environment. 

## Downloading Data for this Course

Once you have cloned this repository locally, simply navigate to the folder you have 
 stored the repo in and run:  
```python download_data.py``` 

This will populate the `data-sets` folder in your repo with a number of data sets that 
 will be used throughout the course.

## Docker Image Bundled with the Course

### About

The Docker Image bundled with this course (see `Dockerfile`) is based on the jupyter 
distributed and maintained `pyspark-notebook` 
> [Github link](https://github.com/jupyter/docker-stacks/blob/master/pyspark-notebook/Dockerfile)  
> Original copyright (c) Jupyter Development Team. Distributed under the terms of the 
Modified BSD License.

This Course's Docker image extends the `pyspark-notebook` with the following additions:
- enables Jupyter Lab by default
- exposes correct ports for JupyterLab and SparkUI
- sets numerous default settings to improve Quality of Life for the user
- installs numerous add-ons (such as `pyspark-stubs` and `blackcellmagic`) using 
  `jupyter_contrib_nbextensions`

### Instructions for use

There are 2 ways to access the Docker container in this course:
1. Through the bundled `start_jupyter_lab.py` script (recommended to use)
2. Through the Docker CLI (only for advanced users)

#### Using the bundled script to run the container

The easiest way to run the container that belongs to this course is by running 
 ```python start_jupyter_lab.py``` from the course's repository. This will automatically
 build the Docker image, set up the Docker container, and the necessary volume mounts. 

#### Using Docker CLI

1. __Build the image__  
```docker build --rm -f "Dockerfile" -t mastering_pyspark_ml:latest .```

2. __Run the image__  
Ensure that you replace `/path/to/mastering_pyspark_ml/repo/` in the following command, and run it in a terminal or command prompt:  
```docker run  -v /path/to/mastering_pyspark_ml/repo/:/home/jovyan/ --rm -d -p 8888:8888 -p 4040:4040 -p 4041:4041 --name mastering_pyspark_ml mastering_pyspark_ml .```

3. __Open Jupyter lab once Docker image is running__  
[http://localhost:8888/lab](http://localhost:8888/lab?token=masteringpysparkml)
