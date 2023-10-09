FROM jupyter/pyspark-notebook:hadoop-3

WORKDIR /home/jovyan/work

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt
