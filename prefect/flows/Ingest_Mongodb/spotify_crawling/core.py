from .spotify_api_auth import get_token as spotify_get_token, get_auth_header as spotify_get_auth_header
from .spotify_scrapper import SpotifyCrawler
from .mongodb_process import MongoDB
import os


def spotify_crawler(client, artists_name, start_index=0, end_index=20):
    # Begin
    print("Start Crawling...")

    # Authentication
    try:
        spotify_access_token, spotify_token_type = spotify_get_token()
        spotify_headers = spotify_get_auth_header(
            spotify_token_type, spotify_access_token)
    except Exception:
        raise Exception("Invalid Token")

    # Initialize Spotify Scrapper
    sc = SpotifyCrawler(spotify_headers)

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
        except Exception as e:
            raise e

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

    # Insert data
    mongodb.insert_many(final_artists_information, db=crawling_data,
                        coll=artists_data)
    mongodb.insert_many(final_albums_information, db=crawling_data,
                        coll=albums_data)
    mongodb.insert_many(final_tracks_information, db=crawling_data,
                        coll=tracks_data)
    mongodb.insert_many(final_tracks_features_information, db=crawling_data,
                        coll=tracks_features_data)

    # End
    print("Done")
