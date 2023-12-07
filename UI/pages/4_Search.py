from streamlit import session_state as ss
from utils.dremio import DremioClient
from PIL import Image
from io import BytesIO
import streamlit as st
import pandas as pd
import os
import requests

# Define constants
CSS = "style.css"
TABLE = {
    "Artist": "home.artist",
    "Album": "home.album",
    "Track": "home.track"
}

# Set page config
st.set_page_config(page_title="Search",
                   page_icon=":mag:",
                   layout="wide")

# Set session state
if "search_term" not in ss:
    ss["search_term"] = None
if "type" not in ss:
    ss["type"] = "Artist"


@st.cache_data
def fetch_response(url):
    with st.spinner(text="Loading image..."):
        response = requests.get(url)
        return response


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load CSS file
local_css(os.path.dirname(os.path.dirname(os.path.abspath(
    __file__))) + "/assets/{}".format(CSS))


def get_dremio_client(host, port, uid, pwd):
    client = DremioClient(host, port, uid, pwd)
    client.connect()
    options = client.authenticate()
    return client, options


def post_result(row):

    with st.expander("{} - {} - {}".format(row["track_name"], row["album_name"], row["artist_name"])):
        with st.spinner(text="Loading details..."):
            _, audio_middle_column, _ = st.columns(
                [1, 2, 1])
            with audio_middle_column:
                st.audio(row["track_url"])

            left_column, right_column = st.columns([10, 4])
            with right_column:
                with st.container():
                    table_markdown = """
                    ##### <ins>Song Info</ins>
                    | | |
                    | ----------- | -----------: |
                    | **Released on** | {} |
                    | **On Album** | {} |
                    | **Duration** | {} (ms) |
                    | **Spotify** | [{}]({}) |
                    """.format(row["track_release_year"], row["album_name"], row["duration_ms"], "Listen 🎧", row["track_url"])
                    st.markdown(table_markdown, unsafe_allow_html=True)

                with st.container():
                    table_markdown = """
                    ##### <ins>Artist Info</ins>
                    | | |
                    | ----------- | -----------: |
                    | **Produced** by | {} |
                    | **Popularity** | {} |
                    """.format(row["artist_name"], row["artist_popularity"])
                    st.markdown(table_markdown, unsafe_allow_html=True)

                with st.container():
                    # response = fetch_response(
                    #     "https://www.popsci.com/uploads/2021/12/02/imtiyaz-ali-LxBMsvUPAgo-unsplash-scaled.jpg?auto=webp&width=1440&height=895.5")
                    # image = Image.open(
                    #     BytesIO(response.content))
                    # st.image(image, use_column_width=True)
                    st.image(
                        row["artist_image"], use_column_width=False)

            with left_column:
                st.markdown("""#####  Want to taste similar songs?""")
                st.write("Here are some recommendations for you:")
                with st.container():
                    # 5 sample music and its artist name
                    five_sample_data = [
                        {"name": "25 Minutes", "artist": "Michael Learns to Rock"},
                        {"name": "Nothinig Gonna Change My Love",
                            "artist": "Westlife"},
                        {"name": "Beautiful In White", "artist": "Westlife"},
                        {"name": "No Promises", "artist": "Westlife"},
                        {"name": "Until You", "artist": "Westlife"}
                    ]
                    # Display 5 songs by row using streamlit
                    for data in five_sample_data:
                        # st.markdown("""###### {} - {}""".format(
                        #     data["name"], data["artist"]))
                        st.markdown(
                            "<p class='recommend-track-section'>{} - {}</p>".format(data["name"], data["artist"]), unsafe_allow_html=True)


def post_results(df_search):
    for _, row in df_search.reset_index().iterrows():
        post_result(row)


def find_results(client, options):
    sql = None

    if ss["type"] == "Track":
        sql = f"""
            SELECT track.id AS track_id, track.name AS track_name, track.external_urls AS track_url, track.popularity as track_popularity, artist.name AS artist_name, artist.popularity AS artist_popularity, artist.image_url AS artist_image, SUBSTRING(album.release_date, 1, 4) AS track_release_year, album.name AS album_name, track_features.danceability, track_features.energy, track_features.key, track_features.loudness, track_features.mode, track_features.speechiness, track_features.acousticness, track_features.instrumentalness, track_features.liveness, track_features.valence, track_features.tempo, track_features.duration_ms, track_features.time_signature, LISTAGG(artist_genres.genre, ', ') AS genres
            FROM home.track AS track
            JOIN home.album AS album
            ON track.album_id = album.id
            JOIN home.artist AS artist
            ON track.artist_id = artist.id
            JOIN home.track_features AS track_features
            ON track.id = track_features.id
            JOIN home.artist_genres as artist_genres
            ON artist.id = artist_genres.id
            WHERE track.name LIKE '%{ss['search_term']}%'
            GROUP BY track_id, track_name, track_url, track_popularity, artist_name, artist_popularity, artist_image, track_release_year, album_name, track_features.danceability, track_features.energy, track_features.key, track_features.loudness, track_features.mode, track_features.speechiness, track_features.acousticness, track_features.instrumentalness, track_features.liveness, track_features.valence, track_features.tempo, track_features.duration_ms, track_features.time_signature
            ORDER BY track_name
        """
    elif ss["type"] == "Album":
        columns_query = "album_type, artist_id, external_urls, name, popularity, release_date, total_tracks"
    elif ss["type"] == "Artist":
        columns_query = "external_urls, followers, genres, name, popularity"

    df = client.query(sql, options)
    return df

# @st.cache_data


def show_results(search_term, df_search):
    for i, row in df_search.reset_index().iterrows():
        if row["genre"] == search_term:
            post_result(i)


try:
    client, options = get_dremio_client(
        "localhost", 32010, "tntuan0910", "Hoang999@")
except Exception:
    st.error(
        "Cannot connect to Dremio. Please check your dremio status and try again.")
    st.stop()

st.write("# Searchinggg 🔎")

with st.form(key='search_form'):
    nav1, nav2, = st.columns([3, 2])

    with nav1:
        ss["search_term"] = st.text_input(
            "# Search", value=ss["search_term"], placeholder="Westlife", help="Enter the name of the artist, album or track")
    with nav2:
        ss["type"] = st.selectbox(
            "# Type", ["Artist", "Album", "Track"], placeholder="Artist", help="Select the type of search")
    search_button = st.form_submit_button(
        label="# Find")


if search_button:
    if ss['search_term'] is None:
        st.error("Please enter the search term")
        st.stop()
    df_search = find_results(client, options)
    post_results(df_search)
