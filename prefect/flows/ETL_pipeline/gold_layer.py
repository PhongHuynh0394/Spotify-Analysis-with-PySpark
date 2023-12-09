from prefect import task, flow
from prefect.tasks import task_input_hash
from datetime import datetime, timedelta
from prefect.task_runners import ConcurrentTaskRunner
from pyspark.sql.types import *
from .utils.layer_utils import GoldCleanDataframe as gold 
import pyspark

@task(name="gold artists task")
def gold_artist_task(silver_artists: pyspark.sql.DataFrame) -> None:
    """Cleaning silver artist table

    return: None
    """
    table_name = 'gold_artists'
    hdfs_uri = f"hdfs://namenode:8020/gold_layer/{table_name}.parquet"

    gold_artists = gold(df=silver_artists,
                        drop_duplicate=True,
                        drop_null=True,
                        drop_columns=["href", "images", "type", "uri"]).clean()

   # Write backup
    print(f'Start writing {table_name}.parquet')
    gold_artists.write.parquet(hdfs_uri, mode='overwrite')
    print(f'Gold: Successfully writing {gold_artists.count()} into {table_name}')


@task(name="gold genres task")
def gold_genres_task(silver_genres: pyspark.sql.DataFrame) -> None:
    """Cleaning silver albums table

    return: None
    """
    table_name = 'gold_genres'
    hdfs_uri = f"hdfs://namenode:8020/gold_layer/{table_name}.parquet"

    gold_genres = gold(df=silver_genres,
                        drop_duplicate=True,
                        drop_null=True).clean()


   # Write backup
    print(f'Start writing {table_name}.parquet')
    gold_genres.write.parquet(hdfs_uri, mode='overwrite')
    print(f'Gold: Successfully writing {gold_genres.count()} into {table_name}')


@task(name="gold albums task")
def gold_albums_task(silver_albums: pyspark.sql.DataFrame) -> None:
    """Cleaning silver albums table

    return: None
    """
    table_name = 'gold_albums'
    hdfs_uri = f"hdfs://namenode:8020/gold_layer/{table_name}.parquet"

    gold_albums= gold(df=silver_albums,
                        drop_duplicate=True,
                        drop_null=True,
                        drop_columns=["copyrights", "external_ids", "genres", "href", "images", "type", "uri"]).clean()

   # Write backup
    print(f'Start writing {table_name}.parquet')
    gold_albums.write.parquet(hdfs_uri, mode='overwrite')
    print(f'Gold: Successfully writing {gold_albums.count()} into {table_name}')


@task(name="gold tracks task")
def gold_tracks_task(silver_tracks: pyspark.sql.DataFrame) -> None:
    """Cleaning silver tracks table

    return: None
    """
    table_name = 'gold_tracks'
    hdfs_uri = f"hdfs://namenode:8020/gold_layer/{table_name}.parquet"

    gold_tracks = gold(df=silver_tracks,
                        drop_duplicate=True,
                        drop_null=True,
                        drop_columns=["duration_ms", "external_ids", "href", "is_local", "type", "uri"]).clean()

   # Write backup
    print(f'Start writing {table_name}.parquet')
    gold_tracks.write.parquet(hdfs_uri, mode='overwrite')
    print(f'Gold: Successfully writing {gold_tracks.count()} into {table_name}')



@task(name="gold track's features task")
def gold_tracks_feat_task(silver_tracks_features: pyspark.sql.DataFrame) -> None:
    """Cleaning silver track's features table

    return: None
    """
    table_name = 'gold_tracks_features'
    hdfs_uri = f"hdfs://namenode:8020/gold_layer/{table_name}.parquet"

    gold_tracks_features = gold(df=silver_tracks_features,
                        drop_duplicate=True,
                        drop_null=True,
                        drop_columns=["type", "uri", "track_href", "analysis_url"]).clean()

   # Write backup
    print(f'Start writing {table_name}.parquet')
    gold_tracks_features.write.parquet(hdfs_uri, mode='overwrite')
    print(f'Gold: Successfully writing {gold_tracks_features.count()} into {table_name}')

@flow(name="Gold layer",
      task_runner=ConcurrentTaskRunner(),
      log_prints=True)
def Goldlayer(silver_data) -> None:
    """Gold layer"""
    gold_artist_task.submit(silver_data['artists'])
    gold_genres_task.submit(silver_data['genres'])
    gold_albums_task.submit(silver_data['albums'])
    gold_tracks_task.submit(silver_data['tracks'])
    gold_tracks_feat_task.submit(silver_data['tracks_feat'])

