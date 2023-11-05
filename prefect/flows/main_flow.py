from prefect import flow, serve
from sample_task import *
from ELT.bronze_layer import *
from Ingest_Mongodb.mongodb_task import *
from datetime import datetime
from pyspark import SparkContext
from pyspark.sql import SparkSession, SQLContext


@flow(name="Ingest MongoDB Atlas flow", 
      log_prints=True)
def pipeline_A():
    """Ingest data from raw source to MongoDB Atlas"""
    ingest_Mongodb()


@flow(name="ELT flow", 
      log_prints=True) 
def pipeline_B():
    """ELT pipeline with pyspark"""
    IngestHadoop()



if __name__ == "__main__":
    pipeline_A = pipeline_A.to_deployment(name='Ingest data MongoDB deployment',
                             tags=['Ingest data','MongoDB Atlas'],
                             interval=600)

    pipeline_B = pipeline_B.to_deployment(name='Pipeline ELT deployment',
                             tags=['ELT'])

    serve(pipeline_A, pipeline_B)
