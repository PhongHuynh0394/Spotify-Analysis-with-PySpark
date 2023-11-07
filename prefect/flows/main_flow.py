from prefect import flow, serve
from sample_task import *
from ELT_pipeline.bronze_layer import *
from Ingest_Mongodb.mongodb_task import *
from resources.spark_io import *
from resources.mongodb_io import *
from datetime import datetime
# from pyspark.sql import SparkSession
from pyspark import SparkConf


@flow(name="Ingest MongoDB Atlas flow", 
      log_prints=True)
def pipeline_A():
    """Ingest data from raw source to MongoDB Atlas"""
    ingest_MongoDB_flow()


@flow(name="ELT flow", 
      log_prints=True) 
def pipeline_B():
    """ELT pipeline with pyspark"""

    conf = (SparkConf().setAppName("ELT-app-{}".format(datetime.today()))
            .setMaster("local[*]"))

    with SparkIO(conf) as spark:
        IngestHadoop(spark)


if __name__ == "__main__":
    pipeline_A = pipeline_A.to_deployment(name='Ingest data MongoDB deployment',
                             tags=['Ingest data','MongoDB Atlas'],
                             interval=600)

    pipeline_B = pipeline_B.to_deployment(name='Pipeline ELT deployment',
                             tags=['ELT'])

    serve(pipeline_A, pipeline_B)
