# Script author Danny Meijer - 2019

# This Dockerfile is based on the jupyter distributed and maintained pyspark-notebook
# Github link: https://github.com/jupyter/docker-stacks/blob/master/pyspark-notebook/Dockerfile
# Original copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# This Docker image simply extends the pyspark-notebook with the following additions:
#  - enables Jupyter Lab by default
#  - exposes correct ports for JupyterLab and SparkUI
#  - with current port setup, SparkUI supports up to ten consecutive Spark applications

# Although generally considered bad practice, I have opted to hard EXPOSE the ports between
# host and container. This is done solely because of me expacted this container to be used
# by Docker novices that might not know exactly how port bindings work. The intend of this
# container is to be able to follow along the PySpark tutorials that I have provided, and
# not to teach one how to use Docker.

FROM jupyter/pyspark-notebook:d4cbf2f80a2a
LABEL maintainer="Danny Meijer <chilltake@gmail.com>"
ARG VERSION='20190708'

# Maintain last refresh date as version - for simple version control
LABEL version=${VERSION}
ENV VERSION ${VERSION}

# Install blackcellmagic. Python plugin for formatting Python code
RUN pip install blackcellmagic
# To load:
# %load_ext blackcellmagic
# To run (once loaded):
# %%black

# Enable Jupyter Lab
ENV SPARK_JUPYTER_ENABLE_LABHOME yes

# # Disable Notebook App Token
ENV JUPYTER_TOKEN 'masteringpysparkml'

## Exposing neccesary ports
# Jupyter Lab
EXPOSE 8888
# SparkUI ports
EXPOSE 4040
EXPOSE 4041
EXPOSE 4042
EXPOSE 4043
EXPOSE 4044
EXPOSE 4045
EXPOSE 4046
EXPOSE 4047
EXPOSE 4048
EXPOSE 4049

