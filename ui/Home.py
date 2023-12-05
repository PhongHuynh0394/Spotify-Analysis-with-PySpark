import streamlit as st
from streamlit.components.v1 import html
import os
import requests
from PIL import Image
from io import BytesIO
from streamlit_extras.switch_page_button import switch_page

MUSIC_NAME = "VoKichCuaEm.mp3"
HOME_PAGE_MUSIC = os.path.dirname(os.path.abspath(
    __file__)) + "/assets/{}".format(MUSIC_NAME)


@st.cache_data
def fetch_response(url):
    with st.spinner(text="Loading image..."):
        response = requests.get(url)
        return response


st.set_page_config(page_title="Home",
                   page_icon=":house:",
                   layout="wide",
                   menu_items={'About': "# This is the home page of our UI!"})


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("ui/assets/style.css")

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
        play_music("Last Christmas - Cardi B")
    '''
    left_column, right_column = st.columns(spec=2, gap="large")
    with left_column:
        st.code(code, language="python")
        st.audio(HOME_PAGE_MUSIC)
    with right_column:
        response = fetch_response(
            "https://www.popsci.com/uploads/2021/12/02/imtiyaz-ali-LxBMsvUPAgo-unsplash-scaled.jpg?auto=webp&width=1440&height=895.5")
        image = Image.open(BytesIO(response.content)).resize((400, 235))
        st.image(image, use_column_width=False)

    st.write("Let's begin exploring our project slowly and steadily.")

    _, middle_button_column, _ = st.columns([5, 2, 5])
    with middle_button_column:
        get_started = st.button(
            "Get Started", key="get_started", use_container_width=True)
        if get_started:
            switch_page("About")

    st.divider()
with st.container():
    # st.header("About Us", divider="rainbow")
    st.write("# About Us")
    st.write("We are four students from the University of Sciences and we are working on this project with the aim of applying the knowledge we have learned to real-world projects and striving to learn new concepts and skills.")
    left_column, right_column = st.columns(2)
    with left_column:
        st.text("- Tran Ngoc Tuan")
        st.text("- Huynh Luu Vinh Phong")
        st.text("- Mai Chien Vi Thien")
        st.text("- Pham Duy Son")

    with right_column:
        st.text("https://github.com/TuanTran0910")
        st.text("https://github.com/TuanTran0910")
        st.text("https://github.com/TuanTran0910")
        st.text("https://github.com/TuanTran0910")
