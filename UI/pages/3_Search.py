from streamlit import session_state as ss
from utils.dremio import DremioClient
from utils.model import SongRecommendationSystem 
from PIL import Image
from io import BytesIO
import streamlit as st
import pandas as pd
import os
import requests
# import dill
# import time


# Define constants
CSS = "style.css"
TABLE = {
    "Artist": "home.artist",
    "Album": "home.album",
    "Track": "home.track",
    "Genre": "home.genre",
    "Track Feat": "home.track_feat"
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


def get_dremio_client():
    host = os.getenv("DREMIO_HOST")
    uid = os.getenv("DREMIO_USER")
    pwd = os.getenv("DREMIO_PASSWORD")
    port = os.getenv("DREMIO_PORT")
    client = DremioClient(host, port, uid, pwd)
    client.connect()
    options = client.authenticate()
    return client, options

def get_model(client, options):
    model = SongRecommendationSystem(client, options)
    model.fit('home.model')
    return model

def post_result(row, model):

    with st.expander("{} - {} - {}".format(row["track_name"], row["album_name"], row["artist_name"])):
        with st.spinner(text="Loading details..."):

            if row["track_preview"]:
                _, audio_middle_column, _ = st.columns(
                    [1, 2, 1])
                with audio_middle_column:
                    st.audio(row["track_preview"])

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
                    st.markdown("<img src='{}' class='artist-image'>".format(
                        row["artist_image"]), unsafe_allow_html=True)

            with left_column:
                st.write("""##### Want to tast similar songs?""")
                st.write("Here are some recommendations for you:")
                with st.container():
                    print(type(row['track_name']))
                    ## Model here
                    result = model.recommend_songs(str(row['track_name']))
                    for data in result[['track_name', 'artist_name']].values:
                        st.markdown(
                            "<p class='recommend-track-section'>{} - {}</p>".format(data[0], data[1]), unsafe_allow_html=True)


def post_results(df_search, model):
    for _, row in df_search.reset_index().iterrows():
        post_result(row, model)


def find_results(client, options):
    sql = None

    if ss["type"] == "Track":
        sql = f"""SELECT * FROM home.searchs
            WHERE LOWER(track_name) LIKE '%{ss["search_term"]}%'
            ORDER BY track_popularity
            LIMIT 10
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
    client, options = get_dremio_client()
except Exception:
    st.error(
        "Cannot connect to Dremio. Please check your dremio status and try again.")
    st.stop()

model = get_model(client, options)


st.write("# Searchinggg 🔎")

with st.form(key='search_form'):
    nav1, nav2, = st.columns([3, 2])

    with nav1:
        ss["search_term"] = st.text_input(
            "# Search", value=ss["search_term"], placeholder="Westlife", help="Enter the name of the artist, album or track")
    with nav2:
        ss["type"] = st.selectbox(
            "# Type", ["Track"], placeholder="Track", help="Select the type of search")
    search_button = st.form_submit_button(
        label="# Find")


if search_button:
    if ss['search_term'] is None:
        st.error("Please enter the search term")
        st.stop()
    else:
        ss['search_term'] = ss['search_term'].lower().strip()
    df_search = find_results(client, options)
    with st.spinner(text="Loading results..."):
        post_results(df_search, model)

