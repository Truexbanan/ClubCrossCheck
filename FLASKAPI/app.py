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

def find_common_players(team1, team2):
    data = load_data()
    team1_players = set(data.get(team1, []))
    team2_players = set(data.get(team2, []))
    # Sort the common players in alphabetical order before returning
    return sorted(list(team1_players.intersection(team2_players)))

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
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }
            header { background: #333; color: white; text-align: center; padding: 1em 0; }
            section { width: 80%; margin: 20px auto; }
            form { background: white; padding: 20px; border-radius: 8px; }
            label { margin-top: 10px; display: block; }
            input[type="text"] { width: 100%; padding: 8px; margin: 10px 0; border-radius: 4px; border: 1px solid #ddd; }
            input[type="submit"] { background: #28a745; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }
            input[type="submit"]:hover { background: #218838; }
        </style>
    </head>
    <body>
        <header>
            <h1>Welcome to the Soccer Data Project</h1>
        </header>
        <section>
            <form action="/show_common_players" method="post">
                <label for="team1">Team 1:</label>
                <input type="text" id="team1" name="team1"><br>
                <label for="team2">Team 2:</label>
                <input type="text" id="team2" name="team2"><br>
                <input type="submit" value="Find Common Players">
            </form>
        </section>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/show_common_players', methods=['POST'])
def show_common_players():
    team1 = request.form['team1']
    team2 = request.form['team2']
    common_players = find_common_players(team1, team2)

    player_list_html = "<ul>" + "".join([f"<li>{player}</li>" for player in common_players]) + "</ul>" if common_players else "<p>No common players found.</p>"

    html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Common Players</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }}
        header {{
            background: #333;
            color: white;
            text-align: center;
            padding: 1em 0;
        }}
        section {{
            width: 80%;
            margin: 20px auto;
            text-align: center;
        }}
        ul {{
            list-style-type: none;
            padding: 0;
        }}
        li {{
            background: white;
            margin: 5px 0;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #ddd;
        }}
        p {{
            color: #333;
        }}
        .button {{
            display: inline-block;
            padding: 10px 15px;
            font-size: 16px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            outline: none;
            color: #fff;
            background-color: #4CAF50;
            border: none;
            border-radius: 15px;
            box-shadow: 0 9px #999;
        }}
        .button:hover {{background-color: #3e8e41}}
        .button:active {{
            background-color: #3e8e41;
            box-shadow: 0 5px #666;
            transform: translateY(4px);
        }}
    </style>
</head>
<body>
    <header>
        <h1>Common Players</h1>
    </header>
    <section>
        <h2>Players who have played for both {team1} and {team2}</h2>
        {player_list_html}
        <button class="button" onclick="window.location.href='/select_teams';">Select New Teams</button>
    </section>
</body>
</html>
'''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)