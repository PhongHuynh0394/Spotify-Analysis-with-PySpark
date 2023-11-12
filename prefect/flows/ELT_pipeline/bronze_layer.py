from pymongo.mongo_client import MongoClient
from prefect import task, flow
from prefect.tasks import task_input_hash
from datetime import datetime, timedelta
from prefect.task_runners import ConcurrentTaskRunner
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pandas as pd
from resources.mongodb_io import MongodbIO

def createSchema(df: pd.DataFrame):
    """This function create Pyspark Schema"""
    field = []

    for col in df.columns:
        dtype = str(df[col].dtype)

        if dtype == 'object':
            field_type = StringType()
        elif 'int' in dtype:
            field_type = IntegerType()
        elif 'bool' in dtype: 
            field_type = BooleanType()
        elif 'float' in dtype: 
            field_type = FloatType()
        elif dtype == 'double':
            field_type = DoubleType()
        else:
            field_type = StringType()
        
        field.append(StructField(col, field_type, True))

    return StructType(field)

@task(name="bronze_layer_task",
      description="Extract data from MongoDB to HDFS at bronze layer",
      cache_key_fn=task_input_hash, 
      cache_expiration=timedelta(hours=1),
      task_run_name="bronze_{table_name}",
      tags=["bronze layer", "pyspark"])
def bronze_layer_task(collection, spark: SparkSession, table_name: str) -> None:
    """Extract data from MongoDB to HDFS at bronze layer"""

    hdfs_uri = f"hdfs://namenode:8020/bronze_layer/{table_name}.parquet"
    mongo_data = pd.DataFrame(list(collection.find({}, {"_id": 0}))) # eliminate the _id field

    try:
        spark_data = spark.createDataFrame(mongo_data, schema=mongo_data.columns.tolist())
    except Exception as e:
        print(f"Error to Create Spark DataFrame {table_name} {e}")
        print(f"Start Create Schema for {table_name}")

        schema = createSchema(mongo_data)
        spark_data = spark.createDataFrame(mongo_data, schema=schema)

    print(f"Writing {table_name}")
    spark_data.write.parquet(hdfs_uri, mode="overwrite")
    print(f"Bronze: Successfully push {table_name}.parquet")


@flow(name="Ingest Hadoop from MongoDB flow",
      task_runner=ConcurrentTaskRunner(),
      log_prints=True)
def IngestHadoop(spark: SparkSession):
    """Extract data From MongoDb and Load to HDFS"""

    database_name = "crawling_data"

    with MongodbIO() as client:
        mongo_db = client[database_name] 
        collections = mongo_db.list_collection_names() #get all collectons

        #Running task concurrently
        for collection in collections:
            print(f"{collection} start being Ingested...")
            future = bronze_layer_task.submit(mongo_db[collection], spark, collection) #collection is also the name of table
            future.wait()
            
