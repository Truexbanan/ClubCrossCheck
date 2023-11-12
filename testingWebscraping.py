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
        all_teams.update(teams_data)  # Merge the data

# Now, all_teams contains data from all the JSON files in the jsonteams folder