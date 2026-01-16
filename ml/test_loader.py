from data_loader import load_players, load_matches

players = load_players()
matches = load_matches()

print(players.shape)
print(matches.shape)
