from data_loader import load_players, load_matches, load_player_attributes

players = load_players()
matches = load_matches()
attrs = load_player_attributes()

print("PLAYERS")
print(players.columns)
print(players.shape)

print("\nMATCHES")
print(matches.columns)
print(matches.shape)

print("\nPLAYER ATTRIBUTES")
print(attrs.columns)
print(attrs.shape)
