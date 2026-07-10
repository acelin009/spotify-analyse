# app.py - Spotify Music Intelligence Dashboard (REFACTORED - FIXED)

import streamlit as st
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_data
import pandas as pd
import numpy as np
from PIL import Image
import base64
import random

# -----------------------------
# Page Configuration
# -----------------------------

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

# Hero Wrapper
st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)

logo_path = Path(__file__).parent / "assets" / "spotify_logo.png"

if logo_path.exists():
    with open(logo_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    
    st.markdown(f"""
    <div class="hero-header">
        <img src="data:image/png;base64,{img_base64}" class="hero-logo" alt="Spotify Logo">
        <div>
            <div class="hero-title">Spotify Music Intelligence</div>
            <div class="hero-subtitle">Interactive analytics platform exploring over 170,000 Spotify tracks using data visualization, statistical analysis and machine learning.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="hero-header">
        <div style="background: #1DB954; width: 120px; height: 120px; border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 56px; font-weight: 900; color: #000000; flex-shrink: 0;">S</div>
        <div>
            <div class="hero-title">Spotify Music Intelligence</div>
            <div class="hero-subtitle">Interactive analytics platform exploring over 170,000 Spotify tracks using data visualization, statistical analysis and machine learning.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

# -----------------------------
# KPI Cards - Now 5 cards with real metadata
# -----------------------------

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Tracks Available</div>
        <div class="kpi-value">{len(songs):,}</div>
        <div class="kpi-delta">Total songs in dataset</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Unique Artists</div>
        <div class="kpi-value">{songs['artists'].nunique():,}</div>
        <div class="kpi-delta">Distinct performers</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Genres Mapped</div>
        <div class="kpi-value">{len(genres):,}</div>
        <div class="kpi-delta">Musical categories</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_pop = songs['popularity'].mean()
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Avg Popularity</div>
        <div class="kpi-value">{avg_pop:.1f}</div>
        <div class="kpi-delta">Industry benchmark</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    min_year = songs['year'].min()
    max_year = songs['year'].max()
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Years Covered</div>
        <div class="kpi-value">{min_year}–{max_year}</div>
        <div class="kpi-delta">{max_year - min_year} years of music</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# -----------------------------
# "Did You Know?" Card - Rotating Insights
# -----------------------------

# Prepare insights with error handling
try:
    most_popular = songs.loc[songs['popularity'].idxmax()]
except:
    most_popular = None

try:
    # Check if genres has 'count' column, if not create it
    if 'count' not in genres.columns:
        # Count songs per genre using songs_with_genres if available
        if len(songs_with_genres) > 0:
            genre_counts = songs_with_genres['genres'].value_counts().reset_index()
            genre_counts.columns = ['genres', 'count']
            genres = genres.merge(genre_counts, on='genres', how='left')
            genres['count'] = genres['count'].fillna(0)
        else:
            # Fallback: count occurrences in songs
            genre_counts = songs['track_genre'].value_counts().reset_index()
            genre_counts.columns = ['genres', 'count']
            genres = genres.merge(genre_counts, on='genres', how='left')
            genres['count'] = genres['count'].fillna(0)
    
    top_genre = genres.sort_values('count', ascending=False).iloc[0]
except:
    top_genre = None

try:
    oldest_song = songs.loc[songs['year'].idxmin()]
except:
    oldest_song = None

try:
    most_prolific = artists.sort_values('popularity', ascending=False).iloc[0]
except:
    most_prolific = None

# Build insights list with fallbacks
insights = []

if most_popular is not None:
    insights.append(f"🎵 The most popular track is **{most_popular['name']}** by **{most_popular['artists']}** with a popularity score of **{most_popular['popularity']}**.")

if top_genre is not None:
    try:
        insights.append(f"🎵 The most represented genre is **{top_genre['genres']}** with **{int(top_genre['count']):,}** songs.")
    except:
        insights.append(f"🎵 The most represented genre is **{top_genre['genres']}**.")

if oldest_song is not None:
    insights.append(f"🎵 The oldest song in the dataset is **{oldest_song['name']}** released in **{oldest_song['year']}**.")

if most_prolific is not None:
    insights.append(f"🎵 **{most_prolific['artists']}** has the highest average popularity at **{most_prolific['popularity']:.1f}** across their tracks.")

# Fallback if no insights could be generated
if not insights:
    insights = [
        "🎵 This dataset contains over 170,000 Spotify tracks for analysis.",
        "🎵 Explore songs, artists, genres, and trends in this interactive dashboard.",
        "🎵 Use the ML Predictor to forecast song popularity."
    ]

selected_insight = random.choice(insights)

st.markdown(f"""
<div class="chart-card" style="background: linear-gradient(135deg, #1DB95415 0%, #1DB95405 100%); border-left: 4px solid #1DB954; padding: 20px;">
    <div style="font-size: 1.1rem; color: #FFFFFF; font-weight: 500;">
        {selected_insight}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# -----------------------------
# Section: Genre Mix (Donut Chart)
# -----------------------------

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

# Get top genres for donut chart with error handling
try:
    if 'count' in genres.columns:
        top_n_genres = genres.sort_values('count', ascending=False).head(6)
        other_count = genres['count'].sum() - top_n_genres['count'].sum()
        
        genre_pie_data = pd.DataFrame({
            'genre': list(top_n_genres['genres']) + ['Other'],
            'count': list(top_n_genres['count']) + [other_count]
        })
    else:
        # Fallback: use songs_with_genres
        if len(songs_with_genres) > 0:
            genre_counts = songs_with_genres['genres'].value_counts().reset_index()
            genre_counts.columns = ['genre', 'count']
            top_n_genres = genre_counts.head(6)
            other_count = genre_counts['count'].sum() - top_n_genres['count'].sum()
            
            genre_pie_data = pd.DataFrame({
                'genre': list(top_n_genres['genre']) + ['Other'],
                'count': list(top_n_genres['count']) + [other_count]
            })
        else:
            # Final fallback: use track_genre from songs
            genre_counts = songs['track_genre'].value_counts().reset_index()
            genre_counts.columns = ['genre', 'count']
            top_n_genres = genre_counts.head(6)
            other_count = genre_counts['count'].sum() - top_n_genres['count'].sum()
            
            genre_pie_data = pd.DataFrame({
                'genre': list(top_n_genres['genre']) + ['Other'],
                'count': list(top_n_genres['count']) + [other_count]
            })

    genre_fig = px.pie(
        genre_pie_data,
        values='count',
        names='genre',
        title='Genre Distribution',
        color_discrete_sequence=['#1DB954', '#1ED760', '#169C46', '#0D7C3A', '#1DB95480', '#1DB95460', '#282828'],
        hole=0.4
    )

    genre_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(color="#B3B3B3", size=11)
        ),
        margin=dict(l=10, r=10, t=40, b=40),
        height=400,
        title_font=dict(color="#FFFFFF", size=16)
    )

    genre_fig.update_traces(
        textinfo='percent',
        textfont=dict(color="#FFFFFF", size=12),
        hoverinfo='label+value+percent',
        pull=[0.05, 0, 0, 0, 0, 0, 0]
    )

    st.plotly_chart(genre_fig, use_container_width=True, config={"displayModeBar": False})
except Exception as e:
    st.warning(f"Could not generate genre distribution chart: {e}")
    
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# -----------------------------
# Two column layout: Top Artists Preview + Songs by Decade
# -----------------------------

col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    
    # Top 5 artists only (preview)
    top_artists = artists.sort_values("popularity", ascending=False).head(5)
    
    artist_fig = px.bar(
        top_artists,
        x="popularity",
        y="artists",
        orientation="h",
        color="popularity",
        color_continuous_scale=["#169C46", "#1DB954", "#1ED760"],
        title="Top 5 Artists",
        text_auto='.1f'
    )
    
    artist_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
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
        title_font=dict(color="#FFFFFF", size=14)
    )
    
    artist_fig.update_traces(
        textposition='outside',
        textfont=dict(color="#B3B3B3")
    )
    
    st.plotly_chart(artist_fig, use_container_width=True, config={"displayModeBar": False})
    
    # Navigation link using st.page_link
    st.page_link("pages/2_Artists.py", label="View full artist analysis →", icon="🎵")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    
    # Songs by Decade (replaces popularity over time)
    songs['decade'] = (songs['year'] // 10) * 10
    decade_counts = songs.groupby('decade').size().reset_index(name='count')
    decade_counts = decade_counts[decade_counts['decade'] > 0]
    
    decade_fig = px.bar(
        decade_counts,
        x='decade',
        y='count',
        color='count',
        color_continuous_scale=['#169C46', '#1DB954', '#1ED760'],
        title="Songs by Decade",
        labels={'count': 'Number of Songs', 'decade': 'Decade'}
    )
    
    decade_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
        xaxis=dict(
            gridcolor="#282828",
            tickangle=45,
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
        title_font=dict(color="#FFFFFF", size=14),
        bargap=0.15
    )
    
    decade_fig.update_traces(
        marker=dict(line=dict(width=0))
    )
    
    st.plotly_chart(decade_fig, use_container_width=True, config={"displayModeBar": False})
    
    # Navigation link using st.page_link
    st.page_link("pages/5_Trends.py", label="Explore trends over time →", icon="📈")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# -----------------------------
# Interactive Navigation Cards with st.page_link
# -----------------------------

st.markdown("""
<div style="margin-bottom: 12px;">
    <div style="color: #FFFFFF; font-size: 1.2rem; font-weight: 600;">Explore the Dashboard</div>
    <div style="color: #B3B3B3; font-size: 0.9rem;">Choose a section to dive deeper into the data</div>
</div>
""", unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    with st.container():
        st.markdown(f"""
        <div class="spotify-card" style="text-align: center; padding: 20px;">
            <div style="font-size: 2.4rem; margin-bottom: 6px;">♫</div>
            <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">Song Explorer</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">Search & filter {len(songs):,} songs</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/3_Song_Explorer.py", label="Open →", use_container_width=True)

with nav_col2:
    with st.container():
        st.markdown(f"""
        <div class="spotify-card" style="text-align: center; padding: 20px;">
            <div style="font-size: 2.4rem; margin-bottom: 6px;">◎</div>
            <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">Artists</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">{songs['artists'].nunique():,} artist profiles</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/2_Artists.py", label="Open →", use_container_width=True)

with nav_col3:
    with st.container():
        st.markdown(f"""
        <div class="spotify-card" style="text-align: center; padding: 20px;">
            <div style="font-size: 2.4rem; margin-bottom: 6px;">◈</div>
            <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">Genres</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">{len(genres):,} genre categories</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/4_Genres.py", label="Open →", use_container_width=True)

nav_col4, nav_col5, nav_col6 = st.columns(3)

with nav_col4:
    with st.container():
        st.markdown("""
        <div class="spotify-card" style="text-align: center; padding: 20px;">
            <div style="font-size: 2.4rem; margin-bottom: 6px;">↗</div>
            <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">Trends</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">Time-series analysis</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/5_Trends.py", label="Open →", use_container_width=True)

with nav_col5:
    with st.container():
        st.markdown("""
        <div class="spotify-card" style="text-align: center; padding: 20px;">
            <div style="font-size: 2.4rem; margin-bottom: 6px;">◉</div>
            <div style="color: #FFFFFF; font-weight: 600; font-size: 1.1rem;">ML Predictor</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">Predict song popularity</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/6_ML_Predictor.py", label="Open →", use_container_width=True)

with nav_col6:
    with st.container():
        st.markdown("""
        <div class="spotify-card" style="text-align: center; background: #1DB95415; border: 1px solid #1DB954; padding: 20px;">
            <div style="font-size: 2.4rem; margin-bottom: 6px;">⌂</div>
            <div style="color: #1DB954; font-weight: 600; font-size: 1.1rem;">Home</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">Dashboard overview</div>
            <div style="color: #1DB954; font-size: 0.8rem; margin-top: 6px;">◀ Active</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# -----------------------------
# Dashboard Journey Footer
# -----------------------------

st.markdown("""
<div style="
    background: linear-gradient(135deg, #181818 0%, #282828 100%);
    border-radius: 12px;
    padding: 24px 32px;
    border: 1px solid #282828;
">
    <div style="color: #FFFFFF; font-weight: 600; font-size: 1rem; margin-bottom: 12px;">Dashboard Journey</div>
    <div style="display: flex; flex-wrap: wrap; gap: 12px; align-items: center;">
        <span style="color: #1DB954; font-weight: 500;">Overview</span>
        <span style="color: #404040;">→</span>
        <span style="color: #B3B3B3;">Song Explorer</span>
        <span style="color: #404040;">→</span>
        <span style="color: #B3B3B3;">Artists</span>
        <span style="color: #404040;">→</span>
        <span style="color: #B3B3B3;">Genres</span>
        <span style="color: #404040;">→</span>
        <span style="color: #B3B3B3;">Trends</span>
        <span style="color: #404040;">→</span>
        <span style="color: #B3B3B3;">ML Prediction</span>
    </div>
    <div style="color: #B3B3B3; font-size: 0.8rem; margin-top: 8px;">
        💡 Start with Overview to understand the dataset, then explore each section
    </div>
</div>
""", unsafe_allow_html=True)