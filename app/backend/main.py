from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
from pathlib import Path
import pandas as pd
import numpy as np

from ml.feature_engineering import build_player_features
from ml.data_loader import load_players

app = FastAPI(title="PlayerLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = Path("models/playerlens_model.pkl")
IMPUTER_PATH = Path("models/imputer.pkl")

model = joblib.load(MODEL_PATH)
imputer = joblib.load(IMPUTER_PATH)

players_df = load_players()
features_df = build_player_features()

FEATURE_COLUMNS = (
    features_df
    .select_dtypes(include=["int64", "float64"])
    .columns
)

# ---------- POSITION ATTRIBUTES ----------
DEF_ATTRS = [
    "marking_mean",
    "standing_tackle_mean",
    "sliding_tackle_mean",
    "interceptions_mean"
]

MID_ATTRS = [
    "short_passing_mean",
    "vision_mean",
    "ball_control_mean",
    "stamina_mean"
]

ATT_ATTRS = [
    "finishing_mean",
    "positioning_mean",
    "dribbling_mean",
    "shot_power_mean"
]

# ---------- IMPACT BREAKDOWN (INTENDED ATTRS) ----------
ABILITY_BASE = [
    "ball_control_mean",
    "dribbling_mean",
    "short_passing_mean",
    "long_passing_mean",
    "vision_mean",
    "finishing_mean"
]

PHYSICAL_BASE = [
    "stamina_mean",
    "strength_mean",
    "acceleration_mean",
    "sprint_speed_mean",
    "jumping_mean"
]

CONSISTENCY_BASE = [
    "reactions_mean",
    "positioning_mean",
    "balance_mean",
    "composure_mean"  # optional, may not exist
]

def existing(cols):
    return [c for c in cols if c in features_df.columns]

ABILITY_ATTRS = existing(ABILITY_BASE)
PHYSICAL_ATTRS = existing(PHYSICAL_BASE)
CONSISTENCY_ATTRS = existing(CONSISTENCY_BASE)

@app.get("/")
def root():
    return {"message": "PlayerLens API is running"}

@app.get("/players")
def list_players():
    return (
        features_df[["player_api_id", "player_name"]]
        .sort_values("player_name")
        .to_dict(orient="records")
    )


@app.get("/player/{player_id}")
def get_player(player_id: int):
    row = features_df[features_df["player_api_id"] == player_id]

    if row.empty:
        return {"error": "Player not found"}

    X = row[FEATURE_COLUMNS]
    X_imputed = imputer.transform(X)
    impact_score = float(model.predict(X_imputed)[0])

    # ---------- POSITION ----------
    def_score = row[DEF_ATTRS].mean(axis=1).values[0]
    mid_score = row[MID_ATTRS].mean(axis=1).values[0]
    att_score = row[ATT_ATTRS].mean(axis=1).values[0]

    position = max(
        {
            "Defender": def_score,
            "Midfielder": mid_score,
            "Forward": att_score
        },
        key=lambda k: {
            "Defender": def_score,
            "Midfielder": mid_score,
            "Forward": att_score
        }[k]
    )

    # ---------- IMPACT BREAKDOWN ----------
    ability = float(row[ABILITY_ATTRS].mean(axis=1).values[0])
    physical = float(row[PHYSICAL_ATTRS].mean(axis=1).values[0])
    consistency = float(row[CONSISTENCY_ATTRS].mean(axis=1).values[0])

    # ---------- CONTRIBUTING ATTRIBUTES ----------
    contributions = np.abs(model.coef_ * X_imputed[0])

    contrib_df = pd.DataFrame({
        "attribute": FEATURE_COLUMNS,
        "contribution": contributions
    }).sort_values(by="contribution", ascending=False)

    top_attributes = (
        contrib_df
        .head(5)["attribute"]
        .str.replace("_mean", "")
        .tolist()
    )

    base_player = players_df[players_df["player_api_id"] == player_id].iloc[0]

    return {
        "player_id": int(player_id),
        "impact_score": impact_score,
        "position": position,
        "height": int(base_player["height"]) if not pd.isna(base_player["height"]) else None,
        "weight": int(base_player["weight"]) if not pd.isna(base_player["weight"]) else None,
        "impact_breakdown": {
            "ability": ability,
            "physical": physical,
            "consistency": consistency
        },
        "top_attributes": top_attributes
    }
