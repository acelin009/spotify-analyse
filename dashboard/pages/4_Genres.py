# dashboard/pages/4_Genre_Analytics.py

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
            page_title="Genre Analytics • Spotify Music Intelligence",
            page_icon=favicon,
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except:
        st.set_page_config(
            page_title="Genre Analytics • Spotify Music Intelligence",
            page_icon="🎸",
            layout="wide",
            initial_sidebar_state="expanded"
        )
else:
    st.set_page_config(
        page_title="Genre Analytics • Spotify Music Intelligence",
        page_icon="🎸",
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
            color: #E8D5C0 !important;
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
        
        /* KPI Cards - Dark for orange theme */
        div.kpi-card {
            background: rgba(30, 25, 20, 0.92) !important;
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
        
        /* Chart container - Dark for orange theme */
        div.chart-card {
            background: rgba(30, 25, 20, 0.92) !important;
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
            background: rgba(30, 25, 20, 0.92) !important;
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
# Page-specific gradient (Dark Orange/Burnt Orange for Genres)
# -----------------------------

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(
            circle at 50% -15%,
            rgba(205, 118, 42, 0.38),
            transparent 55%
        ),
        linear-gradient(
            180deg,
            #8C4F19 0%,
            #6C3E16 18%,
            #4E2D12 40%,
            #2F2117 62%,
            #1B1B1B 82%,
            #121212 100%
        ) !important;
    background-attachment: fixed !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Constants
# -----------------------------
FEATURES = [
    "danceability",
    "energy",
    "acousticness",
    "speechiness",
    "instrumentalness",
    "valence",
]

FEATURES_COMPARE = [
    "popularity", 
    "danceability", 
    "energy", 
    "valence", 
    "acousticness",
    "speechiness"
]

# -----------------------------
# Helper Functions
# -----------------------------
def create_radar_chart(data_a, data_b, features, label_a, label_b, title):
    """
    Create a radar chart comparing two entities.
    """
    fig = go.Figure()
    
    # Entity A
    fig.add_trace(
        go.Scatterpolar(
            r=[data_a[f] for f in features],
            theta=[f.capitalize() for f in features],
            fill="toself",
            name=label_a,
            line=dict(color="#1DB954"),
            fillcolor="rgba(29, 185, 84, 0.3)"
        )
    )
    
    # Entity B
    fig.add_trace(
        go.Scatterpolar(
            r=[data_b[f] for f in features],
            theta=[f.capitalize() for f in features],
            fill="toself",
            name=label_b,
            line=dict(color="#43D17D"),
            fillcolor="rgba(67, 209, 125, 0.25)"
        )
    )
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(color="#B3B3B3")),
            angularaxis=dict(tickfont=dict(color="#B3B3B3"))
        ),
        title=dict(text=title, font=dict(color="#FFFFFF", size=16)),
        legend=dict(font=dict(color="#B3B3B3"), bgcolor="rgba(0,0,0,0.5)"),
        height=650,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    
    return fig

def generate_comparison_summary(entity_a, entity_b, label_a, label_b, features):
    """
    Generate comparison summary between two entities.
    """
    col_summary1, col_summary2 = st.columns(2)
    
    # Entity A advantages
    with col_summary1:
        st.markdown(f"""
        <div class="table-card">
            <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-bottom:12px;">{label_a} has higher:</div>
        """, unsafe_allow_html=True)
        advantages_a = []
        
        for feature in features:
            if entity_a[feature] > entity_b[feature]:
                diff = abs(entity_a[feature] - entity_b[feature])
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
    
    # Entity B advantages
    with col_summary2:
        st.markdown(f"""
        <div class="table-card">
            <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-bottom:12px;">{label_b} has higher:</div>
        """, unsafe_allow_html=True)
        advantages_b = []
        
        for feature in features:
            if entity_b[feature] > entity_a[feature]:
                diff = abs(entity_b[feature] - entity_a[feature])
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
            <div class="hero-title">Genre Analytics</div>
            <div class="hero-subtitle">Discover Genre Trends & Audio Characteristics</div>
            <p style="color:#E8D5C0; font-size:15px; margin-top:12px; font-weight:500;">
                <b>{len(genres):,}</b> Genres
                &nbsp;&nbsp;•&nbsp;&nbsp;
                <b>{len(songs):,}</b> Songs
                &nbsp;&nbsp;•&nbsp;&nbsp;
                <b>{genres['popularity'].mean():.1f}</b> Avg Popularity
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
            <div class="hero-title">Genre Analytics</div>
            <div class="hero-subtitle">Discover Genre Trends & Audio Characteristics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# -----------------------------
# KPI Cards
# -----------------------------

top_genre = genres.sort_values("popularity", ascending=False).iloc[0]

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Most Popular Genre</div>
        <div class="kpi-value">{top_genre["genres"]}</div>
        <div class="kpi-delta">★ {top_genre["popularity"]:.1f} avg popularity</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Genres</div>
        <div class="kpi-value">{len(genres):,}</div>
        <div class="kpi-delta">▲ Complete catalog</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi3:
    avg_genre_pop = genres['popularity'].mean()
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Avg Genre Popularity</div>
        <div class="kpi-value">{avg_genre_pop:.1f}</div>
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
# Top 20 Genres
# -----------------------------

st.markdown('<div class="section-title">Top Genres</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

top20 = genres.sort_values("popularity", ascending=False).head(20)

fig_top = px.bar(
    top20,
    x="popularity",
    y="genres",
    orientation="h",
    color="popularity",
    color_continuous_scale=["#169C46", "#1DB954", "#1ED760"],
    title="Top Genres by Average Popularity",
    labels={
        "popularity": "Average Popularity",
        "genres": "Genre"
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
# Genre Comparison
# -----------------------------

st.markdown('<div class="section-title">Compare Genres</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

# Get genre names for dropdown
genre_names = sorted(genres["genres"].unique())

# Two columns for genre selection
left, right = st.columns(2)

with left:
    genre1 = st.selectbox(
        "Genre A",
        genre_names,
        index=0 if genre_names else 0,
        placeholder="Type to search for a genre...",
        label_visibility="collapsed"
    )
    st.caption("Search for Genre A")

with right:
    default_index = 1 if len(genre_names) > 1 else 0
    genre2 = st.selectbox(
        "Genre B",
        genre_names,
        index=default_index,
        placeholder="Type to search for a genre...",
        label_visibility="collapsed"
    )
    st.caption("Search for Genre B")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# Create comparison button
if st.button("Compare Genres", use_container_width=True):
    if genre1 == genre2:
        st.warning("Please select two different genres for comparison.")
    else:
        g1 = genres[genres["genres"] == genre1].iloc[0]
        g2 = genres[genres["genres"] == genre2].iloc[0]

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        # Compare KPIs
        col1, col2 = st.columns(2)

        # Genre A
        with col1:
            st.markdown(f"""
            <div style="color:#FFFFFF; font-size:24px; font-weight:700; margin-bottom:16px;">{genre1}</div>
            """, unsafe_allow_html=True)
            
            metrics_col1, metrics_col2 = st.columns(2)
            
            with metrics_col1:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Popularity</div>
                    <div class="kpi-value">{g1['popularity']:.1f}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Danceability</div>
                    <div class="kpi-value">{g1['danceability']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Energy</div>
                    <div class="kpi-value">{g1['energy']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metrics_col2:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Valence</div>
                    <div class="kpi-value">{g1['valence']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Acousticness</div>
                    <div class="kpi-value">{g1['acousticness']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Speechiness</div>
                    <div class="kpi-value">{g1['speechiness']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)

        # Genre B
        with col2:
            st.markdown(f"""
            <div style="color:#FFFFFF; font-size:24px; font-weight:700; margin-bottom:16px;">{genre2}</div>
            """, unsafe_allow_html=True)
            
            metrics_col3, metrics_col4 = st.columns(2)
            
            with metrics_col3:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Popularity</div>
                    <div class="kpi-value">{g2['popularity']:.1f}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Danceability</div>
                    <div class="kpi-value">{g2['danceability']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Energy</div>
                    <div class="kpi-value">{g2['energy']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metrics_col4:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Valence</div>
                    <div class="kpi-value">{g2['valence']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Acousticness</div>
                    <div class="kpi-value">{g2['acousticness']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Speechiness</div>
                    <div class="kpi-value">{g2['speechiness']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

        # Radar Chart
        st.markdown('<div class="section-title">Audio Feature Comparison</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)

        fig_radar = create_radar_chart(
            g1, g2, FEATURES, 
            genre1, genre2,
            "Genre Audio Profile Comparison"
        )

        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

        # Comparison Summary
        st.markdown('<div class="section-title">Comparison Summary</div>', unsafe_allow_html=True)

        generate_comparison_summary(g1, g2, genre1, genre2, FEATURES_COMPARE)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        st.info(f"""
        **Key Insight**: The radar chart reveals that {genre1} and {genre2} have 
        distinct audio profiles. The overall "shape" of their features helps 
        understand their unique sound characteristics and audience appeal.
        """)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# -----------------------------
# Heatmap
# -----------------------------

st.markdown('<div class="section-title">Genre Audio Feature Heatmap</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

heatmap_data = genres.set_index("genres")[FEATURES]

top50_genres = (
    genres
    .sort_values("popularity", ascending=False)
    .head(50)["genres"]
    .tolist()
)

heatmap_top50 = heatmap_data.loc[top50_genres]

fig_heatmap = px.imshow(
    heatmap_top50,
    aspect="auto",
    color_continuous_scale="Viridis",
    labels=dict(x="Audio Features", y="Genre", color="Value")
)

fig_heatmap.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
    height=600,
    xaxis=dict(tickangle=45, tickfont=dict(color="#B3B3B3")),
    yaxis=dict(tickfont=dict(color="#B3B3B3")),
    margin=dict(l=10, r=10, t=10, b=10)
)

st.plotly_chart(fig_heatmap, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# -----------------------------
# Scatter Plot
# -----------------------------

st.markdown('<div class="section-title">Genre Energy vs Popularity</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

fig_scatter = px.scatter(
    genres,
    x="energy",
    y="popularity",
    size="danceability",
    hover_name="genres",
    color="valence",
    color_continuous_scale="Viridis",
    labels={
        "energy": "Energy Score",
        "popularity": "Popularity Score",
        "danceability": "Danceability",
        "valence": "Valence"
    },
    size_max=30
)

fig_scatter.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
    margin=dict(l=10, r=10, t=10, b=10),
    height=500,
    xaxis=dict(gridcolor="#282828", zeroline=False, tickfont=dict(color="#B3B3B3")),
    yaxis=dict(gridcolor="#282828", zeroline=False, tickfont=dict(color="#B3B3B3"))
)

st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# -----------------------------
# Genre Explorer
# -----------------------------

st.markdown('<div class="section-title">Genre Explorer</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

genre_search = st.text_input(
    "Search Genre",
    placeholder="Type a genre name...",
    help="Search for genres by name (case-insensitive)",
    label_visibility="collapsed"
)
st.caption("Search by genre name")

filtered_genres = genres.copy()

if genre_search:
    filtered_genres = filtered_genres[
        filtered_genres["genres"]
        .str.contains(genre_search, case=False, na=False)
    ]
    
    if len(filtered_genres) > 0:
        st.success(f"Found {len(filtered_genres)} genre(s) matching '{genre_search}'")
    else:
        st.warning(f"No genres found matching '{genre_search}'")

st.dataframe(
    filtered_genres,
    use_container_width=True,
    height=400,
    column_config={
        "genres": "Genre",
        "popularity": st.column_config.NumberColumn(
            "Popularity",
            format="%.1f"
        ),
        "danceability": st.column_config.NumberColumn(
            "Danceability",
            format="%.2f"
        ),
        "energy": st.column_config.NumberColumn(
            "Energy",
            format="%.2f"
        ),
        "valence": st.column_config.NumberColumn(
            "Valence",
            format="%.2f"
        ),
        "acousticness": st.column_config.NumberColumn(
            "Acousticness",
            format="%.2f"
        ),
        "speechiness": st.column_config.NumberColumn(
            "Speechiness",
            format="%.2f"
        ),
        "instrumentalness": st.column_config.NumberColumn(
            "Instrumentalness",
            format="%.2f"
        ),
    }
)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# -----------------------------
# Export Section
# -----------------------------

st.markdown('<div class="section-title">Export Genre Data</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

col_download1, col_download2, col_download3 = st.columns([1, 2, 1])

with col_download2:
    csv_genres = filtered_genres.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        csv_genres,
        file_name=f"genres_{len(filtered_genres)}.csv",
        mime="text/csv",
        use_container_width=True,
        help="Download the current genre data as a CSV file"
    )

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# -----------------------------
# Business Insights
# -----------------------------

st.markdown('<div class="section-title">Key Insights</div>', unsafe_allow_html=True)

col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    st.markdown("""
    <div class="table-card">
        <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-bottom:12px;">Genre Performance</div>
        <div style="color:#B3B3B3; font-size:14px; line-height:1.8;">
        • Some genres consistently achieve higher popularity than others<br>
        • The top genres show strong performance across multiple audio features<br>
        • Genre popularity distribution shows significant variation
        </div>
        <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-top:16px; margin-bottom:12px;">Audio Characteristics</div>
        <div style="color:#B3B3B3; font-size:14px; line-height:1.8;">
        • Danceability varies significantly across genres<br>
        • Highly energetic genres are not always the most popular<br>
        • Acousticness and instrumentalness define genre identity<br>
        • Speechiness is a key differentiator for certain genres
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_insight2:
    st.markdown("""
    <div class="table-card">
        <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-bottom:12px;">Strategic Recommendations</div>
        <div style="color:#B3B3B3; font-size:14px; line-height:1.8;">
        • Invest marketing resources in genres with high popularity and strong engagement<br>
        • Cross-genre collaboration opportunities where audio profiles are complementary<br>
        • Playlist curation can target specific audio feature combinations<br>
        • Emerging genres with unique audio profiles may represent untapped markets
        </div>
        <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-top:16px; margin-bottom:12px;">Future Applications</div>
        <div style="color:#B3B3B3; font-size:14px; line-height:1.8;">
        • Heatmaps help identify genre clusters for recommendation systems<br>
        • Radar charts enable visual genre positioning<br>
        • Time-based analysis can reveal genre evolution trends<br>
        • Machine learning can predict genre success based on audio features
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
st.caption(f"Updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}  •  {len(genres):,} Genres  •  {len(songs):,} Songs")