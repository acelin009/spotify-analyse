import argparse
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

# Add src to path if running from project root
sys.path.append(str(Path(__file__).resolve().parent))

from config import (
    FEATURE_COLUMNS,
    FIGURE_DIR,
    MODEL_DIR,
    RANDOM_STATE,
    RAW_DATA_DIR,
    REPORT_DIR,
    RF_MODEL_PARAMS,
    TARGET_COLUMN,
    TEST_SIZE,
)
from evaluate import (
    compare_models,
    evaluate_all_models,
    get_best_model,
    save_feature_importance,
    save_metrics,
    save_model_metadata,
    save_predictions_csv,
    save_prediction_plots,
    save_training_config,
    save_training_summary,
)
from feature_engineering import create_additional_features, prepare_features
from preprocessing import preprocess

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def get_model(model_name: str, **kwargs):
    """
    Get a model instance by name.

    Parameters
    ----------
    model_name : str
        Name of the model ('linear', 'decision_tree', 'random_forest')
    **kwargs
        Additional parameters to pass to the model

    Returns
    -------
    object
        Model instance
    """
    models = {
        "linear": LinearRegression,
        "decision_tree": DecisionTreeRegressor,
        "random_forest": RandomForestRegressor,
    }

    model_class = models.get(model_name.lower())
    if model_class is None:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(models.keys())}")

    # Default parameters for each model
    default_params = {
        "linear": {},
        "decision_tree": {"random_state": RANDOM_STATE, "max_depth": 10},
        "random_forest": RF_MODEL_PARAMS,
    }

    params = default_params.get(model_name.lower(), {})
    params.update(kwargs)

    return model_class(**params)


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

    # Create additional features
    songs_enhanced = create_additional_features(songs)
    logger.info(f"Created additional features: {songs_enhanced.shape}")

    # Prepare features for ML
    logger.info("Preparing features for machine learning...")
    X_train, X_test, y_train, y_test, scaler = prepare_features(
        songs_enhanced,
        scaler_type="standard"
    )

    logger.info(f"Training set: {X_train.shape[0]} samples, {X_train.shape[1]} features")
    logger.info(f"Test set: {X_test.shape[0]} samples")

    return X_train, X_test, y_train, y_test, scaler, songs_enhanced


def train_model(X_train, y_train, model_name="random_forest", **kwargs):
    """Train a single model."""
    logger.info(f"Training {model_name} model...")

    model = get_model(model_name, **kwargs)
    start_time = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start_time

    logger.info(f"Model trained in {training_time:.2f} seconds")
    return model, training_time


def train_all_models(X_train, y_train, models_to_train=None):
    """Train multiple models and return them."""
    if models_to_train is None:
        models_to_train = ["linear", "decision_tree", "random_forest"]

    trained_models = {}
    training_times = {}

    for model_name in models_to_train:
        model, train_time = train_model(X_train, y_train, model_name)
        trained_models[model_name] = model
        training_times[model_name] = train_time

    return trained_models, training_times


def save_artifacts(
    model,
    model_name,
    X_train,
    X_test,
    y_train,
    y_test,
    scaler,
    feature_names,
    training_time,
    metrics,
):
    """Save all artifacts to disk."""
    logger.info("Saving artifacts...")

    # Create directories
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    # Save model
    model_file = MODEL_DIR / f"{model_name}_model.pkl"
    joblib.dump(model, model_file)
    logger.info(f"Model saved to: {model_file}")

    # Save scaler
    scaler_file = MODEL_DIR / "scaler.pkl"
    joblib.dump(scaler, scaler_file)
    logger.info(f"Scaler saved to: {scaler_file}")

    # Generate predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    # Save metrics
    save_metrics(metrics, model_name)

    # Save predictions CSV
    save_predictions_csv(y_test, y_pred_test, model_name)

    # Save prediction plots
    save_prediction_plots(y_test, y_pred_test, model_name)

    # Save feature importance (if available)
    if hasattr(model, "feature_importances_"):
        save_feature_importance(model, feature_names, model_name)

    # Save training summary
    save_training_summary(
        metrics,
        model_name,
        training_time=training_time,
        additional_info={
            "test_size": TEST_SIZE,
            "n_features": len(feature_names),
            "n_train_samples": len(X_train),
            "n_test_samples": len(X_test),
        }
    )

    # Save model metadata
    save_model_metadata(
        model,
        model_name,
        feature_names=feature_names,
        metrics=metrics,
        additional_info={
            "training_time": training_time,
            "test_size": TEST_SIZE,
        }
    )

    return y_pred_test


def main():
    """Main training pipeline orchestrator."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Train Spotify popularity prediction models")
    parser.add_argument(
        "--model",
        type=str,
        default="random_forest",
        choices=["linear", "decision_tree", "random_forest", "all"],
        help="Model to train (default: random_forest)"
    )
    parser.add_argument(
        "--save-best",
        action="store_true",
        help="Save only the best performing model"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    print("=" * 70)
    print("SPOTIFY POPULARITY PREDICTION - TRAINING PIPELINE")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()

    try:
        # Step 1: Load and preprocess data
        songs = load_and_preprocess_data()

        # Step 2: Feature engineering
        X_train, X_test, y_train, y_test, scaler, songs_enhanced = engineer_features(songs)

        # Get feature names
        feature_names = songs_enhanced[FEATURE_COLUMNS].columns.tolist()
        logger.info(f"Using {len(feature_names)} features")

        # Step 3: Train model(s)
        if args.model == "all":
            # Train multiple models
            models_to_train = ["linear", "decision_tree", "random_forest"]
            trained_models, training_times = train_all_models(X_train, y_train, models_to_train)

            # Evaluate all models
            logger.info("Evaluating all models...")
            results = evaluate_all_models(
                trained_models, X_train, X_test, y_train, y_test
            )

            # Compare models
            comparison_df = compare_models(results)
            logger.info("\nModel Comparison:")
            print(comparison_df.round(4))

            # Save comparison
            comparison_df.to_csv(REPORT_DIR / "model_comparison.csv")
            logger.info(f"Model comparison saved to: {REPORT_DIR}/model_comparison.csv")

            # Find best model
            best_model_name, best_metrics = get_best_model(results)
            logger.info(f"Best model: {best_model_name} with R2 = {best_metrics['test_R2']:.4f}")

            if args.save_best:
                # Save only the best model
                logger.info(f"Saving best model: {best_model_name}")
                best_model = trained_models[best_model_name]
                best_time = training_times[best_model_name]

                save_artifacts(
                    best_model,
                    f"{best_model_name}_best",
                    X_train,
                    X_test,
                    y_train,
                    y_test,
                    scaler,
                    feature_names,
                    best_time,
                    best_metrics
                )
            else:
                # Save all models
                for model_name, model in trained_models.items():
                    metrics = results[model_name]
                    save_artifacts(
                        model,
                        model_name,
                        X_train,
                        X_test,
                        y_train,
                        y_test,
                        scaler,
                        feature_names,
                        training_times[model_name],
                        metrics
                    )

        else:
            # Train a single model
            model, training_time = train_model(X_train, y_train, args.model)

            # Generate predictions
            y_pred_train = model.predict(X_train)
            y_pred_test = model.predict(X_test)

            # Calculate metrics
            from evaluate import evaluate_model
            train_metrics = evaluate_model(y_train, y_pred_train, "train_")
            test_metrics = evaluate_model(y_test, y_pred_test, "test_")
            metrics = {**train_metrics, **test_metrics}

            # Display metrics
            print("\n" + "-" * 70)
            print("MODEL PERFORMANCE")
            print("-" * 70)
            print("Training Metrics:")
            for key, value in train_metrics.items():
                if key == "train_MAPE":
                    print(f"  {key.replace('train_', ''):10s}: {value:8.2f}%")
                else:
                    print(f"  {key.replace('train_', ''):10s}: {value:8.4f}")

            print("\nTest Metrics:")
            for key, value in test_metrics.items():
                if key == "test_MAPE":
                    print(f"  {key.replace('test_', ''):10s}: {value:8.2f}%")
                else:
                    print(f"  {key.replace('test_', ''):10s}: {value:8.4f}")

            # Save artifacts
            save_artifacts(
                model,
                args.model,
                X_train,
                X_test,
                y_train,
                y_test,
                scaler,
                feature_names,
                training_time,
                metrics
            )

        # Step 4: Save training configuration
        config = {
            "model": args.model,
            "test_size": TEST_SIZE,
            "random_state": RANDOM_STATE,
            "n_features": len(feature_names),
            "feature_columns": FEATURE_COLUMNS,
            "target_column": TARGET_COLUMN,
        }
        save_training_config(config)

        print("\n" + "=" * 70)
        print("TRAINING COMPLETE!")
        print("=" * 70)
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Artifacts saved to:")
        print(f"  - Models: {MODEL_DIR}")
        print(f"  - Reports: {REPORT_DIR}")
        print(f"  - Figures: {FIGURE_DIR}")
        print("=" * 70)

    except Exception as e:
        logger.error(f"Training failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()