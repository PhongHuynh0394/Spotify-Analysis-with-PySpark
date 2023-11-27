from prefect import flow, serve
from sample_task import *
from ETL_pipeline.bronze_layer import *
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


@flow(name="ETL flow",
      log_prints=True)
def pipeline_B():
    """ETL pipeline with pyspark"""

    conf = (SparkConf().setAppName("ETL-app-{}".format(datetime.today()))
            .set("spark.executor.memory", "2g")
            .setMaster("local[*]"))

    with SparkIO(conf) as spark:
        # Bronze task
        with MongodbIO() as client:
            IngestHadoop(client, spark, return_state=True)

        # Silver task


if __name__ == "__main__":
    pipeline_A = pipeline_A.to_deployment(name='Ingest data MongoDB deployment',
                                          tags=['Ingest data',
                                                'MongoDB Atlas'],
                                          parameters={"batch_size": 50,
                                                      "start_index": None
                                                      }
                                          # interval=2700
                                          )

    pipeline_B = pipeline_B.to_deployment(name='Pipeline ETL deployment',
                                          tags=['ETL'])

    serve(pipeline_A, pipeline_B)
