import streamlit as st
import os
import base64
from streamlit_lottie import st_lottie

MUSIC_NAME = "VoKichCuaEm.mp3"
HOME_PAGE_MUSIC = os.path.dirname(os.path.abspath(
    __file__)) + "/assets/{}".format(MUSIC_NAME)
SQUAD_IMAGE = "https://lottie.host/fa171cbb-5a2f-4879-aaf5-0a4699802616/j8368sPXYN.json"

st.set_page_config(page_title="Home", page_icon=":house:", layout="wide")

with st.container():
    st.title("Welcome to our project")
    st.caption(
        "This is a project for the course of Data Science at the University of Bologna")
    st.write("Before we delve into our project, I recommend taking a moment to enjoy some soothing music.")
    st.audio(HOME_PAGE_MUSIC)


with st.container():
    left_column, right_column = st.columns(2)
    left_column.subheader("Our team")
    with left_column:
        st.markdown("""
        - Tran Ngoc Tuan
        - Huynh Luu Vinh Phong
        - Mai Chien Vi Thien
        - Pham Duy Son
        """)

    with right_column:
        st_lottie(SQUAD_IMAGE, speed=1, height=200, key="initial")
