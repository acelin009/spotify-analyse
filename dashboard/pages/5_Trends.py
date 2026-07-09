# dashboard/pages/5_Trends_Analytics.py

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from data_loader import load_data

# Page Configuration
st.set_page_config(
    page_title="Trends Analytics",
    page_icon="📈",
    layout="wide"
)

# Load Data
songs, artists, genres, years, songs_with_genres = load_data()

# -----------------------------
# Constants & Configuration
# -----------------------------
METRICS = ["popularity", "danceability", "energy", "tempo"]
METRIC_LABELS = {
    "popularity": "⭐ Popularity",
    "danceability": "💃 Danceability",
    "energy": "⚡ Energy",
    "tempo": "🎵 Tempo"
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
# Page Title
# -----------------------------
st.title("📈 Trends Analytics")
st.write("Explore how music has evolved over time. Analyze trends in popularity, danceability, energy, and tempo across the years.")
st.divider()

# -----------------------------
# KPI Cards
# -----------------------------
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.metric("📅 Years Covered", f"{years['year'].min()} - {years['year'].max()}")

with col_kpi2:
    latest_pop = years[years['year'] == years['year'].max()]['popularity'].values[0]
    st.metric("⭐ Latest Avg Popularity", f"{latest_pop:.1f}")

with col_kpi3:
    earliest_pop = years[years['year'] == years['year'].min()]['popularity'].values[0]
    st.metric("📊 Earliest Avg Popularity", f"{earliest_pop:.1f}")

with col_kpi4:
    pop_change = latest_pop - earliest_pop
    st.metric("📈 Total Change", f"{pop_change:+.1f}", delta=f"{pop_change:+.1f}")

st.divider()

# -----------------------------
# Individual Trend Charts
# -----------------------------
for metric in available_metrics:
    st.subheader(METRIC_LABELS.get(metric, metric.capitalize()))
    st.write(METRIC_DESCRIPTIONS.get(metric, f"Track {metric} over time."))
    
    fig = px.line(
        years,
        x="year",
        y=metric,
        markers=True,
        title=f"{METRIC_LABELS.get(metric, metric.capitalize())} Over Time",
        labels={"year": "Year", metric: f"Average {metric.capitalize()}"}
    )
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#121212",
        plot_bgcolor="#121212",
        font=dict(color="white"),
        height=400,
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.divider()

# -----------------------------
# Rolling Averages
# -----------------------------
st.subheader("📊 Rolling Averages")
st.write("Rolling averages smooth out year-to-year fluctuations to reveal underlying trends.")

# Calculate rolling averages
for metric in available_metrics:
    if metric != "tempo":  # Tempo doesn't need rolling average
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
            line=dict(color="#1DB954", width=1),
            opacity=0.5
        ))
        
        fig.add_trace(go.Scatter(
            x=years["year"],
            y=years[f"rolling_{metric}"],
            name="5-Year Rolling Average",
            line=dict(color="#FF6B6B", width=3)
        ))
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#121212",
            plot_bgcolor="#121212",
            font=dict(color="white"),
            title=f"{label} with 5-Year Rolling Average",
            xaxis_title="Year",
            yaxis_title=label,
            height=400,
            legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0.5)"),
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.info("💡 **Business Insight**: The rolling average reveals the underlying trend, filtering out short-term fluctuations to show the true direction of change.")
st.divider()

# -----------------------------
# Year-over-Year Growth
# -----------------------------
st.subheader("📈 Year-over-Year Growth")
st.write("See the percentage change in popularity from year to year.")

if "popularity" in available_metrics:
    years["pop_growth"] = years["popularity"].pct_change() * 100
    
    fig_growth = px.bar(
        years,
        x="year",
        y="pop_growth",
        title="Popularity Growth (%)",
        labels={"year": "Year", "pop_growth": "Growth Rate (%)"},
        color="pop_growth",
        color_continuous_scale="RdYlGn"
    )
    
    fig_growth.update_layout(
        template="plotly_dark",
        paper_bgcolor="#121212",
        plot_bgcolor="#121212",
        font=dict(color="white"),
        height=400,
        hovermode="x unified"
    )
    
    fig_growth.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.3)
    
    st.plotly_chart(fig_growth, use_container_width=True, config={"displayModeBar": False})
    
    st.info("💡 **Business Insight**: Positive growth rates indicate years where music resonated more with listeners, while negative rates suggest potential shifts in taste or market saturation.")
    st.divider()

# -----------------------------
# Combined Trends Dashboard
# -----------------------------
st.subheader("📊 Trends Dashboard")
st.write("Compare all trends in one view to see the big picture.")

if len(available_metrics) >= 2:
    # Determine grid layout
    n_metrics = len(available_metrics)
    n_cols = 2 if n_metrics > 2 else n_metrics
    n_rows = (n_metrics + 1) // 2
    
    fig_combined = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=[METRIC_LABELS.get(m, m.capitalize()) for m in available_metrics])
    
    colors = ["#1DB954", "#FF6B6B", "#4ECDC4", "#FFE66D"]
    
    for idx, metric in enumerate(available_metrics):
        row = idx // 2 + 1
        col = idx % 2 + 1
        
        fig_combined.add_trace(
            go.Scatter(
                x=years["year"],
                y=years[metric],
                mode="lines+markers",
                name=METRIC_LABELS.get(metric, metric.capitalize()),
                line=dict(color=colors[idx % len(colors)])
            ),
            row=row,
            col=col
        )
    
    fig_combined.update_layout(
        template="plotly_dark",
        paper_bgcolor="#121212",
        plot_bgcolor="#121212",
        font=dict(color="white"),
        height=600,
        showlegend=False,
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_combined, use_container_width=True, config={"displayModeBar": False})

st.divider()

# -----------------------------
# Business Insights
# -----------------------------
st.subheader("📌 Key Business Insights")

col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    st.markdown("""
    **🎯 Trend Analysis**
    - Popularity has evolved over the years, reflecting changes in listener engagement
    - Danceability trends reveal shifting preferences for rhythm and groove
    - Energy levels show how musical intensity has evolved
    - Tempo analysis indicates changing pace preferences
    
    **📊 Statistical Patterns**
    - Rolling averages reveal underlying trends beyond short-term fluctuations
    - Year-over-year growth identifies periods of significant change
    - Combined trends show the relationship between different musical attributes
    """)

with col_insight2:
    st.markdown("""
    **💡 Strategic Recommendations**
    - Use trend data to predict future musical directions
    - Identify which audio features are gaining or losing popularity
    - Inform A&R decisions based on emerging trends
    - Guide playlist curation toward trending sounds
    
    **🔮 Future Applications**
    - Extend analysis to specific genres or artists
    - Build predictive models for trend forecasting
    - Identify correlations between trends and external factors
    - Create automated trend alerts for significant changes
    """)

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption(f"Data last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption(f"Total years in dataset: {len(years):,} | Total songs: {len(songs):,}")