# dashboard/pages/2_Song_Explorer.py

import streamlit as st
import pandas as pd

from data_loader import load_data

# Page Configuration
st.set_page_config(
    page_title="Song Explorer",
    page_icon="🎵",
    layout="wide"
)

# Load Data
songs, artists, genres, years, songs_with_genres = load_data()

# Cached functions for performance
@st.cache_data
def convert_csv(df):
    """Convert dataframe to CSV with caching."""
    return df.to_csv(index=False).encode("utf-8")

# Page Title
st.title("🎵 Song Explorer")
st.write(
    """
    Search, filter and explore Spotify songs. Use the filters below to narrow down 
    your search and discover insights about your favorite tracks.
    """
)

# Create a copy of the original dataframe for filtering
filtered = songs.copy()

# Sidebar or Top Filters - Let's use columns for a cleaner layout
st.markdown("---")

# Row 1: Search and Artist Filter
col1, col2 = st.columns([2, 1])

with col1:
    search = st.text_input(
        "🔍 Search Song",
        placeholder="Type a song name...",
        help="Search for songs by name (case-insensitive)"
    )

with col2:
    # Artist Search - using text_input for better performance with large datasets
    artist_search = st.text_input(
        "🎤 Search Artist",
        placeholder="Type an artist name...",
        help="Search for artists (case-insensitive, partial matches supported)"
    )

# Row 2: Year and Popularity Sliders
col3, col4 = st.columns(2)

with col3:
    year_range = st.slider(
        "📅 Release Year",
        int(songs["year"].min()),
        int(songs["year"].max()),
        (
            int(songs["year"].min()),
            int(songs["year"].max())
        ),
        help="Select a range of release years"
    )

with col4:
    popularity = st.slider(
        "⭐ Popularity",
        0,
        100,
        (0, 100),
        help="Filter songs by popularity score (0-100)"
    )

# Row 3: Explicit Filter
col5, col6 = st.columns([1, 3])

with col5:
    explicit = st.selectbox(
        "🔞 Explicit Content",
        ["All", "Yes", "No"],
        help="Filter songs by explicit content label"
    )

st.markdown("---")

# Apply all filters

# 1. Search filter
if search:
    filtered = filtered[
        filtered["name"]
        .str.contains(search, case=False, na=False)
    ]

# 2. Artist filter - using text search
if artist_search:
    filtered = filtered[
        filtered["artists"]
        .str.contains(artist_search, case=False, na=False)
    ]

# 3. Year range filter
filtered = filtered[
    filtered["year"].between(
        year_range[0],
        year_range[1]
    )
]

# 4. Popularity filter
filtered = filtered[
    filtered["popularity"].between(
        popularity[0],
        popularity[1]
    )
]

# 5. Explicit filter
if explicit == "Yes":
    filtered = filtered[
        filtered["explicit"] == 1
    ]
elif explicit == "No":
    filtered = filtered[
        filtered["explicit"] == 0
    ]

# Display Results Count
st.subheader(f"Showing {len(filtered):,} Songs")

# Summary Metrics Row
col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)

with col_metric1:
    st.metric(
        "Total Songs Found",
        f"{len(filtered):,}"
    )

with col_metric2:
    avg_popularity = filtered['popularity'].mean()
    st.metric(
        "Average Popularity",
        f"{avg_popularity:.1f}" if not filtered.empty else "N/A",
        delta=f"{avg_popularity - songs['popularity'].mean():.1f}" if not filtered.empty else None
    )

with col_metric3:
    avg_danceability = filtered['danceability'].mean()
    st.metric(
        "Average Danceability",
        f"{avg_danceability:.2f}" if not filtered.empty else "N/A"
    )

with col_metric4:
    avg_energy = filtered['energy'].mean()
    st.metric(
        "Average Energy",
        f"{avg_energy:.2f}" if not filtered.empty else "N/A"
    )

st.markdown("---")

# Interactive Data Table - Only show first 1000 rows for performance
MAX_ROWS = 1000
display_df = filtered.head(MAX_ROWS)

st.dataframe(
    display_df,
    use_container_width=True,
    height=600,
    column_config={
        "name": "Song Name",
        "artists": "Artist",
        "year": "Year",
        "popularity": st.column_config.NumberColumn(
            "Popularity",
            help="Popularity score (0-100)",
            format="%d"
        ),
        "danceability": st.column_config.NumberColumn(
            "Danceability",
            format="%.2f"
        ),
        "energy": st.column_config.NumberColumn(
            "Energy",
            format="%.2f"
        ),
        "explicit": st.column_config.CheckboxColumn(
            "Explicit",
            help="Whether the song contains explicit content"
        ),
    }
)

# Show warning if more rows exist
if len(filtered) > MAX_ROWS:
    st.warning(
        f"Showing the first {MAX_ROWS:,} of {len(filtered):,} matching songs. "
        "Use the filters to narrow down the results."
    )

# Download Section
st.markdown("---")
col_download1, col_download2, col_download3 = st.columns([1, 2, 1])

with col_download2:
    # Create CSV - using cached function
    csv = convert_csv(filtered)
    
    st.download_button(
        "⬇ Download Filtered Data (CSV)",
        csv,
        file_name=f"filtered_spotify_songs_{len(filtered)}.csv",
        mime="text/csv",
        use_container_width=True,
        help="Download the current filtered results as a CSV file"
    )

# Additional Info about current filter state
st.markdown("---")
with st.expander("🔍 Current Filter Summary"):
    st.write(f"**Search Term:** {search if search else 'None'}")
    st.write(f"**Artist Search:** {artist_search if artist_search else 'None'}")
    st.write(f"**Year Range:** {year_range[0]} - {year_range[1]}")
    st.write(f"**Popularity Range:** {popularity[0]} - {popularity[1]}")
    st.write(f"**Explicit Content:** {explicit}")
    st.write(f"**Total Records After Filtering:** {len(filtered):,}")

# Footer with data freshness info
st.markdown("---")
st.caption(f"Data last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption(f"Total songs in dataset: {len(songs):,}")