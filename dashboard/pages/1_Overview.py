import streamlit as st
from data_loader import load_data

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
    st.metric("🎵 Total Songs", f"{total_songs:,}")

with col2:
    st.metric("🎤 Artists", f"{total_artists:,}")

with col3:
    st.metric(
        "⭐ Average Popularity",
        f"{average_popularity:.1f}",
    )

with col4:
    st.metric(
        "📅 Years",
        f"{years_covered[0]} - {years_covered[1]}",
    )

st.divider()

st.subheader("Dataset Preview")

st.dataframe(
    songs.head(10),
    use_container_width=True,
)