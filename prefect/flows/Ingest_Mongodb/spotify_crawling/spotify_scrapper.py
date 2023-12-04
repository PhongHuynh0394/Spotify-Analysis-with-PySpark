from requests import get
import json
import time
from typing import List


class SpotifyCrawler:
    def __init__(self, headers, max_retry_attempts=3, retry_wait_time=30, retry_factor=0, retry_status_codes: List[int] = [429]):
        self.headers = headers.get_auth_header()
        self.max_retry_attempts = max_retry_attempts
        self.retry_wait_time = retry_wait_time
        self.retry_factor = retry_factor
        self.retry_status_codes = retry_status_codes

    def __make_request(self, url, params: dict = None):
        retry_attempts = 0
        # retry_wait_time = self.retry_wait_time

        while retry_attempts < self.max_retry_attempts:
            response = get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return json.loads(response.content)
            elif response.status_code in self.retry_status_codes:
                # HTTP response will include a header named 'Retry-After' if the request is rate limited
                retry_wait_time = int(response.headers.get('Retry-After'))

                print(
                    f"Too many requests! Retrying after {retry_wait_time} seconds.")
                time.sleep(retry_wait_time)
                retry_attempts += 1
                # retry_wait_time *= (1 + self.retry_factor)
            else:
                raise Exception(f"Error: {response.status_code}")

        # Max retry attempts reached
        print("Max retry attempts reached!")
        raise RuntimeError("Max retry attempts reached!")

    def __search_artist(self, artist_name):
        url = 'https://api.spotify.com/v1/search'
        params = {
            'q': artist_name,
            'type': 'artist',
            'limit': 1
        }
        json_result = self.__make_request(url, params)
        artist = json_result['artists']['items'][0]
        return artist

    def __get_albums_of_artist(self, artist_id, limit=20):
        url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
        params = {
            'limit': limit
        }
        json_result = self.__make_request(url, params)
        albums = json_result['items']
        return albums

    def __get_albums_information(self, albums_id, artist_id):
        # Split albums_id into chunks of 20
        chunks = [albums_id[x:x+20] for x in range(0, len(albums_id), 20)]
        albums_information = []
        for chunk in chunks:
            url = 'https://api.spotify.com/v1/albums'
            params = {
                'ids': ','.join(chunk)
            }
            json_result = self.__make_request(url, params)
            albums_information.extend(json_result['albums'])

        # Remove tracks and markets from albums_information
        for album_information in albums_information:
            # Add artist_id to album_information
            album_information['artist_id'] = artist_id

            # Remove unnecessary keys
            del album_information['tracks']
            del album_information['available_markets']
            del album_information['artists']

        return albums_information

    def __get_tracks_of_album(self, album_id):
        url = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
        params = {
            'limit': 30
        }
        json_result = self.__make_request(url, params)
        tracks_of_album = json_result['items']

        return tracks_of_album

    def __get_tracks_of_albums(self, albums_id):
        tracks = []
        for album_id in albums_id:
            tracks_of_album = self.__get_tracks_of_album(album_id)
            tracks.extend(tracks_of_album)
        return tracks

    def __get_tracks_information(self, tracks_id):
        # Split tracks_id into chunks of 50
        chunks = [tracks_id[x:x+50] for x in range(0, len(tracks_id), 50)]
        tracks_information = []
        for chunk in chunks:
            url = 'https://api.spotify.com/v1/tracks'
            params = {
                'ids': ','.join(chunk)
            }
            json_result = self.__make_request(url, params)
            tracks_information.extend(json_result['tracks'])

        for track_information in tracks_information:
            # Add artist_id and album_id to track_information
            track_information['artist_id'] = track_information['artists'][0]['id']
            track_information['album_id'] = track_information['album']['id']

            # Remove unnecessary keys
            del track_information['available_markets']
            del track_information['artists']
            del track_information['album']

        return tracks_information

    def __get_tracks_features(self, tracks_id):
        # Split tracks_id into chunks of 100
        chunks = [tracks_id[x:x+100]
                  for x in range(0, len(tracks_id), 100)]
        tracks_features = []
        for chunk in chunks:
            url = 'https://api.spotify.com/v1/audio-features'
            params = {
                'ids': ','.join(chunk)
            }
            json_result = self.__make_request(url, params)
            tracks_features.extend(json_result['audio_features'])
        tracks_features = [
            track_feature for track_feature in tracks_features if track_feature is not None]
        return tracks_features

    def get_all_information_from_artist(self, artist_name: str):
        artist_information = self.__search_artist(artist_name)
        artist_id = artist_information.get('id')

        albums_of_artist = self.__get_albums_of_artist(
            artist_id, limit=20)
        albums_id = [album.get('id') for album in albums_of_artist]
        albums_information = self.__get_albums_information(
            albums_id, artist_id)

        tracks_of_albums = self.__get_tracks_of_albums(albums_id)
        tracks_id = [track.get('id') for track in tracks_of_albums]
        tracks_information = self.__get_tracks_information(tracks_id)

        tracks_features_information = self.__get_tracks_features(tracks_id)
        return [artist_information], albums_information, tracks_information, tracks_features_information

    def get_all_information_from_artists(self, artists_name: List[str]):
        final_artists_information, final_albums_information, final_tracks_information, final_tracks_features_information = [], [], [], []
        for artist_name in artists_name:
            artists_information, albums_information, tracks_information, tracks_features_information = self.get_all_information_from_artist(
                artist_name)
            final_artists_information.extend(artists_information)
            final_albums_information.extend(albums_information)
            final_tracks_information.extend(tracks_information)
            final_tracks_features_information.extend(
                tracks_features_information)
        print("Finish crawling")
        return final_artists_information, final_albums_information, final_tracks_information, final_tracks_features_information
