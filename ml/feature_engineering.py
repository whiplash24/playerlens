import pandas as pd
from ml.data_loader import load_players, load_player_attributes


def build_player_features():
    players = load_players()
    attrs = load_player_attributes()

    # Keep only numeric attributes
    numeric_attrs = attrs.select_dtypes(include=["int64", "float64"])

    # Aggregate attributes per player
    agg_attrs = numeric_attrs.groupby(attrs["player_api_id"]).agg(
        ["mean", "std"]
    )

    # Flatten column names
    agg_attrs.columns = [
        f"{col[0]}_{col[1]}" for col in agg_attrs.columns
    ]
    agg_attrs.reset_index(inplace=True)

    # Merge with player profile
    features = players.merge(
        agg_attrs,
        left_on="player_api_id",
        right_on="player_api_id",
        how="inner"
    )

    return features
