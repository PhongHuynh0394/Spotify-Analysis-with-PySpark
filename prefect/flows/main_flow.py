from prefect import flow, serve
from ETL_pipeline.bronze_layer import *
from ETL_pipeline.silver_layer import *
from ETL_pipeline.gold_layer import *
from ETL_pipeline.warehouse_layer import *
from Ingest_Mongodb.mongodb_task import *
from resources.spark_io import *
from resources.mongodb_io import *
from datetime import datetime
from pyspark import SparkConf


@flow(name="Ingest MongoDB Atlas flow",
      log_prints=True)
def pipeline_A(batch_size, start_index=None):
    """Ingest data from raw source to MongoDB Atlas"""

    # Crawling artist names if not found
    artists = crawling_artist()

    ingest_Mongodb(artists, batch_size, start_index)


def getMongoAuth():
    user = os.getenv("MONGODB_USER")
    password = os.getenv("MONGODB_PASSWORD")
    cluster = os.getenv("MONGODB_SRV")
    cluster = cluster.split("//")[-1]
    return f"mongodb+srv://{user}:{password}@{cluster}/?retryWrites=true&w=majority"


@flow(name="ETL flow",
      log_prints=True)
def pipeline_B():
    """ETL pipeline with pyspark"""
    uri = getMongoAuth()
    conf = (SparkConf().setAppName("ETL-app-{}".format(datetime.today()))
            .set("spark.executor.memory", "4g")
            # .set("spark.driver.memory", "2g")
            .set("spark.mongodb.read.connection.uri", uri)
            .set("spark.mongodb.write.connection.uri", uri)
            .set("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.2.1")
            .setMaster("local[*]")
            )
    with SparkIO(conf) as spark:
        # Bronze task
        with MongodbIO() as client:
            IngestHadoop(client, uri, spark, return_state=True)

        # Silver task
        silver_artist, silver_genre, silver_tracks, silver_tracks_feat, silver_albums = Silverlayer(
            spark)
        silver_data = {"artists": silver_artist,
                       "genres": silver_genre,
                       "tracks": silver_tracks,
                       "tracks_feat": silver_tracks_feat,
                       "albums": silver_albums}

        # Gold layer
        gold_artist, gold_genre, gold_album, gold_track, gold_track_feat = Goldlayer(silver_data)

        # Warehouse layer
        searchs_table = warehouse_search_task(gold_artist, gold_genre, gold_album, gold_track, gold_track_feat)
        feature_matrix = warehouse_model_task(searchs_table)



if __name__ == "__main__":
    pipeline_A = pipeline_A.to_deployment(name='Ingest data MongoDB deployment',
                                          tags=['Ingest data',
                                                'MongoDB Atlas'],
                                          parameters={"batch_size": 5,
                                                      "start_index": None
                                                      }
                                          #   ,interval=125
                                          )

    pipeline_B = pipeline_B.to_deployment(name='Pipeline ETL deployment',
                                          tags=['ETL'])

    serve(pipeline_A, pipeline_B)
