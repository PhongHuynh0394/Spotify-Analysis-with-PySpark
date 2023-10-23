from auth import get_token, get_auth_header
from spotify import search_for_artist_id, get_artist_albums, get_songs_from_album, get_info_of_artist, get_info_of_song, get_info_of_album
from spotify import get_info_features_of_song

if __name__ == "__main__":
    access_token, token_type = get_token()
    headers = get_auth_header(token_type, access_token)

    artist_name = "Justin Bieber"
    artist_id = search_for_artist_id(artist_name, headers)
    artist_popularity, artist_followers = get_info_of_artist(
        artist_id, headers)
    # artist_genres, artist_images_url

    artist_albums = get_artist_albums(artist_id, headers)
    for idx, album in enumerate(artist_albums):
        # album_available_markets
        album_id, album_name, album_release_date, album_group, album_type = album[
            "id"], album["name"], album["release_date"], album["album_group"], album["album_type"]
        songs = get_songs_from_album(album_id, headers)
        for song in songs:
            # song_available_markets, song_track_number
            song_id = song["id"]
            song_name, song_popularity, song_disc_number, song_explicit = get_info_of_song(
                song_id, headers)
            song_danceability, song_energy, song_key, song_loudness, song_mode, song_speechiness, song_acousticness, song_instrumentalness, song_liveness, song_valence, song_tempo, song_duration_ms, song_time_signature = get_info_features_of_song(
                song_id, headers)
            print(album_name, song_name, song_popularity, song_disc_number)
        break
