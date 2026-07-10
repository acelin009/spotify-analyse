"""
Tests for the configuration module.
"""

import pytest
from pathlib import Path
import sys

# Add paths
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_path))

from src.config import (
    BASE_DIR,
    DATA_DIR,
    MODEL_DIR,
    REPORT_DIR,
    FIGURE_DIR,
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    TEST_SIZE,
    RANDOM_STATE,
    RF_MODEL_PARAMS,
)


def test_config_paths_exist():
    """Test that all configured paths exist or are created."""
    assert DATA_DIR.exists() or DATA_DIR.parent.exists()
    assert MODEL_DIR.parent.exists() or MODEL_DIR.parent.parent.exists()


def test_config_base_dir():
    """Test that BASE_DIR is correctly set."""
    assert BASE_DIR.name == "spotify-analyse" or BASE_DIR.exists()


def test_config_feature_columns():
    """Test that feature columns are defined."""
    assert len(FEATURE_COLUMNS) > 0
    assert "danceability" in FEATURE_COLUMNS
    assert "energy" in FEATURE_COLUMNS


def test_config_target_column():
    """Test that target column is defined."""
    assert TARGET_COLUMN == "popularity"


def test_config_test_size():
    """Test that test size is within valid range."""
    assert 0 < TEST_SIZE < 1


def test_config_random_state():
    """Test that random state is valid."""
    assert isinstance(RANDOM_STATE, int)
    assert RANDOM_STATE >= 0


def test_config_rf_params():
    """Test that RF model parameters are valid."""
    assert "n_estimators" in RF_MODEL_PARAMS
    assert "random_state" in RF_MODEL_PARAMS
    assert RF_MODEL_PARAMS["random_state"] == RANDOM_STATE