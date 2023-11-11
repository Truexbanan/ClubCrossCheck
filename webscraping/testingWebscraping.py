import json

# Load the first JSON file
with open('jsonFolder/premierLeague.json', 'r') as file:
    Prem_teams = json.load(file)

# Load the second JSON file
with open('jsonFolder/LaLiga.json', 'r') as file:
    LaLiga_teams = json.load(file)

# Create a new dictionary that contains all teams
all_teams = {}

# Add the premier league teams to the all_teams dictionary
all_teams.update(Prem_teams)

# Add the new teams to the all_teams dictionary
# This won't affect premier_league_teams dictionary
all_teams.update(LaLiga_teams)

# Now, all_teams contains data from both JSON files

arsenal_fc_data = all_teams.get('arsenal-fc', None)

for item in arsenal_fc_data:
    print(item)
