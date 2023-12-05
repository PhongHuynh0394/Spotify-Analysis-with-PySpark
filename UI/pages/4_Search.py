import streamlit as st
import pandas as pd
from streamlit import session_state as ss
import os

st.set_page_config(page_title="Search",
                   page_icon=":mag:",
                   layout="wide")


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("ui/assets/style.css")

if "search_term" not in ss:
    ss["search_term"] = None


def post_result(i):
    with st.expander("We don't talk anymore - Charlie Puth, Selena Gomez"):
        with st.spinner(text="Loading details..."):
            _, audio_middle_column, _ = st.columns(
                [1, 2, 1])
            with audio_middle_column:
                st.audio(
                    "https://p.scdn.co/mp3-preview/67ade7479434acdfc2fd6031fd6d06a6ca0271a1?cid=4a22b8f63a174da5807b38e7f599fe77")

            left_column, right_column = st.columns([8, 3])
            with right_column:
                with st.container():
                    table_markdown = """
                    ##### <ins>Song Info</ins>
                    | | |
                    | ----------- | -----------: |
                    | **Released on** | 2016-01-29 |
                    | **On Album** | Nine Track Mind |
                    | **Duration** | 323243 (ms) |
                    | **Preview url** | Url |
                    """
                    st.markdown(table_markdown, unsafe_allow_html=True)

                with st.container():
                    table_markdown = """
                    ##### <ins>Artist Info</ins>
                    | | |
                    | ----------- | -----------: |
                    | **Produced** by | Charlie Puth |
                    | **Popularity** | 90 |
                    """
                    st.markdown(table_markdown, unsafe_allow_html=True)
                    st.image(
                        "https://i.ytimg.com/vi/i_yLpCLMaKk/maxresdefault.jpg")

            with left_column:
                st.markdown("""#####  Want to taste similar songs?""")
                if st.button("Recommend", key=i):
                    with st.container():
                        # 5 sample music and its artist name
                        five_sample_data = [
                            {"name": "25 Minutes", "artist": "Michael Learns to Rock"},
                            {"name": "Nothing Gonna Change My Love",
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


# @st.cache_data


def show_results(search_term, df_search):
    for i, row in df_search.reset_index().iterrows():
        if row["genre"] == search_term:
            post_result(i)


st.write("# Searchinggg 🔎")

with st.form(key='search_form'):
    nav1, nav2, = st.columns([3, 2])

    with nav1:
        ss["search_term"] = st.text_input(
            "# Search", value=ss["search_term"], placeholder="Westlife", help="Enter the name of the artist, album or track")
    with nav2:
        type = st.selectbox(
            "# Type", ["Artist", "Album", "Track"], placeholder="Artist", help="Select the type of search")
    search_button = st.form_submit_button(
        label="# Find")

data = [
    {"name": "Item 1", "description": "Description of item 1", "genre": "rock"},
    {"name": "Item 2", "description": "Description of item 2", "genre": "rock"},
    {"name": "Item 3", "description": "Description of item 3", "genre": "rock"}
]
df_search = pd.DataFrame(data)

search_term = ss.search_term
show_results(search_term, df_search)
