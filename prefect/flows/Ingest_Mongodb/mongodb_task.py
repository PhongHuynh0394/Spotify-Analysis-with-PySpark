from prefect import task
from prefect.tasks import task_input_hash
from resources.mongodb_io import MongodbIO
from .spotify_crawling import core, artists_name_extract
from datetime import datetime, timedelta
import os


@task(name="Crawling Artists name",
      log_prints=True)
def crawling_artist():
    """Crawling artists names"""
    file_path = os.path.abspath(__file__)
    data_dir = os.path.join(os.path.dirname(
        file_path), 'spotify_crawling/data')
    os.makedirs(data_dir, exist_ok=True)  # Make dir if not exist
    art_path = os.path.join(os.path.dirname(file_path),
                            'spotify_crawling/data/artists_names.txt')
    log_path = os.path.join(os.path.dirname(file_path),
                            'spotify_crawling/data/logs.txt')

    # Check whether artists_names.txt existed
    if not os.path.exists(art_path):
        print("artists_name.txt not found")
        print("Start crawling artists_name")
        artists_name_extract.artists_crawler(art_path)
        print(f"Created {art_path}")

    with open(art_path, 'r') as file:
        data = file.read().splitlines()

    # Check whether logs.txt existed
    if not os.path.exists(log_path):
        index_log = 0
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Writing to logs.txt: Create artists_name file at {start_time}")
        with open(log_path, 'w') as file:
            file.write(f"{index_log} {start_time}\n")

    return data


@task(name="crawling Spotify data",
      tags=["MongoDB", "Ingesting data"],
      log_prints=True)
def ingest_Mongodb(artists_names, batch_size: int = 20, start_index=None):
    """Ingest Data to MongoDB using Spotify API"""

    if start_index == None:
        print("Reading logs.txt")

    file_path = os.path.abspath(__file__)
    log_path = os.path.join(os.path.dirname(file_path),
                            'spotify_crawling/data/logs.txt')
    custom_run = True
    with open(log_path, 'a+') as file:
        file.seek(0)
        # Check empty

        content = file.read()
        if not content.strip():
            init_index = 0
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{init_index} {start_time}\n")

        file.seek(0)

        log_data = file.readlines()[-1].strip().split()

        if start_index == None:
            start_index = int(log_data[0])
            custom_run = False

        if (start_index >= len(artists_names) and not custom_run) or (start_index == len(artists_names) and custom_run):
            print("Everything is up to date!")
            return

        elif start_index > len(artists_names) and custom_run:
            raise Exception("Invalid start index")

        end_index = start_index + batch_size

        if end_index >= len(artists_names):
            end_index = len(artists_names)

        print(f"Incremental load from index {start_index} to {end_index}")

        with MongodbIO() as client:
            try:
                core.spotify_crawler(client, artists_names,
                                     start_index, end_index)
            except Exception:
                raise Exception

        if not custom_run:
            print("Updating logs.txt")
            track_time = datetime.now()
            track_time = track_time.strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{end_index} {track_time}\n")
