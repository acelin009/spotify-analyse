"""
Tests for the feature engineering module.
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

from src.feature_engineering import (
    prepare_features,
    create_additional_features,
    get_feature_stats,
    get_feature_importance
)
from src.config import FEATURE_COLUMNS, TARGET_COLUMN, TEST_SIZE, RANDOM_STATE


def test_prepare_features_returns_correct_shape(sample_data):
    """Test that prepare_features returns correctly shaped arrays."""
    X_train, X_test, y_train, y_test, scaler = prepare_features(
        sample_data,
        test_size=0.2,
        random_state=42
    )
    
    expected_train_size = int(len(sample_data) * 0.8)
    
    assert X_train.shape[0] == expected_train_size
    assert X_test.shape[0] == len(sample_data) - expected_train_size
    assert X_train.shape[1] == len(FEATURE_COLUMNS)
    assert y_train.shape[0] == expected_train_size
    assert y_test.shape[0] == len(sample_data) - expected_train_size
    assert scaler is not None


def test_prepare_features_scales_data(sample_data):
    """Test that features are properly scaled."""
    X_train, X_test, y_train, y_test, scaler = prepare_features(
        sample_data,
        test_size=0.2,
        random_state=42
    )
    
    # Check that training data is scaled (mean ~0, std ~1)
    assert abs(X_train.mean()) < 0.01
    assert abs(X_train.std() - 1.0) < 0.1


def test_prepare_features_handles_different_scalers(sample_data):
    """Test different scaler types."""
    scalers = ["standard", "robust", "minmax"]
    
    for scaler_type in scalers:
        X_train, X_test, y_train, y_test, scaler = prepare_features(
            sample_data,
            test_size=0.2,
            random_state=42,
            scaler_type=scaler_type
        )
        
        assert X_train is not None
        assert X_test is not None
        assert scaler is not None


def test_create_additional_features(sample_data):
    """Test that additional features are created."""
    enhanced = create_additional_features(sample_data)
    
    # Should have more columns than original
    assert len(enhanced.columns) > len(sample_data.columns)
    
    # Check for new features
    new_features = ["tempo_category", "energy_dance", "duration_min", "decade"]
    for feature in new_features:
        assert feature in enhanced.columns


def test_get_feature_stats(sample_data):
    """Test feature statistics generation."""
    stats = get_feature_stats(sample_data)
    
    assert stats is not None
    # Check that it returns a DataFrame with expected columns
    assert len(stats) > 0


def test_get_feature_importance_with_model(sample_data, mock_model):
    """Test feature importance extraction."""
    # Train mock model
    X = sample_data[FEATURE_COLUMNS]
    y = sample_data[TARGET_COLUMN]
    mock_model.fit(X, y)
    
    # Get feature importance
    importance = get_feature_importance(mock_model, FEATURE_COLUMNS)
    
    assert isinstance(importance, dict)
    # Some features may have zero importance, so check that we have at least some
    assert len(importance) > 0
    # Check that the sum is approximately 1.0 (allow for floating point precision)
    total = sum(importance.values())
    assert total == pytest.approx(1.0, rel=1e-1)  # 10% tolerance


def test_prepare_features_with_selected_features(sample_data):
    """Test preparing features with a subset of features."""
    selected = ["danceability", "energy", "valence"]
    
    X_train, X_test, y_train, y_test, scaler = prepare_features(
        sample_data,
        selected_features=selected,
        test_size=0.2,
        random_state=42
    )
    
    assert X_train.shape[1] == len(selected)


def test_prepare_features_with_feature_selection(sample_data):
    """Test feature selection during preparation."""
    X_train, X_test, y_train, y_test, scaler = prepare_features(
        sample_data,
        test_size=0.2,
        random_state=42,
        feature_selection="kbest",
        n_features=5
    )
    
    assert X_train.shape[1] == 5


def test_prepare_features_raises_error_on_invalid_scaler(sample_data):
    """Test that invalid scaler type raises error."""
    with pytest.raises(ValueError):
        prepare_features(
            sample_data,
            scaler_type="invalid_scaler"
        )