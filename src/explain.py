"""
SHAP Explainability Module for the Spotify Popularity Prediction Model.

This module generates SHAP (SHapley Additive exPlanations) values and visualizations
to explain model predictions. It provides both global and local interpretability.

Global explanations:
- SHAP Summary Plot (beeswarm)
- SHAP Bar Plot (feature importance)
- SHAP Dependence Plots for top features

Local explanations:
- Waterfall Plot for individual predictions
- Force Plot for individual predictions

Usage:
    python src/explain.py
    python src/explain.py --sample 5
    python src/explain.py --all
"""

import argparse
import joblib
import json
import logging
import sys
import warnings
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)

# ==========================
# Setup Path
# ==========================

_current_file = Path(__file__).resolve()
project_root = _current_file.parent.parent
src_path = project_root / "src"

if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# ==========================
# Import Project Modules
# ==========================

from config import (
    FEATURE_COLUMNS,
    FIGURE_DIR,
    MODEL_DIR,
    RANDOM_STATE,
    RAW_DATA_DIR,
    REPORT_DIR,
    TARGET_COLUMN,
)
from feature_engineering import create_additional_features, prepare_features
from preprocessing import preprocess, validate_data

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ==========================
# Configuration
# ==========================

# Directory for SHAP outputs
SHAP_DIR = REPORT_DIR / "explainability"
SHAP_DIR.mkdir(parents=True, exist_ok=True)

# Features to create dependence plots for
TOP_FEATURES_FOR_DEPENDENCE = 6

# Number of samples to explain individually
N_SAMPLES_TO_EXPLAIN = 3


# ==========================
# Data Loading Functions
# ==========================

def load_data():
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


def load_model():
    """Load the trained model."""
    model_file = MODEL_DIR / "random_forest_model.pkl"
    if not model_file.exists():
        raise FileNotFoundError(f"Model not found at {model_file}")
    
    model = joblib.load(model_file)
    logger.info(f"Model loaded from: {model_file}")
    logger.info(f"Model type: {type(model).__name__}")
    
    return model


def prepare_features_for_explanation(songs):
    """Prepare features for SHAP explanation."""
    logger.info("Preparing features for SHAP explanation...")
    
    # Create additional features
    songs_enhanced = create_additional_features(songs)
    logger.info(f"Created additional features: {songs_enhanced.shape}")
    
    # Select features
    X = songs_enhanced[FEATURE_COLUMNS]
    y = songs_enhanced[TARGET_COLUMN]
    
    logger.info(f"Features: {X.shape[1]} columns")
    logger.info(f"Samples: {X.shape[0]}")
    
    return X, y, songs_enhanced


# ==========================
# SHAP Computation
# ==========================

def compute_shap_values(model, X, sample_size=None):
    """
    Compute SHAP values for the model.
    
    Parameters
    ----------
    model : object
        Trained model
    X : pd.DataFrame
        Feature matrix
    sample_size : int, optional
        Number of samples to use (for faster computation)
    
    Returns
    -------
    tuple
        (explainer, shap_values, X_subset)
    """
    logger.info("Computing SHAP values...")
    
    # Use subset for faster computation if specified
    if sample_size and len(X) > sample_size:
        X_subset = X.sample(n=sample_size, random_state=RANDOM_STATE)
        logger.info(f"Using subset of {sample_size} samples for faster computation")
    else:
        X_subset = X
        logger.info(f"Using all {len(X)} samples")
    
    # Create TreeExplainer for Random Forest
    logger.info("Creating SHAP TreeExplainer...")
    explainer = shap.TreeExplainer(model)
    
    # Compute SHAP values
    logger.info("Computing SHAP values (this may take a moment)...")
    shap_values = explainer.shap_values(X_subset)
    
    logger.info(f"SHAP values shape: {shap_values.shape}")
    
    return explainer, shap_values, X_subset


# ==========================
# Global Explanation Plots
# ==========================

def plot_shap_summary(shap_values, X, feature_names=None, max_display=20):
    """
    Create SHAP summary plot (beeswarm).
    """
    logger.info("Creating SHAP summary plot...")
    
    plt.figure(figsize=(12, 8))
    
    shap.summary_plot(
        shap_values,
        X,
        feature_names=feature_names,
        max_display=max_display,
        show=False,
        plot_size=None
    )
    
    plt.tight_layout()
    
    # Save figure
    fig_file = SHAP_DIR / "shap_summary.png"
    plt.savefig(fig_file, dpi=300, bbox_inches="tight")
    plt.close()
    
    logger.info(f"SHAP summary plot saved to: {fig_file}")
    
    return fig_file


def plot_shap_bar(shap_values, X, feature_names=None, max_display=20):
    """
    Create SHAP bar plot (feature importance).
    """
    logger.info("Creating SHAP bar plot...")
    
    plt.figure(figsize=(10, 8))
    
    shap.summary_plot(
        shap_values,
        X,
        feature_names=feature_names,
        plot_type="bar",
        max_display=max_display,
        show=False,
        plot_size=None
    )
    
    plt.tight_layout()
    
    # Save figure
    fig_file = SHAP_DIR / "shap_bar.png"
    plt.savefig(fig_file, dpi=300, bbox_inches="tight")
    plt.close()
    
    logger.info(f"SHAP bar plot saved to: {fig_file}")
    
    return fig_file


def plot_shap_dependence(shap_values, X, feature_name, feature_names=None):
    """
    Create SHAP dependence plot for a specific feature.
    """
    logger.info(f"Creating SHAP dependence plot for: {feature_name}")
    
    plt.figure(figsize=(10, 6))
    
    shap.dependence_plot(
        feature_name,
        shap_values,
        X,
        feature_names=feature_names,
        show=False,
        dot_size=10,
        alpha=0.7,
    )
    
    plt.tight_layout()
    
    # Save figure
    fig_file = SHAP_DIR / f"shap_dependence_{feature_name}.png"
    plt.savefig(fig_file, dpi=300, bbox_inches="tight")
    plt.close()
    
    logger.info(f"SHAP dependence plot saved to: {fig_file}")
    
    return fig_file


def plot_shap_waterfall(explainer, shap_values, X, sample_idx=0, feature_names=None):
    """
    Create SHAP waterfall plot for a single prediction.
    """
    logger.info(f"Creating SHAP waterfall plot for sample {sample_idx}...")
    
    # Get the SHAP values for the specific sample
    shap_values_sample = shap_values[sample_idx:sample_idx+1]
    X_sample = X.iloc[sample_idx:sample_idx+1]
    
    # Handle base values properly
    if hasattr(explainer, 'expected_value'):
        base_value = explainer.expected_value
        # If it's an array, take the first element or mean
        if isinstance(base_value, (list, np.ndarray)):
            if len(base_value) > 1:
                # For multi-output, take first output
                base_value = base_value[0]
            elif len(base_value) == 1:
                base_value = base_value[0]
    else:
        base_value = 0
    
    # Create Explanation object
    shap_values_flat = shap_values_sample[0]
    if isinstance(shap_values_flat, (list, np.ndarray)) and len(shap_values_flat) > 0:
        # If it's a 2D array, flatten it
        if shap_values_flat.ndim > 1:
            shap_values_flat = shap_values_flat.flatten()
    
    # Get feature names
    if feature_names is None:
        feature_names = X.columns.tolist()
    
    # Ensure we have the right number of features
    if len(shap_values_flat) != len(feature_names):
        # If mismatch, use generic feature names
        feature_names = [f"Feature_{i}" for i in range(len(shap_values_flat))]
    
    # Create explanation
    exp = shap.Explanation(
        values=shap_values_flat,
        base_values=float(base_value) if not isinstance(base_value, (list, np.ndarray)) else float(base_value[0]) if isinstance(base_value, (list, np.ndarray)) else 0,
        data=X_sample.values[0],
        feature_names=feature_names
    )
    
    # Create waterfall plot
    try:
        plt.figure(figsize=(12, 8))
        
        shap.waterfall_plot(
            exp,
            show=False,
            max_display=15
        )
        
        plt.tight_layout()
        
        # Save figure
        fig_file = SHAP_DIR / f"shap_waterfall_sample_{sample_idx}.png"
        plt.savefig(fig_file, dpi=300, bbox_inches="tight")
        plt.close()
        
        logger.info(f"SHAP waterfall plot saved to: {fig_file}")
        return fig_file
        
    except Exception as e:
        logger.warning(f"Waterfall plot failed, trying alternative method...")
        plt.close()
        
        # Alternative: Use simpler waterfall plot
        try:
            # Create a simpler waterfall plot using matplotlib
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Sort features by importance
            indices = np.argsort(np.abs(shap_values_flat))[::-1]
            sorted_shap = shap_values_flat[indices]
            sorted_features = [feature_names[i] for i in indices]
            
            # Create waterfall bars
            cumulative = float(base_value) if not isinstance(base_value, (list, np.ndarray)) else float(base_value[0])
            bar_data = []
            for shap_val in sorted_shap:
                bar_data.append((cumulative, shap_val))
                cumulative += shap_val
            
            # Plot the waterfall
            for i, (start, value) in enumerate(bar_data):
                color = 'green' if value > 0 else 'red'
                ax.barh(i, value, left=start, color=color, alpha=0.7)
                # Add value label
                ax.text(start + value/2, i, f'{value:.2f}', 
                        ha='center', va='center', fontsize=8)
            
            # Add starting and ending values
            ax.barh(len(bar_data), 0, left=float(base_value) if not isinstance(base_value, (list, np.ndarray)) else float(base_value[0]), 
                    color='gray', alpha=0.3, label='Base Value')
            
            # Add labels
            ax.set_yticks(range(len(sorted_features)))
            ax.set_yticklabels(sorted_features)
            ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
            
            # Add title
            ax.set_title(f"SHAP Waterfall Plot - Sample {sample_idx}")
            ax.set_xlabel("SHAP Value")
            
            # Add final prediction text
            final_pred = cumulative
            base_val = float(base_value) if not isinstance(base_value, (list, np.ndarray)) else float(base_value[0])
            ax.text(0.95, 0.95, f"Base: {base_val:.2f}\nPrediction: {final_pred:.2f}", 
                    transform=ax.transAxes, ha='right', va='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            plt.tight_layout()
            
            # Save figure
            fig_file = SHAP_DIR / f"shap_waterfall_sample_{sample_idx}.png"
            plt.savefig(fig_file, dpi=300, bbox_inches="tight")
            plt.close()
            
            logger.info(f"SHAP waterfall plot (alternative) saved to: {fig_file}")
            return fig_file
            
        except Exception as e2:
            logger.error(f"Both waterfall methods failed: {e2}")
            return None


def plot_shap_force(explainer, shap_values, X, sample_idx=0):
    """
    Create SHAP force plot for a single prediction.
    """
    logger.info(f"Creating SHAP force plot for sample {sample_idx}...")
    
    # Get the SHAP values for the specific sample
    shap_values_sample = shap_values[sample_idx:sample_idx+1]
    X_sample = X.iloc[sample_idx:sample_idx+1]
    
    try:
        # Create force plot
        shap.force_plot(
            explainer.expected_value,
            shap_values_sample,
            X_sample,
            matplotlib=True,
            show=False,
            figsize=(15, 4)
        )
        
        # Save figure
        fig_file = SHAP_DIR / f"shap_force_sample_{sample_idx}.png"
        plt.savefig(fig_file, dpi=300, bbox_inches="tight")
        plt.close()
        
        logger.info(f"SHAP force plot saved to: {fig_file}")
        return fig_file
        
    except Exception as e:
        logger.warning(f"Force plot failed: {e}")
        plt.close()
        return None


# ==========================
# Feature Importance Analysis
# ==========================

def get_feature_importance_from_shap(shap_values, X):
    """
    Get feature importance from SHAP values.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with feature names and mean absolute SHAP values
    """
    # Mean absolute SHAP values per feature
    mean_shap = np.abs(shap_values).mean(axis=0)
    
    # Create DataFrame
    importance_df = pd.DataFrame({
        'feature': X.columns,
        'mean_shap': mean_shap
    }).sort_values('mean_shap', ascending=False)
    
    # Add percentage
    importance_df['percentage'] = (importance_df['mean_shap'] / importance_df['mean_shap'].sum()) * 100
    
    return importance_df


def get_top_features(shap_values, X, n=10):
    """
    Get top n features by SHAP importance.
    """
    importance_df = get_feature_importance_from_shap(shap_values, X)
    return importance_df.head(n)


def save_feature_importance_report(importance_df):
    """
    Save feature importance report to CSV.
    """
    csv_file = SHAP_DIR / "shap_feature_importance.csv"
    importance_df.to_csv(csv_file, index=False)
    logger.info(f"Feature importance report saved to: {csv_file}")
    
    return csv_file


# ==========================
# Explanation Report
# ==========================

def generate_shap_report(
    shap_values,
    X,
    importance_df,
    sample_explanations=None,
    training_time=None
):
    """
    Generate a comprehensive SHAP explanation report.
    """
    logger.info("Generating SHAP explanation report...")
    
    report_file = SHAP_DIR / "explanation_report.md"
    
    with open(report_file, "w", encoding="utf-8") as f:
        # Header
        f.write("# Spotify Popularity Prediction - SHAP Explanation Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        if training_time:
            f.write(f"**Training Time:** {training_time:.2f} seconds\n\n")
        
        # Overview
        f.write("## Overview\n\n")
        f.write(f"- **Model Type:** Random Forest Regressor\n")
        f.write(f"- **Number of Features:** {len(X.columns)}\n")
        f.write(f"- **Number of Samples Explained:** {len(X)}\n")
        f.write(f"- **SHAP Method:** TreeExplainer (exact)\n\n")
        
        # Top Features
        f.write("## Top 10 Most Influential Features\n\n")
        f.write("| Rank | Feature | Mean SHAP | Percentage |\n")
        f.write("|------|---------|-----------|------------|\n")
        
        for idx, row in importance_df.head(10).iterrows():
            f.write(f"| {idx+1} | {row['feature']} | {row['mean_shap']:.3f} | {row['percentage']:.1f}% |\n")
        
        f.write("\n")
        
        # Interpretation
        f.write("## Interpretation\n\n")
        f.write("### How to Read the SHAP Summary Plot\n\n")
        f.write("1. **Features are ordered by importance** (top = most influential)\n")
        f.write("2. **Color represents feature value** (red = high, blue = low)\n")
        f.write("3. **Position on x-axis shows impact on prediction**:\n")
        f.write("   - Positive SHAP value = pushes prediction higher\n")
        f.write("   - Negative SHAP value = pushes prediction lower\n\n")
        
        f.write("### Key Observations\n\n")
        
        # Get top 3 features
        top_features = importance_df.head(3)['feature'].tolist()
        f.write(f"1. **{top_features[0]}** is the most influential feature\n")
        f.write(f"2. **{top_features[1]}** and **{top_features[2]}** are also significant\n")
        f.write("3. Some features show non-linear relationships (visible in dependence plots)\n\n")
        
        # Individual Explanations
        if sample_explanations:
            f.write("## Individual Prediction Explanations\n\n")
            f.write("The following waterfall plots show how features contributed to specific predictions:\n\n")
            
            for sample_idx in sample_explanations:
                f.write(f"### Sample {sample_idx}\n\n")
                f.write(f"![Waterfall Plot](shap_waterfall_sample_{sample_idx}.png)\n\n")
        
        # Visualizations
        f.write("## Visualization Gallery\n\n")
        f.write("### 1. SHAP Summary Plot (Beeswarm)\n\n")
        f.write("![SHAP Summary](shap_summary.png)\n\n")
        f.write("*This plot shows global feature importance and direction of impact.*\n\n")
        
        f.write("### 2. SHAP Bar Plot\n\n")
        f.write("![SHAP Bar](shap_bar.png)\n\n")
        f.write("*This plot ranks features by average absolute SHAP value.*\n\n")
        
        f.write("### 3. Feature Dependence Plots\n\n")
        f.write("These plots show how individual features affect predictions:\n\n")
        
        for feature in top_features[:3]:
            f.write(f"#### {feature}\n\n")
            f.write(f"![{feature} Dependence](shap_dependence_{feature}.png)\n\n")
        
        # Recommendations
        f.write("## Recommendations\n\n")
        f.write("Based on the SHAP analysis:\n\n")
        f.write("1. **Focus on top features** for model improvement and feature engineering\n")
        f.write("2. **Investigate non-linear relationships** shown in dependence plots\n")
        f.write("3. **Consider feature interactions** between top features\n")
        f.write("4. **Use individual explanations** for business decisions and stakeholder communication\n\n")
        
        f.write("---\n")
        f.write("*Report generated by Spotify Popularity Prediction Pipeline*\n")
    
    logger.info(f"SHAP explanation report saved to: {report_file}")
    
    return report_file


# ==========================
# Main Execution
# ==========================

def main():
    """Main SHAP explanation orchestrator."""
    parser = argparse.ArgumentParser(
        description="Generate SHAP explanations for the Spotify model"
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=0,
        help="Sample index to explain (for waterfall plot)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate all plots (may take longer)"
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=1000,
        help="Number of samples to use for SHAP computation (default: 1000)"
    )
    parser.add_argument(
        "--skip-dependence",
        action="store_true",
        help="Skip dependence plots (saves time)"
    )
    args = parser.parse_args()
    
    print("=" * 70)
    print("SHAP EXPLAINABILITY - MODEL INTERPRETATION")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    try:
        # Step 1: Load data and model
        logger.info("Step 1: Loading data and model...")
        songs = load_data()
        model = load_model()
        
        # Step 2: Prepare features
        logger.info("Step 2: Preparing features...")
        X, y, songs_enhanced = prepare_features_for_explanation(songs)
        
        # Step 3: Compute SHAP values
        logger.info("Step 3: Computing SHAP values...")
        sample_size = args.samples if args.all else min(args.samples, 1000)
        explainer, shap_values, X_subset = compute_shap_values(
            model, X, sample_size=sample_size
        )
        
        # Step 4: Get feature importance
        logger.info("Step 4: Analyzing feature importance...")
        importance_df = get_feature_importance_from_shap(shap_values, X_subset)
        save_feature_importance_report(importance_df)
        
        # Print top features
        print("\n" + "-" * 70)
        print("TOP 10 FEATURES BY SHAP IMPORTANCE")
        print("-" * 70)
        for idx, row in importance_df.head(10).iterrows():
            print(f"{idx+1:2d}. {row['feature']:20s} | Mean SHAP: {row['mean_shap']:.3f} | {row['percentage']:.1f}%")
        print("-" * 70)
        print()
        
        # Step 5: Generate global plots
        logger.info("Step 5: Generating global SHAP plots...")
        feature_names = X_subset.columns.tolist()
        
        # Summary plot
        plot_shap_summary(shap_values, X_subset, feature_names)
        
        # Bar plot
        plot_shap_bar(shap_values, X_subset, feature_names)
        
        # Dependence plots for top features
        if not args.skip_dependence:
            logger.info("Generating dependence plots for top features...")
            top_features = importance_df.head(TOP_FEATURES_FOR_DEPENDENCE)['feature'].tolist()
            for feature in top_features:
                plot_shap_dependence(shap_values, X_subset, feature, feature_names)
        
        # Step 6: Generate individual explanations
        logger.info("Step 6: Generating individual explanations...")
        
        sample_explanations = []
        
        # Waterfall plot for specified sample
        if args.sample < len(X_subset):
            plot_shap_waterfall(explainer, shap_values, X_subset, args.sample, feature_names)
            sample_explanations.append(args.sample)
        
        # Generate a few more waterfall plots
        for i in range(min(N_SAMPLES_TO_EXPLAIN, len(X_subset))):
            if i != args.sample:
                plot_shap_waterfall(explainer, shap_values, X_subset, i, feature_names)
                sample_explanations.append(i)
        
        # Force plot for the first sample
        plot_shap_force(explainer, shap_values, X_subset, 0)
        
        # Step 7: Generate report
        logger.info("Step 7: Generating SHAP explanation report...")
        generate_shap_report(
            shap_values,
            X_subset,
            importance_df,
            sample_explanations=sample_explanations[:3]
        )
        
        # Summary
        print("=" * 70)
        print("SHAP EXPLANATION COMPLETE!")
        print("=" * 70)
        print(f"Generated files saved to: {SHAP_DIR}")
        print("\nFiles created:")
        for file in SHAP_DIR.glob("*"):
            print(f"  - {file.name}")
        print()
        print("=" * 70)
        print("Next: Open the explanation report to view insights:")
        print(f"  {SHAP_DIR}/explanation_report.md")
        print("=" * 70)
        
    except Exception as e:
        logger.error(f"SHAP explanation failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()