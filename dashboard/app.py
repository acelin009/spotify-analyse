# app.py - Spotify Music Intelligence Dashboard

import streamlit as st
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_data
import pandas as pd
import numpy as np
from PIL import Image

# -----------------------------
# Page Configuration
# -----------------------------

# Try to load logo for favicon
logo_path = Path(__file__).parent / "assets" / "spotify_logo.png"
if logo_path.exists():
    try:
        favicon = Image.open(logo_path)
        st.set_page_config(
            page_title="Spotify Music Intelligence",
            page_icon=favicon,
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except:
        st.set_page_config(
            page_title="Spotify Music Intelligence",
            page_icon="🎵",
            layout="wide",
            initial_sidebar_state="expanded"
        )
else:
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
    css_file = Path(__file__).parent / "assets" / "styles.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # Premium Spotify-inspired CSS
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
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Main container */
        .main > div {
            padding: 0.5rem 2rem 1rem 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        /* Sidebar - Spotify black */
        .css-1d391kg, .css-12oz5g7 {
            background-color: #000000 !important;
        }
        
        /* Remove padding from sidebar top */
        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 0rem !important;
        }
        
        /* Add Spotify branding above navigation using pseudo-elements */
        section[data-testid="stSidebarNav"]::before {
            content: "";
            display: block;
            background-image: url("https://upload.wikimedia.org/wikipedia/commons/8/84/Spotify_icon.svg");
            background-repeat: no-repeat;
            background-size: 52px;
            background-position: center;
            width: 100%;
            height: 60px;
            margin: 16px 0 4px 0;
        }
        
        section[data-testid="stSidebarNav"]::after {
            content: "Spotify\nMusic Intelligence";
            white-space: pre;
            display: block;
            text-align: center;
            color: #FFFFFF;
            font-size: 22px;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 20px;
            letter-spacing: -0.5px;
        }
        
        /* Style Streamlit's navigation */
        section[data-testid="stSidebarNav"] {
            margin-top: 0px !important;
        }
        
        section[data-testid="stSidebarNav"] a {
            border-radius: 10px;
            padding: 10px 14px;
            margin-bottom: 4px;
            color: #B3B3B3 !important;
            font-weight: 500;
            transition: all 0.2s ease;
            font-size: 0.95rem;
        }
        
        section[data-testid="stSidebarNav"] a:hover {
            background: #282828 !important;
            color: #FFFFFF !important;
        }
        
        section[data-testid="stSidebarNav"] a[aria-current="page"] {
            background: #282828 !important;
            color: #FFFFFF !important;
            border-left: 4px solid #1DB954 !important;
        }
        
        /* Premium cards */
        .spotify-card {
            background: #181818;
            border-radius: 20px;
            padding: 24px;
            border: 1px solid #282828;
            transition: all 0.25s ease;
            margin-bottom: 16px;
        }
        
        .spotify-card:hover {
            border-color: #1DB954;
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.6);
        }
        
        /* KPI Cards */
        .kpi-card {
            background: #181818;
            border-radius: 18px;
            padding: 20px 24px;
            border: 1px solid #282828;
            transition: all 0.25s ease;
        }
        
        .kpi-card:hover {
            border-color: #1DB954;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.5);
        }
        
        .kpi-value {
            font-size: 3.25rem;
            font-weight: 800;
            color: #FFFFFF;
            margin: 8px 0 4px 0;
            letter-spacing: -1px;
            line-height: 1.1;
        }
        
        .kpi-label {
            font-size: 0.9rem;
            color: #B3B3B3;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 600;
        }
        
        .kpi-delta {
            font-size: 0.85rem;
            color: #1DB954;
            font-weight: 500;
        }
        
        /* Chart container */
        .chart-card {
            background: #181818;
            border-radius: 18px;
            padding: 24px;
            border: 1px solid #282828;
            margin-bottom: 16px;
            transition: all 0.25s ease;
        }
        
        .chart-card:hover {
            border-color: #282828;
        }
        
        .chart-title {
            color: #FFFFFF;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 16px;
            letter-spacing: -0.3px;
        }
        
        /* Typography */
        .hero-title {
            font-size: 4.8rem;
            font-weight: 900;
            color: #FFFFFF;
            letter-spacing: -3px;
            line-height: 1;
            margin-bottom: 6px;
        }
        
        .hero-subtitle {
            font-size: 1.25rem;
            color: #B3B3B3;
            font-weight: 400;
            margin-bottom: 10px;
            letter-spacing: -0.2px;
        }
        
        .hero-stats {
            font-size: 1rem;
            color: #666;
            font-weight: 400;
        }
        
        .hero-stats span {
            color: #B3B3B3;
        }
        
        .hero-stats .separator {
            color: #282828;
            margin: 0 14px;
        }
        
        .section-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 20px;
            letter-spacing: -0.5px;
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
# Main Content
# -----------------------------

# Header with Spotify logo and title
logo_path = Path(__file__).parent / "assets" / "spotify_logo.png"

if logo_path.exists():
    col_logo, col_title = st.columns([0.8, 14])
    with col_logo:
        st.image(str(logo_path), width=110)
    with col_title:
        st.markdown("""
        <div class="hero-title">Spotify Music Intelligence</div>
        <div class="hero-subtitle">Interactive Music Analytics Platform</div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 8px;">
        <div style="background: #1DB954; width: 72px; height: 72px; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 900; color: #000000;">S</div>
        <div>
            <div class="hero-title">Spotify Music Intelligence</div>
            <div class="hero-subtitle">Interactive Music Analytics Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Stats line
st.markdown(f"""
<div class="hero-stats">
    <span>{len(songs):,}</span> songs
    <span class="separator">•</span>
    <span>{songs['artists'].nunique():,}</span> artists
    <span class="separator">•</span>
    <span>{len(genres):,}</span> genres
    <span class="separator">•</span>
    <span>{years['year'].min()}–{years['year'].max()}</span> years
</div>
""", unsafe_allow_html=True)

# Add spacing
st.markdown("<div style='height: 36px;'></div>", unsafe_allow_html=True)

# -----------------------------
# KPI Cards - Spotify Style
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Songs</div>
        <div class="kpi-value">{len(songs):,}</div>
        <div class="kpi-delta">▲ {len(songs) // 1000}K tracks</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Artists</div>
        <div class="kpi-value">{songs['artists'].nunique():,}</div>
        <div class="kpi-delta">▲ Diverse catalog</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Genres</div>
        <div class="kpi-value">{len(genres):,}</div>
        <div class="kpi-delta">▲ Musical variety</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_pop = songs['popularity'].mean()
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Avg Popularity</div>
        <div class="kpi-value">{avg_pop:.1f}</div>
        <div class="kpi-delta">▲ Industry benchmark</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# Charts Section
# -----------------------------

# Popularity Distribution
st.markdown("""
<div class="chart-card">
    <div class="chart-title">Popularity Distribution</div>
""", unsafe_allow_html=True)

popularity_fig = px.histogram(
    songs,
    x="popularity",
    nbins=30,
    color_discrete_sequence=["#1DB954"]
)

popularity_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
    showlegend=False,
    margin=dict(l=10, r=10, t=10, b=10),
    height=350,
    xaxis=dict(
        gridcolor="#282828",
        title_font=dict(color="#B3B3B3"),
        tickfont=dict(color="#B3B3B3"),
        zeroline=False
    ),
    yaxis=dict(
        gridcolor="#282828",
        title_font=dict(color="#B3B3B3"),
        tickfont=dict(color="#B3B3B3"),
        zeroline=False
    ),
    bargap=0.1
)

popularity_fig.update_traces(
    marker=dict(line=dict(width=0))
)

st.plotly_chart(popularity_fig, use_container_width=True, config={"displayModeBar": False})
st.markdown("</div>", unsafe_allow_html=True)

# Two column layout for charts
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Top Artists</div>
    """, unsafe_allow_html=True)
    
    top_artists = artists.sort_values("popularity", ascending=False).head(10)
    
    artist_fig = px.bar(
        top_artists,
        x="popularity",
        y="artists",
        orientation="h",
        color="popularity",
        color_continuous_scale=["#169C46", "#1DB954", "#1ED760"],
        text_auto='.1f'
    )
    
    artist_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=400,
        xaxis=dict(
            gridcolor="#282828",
            range=[0, 100],
            title_font=dict(color="#B3B3B3"),
            tickfont=dict(color="#B3B3B3"),
            zeroline=False
        ),
        yaxis=dict(
            gridcolor="#282828",
            title_font=dict(color="#B3B3B3"),
            tickfont=dict(color="#B3B3B3"),
            zeroline=False
        )
    )
    
    artist_fig.update_traces(
        textposition='outside',
        textfont=dict(color="#B3B3B3")
    )
    
    st.plotly_chart(artist_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Popularity Over Time</div>
    """, unsafe_allow_html=True)
    
    year_fig = px.line(
        years,
        x="year",
        y="popularity",
        markers=True,
        color_discrete_sequence=["#1DB954"]
    )
    
    year_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=400,
        xaxis=dict(
            gridcolor="#282828",
            title_font=dict(color="#B3B3B3"),
            tickfont=dict(color="#B3B3B3"),
            zeroline=False
        ),
        yaxis=dict(
            gridcolor="#282828",
            title_font=dict(color="#B3B3B3"),
            tickfont=dict(color="#B3B3B3"),
            zeroline=False
        )
    )
    
    year_fig.update_traces(
        line=dict(width=2),
        marker=dict(size=6)
    )
    
    st.plotly_chart(year_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Navigation Cards
# -----------------------------

st.markdown('<div class="section-title">Explore</div>', unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    st.markdown("""
    <div class="spotify-card" style="text-align: center;">
        <div style="font-size: 2.2rem; margin-bottom: 8px;">♫</div>
        <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">Song Explorer</div>
        <div style="color: #B3B3B3; font-size: 0.9rem;">Search & filter songs</div>
    </div>
    """, unsafe_allow_html=True)

with nav_col2:
    st.markdown("""
    <div class="spotify-card" style="text-align: center;">
        <div style="font-size: 2.2rem; margin-bottom: 8px;">◎</div>
        <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">Artists</div>
        <div style="color: #B3B3B3; font-size: 0.9rem;">Compare artist profiles</div>
    </div>
    """, unsafe_allow_html=True)

with nav_col3:
    st.markdown("""
    <div class="spotify-card" style="text-align: center;">
        <div style="font-size: 2.2rem; margin-bottom: 8px;">◈</div>
        <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">Genres</div>
        <div style="color: #B3B3B3; font-size: 0.9rem;">Genre comparison & heatmaps</div>
    </div>
    """, unsafe_allow_html=True)

nav_col4, nav_col5, nav_col6 = st.columns(3)

with nav_col4:
    st.markdown("""
    <div class="spotify-card" style="text-align: center;">
        <div style="font-size: 2.2rem; margin-bottom: 8px;">↗</div>
        <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">Trends</div>
        <div style="color: #B3B3B3; font-size: 0.9rem;">Time-series analysis</div>
    </div>
    """, unsafe_allow_html=True)

with nav_col5:
    st.markdown("""
    <div class="spotify-card" style="text-align: center;">
        <div style="font-size: 2.2rem; margin-bottom: 8px;">◉</div>
        <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">ML Predictor</div>
        <div style="color: #B3B3B3; font-size: 0.9rem;">Predict song popularity</div>
    </div>
    """, unsafe_allow_html=True)

with nav_col6:
    st.markdown("""
    <div class="spotify-card" style="text-align: center;">
        <div style="font-size: 2.2rem; margin-bottom: 8px;">⌂</div>
        <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">Home</div>
        <div style="color: #B3B3B3; font-size: 0.9rem;">Dashboard overview</div>
    </div>
    """, unsafe_allow_html=True)