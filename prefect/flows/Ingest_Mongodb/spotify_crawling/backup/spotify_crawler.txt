from requests import get
from requests.exceptions import ConnectionError
from queue import Queue
import json
import time
import threading


BASE_URL = 'https://api.spotify.com/v1'


def make_spotify_api_request(url, headers, params: dict = None):
    """_summary_

    Args:
        url (_type_): Spotify api url
        headers (_type_): Spotify api headers
        params (dict, optional): Spotify api params. Defaults to None.

    Returns:
        object: Spotify api response
    """
    retry_attempts = 0
    max_retry_attempts = 5
    retry_wait_time = 30  # Initial wait time in seconds

    while retry_attempts < max_retry_attempts:
        response = get(url, headers=headers, params=params)
        if response.status_code == 429:
            # retry_wait_time = int(response.headers.get('Retry-After', 15))
            print(f"Rate limited. Retrying after {retry_wait_time} seconds.")
            time.sleep(retry_wait_time)
            retry_attempts += 1
            retry_wait_time += 30
        elif response.status_code == 200:
            # Successful API response
            return response
        else:
            # Handle other response codes as needed
            print(f"Error: {response.status_code}")
            raise ConnectionError

    # Max retry attempts reached
    print("Max retry attempts reached. Aborting.")
    raise ConnectionError("Max retry attempts reached. Aborting.")


class SpotifyScrapper:
    def __init__(self, headers):
        self.headers = headers

    def __check_empty_album(self, artist_albums):
        """_summary_

        Args:
            artist_albums (list): A list of albums

        Returns:
            bool: True if empty, False otherwise
        """
        if len(artist_albums) == 0:
            return True
        return False

    def __check_empty_genres(self, artist_genres):
        """_summary_

        Args:
            artist_genres (list): A list of genres

        Returns:
            bool: True if empty, False otherwise
        """
        if len(artist_genres) == 0:
            return True
        return False

    def search_for_artist_id(self, artist_name: object, limit=1):
        """_summary_

        Args:
            artist_name (object): A artist name
            limit (int, optional): Maximum number of result found. Defaults to 1.

        Returns:
            str: An artist id
        """
        # "https://api.spotify.com/v1/search"
        url = BASE_URL + "/search"
        params = {"q": artist_name, "type": "artist", "limit": limit}
        result = make_spotify_api_request(
            url, headers=self.headers, params=params)
        artist_id = json.loads(result.content)["artists"]["items"][0]["id"]
        return artist_id

    def get_several_artists(self, artists_id: list):
        """_summary_

        Args:
            artists_id (list): A list of artists id

        Returns:
            list: A list of artists
        """
        params = {
            'ids': str.join(",", artists_id)
        }
        # "https://api.spotify.com/v1/artists"
        url = BASE_URL + "/artists"
        result = make_spotify_api_request(
            url, headers=self.headers, params=params)
        artists = json.loads(result.content)["artists"]
        return artists

    def get_info_of_artist(self, artist_info: json):
        """_summary_

        Args:
            artist_info (json): A json object of artist info

        Returns:
            tuple: Tuple of artist_id, artist_name, artist_popularity, artist_followers, artist_genres
        """

        try:
            artist_id = artist_info["id"]
        except Exception:
            artist_id = None

        try:
            artist_name = artist_info["name"]
        except Exception:
            artist_name = None

        try:
            artist_popularity = artist_info["popularity"]
        except Exception:
            artist_popularity = None

        try:
            artist_followers = artist_info["followers"]["total"]
        except Exception:
            artist_followers = None

        try:
            artist_genres = artist_info["genres"]
            if self.__check_empty_genres(artist_genres):
                artist_genres = None
        except Exception:
            artist_genres = None

        return artist_id, artist_name, artist_popularity, artist_followers, artist_genres

    def get_several_albums(self, albums_id: list):
        """_summary_

        Args:
            albums_id (list): A list of albums id

        Returns:
            list: A list of albums
        """
        params = {
            'ids': str.join(",", albums_id)
        }
        # "https://api.spotify.com/v1/albums"
        url = BASE_URL + "/albums"
        result = make_spotify_api_request(
            url, headers=self.headers, params=params)
        albums = json.loads(result.content)["albums"]
        return albums

    def get_info_of_album(self, album_info: json):
        """_summary_

        Args:
            album_info (json): A json object of album info

        Returns:
            tuple: Tuple of album_id, album_type, album_name, album_popularity, album_release_date, album_total_tracks, album_label, album_artist_id
        """
        try:
            album_id = album_info["id"]
        except Exception:
            album_id = None

        try:
            album_type = album_info["album_type"]
        except Exception:
            album_type = None

        try:
            album_name = album_info["name"]
        except Exception:
            album_name = None

        try:
            album_popularity = album_info["popularity"]
        except Exception:
            album_popularity = None

        try:
            album_release_date = album_info["release_date"]
        except Exception:
            album_release_date = None

        try:
            album_total_tracks = album_info["total_tracks"]
        except Exception:
            album_total_tracks = None

        try:
            album_label = album_info["label"]
        except Exception:
            album_label = None

        try:
            album_artist_id = album_info["artists"][0]["id"]
        except Exception:
            album_artist_id = None

        return album_id, album_type, album_name, album_popularity, album_release_date, album_total_tracks, album_label, album_artist_id

    def get_albums_of_artist(self, artist_id, limit=30):
        """_summary_

        Args:
            artist_id (_type_): An artist id
            limit (int, optional): Maximum number of albums. Defaults to 30.

        Returns:
            list: A list of albums
        """
        if artist_id is None:
            return None
        # "https://api.spotify.com/v1/artists/" + artist_id + "/albums"
        url = BASE_URL + "/artists/" + artist_id + "/albums"
        params = {"include_groups": "album", "limit": limit}
        result = make_spotify_api_request(
            url, headers=self.headers, params=params)
        artist_albums = json.loads(result.content)["items"]

        if self.__check_empty_album(artist_albums):
            return None
        return artist_albums

    def get_several_songs(self, songs_id: list):
        """_summary_

        Args:
            songs_id (list): A list of songs id

        Returns:
            list: A list of songs
        """
        params = {
            'ids': str.join(",", songs_id)
        }
        # "https://api.spotify.com/v1/tracks"
        url = BASE_URL + "/tracks"
        result = make_spotify_api_request(
            url, headers=self.headers, params=params)
        songs = json.loads(result.content)["tracks"]
        return songs

    def get_info_of_song(self, song_info: json):
        """_summary_

        Args:
            song_info (json): A json object of song info

        Returns:
            tuple: Tuple of song_id, song_name, song_popularity, song_disc_number, song_explicit, song_is_playable, song_track_number, song_artist_id, song_album_id
        """
        try:
            song_id = song_info["id"]
        except Exception:
            song_id = None

        try:
            song_name = song_info["name"]
        except Exception:
            song_name = None

        try:
            song_popularity = song_info["popularity"]
        except Exception:
            song_popularity = None

        try:
            song_disc_number = song_info["disc_number"]
        except Exception:
            song_disc_number = None

        try:
            song_explicit = song_info["explicit"]
        except Exception:
            song_explicit = None

        try:
            song_is_playable = song_info["is_playable"]
        except Exception:
            song_is_playable = None

        try:
            song_track_number = song_info["track_number"]
        except Exception:
            song_track_number = None

        try:
            song_release_date = song_info["album"]["release_date"]
        except Exception:
            song_release_date = None

        try:
            song_artist_id = song_info["artists"][0]["id"]
        except Exception:
            song_artist_id = None

        try:
            song_album_id = song_info["album"]["id"]
        except Exception:
            song_album_id = None

        return song_id, song_name, song_popularity, song_disc_number, song_explicit, song_is_playable, song_track_number, song_release_date, song_artist_id, song_album_id

    def get_several_songs_features(self, songs_id: list):
        """_summary_

        Args:
            songs_id (list): A list of songs id

        Returns:
            list: A list of songs features
        """
        params = {
            'ids': str.join(",", songs_id)
        }
        # "https://api.spotify.com/v1/audio-features"
        url = BASE_URL + "/audio-features"
        result = make_spotify_api_request(
            url, headers=self.headers, params=params)
        if not result:
            return None
        songs_features = json.loads(result.content)["audio_features"]
        return songs_features

    def get_info_features_of_song(self, song_features: json):
        """_summary_

        Args:
            song_features (json): A json object of song features

        Returns:
            tuple: Tuple of song_danceability, song_energy, song_key, song_loudness, song_mode, song_speechiness, song_acousticness, song_instrumentalness, song_liveness, song_valence, song_tempo, song_duration_ms, song_time_signature
        """
        try:
            song_danceability = song_features["danceability"]
        except Exception:
            song_danceability = None

        try:
            song_energy = song_features["energy"]
        except Exception:
            song_energy = None

        try:
            song_key = song_features["key"]
        except Exception:
            song_key = None

        try:
            song_loudness = song_features["loudness"]
        except Exception:
            song_loudness = None

        try:
            song_mode = song_features["mode"]
        except Exception:
            song_mode = None

        try:
            song_speechiness = song_features["speechiness"]
        except Exception:
            song_speechiness = None

        try:
            song_acousticness = song_features["acousticness"]
        except Exception:
            song_acousticness = None

        try:
            song_instrumentalness = song_features["instrumentalness"]
        except Exception:
            song_instrumentalness = None

        try:
            song_liveness = song_features["liveness"]
        except Exception:
            song_liveness = None

        try:
            song_valence = song_features["valence"]
        except Exception:
            song_valence = None

        try:
            song_tempo = song_features["tempo"]
        except Exception:
            song_tempo = None

        try:
            song_duration_ms = song_features["duration_ms"]
        except Exception:
            song_duration_ms = None

        try:
            song_time_signature = song_features["time_signature"]
        except Exception:
            song_time_signature = None

        return song_danceability, song_energy, song_key, song_loudness, song_mode, song_speechiness, song_acousticness, song_instrumentalness, song_liveness, song_valence, song_tempo, song_duration_ms, song_time_signature


def extract_data_from_artists(artists_names: list, scrapper: SpotifyScrapper, queue: Queue, error_flag):
    """_summary_

    Args:
        artists_names (list): A list of artists names
        scrapper (SpotifyScrapper): SpotifyScrapper object
        queue (Queue): Queue object
    """
    # Data
    artists_data, albums_data, songs_data, genres_data = [], [], [], []

    # Initialize list of artists id
    try:
        artists_id = [scrapper.search_for_artist_id(
            artist_name) for artist_name in artists_names]

        ids_batch_size = 50
        artists_id_batches = [artists_id[i:i+ids_batch_size] for i in range(
            0, len(artists_id), ids_batch_size)]

        # Get all artists
        artists = []
        for batch in artists_id_batches:
            artists.extend(scrapper.get_several_artists(batch))

        # Get all albums id
        albums_id = []
        for artist in artists:
            artist_id, artist_name, artist_popularity, artist_followers, artist_genres = scrapper.get_info_of_artist(
                artist)
            artists_data.append(
                (artist_id, artist_name, artist_popularity, artist_followers))

            if artist_genres:
                for genre in artist_genres:
                    genres_data.append((artist_id, genre))

            artist_albums = scrapper.get_albums_of_artist(artist_id)
            if not artist_albums:
                continue
            albums_id.extend([album["id"] for album in artist_albums])

        # Split albums_id into batches of 20
        album_batch_size = 20
        albums_id_batches = [albums_id[i:i+album_batch_size] for i in range(
            0, len(albums_id), album_batch_size)]

        # Get all albums
        albums = []
        for batch in albums_id_batches:
            albums.extend(scrapper.get_several_albums(batch))

        # Get all tracks id of all albums
        tracks_id = []
        for album in albums:
            albums_id, album_type, album_name, album_popularity, album_release_date, album_total_tracks, album_label, artist_id = scrapper.get_info_of_album(
                album)
            albums_data.append((albums_id, album_type, album_name, album_popularity,
                                album_release_date, album_total_tracks, album_label, artist_id))

            tracks_id.extend([track["id"] for track in album["tracks"]["items"]])

        # Get all tracks
        songs = []
        songs_features = []

        # Split tracks_id into batches of 30
        song_batch_size = 50
        for i in range(0, len(tracks_id), song_batch_size):
            song_batch = tracks_id[i:i+song_batch_size]
            songs.extend(scrapper.get_several_songs(song_batch))
            songs_features.extend(scrapper.get_several_songs_features(song_batch))

        # Extract data from songs and songs features
        for song, song_features in zip(songs, songs_features):
            song_id, song_name, song_popularity, song_disc_number, song_explicit, song_is_playable, song_track_number, song_release_date, artist_id, album_id = scrapper.get_info_of_song(
                song)
            song_danceability, song_energy, song_key, song_loudness, song_mode, song_speechiness, song_acousticness, song_instrumentalness, song_liveness, song_valence, song_tempo, song_duration_ms, song_time_signature = scrapper.get_info_features_of_song(
                song_features)
            songs_data.append((song_id, song_name, song_popularity, song_disc_number, song_explicit, song_is_playable, song_track_number, song_release_date, artist_id, album_id, song_danceability, song_energy, song_key,
                              song_loudness, song_mode, song_speechiness, song_acousticness, song_instrumentalness, song_liveness, song_valence, song_tempo, song_duration_ms, song_time_signature))

        queue.put((artists_data, albums_data, songs_data, genres_data))

    except Exception:
        error_flag[0] = True
        raise Exception


def multithreading_processing_on_artist(artists_names: list, scrapper: SpotifyScrapper, thread_chunk_size: int = 10):
    """_summary_

    Args:
        artists_names (list): A list of artists names
        scrapper (SpotifyScrapper): SpotifyScrapper object
        thread_chunk_size (int, optional): Number of artists that processed by each thread. Defaults to 10.

    Returns:
        tuple: Tuple of artists_data, albums_data, songs_data
    """
    # Initialize queue and artists chunks
    queue = Queue()
    thread_chunk_size = thread_chunk_size
    artists_chunks = [artists_names[i:i+thread_chunk_size]
                      for i in range(0, len(artists_names), thread_chunk_size)]
    error_flag = [False]

    # Initialize threads
    threads = []
    for chunk in artists_chunks:
        thread = threading.Thread(
            target=extract_data_from_artists, args=(chunk, scrapper, queue, error_flag,))
        threads.append(thread)
        thread.start()

    for t in threads:
        # This will run Threads
        t.join()

    if any(error_flag):
        # catch the error if exist
        raise Exception

    # Extract data from queue
    final_artists_data, final_albums_data, final_songs_data, final_genres_data = [], [], [], []
    while not queue.empty():
        artists_data, albums_data, songs_data, genres_data = queue.get()
        final_artists_data.extend(artists_data)
        final_albums_data.extend(albums_data)
        final_songs_data.extend(songs_data)
        final_genres_data.extend(genres_data)
    return final_artists_data, final_albums_data, final_songs_data, final_genres_data
