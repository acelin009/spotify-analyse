import streamlit as st
from data_loader import load_data
from components import kpi_card

songs, artists, genres, years, songs_with_genres = load_data()

st.title("📊 Overview")

st.markdown(
    """
    This page provides a high-level overview of the Spotify dataset, including
    key performance indicators (KPIs) and a preview of the available data.
    """
)

total_songs = len(songs)
total_artists = songs["artists"].nunique()
average_popularity = songs["popularity"].mean()

years_covered = (
    songs["year"].min(),
    songs["year"].max(),
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card(
        "Songs",
        f"{total_songs:,}",
        "🎵"
    )

with col2:
    kpi_card(
        "Artists",
        f"{total_artists:,}",
        "🎤"
    )

with col3:
    kpi_card(
        "Avg Popularity",
        f"{average_popularity:.1f}",
        "⭐"
    )

with col4:
    kpi_card(
        "Years",
        f"{years_covered[0]} - {years_covered[1]}",
        "📅"
    )

st.divider()

st.subheader("Dataset Preview")

st.dataframe(
    songs.head(10),
    use_container_width=True,
)