"""
Tests for the model loading and prediction.
"""

import pytest
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import sys

# Add paths
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_path))

from src.model import load_model, predict, load_scaler
from src.config import FEATURE_COLUMNS, MODEL_DIR


def test_load_model():
    """Test that model loads successfully."""
    try:
        model = load_model()
        assert model is not None
    except FileNotFoundError:
        pytest.skip("Model file not found - skipping test")


def test_load_scaler():
    """Test that scaler loads successfully."""
    try:
        scaler = load_scaler()
        assert scaler is not None
    except FileNotFoundError:
        pytest.skip("Scaler file not found - skipping test")


def test_model_predicts_float():
    """Test that prediction returns a float."""
    try:
        model = load_model()
        scaler = load_scaler()
        
        # Create sample input
        sample = {feature: 0.5 for feature in FEATURE_COLUMNS}
        prediction = predict(model, sample, scaler)
        
        assert isinstance(prediction, float)
    except FileNotFoundError:
        pytest.skip("Model file not found - skipping test")


def test_model_predicts_within_range():
    """Test that predictions are within valid range."""
    try:
        model = load_model()
        scaler = load_scaler()
        
        # Test with various inputs
        for _ in range(10):
            sample = {feature: np.random.uniform(0, 1) for feature in FEATURE_COLUMNS}
            prediction = predict(model, sample, scaler)
            
            # Popularity should be between 0 and 100
            assert 0 <= prediction <= 100
    except FileNotFoundError:
        pytest.skip("Model file not found - skipping test")


def test_model_predicts_consistent():
    """Test that predictions are consistent."""
    try:
        model = load_model()
        scaler = load_scaler()
        
        sample = {feature: 0.5 for feature in FEATURE_COLUMNS}
        
        pred1 = predict(model, sample, scaler)
        pred2 = predict(model, sample, scaler)
        
        # Use approx for floating point comparison
        assert pred1 == pytest.approx(pred2, rel=1e-9)
    except FileNotFoundError:
        pytest.skip("Model file not found - skipping test")