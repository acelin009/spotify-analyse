# dashboard/pages/2_Song_Explorer.py

import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image
import plotly.express as px
import base64

from data_loader import load_data

# -----------------------------
# Page Configuration
# -----------------------------

# Load logo for favicon
logo_path = Path(__file__).parent.parent / "assets" / "spotify_logo.png"
if logo_path.exists():
    try:
        favicon = Image.open(logo_path)
        st.set_page_config(
            page_title="Song Explorer • Spotify Music Intelligence",
            page_icon=favicon,
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except:
        st.set_page_config(
            page_title="Song Explorer • Spotify Music Intelligence",
            page_icon="",
            layout="wide",
            initial_sidebar_state="expanded"
        )
else:
    st.set_page_config(
        page_title="Song Explorer • Spotify Music Intelligence",
        page_icon="",
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
    css_file = Path(__file__).parent.parent / "assets" / "styles.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Import Inter font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
        
        /* Global styles */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }
        
        /* Main container */
        .main > div {
            padding: 0.5rem 2rem 1rem 2rem !important;
            max-width: 1400px !important;
            margin: 0 auto !important;
        }
        
        /* Hero Title */
        div.hero-title {
            font-size: 76px !important;
            font-weight: 900 !important;
            color: #FFFFFF !important;
            letter-spacing: -3px !important;
            line-height: 1 !important;
            margin-bottom: 4px !important;
        }
        
        div.hero-subtitle {
            font-size: 22px !important;
            color: #B3B3B3 !important;
            font-weight: 400 !important;
            margin-top: 4px !important;
            letter-spacing: -0.3px !important;
        }
        
        /* Section Title */
        div.section-title {
            font-size: 34px !important;
            font-weight: 800 !important;
            color: #FFFFFF !important;
            margin-bottom: 24px !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
        }
        
        /* KPI Cards */
        div.kpi-card {
            background: #181818 !important;
            border-radius: 18px !important;
            padding: 20px 24px !important;
            border: 1px solid #282828 !important;
            transition: all 0.25s ease !important;
        }
        
        div.kpi-card:hover {
            border-color: #1DB954 !important;
            transform: translateY(-4px) !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.5) !important;
        }
        
        div.kpi-value {
            font-size: 48px !important;
            font-weight: 900 !important;
            color: #FFFFFF !important;
            margin: 8px 0 4px 0 !important;
            letter-spacing: -2px !important;
            line-height: 1.1 !important;
        }
        
        div.kpi-label {
            font-size: 14px !important;
            color: #B3B3B3 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.8px !important;
            font-weight: 600 !important;
        }
        
        div.kpi-delta {
            font-size: 0.85rem !important;
            color: #1DB954 !important;
            font-weight: 500 !important;
        }
        
        /* Chart container */
        div.chart-card {
            background: #181818 !important;
            border-radius: 18px !important;
            padding: 24px !important;
            border: 1px solid #282828 !important;
            margin-bottom: 16px !important;
            transition: all 0.25s ease !important;
        }
        
        div.chart-card:hover {
            border-color: #282828 !important;
        }
        
        div.chart-title {
            color: #FFFFFF !important;
            font-size: 20px !important;
            font-weight: 700 !important;
            margin-bottom: 16px !important;
            letter-spacing: -0.3px !important;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #121212;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #282828;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #1DB954;
        }
        </style>
        """, unsafe_allow_html=True)

load_css()

# -----------------------------
# Page-specific gradient (Dark Green for Song Explorer)
# -----------------------------

st.markdown("""
<style>
.stApp {
    background:
        linear-gradient(
            180deg,
            #0a4728 0%,
            #083b21 18%,
            #072f1b 35%,
            #061f13 55%,
            #181818 76%,
            #121212 100%
        ) !important;
    background-attachment: fixed !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Cached functions for performance
# -----------------------------

@st.cache_data
def convert_csv(df):
    """Convert dataframe to CSV with caching."""
    return df.to_csv(index=False).encode("utf-8")

@st.cache_data
def get_song_options():
    """Get sorted list of unique song names with 'All' option."""
    song_list = sorted(songs["name"].dropna().unique().tolist())
    return ["All"] + song_list

@st.cache_data
def get_artist_options():
    """Get sorted list of unique artist names with 'All' option."""
    artist_list = sorted(songs["artists"].dropna().unique().tolist())
    return ["All"] + artist_list

# -----------------------------
# Hero Header
# -----------------------------

st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)

logo_path = Path(__file__).parent.parent / "assets" / "spotify_logo.png"

if logo_path.exists():
    with open(logo_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()

    st.markdown(f"""
    <div class="hero-header">
        <img src="data:image/png;base64,{img_base64}" class="hero-logo" alt="Spotify Logo">
        <div>
            <div class="hero-title">Song Explorer</div>
            <div class="hero-subtitle">Search, Filter & Analyze Spotify Tracks</div>
            <p style="color:#B3B3B3; font-size:15px; margin-top:12px; font-weight:500;">
                <b>{len(songs):,}</b> Songs
                &nbsp;&nbsp;•&nbsp;&nbsp;
                <b>{songs['artists'].nunique():,}</b> Artists
                &nbsp;&nbsp;•&nbsp;&nbsp;
                <b>{songs['year'].min()}–{songs['year'].max()}</b>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="hero-header">
        <div style="
            background:#1DB954;
            width:120px;
            height:120px;
            border-radius:20px;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:56px;
            font-weight:900;
            color:#000;
            flex-shrink:0;
        ">
            S
        </div>
        <div>
            <div class="hero-title">Song Explorer</div>
            <div class="hero-subtitle">Search, Filter & Analyze Spotify Tracks</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# -----------------------------
# Filter Section
# -----------------------------

st.markdown('<div class="section-title">Search Filters</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

# Create a copy of the original dataframe for filtering
filtered = songs.copy()

# Row 1: Song Selector and Artist Selector
col1, col2 = st.columns([2, 1])

with col1:
    song_options = get_song_options()
    selected_song = st.selectbox(
        "Song Name",
        options=song_options,
        index=0,
        placeholder="Type to search for a song...",
        label_visibility="collapsed"
    )
    st.caption("Search by song name - type to filter")

with col2:
    artist_options = get_artist_options()
    selected_artist = st.selectbox(
        "Artist Name",
        options=artist_options,
        index=0,
        placeholder="Type to search for an artist...",
        label_visibility="collapsed"
    )
    st.caption("Search by artist name - type to filter")

# Row 2: Year and Popularity Sliders
col3, col4 = st.columns(2)

with col3:
    year_range = st.slider(
        "Release Year",
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
        "Popularity",
        0,
        100,
        (0, 100),
        help="Filter songs by popularity score (0-100)"
    )

# Row 3: Explicit Filter
col5, col6 = st.columns([1, 3])

with col5:
    explicit = st.selectbox(
        "Explicit Content",
        ["All", "Yes", "No"],
        help="Filter songs by explicit content label"
    )

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

# -----------------------------
# Apply all filters
# -----------------------------

# 1. Song filter - exact match if selected (not "All")
if selected_song and selected_song != "All":
    filtered = filtered[filtered["name"] == selected_song]

# 2. Artist filter - exact match if selected (not "All")
if selected_artist and selected_artist != "All":
    filtered = filtered[filtered["artists"] == selected_artist]

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

# -----------------------------
# Results Section
# -----------------------------

st.markdown('<div class="section-title">Search Results</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

# Summary Metrics Row
col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)

with col_metric1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Songs</div>
        <div class="kpi-value">{len(filtered):,}</div>
        <div class="kpi-delta">▲ Filtered results</div>
    </div>
    """, unsafe_allow_html=True)

with col_metric2:
    avg_popularity = filtered['popularity'].mean() if not filtered.empty else 0
    diff = avg_popularity - songs['popularity'].mean()
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Avg Popularity</div>
        <div class="kpi-value">{avg_popularity:.1f}</div>
        <div class="kpi-delta">▲ {diff:+.1f} vs overall</div>
    </div>
    """, unsafe_allow_html=True)

with col_metric3:
    avg_danceability = filtered['danceability'].mean() if not filtered.empty else 0
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Avg Danceability</div>
        <div class="kpi-value">{avg_danceability:.2f}</div>
        <div class="kpi-delta">▲ Audio feature</div>
    </div>
    """, unsafe_allow_html=True)

with col_metric4:
    avg_energy = filtered['energy'].mean() if not filtered.empty else 0
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Avg Energy</div>
        <div class="kpi-value">{avg_energy:.2f}</div>
        <div class="kpi-delta">▲ Audio feature</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

# -----------------------------
# Quick Charts (Feature Distribution)
# -----------------------------

st.markdown('<div class="section-title">Feature Distribution</div>', unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Popularity Distribution</div>
    """, unsafe_allow_html=True)
    
    pop_fig = px.histogram(
        filtered.head(1000),
        x="popularity",
        nbins=20,
        color_discrete_sequence=["#1DB954"]
    )
    
    pop_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B3B3B3", size=11),
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=250,
        xaxis=dict(gridcolor="#282828", zeroline=False),
        yaxis=dict(gridcolor="#282828", zeroline=False)
    )
    
    pop_fig.update_traces(marker=dict(line=dict(width=0)))
    
    st.plotly_chart(pop_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with chart_col2:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Danceability vs Energy</div>
    """, unsafe_allow_html=True)
    
    scatter_fig = px.scatter(
        filtered.head(1000),
        x="danceability",
        y="energy",
        color="popularity",
        color_continuous_scale=["#169C46", "#1DB954", "#1ED760"],
        opacity=0.6
    )
    
    scatter_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B3B3B3", size=11),
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=250,
        xaxis=dict(gridcolor="#282828", zeroline=False),
        yaxis=dict(gridcolor="#282828", zeroline=False)
    )
    
    st.plotly_chart(scatter_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

# -----------------------------
# Data Table
# -----------------------------

st.markdown('<div class="section-title">Raw Song Data</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

# Interactive Data Table - Only show first 1000 rows for performance
MAX_ROWS = 1000
display_df = filtered.head(MAX_ROWS)

st.dataframe(
    display_df,
    use_container_width=True,
    height=500,
    hide_index=True,
    column_config={
        "name": "Song Name",
        "artists": "Artist",
        "year": "Year",
        "popularity": st.column_config.ProgressColumn(
            "Popularity",
            min_value=0,
            max_value=100,
            format="%d",
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

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

# -----------------------------
# Export Section
# -----------------------------

st.markdown('<div class="section-title">Export Filtered Data</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

col_download1, col_download2, col_download3 = st.columns([1, 2, 1])

with col_download2:
    # Create CSV - using cached function
    csv = convert_csv(filtered)
    
    st.download_button(
        "Download CSV",
        csv,
        file_name=f"filtered_spotify_songs_{len(filtered)}.csv",
        mime="text/csv",
        use_container_width=True,
        help="Download the current filtered results as a CSV file"
    )

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

# -----------------------------
# Active Filters (Collapsible)
# -----------------------------

with st.expander("Active Filters"):
    st.markdown(f"""
    - **Song:** {selected_song if selected_song and selected_song != "All" else 'All'}
    - **Artist:** {selected_artist if selected_artist and selected_artist != "All" else 'All'}
    - **Year Range:** {year_range[0]} - {year_range[1]}
    - **Popularity Range:** {popularity[0]} - {popularity[1]}
    - **Explicit Content:** {explicit}
    - **Total Records Found:** {len(filtered):,}
    """)