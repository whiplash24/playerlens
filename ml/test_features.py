from feature_engineering import build_player_features

df = build_player_features()
print(df.shape)
print(df.head())
