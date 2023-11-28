import streamlit as st


with st.form(key='search_form'):
    nav1, nav2, = st.columns([3, 2])

    with nav1:
        search_term = st.text_input("Search")
    with nav2:
        type = st.selectbox("Type", ["Artist", "Album", "Track"])
    search_button = st.form_submit_button(
        label="Search")

    if search_button:
        st.write("Search for {} in {}".format(search_term, type))
