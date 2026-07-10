from pathlib import Path

# ==========================
# Project Paths
# ==========================

# Base directory (project root)
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Model directory
MODEL_DIR = BASE_DIR / "models"
SCALER_DIR = BASE_DIR / "models" / "scalers"

# Reports and figures
REPORT_DIR = BASE_DIR / "reports"
FIGURE_DIR = REPORT_DIR / "figures"

# Ensure directories exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, 
                  MODEL_DIR, SCALER_DIR, REPORT_DIR, FIGURE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ==========================
# Data Settings
# ==========================

# Raw data file names
RAW_DATA_FILE = "data.csv"

# ==========================
# Machine Learning Settings
# ==========================

TARGET_COLUMN = "popularity"

TEST_SIZE = 0.20
RANDOM_STATE = 42

# Model hyperparameters (for Random Forest)
RF_MODEL_PARAMS = {
    "n_estimators": 300,  # From tuning results
    "max_depth": 20,      # From tuning results
    "min_samples_split": 2,
    "min_samples_leaf": 1,
    "max_features": "sqrt",
    "random_state": RANDOM_STATE,
    "n_jobs": -1,
}

# ==========================
# Feature Columns
# ==========================

FEATURE_COLUMNS = [
    "danceability",
    "energy",
    "key",
    "loudness",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "duration_ms",
    "explicit",
    "year"
]

# ==========================
# Evaluation Settings
# ==========================

# Metrics to compute
EVALUATION_METRICS = ["r2", "mae", "mse", "rmse", "mape"]

# Plot settings
PLOT_STYLE = "seaborn-v0_8-darkgrid"
PLOT_SIZE = (10, 6)
PLOT_DPI = 300

# ==========================
# Logging Settings
# ==========================

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"