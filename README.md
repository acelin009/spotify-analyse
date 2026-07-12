# 🎵 Spotify Music Intelligence

**End-to-End Machine Learning Analytics Platform for Spotify Music Data**

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3.0-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**[🌐 Live Demo](https://spotify-analyse.streamlit.app/)**

![Dashboard Demo](images/app.png)

---

## Overview

Spotify Music Intelligence is an end-to-end data science platform that turns raw Spotify track data into actionable insights. It combines exploratory data analysis, predictive modeling, explainable AI, and an interactive Streamlit dashboard, built with production practices like modular code, CI/CD, and cloud deployment.

**Use cases:**
- Discover audio characteristics and patterns in modern music
- Analyze artist and genre performance over time
- Predict song popularity before release
- Understand which features drive commercial success

## Highlights

- ✅ End-to-end ML pipeline, from raw data to deployment
- ✅ Hyperparameter-tuned Random Forest model
- ✅ SHAP explainability for transparent predictions
- ✅ 6-page interactive Streamlit dashboard
- ✅ Automated testing + GitHub Actions CI/CD
- ✅ Live cloud deployment

## Dataset

**170,000+ tracks**, **34,000+ artists** from Spotify, with audio features and metadata.

| Feature | Description |
|---|---|
| `track_name`, `artist_name`, `track_id` | Track metadata |
| `popularity` | Score 0–100 (target variable) |
| `danceability`, `energy`, `valence` | Core audio characteristics (0–1) |
| `loudness` | Overall loudness (dB) |
| `acousticness`, `instrumentalness`, `speechiness`, `liveness` | Audio texture features (0–1) |
| `tempo` | Beats per minute |
| `duration_ms`, `genre`, `year` | Track length, genre, release year |

Source: [Kaggle – Spotify Tracks Dataset](https://www.kaggle.com/code/vatsalmavani/music-recommendation-system-using-spotify-dataset)

## Dashboard Pages

| Page | Purpose |
|---|---|
| 🏠 Home | Dataset KPIs and navigation |
| 📊 Overview | Popularity distribution, correlation heatmap, feature stats |
| 🎵 Song Explorer | Search tracks, radar chart of features, similar songs |
| 🎤 Artist Analytics | Career trajectory, feature profiles, related artists |
| 🎵 Genre Analytics | Genre comparison, distribution, evolution over time |
| 📈 Trends | Feature evolution from the 1960s to present |
| 🤖 Popularity Predictor | Real-time prediction with SHAP explanation |

## Machine Learning

Models evaluated: Linear Regression, Decision Tree, Random Forest, XGBoost.

| Model | MAE | RMSE | R² |
|---|---|---|---|
| Linear Regression | 16.74 | 21.36 | 0.24 |
| Decision Tree | 13.21 | 17.89 | 0.47 |
| **Random Forest** | **11.94** | **16.21** | **0.56** |
| XGBoost | 12.28 | 16.58 | 0.54 |

**Random Forest** was selected — best accuracy, robust to non-linearity, and interpretable via feature importance. Hyperparameter tuning via grid search improved MAE by 8%.

```python
best_params = {
    'n_estimators': 100,
    'max_depth': 12,
    'min_samples_split': 5,
    'min_samples_leaf': 2
}
```

### Explainable AI

Model transparency is provided through **SHAP**, showing global feature importance and per-prediction explanations.

**Top features driving popularity:**
1. Danceability — 23.4%
2. Energy — 18.7%
3. Valence — 15.2%
4. Loudness — 12.8%
5. Acousticness — 10.3%

Danceability shows the strongest positive impact on popularity; instrumentalness is negatively correlated, and feature effects are often non-linear.

## Pipeline

```
Raw Data → Cleaning → EDA → Feature Engineering → Model Training
   → Hyperparameter Tuning → SHAP Analysis → Streamlit Dashboard → Deployment
```

## Project Structure

```
spotify-music-intelligence/
├── .github/workflows/ci_cd.yml   # CI/CD pipeline
├── dashboard/                    # Streamlit app (app.py, pages/, components/)
├── data/                         # raw / processed / external datasets
├── models/                       # trained model, scaler, metadata
├── notebooks/                    # EDA, feature engineering, training, SHAP
├── src/                          # data, features, models, utils modules
├── tests/                        # unit tests
├── requirements.txt
├── Dockerfile
└── README.md
```

## Installation

```bash
git clone https://github.com/acelnaz/spotify-analyse.git
cd spotify-analyse

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Running Locally

```bash
# Launch dashboard
cd dashboard
streamlit run app.py          # opens at http://localhost:8501

# Train model
python src/models/train.py

# Run tests
pytest tests/ --cov=src
```

## Model Performance

| Metric | Value |
|---|---|
| R² Score | 0.56 |
| MAE | 11.94 |
| RMSE | 16.21 |
| MAPE | 15.8% |

5-fold cross-validation mean: **R² = 0.56, MAE = 11.91**

## CI/CD

GitHub Actions runs tests, linting, and model validation on every push/PR, and deploys to Streamlit Cloud on merges to `main`.

## Tech Stack

**Data & ML:** Pandas, NumPy, Scikit-learn, XGBoost, SHAP
**Visualization:** Plotly, Matplotlib, Seaborn
**Dashboard:** Streamlit
**DevOps:** GitHub Actions, Docker, Pytest, Flake8

## Deployment

Deployed via [Streamlit Cloud](https://share.streamlit.io) from the `dashboard/app.py` entry point.

```bash
docker build -t spotify-music-intelligence .
docker run -p 8501:8501 spotify-music-intelligence
```

## Roadmap

- Spotify API integration for real-time data
- Recommendation engine for similar songs
- Deep learning models for improved prediction
- REST API for programmatic access
- Mobile companion app

## License

Licensed under the [MIT License](LICENSE).

## Author

**Acelin Nazareth** — Data Scientist & Machine Learning Engineer

[GitHub](https://github.com/acelin009) · [LinkedIn](https://linkedin.com/in/acelin.nazareth) · [Email](mailto:acelin.nazareth@email.com)

---

⭐ If you find this project useful, consider starring the repo.
