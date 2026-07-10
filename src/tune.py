"""
Test script for hyperparameter tuning module.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).resolve().parent))

try:
    print("Testing tune.py imports...")
    from src.tune import (
        GRID_SEARCH_SPACE,
        RANDOM_SEARCH_SPACE,
        QUICK_SEARCH_SPACE,
        perform_grid_search,
        perform_random_search,
        save_search_results,
        evaluate_best_model,
        compare_with_baseline,
        main
    )
    print("✅ All imports successful!")

    print(f"✅ Grid Search Space: {len(GRID_SEARCH_SPACE)} parameters")
    print(f"✅ Random Search Space: {len(RANDOM_SEARCH_SPACE)} parameters")
    print(f"✅ Quick Search Space: {len(QUICK_SEARCH_SPACE)} parameters")

    print("\n✅ test_tune.py completed successfully!")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please check your file structure and imports.")