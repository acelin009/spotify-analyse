"""
Feature engineering module for preparing data for machine learning.

Handles:
- Feature selection
- Train-test splitting
- Feature scaling
- Feature creation (optional)
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional, List, Dict
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression

from config import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    TEST_SIZE,
    RANDOM_STATE,
)


def prepare_features(
    df: pd.DataFrame,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
    scaler_type: str = "standard",
    selected_features: Optional[List[str]] = None,
    feature_selection: Optional[str] = None,
    n_features: Optional[int] = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, object]:
    """
    Prepare features for machine learning.
    
    This function:
    1. Selects features (all or specified)
    2. Splits data into train and test sets
    3. Scales features using the specified scaler
    4. Optionally performs feature selection
    
    Parameters
    ----------
    df : pd.DataFrame
        Processed dataset
    test_size : float, default=0.20
        Proportion of data to use for testing
    random_state : int, default=42
        Random seed for reproducibility
    scaler_type : str, default="standard"
        Type of scaler to use: "standard", "robust", "minmax"
    selected_features : List[str], optional
        List of feature names to use. If None, uses all from config.
    feature_selection : str, optional
        Method for feature selection: "kbest", "mutual_info"
    n_features : int, optional
        Number of features to select. Only used if feature_selection is specified.
    
    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, object]
        X_train_scaled, X_test_scaled, y_train, y_test, scaler
        
    Examples
    --------
    >>> df = pd.read_csv("processed_spotify_data.csv")
    >>> X_train, X_test, y_train, y_test, scaler = prepare_features(df)
    >>> model = RandomForestRegressor()
    >>> model.fit(X_train, y_train)
    """
    
    # ==========================
    # 1. Select Features
    # ==========================
    
    # Use specified features or default from config
    if selected_features is None:
        features = FEATURE_COLUMNS
    else:
        features = selected_features
    
    # Ensure all features exist in the dataframe
    available_features = [f for f in features if f in df.columns]
    missing_features = set(features) - set(available_features)
    
    if missing_features:
        print(f"Warning: Missing features: {missing_features}")
        print(f"Using available features: {available_features}")
    
    # Separate features and target
    X = df[available_features].copy()
    y = df[TARGET_COLUMN].copy()
    
    print(f"Feature matrix shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    
    # ==========================
    # 2. Train-Test Split
    # ==========================
    
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        shuffle=True,
        stratify=None,  # For regression, no stratification
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # ==========================
    # 3. Feature Selection (Optional)
    # ==========================
    
    if feature_selection is not None:
        if n_features is None:
            n_features = min(len(available_features), 10)  # Default to 10 features
        
        print(f"Performing feature selection using {feature_selection}...")
        
        if feature_selection == "kbest":
            selector = SelectKBest(score_func=f_regression, k=n_features)
            selector.fit(X_train, y_train)
            
            # Get selected feature indices
            selected_indices = selector.get_support(indices=True)
            
            # Transform data
            X_train = selector.transform(X_train)
            X_test = selector.transform(X_test)
            
            # Get selected feature names
            selected_feature_names = [available_features[i] for i in selected_indices]
            print(f"Selected {len(selected_feature_names)} features: {selected_feature_names}")
            
        elif feature_selection == "mutual_info":
            selector = SelectKBest(score_func=mutual_info_regression, k=n_features)
            selector.fit(X_train, y_train)
            
            selected_indices = selector.get_support(indices=True)
            X_train = selector.transform(X_train)
            X_test = selector.transform(X_test)
            
            selected_feature_names = [available_features[i] for i in selected_indices]
            print(f"Selected {len(selected_feature_names)} features: {selected_feature_names}")
        else:
            print(f"Warning: Unknown feature selection method: {feature_selection}")
    
    # ==========================
    # 4. Feature Scaling
    # ==========================
    
    if scaler_type == "standard":
        scaler = StandardScaler()
    elif scaler_type == "robust":
        scaler = RobustScaler()
    elif scaler_type == "minmax":
        scaler = MinMaxScaler()
    else:
        raise ValueError(f"Unknown scaler type: {scaler_type}. Choose from 'standard', 'robust', or 'minmax'.")
    
    # Fit scaler on training data only
    
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"Scaled feature shapes: {X_train_scaled.shape}, {X_test_scaled.shape}")
    print(f"Scaler used: {type(scaler).__name__}")
    
    return (
        X_train_scaled,
        X_test_scaled,
        y_train,
        y_test,
        scaler,
    )


def create_additional_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create additional features from existing data.
    
    This function adds domain-specific features that might improve model performance.
    
    Parameters
    ----------
    df : pd.DataFrame
        Processed dataset
        
    Returns
    -------
    pd.DataFrame
        Dataset with additional features
        
    Examples
    --------
    >>> df = preprocess(raw_df)
    >>> df_enhanced = create_additional_features(df)
    """
    
    data = df.copy()
    
    # ==========================
    # 1. Tempo Categories
    # ==========================
    
    if "tempo" in data.columns:
        # Categorize tempo
        data["tempo_category"] = pd.cut(
            data["tempo"],
            bins=[0, 80, 120, 160, 300],
            labels=["Slow", "Medium", "Fast", "Very Fast"]
        )
        
        # Binary indicators for tempo ranges
        data["is_slow_tempo"] = (data["tempo"] < 80).astype(int)
        data["is_medium_tempo"] = ((data["tempo"] >= 80) & (data["tempo"] < 120)).astype(int)
        data["is_fast_tempo"] = ((data["tempo"] >= 120) & (data["tempo"] < 160)).astype(int)
        data["is_very_fast_tempo"] = (data["tempo"] >= 160).astype(int)
    
    # ==========================
    # 2. Energy-Danceability Interaction
    # ==========================
    
    if "energy" in data.columns and "danceability" in data.columns:
        data["energy_dance"] = data["energy"] * data["danceability"]
        data["energy_dance_ratio"] = data["energy"] / (data["danceability"] + 0.001)
    
    # ==========================
    # 3. Acousticness-Energy Relationship
    # ==========================
    
    if "acousticness" in data.columns and "energy" in data.columns:
        data["acoustic_energy_ratio"] = data["acousticness"] / (data["energy"] + 0.001)
        data["is_acoustic_high_energy"] = ((data["acousticness"] > 0.5) & (data["energy"] > 0.5)).astype(int)
    
    # ==========================
    # 4. Speechiness Categories
    # ==========================
    
    if "speechiness" in data.columns:
        # Categorize speechiness
        data["speechiness_category"] = pd.cut(
            data["speechiness"],
            bins=[0, 0.33, 0.66, 1],
            labels=["Music", "Mixed", "Spoken"]
        )
        data["is_spoken_word"] = (data["speechiness"] > 0.66).astype(int)
    
    # ==========================
    # 5. Liveness Categories
    # ==========================
    
    if "liveness" in data.columns:
        data["is_live_recording"] = (data["liveness"] > 0.8).astype(int)
    
    # ==========================
    # 6. Valence Categories
    # ==========================
    
    if "valence" in data.columns:
        data["mood_category"] = pd.cut(
            data["valence"],
            bins=[0, 0.33, 0.66, 1],
            labels=["Sad", "Neutral", "Happy"]
        )
        data["is_sad"] = (data["valence"] < 0.33).astype(int)
        data["is_happy"] = (data["valence"] > 0.66).astype(int)
    
    # ==========================
    # 7. Duration Categories
    # ==========================
    
    if "duration_ms" in data.columns:
        # Convert to minutes
        data["duration_min"] = data["duration_ms"] / 60000
        
        # Categorize duration
        data["duration_category"] = pd.cut(
            data["duration_min"],
            bins=[0, 2, 3, 4, 5, 10],
            labels=["Short", "Short-medium", "Medium", "Medium-long", "Long"]
        )
        data["is_short_song"] = (data["duration_min"] < 3).astype(int)
        data["is_long_song"] = (data["duration_min"] > 5).astype(int)
    
    # ==========================
    # 8. Year Categories
    # ==========================
    
    if "year" in data.columns:
        # Decade categories
        data["decade"] = (data["year"] // 10) * 10
        data["is_recent"] = (data["year"] >= 2010).astype(int)
    
    # ==========================
    # 9. Interaction Features
    # ==========================
    
    if "explicit" in data.columns:
        data["explicit_numeric"] = data["explicit"].astype(int)
    
    # ==========================
    # 10. Genre Indicators (if available)
    # ==========================
    
    # If you have genre data, you could create genre indicators here
    
    print(f"Created {len(data.columns) - len(df.columns)} additional features")
    print(f"New features: {[col for col in data.columns if col not in df.columns]}")
    
    return data


def get_feature_importance(
    model,
    feature_names: List[str],
    n_top_features: int = 10
) -> Dict[str, float]:
    """
    Extract and sort feature importances from a trained model.
    
    Parameters
    ----------
    model : object
        Trained model with feature_importances_ attribute
    feature_names : List[str]
        List of feature names
    n_top_features : int, default=10
        Number of top features to return
        
    Returns
    -------
    Dict[str, float]
        Dictionary mapping feature names to their importance scores
    """
    
    if not hasattr(model, 'feature_importances_'):
        return {}
    
    importances = model.feature_importances_
    feature_importance_dict = dict(zip(feature_names, importances))
    
    # Sort by importance in descending order
    sorted_importances = dict(
        sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)[:n_top_features]
    )
    
    return sorted_importances


# ==========================
# Utility Functions
# ==========================

def get_feature_stats(df: pd.DataFrame, features: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Get statistical summary for features.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataset
    features : List[str], optional
        List of feature names. If None, uses all numeric features.
        
    Returns
    -------
    pd.DataFrame
        Statistical summary of features
    """
    
    if features is None:
        features = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Remove target if present
    if TARGET_COLUMN in features:
        features.remove(TARGET_COLUMN)
    
    stats = df[features].describe().T
    stats["missing"] = df[features].isnull().sum()
    stats["skew"] = df[features].skew()
    stats["kurtosis"] = df[features].kurtosis()
    
    return stats


def print_feature_summary(X_train_scaled: np.ndarray, feature_names: List[str]):
    """
    Print a summary of the scaled features.
    
    Parameters
    ----------
    X_train_scaled : np.ndarray
        Scaled feature matrix
    feature_names : List[str]
        List of feature names
    """
    
    summary_df = pd.DataFrame(X_train_scaled, columns=feature_names)
    
    print("\n" + "="*60)
    print("FEATURE SUMMARY (Training Set)")
    print("="*60)
    print("\nShape:", X_train_scaled.shape)
    print("\nDescriptive Statistics:")
    print(summary_df.describe().round(3))
    print("\nMissing Values:", summary_df.isnull().sum().sum())
    print("="*60)