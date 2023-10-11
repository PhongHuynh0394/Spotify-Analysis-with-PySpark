FROM jupyter/pyspark-notebook:hadoop-3

USER root

WORKDIR /home/jovyan/work

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt
