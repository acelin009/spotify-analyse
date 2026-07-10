"""
Global pytest configuration and shared fixtures.
"""

import sys
import pytest
import pandas as pd
import numpy as np
from pathlib import Path

# Add src to path for all tests
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Also add project root
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Now we can import from src
from src.config import FEATURE_COLUMNS, TARGET_COLUMN


# ==========================
# Shared Fixtures
# ==========================

@pytest.fixture
def sample_data():
    """Create a small sample dataset for testing."""
    np.random.seed(42)
    n_samples = 100
    
    data = {
        "danceability": np.random.uniform(0, 1, n_samples),
        "energy": np.random.uniform(0, 1, n_samples),
        "key": np.random.randint(0, 11, n_samples),
        "loudness": np.random.uniform(-20, 0, n_samples),
        "mode": np.random.randint(0, 2, n_samples),
        "speechiness": np.random.uniform(0, 0.5, n_samples),
        "acousticness": np.random.uniform(0, 1, n_samples),
        "instrumentalness": np.random.uniform(0, 0.5, n_samples),
        "liveness": np.random.uniform(0, 0.5, n_samples),
        "valence": np.random.uniform(0, 1, n_samples),
        "tempo": np.random.uniform(60, 200, n_samples),
        "duration_ms": np.random.randint(120000, 360000, n_samples),
        "explicit": np.random.randint(0, 2, n_samples),
        "year": np.random.randint(1990, 2024, n_samples),
        TARGET_COLUMN: np.random.randint(0, 100, n_samples),
        "artists": ["Artist A"] * n_samples,
        "name": ["Song X"] * n_samples,
        "id": [f"id_{i}" for i in range(n_samples)],
        "release_date": ["2020-01-01"] * n_samples,
    }
    
    return pd.DataFrame(data)


@pytest.fixture
def sample_data_with_missing():
    """Create sample data with missing values."""
    df = pd.DataFrame({
        "danceability": [0.5, 0.6, None, 0.8],
        "energy": [0.7, None, 0.5, 0.9],
        "popularity": [80, 70, None, 90],
        "artists": ["A", "B", "C", "D"],
        "name": ["X", "Y", "Z", "W"],
        "id": ["1", "2", "3", "4"],
        "release_date": ["2020-01-01"] * 4,
    })
    return df


@pytest.fixture
def sample_duplicate_data():
    """Create sample data with duplicates."""
    df = pd.DataFrame({
        "danceability": [0.5, 0.5, 0.6, 0.6],
        "energy": [0.7, 0.7, 0.8, 0.8],
        "popularity": [80, 80, 70, 70],
        "artists": ["A", "A", "B", "B"],
        "name": ["X", "X", "Y", "Y"],
        "id": ["1", "1", "2", "2"],
        "release_date": ["2020-01-01"] * 4,
    })
    return df


@pytest.fixture
def mock_model():
    """Create a mock model for testing."""
    from sklearn.ensemble import RandomForestRegressor
    model = RandomForestRegressor(n_estimators=2, random_state=42)
    return model


@pytest.fixture
def sample_features():
    """Return the list of feature columns."""
    return FEATURE_COLUMNS


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