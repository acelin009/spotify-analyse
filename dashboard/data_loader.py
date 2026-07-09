from pathlib import Path

import pandas as pd
import streamlit as st

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data folder
DATA_DIR = BASE_DIR / "data" / "raw"


@st.cache_data
def load_data():
    """
    Load all Spotify datasets.

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

    songs = pd.read_csv(DATA_DIR / "data.csv")

    artists = pd.read_csv(DATA_DIR / "data_by_artist.csv")

    genres = pd.read_csv(DATA_DIR / "data_by_genres.csv")

    years = pd.read_csv(DATA_DIR / "data_by_year.csv")

    songs_with_genres = pd.read_csv(DATA_DIR / "data_w_genres.csv")

    return (
        songs,
        artists,
        genres,
        years,
        songs_with_genres,
    )