from feature_engineering import build_player_features
from model import compute_impact_score

def prepare_training_data():
    df = build_player_features()
    df["impact_score"] = compute_impact_score(df)
    return df

if __name__ == "__main__":
    df = prepare_training_data()
    print(df[["player_name", "impact_score"]].head())
