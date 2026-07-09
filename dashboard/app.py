import streamlit as st

st.set_page_config(
    page_title="Spotify Music Intelligence",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎵 Spotify Music Intelligence")

st.markdown(
    """
    Welcome to the Spotify Music Intelligence Dashboard.

    Explore songs, artists, genres, historical trends, and predict the popularity of new songs using Machine Learning.
    """
)

st.sidebar.title("Spotify Analytics")

st.sidebar.success("Select a page from the sidebar.")

st.metric(
    label="Project Status",
    value="Dashboard Under Construction 🚀"
)
