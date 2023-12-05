import streamlit as st
import streamlit.components.v1 as components

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

# html_string = "<h3>this is an html string</h3>"

# st.markdown(html_string, unsafe_allow_html=True)

html_string = """
    <div>
    <h1>Hello World</h1>
    </div>
"""

components.html(html_string)
