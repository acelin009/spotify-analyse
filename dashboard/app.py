import streamlit as st
from pathlib import Path


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Spotify Music Intelligence",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -----------------------------
# Load Custom CSS
# -----------------------------

def load_css():
    css_file = (
        Path(__file__).parent
        / "assets"
        / "styles.css"
    )

    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )


load_css()


# -----------------------------
# Home Page
# -----------------------------

st.title("🎵 Spotify Music Intelligence")

st.markdown(
    """
    ## AI-Powered Music Analytics Dashboard

    Welcome to the **Spotify Music Intelligence Dashboard**.

    This dashboard provides interactive analytics on Spotify songs, artists,
    genres, historical trends, and machine learning predictions.

    Use the **sidebar** to navigate between the different dashboard pages.
    """
)

st.sidebar.title("Spotify Analytics")
st.sidebar.success("Select a page from the sidebar.")

st.info("👈 Choose a page from the sidebar to begin exploring the dashboard.")