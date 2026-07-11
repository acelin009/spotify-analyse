# dashboard/pages/1_Overview.py

import streamlit as st
from pathlib import Path
import plotly.express as px
import pandas as pd
from PIL import Image
from data_loader import load_data
import base64

# -----------------------------
# Page Configuration
# -----------------------------

# Load logo for favicon
logo_path = Path(__file__).parent.parent / "assets" / "spotify_logo.png"
if logo_path.exists():
    try:
        favicon = Image.open(logo_path)
        st.set_page_config(
            page_title="Overview • Spotify Music Intelligence",
            page_icon=favicon,
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except:
        st.set_page_config(
            page_title="Overview • Spotify Music Intelligence",
            page_icon="",
            layout="wide",
            initial_sidebar_state="expanded"
        )
else:
    st.set_page_config(
        page_title="Overview • Spotify Music Intelligence",
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
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

load_css()

# -----------------------------
# Page-specific gradient (Dark Navy for Overview)
# -----------------------------

st.markdown("""
<style>
.stApp {
    background:
        linear-gradient(
            180deg,
            #173b8f 0%,
            #142f72 18%,
            #102654 36%,
            #0d1d3f 52%,
            #181818 74%,
            #121212 100%
        ) !important;
    background-attachment: fixed !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Hero Header (same as Home page)
# -----------------------------

logo_path = Path(__file__).parent.parent / "assets" / "spotify_logo.png"

if logo_path.exists():
    with open(logo_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()

    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 22px; padding: 20px 0 10px 0;">
        <img src="data:image/png;base64,{img_base64}" style="width: 120px; height: 120px; object-fit: contain; flex-shrink: 0;" alt="Spotify Logo">
        <div>
            <div style="font-size: 76px; font-weight: 900; color: #FFFFFF; letter-spacing: -3px; line-height: 1; margin-bottom: 4px;">Overview</div>
            <div style="font-size: 22px; color: #B3B3B3; font-weight: 400; margin-top: 4px; letter-spacing: -0.3px;">Spotify Dataset Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 22px; padding: 20px 0 10px 0;">
        <div style="background:#1DB954; width:120px; height:120px; border-radius:20px; display:flex; align-items:center; justify-content:center; font-size:56px; font-weight:900; color:#000; flex-shrink:0;">
            S
        </div>
        <div>
            <div style="font-size: 76px; font-weight: 900; color: #FFFFFF; letter-spacing: -3px; line-height: 1; margin-bottom: 4px;">Overview</div>
            <div style="font-size: 22px; color: #B3B3B3; font-weight: 400; margin-top: 4px; letter-spacing: -0.3px;">Spotify Dataset Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# -----------------------------
# Quick Stats Row (Compact Stats)
# -----------------------------

col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)

with col_stats1:
    st.markdown(f"""
    <div class="stat-item">
        <div class="stat-value">{songs.shape[0]:,}</div>
        <div class="stat-label">Total Rows</div>
    </div>
    """, unsafe_allow_html=True)

with col_stats2:
    st.markdown(f"""
    <div class="stat-item">
        <div class="stat-value">{songs.shape[1]}</div>
        <div class="stat-label">Total Columns</div>
    </div>
    """, unsafe_allow_html=True)

with col_stats3:
    missing = songs.isnull().sum().sum()
    st.markdown(f"""
    <div class="stat-item">
        <div class="stat-value">{missing:,}</div>
        <div class="stat-label">Missing Values</div>
    </div>
    """, unsafe_allow_html=True)

with col_stats4:
    memory = songs.memory_usage(deep=True).sum() / 1024 / 1024
    st.markdown(f"""
    <div class="stat-item">
        <div class="stat-value">{memory:.1f} MB</div>
        <div class="stat-label">Memory Usage</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Mini Charts Row (with Cards)
# -----------------------------

mini_left, mini_right = st.columns(2)

with mini_left:
    st.markdown('<div class="table-card" style="padding: 16px 20px 12px 20px;">', unsafe_allow_html=True)
    st.markdown('<div style="color:#FFFFFF; font-size:16px; font-weight:600; margin-bottom:8px;">Popularity Distribution</div>', unsafe_allow_html=True)
    
    pop_fig = px.histogram(
        songs,
        x="popularity",
        nbins=20,
        color_discrete_sequence=["#1DB954"],
    )
    
    pop_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B3B3B3", size=12),
        showlegend=False,
        margin=dict(l=10, r=10, t=0, b=10),
        height=280,
        xaxis=dict(
            gridcolor="#282828", 
            zeroline=False, 
            title_font=dict(color="#B3B3B3")
        ),
        yaxis=dict(
            gridcolor="#282828", 
            zeroline=False, 
            title_font=dict(color="#B3B3B3")
        ),
        title=None
    )
    
    pop_fig.update_traces(marker=dict(line=dict(width=0)))
    
    st.plotly_chart(pop_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with mini_right:
    st.markdown('<div class="table-card" style="padding: 16px 20px 12px 20px;">', unsafe_allow_html=True)
    st.markdown('<div style="color:#FFFFFF; font-size:16px; font-weight:600; margin-bottom:8px;">Top Genres</div>', unsafe_allow_html=True)
    
    # Get top genres
    top_genres = genres.sort_values("popularity", ascending=False).head(10)
    
    genre_fig = px.bar(
        top_genres,
        x="popularity",
        y="genres",
        orientation="h",
        color="popularity",
        color_continuous_scale=["#169C46", "#1DB954", "#1ED760"],
        text_auto='.0f',
    )
    
    genre_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B3B3B3", size=12),
        showlegend=False,
        margin=dict(l=10, r=10, t=0, b=10),
        height=280,
        xaxis=dict(
            gridcolor="#282828", 
            zeroline=False, 
            title_font=dict(color="#B3B3B3")
        ),
        yaxis=dict(
            gridcolor="#282828", 
            zeroline=False, 
            title_font=dict(color="#B3B3B3")
        ),
        title=None
    )
    
    genre_fig.update_traces(
        textposition='outside',
        textfont=dict(color="#B3B3B3")
    )
    
    st.plotly_chart(genre_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Dataset Preview (with Card)
# -----------------------------

st.markdown('<div class="table-card" style="padding: 16px 20px 12px 20px;">', unsafe_allow_html=True)
st.markdown('<div style="color:#FFFFFF; font-size:16px; font-weight:600; margin-bottom:8px;">Dataset Preview</div>', unsafe_allow_html=True)

# Display dataframe with progress bars for popularity
st.dataframe(
    songs.head(20),
    use_container_width=True,
    hide_index=True,
    column_config={
        "popularity": st.column_config.ProgressColumn(
            "Popularity",
            min_value=0,
            max_value=100,
            format="%d",
        ),
        "danceability": st.column_config.NumberColumn(
            "Danceability",
            format="%.2f",
        ),
        "energy": st.column_config.NumberColumn(
            "Energy",
            format="%.2f",
        ),
        "valence": st.column_config.NumberColumn(
            "Valence",
            format="%.2f",
        ),
    }
)

st.markdown('</div>', unsafe_allow_html=True)