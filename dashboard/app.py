import streamlit as st
from pathlib import Path
import plotly.express as px
from data_loader import load_data
import pandas as pd

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
# Load Data
# -----------------------------

songs, artists, genres, years, songs_with_genres = load_data()


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

# -----------------------------
# Step 3: Popularity Distribution
# -----------------------------

popularity_fig = px.histogram(
    songs,
    x="popularity",
    nbins=30,
    title="Popularity Distribution"
)

popularity_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#121212",
    plot_bgcolor="#121212",
    font=dict(color="white"),
)

# -----------------------------
# Step 4: Top Artists
# -----------------------------

top_artists = (
    artists
    .sort_values("popularity", ascending=False)
    .head(10)
)

artist_fig = px.bar(
    top_artists,
    x="popularity",
    y="artists",
    orientation="h",
    title="Top 10 Artists by Popularity"
)

artist_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#121212",
    plot_bgcolor="#121212",
    font=dict(color="white"),
)

# -----------------------------
# Step 5: Popularity Over Time
# -----------------------------

year_fig = px.line(
    years,
    x="year",
    y="popularity",
    markers=True,
    title="Average Popularity Over Time"
)

year_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#121212",
    plot_bgcolor="#121212",
    font=dict(color="white"),
)

# -----------------------------
# Step 6: Display the Charts
# -----------------------------

st.divider()

left, right = st.columns(2)

with left:
    st.plotly_chart(
        popularity_fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )

with right:
    st.plotly_chart(
        artist_fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )

st.plotly_chart(
    year_fig,
    use_container_width=True,
    config={"displayModeBar": False},
)

st.divider()
st.caption(f"Data last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption(f"Total songs in dataset: {len(songs):,}")