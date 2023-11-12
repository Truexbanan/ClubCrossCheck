import json
import glob

# Path to your json files
json_files_path = 'jsonteams/*.json'

# Create a new dictionary to hold all the teams
all_teams = {}

# Loop over the JSON files and merge them into the all_teams dictionary
for json_file in glob.glob(json_files_path):
    with open(json_file, 'r') as file:
        teams_data = json.load(file)
        # Assuming the top-level JSON structure is a dictionary with team names as keys
        for team, players in teams_data.items():
            if team in all_teams:
                # If the team already exists, extend the players list
                all_teams[team].extend(players)
            else:
                # If the team doesn't exist, add it to the dictionary
                all_teams[team] = players

# Remove duplicates from each team's list if necessary
for team, players in all_teams.items():
    all_teams[team] = list(set(players))

# Now, all_teams contains data from all the JSON files in the jsonteams folder

# Write the combined data to a new JSON file
with open('jsonteams/combined_teams.json', 'w', encoding='utf-8') as file:
    json.dump(all_teams, file, ensure_ascii=False, indent=4)