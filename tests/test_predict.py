"""
Tests for the prediction module.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# These imports will now work with conftest.py
from src.config import FEATURE_COLUMNS
from src.model import load_model, load_scaler


@pytest.fixture
def sample_song_features():
    """Sample song features for prediction."""
    return {
        "danceability": 0.8,
        "energy": 0.7,
        "key": 5,
        "loudness": -5.0,
        "mode": 1,
        "speechiness": 0.05,
        "acousticness": 0.2,
        "instrumentalness": 0.01,
        "liveness": 0.1,
        "valence": 0.6,
        "tempo": 120.0,
        "duration_ms": 240000,
        "explicit": 0,
        "year": 2022,
    }


@pytest.fixture
def sample_songs_batch():
    """Batch of songs for testing."""
    return [
        {
            "danceability": 0.8,
            "energy": 0.7,
            "key": 5,
            "loudness": -5.0,
            "mode": 1,
            "speechiness": 0.05,
            "acousticness": 0.2,
            "instrumentalness": 0.01,
            "liveness": 0.1,
            "valence": 0.6,
            "tempo": 120.0,
            "duration_ms": 240000,
            "explicit": 0,
            "year": 2022,
        },
        {
            "danceability": 0.3,
            "energy": 0.9,
            "key": 2,
            "loudness": -2.0,
            "mode": 0,
            "speechiness": 0.3,
            "acousticness": 0.8,
            "instrumentalness": 0.5,
            "liveness": 0.3,
            "valence": 0.2,
            "tempo": 180.0,
            "duration_ms": 180000,
            "explicit": 1,
            "year": 2020,
        }
    ]


def test_single_prediction(sample_song_features):
    """Test prediction for a single song."""
    try:
        model = load_model()
        scaler = load_scaler()
        
        prediction = model.predict(
            scaler.transform(pd.DataFrame([sample_song_features])[FEATURE_COLUMNS])
        )[0]
        
        assert isinstance(prediction, float)
        assert 0 <= prediction <= 100
    except FileNotFoundError:
        pytest.skip("Model file not found - skipping test")


def test_batch_prediction(sample_songs_batch):
    """Test prediction for multiple songs."""
    try:
        model = load_model()
        scaler = load_scaler()
        
        # Convert to DataFrame
        df = pd.DataFrame(sample_songs_batch)
        
        # Prepare features
        X = df[FEATURE_COLUMNS]
        X_scaled = scaler.transform(X)
        
        # Make predictions
        predictions = model.predict(X_scaled)
        
        assert len(predictions) == len(sample_songs_batch)
        assert all(isinstance(p, float) for p in predictions)
        assert all(0 <= p <= 100 for p in predictions)
    except FileNotFoundError:
        pytest.skip("Model file not found - skipping test")