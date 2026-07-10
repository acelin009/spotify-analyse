# app.py - Spotify Music Intelligence Dashboard

import streamlit as st
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_data
import pandas as pd
import numpy as np
from PIL import Image
import base64

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
        st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

load_css()

# -----------------------------
# Main Content
# -----------------------------

# Hero Wrapper - Compact
st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)

# Hero Header - Flex Layout
logo_path = Path(__file__).parent / "assets" / "spotify_logo.png"

if logo_path.exists():
    # Convert image to base64 for use in HTML
    with open(logo_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    
    st.markdown(f"""
    <div class="hero-header">
        <img src="data:image/png;base64,{img_base64}" class="hero-logo" alt="Spotify Logo">
        <div>
            <div class="hero-title">Spotify Music Intelligence</div>
            <div class="hero-subtitle">Interactive Music Analytics Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="hero-header">
        <div style="background: #1DB954; width: 120px; height: 120px; border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 56px; font-weight: 900; color: #000000; flex-shrink: 0;">S</div>
        <div>
            <div class="hero-title">Spotify Music Intelligence</div>
            <div class="hero-subtitle">Interactive Music Analytics Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Minimal spacing - cards almost touch hero
st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

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

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# -----------------------------
# Charts Section - No Section Titles
# -----------------------------

# Popularity Distribution
st.markdown('<div class="chart-card">', unsafe_allow_html=True)

popularity_fig = px.histogram(
    songs,
    x="popularity",
    nbins=30,
    color_discrete_sequence=["#1DB954"],
    title="Popularity Distribution"
)

popularity_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
    showlegend=False,
    margin=dict(l=10, r=10, t=40, b=10),
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
    bargap=0.1,
    title_font=dict(color="#FFFFFF", size=16)
)

popularity_fig.update_traces(
    marker=dict(line=dict(width=0))
)

st.plotly_chart(popularity_fig, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Two column layout for charts
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    
    top_artists = artists.sort_values("popularity", ascending=False).head(10)
    
    artist_fig = px.bar(
        top_artists,
        x="popularity",
        y="artists",
        orientation="h",
        color="popularity",
        color_continuous_scale=["#169C46", "#1DB954", "#1ED760"],
        text_auto='.1f',
        title="Top Artists"
    )
    
    artist_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=10),
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
        ),
        title_font=dict(color="#FFFFFF", size=16)
    )
    
    artist_fig.update_traces(
        textposition='outside',
        textfont=dict(color="#B3B3B3")
    )
    
    st.plotly_chart(artist_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    
    year_fig = px.line(
        years,
        x="year",
        y="popularity",
        markers=True,
        color_discrete_sequence=["#1DB954"],
        title="Popularity Over Time"
    )
    
    year_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=10),
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
        ),
        title_font=dict(color="#FFFFFF", size=16)
    )
    
    year_fig.update_traces(
        line=dict(width=2),
        marker=dict(size=6)
    )
    
    st.plotly_chart(year_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# -----------------------------
# Navigation Cards - No Section Title
# -----------------------------

nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    st.markdown("""
    <div class="spotify-card" style="text-align: center;">
        <div style="font-size: 2.4rem; margin-bottom: 6px;">♫</div>
        <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">Song Explorer</div>
        <div style="color: #B3B3B3; font-size: 0.85rem;">Search & filter songs</div>
    </div>
    """, unsafe_allow_html=True)

with nav_col2:
    st.markdown("""
    <div class="spotify-card" style="text-align: center;">
        <div style="font-size: 2.4rem; margin-bottom: 6px;">◎</div>
        <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">Artists</div>
        <div style="color: #B3B3B3; font-size: 0.85rem;">Compare artist profiles</div>
    </div>
    """, unsafe_allow_html=True)

with nav_col3:
    st.markdown("""
    <div class="spotify-card" style="text-align: center;">
        <div style="font-size: 2.4rem; margin-bottom: 6px;">◈</div>
        <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">Genres</div>
        <div style="color: #B3B3B3; font-size: 0.85rem;">Genre comparison & heatmaps</div>
    </div>
    """, unsafe_allow_html=True)

nav_col4, nav_col5, nav_col6 = st.columns(3)

with nav_col4:
    st.markdown("""
    <div class="spotify-card" style="text-align: center;">
        <div style="font-size: 2.4rem; margin-bottom: 6px;">↗</div>
        <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">Trends</div>
        <div style="color: #B3B3B3; font-size: 0.85rem;">Time-series analysis</div>
    </div>
    """, unsafe_allow_html=True)

with nav_col5:
    st.markdown("""
    <div class="spotify-card" style="text-align: center;">
        <div style="font-size: 2.4rem; margin-bottom: 6px;">◉</div>
        <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">ML Predictor</div>
        <div style="color: #B3B3B3; font-size: 0.85rem;">Predict song popularity</div>
    </div>
    """, unsafe_allow_html=True)

with nav_col6:
    st.markdown("""
    <div class="spotify-card" style="text-align: center;">
        <div style="font-size: 2.4rem; margin-bottom: 6px;">⌂</div>
        <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">Home</div>
        <div style="color: #B3B3B3; font-size: 0.85rem;">Dashboard overview</div>
    </div>
    """, unsafe_allow_html=True)