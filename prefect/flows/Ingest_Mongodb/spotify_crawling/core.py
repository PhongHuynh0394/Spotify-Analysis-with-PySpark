from .spotify_api_auth import SpotifyAuth
from .spotify_scrapper import SpotifyCrawler
from .mongodb_process import MongoDB
from .rate_limit_exception import RateLimitException
import os
import threading


def pushing_data_to_mongodb(mongo, data, db, coll, tag):
    print(f"Pushing {tag}: {len(data)} ")
    mongo.insert_many(data, db, coll)


def spotify_crawler(client, artists_name, start_index=0, end_index=20):
    # Begin
    print("Start Crawling...")

    # Authentication
    try:
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        sa = SpotifyAuth(client_id, client_secret)
    except Exception:
        raise Exception("Invalid Token")

    # Initialize Spotify Scrapper
    sc = SpotifyCrawler(sa)

    if start_index < 0 or start_index >= len(artists_name):
        raise Exception("Invalid start index")
    elif start_index > end_index:
        raise Exception("Invalid start and end index")
    elif end_index > len(artists_name):
        raise Exception("Invalid end index")
    else:
        try:
            final_artists_information, final_albums_information, final_tracks_information, final_tracks_features_information = sc.get_all_information_from_artists(
                artists_name[start_index:end_index])
        except RuntimeError:
            raise Exception("Max retry attempts reached!")

    # Initialize MongoDB
    mongodb = MongoDB(client)

    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")
    # # Create database

    print("Pusing raw data to Mongodb ...")

    crawling_data = mongodb.create_database(db_name=MONGODB_DATABASE)

    # Create collections
    artists_data = mongodb.create_collection(
        collection_name="artists_data", db=crawling_data)
    albums_data = mongodb.create_collection(
        collection_name="albums_data", db=crawling_data)
    tracks_data = mongodb.create_collection(
        collection_name="tracks_data", db=crawling_data)
    tracks_features_data = mongodb.create_collection(
        collection_name="tracks_features_data", db=crawling_data)

    # Use multithreading to push data to mongodb
    threads = []
    threads.extend([
        threading.Thread(target=pushing_data_to_mongodb, args=(
            mongodb, final_artists_information, crawling_data, artists_data, "artists data")),
        threading.Thread(target=pushing_data_to_mongodb, args=(
            mongodb, final_albums_information, crawling_data, albums_data, "albums data")),
        threading.Thread(target=pushing_data_to_mongodb, args=(
            mongodb, final_tracks_information, crawling_data, tracks_data, "tracks data")),
        threading.Thread(target=pushing_data_to_mongodb, args=(
            mongodb, final_tracks_features_information, crawling_data, tracks_features_data, "tracks features data"))
    ])

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # End
    print("Done")
