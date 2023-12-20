from PIL import Image
from streamlit_extras.switch_page_button import switch_page
import streamlit as st
import os

IMAGE_NAME = "spotify_image.jpg"
MUSIC_NAME = "MyHeartWillGoOn.mp3"
CSS = "style.css"

st.set_page_config(page_title="Home",
                   page_icon=":house:",
                   layout="wide",
                   menu_items={'About': "# This is the home page of our UI!"})


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css(os.path.dirname(os.path.abspath(
    __file__)) + "/assets/{}".format(CSS))

with st.container():
    # st.header("Spotify Analysis", divider="rainbow")
    st.write("# Spotify Analysis")
    st.caption(
        "Only when listening to music can one maintain a happy mood and give oneself the most beautiful enjoyment in life.")
    st.write("""Spotify is a leading music streaming platform that revolutionized the way people listen to music. With a vast collection of over millions of tracks from various genres and languages, Spotify offers users the opportunity to explore, discover, and enjoy music from all around the world.""")
    code = '''
    if mood = "happy":
        play_music(happy_music)
    elif mood = "sad":
        play_music(sad_music)
    else:
        play_music("My heart will go on - Celine Dion")
    '''
    left_column, right_column = st.columns(spec=2, gap="large")
    with left_column:
        st.code(code, language="python")
        st.audio(os.path.dirname(os.path.abspath(__file__)) +
                 "/assets/{}".format(MUSIC_NAME))
    with right_column:
        image = Image.open(os.path.dirname(os.path.abspath(
            __file__)) + "/assets/{}".format(IMAGE_NAME)).resize((400, 235))
        st.image(image, use_column_width=False)

    st.write("Let's begin exploring our project slowly and steadily.")

    _, middle_button_column, _ = st.columns([5, 2, 5])
    with middle_button_column:
        get_started = st.button(
            "Get Started", key="get_started", use_container_width=True)
        if get_started:
            switch_page("Search")


