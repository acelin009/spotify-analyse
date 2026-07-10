"""
Evaluation module for the Spotify Popularity Prediction Model.

Handles all model evaluation, metrics calculation, visualization,
and report generation.

This module is responsible for:
- Computing regression metrics (MAE, RMSE, R2, MAPE)
- Saving metrics to JSON and CSV
- Generating prediction plots
- Visualizing feature importance
- Creating training summaries
- Saving prediction residuals

Usage:
    from evaluate import evaluate_model, save_metrics, save_prediction_plots
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from config import (
    FIGURE_DIR,
    MODEL_DIR,
    RANDOM_STATE,
    REPORT_DIR,
    TARGET_COLUMN,
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def evaluate_model(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    prefix: str = ""
) -> Dict[str, float]:
    """
    Calculate regression metrics.

    Parameters
    ----------
    y_true : np.ndarray
        Actual target values
    y_pred : np.ndarray
        Predicted target values
    prefix : str, default=""
        Prefix for metric names (e.g., "train_", "test_")

    Returns
    -------
    Dict[str, float]
        Dictionary containing MAE, MSE, RMSE, R2, MAPE
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)

    # Calculate MAPE (Mean Absolute Percentage Error)
    mask = y_true != 0
    if mask.sum() > 0:
        mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
    else:
        mape = np.nan

    metrics = {
        f"{prefix}MAE": mae,
        f"{prefix}MSE": mse,
        f"{prefix}RMSE": rmse,
        f"{prefix}R2": r2,
        f"{prefix}MAPE": mape,
    }

    return metrics


def evaluate_all_models(
    models: Dict[str, object],
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
) -> Dict[str, Dict[str, float]]:
    """
    Evaluate multiple models and return their metrics.

    Parameters
    ----------
    models : Dict[str, object]
        Dictionary of model_name -> trained model
    X_train, X_test : np.ndarray
        Training and test features
    y_train, y_test : np.ndarray
        Training and test targets

    Returns
    -------
    Dict[str, Dict[str, float]]
        Dictionary of model_name -> metrics
    """
    results = {}

    for name, model in models.items():
        logger.info(f"Evaluating {name}...")

        # Predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # Calculate metrics
        train_metrics = evaluate_model(y_train, y_pred_train, "train_")
        test_metrics = evaluate_model(y_test, y_pred_test, "test_")

        # Combine
        results[name] = {**train_metrics, **test_metrics}

        logger.info(f"  {name} R2: {test_metrics['test_R2']:.4f}")

    return results


def save_metrics(
    metrics: Dict[str, float],
    model_name: str = "random_forest",
    additional_info: Optional[Dict] = None,
) -> None:
    """
    Save metrics to JSON and CSV files.

    Parameters
    ----------
    metrics : Dict[str, float]
        Dictionary of evaluation metrics
    model_name : str, default="random_forest"
        Name of the model
    additional_info : Dict, optional
        Additional metadata to include in the report
    """
    # Create report directory if it doesn't exist
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Prepare report
    report = {
        "model_name": model_name,
        "timestamp": datetime.now().isoformat(),
        "metrics": metrics,
        "dataset": "Spotify Tracks",
        "target_column": TARGET_COLUMN,
        "random_state": RANDOM_STATE,
    }

    if additional_info:
        report["additional_info"] = additional_info

    # Save as JSON
    json_file = REPORT_DIR / f"{model_name}_metrics.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
    logger.info(f"Metrics saved to: {json_file}")

    # Save as CSV (flat format)
    metrics_df = pd.DataFrame([metrics])
    csv_file = REPORT_DIR / f"{model_name}_metrics.csv"
    metrics_df.to_csv(csv_file, index=False)
    logger.info(f"Metrics CSV saved to: {csv_file}")

    return report


def save_prediction_plots(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    model_name: str = "random_forest",
    residuals: Optional[np.ndarray] = None,
) -> None:
    """
    Generate and save prediction visualization plots.

    Creates:
    1. Actual vs Predicted scatter plot
    2. Residual plot
    3. Residual distribution histogram
    4. Q-Q plot

    Parameters
    ----------
    y_true : np.ndarray
        Actual target values
    y_pred : np.ndarray
        Predicted target values
    model_name : str, default="random_forest"
        Name of the model
    residuals : np.ndarray, optional
        Pre-computed residuals. If None, calculates from y_true and y_pred.
    """
    # Create figure directory if it doesn't exist
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    # Set style
    plt.style.use("seaborn-v0_8-darkgrid")

    # Calculate residuals if not provided
    if residuals is None:
        residuals = y_true - y_pred

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 1. Actual vs Predicted scatter plot
    ax = axes[0, 0]
    ax.scatter(y_true, y_pred, alpha=0.5, s=10)
    ax.plot(
        [y_true.min(), y_true.max()],
        [y_true.min(), y_true.max()],
        "r--",
        lw=2,
        label="Perfect Prediction",
    )
    ax.set_xlabel("Actual Popularity")
    ax.set_ylabel("Predicted Popularity")
    ax.set_title("Actual vs Predicted")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Calculate and display correlation
    corr = np.corrcoef(y_true, y_pred)[0, 1]
    ax.text(
        0.05,
        0.95,
        f"Correlation: {corr:.3f}",
        transform=ax.transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

    # 2. Residual plot
    ax = axes[0, 1]
    ax.scatter(y_pred, residuals, alpha=0.5, s=10)
    ax.axhline(y=0, color="r", linestyle="--", lw=2)
    ax.set_xlabel("Predicted Popularity")
    ax.set_ylabel("Residuals")
    ax.set_title("Residual Plot")
    ax.grid(True, alpha=0.3)

    # Add residual statistics
    residual_std = np.std(residuals)
    ax.text(
        0.05,
        0.95,
        f"Residual Std: {residual_std:.3f}",
        transform=ax.transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

    # 3. Residual distribution
    ax = axes[1, 0]
    ax.hist(residuals, bins=30, edgecolor="black", alpha=0.7, density=True)
    ax.axvline(x=0, color="r", linestyle="--", lw=2)
    ax.set_xlabel("Residuals")
    ax.set_ylabel("Density")
    ax.set_title("Residual Distribution")

    # Overlay normal distribution
    mu, sigma = stats.norm.fit(residuals)
    x = np.linspace(residuals.min(), residuals.max(), 100)
    ax.plot(x, stats.norm.pdf(x, mu, sigma), "b-", lw=2, label="Normal Fit")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 4. Q-Q plot
    ax = axes[1, 1]
    stats.probplot(residuals, dist="norm", plot=ax)
    ax.set_title("Q-Q Plot")
    ax.grid(True, alpha=0.3)

    # Adjust layout and save
    plt.tight_layout()

    # Save figure
    fig_file = FIGURE_DIR / f"{model_name}_predictions.png"
    fig.savefig(fig_file, dpi=300, bbox_inches="tight")
    plt.close()

    logger.info(f"Prediction plots saved to: {fig_file}")

    return fig_file


def save_feature_importance(
    model,
    feature_names: List[str],
    model_name: str = "random_forest",
    n_top: int = 20,
) -> pd.DataFrame:
    """
    Save feature importance plot and CSV.

    Parameters
    ----------
    model : object
        Trained model with feature_importances_ attribute
    feature_names : List[str]
        List of feature names
    model_name : str, default="random_forest"
        Name of the model
    n_top : int, default=20
        Number of top features to display

    Returns
    -------
    pd.DataFrame
        DataFrame with feature importances
    """
    if not hasattr(model, "feature_importances_"):
        logger.warning("Model doesn't have feature_importances_ attribute. Skipping.")
        return pd.DataFrame()

    # Create directories
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    # Get feature importances
    importances = model.feature_importances_

    # Ensure feature_names length matches importances
    if len(feature_names) != len(importances):
        logger.warning(
            f"Feature names length ({len(feature_names)}) doesn't match "
            f"importances length ({len(importances)}). Using indices as names."
        )
        feature_names = [f"Feature_{i}" for i in range(len(importances))]

    # Create DataFrame
    importance_df = pd.DataFrame(
        {"feature": feature_names, "importance": importances}
    ).sort_values("importance", ascending=False)

    # Save as CSV
    csv_file = REPORT_DIR / f"{model_name}_feature_importance.csv"
    importance_df.to_csv(csv_file, index=False)
    logger.info(f"Feature importance CSV saved to: {csv_file}")

    # Create plot
    plt.figure(figsize=(10, max(6, n_top * 0.4)))

    # Take top n features
    top_features = importance_df.head(n_top)

    # Horizontal bar plot
    plt.barh(top_features["feature"], top_features["importance"])
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.title(f"Top {n_top} Feature Importances - {model_name.upper()}")
    plt.tight_layout()

    # Save plot
    fig_file = FIGURE_DIR / f"{model_name}_feature_importance.png"
    plt.savefig(fig_file, dpi=300, bbox_inches="tight")
    plt.close()

    logger.info(f"Feature importance plot saved to: {fig_file}")

    return importance_df


def save_training_summary(
    metrics: Dict[str, float],
    model_name: str = "random_forest",
    training_time: Optional[float] = None,
    additional_info: Optional[Dict] = None,
) -> str:
    """
    Generate a human-readable training summary text file.

    Parameters
    ----------
    metrics : Dict[str, float]
        Dictionary of evaluation metrics
    model_name : str, default="random_forest"
        Name of the model
    training_time : float, optional
        Training time in seconds
    additional_info : Dict, optional
        Additional information to include

    Returns
    -------
    str
        Path to the summary file
    """
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    summary_file = REPORT_DIR / f"{model_name}_training_summary.txt"

    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("SPOTIFY POPULARITY PREDICTION - TRAINING SUMMARY\n")
        f.write("=" * 70 + "\n\n")

        f.write(f"Model: {model_name.upper()}\n")
        f.write(f"Training Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Random Seed: {RANDOM_STATE}\n")

        if training_time:
            f.write(f"Training Time: {training_time:.2f} seconds\n")

        if additional_info:
            f.write("\n" + "-" * 70 + "\n")
            f.write("ADDITIONAL INFORMATION\n")
            f.write("-" * 70 + "\n")
            for key, value in additional_info.items():
                f.write(f"{key}: {value}\n")

        f.write("\n" + "-" * 70 + "\n")
        f.write("PERFORMANCE METRICS\n")
        f.write("-" * 70 + "\n\n")

        # Separate train and test metrics
        train_metrics = {k: v for k, v in metrics.items() if k.startswith("train_")}
        test_metrics = {k: v for k, v in metrics.items() if k.startswith("test_")}

        if train_metrics:
            f.write("Training Set:\n")
            for key, value in train_metrics.items():
                clean_key = key.replace("train_", "")
                if clean_key == "MAPE":
                    f.write(f"  {clean_key:10s}: {value:8.2f}%\n")
                else:
                    f.write(f"  {clean_key:10s}: {value:8.4f}\n")
            f.write("\n")

        if test_metrics:
            f.write("Test Set:\n")
            for key, value in test_metrics.items():
                clean_key = key.replace("test_", "")
                if clean_key == "MAPE":
                    f.write(f"  {clean_key:10s}: {value:8.2f}%\n")
                else:
                    f.write(f"  {clean_key:10s}: {value:8.4f}\n")
            f.write("\n")

        # Add interpretation
        f.write("-" * 70 + "\n")
        f.write("INTERPRETATION\n")
        f.write("-" * 70 + "\n\n")

        r2 = test_metrics.get("test_R2", metrics.get("R2", 0))
        if r2 >= 0.8:
            f.write("[SUCCESS] Excellent model performance (R2 >= 0.8)\n")
            f.write("  The model explains more than 80% of the variance.\n")
        elif r2 >= 0.6:
            f.write("[GOOD] Good model performance (R2 >= 0.6)\n")
            f.write("  The model explains between 60-80% of the variance.\n")
        elif r2 >= 0.4:
            f.write("[MODERATE] Moderate model performance (R2 >= 0.4)\n")
            f.write("  The model explains between 40-60% of the variance.\n")
        else:
            f.write("[WARNING] Low model performance (R2 < 0.4)\n")
            f.write("  Consider adding more features or trying a different model.\n")

        mae = test_metrics.get("test_MAE", metrics.get("MAE", 0))
        f.write(f"\n  Average prediction error: {mae:.2f} points\n")

        if mae < 5:
            f.write("  [SUCCESS] Very accurate predictions (MAE < 5)\n")
        elif mae < 10:
            f.write("  [GOOD] Reasonably accurate predictions (MAE < 10)\n")
        else:
            f.write("  [WARNING] Considerable prediction error (MAE >= 10)\n")

        f.write("\n" + "=" * 70 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 70 + "\n")

    logger.info(f"Training summary saved to: {summary_file}")
    return str(summary_file)


def save_predictions_csv(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    model_name: str = "random_forest",
    additional_data: Optional[pd.DataFrame] = None,
) -> str:
    """
    Save predictions with residuals to CSV.

    Parameters
    ----------
    y_true : np.ndarray
        Actual target values
    y_pred : np.ndarray
        Predicted target values
    model_name : str, default="random_forest"
        Name of the model
    additional_data : pd.DataFrame, optional
        Additional data to include (e.g., song IDs, names)

    Returns
    -------
    str
        Path to the saved CSV file
    """
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Calculate residuals
    residuals = y_true - y_pred

    # Create DataFrame
    pred_df = pd.DataFrame(
        {
            "actual": y_true,
            "predicted": y_pred,
            "residual": residuals,
            "abs_error": np.abs(residuals),
            "pct_error": np.abs(residuals / (y_true + 1e-10)) * 100,
        }
    )

    # Add additional data if provided
    if additional_data is not None:
        # Reset index to align properly
        additional_data = additional_data.reset_index(drop=True)
        pred_df = pd.concat([additional_data, pred_df], axis=1)

    # Sort by absolute error (worst predictions first)
    pred_df = pred_df.sort_values("abs_error", ascending=False)

    # Save to CSV
    csv_file = REPORT_DIR / f"{model_name}_predictions.csv"
    pred_df.to_csv(csv_file, index=False)
    logger.info(f"Predictions CSV saved to: {csv_file}")

    return str(csv_file)


def save_model_metadata(
    model,
    model_name: str = "random_forest",
    feature_names: Optional[List[str]] = None,
    metrics: Optional[Dict] = None,
    additional_info: Optional[Dict] = None,
) -> str:
    """
    Save model metadata including parameters, features, and performance.

    Parameters
    ----------
    model : object
        Trained model
    model_name : str, default="random_forest"
        Name of the model
    feature_names : List[str], optional
        List of feature names
    metrics : Dict, optional
        Model performance metrics
    additional_info : Dict, optional
        Additional metadata

    Returns
    -------
    str
        Path to the metadata file
    """
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Get model parameters
    model_params = {}
    if hasattr(model, "get_params"):
        model_params = model.get_params()

    # Prepare metadata
    metadata = {
        "model_name": model_name,
        "model_type": type(model).__name__,
        "timestamp": datetime.now().isoformat(),
        "random_state": RANDOM_STATE,
        "target_column": TARGET_COLUMN,
        "parameters": model_params,
        "feature_names": feature_names,
        "n_features": len(feature_names) if feature_names else None,
        "metrics": metrics,
    }

    if additional_info:
        metadata["additional_info"] = additional_info

    # Save to JSON
    metadata_file = REPORT_DIR / f"{model_name}_metadata.json"
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    logger.info(f"Model metadata saved to: {metadata_file}")
    return str(metadata_file)


def save_training_config(config: Dict) -> str:
    """
    Save the training configuration.

    Parameters
    ----------
    config : Dict
        Training configuration dictionary

    Returns
    -------
    str
        Path to the config file
    """
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Add timestamp
    config["timestamp"] = datetime.now().isoformat()

    # Save to JSON
    config_file = REPORT_DIR / "training_config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

    logger.info(f"Training config saved to: {config_file}")
    return str(config_file)


def plot_residuals_by_feature(
    residuals: np.ndarray,
    feature_values: np.ndarray,
    feature_name: str,
    model_name: str = "random_forest",
) -> None:
    """
    Plot residuals vs a specific feature to check for patterns.

    Parameters
    ----------
    residuals : np.ndarray
        Residuals from the model
    feature_values : np.ndarray
        Values of the feature to plot against
    feature_name : str
        Name of the feature
    model_name : str, default="random_forest"
        Name of the model
    """
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.scatter(feature_values, residuals, alpha=0.5, s=10)
    plt.axhline(y=0, color="r", linestyle="--", lw=2)
    plt.xlabel(feature_name)
    plt.ylabel("Residuals")
    plt.title(f"Residuals vs {feature_name} - {model_name.upper()}")
    plt.grid(True, alpha=0.3)

    # Add trend line
    z = np.polyfit(feature_values, residuals, 1)
    p = np.poly1d(z)
    x_sorted = np.sort(feature_values)
    plt.plot(x_sorted, p(x_sorted), "g-", lw=2, label="Trend Line")
    plt.legend()

    plt.tight_layout()

    # Save plot
    fig_file = FIGURE_DIR / f"{model_name}_residuals_vs_{feature_name}.png"
    plt.savefig(fig_file, dpi=300, bbox_inches="tight")
    plt.close()

    logger.info(f"Residuals vs {feature_name} plot saved to: {fig_file}")


# ==========================
# Utility Functions
# ==========================

def get_best_model(
    results: Dict[str, Dict[str, float]],
    metric: str = "test_R2",
) -> Tuple[str, Dict[str, float]]:
    """
    Get the best performing model based on a metric.

    Parameters
    ----------
    results : Dict[str, Dict[str, float]]
        Dictionary of model_name -> metrics
    metric : str, default="test_R2"
        Metric to use for comparison

    Returns
    -------
    Tuple[str, Dict[str, float]]
        Best model name and its metrics
    """
    best_model = max(results.items(), key=lambda x: x[1].get(metric, -np.inf))
    return best_model


def compare_models(results: Dict[str, Dict[str, float]]) -> pd.DataFrame:
    """
    Create a comparison DataFrame of all models.

    Parameters
    ----------
    results : Dict[str, Dict[str, float]]
        Dictionary of model_name -> metrics

    Returns
    -------
    pd.DataFrame
        Comparison table
    """
    df = pd.DataFrame.from_dict(results, orient="index")
    # Select only test metrics for comparison
    test_cols = [col for col in df.columns if col.startswith("test_")]
    if test_cols:
        df = df[test_cols]
        # Rename columns to remove prefix
        df.columns = [col.replace("test_", "") for col in df.columns]
    return df