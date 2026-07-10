"""
Tests for the preprocessing module.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add paths
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_path))

from src.preprocessing import preprocess, validate_data


def test_preprocess_removes_duplicates(sample_duplicate_data):
    """Test that duplicate rows are removed."""
    cleaned = preprocess(sample_duplicate_data)
    
    # Should have 2 rows instead of 4 (2 unique rows)
    assert len(cleaned) == 2
    assert cleaned.duplicated().sum() == 0


def test_preprocess_handles_missing_target():
    """Test that rows with missing target are removed."""
    # Create data with missing target only
    df = pd.DataFrame({
        "danceability": [0.5, 0.6, 0.7, 0.8],
        "energy": [0.7, 0.8, 0.5, 0.9],
        "popularity": [80, 70, None, 90],
        "artists": ["A", "B", "C", "D"],
        "name": ["X", "Y", "Z", "W"],
        "id": ["1", "2", "3", "4"],
        "release_date": ["2020-01-01"] * 4,
    })
    
    cleaned = preprocess(df)
    
    # Should remove the row with None popularity
    # Original: 4 rows → After cleaning: 3 rows
    assert len(cleaned) == 3
    assert cleaned["popularity"].isnull().sum() == 0


def test_preprocess_removes_rows_with_missing_values(sample_data_with_missing):
    """Test that rows with any missing values are removed."""
    cleaned = preprocess(sample_data_with_missing)
    
    # Original: 4 rows
    # After cleaning: 2 rows (rows 0 and 3 are valid)
    assert len(cleaned) == 2
    assert cleaned.isnull().sum().sum() == 0


def test_preprocess_preserves_required_columns(sample_data):
    """Test that required columns are preserved."""
    cleaned = preprocess(sample_data)
    
    required_cols = ["danceability", "energy", "popularity"]
    for col in required_cols:
        assert col in cleaned.columns


def test_preprocess_handles_empty_dataframe():
    """Test preprocessing an empty dataframe."""
    df = pd.DataFrame(columns=["danceability", "energy", "popularity"])
    
    cleaned = preprocess(df)
    
    assert len(cleaned) == 0
    assert cleaned is not None


def test_preprocess_clips_audio_features(sample_data):
    """Test that audio features are clipped to valid ranges."""
    # Create data with out-of-range values
    df = sample_data.copy()
    df.loc[0, "danceability"] = 1.5
    df.loc[1, "energy"] = -0.5
    
    cleaned = preprocess(df)
    
    # Values should be clipped to [0, 1]
    assert cleaned["danceability"].iloc[0] <= 1.0
    assert cleaned["energy"].iloc[1] >= 0.0


def test_validate_data_returns_metrics(sample_data):
    """Test that validate_data returns expected metrics."""
    cleaned = preprocess(sample_data)
    metrics = validate_data(cleaned)
    
    assert "shape" in metrics
    assert "missing_values" in metrics
    assert "columns" in metrics
    assert "dtypes" in metrics
    assert "target_stats" in metrics


def test_preprocess_data_types(sample_data):
    """Test that data types are correctly converted."""
    cleaned = preprocess(sample_data)
    
    # Check numeric columns
    numeric_cols = ["danceability", "energy", "popularity"]
    for col in numeric_cols:
        assert pd.api.types.is_numeric_dtype(cleaned[col])


def test_preprocess_no_side_effects(sample_data):
    """Test that original dataframe is not modified."""
    original = sample_data.copy()
    original_len = len(original)
    
    cleaned = preprocess(sample_data)
    
    # Original should be unchanged
    assert len(original) == original_len
    assert not original.equals(cleaned)  # Different object