from prefect import task, flow, runtime
import pandas as pd
from prefect.tasks import task_input_hash
from datetime import timedelta
from pymongo import MongoClient
from resources.mongodb_io import MongodbIO
from .spotify_crawling import core, artists_name_extract 
from math import ceil 
import os

@task(name="Crawling Artists name",
      log_prints=True)
def crawling_artist():
    '''Crawling artists names'''
    file_path = os.path.abspath(__file__)
    path = os.path.join(os.path.dirname(file_path), 'spotify_crawling/data/artists_names.txt')

    if not os.path.exists(path):
        print("artists_name.txt not found")
        print("Start crawling artists_name")
        artists_name_extract.artists_crawler(path)
        print(f"Created {path}")

    with open(path, 'r') as file:
        data = file.read().splitlines()

    return data


@task(name="crawling Spotify data",
      tags=["MongoDB", "Ingesting data"],
      log_prints=True)
def ingest_Mongodb(artists_names, start_index = 0, end_index = 20, threads = 4):
    """Ingest Data to MongoDB using Spotify API"""

    with MongodbIO() as client:
        try:
            core.spotify_crawler(client,artists_names, start_index, end_index, threads)
        except Exception:
            raise Exception


def generate_flowrun_name():
    params = runtime.flow_run.parameters

    end = params['end_index']
    start = params['start_index']

    batch_num = ceil(end / (end - start))
    return f"batch {str(batch_num)}"


@flow(name="Ingest MongoDB flow",
      flow_run_name=generate_flowrun_name,
      log_prints=True)
def ingest_MongoDB_flow(artists_names, start_index, end_index, threads):
    ingest_Mongodb(artists_names, start_index, end_index, threads)

