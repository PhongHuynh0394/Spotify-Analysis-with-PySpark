import streamlit as st
import os
import requests
from PIL import Image
from io import BytesIO

MUSIC_NAME = "VoKichCuaEm.mp3"
HOME_PAGE_MUSIC = os.path.dirname(os.path.abspath(
    __file__)) + "/assets/{}".format(MUSIC_NAME)
SQUAD_IMAGE = "https://lottie.host/fa171cbb-5a2f-4879-aaf5-0a4699802616/j8368sPXYN.json"


@st.cache_data
def fetch_response(url):
    response = requests.get(url)
    return response


st.set_page_config(page_title="Home", page_icon=":house:", layout="wide")

with st.container():
    st.header("Spotify Analysis", divider="rainbow")
    # st.caption(
    #     "This practical final project is part of the Python for Data Science course in the field of Data Science at VNUHCM - University of Science.")
    st.caption(
        "Only when listening to music can one maintain a happy mood and give oneself the most beautiful enjoyment in life.")
    st.write("Spotify is a leading music streaming platform that revolutionized the way people listen to music. With a vast collection of over millions of tracks from various genres and languages, Spotify offers users the opportunity to explore, discover, and enjoy music from all around the world.")
    code = '''
    if mood = "happy":
        play_music(happy_music)
    elif mood = "sad":
        play_music(sad_music)
    else:
        play_music(normal_music)
    '''
    left_column, right_column = st.columns(2)
    with left_column:
        st.code(code, language="python")
        st.audio(HOME_PAGE_MUSIC)
    with right_column:
        response = fetch_response(
            "https://www.popsci.com/uploads/2021/12/02/imtiyaz-ali-LxBMsvUPAgo-unsplash-scaled.jpg?auto=webp&width=1440&height=895.5")
        image = Image.open(BytesIO(response.content)).resize((500, 325))
        st.image(image, use_column_width=True)

    st.write("Let's begin exploring our project slowly and steadily.")

with st.container():
    st.header("About Us", divider="rainbow")
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
