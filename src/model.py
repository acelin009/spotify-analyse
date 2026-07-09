import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "random_forest_model.pkl"

SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

model = joblib.load(MODEL_PATH)

scaler = joblib.load(SCALER_PATH)

FEATURE_COLUMNS = [
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "duration_ms",
    "explicit",
    "year"
]

def predict_popularity(features: dict):
    """
    Predict Spotify song popularity.
    """

    input_df = pd.DataFrame([features])

    input_df = input_df[FEATURE_COLUMNS]

    scaled_input = scaler.transform(input_df)

    prediction = model.predict(scaled_input)

    return float(prediction[0])

