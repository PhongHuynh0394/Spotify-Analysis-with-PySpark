import os
from pymongo.mongo_client import MongoClient
from prefect import task
from prefect.tasks import task_input_hash
from datetime import datetime, timedelta
from prefect.task_runners import ConcurrentTaskRunner
from pyspark.sql import SparkSession
from pyspark.sql.types import *

@task(name="bronze_layer_task",
      description="Extract data from MongoDB to HDFS at bronze layer",
      cache_key_fn=task_input_hash, 
      cache_expiration=timedelta(hours=1),
      task_run_name="bronze_{table_name}",
      tags=["bronze layer", "pyspark"])
def bronze_layer_task(collection , spark: 'pyspark.sql.SparkSession', table_name: str) -> None:
    """Extract data from MongoDB to HDFS at bronze layer"""
    hdfs_uri = f"hdfs://namenode:8020/bronze_layer/{table_name}"

    mongo_data = pd.DataFrame(list(collection.find({}, {"_id": 0}))) # eliminate the _id field
    spark_data = spark.createDataFrame(mongo_data, schema=mongo_data.columns.tolist())
    try:
        spark_data.write.parquet(hdfs_uri, mode="overwrite")
        print(f"Bronze: Successfully push {table_name}.parquet")
    except Exception as e:
        print(f"Error: {e}")


@flow(name="Ingest Hadoop from MongoDB flow",
        task_runners=ConcurrentTaskRunner())
def IngestHadoop():
    """Extract data From MongoDb and Load to HDFS"""
    # Connect with MongoDB Atlas
    user = os.getenv("MONGODB_USER")
    password = os.getenv("MONGODB_PASSWORD")
    database_name = 'testDB'
    uri = f"mongodb+srv://{user}:{password}@python.zynpktu.mongodb.net/?retryWrites=true&w=majority"

    mongo_client = MongoClient(uri)
    mongo_db = mongo_client[database_name]
    collections = mongo_db.list_collection_names() #get all collections

    # init Spark Session
    spark = (SparkSession.builder 
        .appName("ELT-app-{}".format(datetime.today())) 
        .master('local[*]')  # Run in localmode
        .getOrCreate())

    #Running task concurrently
    for collection in collections:
        bronze_layer_task.submit(mongo_db[collection], spark, collection) #collection is also the name of table
