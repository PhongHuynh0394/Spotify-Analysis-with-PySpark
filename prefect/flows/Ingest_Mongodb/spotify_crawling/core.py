from .spotify_api_auth import get_token as spotify_get_token, get_auth_header as spotify_get_auth_header
from .spotify_scrapper import SpotifyScrapper, multithreading_processing_on_artist
from .mongodb_process import MongoDB
import os
import pandas as pd

def spotify_crawler(client, artists_name, start_index = 0, end_index = 20, thread_chunk_size = 1):
    # Begin
    print("Start Crawling...")

    # Authentication
    try:
        spotify_access_token, spotify_token_type = spotify_get_token()
        spotify_headers = spotify_get_auth_header(
            spotify_token_type, spotify_access_token)
    except Exception:
        raise Exception
    
        
    # Initialize Spotify Scrapper
    ss = SpotifyScrapper(spotify_headers)

    if start_index < 0 or start_index >= len(artists_name):
        raise Exception("Invalid start index")
    elif start_index > end_index:
        raise Exception("Invalid start and end index")
    elif end_index > len(artists_name):
        raise Exception("Invalid end index")
    elif thread_chunk_size < 1 or thread_chunk_size > len(artists_name) or len(artists_name) / thread_chunk_size < 1:
        raise Exception("Invalid thread chunk size")
    else:
        try:
            final_artists_data, final_albums_data, final_songs_data, final_genres_data = multithreading_processing_on_artist(
                artists_name[start_index:end_index], ss, thread_chunk_size=thread_chunk_size)
        except Exception:
            raise Exception


    # Convert into pandas dataframe
    artists_df = pd.DataFrame(final_artists_data, columns=[
                              "artist_id", "artist_name", "artist_popularity", "artist_followers"])
    albums_df = pd.DataFrame(final_albums_data, columns=[
                             "album_id", "album_type", "album_name", "album_popularity", "album_release_date", "album_total_tracks", "album_label", "artist_id"])
    songs_df = pd.DataFrame(final_songs_data, columns=["song_id", "song_name", "song_popularity", "song_disc_number", "song_explicit", "song_is_playable", "song_track_number", "song_release_date", "artist_id", "album_id", "song_danceability",
                                                       "song_energy", "song_key", "song_loudness", "song_mode", "song_speechiness", "song_acousticness", "song_instrumentalness", "song_liveness", "song_valence", "song_tempo", "song_duration_ms", "song_time_signature"])
    genres_df = pd.DataFrame(final_genres_data, columns=[
                             "artist_id", "artist_genres"])


    # Initialize MongoDB
    mongodb = MongoDB(client)

    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")
    # # Create database

    crawling_data = mongodb.create_database(db_name=MONGODB_DATABASE)

    # Create collections
    artists_data = mongodb.create_collection(
        collection_name="artists_data", db=crawling_data)
    albums_data = mongodb.create_collection(
        collection_name="albums_data", db=crawling_data)
    songs_data = mongodb.create_collection(
        collection_name="songs_data", db=crawling_data)
    genres_data = mongodb.create_collection(
        collection_name="genres_data", db=crawling_data)

    # Insert data
    mongodb.insert_many(artists_df.to_dict(orient="records"), db=crawling_data,
                        coll=artists_data)
    mongodb.insert_many(albums_df.to_dict(orient="records"), db=crawling_data,
                        coll=albums_data)
    mongodb.insert_many(songs_df.to_dict(orient="records"), db=crawling_data,
                        coll=songs_data)
    mongodb.insert_many(genres_df.to_dict(orient="records"), db=crawling_data,
                        coll=genres_data)

    # End
    print("Done")
