import pandas as pd
import streamlit as st


tab1, tab2, tab3, tab4 = st.tabs(["Artists", "Albums", "Tracks", "Genres"])

with tab1:
    # Tạo một DataFrame đơn giản
    data = {'Name': ['John', 'Jane', 'Mike', 'Sarah'],
            'Age': [25, 30, 28, 35],
            'City': ['New York', 'London', 'Paris', 'Sydney']}
    df = pd.DataFrame(data)

    # Hiển thị DataFrame trên Streamlit
    st.dataframe(df)
