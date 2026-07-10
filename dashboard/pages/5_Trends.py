# dashboard/pages/5_Trends_Analytics.py

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
            page_title="Trends Analytics • Spotify Music Intelligence",
            page_icon=favicon,
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except:
        st.set_page_config(
            page_title="Trends Analytics • Spotify Music Intelligence",
            page_icon="",
            layout="wide",
            initial_sidebar_state="expanded"
        )
else:
    st.set_page_config(
        page_title="Trends Analytics • Spotify Music Intelligence",
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
            color: #E8C8D4 !important;
            font-weight: 400 !important;
            margin-top: 4px !important;
            letter-spacing: -0.3px !important;
        }
        
        /* Section Title */
        div.section-title {
            font-size: 28px !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
            margin-bottom: 16px !important;
            letter-spacing: 0.5px !important;
        }
        
        /* KPI Cards - Dark for pink theme */
        div.kpi-card {
            background: rgba(30, 20, 25, 0.92) !important;
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
        
        /* Chart container - Dark for pink theme */
        div.chart-card {
            background: rgba(30, 20, 25, 0.92) !important;
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
            background: rgba(30, 20, 25, 0.92) !important;
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
# Page-specific gradient (Dark Pink/Magenta for Trends)
# -----------------------------

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(
            circle at 50% -15%,
            rgba(255, 92, 145, 0.35),
            transparent 55%
        ),
        linear-gradient(
            180deg,
            #7C214A 0%,
            #5D1A39 20%,
            #40142A 40%,
            #27131F 60%,
            #181818 82%,
            #121212 100%
        ) !important;
    background-attachment: fixed !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Constants & Configuration
# -----------------------------
METRICS = ["popularity", "danceability", "energy", "tempo"]
METRIC_LABELS = {
    "popularity": "Popularity",
    "danceability": "Danceability",
    "energy": "Energy",
    "tempo": "Tempo"
}
METRIC_DESCRIPTIONS = {
    "popularity": "How has the average popularity of songs evolved over the years?",
    "danceability": "Are modern songs becoming more danceable? Let's find out.",
    "energy": "How has the energy level of popular music changed over the decades?",
    "tempo": "Are songs getting faster or slower? Explore tempo evolution."
}

# Check available columns and filter
available_metrics = [m for m in METRICS if m in years.columns]
if not available_metrics:
    st.error("No trend metrics found in the dataset. Please check your data.")
    st.stop()

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
            <div class="hero-title">Trends Analytics</div>
            <div class="hero-subtitle">Discover How Music Has Evolved Over Time</div>
            <p style="color:#E8C8D4; font-size:15px; margin-top:12px; font-weight:500;">
                <b>{years['year'].min()}–{years['year'].max()}</b> Years
                &nbsp;&nbsp;•&nbsp;&nbsp;
                <b>{len(songs):,}</b> Songs
                &nbsp;&nbsp;•&nbsp;&nbsp;
                <b>{len(available_metrics)}</b> Metrics
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
            <div class="hero-title">Trends Analytics</div>
            <div class="hero-subtitle">Discover How Music Has Evolved Over Time</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# -----------------------------
# KPI Cards
# -----------------------------

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

latest_year = years['year'].max()
earliest_year = years['year'].min()
latest_pop = years[years['year'] == latest_year]['popularity'].values[0]
earliest_pop = years[years['year'] == earliest_year]['popularity'].values[0]
pop_change = latest_pop - earliest_pop

with col_kpi1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Years Covered</div>
        <div class="kpi-value">{earliest_year}–{latest_year}</div>
        <div class="kpi-delta">▲ {latest_year - earliest_year} years</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Latest Popularity</div>
        <div class="kpi-value">{latest_pop:.1f}</div>
        <div class="kpi-delta">▲ Latest year</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Earliest Popularity</div>
        <div class="kpi-value">{earliest_pop:.1f}</div>
        <div class="kpi-delta">▲ Earliest year</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Change</div>
        <div class="kpi-value">{pop_change:+.1f}</div>
        <div class="kpi-delta">▲ {pop_change:+.1f} change</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# -----------------------------
# Individual Trend Charts
# -----------------------------
for metric in available_metrics:
    st.markdown(f'<div class="section-title">{METRIC_LABELS.get(metric, metric.capitalize())}</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    
    fig = px.line(
        years,
        x="year",
        y=metric,
        markers=True,
        labels={"year": "Year", metric: f"Average {metric.capitalize()}"},
        color_discrete_sequence=["#1DB954"]
    )
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=350,
        xaxis=dict(gridcolor="#282828", zeroline=False, tickfont=dict(color="#B3B3B3")),
        yaxis=dict(gridcolor="#282828", zeroline=False, tickfont=dict(color="#B3B3B3")),
        hovermode="x unified"
    )
    
    fig.update_traces(
        line=dict(width=2),
        marker=dict(size=6)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# -----------------------------
# Rolling Averages
# -----------------------------

st.markdown('<div class="section-title">Rolling Averages</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown("""
<div style="color:#B3B3B3; font-size:14px; margin-bottom:16px;">
Rolling averages smooth out year-to-year fluctuations to reveal underlying trends.
</div>
""", unsafe_allow_html=True)

# Calculate rolling averages
for metric in available_metrics:
    if metric != "tempo":
        years[f"rolling_{metric}"] = years[metric].rolling(5).mean()

# Create rolling average charts
metric_pairs = [
    ("popularity", "Popularity"),
    ("danceability", "Danceability"),
    ("energy", "Energy")
]

for metric, label in metric_pairs:
    if metric in available_metrics and f"rolling_{metric}" in years.columns:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=years["year"],
            y=years[metric],
            name=f"Actual {label}",
            line=dict(color="#1DB954", width=1.5),
            opacity=0.5
        ))
        
        fig.add_trace(go.Scatter(
            x=years["year"],
            y=years[f"rolling_{metric}"],
            name="5-Year Rolling Average",
            line=dict(color="#F8C7D8", width=3)
        ))
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
            title=dict(text=f"{label} with 5-Year Rolling Average", font=dict(color="#FFFFFF", size=16)),
            xaxis_title=dict(text="Year", font=dict(color="#B3B3B3")),
            yaxis_title=dict(text=label, font=dict(color="#B3B3B3")),
            height=350,
            legend=dict(font=dict(color="#B3B3B3"), bgcolor="rgba(0,0,0,0.5)"),
            hovermode="x unified",
            xaxis=dict(gridcolor="#282828", zeroline=False, tickfont=dict(color="#B3B3B3")),
            yaxis=dict(gridcolor="#282828", zeroline=False, tickfont=dict(color="#B3B3B3")),
            margin=dict(l=10, r=10, t=40, b=10)
        )
        
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# -----------------------------
# Year-over-Year Growth
# -----------------------------

st.markdown('<div class="section-title">Year-over-Year Growth</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-card">', unsafe_allow_html=True)

if "popularity" in available_metrics:
    years["pop_growth"] = years["popularity"].pct_change() * 100
    
    fig_growth = px.bar(
        years,
        x="year",
        y="pop_growth",
        labels={"year": "Year", "pop_growth": "Growth Rate (%)"},
        color="pop_growth",
        color_continuous_scale=["#9b1d4d", "#d64d7b", "#ffffff", "#53d769", "#1DB954"]
    )
    
    fig_growth.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=350,
        xaxis=dict(gridcolor="#282828", zeroline=False, tickfont=dict(color="#B3B3B3")),
        yaxis=dict(gridcolor="#282828", zeroline=False, tickfont=dict(color="#B3B3B3"))
    )
    
    fig_growth.add_hline(y=0, line_dash="dash", line_color="#F8C7D8", opacity=0.5)
    
    st.plotly_chart(fig_growth, use_container_width=True, config={"displayModeBar": False})

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# -----------------------------
# Combined Trends Dashboard
# -----------------------------

st.markdown('<div class="section-title">Combined Trends</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-card">', unsafe_allow_html=True)

if len(available_metrics) >= 2:
    n_metrics = len(available_metrics)
    n_cols = 2 if n_metrics > 2 else n_metrics
    n_rows = (n_metrics + 1) // 2
    
    fig_combined = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=[METRIC_LABELS.get(m, m.capitalize()) for m in available_metrics])
    
    colors = ["#1DB954", "#F8C7D8", "#4ECDC4", "#FFE66D"]
    
    for idx, metric in enumerate(available_metrics):
        row = idx // 2 + 1
        col = idx % 2 + 1
        
        fig_combined.add_trace(
            go.Scatter(
                x=years["year"],
                y=years[metric],
                mode="lines+markers",
                name=METRIC_LABELS.get(metric, metric.capitalize()),
                line=dict(color=colors[idx % len(colors)], width=2),
                marker=dict(size=5)
            ),
            row=row,
            col=col
        )
    
    fig_combined.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B3B3B3", family="Inter, sans-serif", size=12),
        height=500,
        showlegend=False,
        hovermode="x unified",
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    # Update axes for each subplot
    for row in range(1, n_rows + 1):
        for col in range(1, n_cols + 1):
            fig_combined.update_xaxes(gridcolor="#282828", zeroline=False, tickfont=dict(color="#B3B3B3"), row=row, col=col)
            fig_combined.update_yaxes(gridcolor="#282828", zeroline=False, tickfont=dict(color="#B3B3B3"), row=row, col=col)
    
    st.plotly_chart(fig_combined, use_container_width=True, config={"displayModeBar": False})

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
        <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-bottom:12px;">Trend Analysis</div>
        <div style="color:#B3B3B3; font-size:14px; line-height:1.8;">
        • Popularity has evolved over the years, reflecting changes in listener engagement<br>
        • Danceability trends reveal shifting preferences for rhythm and groove<br>
        • Energy levels show how musical intensity has evolved<br>
        • Tempo analysis indicates changing pace preferences
        </div>
        <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-top:16px; margin-bottom:12px;">Statistical Patterns</div>
        <div style="color:#B3B3B3; font-size:14px; line-height:1.8;">
        • Rolling averages reveal underlying trends beyond short-term fluctuations<br>
        • Year-over-year growth identifies periods of significant change<br>
        • Combined trends show the relationship between different musical attributes
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_insight2:
    st.markdown("""
    <div class="table-card">
        <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-bottom:12px;">Strategic Recommendations</div>
        <div style="color:#B3B3B3; font-size:14px; line-height:1.8;">
        • Use trend data to predict future musical directions<br>
        • Identify which audio features are gaining or losing popularity<br>
        • Inform A&R decisions based on emerging trends<br>
        • Guide playlist curation toward trending sounds
        </div>
        <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-top:16px; margin-bottom:12px;">Future Applications</div>
        <div style="color:#B3B3B3; font-size:14px; line-height:1.8;">
        • Extend analysis to specific genres or artists<br>
        • Build predictive models for trend forecasting<br>
        • Identify correlations between trends and external factors<br>
        • Create automated trend alerts for significant changes
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
st.caption(f"Updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}  •  {years['year'].min()}–{years['year'].max()} Years  •  {len(songs):,} Songs")