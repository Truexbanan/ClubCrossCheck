from flask import Flask, request, render_template_string
import json

app = Flask(__name__)

def load_data():
    try:
        with open('combined_teams.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file is not found

def find_common_players(teams):
    data = load_data()
    common_players = set(data.get(teams[0], []))  # Initialize with the first team's players

    for team in teams[1:]:
        team_players = set(data.get(team, []))
        common_players.intersection_update(team_players)

    return sorted(list(common_players))

@app.route('/')
def home():
    return "Welcome to the Soccer Data Project!"

@app.route('/select_teams')
def select_teams():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Soccer Data Project</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #e9ecef;
                color: #495057;
            }
            header {
                background: #007bff;
                color: white;
                text-align: center;
                padding: 1em 0;
                margin-bottom: 2em;
            }
            section {
                width: 50%;
                margin: 0 auto;
                padding: 2em;
                background: white;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
            }
            form {
                display: flex;
                flex-direction: column;
            }
            label {
                margin-bottom: .5em;
                font-weight: bold;
            }
            input[type="text"] {
                padding: 8px;
                margin-bottom: 1em;
                border-radius: 4px;
                border: 1px solid #ced4da;
            }
            input[type="submit"] {
                padding: 10px 15px;
                background: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
            }
            input[type="submit"]:hover {
                background: #218838;
            }
        </style>
        <script>
            function addTeamInput() {
                var container = document.getElementById("team-inputs");
                var count = container.children.length / 2 + 1; // Adjusted to account for label and input pairs
                var label = document.createElement("label");
                label.htmlFor = "team" + count;
                label.textContent = "Team " + count + ":";
                container.appendChild(label);

                var input = document.createElement("input");
                input.type = "text";
                input.name = "team[]";
                input.id = "team" + count;
                input.required = true;
                container.appendChild(input);
            }
        </script>
    </head>
    <body>
        <header>
            <h1>Soccer Data Project</h1>
        </header>
        <section>
            <form action="/show_common_players" method="post">
                <div id="team-inputs">
                    <label for="team1">Team 1:</label>
                    <input type="text" id="team1" name="team[]" required>
                    <label for="team2">Team 2:</label>
                    <input type="text" id="team2" name="team[]" required>
                </div>
                <button type="button" onclick="addTeamInput()">Add Another Team</button>
                <input type="submit" value="Find Common Players">
            </form>
        </section>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/show_common_players', methods=['POST'])
def show_common_players():
    teams = request.form.getlist('team[]')
    common_players = find_common_players(teams)

    team_names = ", ".join(teams)  # Joining team names into a single string
    player_list_html = "<ul>" + "".join([f"<li>{player}</li>" for player in common_players]) + "</ul>" if common_players else "<p>No common players found.</p>"

    html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Common Players</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #e9ecef;
            color: #495057;
        }}
        header {{
            background: #007bff;
            color: white;
            text-align: center;
            padding: 1em 0;
        }}
        section {{
            width: 50%;
            margin: 20px auto;
            text-align: center;
            background: white;
            padding: 2em;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        ul {{
            list-style-type: none;
            padding: 0;
        }}
        li {{
            background: #f8f9fa;
            margin: 5px 0;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #ced4da;
            list-style-position: inside;
        }}
        p {{
            color: #495057;
        }}
        .button {{
            display: block;
            width: auto;
            padding: 10px 15px;
            font-size: 16px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            outline: none;
            color: white;
            background-color: #007bff;
            border: none;
            border-radius: 8px;
            margin: 20px auto;
            font-weight: bold;
        }}
        .button:hover {{
            background-color: #0056b3;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Common Players</h1>
    </header>
    <section>
        <h2>Players who have played for {team_names}</h2>  <!-- Update this line -->
        {player_list_html}
        <a href="/select_teams" class="button">Select New Teams</a>
    </section>
</body>
</html>
'''
    return render_template_string(html)


if __name__ == '__main__':
    app.run(debug=True)