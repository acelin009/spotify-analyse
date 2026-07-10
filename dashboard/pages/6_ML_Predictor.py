# dashboard/pages/6_ML_Predictor.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
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
            page_title="ML Predictor • Spotify Music Intelligence",
            page_icon=favicon,
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except:
        st.set_page_config(
            page_title="ML Predictor • Spotify Music Intelligence",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
else:
    st.set_page_config(
        page_title="ML Predictor • Spotify Music Intelligence",
        page_icon="🤖",
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
            color: #D8C8E8 !important;
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
        
        /* KPI Cards - Dark for purple theme */
        div.kpi-card {
            background: rgba(25, 20, 30, 0.92) !important;
            border-radius: 18px !important;
            padding: 20px 24px !important;
            border: 1px solid rgba(255, 255, 255, 0.04) !important;
            transition: all 0.25s ease !important;
        }
        
        div.kpi-card:hover {
            border-color: #9B6DFF !important;
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
            color: #9B6DFF !important;
            font-weight: 500 !important;
        }
        
        /* Chart container - Dark for purple theme */
        div.chart-card {
            background: rgba(25, 20, 30, 0.92) !important;
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
            background: rgba(25, 20, 30, 0.92) !important;
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
        
        /* Progress bar styling - Purple theme */
        .stProgress > div > div > div {
            background-color: #9B6DFF !important;
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
            background: #9B6DFF;
        }
        </style>
        """, unsafe_allow_html=True)

load_css()

# -----------------------------
# Page-specific gradient (Deep Purple for ML Predictor)
# -----------------------------

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(
            circle at 50% -15%,
            rgba(146, 96, 255, 0.35),
            transparent 55%
        ),
        linear-gradient(
            180deg,
            #5C2E91 0%,
            #472371 20%,
            #341A57 40%,
            #23133A 60%,
            #181818 82%,
            #121212 100%
        ) !important;
    background-attachment: fixed !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Temporary Model Function
# -----------------------------
def predict_popularity(features):
    """
    Temporary placeholder for popularity prediction.
    Replace with actual model once trained.
    """
    weights = {
        "danceability": 0.20,
        "energy": 0.15,
        "loudness": 0.10,
        "valence": 0.15,
        "tempo": 0.05,
        "acousticness": -0.10,
        "instrumentalness": -0.05,
        "speechiness": 0.05,
        "liveness": 0.05,
        "duration_ms": 0.05,
        "explicit": 0.10
    }
    
    normalized_features = features.copy()
    normalized_features["loudness"] = (features["loudness"] + 60) / 60
    normalized_features["duration_ms"] = features["duration_ms"] / 600000
    
    score = 50
    for feature, weight in weights.items():
        if feature in normalized_features:
            score += normalized_features[feature] * weight * 50
    
    score += np.random.normal(0, 3)
    return max(0, min(100, score))

# -----------------------------
# Helper Functions
# -----------------------------
def create_gauge_chart(value, title="Predicted Popularity"):
    """Create a gauge chart for popularity prediction."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": "/100", "font": {"size": 40, "color": "#FFFFFF"}},
            title={"text": title, "font": {"size": 20, "color": "#FFFFFF"}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "white",
                    "tickfont": {"color": "#B3B3B3"}
                },
                "bar": {"color": "#9B6DFF"},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 2,
                "bordercolor": "#9B6DFF",
                "steps": [
                    {"range": [0, 40], "color": "rgba(155, 109, 255, 0.15)"},
                    {"range": [40, 60], "color": "rgba(155, 109, 255, 0.25)"},
                    {"range": [60, 80], "color": "rgba(155, 109, 255, 0.35)"},
                    {"range": [80, 100], "color": "rgba(155, 109, 255, 0.50)"}
                ],
                "threshold": {
                    "line": {"color": "#FFFFFF", "width": 4},
                    "thickness": 0.75,
                    "value": value
                }
            }
        )
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
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
            <div class="hero-title">ML Popularity Predictor</div>
            <div class="hero-subtitle">Predict Song Success Using Audio Features</div>
            <p style="color:#D8C8E8; font-size:15px; margin-top:12px; font-weight:500;">
                <b>11</b> Audio Features
                &nbsp;&nbsp;•&nbsp;&nbsp;
                <b>AI</b> Prediction
                &nbsp;&nbsp;•&nbsp;&nbsp;
                <b>{len(songs):,}</b> Songs
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
            <div class="hero-title">ML Popularity Predictor</div>
            <div class="hero-subtitle">Predict Song Success Using Audio Features</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# -----------------------------
# Example Song Selector
# -----------------------------

st.markdown('<div class="section-title">Example Song</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

example_songs = get_example_songs()
song_options = ["Custom Input"] + example_songs["display_name"].tolist()

selected_example = st.selectbox(
    "Select a song to load its audio features:",
    options=song_options,
    help="Choose a song to automatically populate the sliders with its features.",
    label_visibility="collapsed"
)
st.caption("Load a song from the dataset")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# -----------------------------
# Input Features
# -----------------------------

st.markdown('<div class="section-title">Audio Features</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    
    danceability = st.slider(
        "Danceability",
        0.0, 1.0,
        st.session_state.slider_values["danceability"],
        0.01,
        help="How suitable a track is for dancing (0-1)"
    )
    st.session_state.slider_values["danceability"] = danceability
    
    energy = st.slider(
        "Energy",
        0.0, 1.0,
        st.session_state.slider_values["energy"],
        0.01,
        help="Perceptual measure of intensity and activity (0-1)"
    )
    st.session_state.slider_values["energy"] = energy
    
    loudness = st.slider(
        "Loudness",
        -60.0, 0.0,
        st.session_state.slider_values["loudness"],
        0.1,
        help="Overall loudness in decibels (dB)"
    )
    st.session_state.slider_values["loudness"] = loudness
    
    speechiness = st.slider(
        "Speechiness",
        0.0, 1.0,
        st.session_state.slider_values["speechiness"],
        0.01,
        help="Presence of spoken words in the track (0-1)"
    )
    st.session_state.slider_values["speechiness"] = speechiness
    
    acousticness = st.slider(
        "Acousticness",
        0.0, 1.0,
        st.session_state.slider_values["acousticness"],
        0.01,
        help="Confidence measure of whether the track is acoustic (0-1)"
    )
    st.session_state.slider_values["acousticness"] = acousticness
    
    instrumentalness = st.slider(
        "Instrumentalness",
        0.0, 1.0,
        st.session_state.slider_values["instrumentalness"],
        0.01,
        help="Predicts whether a track contains no vocals (0-1)"
    )
    st.session_state.slider_values["instrumentalness"] = instrumentalness
    
    liveness = st.slider(
        "Liveness",
        0.0, 1.0,
        st.session_state.slider_values["liveness"],
        0.01,
        help="Detects the presence of an audience in the recording (0-1)"
    )
    st.session_state.slider_values["liveness"] = liveness
    
    valence = st.slider(
        "Valence",
        0.0, 1.0,
        st.session_state.slider_values["valence"],
        0.01,
        help="Musical positiveness conveyed by a track (0-1)"
    )
    st.session_state.slider_values["valence"] = valence
    
    tempo = st.slider(
        "Tempo (BPM)",
        0.0, 250.0,
        st.session_state.slider_values["tempo"],
        0.5,
        help="Overall estimated tempo in beats per minute (BPM)"
    )
    st.session_state.slider_values["tempo"] = tempo
    
    duration_ms = st.slider(
        "Duration (seconds)",
        30000, 600000,
        int(st.session_state.slider_values["duration_ms"]),
        1000,
        help="Duration of the track in milliseconds"
    )
    st.session_state.slider_values["duration_ms"] = duration_ms
    
    explicit = st.selectbox(
        "Explicit Content",
        [0, 1],
        index=st.session_state.slider_values["explicit"],
        format_func=lambda x: "No" if x == 0 else "Yes",
        help="Whether the track has explicit lyrics"
    )
    st.session_state.slider_values["explicit"] = explicit
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Predict button
    predict_button = st.button("Predict Popularity", use_container_width=True)

# Right column: Prediction results
with right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    
    if predict_button:
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
        
        try:
            prediction = predict_popularity(features)
            
            # Display KPI card
            label, color = get_prediction_label(prediction)
            st.markdown(f"""
            <div class="kpi-card" style="text-align:center;">
                <div class="kpi-label">Predicted Popularity</div>
                <div class="kpi-value">{prediction:.1f}</div>
                <div class="kpi-delta">{label}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display gauge chart
            fig = create_gauge_chart(prediction)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            
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
        st.markdown("""
        <div style="text-align:center; padding:40px 0; color:#B3B3B3;">
            <div style="font-size:48px; margin-bottom:16px;"></div>
            <div style="font-size:18px; font-weight:500;">Adjust the sliders</div>
            <div style="font-size:14px;">and click 'Predict Popularity' to see the result</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# -----------------------------
# Feature Summary
# -----------------------------

st.markdown('<div class="section-title">Song Profile Summary</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)

# Display feature summary in a grid
col_summary1, col_summary2, col_summary3 = st.columns(3)

def get_feature_level(value, max_val=1.0):
    normalized = value / max_val
    if normalized >= 0.7:
        return "High", normalized
    elif normalized >= 0.4:
        return "Medium", normalized
    else:
        return "Low", normalized

with col_summary1:
    level, val = get_feature_level(danceability)
    st.write(f"**Danceability:** {level}")
    st.progress(val, text=f"{danceability:.2f}")
    
    level, val = get_feature_level(energy)
    st.write(f"**Energy:** {level}")
    st.progress(val, text=f"{energy:.2f}")
    
    loudness_normalized = 1 - (abs(loudness) / 60)
    st.write(f"**Loudness:** {get_feature_level(loudness_normalized)[0]}")
    st.progress(loudness_normalized, text=f"{loudness:.1f} dB")

with col_summary2:
    level, val = get_feature_level(speechiness)
    st.write(f"**Speechiness:** {level}")
    st.progress(val, text=f"{speechiness:.2f}")
    
    level, val = get_feature_level(acousticness)
    st.write(f"**Acousticness:** {level}")
    st.progress(val, text=f"{acousticness:.2f}")
    
    level, val = get_feature_level(instrumentalness)
    st.write(f"**Instrumentalness:** {level}")
    st.progress(val, text=f"{instrumentalness:.3f}")

with col_summary3:
    level, val = get_feature_level(liveness)
    st.write(f"**Liveness:** {level}")
    st.progress(val, text=f"{liveness:.2f}")
    
    level, val = get_feature_level(valence)
    st.write(f"**Valence:** {level}")
    st.progress(val, text=f"{valence:.2f}")
    
    if tempo >= 140:
        tempo_level = "Fast"
        tempo_val = 0.8
    elif tempo >= 100:
        tempo_level = "Medium"
        tempo_val = 0.5
    else:
        tempo_level = "Slow"
        tempo_val = 0.3
    st.write(f"**Tempo:** {tempo_level}")
    st.progress(tempo_val, text=f"{tempo:.1f} BPM")

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
        <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-bottom:12px;">How This Tool Helps</div>
        <div style="color:#B3B3B3; font-size:14px; line-height:1.8;">
        • <b>A&R Teams</b>: Evaluate potential hits before signing artists<br>
        • <b>Music Producers</b>: Optimize song features for better performance<br>
        • <b>Playlist Curators</b>: Identify tracks that will resonate with audiences<br>
        • <b>Marketing Teams</b>: Prioritize songs with higher predicted popularity
        </div>
        <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-top:16px; margin-bottom:12px;">Key Factors</div>
        <div style="color:#B3B3B3; font-size:14px; line-height:1.8;">
        • Danceability and energy are strong predictors of popularity<br>
        • Valence (positivity) can significantly impact listener engagement<br>
        • Acousticness and instrumentalness may limit mainstream appeal
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_insight2:
    st.markdown("""
    <div class="table-card">
        <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-bottom:12px;">Recommendations by Prediction</div>
        <div style="color:#B3B3B3; font-size:14px; line-height:1.8;">
        • <b>80-100</b>: Strong hit potential - major promotional investment<br>
        • <b>60-80</b>: Above average - good for playlist placement<br>
        • <b>40-60</b>: Average - consider feature adjustments<br>
        • <b>0-40</b>: Low potential - review production decisions
        </div>
        <div style="color:#FFFFFF; font-weight:600; font-size:18px; margin-top:16px; margin-bottom:12px;">Future Enhancements</div>
        <div style="color:#B3B3B3; font-size:14px; line-height:1.8;">
        • Genre-specific models for more accurate predictions<br>
        • Time-of-release optimization recommendations<br>
        • Competitive analysis against similar artists<br>
        • Historical trend integration for better accuracy
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
st.caption(f"Updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}  •  {len(songs):,} Songs  •  AI Popularity Predictor")