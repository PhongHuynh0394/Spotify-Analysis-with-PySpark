from requests import get
import json


class SpotifyScrapper:
    def __init__(self, headers):
        self.headers = headers

    def __check_empty_genres(self, genres):
        if len(genres) == 0:
            return True
        return False

    def __get_info_of_artist(self, artist_id):
        '''
        Returns a list of songs from the album
        '''
        url = "https://api.spotify.com/v1/artists/" + artist_id
        result = get(url, headers=self.headers)
        artist_info = json.loads(result.content)

        try:
            artist_popularity = artist_info["popularity"]
        except KeyError as e:
            artist_popularity = None

        try:
            artist_followers = artist_info["followers"]["total"]
        except KeyError as e:
            artist_followers = None

        try:
            artist_genres = artist_info["genres"]
            if self.__check_empty_genres(artist_genres):
                artist_genres = None
        except KeyError as e:
            artist_genres = None

        return artist_popularity, artist_followers, artist_genres

    def search_for_artist_id(self, artist_name, info=False, limit=1):
        '''
        Returns the artist id of the first artist found
        '''
        url = "https://api.spotify.com/v1/search"
        params = {"q": artist_name, "type": "artist", "limit": limit}
        result = get(url, headers=self.headers, params=params)
        artist_id = json.loads(result.content)["artists"]["items"][0]["id"]

        if info:
            artist_popularity, artist_followers, artist_genres = self.__get_info_of_artist(
                artist_id)
            return artist_id, artist_popularity, artist_followers, artist_genres
        return artist_id

    def __check_empty_album(self, artist_albums):
        if len(artist_albums) == 0:
            return True
        return False

    def __get_info_of_album(self, album_id):
        '''
        Returns a list of songs from the album
        '''
        url = "https://api.spotify.com/v1/albums/" + album_id
        result = get(url, headers=self.headers)
        album_info = json.loads(result.content)

        try:
            album_type = album_info["album_type"]
        except KeyError:
            album_type = None

        try:
            album_name = album_info["name"]
        except KeyError:
            album_name = None

        try:
            album_popularity = album_info["popularity"]
        except KeyError:
            album_popularity = None

        try:
            album_release_date = album_info["release_date"]
        except KeyError:
            album_release_date = None

        try:
            album_total_tracks = album_info["total_tracks"]
        except KeyError:
            album_total_tracks = None

        try:
            album_label = album_info["label"]
        except KeyError:
            album_label = None

        return album_type, album_name, album_popularity, album_release_date, album_total_tracks, album_label

    def get_artist_albums(self, artist_id, info=False, limit=30):
        '''
        Returns a list of albums from the artist
        '''
        url = "https://api.spotify.com/v1/artists/" + artist_id + "/albums"
        params = {"include_groups": "album", "limit": limit}
        result = get(url, headers=self.headers, params=params)
        artist_albums = json.loads(result.content)["items"]

        if self.__check_empty_album(artist_albums):
            return None

        if info:
            albums = []
            for artist_album in artist_albums:
                album_id = artist_album["id"]
                album_type, album_name, album_popularity, album_release_date, album_total_tracks, album_label = self.__get_info_of_album(
                    album_id)
                albums.append((album_id, album_type, album_name, album_popularity,
                               album_release_date, album_total_tracks, album_label))
            return albums
        return artist_albums

    def __get_info_features_of_song(self, song_id):
        '''
        Return features of a song
        '''
        url = "https://api.spotify.com/v1/audio-features/" + song_id
        result = get(url, headers=self.headers)
        song_features = json.loads(result.content)

        try:
            song_danceability = song_features["danceability"]
        except KeyError:
            song_danceability = None

        try:
            song_energy = song_features["energy"]
        except KeyError:
            song_energy = None

        try:
            song_key = song_features["key"]
        except KeyError:
            song_key = None

        try:
            song_loudness = song_features["loudness"]
        except KeyError:
            song_loudness = None

        try:
            song_mode = song_features["mode"]
        except KeyError:
            song_mode = None

        try:
            song_speechiness = song_features["speechiness"]
        except KeyError:
            song_speechiness = None

        try:
            song_acousticness = song_features["acousticness"]
        except KeyError:
            song_acousticness = None

        try:
            song_instrumentalness = song_features["instrumentalness"]
        except KeyError:
            song_instrumentalness = None

        try:
            song_liveness = song_features["liveness"]
        except KeyError:
            song_liveness = None

        try:
            song_valence = song_features["valence"]
        except KeyError:
            song_valence = None

        try:
            song_tempo = song_features["tempo"]
        except KeyError:
            song_tempo = None

        try:
            song_duration_ms = song_features["duration_ms"]
        except KeyError:
            song_duration_ms = None

        try:
            song_time_signature = song_features["time_signature"]
        except KeyError:
            song_time_signature = None

        return song_danceability, song_energy, song_key, song_loudness, song_mode, song_speechiness, song_acousticness, song_instrumentalness, song_liveness, song_valence, song_tempo, song_duration_ms, song_time_signature

    def __get_info_of_song(self, song_id):
        '''
        Returns a list of songs from the album
        '''
        url = "https://api.spotify.com/v1/tracks/" + song_id
        result = get(url, headers=self.headers)
        song_info = json.loads(result.content)

        try:
            song_name = song_info["name"]
        except KeyError:
            song_name = None

        try:
            song_popularity = song_info["popularity"]
        except KeyError:
            song_popularity = None

        try:
            song_disc_number = song_info["disc_number"]
        except KeyError:
            song_disc_number = None

        try:
            song_explicit = song_info["explicit"]
        except KeyError:
            song_explicit = None

        try:
            song_available_markets = song_info["available_markets"]
        except KeyError:
            song_available_markets = None

        try:
            song_is_playable = song_info["is_playable"]
        except KeyError:
            song_is_playable = None

        try:
            song_track_number = song_info["track_number"]
        except KeyError:
            song_track_number = None

        song_dancibility, song_energy, song_key, song_loudness, song_mode, song_speechiness, song_acousticness, song_instrumentalness, song_liveness, song_valence, song_tempo, song_duration_ms, song_time_signature = self.__get_info_features_of_song(
            song_id)
        return song_name, song_popularity, song_disc_number, song_explicit, song_available_markets, song_is_playable, song_track_number, song_dancibility, song_energy, song_key, song_loudness, song_mode, song_speechiness, song_acousticness, song_instrumentalness, song_liveness, song_valence, song_tempo, song_duration_ms, song_time_signature

    def get_songs_from_album(self, album_id, info=False, limit=30):
        '''
        Returns a list of songs from the album
        '''
        url = "https://api.spotify.com/v1/albums/" + album_id + "/tracks"
        params = {"limit": limit}
        result = get(url, headers=self.headers, params=params)
        album_songs = json.loads(result.content)["items"]

        if info:
            songs = []
            for song in album_songs:
                song_id = song["id"]
                song_name, song_popularity, song_disc_number, song_explicit, song_available_markets, song_is_playable, song_track_number, song_dancibility, song_energy, song_key, song_loudness, song_mode, song_speechiness, song_acousticness, song_instrumentalness, song_liveness, song_valence, song_tempo, song_duration_ms, song_time_signature = self.__get_info_of_song(
                    song_id)
                songs.append((song_id, song_name, song_popularity, song_disc_number, song_explicit, song_available_markets, song_is_playable, song_track_number, song_dancibility, song_energy, song_key,
                             song_loudness, song_mode, song_speechiness, song_acousticness, song_instrumentalness, song_liveness, song_valence, song_tempo, song_duration_ms, song_time_signature))
            return songs
        return album_songs


def search_for_artist_id(artist_name, headers):
    '''
    Returns the artist id of the first artist found
    '''
    url = "https://api.spotify.com/v1/search"
    params = {"q": artist_name, "type": "artist", "limit": 1}
    result = get(url, headers=headers, params=params)
    json_result = json.loads(result.content)["artists"]["items"][0]["id"]
    return json_result
