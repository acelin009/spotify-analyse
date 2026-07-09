# dashboard/pages/3_Artist_Analytics.py

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from data_loader import load_data

# Page Configuration
st.set_page_config(
    page_title="Artist Analytics",
    page_icon="🎤",
    layout="wide"
)

# Load Data
songs, artists, genres, years, songs_with_genres = load_data()

# -----------------------------
# Page Title
# -----------------------------
st.title("🎤 Artist Analytics")

st.write(
    """
    Analyze artist performance and compare musical characteristics. 
    Discover insights about top artists and their audio profiles.
    """
)

st.divider()

# -----------------------------
# Step 3: Top Artist KPI
# -----------------------------
top_artist = artists.sort_values(
    "popularity",
    ascending=False
).iloc[0]

# Display top artist KPI with styling
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.metric(
        "🏆 Most Popular Artist",
        top_artist["artists"],
        f"{top_artist['popularity']:.1f} avg popularity"
    )

with col_kpi2:
    st.metric(
        "🎵 Total Artists",
        f"{len(artists):,}"
    )

with col_kpi3:
    avg_artist_pop = artists['popularity'].mean()
    st.metric(
        "⭐ Avg Artist Popularity",
        f"{avg_artist_pop:.1f}"
    )

with col_kpi4:
    total_songs = songs['artists'].count()
    st.metric(
        "📀 Total Songs",
        f"{total_songs:,}"
    )

st.divider()

# -----------------------------
# Step 4: Top 15 Artists
# -----------------------------
st.subheader("🏆 Top 15 Artists by Popularity")

top15 = (
    artists
    .sort_values(
        "popularity",
        ascending=False
    )
    .head(15)
)

fig_top = px.bar(
    top15,
    x="popularity",
    y="artists",
    orientation="h",
    color="popularity",
    color_continuous_scale="Viridis",
    title="Top 15 Artists by Average Popularity",
    labels={
        "popularity": "Average Popularity",
        "artists": "Artist"
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

st.divider()

# -----------------------------
# Step 5-8: Artist Comparison with Search Boxes
# -----------------------------
st.subheader("🎯 Compare Artists")

st.write(
    """
    Search for two artists to compare their audio features and popularity metrics.
    """
)

# Two columns for artist search
left, right = st.columns(2)

with left:
    artist1_search = st.text_input(
        "🎤 Search Artist A",
        placeholder="Type artist name... (e.g., Taylor Swift)",
        help="Type the name of the first artist to compare"
    )

with right:
    artist2_search = st.text_input(
        "🎤 Search Artist B",
        placeholder="Type artist name... (e.g., Ed Sheeran)",
        help="Type the name of the second artist to compare"
    )

# Search for artists in the dataset
if artist1_search and artist2_search:
    # Find matching artists
    artist_a_matches = artists[
        artists["artists"].str.contains(artist1_search, case=False, na=False)
    ]
    artist_b_matches = artists[
        artists["artists"].str.contains(artist2_search, case=False, na=False)
    ]
    
    # Check if artists were found
    if len(artist_a_matches) == 0:
        st.warning(f"❌ No artist found matching '{artist1_search}'. Please try a different name.")
    elif len(artist_b_matches) == 0:
        st.warning(f"❌ No artist found matching '{artist2_search}'. Please try a different name.")
    else:
        # Use the first match if multiple found
        a = artist_a_matches.iloc[0]
        b = artist_b_matches.iloc[0]
        
        # Check if same artist
        if a["artists"] == b["artists"]:
            st.warning("⚠️ Please search for two different artists.")
        else:
            # Display artist names
            st.success(f"✅ Found: **{a['artists']}** and **{b['artists']}**")
            
            # Show all matches if multiple found
            if len(artist_a_matches) > 1:
                with st.expander(f"Multiple matches found for '{artist1_search}'"):
                    st.write("Did you mean one of these?")
                    for idx, row in artist_a_matches.iterrows():
                        st.write(f"• {row['artists']} (Popularity: {row['popularity']:.1f})")
            
            if len(artist_b_matches) > 1:
                with st.expander(f"Multiple matches found for '{artist2_search}'"):
                    st.write("Did you mean one of these?")
                    for idx, row in artist_b_matches.iterrows():
                        st.write(f"• {row['artists']} (Popularity: {row['popularity']:.1f})")
            
            st.divider()

            # Step 7: Compare KPIs
            col1, col2 = st.columns(2)

            # Artist A
            with col1:
                st.subheader(f"🎤 {a['artists']}")
                
                # Create metrics in a grid
                metrics_col1, metrics_col2 = st.columns(2)
                
                with metrics_col1:
                    st.metric(
                        "⭐ Popularity",
                        f"{a['popularity']:.1f}"
                    )
                    st.metric(
                        "💃 Danceability",
                        f"{a['danceability']:.2f}"
                    )
                    st.metric(
                        "⚡ Energy",
                        f"{a['energy']:.2f}"
                    )
                
                with metrics_col2:
                    st.metric(
                        "😊 Valence",
                        f"{a['valence']:.2f}"
                    )
                    st.metric(
                        "🎸 Acousticness",
                        f"{a['acousticness']:.2f}"
                    )
                    st.metric(
                        "🎤 Speechiness",
                        f"{a['speechiness']:.2f}"
                    )

            # Artist B
            with col2:
                st.subheader(f"🎤 {b['artists']}")
                
                metrics_col3, metrics_col4 = st.columns(2)
                
                with metrics_col3:
                    st.metric(
                        "⭐ Popularity",
                        f"{b['popularity']:.1f}"
                    )
                    st.metric(
                        "💃 Danceability",
                        f"{b['danceability']:.2f}"
                    )
                    st.metric(
                        "⚡ Energy",
                        f"{b['energy']:.2f}"
                    )
                
                with metrics_col4:
                    st.metric(
                        "😊 Valence",
                        f"{b['valence']:.2f}"
                    )
                    st.metric(
                        "🎸 Acousticness",
                        f"{b['acousticness']:.2f}"
                    )
                    st.metric(
                        "🎤 Speechiness",
                        f"{b['speechiness']:.2f}"
                    )

            st.divider()

            # -----------------------------
            # Step 8: Radar Chart
            # -----------------------------
            st.subheader("📊 Audio Feature Comparison")

            features = [
                "danceability",
                "energy",
                "acousticness",
                "speechiness",
                "valence",
                "liveness"
            ]

            # Create radar chart
            fig_radar = go.Figure()

            # Artist A
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=[a[f] for f in features],
                    theta=[f.capitalize() for f in features],
                    fill="toself",
                    name=a['artists'],
                    line=dict(color="#1DB954"),
                    fillcolor="rgba(29, 185, 84, 0.3)"
                )
            )

            # Artist B
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=[b[f] for f in features],
                    theta=[f.capitalize() for f in features],
                    fill="toself",
                    name=b['artists'],
                    line=dict(color="#FF6B6B"),
                    fillcolor="rgba(255, 107, 107, 0.3)"
                )
            )

            fig_radar.update_layout(
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
                    text="Artist Audio Feature Comparison",
                    font=dict(color="white")
                ),
                legend=dict(
                    font=dict(color="white"),
                    bgcolor="rgba(0,0,0,0.5)"
                ),
                height=600
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

            # Auto-generate comparison insights
            col_summary1, col_summary2 = st.columns(2)

            # Artist A advantages
            with col_summary1:
                st.markdown(f"**{a['artists']} has higher:**")
                advantages_a = []
                
                # Compare all audio features
                features_compare = [
                    "popularity", 
                    "danceability", 
                    "energy", 
                    "valence", 
                    "acousticness",
                    "speechiness"
                ]
                
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

            # Artist B advantages
            with col_summary2:
                st.markdown(f"**{b['artists']} has higher:**")
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

            # Additional insight
            st.divider()
            st.info(
                f"""
                **💡 Key Insight**: The radar chart reveals that {a['artists']} and {b['artists']} have 
                distinct musical profiles. The overall "shape" of their audio features 
                helps understand their unique sound characteristics.
                """
            )

# Show helpful message if both artists not searched
elif artist1_search and not artist2_search:
    st.info("🔍 Please search for a second artist (Artist B) to compare.")
elif not artist1_search and artist2_search:
    st.info("🔍 Please search for a first artist (Artist A) to compare.")
else:
    st.info("🔍 Enter two artist names above to compare their audio features and popularity metrics.")

# -----------------------------
# Step 9: Distribution
# -----------------------------
st.divider()
st.subheader("📊 Artist Popularity Distribution")

fig_dist = px.histogram(
    artists,
    x="popularity",
    nbins=20,
    title="Artist Popularity Distribution",
    labels={"popularity": "Popularity Score", "count": "Number of Artists"},
    color_discrete_sequence=["#1DB954"]
)

fig_dist.update_layout(
    template="plotly_dark",
    paper_bgcolor="#121212",
    plot_bgcolor="#121212",
    font=dict(color="white"),
    height=400,
    bargap=0.1
)

# Add vertical line for mean
fig_dist.add_vline(
    x=artists['popularity'].mean(),
    line_dash="dash",
    line_color="red",
    annotation_text=f"Mean: {artists['popularity'].mean():.1f}",
    annotation_font=dict(color="white")
)

st.plotly_chart(
    fig_dist,
    use_container_width=True,
    config={"displayModeBar": False}
)

# -----------------------------
# Step 10: Business Insights
# -----------------------------
st.divider()
st.subheader("📌 Key Business Insights")

col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    st.markdown("""
    **🎯 Artist Performance**
    - Most artists have moderate popularity, with only a few reaching the highest levels
    - The distribution shows a long tail, typical of music industry data
    - Top artists consistently show higher engagement across multiple audio features
    
    **🎵 Audio Characteristics**
    - Radar charts reveal distinct musical styles across artists
    - High popularity does not always correspond to high energy or danceability
    - Acousticness and speechiness vary significantly across artists
    """)

with col_insight2:
    st.markdown("""
    **💡 Strategic Recommendations**
    - A&R teams can use audio feature profiles to identify emerging artists with desired sound characteristics
    - Marketing can tailor campaigns based on an artist's unique audio footprint
    - Playlist curators can identify artists that would complement specific moods or activities
    
    **🔮 Future Applications**
    - Audio features can help identify unique artist profiles and support recommendation systems
    - Similarity metrics can be developed to find artists with comparable sound signatures
    - Trend analysis over time can reveal shifts in musical preferences
    """)

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption(f"Data last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption(f"Total artists in dataset: {len(artists):,} | Total songs: {len(songs):,}")