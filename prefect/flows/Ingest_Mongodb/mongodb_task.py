from prefect import task, flow
import pandas as pd
from prefect.tasks import task_input_hash
from datetime import timedelta
from pymongo import MongoClient
from resources.mongodb_io import MongodbIO
from .spotify_crawling import core
import os


@task(name="crawling Spotify data",
      tags=["MongoDB", "Ingesting data"])
def ingest_Mongodb():
    """Ingest Data to MongoDB using Spotify API"""

    with MongodbIO() as client:
        try:
            core.spotify_crawler(client, 0, 20, 4)
        except Exception:
            raise Exception

@flow(name="Ingest MongoDB flow",
      log_prints=True)
def ingest_MongoDB_flow():
    ingest_Mongodb()
