"""
Spotify Analysis Package

A production-ready machine learning pipeline for predicting song popularity.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

# Import main modules for easy access
from . import config
from . import preprocessing
from . import feature_engineering

# Optional: define what gets imported with `from src import *`
__all__ = [
    "config",
    "preprocessing",
    "feature_engineering",
]