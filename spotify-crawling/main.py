from auth import get_token, get_auth_header
from spotify import SpotifyScrapper
import pickle
import csv

ARTIST = "artist.csv"
ALBUM = "album.csv"
SONG = "song.csv"
GENRE = "genre.csv"

if __name__ == "__main__":
    # Authentication
    access_token, token_type = get_token()
    headers = get_auth_header(token_type, access_token)

    # Data
    artists_data, albums_data, songs_data, genres_data = [], [], [], []

    # Read artists's name
    artists_name = list(pickle.load(open("data/artists_name.pkl", "rb")))
    test_artists_name = artists_name[:1]

    # Initialize Spotify Scrapper
    ss = SpotifyScrapper(headers)

    # Find songs from artists
    for artist_name in test_artists_name:
        # Search for artist
        artist_id, artist_popularity, artist_followers, artist_genres = ss.search_for_artist_id(
            artist_name, info=True)

        # TODO: Add genre to csv
        for genre in artist_genres:
            genres_data.append((artist_id, genre))

        # TODO: Add artist to csv
        artists_data.append((artist_id, artist_name,
                             artist_popularity, artist_followers))

        # Get artist's albums, artist_genres
        artist_albums = ss.get_artist_albums(artist_id, info=True)
        for artist_album in artist_albums:
            album_id, album_type, album_name, album_popularity, album_release_date, album_total_tracks, album_label = artist_album

            # TODO: Add album to csv
            albums_data.append((album_id, album_type, album_name,
                                album_popularity, album_release_date, album_total_tracks, album_label, artist_id))

            # Get album's songs
            songs = ss.get_songs_from_album(album_id=album_id, info=True)
            for song in songs:
                song_id, song_name, song_popularity, song_disc_number, song_explicit, song_available_markets, song_is_playable, song_track_number, song_dancibility, song_energy, song_key, song_loudness, song_mode, song_speechiness, song_acousticness, song_instrumentalness, song_liveness, song_valence, song_tempo, song_duration_ms, song_time_signature = song
                # TODO: Add song to csv
                songs_data.append((song_id, song_name, song_popularity, song_disc_number, song_explicit, song_dancibility, song_energy, song_key, song_loudness, song_mode,
                                  song_speechiness, song_acousticness, song_instrumentalness, song_liveness, song_valence, song_tempo, song_duration_ms, song_time_signature, album_id, artist_id))

    # Write to csv
    with open(ARTIST, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["artist_id", "artist_name",
                         "artist_popularity", "artist_followers"])
        writer.writerows(artists_data)

    with open(ALBUM, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["album_id", "album_type", "album_name", "album_popularity",
                        "album_release_date", "album_total_tracks", "album_label", "artist_id"])
        writer.writerows(albums_data)

    with open(SONG, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["song_id", "song_name", "song_popularity", "song_disc_number", "song_explicit", "song_dancibility", "song_energy", "song_key", "song_loudness", "song_mode",
                        "song_speechiness", "song_acousticness", "song_instrumentalness", "song_liveness", "song_valence", "song_tempo", "song_duration_ms", "song_time_signature", "album_id", "artist_id"])
        writer.writerows(songs_data)

    with open(GENRE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["artist_id", "genre"])
        writer.writerows(genres_data)
