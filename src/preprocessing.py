"""
Data preprocessing module for cleaning the Spotify dataset.

Handles:
- Duplicate removal
- Missing value handling
- Data type conversions
- Outlier detection (optional)
"""

import pandas as pd
import numpy as np
from typing import Optional, List

from config import TARGET_COLUMN


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the Spotify dataset and return a processed DataFrame.
    
    This function handles:
    1. Removing duplicate rows
    2. Removing rows with missing target values
    3. Converting data types (if needed)
    4. Handling outliers (optional)
    5. Additional cleaning based on domain knowledge
    
    Parameters
    ----------
    df : pd.DataFrame
        Raw Spotify dataset
        
    Returns
    -------
    pd.DataFrame
        Cleaned dataset ready for feature engineering
        
    Examples
    --------
    >>> df = pd.read_csv("spotify_tracks.csv")
    >>> clean_df = preprocess(df)
    """
    
    data = df.copy()
    
    print(f"Initial dataset shape: {data.shape}")
    
    # ==========================
    # 1. Remove Duplicate Rows
    # ==========================
    initial_rows = len(data)
    data = data.drop_duplicates()
    duplicates_removed = initial_rows - len(data)
    if duplicates_removed > 0:
        print(f"Removed {duplicates_removed} duplicate rows")
    
    # ==========================
    # 2. Handle Missing Values
    # ==========================
    
    # Remove rows with missing target
    initial_rows = len(data)
    data = data.dropna(subset=[TARGET_COLUMN])
    missing_target_removed = initial_rows - len(data)
    if missing_target_removed > 0:
        print(f"Removed {missing_target_removed} rows with missing target")
    
    # Handle missing values in feature columns
    # Option 1: Remove rows with any missing values (strict)
    initial_rows = len(data)
    data = data.dropna()
    missing_features_removed = initial_rows - len(data)
    if missing_features_removed > 0:
        print(f"Removed {missing_features_removed} rows with missing features")
    
    # Option 2: Impute missing values (uncomment to use)
    # from sklearn.impute import SimpleImputer
    # numeric_cols = data.select_dtypes(include=[np.number]).columns
    # imputer = SimpleImputer(strategy='median')
    # data[numeric_cols] = imputer.fit_transform(data[numeric_cols])
    
    # ==========================
    # 3. Data Type Conversions
    # ==========================
    
    # Ensure numeric columns are properly typed
    numeric_columns = [
        "danceability", "energy", "key", "loudness", "mode",
        "speechiness", "acousticness", "instrumentalness", 
        "liveness", "valence", "tempo", "duration_ms", "popularity"
    ]
    
    for col in numeric_columns:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
    
    # Ensure boolean columns are properly typed
    if "explicit" in data.columns:
        data["explicit"] = data["explicit"].astype(bool)
    
    # ==========================
    # 4. Handle Outliers (Optional)
    # ==========================
    
    # Remove extreme outliers using IQR method
    # Uncomment to enable
    """
    from scipy import stats
    
    def remove_outliers_iqr(data, column, multiplier=1.5):
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        return data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
    
    # Apply to continuous features
    continuous_features = ["danceability", "energy", "loudness", 
                          "speechiness", "acousticness", "valence", "tempo"]
    for col in continuous_features:
        if col in data.columns:
            data = remove_outliers_iqr(data, col)
    """
    
    # ==========================
    # 5. Additional Domain-Specific Cleaning
    # ==========================
    
    # Ensure valid ranges for audio features
    # Features should be between 0 and 1 (except loudness, tempo, etc.)
    audio_features = ["danceability", "energy", "speechiness", 
                     "acousticness", "instrumentalness", "liveness", "valence"]
    
    for col in audio_features:
        if col in data.columns:
            # Clip values to valid range [0, 1]
            data[col] = data[col].clip(0, 1)
    
    # Ensure loudness is in a reasonable range
    if "loudness" in data.columns:
        # Typical range is -60 to 0 dB
        data["loudness"] = data["loudness"].clip(-60, 0)
    
    # Ensure tempo is in a reasonable range
    if "tempo" in data.columns:
        # Most songs are between 60-200 BPM
        data["tempo"] = data["tempo"].clip(20, 300)
    
    # ==========================
    # 6. Reset Index
    # ==========================
    
    data = data.reset_index(drop=True)
    
    print(f"Final dataset shape: {data.shape}")
    print(f"Final dataset columns: {data.columns.tolist()}")
    
    return data


def validate_data(df: pd.DataFrame) -> dict:
    """
    Validate the dataset and return a report of quality metrics.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataset to validate
        
    Returns
    -------
    dict
        Dictionary containing validation metrics
    """
    
    validation_report = {
        "shape": df.shape,
        "missing_values": df.isnull().sum().to_dict(),
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.to_dict(),
        "target_stats": df[TARGET_COLUMN].describe().to_dict() if TARGET_COLUMN in df.columns else {},
    }
    
    return validation_report


def save_processed_data(df: pd.DataFrame, filepath: Optional[str] = None):
    """
    Save the processed dataset to disk.
    
    Parameters
    ----------
    df : pd.DataFrame
        Processed dataset to save
    filepath : str, optional
        Path where to save the file. If not provided, uses config default.
    """
    
    if filepath is None:
        from config import PROCESSED_DATA_DIR, PROCESSED_DATA_FILE
        filepath = PROCESSED_DATA_DIR / PROCESSED_DATA_FILE
    
    df.to_csv(filepath, index=False)
    print(f"Processed data saved to: {filepath}")


# ==========================
# Utility Functions
# ==========================

def get_feature_names(df: pd.DataFrame, exclude_target: bool = True) -> List[str]:
    """
    Get the list of feature column names.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataset
    exclude_target : bool, default=True
        Whether to exclude the target column
        
    Returns
    -------
    List[str]
        List of feature column names
    """
    
    columns = df.columns.tolist()
    
    if exclude_target and TARGET_COLUMN in columns:
        columns.remove(TARGET_COLUMN)
    
    return columns