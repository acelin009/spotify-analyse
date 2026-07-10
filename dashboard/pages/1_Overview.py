# dashboard/pages/1_Overview.py (COMPLETE REFACTOR)

import streamlit as st
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from PIL import Image
from data_loader import load_data
import base64

# -----------------------------
# Page Configuration
# -----------------------------

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
            page_icon="🎵",
            layout="wide",
            initial_sidebar_state="expanded"
        )
else:
    st.set_page_config(
        page_title="Overview • Spotify Music Intelligence",
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
# Page-specific gradient
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
            <div class="hero-title">📊 Dataset Overview</div>
            <div class="hero-subtitle">Complete data literacy — understand every aspect of the Spotify dataset before diving deeper</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="hero-header">
        <div style="background:#1DB954;width:120px;height:120px;border-radius:20px;display:flex;align-items:center;justify-content:center;font-size:56px;font-weight:900;color:#000;flex-shrink:0;">S</div>
        <div>
            <div class="hero-title">📊 Dataset Overview</div>
            <div class="hero-subtitle">Complete data literacy — understand every aspect of the Spotify dataset before diving deeper</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# -----------------------------
# 1. How to use this dashboard
# -----------------------------

min_year = songs['year'].min()
max_year = songs['year'].max()

st.info(f"""
**🎯 How to use this dashboard**  
This dashboard explores **{songs.shape[0]:,}** Spotify tracks across **{min_year}–{max_year}** ({max_year - min_year} years of music).  
Use the sidebar to dive into **Artists**, **Genres**, **Trends**, or try the **ML Predictor** to forecast song popularity.
""")

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# -----------------------------
# 2. Dataset Scale & Health Stats
# -----------------------------

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Tracks</div>
        <div class="kpi-value">{songs.shape[0]:,}</div>
        <div class="kpi-delta">Rows in dataset</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi2:
    avg_duration = songs['duration_ms'].mean() / 60000
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Avg Duration</div>
        <div class="kpi-value">{avg_duration:.1f} min</div>
        <div class="kpi-delta">Average song length</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Years Covered</div>
        <div class="kpi-value">{min_year}–{max_year}</div>
        <div class="kpi-delta">{max_year - min_year} years of music</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi4:
    missing = songs.isnull().sum().sum()
    total_cells = songs.shape[0] * songs.shape[1]
    completeness = ((total_cells - missing) / total_cells * 100)
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Data Completeness</div>
        <div class="kpi-value">{completeness:.1f}%</div>
        <div class="kpi-delta">{missing:,} missing values</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Per-column missing values (mini visualization)
missing_df = pd.DataFrame({
    'Column': songs.columns,
    'Missing %': (songs.isnull().sum() / len(songs) * 100).values,
    'Missing Count': songs.isnull().sum().values
})
missing_df = missing_df[missing_df['Missing %'] > 0].sort_values('Missing %', ascending=False)

if len(missing_df) > 0:
    st.markdown("""
    <div style="color: #B3B3B3; font-size: 0.9rem; margin-bottom: 6px;">
        <strong style="color: #FFFFFF;">Columns with missing data:</strong>
    </div>
    """, unsafe_allow_html=True)
    
    missing_cols = st.columns(min(len(missing_df), 4))
    for idx, (_, row) in enumerate(missing_df.iterrows()):
        col_idx = idx % 4
        with missing_cols[col_idx]:
            st.markdown(f"""
            <div style="background: #282828; border-radius: 6px; padding: 6px 12px; margin-bottom: 4px; display: flex; justify-content: space-between;">
                <span style="color: #B3B3B3; font-size: 0.8rem;">{row['Column']}</span>
                <span style="color: #1DB954; font-size: 0.8rem;">{row['Missing %']:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# -----------------------------
# 3. Data Dictionary (Expandable)
# -----------------------------

with st.expander("📖 What do these columns mean? — Data Dictionary", expanded=False):
    st.markdown("""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 8px 0;">
        <div style="background: #282828; border-radius: 8px; padding: 14px 16px; border-left: 3px solid #1DB954;">
            <div style="color: #1DB954; font-weight: 600; font-size: 0.95rem;">🎵 popularity</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">Score from 0–100 indicating how popular a track is. Calculated by Spotify based on play count, recency, and other factors.</div>
        </div>
        <div style="background: #282828; border-radius: 8px; padding: 14px 16px; border-left: 3px solid #1DB954;">
            <div style="color: #1DB954; font-weight: 600; font-size: 0.95rem;">💃 danceability</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">How suitable a track is for dancing (0–1). Based on tempo, rhythm stability, beat strength, and overall regularity.</div>
        </div>
        <div style="background: #282828; border-radius: 8px; padding: 14px 16px; border-left: 3px solid #1DB954;">
            <div style="color: #1DB954; font-weight: 600; font-size: 0.95rem;">⚡ energy</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">Perceived intensity and activity (0–1). Energetic tracks feel fast, loud, and noisy — think rock, EDM, hip-hop.</div>
        </div>
        <div style="background: #282828; border-radius: 8px; padding: 14px 16px; border-left: 3px solid #1DB954;">
            <div style="color: #1DB954; font-weight: 600; font-size: 0.95rem;">😊 valence</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">Musical positivity (0–1). High valence = happy, cheerful, euphoric. Low valence = sad, depressed, angry.</div>
        </div>
        <div style="background: #282828; border-radius: 8px; padding: 14px 16px; border-left: 3px solid #1DB954;">
            <div style="color: #1DB954; font-weight: 600; font-size: 0.95rem;">🎸 acousticness</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">Confidence measure (0–1) of whether the track is acoustic. 1.0 = high confidence the track is acoustic.</div>
        </div>
        <div style="background: #282828; border-radius: 8px; padding: 14px 16px; border-left: 3px solid #1DB954;">
            <div style="color: #1DB954; font-weight: 600; font-size: 0.95rem;">🎤 speechiness</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">Presence of spoken words (0–1). Above 0.66 = pure speech (podcast, audiobook); 0.33–0.66 = music + speech.</div>
        </div>
        <div style="background: #282828; border-radius: 8px; padding: 14px 16px; border-left: 3px solid #1DB954;">
            <div style="color: #1DB954; font-weight: 600; font-size: 0.95rem;">🎵 tempo</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">Beats per minute (BPM) — the average tempo of the track. Ranges from ~60 (slow) to ~200 (very fast).</div>
        </div>
        <div style="background: #282828; border-radius: 8px; padding: 14px 16px; border-left: 3px solid #1DB954;">
            <div style="color: #1DB954; font-weight: 600; font-size: 0.95rem;">🎹 instrumentalness</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">Predicts whether a track contains no vocals (0–1). Closer to 1.0 = higher likelihood of being instrumental-only.</div>
        </div>
        <div style="background: #282828; border-radius: 8px; padding: 14px 16px; border-left: 3px solid #1DB954;">
            <div style="color: #1DB954; font-weight: 600; font-size: 0.95rem;">🎤 liveness</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">Detects presence of an audience (0–1). Higher values (>0.8) suggest the track was recorded live.</div>
        </div>
        <div style="background: #282828; border-radius: 8px; padding: 14px 16px; border-left: 3px solid #1DB954;">
            <div style="color: #1DB954; font-weight: 600; font-size: 0.95rem;">🔊 loudness</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">Overall loudness in decibels (dB). Ranges from -60 to 0 dB — higher values = louder tracks.</div>
        </div>
        <div style="background: #282828; border-radius: 8px; padding: 14px 16px; border-left: 3px solid #1DB954;">
            <div style="color: #1DB954; font-weight: 600; font-size: 0.95rem;">🎵 key</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">The key the track is in (0–11 mapped to pitches C, C#, D, etc.). Standard Western music theory.</div>
        </div>
        <div style="background: #282828; border-radius: 8px; padding: 14px 16px; border-left: 3px solid #1DB954;">
            <div style="color: #1DB954; font-weight: 600; font-size: 0.95rem;">🔀 mode</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">Modality: 0 = minor, 1 = major. Major keys generally sound happier; minor keys sound darker/sadder.</div>
        </div>
        <div style="background: #282828; border-radius: 8px; padding: 14px 16px; border-left: 3px solid #1DB954;">
            <div style="color: #1DB954; font-weight: 600; font-size: 0.95rem;">⚠️ explicit</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">Binary flag: 1 = contains explicit lyrics, 0 = clean. Important for content filtering.</div>
        </div>
        <div style="background: #282828; border-radius: 8px; padding: 14px 16px; border-left: 3px solid #1DB954;">
            <div style="color: #1DB954; font-weight: 600; font-size: 0.95rem;">⏱️ duration_ms</div>
            <div style="color: #B3B3B3; font-size: 0.85rem;">Track length in milliseconds. Can be converted to minutes for easier interpretation.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# -----------------------------
# 4. Column-level breakdown table
# -----------------------------

st.markdown("""
<div style="color: #FFFFFF; font-weight: 600; margin-bottom: 8px; font-size: 1.05rem;">
    📋 Column-level Breakdown
</div>
""", unsafe_allow_html=True)

# Build column info table
column_info = []
for col in songs.columns:
    dtype = songs[col].dtype
    unique_vals = songs[col].nunique()
    missing_pct = (songs[col].isnull().sum() / len(songs) * 100)
    
    if pd.api.types.is_numeric_dtype(songs[col]):
        min_val = songs[col].min()
        max_val = songs[col].max()
        range_str = f"{min_val:.2f} – {max_val:.2f}" if min_val != max_val else str(min_val)
    else:
        range_str = "—"
    
    column_info.append({
        'Column': col,
        'Type': str(dtype),
        'Unique': unique_vals,
        'Range': range_str,
        'Missing %': f"{missing_pct:.1f}%"
    })

col_df = pd.DataFrame(column_info)

# Display as a styled table
st.dataframe(
    col_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        'Column': st.column_config.TextColumn('Column', width='medium'),
        'Type': st.column_config.TextColumn('Data Type', width='small'),
        'Unique': st.column_config.NumberColumn('Unique Values', format='%d'),
        'Range': st.column_config.TextColumn('Min – Max', width='medium'),
        'Missing %': st.column_config.TextColumn('Missing %', width='small'),
    }
)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# -----------------------------
# 5. Small-multiples distribution grid
# -----------------------------

st.markdown("""
<div style="color: #FFFFFF; font-weight: 600; margin-bottom: 8px; font-size: 1.05rem;">
    📊 Feature Distributions
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

# Select features for small multiples
features = ['popularity', 'danceability', 'energy', 'valence', 'acousticness', 'tempo']
feature_labels = ['Popularity', 'Danceability', 'Energy', 'Valence', 'Acousticness', 'Tempo (BPM)']

# Create subplots
fig = make_subplots(
    rows=2, cols=3,
    subplot_titles=feature_labels,
    shared_yaxes=False,
    vertical_spacing=0.12,
    horizontal_spacing=0.08
)

colors = ['#1DB954', '#1ED760', '#169C46', '#0D7C3A', '#1DB95480', '#1DB95460']

for idx, (feature, label, color) in enumerate(zip(features, feature_labels, colors)):
    row = idx // 3 + 1
    col = idx % 3 + 1
    
    # Filter out outliers for tempo (keep between 60-200 BPM for better visualization)
    data = songs[feature].dropna()
    if feature == 'tempo':
        data = data[(data >= 60) & (data <= 200)]
    
    fig.add_trace(
        go.Histogram(
            x=data,
            nbinsx=25,
            marker_color=color,
            marker=dict(line=dict(width=0)),
            showlegend=False,
            hovertemplate='%{x:.1f}<br>Count: %{y}<extra></extra>'
        ),
        row=row, col=col
    )
    
    # Update each subplot
    fig.update_xaxes(
        gridcolor="#282828",
        zeroline=False,
        title_font=dict(color="#B3B3B3", size=10),
        tickfont=dict(color="#B3B3B3", size=9),
        row=row, col=col
    )
    fig.update_yaxes(
        gridcolor="#282828",
        zeroline=False,
        title_font=dict(color="#B3B3B3", size=10),
        tickfont=dict(color="#B3B3B3", size=9),
        row=row, col=col
    )

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#B3B3B3", family="Inter, sans-serif", size=11),
    height=500,
    margin=dict(l=20, r=20, t=50, b=20),
    showlegend=False,
    bargap=0.08
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# -----------------------------
# 6. Correlation Heatmap
# -----------------------------

st.markdown("""
<div style="color: #FFFFFF; font-weight: 600; margin-bottom: 8px; font-size: 1.05rem;">
    🔗 Feature Correlations
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

# Select audio features for correlation (including popularity)
audio_features = ['popularity', 'danceability', 'energy', 'valence', 'speechiness', 
                  'acousticness', 'liveness', 'instrumentalness', 'tempo']

# Calculate correlation matrix
corr_matrix = songs[audio_features].corr()

# Create heatmap with annotations
heatmap_fig = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.columns,
    colorscale=[
        [0, '#0D7C3A'],
        [0.3, '#169C46'],
        [0.5, '#1DB954'],
        [0.7, '#1ED760'],
        [1, '#1ED760']
    ],
    zmid=0,
    text=corr_matrix.values.round(2),
    texttemplate='%{text}',
    textfont=dict(color='#FFFFFF', size=10),
    hovertemplate='%{x} vs %{y}<br>Correlation: %{z:.2f}<extra></extra>'
))

heatmap_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#B3B3B3", size=11),
    margin=dict(l=10, r=10, t=10, b=10),
    height=500,
    xaxis=dict(
        tickangle=45,
        tickfont=dict(color="#B3B3B3", size=10),
        side='top'
    ),
    yaxis=dict(
        tickfont=dict(color="#B3B3B3", size=10)
    )
)

st.plotly_chart(heatmap_fig, use_container_width=True, config={"displayModeBar": False})

# Observations from correlation heatmap
st.markdown("""
<div style="background: #282828; border-radius: 8px; padding: 12px 16px; margin-top: 8px;">
    <div style="color: #B3B3B3; font-size: 0.85rem;">
        <strong style="color: #1DB954;">Key observations:</strong><br>
        • <strong style="color: #FFFFFF;">Energy</strong> and <strong style="color: #FFFFFF;">Danceability</strong> show positive correlation — energetic songs tend to be more danceable.<br>
        • <strong style="color: #FFFFFF;">Acousticness</strong> inversely correlates with both Energy and Danceability — acoustic songs are generally less energetic.<br>
        • <strong style="color: #FFFFFF;">Popularity</strong> has weak correlation with most audio features — popularity depends more on other factors.<br>
        • <strong style="color: #FFFFFF;">Valence</strong> and <strong style="color: #FFFFFF;">Energy</strong> are moderately correlated — happier songs tend to be more energetic.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# -----------------------------
# 7. Raw data preview with table selector
# -----------------------------

st.markdown("""
<div style="color: #FFFFFF; font-weight: 600; margin-bottom: 8px; font-size: 1.05rem;">
    📄 Raw Data Preview
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="table-card">', unsafe_allow_html=True)

# Table selector
table_options = {
    'songs': songs,
    'artists': artists,
    'genres': genres,
    'years': years
}

selected_table = st.selectbox(
    "Choose a table to preview:",
    options=list(table_options.keys()),
    format_func=lambda x: x.capitalize(),
    label_visibility="collapsed"
)

preview_df = table_options[selected_table]

st.markdown(f"""
<div style="color: #B3B3B3; font-size: 0.85rem; margin-bottom: 8px;">
    Showing first 20 rows of <strong style="color: #FFFFFF;">{selected_table}</strong> table ({preview_df.shape[0]:,} rows × {preview_df.shape[1]} columns)
</div>
""", unsafe_allow_html=True)

# Dynamic column config
column_config = {}
if 'popularity' in preview_df.columns:
    column_config['popularity'] = st.column_config.ProgressColumn(
        "Popularity",
        min_value=0,
        max_value=100,
        format="%d",
    )
if 'danceability' in preview_df.columns:
    column_config['danceability'] = st.column_config.NumberColumn("Danceability", format="%.2f")
if 'energy' in preview_df.columns:
    column_config['energy'] = st.column_config.NumberColumn("Energy", format="%.2f")
if 'valence' in preview_df.columns:
    column_config['valence'] = st.column_config.NumberColumn("Valence", format="%.2f")
if 'count' in preview_df.columns:
    column_config['count'] = st.column_config.NumberColumn("Count", format="%d")

st.dataframe(
    preview_df.head(20),
    use_container_width=True,
    hide_index=True,
    column_config=column_config
)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Download buttons
# -----------------------------

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

download_col1, download_col2, download_col3 = st.columns([1, 1, 2])
with download_col1:
    st.download_button(
        label="Download Songs CSV",
        data=songs.to_csv(index=False).encode('utf-8'),
        file_name='spotify_songs.csv',
        mime='text/csv',
        use_container_width=True
    )

with download_col2:
    st.download_button(
        label="Download Artists CSV",
        data=artists.to_csv(index=False).encode('utf-8'),
        file_name='spotify_artists.csv',
        mime='text/csv',
        use_container_width=True
    )