from pathlib import Path
import pandas as pd
import streamlit as st
import time
from typing import Dict, Tuple, Optional

# -----------------------------
# Constants
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
PARQUET_DIR = BASE_DIR / "data" / "parquet"

# File mapping
FILES = {
    "songs": "data.csv",
    "artists": "data_by_artist.csv",
    "genres": "data_by_genres.csv",
    "years": "data_by_year.csv",
    "songs_with_genres": "data_w_genres.csv",
}

# Column dtypes for memory optimization
DTYPES = {
    "explicit": "int8",
    "mode": "int8",
    "key": "int8",
    "popularity": "int16",
    "year": "int16",
    "duration_ms": "int32",
    "danceability": "float32",
    "energy": "float32",
    "valence": "float32",
    "acousticness": "float32",
    "instrumentalness": "float32",
    "liveness": "float32",
    "speechiness": "float32",
    "tempo": "float32",
    "loudness": "float32",
}

# Columns needed by each page to avoid loading everything
PAGE_COLUMNS = {
    "home": ["name", "artists", "popularity", "year", "track_genre"],
    "overview": ["popularity", "danceability", "energy", "valence", 
                 "acousticness", "instrumentalness", "liveness", 
                 "speechiness", "tempo", "year", "duration_ms"],
    "artists": ["artists", "popularity"],
    "genres": ["genres", "popularity", "count"],
    "trends": ["year", "popularity", "count"],
    "ml": ["popularity", "danceability", "energy", "valence", 
           "acousticness", "instrumentalness", "liveness", 
           "speechiness", "tempo", "duration_ms", "explicit", "mode", "key"],
}


# -----------------------------
# Helper Functions
# -----------------------------

def check_data_files() -> Tuple[bool, list]:
    """Check if all required data files exist."""
    required_files = list(FILES.values())
    missing = [f for f in required_files if not (DATA_DIR / f).exists()]
    return len(missing) == 0, missing


def convert_to_parquet():
    """Convert CSV files to Parquet for faster loading."""
    if not DATA_DIR.exists():
        return
    
    PARQUET_DIR.mkdir(parents=True, exist_ok=True)
    
    for name, filename in FILES.items():
        csv_path = DATA_DIR / filename
        parquet_path = PARQUET_DIR / f"{name}.parquet"
        
        if csv_path.exists() and not parquet_path.exists():
            df = pd.read_csv(csv_path)
            df.to_parquet(parquet_path, index=False)


def optimize_memory(df: pd.DataFrame) -> pd.DataFrame:
    """Optimize DataFrame memory usage by converting dtypes."""
    for col in df.columns:
        if col in DTYPES:
            try:
                df[col] = df[col].astype(DTYPES[col])
            except (ValueError, TypeError):
                pass
        elif df[col].dtype == "object":
            # Convert string columns to category if few unique values
            if df[col].nunique() / len(df) < 0.5:
                df[col] = df[col].astype("category")
    return df


def show_error_message(missing_files: list):
    """Display a professional error message when data is missing."""
    st.error("""
    ## ⚠️ Unable to Load Spotify Dataset
    
    The required data files were not found in the expected location.
    
    **Expected files:**
    """)
    
    for file in FILES.values():
        if file in missing_files:
            st.markdown(f"❌ `{file}` (missing)")
        else:
            st.markdown(f"✅ `{file}`")
    
    st.markdown("""
    ---
    **Please ensure:**
    1. The data files are in the `data/raw/` directory
    2. The files have the correct names
    3. You have read permissions for the files
    
    If you're the developer, check that the dataset has been properly downloaded.
    """)


# -----------------------------
# Individual Loaders (Lazy Loading)
# -----------------------------

@st.cache_data(show_spinner=False)
def load_songs(columns: Optional[list] = None, nrows: Optional[int] = None) -> pd.DataFrame:
    """
    Load songs dataset.
    
    Parameters
    ----------
    columns : list, optional
        Specific columns to load
    nrows : int, optional
        Number of rows to load (None = all)
    
    Returns
    -------
    pd.DataFrame
        Songs dataset
    """
    start = time.time()
    
    try:
        # Try Parquet first (faster)
        parquet_path = PARQUET_DIR / "songs.parquet"
        if parquet_path.exists():
            df = pd.read_parquet(parquet_path, columns=columns)
            if nrows:
                df = df.head(nrows)
            st.session_state['load_time'] = time.time() - start
            return df
        
        # Fallback to CSV
        csv_path = DATA_DIR / FILES["songs"]
        if not csv_path.exists():
            return pd.DataFrame()
        
        # Load only needed columns to save memory
        usecols = columns if columns else None
        df = pd.read_csv(csv_path, usecols=usecols, nrows=nrows)
        
        # Optimize memory
        df = optimize_memory(df)
        
        st.session_state['load_time'] = time.time() - start
        return df
        
    except Exception as e:
        st.error(f"Error loading songs: {e}")
        return pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_artists() -> pd.DataFrame:
    """Load artists dataset."""
    try:
        parquet_path = PARQUET_DIR / "artists.parquet"
        if parquet_path.exists():
            return pd.read_parquet(parquet_path)
        
        csv_path = DATA_DIR / FILES["artists"]
        if not csv_path.exists():
            return pd.DataFrame()
        
        df = pd.read_csv(csv_path)
        df = optimize_memory(df)
        return df
        
    except Exception as e:
        st.error(f"Error loading artists: {e}")
        return pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_genres() -> pd.DataFrame:
    """Load genres dataset."""
    try:
        parquet_path = PARQUET_DIR / "genres.parquet"
        if parquet_path.exists():
            return pd.read_parquet(parquet_path)
        
        csv_path = DATA_DIR / FILES["genres"]
        if not csv_path.exists():
            return pd.DataFrame()
        
        df = pd.read_csv(csv_path)
        df = optimize_memory(df)
        return df
        
    except Exception as e:
        st.error(f"Error loading genres: {e}")
        return pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_years() -> pd.DataFrame:
    """Load years dataset."""
    try:
        parquet_path = PARQUET_DIR / "years.parquet"
        if parquet_path.exists():
            return pd.read_parquet(parquet_path)
        
        csv_path = DATA_DIR / FILES["years"]
        if not csv_path.exists():
            return pd.DataFrame()
        
        df = pd.read_csv(csv_path)
        df = optimize_memory(df)
        return df
        
    except Exception as e:
        st.error(f"Error loading years: {e}")
        return pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_songs_with_genres(columns: Optional[list] = None, nrows: Optional[int] = None) -> pd.DataFrame:
    """Load songs with genres dataset."""
    try:
        parquet_path = PARQUET_DIR / "songs_with_genres.parquet"
        if parquet_path.exists():
            df = pd.read_parquet(parquet_path, columns=columns)
            if nrows:
                df = df.head(nrows)
            return df
        
        csv_path = DATA_DIR / FILES["songs_with_genres"]
        if not csv_path.exists():
            return pd.DataFrame()
        
        usecols = columns if columns else None
        df = pd.read_csv(csv_path, usecols=usecols, nrows=nrows)
        df = optimize_memory(df)
        return df
        
    except Exception as e:
        st.error(f"Error loading songs with genres: {e}")
        return pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_summary() -> Dict:
    """
    Load dataset summary statistics.
    
    Returns
    -------
    Dict
        Summary statistics about the dataset
    """
    songs = load_songs(columns=["popularity", "year", "artists", "track_genre"])
    
    if songs.empty:
        return {
            "total_songs": 0,
            "unique_artists": 0,
            "unique_genres": 0,
            "year_min": None,
            "year_max": None,
            "avg_popularity": 0,
            "avg_duration": 0,
        }
    
    # Load genres for genre count
    genres_df = load_genres()
    
    return {
        "total_songs": len(songs),
        "unique_artists": songs['artists'].nunique(),
        "unique_genres": len(genres_df) if not genres_df.empty else songs['track_genre'].nunique(),
        "year_min": int(songs['year'].min()) if 'year' in songs.columns else None,
        "year_max": int(songs['year'].max()) if 'year' in songs.columns else None,
        "avg_popularity": float(songs['popularity'].mean()) if 'popularity' in songs.columns else 0,
        "avg_duration": float(songs['duration_ms'].mean() / 60000) if 'duration_ms' in songs.columns else 0,
    }


def get_load_time() -> float:
    """Get the time taken to load data."""
    return st.session_state.get('load_time', 0)


# -----------------------------
# Main Loader (Backward Compatibility)
# -----------------------------

def load_data():
    """
    Legacy loader that returns all datasets.
    
    Note: This is kept for backward compatibility.
    For new code, use individual loaders instead.
    """
    # Convert to Parquet if needed (one-time)
    convert_to_parquet()
    
    # Check if files exist
    all_exist, missing = check_data_files()
    
    if not all_exist:
        show_error_message(missing)
        st.stop()
    
    # Load all datasets
    songs = load_songs()
    artists = load_artists()
    genres = load_genres()
    years = load_years()
    songs_with_genres = load_songs_with_genres()
    
    # Show load time
    if st.sidebar:
        st.sidebar.caption(f"Data loaded in {get_load_time():.2f}s")
    
    return songs, artists, genres, years, songs_with_genres


# -----------------------------
# Page-Specific Loaders (Recommended)
# -----------------------------

def load_for_home():
    """Load only the data needed for the Home page."""
    songs = load_songs(columns=PAGE_COLUMNS["home"])
    summary = load_summary()
    return songs, summary


def load_for_overview():
    """Load only the data needed for the Overview page."""
    songs = load_songs(columns=PAGE_COLUMNS["overview"])
    genres = load_genres()
    return songs, genres


def load_for_artists():
    """Load only the data needed for the Artists page."""
    return load_artists()


def load_for_genres():
    """Load only the data needed for the Genres page."""
    return load_genres()


def load_for_trends():
    """Load only the data needed for the Trends page."""
    return load_years()


def load_for_ml():
    """Load only the data needed for the ML Predictor page."""
    songs = load_songs(columns=PAGE_COLUMNS["ml"])
    return songs