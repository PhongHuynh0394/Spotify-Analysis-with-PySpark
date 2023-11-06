from prefect import flow, serve
from sample_task import *
from ELT_pipeline.bronze_layer import *
from Ingest_Mongodb.mongodb_task import *
from datetime import datetime
from pyspark.sql import SparkSession


@flow(name="Ingest MongoDB Atlas flow", 
      log_prints=True)
def pipeline_A():
    """Ingest data from raw source to MongoDB Atlas"""
    ingest_Mongodb()


@flow(name="ELT flow", 
      log_prints=True) 
def pipeline_B():
    """ELT pipeline with pyspark"""
    # init Spark Session
    spark = (SparkSession.builder 
        .appName("ELT-app-{}".format(datetime.today())) 
        .master('local[*]')  # Run in localmode
        .getOrCreate())

    IngestHadoop(spark)

    spark.stop()



if __name__ == "__main__":
    pipeline_A = pipeline_A.to_deployment(name='Ingest data MongoDB deployment',
                             tags=['Ingest data','MongoDB Atlas'],
                             interval=600)

    pipeline_B = pipeline_B.to_deployment(name='Pipeline ELT deployment',
                             tags=['ELT'])

    serve(pipeline_A, pipeline_B)
