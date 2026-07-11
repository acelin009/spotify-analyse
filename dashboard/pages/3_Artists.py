# dashboard/pages/3_Artist_Analytics.py

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
from PIL import Image
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
            page_title="Artist Analytics • Spotify Music Intelligence",
            page_icon=favicon,
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except:
        st.set_page_config(
            page_title="Artist Analytics • Spotify Music Intelligence",
            page_icon="",
            layout="wide",
            initial_sidebar_state="expanded"
        )
else:
    st.set_page_config(
        page_title="Artist Analytics • Spotify Music Intelligence",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# -----------------------------
# Load Data
# -----------------------------

songs, artists, genres, years, songs_with_genres = load_data()

# Calculate number of songs per artist
artist_song_counts = songs.groupby('artists').size().reset_index(name='song_count')
artists_with_counts = artists.merge(artist_song_counts, on='artists', how='left')

# Fill NaN values in song_count with 0 (artists with no songs)
artists_with_counts['song_count'] = artists_with_counts['song_count'].fillna(0)

# Ensure all numeric columns are properly typed
numeric_cols = ['danceability', 'popularity', 'energy', 'valence', 'song_count']
for col in numeric_cols:
    artists_with_counts[col] = pd.to_numeric(artists_with_counts[col], errors='coerce')

# Drop rows with NaN values in key columns for the quadrant chart
artists_clean = artists_with_counts.dropna(subset=['danceability', 'popularity', 'energy'])

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
            color: #C4B8A8 !important;
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
        
        /* KPI Cards - Dark sand theme */
        div.kpi-card {
            background: rgba(30, 27, 22, 0.92) !important;
            border-radius: 18px !important;
            padding: 20px 24px !important;
            border: 1px solid rgba(255, 255, 255, 0.04) !important;
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
        
        /* Chart container - Dark sand theme */
        div.chart-card {
            background: rgba(30, 27, 22, 0.92) !important;
            border-radius: 18px !important;
            padding: 24px !important;
            border: 1px solid rgba(255, 255, 255, 0.04) !important;
            margin-bottom: 16px !important;
            transition: all 0.25s ease !important;
        }
        
        div.chart-card:hover {
            border-color: rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Table card for insights */
        div.table-card {
            background: rgba(30, 27, 22, 0.92) !important;
            border-radius: 18px !important;
            padding: 24px !important;
            border: 1px solid rgba(255, 255, 255, 0.04) !important;
            margin-bottom: 16px !important;
            transition: all 0.25s ease !important;
            height: 100%;
        }
        
        div.table-card:hover {
            border-color: rgba(255, 255, 255, 0.1) !important;
            transform: translateY(-2px) !important;
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
# Page-specific gradient (Dark Sand for Artists)
# -----------------------------

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(
            circle at 50% -10%,
            rgba(180, 150, 110, 0.30),
            transparent 60%
        ),
        linear-gradient(
            180deg,
            #A89070 0%,
            #7A6B55 20%,
            #4F4235 45%,
            #2C251F 70%,
            #181818 88%,
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
            <div class="hero-title">Artist Analytics</div>
            <div class="hero-subtitle">Discover Artist Performance & Audio Characteristics</div>
            <p style="color:#C4B8A8; font-size:15px; margin-top:12px; font-weight:500;">
                <b>{len(artists):,}</b> Artists
                &nbsp;&nbsp;•&nbsp;&nbsp;
                <b>{len(songs):,}</b> Songs
                &nbsp;&nbsp;•&nbsp;&nbsp;
                <b>{artists['popularity'].mean():.1f}</b> Avg Popularity
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
            <div class="hero-title">Artist Analytics</div>
            <div class="hero-subtitle">Discover Artist Performance & Audio Characteristics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# -----------------------------
# KPI Cards
# -----------------------------

top_artist = artists.sort_values("popularity", ascending=False).iloc[0]

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Most Popular Artist</div>
        <div class="kpi-value">{top_artist["artists"]}</div>
        <div class="kpi-delta">★ {top_artist["popularity"]:.1f} avg popularity</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Artists</div>
        <div class="kpi-value">{len(artists):,}</div>
        <div class="kpi-delta">▲ Complete catalog</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi3:
    avg_artist_pop = artists['popularity'].mean()
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Avg Artist Popularity</div>
        <div class="kpi-value">{avg_artist_pop:.1f}</div>
        <div class="kpi-delta">▲ Industry benchmark</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi4:
    total_songs = len(songs)
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Songs</div>
        <div class="kpi-value">{total_songs:,}</div>
        <div class="kpi-delta">▲ Complete dataset</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# -----------------------------
# Top 15 Artists
# -----------------------------

st.markdown('<div class="section-title">Top 15 Artists</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

top15 = artists.sort_values("popularity", ascending=False).head(15)

fig_top = px.bar(
    top15,
    x="popularity",
    y="artists",
    orientation="h",
    color="popularity",
    color_continuous_scale=["#169C46", "#1DB954", "#1ED760"],
    title="Top 15 Artists by Average Popularity",
    labels={
        "popularity": "Average Popularity",
        "artists": "Artist"
    }
)

fig_top.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
    showlegend=False,
    margin=dict(l=10, r=10, t=40, b=10),
    height=500,
    xaxis=dict(gridcolor="#282828", range=[0, 100], zeroline=False),
    yaxis=dict(gridcolor="#282828", zeroline=False),
    title_font=dict(color="#FFFFFF", size=16)
)

fig_top.update_traces(
    textposition='outside',
    textfont=dict(color="#B3B3B3")
)

st.plotly_chart(fig_top, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# -----------------------------
# Artist Comparison
# -----------------------------

st.markdown('<div class="section-title">Compare Artists</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

# Two columns for artist search
left, right = st.columns(2)

with left:
    artist1_search = st.text_input(
        "Artist A",
        placeholder="Search Taylor Swift...",
        help="Type the name of the first artist to compare",
        label_visibility="collapsed"
    )
    st.caption("Search for Artist A")

with right:
    artist2_search = st.text_input(
        "Artist B",
        placeholder="Search Ed Sheeran...",
        help="Type the name of the second artist to compare",
        label_visibility="collapsed"
    )
    st.caption("Search for Artist B")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# Search for artists in the dataset
if artist1_search and artist2_search:
    artist_a_matches = artists[
        artists["artists"].str.contains(artist1_search, case=False, na=False)
    ]
    artist_b_matches = artists[
        artists["artists"].str.contains(artist2_search, case=False, na=False)
    ]
    
    if len(artist_a_matches) == 0:
        st.warning(f"No artist found matching '{artist1_search}'. Please try a different name.")
    elif len(artist_b_matches) == 0:
        st.warning(f"No artist found matching '{artist2_search}'. Please try a different name.")
    else:
        a = artist_a_matches.iloc[0]
        b = artist_b_matches.iloc[0]
        
        if a["artists"] == b["artists"]:
            st.warning("Please search for two different artists.")
        else:
            st.success(f"Found: **{a['artists']}** and **{b['artists']}**")
            
            if len(artist_a_matches) > 1:
                with st.expander(f"Multiple matches found for '{artist1_search}'"):
                    for idx, row in artist_a_matches.iterrows():
                        st.write(f"• {row['artists']} (Popularity: {row['popularity']:.1f})")
            
            if len(artist_b_matches) > 1:
                with st.expander(f"Multiple matches found for '{artist2_search}'"):
                    for idx, row in artist_b_matches.iterrows():
                        st.write(f"• {row['artists']} (Popularity: {row['popularity']:.1f})")
            
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

            # Compare KPIs
            col1, col2 = st.columns(2)

            # Artist A
            with col1:
                st.markdown(f"""
                <div style="color:#FFFFFF; font-size:24px; font-weight:700; margin-bottom:16px;">{a['artists']}</div>
                """, unsafe_allow_html=True)
                
                metrics_col1, metrics_col2 = st.columns(2)
                
                with metrics_col1:
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Popularity</div>
                        <div class="kpi-value">{a['popularity']:.1f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Danceability</div>
                        <div class="kpi-value">{a['danceability']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Energy</div>
                        <div class="kpi-value">{a['energy']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metrics_col2:
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Valence</div>
                        <div class="kpi-value">{a['valence']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Acousticness</div>
                        <div class="kpi-value">{a['acousticness']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Speechiness</div>
                        <div class="kpi-value">{a['speechiness']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Artist B
            with col2:
                st.markdown(f"""
                <div style="color:#FFFFFF; font-size:24px; font-weight:700; margin-bottom:16px;">{b['artists']}</div>
                """, unsafe_allow_html=True)
                
                metrics_col3, metrics_col4 = st.columns(2)
                
                with metrics_col3:
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Popularity</div>
                        <div class="kpi-value">{b['popularity']:.1f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Danceability</div>
                        <div class="kpi-value">{b['danceability']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Energy</div>
                        <div class="kpi-value">{b['energy']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metrics_col4:
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Valence</div>
                        <div class="kpi-value">{b['valence']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Acousticness</div>
                        <div class="kpi-value">{b['acousticness']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Speechiness</div>
                        <div class="kpi-value">{b['speechiness']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

            # Radar Chart
            st.markdown('<div class="section-title">Audio Feature Comparison</div>', unsafe_allow_html=True)

            st.markdown('<div class="chart-card">', unsafe_allow_html=True)

            features = ["danceability", "energy", "acousticness", "speechiness", "valence", "liveness"]

            fig_radar = go.Figure()

            fig_radar.add_trace(go.Scatterpolar(
                r=[a[f] for f in features],
                theta=[f.capitalize() for f in features],
                fill="toself",
                name=a['artists'],
                line=dict(color="#1DB954"),
                fillcolor="rgba(29, 185, 84, 0.3)"
            ))

            fig_radar.add_trace(go.Scatterpolar(
                r=[b[f] for f in features],
                theta=[f.capitalize() for f in features],
                fill="toself",
                name=b['artists'],
                line=dict(color="#888888"),
                fillcolor="rgba(136, 136, 136, 0.25)"
            ))

            fig_radar.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(color="#B3B3B3")),
                    angularaxis=dict(tickfont=dict(color="#B3B3B3"))
                ),
                title=dict(text="Artist Audio Feature Comparison", font=dict(color="#FFFFFF", size=16)),
                legend=dict(font=dict(color="#B3B3B3"), bgcolor="rgba(0,0,0,0.5)"),
                height=650,
                margin=dict(l=10, r=10, t=40, b=10)
            )

            st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

            # Comparison Summary
            st.markdown('<div class="section-title">Comparison Summary</div>', unsafe_allow_html=True)

            col_summary1, col_summary2 = st.columns(2)

            with col_summary1:
                st.markdown(f"""
                <div class="table-card">
                    <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-bottom:12px;">{a['artists']} has higher:</div>
                """, unsafe_allow_html=True)
                advantages_a = []
                features_compare = ["popularity", "danceability", "energy", "valence", "acousticness", "speechiness"]
                for feature in features_compare:
                    if a[feature] > b[feature]:
                        diff = abs(a[feature] - b[feature])
                        if feature == "popularity":
                            advantages_a.append(f"✅ {feature.capitalize()} ({diff:.1f} higher)")
                        else:
                            advantages_a.append(f"✅ {feature.capitalize()} ({diff:.3f} higher)")
                if advantages_a:
                    for adv in advantages_a:
                        st.markdown(adv)
                else:
                    st.markdown("No significant advantages")
                st.markdown('</div>', unsafe_allow_html=True)

            with col_summary2:
                st.markdown(f"""
                <div class="table-card">
                    <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-bottom:12px;">{b['artists']} has higher:</div>
                """, unsafe_allow_html=True)
                advantages_b = []
                for feature in features_compare:
                    if b[feature] > a[feature]:
                        diff = abs(b[feature] - a[feature])
                        if feature == "popularity":
                            advantages_b.append(f"✅ {feature.capitalize()} ({diff:.1f} higher)")
                        else:
                            advantages_b.append(f"✅ {feature.capitalize()} ({diff:.3f} higher)")
                if advantages_b:
                    for adv in advantages_b:
                        st.markdown(adv)
                else:
                    st.markdown("No significant advantages")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

            st.info(f"""
            **Key Insight**: The radar chart reveals that {a['artists']} and {b['artists']} have 
            distinct musical profiles. The overall "shape" of their audio features 
            helps understand their unique sound characteristics.
            """)

elif artist1_search and not artist2_search:
    st.info("Please search for a second artist to compare.")
elif not artist1_search and artist2_search:
    st.info("Please search for a first artist to compare.")
else:
    st.info("Enter two artist names above to compare their audio features and popularity metrics.")

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# -----------------------------
# Artist Quadrant Analysis (Danceability vs Popularity)
# -----------------------------

st.markdown('<div class="section-title">Artist Quadrant Analysis</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

# Get median values for quadrant lines
median_danceability = artists_clean['danceability'].median()
median_popularity = artists_clean['popularity'].median()

# Check if we have data to plot
if len(artists_clean) > 0:
    # Create quadrant scatter plot with green shades and white
    fig_quadrant = px.scatter(
        artists_clean,
        x="danceability",
        y="popularity",
        size="song_count",
        color="energy",
        hover_name="artists",
        hover_data={
            "danceability": True,
            "popularity": True,
            "energy": True,
            "song_count": True,
            "valence": True
        },
        size_max=50,
        color_continuous_scale=["#FFFFFF", "#90EE90", "#32CD32", "#228B22", "#006400"],
        labels={
            "danceability": "Danceability Score",
            "popularity": "Average Popularity",
            "energy": "Energy",
            "song_count": "Number of Songs"
        },
        title="Artist Quadrant: Danceability vs Popularity"
    )

    # Add quadrant lines with white color for better visibility
    fig_quadrant.add_hline(
        y=median_popularity,
        line_dash="dash",
        line_color="#FFFFFF",
        opacity=0.7,
        annotation_text=f"Median Popularity: {median_popularity:.1f}",
        annotation_font=dict(color="#FFFFFF", size=12)
    )

    fig_quadrant.add_vline(
        x=median_danceability,
        line_dash="dash",
        line_color="#FFFFFF",
        opacity=0.7,
        annotation_text=f"Median Danceability: {median_danceability:.2f}",
        annotation_font=dict(color="#FFFFFF", size=12)
    )

    # Add quadrant labels with bright green - fixed font parameters
    fig_quadrant.add_annotation(
        x=0.85,
        y=88,
        text="⭐ Hit Makers",
        font=dict(color="#1DB954", size=18),
        showarrow=False,
        opacity=0.95,
        bgcolor="rgba(0,0,0,0.6)",
        bordercolor="#1DB954",
        borderwidth=2,
        borderpad=4
    )

    fig_quadrant.add_annotation(
        x=0.85,
        y=12,
        text="🕺 Dance Icons",
        font=dict(color="#1DB954", size=18),
        showarrow=False,
        opacity=0.95,
        bgcolor="rgba(0,0,0,0.6)",
        bordercolor="#1DB954",
        borderwidth=2,
        borderpad=4
    )

    fig_quadrant.add_annotation(
        x=0.15,
        y=88,
        text="🎨 Niche Artists",
        font=dict(color="#1DB954", size=18),
        showarrow=False,
        opacity=0.95,
        bgcolor="rgba(0,0,0,0.6)",
        bordercolor="#1DB954",
        borderwidth=2,
        borderpad=4
    )

    fig_quadrant.add_annotation(
        x=0.15,
        y=12,
        text="🔬 Experimental",
        font=dict(color="#1DB954", size=18),
        showarrow=False,
        opacity=0.95,
        bgcolor="rgba(0,0,0,0.6)",
        bordercolor="#1DB954",
        borderwidth=2,
        borderpad=4
    )

    fig_quadrant.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF", family="Inter, sans-serif", size=13),
        margin=dict(l=10, r=10, t=40, b=10),
        height=550,
        xaxis=dict(
            gridcolor="#555555", 
            zeroline=False,
            range=[0, 1.05],
            title_font=dict(color="#FFFFFF", size=15),
            tickfont=dict(color="#FFFFFF", size=12)
        ),
        yaxis=dict(
            gridcolor="#555555", 
            zeroline=False,
            range=[0, 105],
            title_font=dict(color="#FFFFFF", size=15),
            tickfont=dict(color="#FFFFFF", size=12)
        ),
        title_font=dict(color="#FFFFFF", size=20),
        legend=dict(
            font=dict(color="#FFFFFF", size=12),
            bgcolor="rgba(0,0,0,0.8)",
            bordercolor="#1DB954",
            borderwidth=2,
            borderpad=6
        ),
        coloraxis_colorbar=dict(
            title=dict(text="Energy", font=dict(color="#FFFFFF", size=13)),
            tickfont=dict(color="#FFFFFF", size=11)
        )
    )

    st.plotly_chart(fig_quadrant, use_container_width=True, config={"displayModeBar": False})
else:
    st.warning("No data available for the quadrant chart. Please check your data source.")

st.markdown('</div>', unsafe_allow_html=True)

# Add quadrant explanation with green theme
st.markdown("""
<div style="background: rgba(30, 27, 22, 0.92); border-radius: 12px; padding: 16px 20px; margin-top: 8px; border: 1px solid rgba(255, 255, 255, 0.08);">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; color: #E0E0E0; font-size: 14px;">
        <div>
            <span style="color: #1DB954; font-weight: 700; font-size: 15px;">⭐ Hit Makers</span> — High popularity, high danceability<br>
            <span style="color: #1DB954; font-weight: 700; font-size: 15px;">🎨 Niche Artists</span> — High popularity, low danceability
        </div>
        <div>
            <span style="color: #1DB954; font-weight: 700; font-size: 15px;">🕺 Dance Icons</span> — Low popularity, high danceability<br>
            <span style="color: #1DB954; font-weight: 700; font-size: 15px;">🔬 Experimental</span> — Low popularity, low danceability
        </div>
    </div>
    <div style="color: #AAAAAA; font-size: 12px; margin-top: 10px; text-align: center; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px;">
        💡 <strong>Bubble size</strong> = Number of Songs &nbsp;•&nbsp; <strong>Color</strong> = Energy Level (White → Dark Green)
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# -----------------------------
# Business Insights
# -----------------------------

st.markdown('<div class="section-title">Key Insights</div>', unsafe_allow_html=True)

col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    st.markdown("""
    <div class="table-card">
        <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-bottom:12px;">Artist Performance</div>
        <div style="color:#B3B3B3; font-size:14px; line-height:1.8;">
        • Most artists have moderate popularity, with only a few reaching the highest levels<br>
        • The distribution shows a long tail, typical of music industry data<br>
        • Top artists consistently show higher engagement across multiple audio features
        </div>
        <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-top:16px; margin-bottom:12px;">Audio Characteristics</div>
        <div style="color:#B3B3B3; font-size:14px; line-height:1.8;">
        • Radar charts reveal distinct musical styles across artists<br>
        • High popularity does not always correspond to high energy or danceability<br>
        • Acousticness and speechiness vary significantly across artists
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_insight2:
    st.markdown("""
    <div class="table-card">
        <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-bottom:12px;">Strategic Recommendations</div>
        <div style="color:#B3B3B3; font-size:14px; line-height:1.8;">
        • A&R teams can use audio feature profiles to identify emerging artists<br>
        • Marketing can tailor campaigns based on an artist's unique audio footprint<br>
        • Playlist curators can identify artists that complement specific moods
        </div>
        <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-top:16px; margin-bottom:12px;">Future Applications</div>
        <div style="color:#B3B3B3; font-size:14px; line-height:1.8;">
        • Audio features can help identify unique artist profiles<br>
        • Similarity metrics can find artists with comparable sound signatures<br>
        • Trend analysis over time can reveal shifts in musical preferences
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
st.caption(f"Updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}  •  {len(artists):,} Artists  •  {len(songs):,} Songs")