import json

# Assuming the JSON data is saved in a file named 'teamPlayers.json'
with open('teamPlayers.json', 'r') as file:
    team_players = json.load(file)


for key, value in team_players.items():
    print(f"{key}: {value}")
