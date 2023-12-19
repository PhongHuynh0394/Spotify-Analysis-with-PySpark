import os
from prefect import task, flow
from prefect.tasks import task_input_hash
from datetime import datetime, timedelta
from prefect.task_runners import ConcurrentTaskRunner
from pyspark.sql import SparkSession
from pyspark.sql.types import *

def getSchema(table_name):
    """This function create Pyspark Schema"""
    artist_schema = StructType([
        StructField("_id", StringType(), True),
        StructField(
            "external_urls",
            StructType([
                StructField("spotify", StringType(), True)
            ])
        ),
        StructField(
            "followers", 
            StructType([
                StructField("href", StringType(), True),
                StructField("total", IntegerType(), True)
            ])
        ),
        StructField(
            "genres",
            ArrayType(StringType(), True)      
        ),
        StructField("href", StringType(), True),
        StructField("id", StringType(), True),
        StructField(
            "images",
            ArrayType(
                StructType([
                    StructField("height", IntegerType(), True),
                    StructField("url", StringType(), True),
                    StructField("width", IntegerType(), True)
                ])
            )
        ),
        StructField("name", StringType(), True),
        StructField("popularity", IntegerType(), True),
        StructField("type", StringType(), True),
        StructField("uri", StringType(), True)
    ])

    album_schema = StructType([
        StructField("_id", StringType(), True),
        StructField("album_type", StringType(), True),
        StructField(
            "copyrights",
            ArrayType(
                StructType([
                    StructField("text", StringType(), True),
                    StructField("type", StringType(), True)
                ])
            )
        ),
        StructField(
            "external_ids",
            StructType([
                StructField("upc", StringType(), True)
            ])
        ),
        StructField(
            "external_urls",
            StructType([
                StructField("spotify", StringType(), True)
            ])
        ),
        StructField(
            "genres",
            ArrayType(StringType(), True)
        ),
        StructField("href", StringType(), True),
        StructField("id", StringType(), True),
        StructField(
            "images",
            ArrayType(
                StructType([
                    StructField("height", IntegerType(), True),
                    StructField("url", StringType(), True),
                    StructField("width", IntegerType(), True)
                ])
            )
        ),
        StructField("label", StringType(), True),
        StructField("name", StringType(), True),
        StructField("popularity", IntegerType(), True),
        StructField("release_date", StringType(), True),
        StructField("release_date_precision", StringType(), True),
        StructField("total_tracks", IntegerType(), True),
        StructField("type", StringType(), True),
        StructField("uri", StringType(), True),
        StructField("artist_id", StringType(), True)
    ])

    track_schema = StructType([
        StructField("_id", StringType(), True),
        StructField("disc_number", IntegerType(), True),
        StructField("duration_ms", LongType(), True),
        StructField("explicit", BooleanType(), True),
        StructField(
            "external_ids",
            StructType([
                StructField("isrc", StringType(), True)
            ])
        ),
        StructField(
            "external_urls",
            StructType([
                StructField("spotify", StringType(), True)
            ])
        ),
        StructField("href", StringType(), True),
        StructField("id", StringType(), True),
        StructField("is_local", BooleanType(), True),
        StructField("name", StringType(), True),
        StructField("popularity", IntegerType(), True),
        StructField("preview_url", StringType(), True),
        StructField("track_number", IntegerType(), True),
        StructField("type", StringType(), True),
        StructField("uri", StringType(), True),
        StructField("artist_id", StringType(), True),
        StructField("album_id", StringType(), True)
    ])

    track_features_schema = StructType([
        StructField("_id", StringType(), True),
        StructField("danceability", DoubleType(), True),
        StructField("energy", DoubleType(), True),
        StructField("key", IntegerType(), True),
        StructField("loudness", DoubleType(), True),
        StructField("mode", IntegerType(), True),
        StructField("speechiness", DoubleType(), True),
        StructField("acousticness", DoubleType(), True),
        StructField("instrumentalness", DoubleType(), True),
        StructField("liveness", DoubleType(), True),
        StructField("valence", DoubleType(), True),
        StructField("tempo", DoubleType(), True),
        StructField("type", StringType(), True),
        StructField("id", StringType(), True),
        StructField("uri", StringType(), True),
        StructField("track_href", StringType(), True),
        StructField("analysis_url", StringType(), True),
        StructField("duration_ms", LongType(), True),
        StructField("time_signature", IntegerType(), True)
    ])
    if 'artist' in table_name:
        return artist_schema
    elif 'album' in table_name:
        return album_schema
    elif 'feature' in table_name:
        return track_features_schema
    else:
        return track_schema

@task(name="bronze_layer_task",
      description="Extract data from MongoDB to HDFS at bronze layer",
      cache_key_fn=task_input_hash, 
      cache_expiration=timedelta(hours=1),
      task_run_name="bronze_{table_name}",
      tags=["bronze layer", "pyspark"])
def bronze_layer_task(spark: SparkSession, mongo_uri: str, database_name: str, table_name: str) -> None:
    """Extract data from MongoDB to HDFS at bronze layer"""

    hdfs_uri = f"hdfs://namenode:8020/bronze_layer/{table_name}.parquet"

    spark_data = (spark.read.format("mongodb")
              .schema(getSchema(table_name))
              .option("uri", mongo_uri)
              .option('database', database_name)
              .option('collection', table_name)
              .load()
              .select([col for col in getSchema(table_name).fieldNames() if col != '_id'])
              )

    print(f"Writing {table_name}")
    spark_data.write.parquet(hdfs_uri, mode="overwrite")
    print(f"Bronze: Successfully writing {table_name}.parquet")



@flow(name="Ingest Hadoop from MongoDB flow",
      task_runner=ConcurrentTaskRunner(),
      log_prints=True)
def IngestHadoop(client, uri, spark: SparkSession):
    """Extract data From MongoDB and Load to HDFS"""

    database_name = os.getenv("MONGODB_DATABASE")
    mongo_db = client[database_name] 
    collections = mongo_db.list_collection_names() #get all collectons

    #Running task concurrently
    for collection in collections:
        print(f"{collection} start being Ingested...")
        future = bronze_layer_task.submit(spark, uri, database_name, collection) #collection is also the name of table
    print("Done")
