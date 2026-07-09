# dashboard/pages/4_Genre_Analytics.py

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from data_loader import load_data

# Page Configuration
st.set_page_config(
    page_title="Genre Analytics",
    page_icon="🎸",
    layout="wide"
)

# Load Data
songs, artists, genres, years, songs_with_genres = load_data()

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
            line=dict(color="#FF6B6B"),
            fillcolor="rgba(255, 107, 107, 0.3)"
        )
    )
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#121212",
        plot_bgcolor="#121212",
        font=dict(color="white"),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickfont=dict(color="white")
            ),
            angularaxis=dict(
                tickfont=dict(color="white")
            )
        ),
        title=dict(
            text=title,
            font=dict(color="white")
        ),
        legend=dict(
            font=dict(color="white"),
            bgcolor="rgba(0,0,0,0.5)"
        ),
        height=600
    )
    
    return fig

def generate_comparison_summary(entity_a, entity_b, label_a, label_b, features):
    """
    Generate comparison summary between two entities.
    """
    col_summary1, col_summary2 = st.columns(2)
    
    # Entity A advantages
    with col_summary1:
        st.markdown(f"**{label_a} has higher:**")
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
    
    # Entity B advantages
    with col_summary2:
        st.markdown(f"**{label_b} has higher:**")
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

# -----------------------------
# Page Title
# -----------------------------
st.title("🎸 Genre Analytics")

st.write(
    """
    Analyze Spotify genres using popularity and audio features. 
    Compare genres and discover their unique musical characteristics.
    """
)

st.divider()

# -----------------------------
# Step 3: Top Genre KPI
# -----------------------------
top_genre = genres.sort_values(
    "popularity",
    ascending=False
).iloc[0]

# Display KPIs
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.metric(
        "🏆 Most Popular Genre",
        top_genre["genres"],
        f"{top_genre['popularity']:.1f} avg popularity"
    )

with col_kpi2:
    st.metric(
        "🎼 Total Genres",
        f"{len(genres):,}"
    )

with col_kpi3:
    avg_genre_pop = genres['popularity'].mean()
    st.metric(
        "⭐ Avg Genre Popularity",
        f"{avg_genre_pop:.1f}"
    )

with col_kpi4:
    # Fix: Use len(songs) instead of songs["genres"].count()
    total_songs = len(songs)
    st.metric(
        "📀 Total Songs",
        f"{total_songs:,}"
    )

st.divider()

# -----------------------------
# Step 4: Top 20 Genres
# -----------------------------
st.subheader("🏆 Top 20 Genres by Popularity")

top20 = (
    genres
    .sort_values(
        "popularity",
        ascending=False
    )
    .head(20)
)

fig_top = px.bar(
    top20,
    x="popularity",
    y="genres",
    orientation="h",
    color="popularity",
    color_continuous_scale="Viridis",
    title="Top 20 Genres by Average Popularity",
    labels={
        "popularity": "Average Popularity",
        "genres": "Genre"
    }
)

fig_top.update_layout(
    template="plotly_dark",
    paper_bgcolor="#121212",
    plot_bgcolor="#121212",
    font=dict(color="white"),
    height=500,
    xaxis=dict(range=[0, 100])
)

st.plotly_chart(
    fig_top,
    use_container_width=True,
    config={"displayModeBar": False}
)

# Business Insight
st.info(
    """
    💡 **Business Insight**: These genres consistently produce highly popular songs and may 
    deserve greater editorial promotion and playlist placement.
    """
)

st.divider()

# -----------------------------
# Step 5-6: Genre Comparison
# -----------------------------
st.subheader("🎯 Compare Genres")

st.write(
    """
    Select two genres to compare their audio features and popularity metrics.
    """
)

# Get genre names for dropdown
genre_names = sorted(
    genres["genres"].unique()
)

# Two columns for genre selection
left, right = st.columns(2)

with left:
    genre1 = st.selectbox(
        "🎸 Select Genre A",
        genre_names,
        index=0 if genre_names else 0,
        placeholder="Type to search for a genre..."
    )

with right:
    default_index = 1 if len(genre_names) > 1 else 0
    genre2 = st.selectbox(
        "🎸 Select Genre B",
        genre_names,
        index=default_index,
        placeholder="Type to search for a genre..."
    )

# Create comparison button
if st.button("🔄 Compare Genres", use_container_width=True):
    if genre1 == genre2:
        st.warning("Please select two different genres for comparison.")
    else:
        # Extract genre data
        g1 = genres[genres["genres"] == genre1].iloc[0]
        g2 = genres[genres["genres"] == genre2].iloc[0]

        st.divider()

        # Compare KPIs
        col1, col2 = st.columns(2)

        # Genre A
        with col1:
            st.subheader(f"🎸 {genre1}")
            
            # Create metrics in a grid
            metrics_col1, metrics_col2 = st.columns(2)
            
            with metrics_col1:
                st.metric(
                    "⭐ Popularity",
                    f"{g1['popularity']:.1f}"
                )
                st.metric(
                    "💃 Danceability",
                    f"{g1['danceability']:.2f}"
                )
                st.metric(
                    "⚡ Energy",
                    f"{g1['energy']:.2f}"
                )
            
            with metrics_col2:
                st.metric(
                    "😊 Valence",
                    f"{g1['valence']:.2f}"
                )
                st.metric(
                    "🎸 Acousticness",
                    f"{g1['acousticness']:.2f}"
                )
                st.metric(
                    "🎤 Speechiness",
                    f"{g1['speechiness']:.2f}"
                )

        # Genre B
        with col2:
            st.subheader(f"🎸 {genre2}")
            
            metrics_col3, metrics_col4 = st.columns(2)
            
            with metrics_col3:
                st.metric(
                    "⭐ Popularity",
                    f"{g2['popularity']:.1f}"
                )
                st.metric(
                    "💃 Danceability",
                    f"{g2['danceability']:.2f}"
                )
                st.metric(
                    "⚡ Energy",
                    f"{g2['energy']:.2f}"
                )
            
            with metrics_col4:
                st.metric(
                    "😊 Valence",
                    f"{g2['valence']:.2f}"
                )
                st.metric(
                    "🎸 Acousticness",
                    f"{g2['acousticness']:.2f}"
                )
                st.metric(
                    "🎤 Speechiness",
                    f"{g2['speechiness']:.2f}"
                )

        st.divider()

        # -----------------------------
        # Step 6: Radar Chart
        # -----------------------------
        st.subheader("📊 Genre Audio Feature Comparison")

        # Create radar chart using helper function
        fig_radar = create_radar_chart(
            g1, g2, FEATURES, 
            genre1, genre2,
            "Genre Audio Profile Comparison"
        )

        st.plotly_chart(
            fig_radar,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        # -----------------------------
        # Comparison Summary
        # -----------------------------
        st.divider()
        st.subheader("📌 Comparison Summary")

        # Use helper function for comparison
        generate_comparison_summary(g1, g2, genre1, genre2, FEATURES_COMPARE)

        st.divider()
        st.info(
            f"""
            💡 **Key Insight**: The radar chart reveals that {genre1} and {genre2} have 
            distinct audio profiles. The overall "shape" of their features helps 
            understand their unique sound characteristics and audience appeal.
            """
        )

st.divider()

# -----------------------------
# Step 7: Heatmap
# -----------------------------
st.subheader("🔥 Genre Audio Feature Heatmap")

st.write(
    """
    This heatmap shows the average audio features for each genre. 
    Darker colors indicate higher values.
    """
)

# Prepare heatmap data - using FEATURES constant
heatmap_data = genres.set_index("genres")[FEATURES]

# Limit to top 50 genres for readability
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
    title="Top 50 Genres - Audio Feature Heatmap",
    labels=dict(
        x="Audio Features",
        y="Genre",
        color="Value"
    )
)

fig_heatmap.update_layout(
    template="plotly_dark",
    paper_bgcolor="#121212",
    plot_bgcolor="#121212",
    font=dict(color="white"),
    height=600,
    xaxis=dict(tickangle=45)
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True,
    config={"displayModeBar": False}
)

st.info(
    """
    💡 **Business Insight**: Genres with similar color patterns have similar audio characteristics. 
    This helps identify genre clusters and potential cross-genre opportunities.
    """
)

st.divider()

# -----------------------------
# Step 8: Scatter Plot
# -----------------------------
st.subheader("📊 Genre Energy vs Popularity")

st.write(
    """
    Each bubble represents a genre. Size represents danceability, 
    and color represents valence (musical positiveness).
    """
)

fig_scatter = px.scatter(
    genres,
    x="energy",
    y="popularity",
    size="danceability",
    hover_name="genres",
    color="valence",
    color_continuous_scale="Viridis",
    title="Genre Energy vs Popularity",
    labels={
        "energy": "Energy Score",
        "popularity": "Popularity Score",
        "danceability": "Danceability",
        "valence": "Valence"
    },
    size_max=30,
    height=500
)

fig_scatter.update_layout(
    template="plotly_dark",
    paper_bgcolor="#121212",
    plot_bgcolor="#121212",
    font=dict(color="white"),
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True,
    config={"displayModeBar": False}
)

# Business Insight
st.info(
    """
    💡 **Business Insight**: Highly energetic genres are not always the most popular. 
    Genres with moderate energy but high danceability often perform better across audiences.
    """
)

st.divider()

# -----------------------------
# Step 9: Genre Explorer
# -----------------------------
st.subheader("🔍 Genre Explorer")

st.write(
    """
    Search for specific genres and explore their audio features and popularity.
    """
)

# Search box
genre_search = st.text_input(
    "🔍 Search Genre",
    placeholder="Type a genre name...",
    help="Search for genres by name (case-insensitive)"
)

# Filter genres
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

# Display genre data
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

# Download filtered genres
st.markdown("---")
csv_genres = filtered_genres.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇ Download Genre Data (CSV)",
    csv_genres,
    file_name=f"genres_{len(filtered_genres)}.csv",
    mime="text/csv",
    use_container_width=True,
    help="Download the current genre data as a CSV file"
)

st.divider()

# -----------------------------
# Step 10: Business Insights
# -----------------------------
st.subheader("📌 Key Business Insights")

col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    st.markdown("""
    **🎯 Genre Performance**
    - Some genres consistently achieve higher popularity than others
    - The top genres show strong performance across multiple audio features
    - Genre popularity distribution shows significant variation
    
    **🎵 Audio Characteristics**
    - Danceability varies significantly across genres
    - Highly energetic genres are not always the most popular
    - Acousticness and instrumentalness define genre identity
    - Speechiness is a key differentiator for certain genres
    """)

with col_insight2:
    st.markdown("""
    **💡 Strategic Recommendations**
    - Invest marketing resources in genres with high popularity and strong engagement
    - Cross-genre collaboration opportunities where audio profiles are complementary
    - Playlist curation can target specific audio feature combinations
    - Emerging genres with unique audio profiles may represent untapped markets
    
    **🔮 Future Applications**
    - Heatmaps help identify genre clusters for recommendation systems
    - Radar charts enable visual genre positioning
    - Time-based analysis can reveal genre evolution trends
    - Machine learning can predict genre success based on audio features
    """)

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption(f"Data last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption(f"Total genres in dataset: {len(genres):,} | Total songs: {len(songs):,}")