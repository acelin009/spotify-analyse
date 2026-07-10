"""
Hyperparameter tuning module for the Spotify Popularity Prediction Model.
"""

import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ==========================
# Setup Path
# ==========================

# Get the project root
_current_file = Path(__file__).resolve()
project_root = _current_file.parent.parent
src_path = project_root / "src"

# Add paths
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# ==========================
# Import Project Modules
# ==========================

from config import (
    FEATURE_COLUMNS,
    MODEL_DIR,
    RANDOM_STATE,
    RAW_DATA_DIR,
    REPORT_DIR,
    TARGET_COLUMN,
    TEST_SIZE,
)
from feature_engineering import create_additional_features, prepare_features
from preprocessing import preprocess

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ==========================
# Search Spaces
# ==========================

GRID_SEARCH_SPACE = {
    "n_estimators": [100, 200, 300, 400, 500],
    "max_depth": [10, 15, 20, 30, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "max_features": ["sqrt", "log2", None],
}

RANDOM_SEARCH_SPACE = {
    "n_estimators": [50, 100, 150, 200, 250, 300, 400, 500],
    "max_depth": [5, 10, 15, 20, 25, 30, None],
    "min_samples_split": [2, 3, 4, 5, 7, 10],
    "min_samples_leaf": [1, 2, 3, 4, 5],
    "max_features": ["sqrt", "log2", None, 0.3, 0.5, 0.7],
}

QUICK_SEARCH_SPACE = {
    "n_estimators": [100, 200],
    "max_depth": [10, 20],
    "min_samples_split": [2, 5],
    "min_samples_leaf": [1, 2],
    "max_features": ["sqrt", "log2"],
}

# ==========================
# Helper Functions
# ==========================

def load_and_preprocess_data():
    """Load and preprocess the dataset."""
    logger.info("Loading dataset...")
    
    raw_file = RAW_DATA_DIR / "data.csv"
    if not raw_file.exists():
        raise FileNotFoundError(f"Data file not found at {raw_file}")
    
    songs = pd.read_csv(raw_file)
    logger.info(f"Loaded {len(songs)} songs with {len(songs.columns)} features")
    
    logger.info("Preprocessing data...")
    songs = preprocess(songs)
    logger.info(f"After preprocessing: {len(songs)} songs")
    
    return songs


def engineer_features(songs):
    """Engineer features and prepare for ML."""
    logger.info("Feature engineering...")
    
    songs_enhanced = create_additional_features(songs)
    logger.info(f"Created additional features: {songs_enhanced.shape}")
    
    logger.info("Preparing features for machine learning...")
    X_train, X_test, y_train, y_test, scaler = prepare_features(
        songs_enhanced,
        scaler_type="standard"
    )
    
    logger.info(f"Training set: {X_train.shape[0]} samples, {X_train.shape[1]} features")
    logger.info(f"Test set: {X_test.shape[0]} samples")
    
    return X_train, X_test, y_train, y_test, scaler, songs_enhanced


def evaluate_model_simple(y_true, y_pred):
    """Simple evaluation function to avoid circular import."""
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    
    # MAPE
    mask = y_true != 0
    if mask.sum() > 0:
        mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
    else:
        mape = np.nan
    
    return {
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2,
        "MAPE": mape
    }


def perform_grid_search(X_train, y_train, param_grid=None, cv=5, verbose=2):
    """Perform exhaustive grid search."""
    if param_grid is None:
        param_grid = GRID_SEARCH_SPACE
    
    logger.info("Starting Grid Search...")
    logger.info(f"Cross-validation folds: {cv}")
    
    total_combinations = 1
    for values in param_grid.values():
        total_combinations *= len(values)
    logger.info(f"Total parameter combinations: {total_combinations}")
    logger.info(f"Total fits: {total_combinations * cv}")
    
    model = RandomForestRegressor(random_state=RANDOM_STATE)
    
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring="r2",
        cv=cv,
        n_jobs=-1,
        verbose=verbose,
        return_train_score=True,
    )
    
    start_time = time.time()
    grid_search.fit(X_train, y_train)
    elapsed_time = time.time() - start_time
    
    logger.info(f"Grid search completed in {elapsed_time:.2f} seconds")
    return grid_search


def perform_random_search(X_train, y_train, param_distributions=None, n_iter=50, cv=5, verbose=2):
    """Perform randomized search."""
    if param_distributions is None:
        param_distributions = RANDOM_SEARCH_SPACE
    
    logger.info("Starting Random Search...")
    logger.info(f"Number of iterations: {n_iter}")
    logger.info(f"Cross-validation folds: {cv}")
    logger.info(f"Total fits: {n_iter * cv}")
    
    model = RandomForestRegressor(random_state=RANDOM_STATE)
    
    random_search = RandomizedSearchCV(
        estimator=model,
        param_distributions=param_distributions,
        n_iter=n_iter,
        scoring="r2",
        cv=cv,
        n_jobs=-1,
        verbose=verbose,
        random_state=RANDOM_STATE,
        return_train_score=True,
    )
    
    start_time = time.time()
    random_search.fit(X_train, y_train)
    elapsed_time = time.time() - start_time
    
    logger.info(f"Random search completed in {elapsed_time:.2f} seconds")
    return random_search


def save_search_results(search_results, method_name="grid_search"):
    """Save search results to disk."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save best parameters
    best_params = search_results.best_params_
    params_file = REPORT_DIR / f"best_parameters_{method_name}.json"
    with open(params_file, "w", encoding="utf-8") as f:
        json.dump(best_params, f, indent=4)
    logger.info(f"Best parameters saved to: {params_file}")
    
    # Save all results
    results_df = pd.DataFrame(search_results.cv_results_)
    csv_file = REPORT_DIR / f"search_results_{method_name}.csv"
    results_df.to_csv(csv_file, index=False)
    logger.info(f"All search results saved to: {csv_file}")
    
    # Save best model
    model_file = MODEL_DIR / f"best_model_{method_name}.pkl"
    joblib.dump(search_results.best_estimator_, model_file)
    logger.info(f"Best model saved to: {model_file}")
    
    # Create summary
    summary_file = REPORT_DIR / f"search_summary_{method_name}.txt"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("HYPERPARAMETER SEARCH SUMMARY\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Method: {method_name.upper()}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Best Score (R2): {search_results.best_score_:.4f}\n\n")
        f.write("Best Parameters:\n")
        for key, value in best_params.items():
            f.write(f"  {key:20s}: {value}\n")
        f.write("\n" + "=" * 70 + "\n")
    
    logger.info(f"Search summary saved to: {summary_file}")
    
    return best_params


def evaluate_best_model(search_results, X_test, y_test, method_name="grid_search"):
    """Evaluate the best model on test set."""
    best_model = search_results.best_estimator_
    y_pred = best_model.predict(X_test)
    metrics = evaluate_model_simple(y_test, y_pred)
    
    logger.info("Best model test performance:")
    for key, value in metrics.items():
        if key == "MAPE":
            logger.info(f"  {key}: {value:.2f}%")
        else:
            logger.info(f"  {key}: {value:.4f}")
    
    # Save metrics
    metrics_file = REPORT_DIR / f"best_model_metrics_{method_name}.json"
    metrics_data = {
        "model": "RandomForestRegressor",
        "method": method_name,
        "best_params": search_results.best_params_,
        "best_score": search_results.best_score_,
        "test_metrics": metrics,
        "timestamp": datetime.now().isoformat(),
    }
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=4)
    
    logger.info(f"Best model metrics saved to: {metrics_file}")
    
    return metrics


def compare_with_baseline(best_metrics, baseline_metrics=None):
    """Compare tuned model with baseline."""
    if baseline_metrics is None:
        # Use default baseline values from earlier training
        baseline_metrics = {
            "R2": 0.8132,
            "MAE": 6.6365,
            "RMSE": 9.4556,
            "MAPE": 34.28,
        }
    
    comparison = pd.DataFrame({
        "Metric": ["R2", "MAE", "RMSE", "MAPE"],
        "Baseline": [
            baseline_metrics.get("R2", 0),
            baseline_metrics.get("MAE", 0),
            baseline_metrics.get("RMSE", 0),
            baseline_metrics.get("MAPE", 0),
        ],
        "Tuned": [
            best_metrics.get("R2", 0),
            best_metrics.get("MAE", 0),
            best_metrics.get("RMSE", 0),
            best_metrics.get("MAPE", 0),
        ]
    })
    
    # Calculate improvement
    comparison["Improvement"] = comparison["Tuned"] - comparison["Baseline"]
    for metric in ["MAE", "RMSE", "MAPE"]:
        comparison.loc[comparison["Metric"] == metric, "Improvement"] = (
            comparison.loc[comparison["Metric"] == metric, "Baseline"] - 
            comparison.loc[comparison["Metric"] == metric, "Tuned"]
        )
    
    comparison["Improvement %"] = (
        comparison["Improvement"] / comparison["Baseline"] * 100
    ).round(2)
    
    comp_file = REPORT_DIR / "model_comparison_tuned_vs_baseline.csv"
    comparison.to_csv(comp_file, index=False)
    logger.info(f"Comparison saved to: {comp_file}")
    
    print("\n" + "-" * 70)
    print("MODEL COMPARISON")
    print("-" * 70)
    print(comparison.to_string(index=False))
    
    return comparison


# ==========================
# Main Function
# ==========================

def main():
    """Main tuning orchestrator."""
    print("=" * 70)
    print("HYPERPARAMETER TUNING")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    try:
        # Step 1: Load and preprocess data
        songs = load_and_preprocess_data()
        
        # Step 2: Feature engineering
        X_train, X_test, y_train, y_test, scaler, songs_enhanced = engineer_features(songs)
        
        # Step 3: Perform hyperparameter search (using quick search for testing)
        logger.info("Starting hyperparameter search...")
        search = perform_random_search(
            X_train, y_train,
            param_distributions=QUICK_SEARCH_SPACE,
            n_iter=10,
            cv=3,
            verbose=1
        )
        
        # Step 4: Save results
        best_params = save_search_results(search, "random_search_quick")
        
        # Step 5: Evaluate best model
        test_metrics = evaluate_best_model(search, X_test, y_test, "random_search_quick")
        
        # Step 6: Compare with baseline
        comparison = compare_with_baseline(test_metrics)
        
        print("\n" + "=" * 70)
        print("TUNING COMPLETE!")
        print("=" * 70)
        print(f"Best Parameters: {best_params}")
        print(f"Best CV Score (R2): {search.best_score_:.4f}")
        print(f"Test R2: {test_metrics['R2']:.4f}")
        print(f"Test MAE: {test_metrics['MAE']:.4f}")
        print()
        print("Results saved to:")
        print(f"  - Parameters: {REPORT_DIR}/best_parameters_random_search_quick.json")
        print(f"  - Results: {REPORT_DIR}/search_results_random_search_quick.csv")
        print(f"  - Summary: {REPORT_DIR}/search_summary_random_search_quick.txt")
        print(f"  - Best Model: {MODEL_DIR}/best_model_random_search_quick.pkl")
        print("=" * 70)
        
    except Exception as e:
        logger.error(f"Tuning failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()