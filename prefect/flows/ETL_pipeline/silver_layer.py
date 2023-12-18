from prefect import task, flow
from prefect.tasks import task_input_hash
from datetime import datetime, timedelta
from prefect.task_runners import ConcurrentTaskRunner
from pyspark.sql.types import *
from .utils.layer_utils import SilverCleanDataframe as silver
from pyspark.sql import SparkSession
from pyspark.sql.functions import col


@task(name="silver_layer_task",
      description="Extract data from MongoDB to HDFS at bronze layer",
      # cache_key_fn=task_input_hash, 
      # cache_expiration=timedelta(hours=1),
      task_run_name="silver_{table_name}")
def silver_artists_task(spark: SparkSession, table_name: str = 'artists_data'):
    """Cleaning Artist table
    
    return: artist table, genre 
    """

    hdfs_uri = f"hdfs://namenode:8020/bronze_layer/{table_name}.parquet"

    print('Getting artist data from HDFS')
    artists_data = spark.read.parquet(hdfs_uri, inferSchema=True, header=True)

    print('Start Transforming')
    silver_artists, silver_genres = silver(df=artists_data,
                                    nested_columns={"external_urls": col("external_urls.spotify"), 
                                                    "followers": col("followers.total"),
                                                    "image_url": col("images")[0].url},
                                    list_value_columns={"genres": "genre"},
                                    remove_old_list_value_columns=True,
                                    split_df=True,
                                    column_to_split="genre",
                                    primary_foreign_key="id").clean()

    # Writing to HDFS
    tables = {'silver_artists': silver_artists, 'silver_genres': silver_genres}
    for table, df in tables.items():
        target_uri = f"hdfs://namenode:8020/silver_layer/{table}.parquet"
        print(f"Start Writing {table}.parquet")
        df.write.parquet(target_uri, mode="overwrite")
        print(f"Silver: Successfully writing {table}.parquet")

    # return tables
    return silver_artists, silver_genres

@task(name="silver Track's Features task",
      task_run_name="silver_{table_name}")
def silver_tracks_feat_task(spark, table_name: str = 'tracks_features_data'):
    """Cleaning Track's features table
    
    return: clean tracks feature table
    """

    hdfs_uri = f"hdfs://namenode:8020/bronze_layer/{table_name}.parquet"

    print('Getting tracks features data from HDFS')
    tracks_feat_data = spark.read.parquet(hdfs_uri, inferSchema=True, header=True)

    print('Start Transforming')
    silver_tracks_feat = silver(df=tracks_feat_data).clean()

    # Writing to HDFS
    target_uri = f"hdfs://namenode:8020/silver_layer/silver_tracks_features.parquet"

    print(f"Start Writing silver_tracks_features.parquet")
    silver_tracks_feat.write.parquet(target_uri, mode="overwrite")
    print(f"Silver: Successfully writing silver_tracks_features.parquet")

    return silver_tracks_feat

@task(name="silver Tracks task",
      task_run_name="silver_{table_name}")
def silver_tracks_task(spark, table_name: str = 'tracks_data'):
    """Cleaning Tracks table
    
    return: clean tracks table
    """

    hdfs_uri = f"hdfs://namenode:8020/bronze_layer/{table_name}.parquet"

    print('Getting tracks data from HDFS')
    tracks_data = spark.read.parquet(hdfs_uri, inferSchema=True, header=True)

    print('Start Transforming')
    silver_tracks= silver(df=tracks_data,
                            nested_columns={"external_urls": col("external_urls.spotify")}).clean()

    # Writing to HDFS
    target_uri = f"hdfs://namenode:8020/silver_layer/silver_tracks.parquet"

    print(f"Start Writing silver_tracks.parquet")
    silver_tracks.write.parquet(target_uri, mode="overwrite")
    print(f"Silver: Successfully writing silver_tracks.parquet")

    return silver_tracks


@task(name="silver Albums task",
      task_run_name="silver_{table_name}")
def silver_albums_task(spark, table_name: str = 'albums_data'):
    """Cleaning Albums table
    
    return: clean Albums table
    """

    hdfs_uri = f"hdfs://namenode:8020/bronze_layer/{table_name}.parquet"

    print('Getting albums data from HDFS')
    albums_data = spark.read.parquet(hdfs_uri, inferSchema=True, header=True)

    print('Start Transforming')
    silver_albums = silver(df=albums_data,
                            nested_columns={"external_urls": col("external_urls.spotify"), "image_url": col("images")[0].url}).clean()

    # Writing to HDFS
    target_uri = f"hdfs://namenode:8020/silver_layer/silver_albums.parquet"

    print(f"Start Writing silver_albums.parquet")
    silver_albums.write.parquet(target_uri, mode="overwrite")
    print(f"Silver: Successfully writing silver_albums.parquet")

    return silver_albums

@flow(name="Transforming Silver layer",
      task_runner=ConcurrentTaskRunner(),
      log_prints=True)
def Silverlayer(spark: SparkSession):
    silver_artists, silver_genres = silver_artists_task.submit(spark, 'artists_data').result()
    silver_tracks = silver_tracks_task.submit(spark, 'tracks_data')
    silver_tracks_feat = silver_tracks_feat_task.submit(spark, 'tracks_features_data')
    silver_albums = silver_albums_task.submit(spark, 'albums_data')

    return silver_artists, silver_genres, silver_tracks, silver_tracks_feat, silver_albums

