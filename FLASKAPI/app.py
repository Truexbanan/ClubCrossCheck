from flask import Flask, request
import json

app = Flask(__name__)

def load_data():
    with open('combined_teams.json', 'r') as file:
        data = json.load(file)
    return data

def find_common_players(team1, team2):
    data = load_data()
    # Assuming data is structured as a dictionary of teams with player lists
    team1_players = set(data.get(team1, []))
    team2_players = set(data.get(team2, []))
    return list(team1_players.intersection(team2_players))

@app.route('/')
def home():
    return "Welcome to the Soccer Data Project!"

@app.route('/select_teams')
def select_teams():
    return '''<form action="/show_common_players" method="post">
                  Team 1: <input type="text" name="team1"><br>
                  Team 2: <input type="text" name="team2"><br>
                  <input type="submit" value="Find Common Players">
              </form>'''

@app.route('/show_common_players', methods=['POST'])
def show_common_players():
    team1 = request.form['team1']
    team2 = request.form['team2']
    common_players = find_common_players(team1, team2)
    return f"Common Players: {', '.join(common_players)}"

if __name__ == '__main__':
    app.run(debug=True)