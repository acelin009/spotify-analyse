from src.model import predict_popularity

sample_song = {
    "danceability": 0.72,
    "energy": 0.81,
    "key": 5,
    "loudness": -5.3,
    "mode": 1,
    "speechiness": 0.05,
    "acousticness": 0.15,
    "instrumentalness": 0.0,
    "liveness": 0.11,
    "valence": 0.64,
    "tempo": 120.5,
    "duration_ms": 210000,
    "explicit": 0,
    "year": 2023
}

prediction = predict_popularity(sample_song)

print(f"Predicted Popularity: {prediction:.2f}")