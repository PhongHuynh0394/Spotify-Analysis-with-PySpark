from prefect import task, flow
import pandas as pd
from prefect.tasks import task_input_hash
from datetime import timedelta
from pymongo.mongo_client import MongoClient
from resources.mongodb_io import MongodbIO
import os


@task
def ingest_Mongodb():
    """Ingest Data to MongoDB using Spotify API"""
    pass

@flow
def ingest_MongoDB_flow():
    pass
