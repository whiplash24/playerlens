import numpy as np

def compute_impact_score(df):
    ability_cols = [
        "overall_rating_mean",
        "ball_control_mean",
        "short_passing_mean",
        "long_passing_mean",
        "dribbling_mean",
        "standing_tackle_mean",
        "sliding_tackle_mean",
        "finishing_mean",
    ]

    consistency_cols = [
        "overall_rating_std"
    ]

    physical_cols = [
        "stamina_mean",
        "strength_mean",
        "balance_mean"
    ]

    ability_score = df[ability_cols].mean(axis=1)
    consistency_penalty = df[consistency_cols].fillna(0).mean(axis=1)
    physical_score = df[physical_cols].mean(axis=1)

    impact_score = (
        0.6 * ability_score +
        0.25 * physical_score -
        0.15 * consistency_penalty
    )

    return impact_score
