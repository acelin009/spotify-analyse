# src/model.py
"""
Model loading and prediction functions.
"""

import joblib
import pandas as pd
import numpy as np
from pathlib import Path

from src.config import MODEL_DIR, FEATURE_COLUMNS


def load_model(model_path=None):
    """
    Load the trained model from disk.
    
    Parameters
    ----------
    model_path : str or Path, optional
        Path to the model file. If None, uses default path.
    
    Returns
    -------
    object
        Loaded model
    """
    if model_path is None:
        model_path = MODEL_DIR / "random_forest_model.pkl"
    
    if not Path(model_path).exists():
        raise FileNotFoundError(f"Model not found at {model_path}")
    
    model = joblib.load(model_path)
    return model


def load_scaler(scaler_path=None):
    """
    Load the trained scaler from disk.
    
    Parameters
    ----------
    scaler_path : str or Path, optional
        Path to the scaler file. If None, uses default path.
    
    Returns
    -------
    object
        Loaded scaler
    """
    if scaler_path is None:
        scaler_path = MODEL_DIR / "scaler.pkl"
    
    if not Path(scaler_path).exists():
        raise FileNotFoundError(f"Scaler not found at {scaler_path}")
    
    scaler = joblib.load(scaler_path)
    return scaler


def predict(model, features, scaler=None):
    """
    Make a prediction using the trained model.
    
    Parameters
    ----------
    model : object
        Trained model
    features : dict or pd.DataFrame
        Input features
    scaler : object, optional
        Trained scaler to transform features
    
    Returns
    -------
    float
        Predicted popularity
    """
    # Convert dict to DataFrame if needed
    if isinstance(features, dict):
        features = pd.DataFrame([features])
    
    # Ensure features are in the correct order
    missing_cols = set(FEATURE_COLUMNS) - set(features.columns)
    if missing_cols:
        raise ValueError(f"Missing features: {missing_cols}")
    
    # Select and order features
    X = features[FEATURE_COLUMNS]
    
    # Scale if scaler is provided
    if scaler is not None:
        X = scaler.transform(X)
    
    # Make prediction
    prediction = model.predict(X)[0]
    
    return float(prediction)