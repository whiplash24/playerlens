from fastapi import FastAPI
import joblib
import pandas as pd
from pathlib import Path

from ml.feature_engineering import build_player_features

app = FastAPI(title="PlayerLens API")

MODEL_PATH = Path("models/playerlens_model.pkl")
IMPUTER_PATH = Path("models/imputer.pkl")

model = joblib.load(MODEL_PATH)
imputer = joblib.load(IMPUTER_PATH)

@app.get("/")
def root():
    return {"message": "PlayerLens API is running"}

@app.get("/players")
def list_players():
    df = build_player_features()
    return df[["player_api_id", "player_name"]].head(50).to_dict(orient="records")

@app.get("/player/{player_id}")
def get_player_impact(player_id: int):
    df = build_player_features()
    player = df[df["player_api_id"] == player_id]

    if player.empty:
        return {"error": "Player not found"}

    X = player.select_dtypes(include=["int64", "float64"])
    X_imputed = imputer.transform(X)
    score = model.predict(X_imputed)[0]

    return {
        "player_id": player_id,
        "impact_score": float(score)
    }
