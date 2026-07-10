from pathlib import Path
import pandas as pd
import streamlit as st
import numpy as np

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data folder
DATA_DIR = BASE_DIR / "data" / "raw"


def create_sample_data():
    """Create sample data for testing when files are missing."""
    np.random.seed(42)
    
    # Sample songs (50 rows for testing)
    n_samples = 50
    songs = pd.DataFrame({
        'name': [f'Song_{i}' for i in range(n_samples)],
        'artists': [f'Artist_{np.random.randint(1, 10)}' for i in range(n_samples)],
        'popularity': np.random.randint(0, 100, n_samples),
        'year': np.random.randint(2000, 2020, n_samples),
        'danceability': np.random.random(n_samples),
        'energy': np.random.random(n_samples),
        'valence': np.random.random(n_samples),
        'acousticness': np.random.random(n_samples),
        'instrumentalness': np.random.random(n_samples),
        'liveness': np.random.random(n_samples),
        'speechiness': np.random.random(n_samples),
        'tempo': np.random.randint(60, 200, n_samples),
        'duration_ms': np.random.randint(120000, 300000, n_samples),
        'track_genre': np.random.choice(['Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Electronic', 'R&B', 'Country'], n_samples),
    })
    
    # Sample artists
    artists = pd.DataFrame({
        'artists': [f'Artist_{i}' for i in range(1, 11)],
        'popularity': np.random.randint(0, 100, 10),
    })
    
    # Sample genres
    genres = pd.DataFrame({
        'genres': ['Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Electronic', 'R&B', 
                   'Country', 'Classical', 'Metal', 'Folk', 'Blues', 'Reggae'],
        'popularity': np.random.randint(0, 100, 12),
        'count': np.random.randint(100, 1000, 12),
    })
    
    years = pd.DataFrame({
        'year': range(2000, 2020),
        'popularity': np.random.randint(0, 100, 20),
        'count': np.random.randint(100, 5000, 20),
    })
    
    songs_with_genres = songs.copy()
    
    return songs, artists, genres, years, songs_with_genres


@st.cache_data
def load_data():
    """
    Load all Spotify datasets with fallback to sample data.
    
    Returns
    -------
    tuple
        (
            songs,
            artists,
            genres,
            years,
            songs_with_genres
        )
    """
    try:
        # Check if data directory exists
        if not DATA_DIR.exists():
            st.warning(f"Data directory not found at {DATA_DIR}. Using sample data.")
            return create_sample_data()
        
        # Check each file
        files = ["data.csv", "data_by_artist.csv", "data_by_genres.csv", 
                 "data_by_year.csv", "data_w_genres.csv"]
        
        missing_files = []
        for file in files:
            if not (DATA_DIR / file).exists():
                missing_files.append(file)
        
        if missing_files:
            st.warning(f"Missing files: {missing_files}. Using sample data.")
            return create_sample_data()
        
        # Load with limits to prevent memory issues on Streamlit Cloud
        songs = pd.read_csv(DATA_DIR / "data.csv", nrows=50000)
        artists = pd.read_csv(DATA_DIR / "data_by_artist.csv")
        genres = pd.read_csv(DATA_DIR / "data_by_genres.csv")
        years = pd.read_csv(DATA_DIR / "data_by_year.csv")
        songs_with_genres = pd.read_csv(DATA_DIR / "data_w_genres.csv", nrows=50000)
        
        return songs, artists, genres, years, songs_with_genres
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return create_sample_data()