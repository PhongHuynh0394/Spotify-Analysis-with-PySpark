from prefect import flow, serve
from sample_task import *
from ELT_pipeline.bronze_layer import *
from Ingest_Mongodb.mongodb_task import *
from resources.spark_io import *
from resources.mongodb_io import *
from datetime import datetime
# from pyspark.sql import SparkSession
from pyspark import SparkConf
from math import ceil
from time import sleep


@flow(name="Ingest MongoDB Atlas flow", 
      log_prints=True)
def pipeline_A():
    """Ingest data from raw source to MongoDB Atlas"""
    batch_size = 20 
    threads = 4

    # Crawling artist names if not found 
    artists = crawling_artist()

    num_workflows = ceil(len(artists) / batch_size)

    for i in range(num_workflows):
        start_index = i * batch_size
        end_index = min(start_index + batch_size, len(artists))

        ingest_MongoDB_flow(artists, start_index, end_index, threads)
        sleep_time = 5
        print(f'Sleep in {sleep_time}s')
        sleep(sleep_time)


@flow(name="ELT flow", 
      log_prints=True) 
def pipeline_B():
    """ELT pipeline with pyspark"""

    conf = (SparkConf().setAppName("ELT-app-{}".format(datetime.today()))
            .setMaster("local[*]"))

    with SparkIO(conf) as spark:
        IngestHadoop(spark, return_state=True)


if __name__ == "__main__":
    pipeline_A = pipeline_A.to_deployment(name='Ingest data MongoDB deployment',
                             tags=['Ingest data','MongoDB Atlas']
                             )

    pipeline_B = pipeline_B.to_deployment(name='Pipeline ELT deployment',
                             tags=['ELT'])

    serve(pipeline_A, pipeline_B)
