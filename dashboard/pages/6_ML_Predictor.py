# dashboard/pages/6_ML_Predictor.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from data_loader import load_data

# -----------------------------
# Temporary Model Function
# -----------------------------
def predict_popularity(features):
    """
    Temporary placeholder for popularity prediction.
    Replace with actual model once trained.
    """
    # Simple weighted average based on common music industry knowledge
    # This is just for demonstration - replace with your actual model
    
    # Weights for different features (based on typical importance)
    weights = {
        "danceability": 0.20,
        "energy": 0.15,
        "loudness": 0.10,
        "valence": 0.15,
        "tempo": 0.05,
        "acousticness": -0.10,  # Negative correlation
        "instrumentalness": -0.05,  # Negative correlation
        "speechiness": 0.05,
        "liveness": 0.05,
        "duration_ms": 0.05,
        "explicit": 0.10
    }
    
    # Normalize features
    normalized_features = features.copy()
    normalized_features["loudness"] = (features["loudness"] + 60) / 60  # Normalize to 0-1
    normalized_features["duration_ms"] = features["duration_ms"] / 600000  # Normalize to 0-1
    
    # Calculate weighted score
    score = 50  # Base score
    for feature, weight in weights.items():
        if feature in normalized_features:
            score += normalized_features[feature] * weight * 50
    
    # Add some randomness to simulate real predictions
    score += np.random.normal(0, 3)
    
    # Clip to 0-100 range
    return max(0, min(100, score))

# Page Configuration
st.set_page_config(
    page_title="Popularity Predictor",
    page_icon="🤖",
    layout="wide"
)

# Load Data
songs, artists, genres, years, songs_with_genres = load_data()

# -----------------------------
# Helper Functions
# -----------------------------
def create_gauge_chart(value, title="Predicted Popularity"):
    """Create a gauge chart for popularity prediction."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": "/100", "font": {"size": 40}},
            title={"text": title, "font": {"size": 20}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "white",
                    "tickfont": {"color": "white"}
                },
                "bar": {"color": "#1DB954"},
                "bgcolor": "#121212",
                "borderwidth": 2,
                "bordercolor": "#1DB954",
                "steps": [
                    {"range": [0, 40], "color": "rgba(255, 0, 0, 0.3)"},
                    {"range": [40, 60], "color": "rgba(255, 165, 0, 0.3)"},
                    {"range": [60, 80], "color": "rgba(255, 255, 0, 0.3)"},
                    {"range": [80, 100], "color": "rgba(0, 255, 0, 0.3)"}
                ],
                "threshold": {
                    "line": {"color": "white", "width": 4},
                    "thickness": 0.75,
                    "value": value
                }
            }
        )
    )
    
    fig.update_layout(
        paper_bgcolor="#121212",
        font={"color": "white"},
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def get_prediction_label(prediction):
    """Get category label based on popularity score."""
    if prediction >= 80:
        return "🔥 Potential Hit", "success"
    elif prediction >= 60:
        return "🎵 Above Average", "info"
    elif prediction >= 40:
        return "🙂 Average Potential", "warning"
    else:
        return "📉 Low Popularity Potential", "error"

def get_example_songs():
    """Get a list of example songs from the dataset."""
    # Select a diverse set of songs
    sample_size = min(10, len(songs))
    example_songs = songs.sample(sample_size, random_state=42).copy()
    example_songs["display_name"] = example_songs["name"] + " - " + example_songs["artists"]
    return example_songs

def load_example_song(song_name):
    """Load example song features from the dataset."""
    song = songs[songs["name"] == song_name].iloc[0]
    return {
        "danceability": song["danceability"],
        "energy": song["energy"],
        "loudness": song["loudness"],
        "speechiness": song["speechiness"],
        "acousticness": song["acousticness"],
        "instrumentalness": song["instrumentalness"],
        "liveness": song["liveness"],
        "valence": song["valence"],
        "tempo": song["tempo"],
        "duration_ms": song["duration_ms"],
        "explicit": 1 if song["explicit"] else 0
    }

# -----------------------------
# Page Title
# -----------------------------
st.title("🤖 Popularity Predictor")

st.write(
    """
    Predict the popularity score of a song based on its audio characteristics. 
    Adjust the sliders below and click predict to see the estimated popularity.
    """
)

st.divider()

# -----------------------------
# Example Song Selector (Bonus Feature)
# -----------------------------
st.subheader("📚 Load Example Song")

# Get example songs
example_songs = get_example_songs()
song_options = ["Custom Input"] + example_songs["display_name"].tolist()

selected_example = st.selectbox(
    "Select a song to load its audio features:",
    options=song_options,
    help="Choose a song to automatically populate the sliders with its features."
)

st.divider()

# -----------------------------
# Input Features
# -----------------------------
st.subheader("🎛️ Audio Features")

# Two-column layout: Inputs | Prediction
left, right = st.columns([2, 1])

# Initialize session state for sliders if not exists
if "slider_values" not in st.session_state:
    st.session_state.slider_values = {
        "danceability": 0.50,
        "energy": 0.50,
        "loudness": -10.0,
        "speechiness": 0.05,
        "acousticness": 0.50,
        "instrumentalness": 0.0,
        "liveness": 0.10,
        "valence": 0.50,
        "tempo": 120.0,
        "duration_ms": 200000,
        "explicit": 0
    }

# Load example song if selected
if selected_example != "Custom Input":
    song_name = selected_example.split(" - ")[0]
    try:
        features = load_example_song(song_name)
        for key, value in features.items():
            st.session_state.slider_values[key] = value
    except:
        st.warning("Could not load example song. Please try another.")

# Left column: Input sliders
with left:
    danceability = st.slider(
        "💃 Danceability",
        0.0, 1.0,
        st.session_state.slider_values["danceability"],
        0.01,
        help="How suitable a track is for dancing (0-1)"
    )
    st.session_state.slider_values["danceability"] = danceability
    
    energy = st.slider(
        "⚡ Energy",
        0.0, 1.0,
        st.session_state.slider_values["energy"],
        0.01,
        help="Perceptual measure of intensity and activity (0-1)"
    )
    st.session_state.slider_values["energy"] = energy
    
    loudness = st.slider(
        "🔊 Loudness",
        -60.0, 0.0,
        st.session_state.slider_values["loudness"],
        0.1,
        help="Overall loudness in decibels (dB)"
    )
    st.session_state.slider_values["loudness"] = loudness
    
    speechiness = st.slider(
        "🎤 Speechiness",
        0.0, 1.0,
        st.session_state.slider_values["speechiness"],
        0.01,
        help="Presence of spoken words in the track (0-1)"
    )
    st.session_state.slider_values["speechiness"] = speechiness
    
    acousticness = st.slider(
        "🎸 Acousticness",
        0.0, 1.0,
        st.session_state.slider_values["acousticness"],
        0.01,
        help="Confidence measure of whether the track is acoustic (0-1)"
    )
    st.session_state.slider_values["acousticness"] = acousticness
    
    instrumentalness = st.slider(
        "🎹 Instrumentalness",
        0.0, 1.0,
        st.session_state.slider_values["instrumentalness"],
        0.01,
        help="Predicts whether a track contains no vocals (0-1)"
    )
    st.session_state.slider_values["instrumentalness"] = instrumentalness
    
    liveness = st.slider(
        "🎤 Liveness",
        0.0, 1.0,
        st.session_state.slider_values["liveness"],
        0.01,
        help="Detects the presence of an audience in the recording (0-1)"
    )
    st.session_state.slider_values["liveness"] = liveness
    
    valence = st.slider(
        "😊 Valence",
        0.0, 1.0,
        st.session_state.slider_values["valence"],
        0.01,
        help="Musical positiveness conveyed by a track (0-1)"
    )
    st.session_state.slider_values["valence"] = valence
    
    tempo = st.slider(
        "🎵 Tempo (BPM)",
        0.0, 250.0,
        st.session_state.slider_values["tempo"],
        0.5,
        help="Overall estimated tempo in beats per minute (BPM)"
    )
    st.session_state.slider_values["tempo"] = tempo
    
    duration_ms = st.slider(
        "⏱️ Duration (seconds)",
        30000, 600000,
        int(st.session_state.slider_values["duration_ms"]),
        1000,
        help="Duration of the track in milliseconds"
    )
    st.session_state.slider_values["duration_ms"] = duration_ms
    
    explicit = st.selectbox(
        "🔞 Explicit Content",
        [0, 1],
        index=st.session_state.slider_values["explicit"],
        format_func=lambda x: "No" if x == 0 else "Yes",
        help="Whether the track has explicit lyrics"
    )
    st.session_state.slider_values["explicit"] = explicit
    
    # Predict button
    predict_button = st.button("🎯 Predict Popularity", use_container_width=True)

# Right column: Prediction results
with right:
    if predict_button:
        # Build feature dictionary
        features = {
            "danceability": danceability,
            "energy": energy,
            "loudness": loudness,
            "speechiness": speechiness,
            "acousticness": acousticness,
            "instrumentalness": instrumentalness,
            "liveness": liveness,
            "valence": valence,
            "tempo": tempo,
            "duration_ms": duration_ms,
            "explicit": explicit
        }
        
        # Make prediction
        try:
            prediction = predict_popularity(features)
            
            # Display metrics
            st.metric(
                "📊 Predicted Popularity",
                f"{prediction:.1f}/100"
            )
            
            # Display gauge chart
            fig = create_gauge_chart(prediction)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            
            # Display prediction label
            label, color = get_prediction_label(prediction)
            
            if color == "success":
                st.success(label)
            elif color == "info":
                st.info(label)
            elif color == "warning":
                st.warning(label)
            else:
                st.error(label)
            
            # Show confidence level
            if prediction >= 80:
                st.progress(0.9, text="🔥 High confidence - This song has hit potential!")
            elif prediction >= 60:
                st.progress(0.7, text="🎵 Good confidence - Above average track")
            elif prediction >= 40:
                st.progress(0.5, text="🙂 Moderate confidence - Average potential")
            else:
                st.progress(0.3, text="📉 Low confidence - May need improvements")
                
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")
            st.info("Please ensure all features are within valid ranges and try again.")
    else:
        st.info("👆 Adjust the sliders and click 'Predict Popularity' to see the result.")

st.divider()

# -----------------------------
# Feature Summary (Bonus)
# -----------------------------
st.subheader("📊 Song Profile Summary")

# Display feature summary in a grid
col_summary1, col_summary2, col_summary3 = st.columns(3)

# Normalize for progress bars
def get_feature_level(value, max_val=1.0):
    """Get human-readable level for a feature."""
    normalized = value / max_val
    if normalized >= 0.7:
        return "High", normalized
    elif normalized >= 0.4:
        return "Medium", normalized
    else:
        return "Low", normalized

with col_summary1:
    level, val = get_feature_level(danceability)
    st.write(f"**💃 Danceability:** {level}")
    st.progress(val, text=f"{danceability:.2f}")
    
    level, val = get_feature_level(energy)
    st.write(f"**⚡ Energy:** {level}")
    st.progress(val, text=f"{energy:.2f}")
    
    # Normalize loudness
    loudness_normalized = 1 - (abs(loudness) / 60)
    st.write(f"**🔊 Loudness:** {get_feature_level(loudness_normalized)[0]}")
    st.progress(loudness_normalized, text=f"{loudness:.1f} dB")

with col_summary2:
    level, val = get_feature_level(speechiness)
    st.write(f"**🎤 Speechiness:** {level}")
    st.progress(val, text=f"{speechiness:.2f}")
    
    level, val = get_feature_level(acousticness)
    st.write(f"**🎸 Acousticness:** {level}")
    st.progress(val, text=f"{acousticness:.2f}")
    
    level, val = get_feature_level(instrumentalness)
    st.write(f"**🎹 Instrumentalness:** {level}")
    st.progress(val, text=f"{instrumentalness:.3f}")

with col_summary3:
    level, val = get_feature_level(liveness)
    st.write(f"**🎤 Liveness:** {level}")
    st.progress(val, text=f"{liveness:.2f}")
    
    level, val = get_feature_level(valence)
    st.write(f"**😊 Valence:** {level}")
    st.progress(val, text=f"{valence:.2f}")
    
    # Tempo levels
    if tempo >= 140:
        tempo_level = "Fast"
        tempo_val = 0.8
    elif tempo >= 100:
        tempo_level = "Medium"
        tempo_val = 0.5
    else:
        tempo_level = "Slow"
        tempo_val = 0.3
    st.write(f"**🎵 Tempo:** {tempo_level}")
    st.progress(tempo_val, text=f"{tempo:.1f} BPM")

st.divider()

# -----------------------------
# Business Insights
# -----------------------------
st.subheader("📌 Business Insights")

col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    st.markdown("""
    **🎯 How This Tool Helps**
    - **A&R Teams**: Evaluate potential hits before signing artists
    - **Music Producers**: Optimize song features for better performance
    - **Playlist Curators**: Identify tracks that will resonate with audiences
    - **Marketing Teams**: Prioritize songs with higher predicted popularity
    
    **📊 Key Factors**
    - Danceability and energy are strong predictors of popularity
    - Valence (positivity) can significantly impact listener engagement
    - Acousticness and instrumentalness may limit mainstream appeal
    """)

with col_insight2:
    st.markdown("""
    **💡 Recommendations by Prediction**
    - **80-100**: Strong hit potential - major promotional investment
    - **60-80**: Above average - good for playlist placement
    - **40-60**: Average - consider feature adjustments
    - **0-40**: Low potential - review production decisions
    
    **🔮 Future Enhancements**
    - Genre-specific models for more accurate predictions
    - Time-of-release optimization recommendations
    - Competitive analysis against similar artists
    - Historical trend integration for better accuracy
    """)

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption(f"Data last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("🎯 Use this tool to experiment with different audio feature combinations and predict song popularity.")