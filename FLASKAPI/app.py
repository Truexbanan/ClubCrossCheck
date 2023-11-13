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

#this html style shits fucking lame 

@app.route('/select_teams')
def select_teams():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Soccer Data Project</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary-color: #8FA880; /* Sage green */
                --secondary-color: #3D5A80; /* Deep blue */
                --accent-color: #E09F3E; /* Muted orange */
                --background-color: #F4F4F4; /* Off-white */
            }
            body {
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                background-color: var(--background-color);
                color: var(--secondary-color);
            }
            header {
                background: var(--primary-color);
                color: white;
                text-align: center;
                padding: 1em 0;
                margin-bottom: 2em;
            }
            section {
                width: 80%;
                margin: 0 auto;
                padding: 2em; 
                background: white;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                position: relative;
            }

            form {
                 display: flex;
                 flex-direction: column;
                 margin-bottom: 20px; /* You can increase this margin to add more space below the form */
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
            button {
                padding: 10px 15px;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 1em;
            }
            button:hover, input[type="submit"]:hover {
                background-color: #006644; /* Darkened primary color */
            }
          button, input[type="submit"] {
    padding: 12px 20px;
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: 25px; /* Rounded buttons */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    transition: background-color 0.3s, box-shadow 0.3s; /* Smooth transition for hover effect */
}
            input[type="submit"]:hover {
                background: #006644;
            }
            h1, h2, h3, h4 {
                font-family: 'Lato', sans-serif;
                font-weight: 700;
            }
            .leagues-container {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                justify-content: space-between;
                margin-top: 20px;
            }
            .league-box {
                flex: 1 1 18%; /* Adjusted the flex-basis to ensure that the boxes have some space between them */
                padding: 20px; /* Increased padding inside each box */
                background-color: #f2f2f2;
                border-radius: 8px;
                margin-bottom: 20px; /* Increased margin for more space between boxes */
                max-height: 400px;
                overflow-y: auto;
            }
            .league-box h4 {
             margin: 0 0 20px 0; /* Add more space below headings */
            }
            .league-box ul {
                list-style-type: none;
                p adding: 0;
                margin: 0;
                font-size: 0.9em;
                height: 340px;
                overflow-y: auto;
            }

            .league-box ul li {
                margin: 10px 0; 
                padding: 10px; 
                border-bottom: 1px solid #ddd;
            }
            @media (max-width: 768px) {
                .leagues-container {
                    flex-direction: column;
                    align-items: center;
                }
                .league-box {
                    flex-basis: 90%;
                    margin-bottom: 20px;
                }
            }
        </style>
        <script>
            function addTeamInput() {
                var container = document.getElementById("team-inputs");
                var newLabel = document.createElement("label");
                newLabel.innerHTML = "Team " + (container.childElementCount / 2 + 1) + ":";
                container.appendChild(newLabel);
                var newInput = document.createElement("input");
                newInput.type = "text";
                newInput.name = "team[]";
                newInput.required = true;
                container.appendChild(newInput);
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
            <div class="leagues-container">
                <div class="league-box">
    <h4>Premier League</h4>
    <ul>
        <li>arsenal-fc</li>
        <li>afc-bournemouth</li>
        <li>aston-villa</li>
        <li>brentford-fc</li>
        <li>brighton-hove-albion</li>
        <li>burnley-fc</li>
        <li>chelsea-fc</li>
        <li>crystal-palace</li>
        <li>everton-fc</li>
        <li>fulham-fc</li>
        <li>liverpool-fc</li>
        <li>luton-town</li>
        <li>manchester-city</li>
        <li>newcastle-united</li>
        <li>manchester-united</li>
        <li>nottingham-forest</li>
        <li>sheffield-united</li>
        <li>tottenham-hotspur</li>
        <li>west-ham-united</li>
        <li>wolverhampton-wanderers</li>
    </ul>
</div>

<div class="league-box">
    <h4>LaLiga</h4>
    <ul>
        <li>athletic-bilbao</li>
        <li>atletico-madrid</li>
        <li>ca-osasuna</li>
        <li>cadiz-cf</li>
        <li>cd-alaves</li>
        <li>celta-vigo</li>
        <li>fc-barcelona</li>
        <li>getafe-cf</li>
        <li>girona-fc</li>
        <li>granada-cf</li>
        <li>rayo-vallecano</li>
        <li>rcd-mallorca</li>
        <li>real-betis</li>
        <li>real-madrid</li>
        <li>real-sociedad</li>
        <li>sevilla-fc</li>
        <li>ud-almeria</li>
        <li>ud-las-palmas</li>
        <li>valencia-cf</li>
        <li>villarreal-cf</li>
    </ul>
</div>

<div class="league-box">
    <h4>Serie A</h4>
    <ul>
        <li>ac-milan</li>
        <li>ac-monza</li>
        <li>acf-fiorentina</li>
        <li>as-roma</li>
        <li>atalanta</li>
        <li>bologna-fc</li>
        <li>cagliari-calcio</li>
        <li>empoli-fc</li>
        <li>frosinone-calcio</li>
        <li>genoa-cfc</li>
        <li>hellas-verona</li>
        <li>inter</li>
        <li>juventus</li>
        <li>lazio-roma</li>
        <li>sassuolo-calcio</li>
        <li>ssc-napoli</li>
        <li>torino-fc</li>
        <li>udinese-calcio</li>
        <li>us-lecce</li>
        <li>us-salernitana-1919</li>
    </ul>
</div>

<div class="league-box">
    <h4>Bundesliga</h4>
    <ul>
        <li>1-fc-heidenheim-1846</li>
        <li>1-fc-koeln</li>
        <li>1-fc-union-berlin</li>
        <li>1-fsv-mainz-05</li>
        <li>1899-hoffenheim</li>
        <li>bayer-leverkusen</li>
        <li>bayern-muenchen</li>
        <li>bor-moenchengladbach</li>
        <li>borussia-dortmund</li>
        <li>eintracht-frankfurt</li>
        <li>fc-augsburg</li>
        <li>rb-leipzig</li>
        <li>sc-freiburg</li>
        <li>sv-darmstadt-98</li>
        <li>vfb-stuttgart</li>
        <li>vfl-bochum</li>
        <li>vfl-wolfsburg</li>
        <li>werder-bremen</li>
            </div>
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
        :root {{
            --primary-color: #8FA880; /* Sage green */
            --secondary-color: #3D5A80; /* Deep blue */
            --accent-color: #E09F3E; /* Muted orange */
            --background-color: #F4F4F4; /* Off-white */
        }}
        body {{
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
            background-color: var(--background-color);
            color: var(--secondary-color);
        }}
        header {{
            background: var(--primary-color);
            color: white;
            text-align: center;
            padding: 1em 0;
        }}
        section {{
            width: 80%;
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
            color: var(--secondary-color);
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
            background-color: var(--primary-color);
            border: none;
            border-radius: 4px; /* Match border-radius with select_teams page */
            margin: 20px auto;
            font-weight: bold;
            transition: background-color 0.3s; /* Smooth transition for hover effect */
        }}
        .button:hover {{
            background-color: darken(var(--primary-color), 10%); /* Darken button color on hover */
        }}
        @media (max-width: 768px) {{
            section {{
                width: 90%;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>Common Players</h1>
    </header>
    <section>
        <h2>Players who have played for {team_names}</h2>
        {player_list_html}
        <a href="/select_teams" class="button">Select New Teams</a>
    </section>
</body>
</html>
'''
    return render_template_string(html)


if __name__ == '__main__':
    app.run(debug=True)