import os
from flask import Flask, get_flashed_messages, request, render_template_string, redirect, url_for, flash
import json


app = Flask(__name__)
app.secret_key = os.urandom(24)


#these arrays are used for code in select_teams in regards to renaming them to more user friendly options ( not important for main code)
premier_league_teams = [
    'arsenal-fc', 'afc-bournemouth', 'aston-villa', 'brentford-fc', 'brighton-hove-albion', 'burnley-fc',
    'chelsea-fc', 'crystal-palace', 'everton-fc', 'fulham-fc', 'liverpool-fc', 'luton-town',
    'manchester-city', 'newcastle-united', 'manchester-united', 'nottingham-forest', 'sheffield-united',
    'tottenham-hotspur', 'west-ham-united', 'wolverhampton-wanderers'
]

la_liga_teams = [
    'athletic-bilbao', 'atletico-madrid', 'ca-osasuna', 'cadiz-cf', 'cd-alaves', 'celta-vigo', 
    'fc-barcelona', 'getafe-cf', 'girona-fc', 'granada-cf', 'rayo-vallecano', 'rcd-mallorca', 
    'real-betis', 'real-madrid', 'real-sociedad', 'sevilla-fc', 'ud-almeria', 'ud-las-palmas', 
    'valencia-cf', 'villarreal-cf'
]

serie_a_teams = [
    'ac-milan', 'ac-monza', 'acf-fiorentina', 'as-roma', 'atalanta', 'bologna-fc', 'cagliari-calcio', 
    'empoli-fc', 'frosinone-calcio', 'genoa-cfc', 'hellas-verona', 'inter', 'juventus', 'lazio-roma', 
    'sassuolo-calcio', 'ssc-napoli', 'torino-fc', 'udinese-calcio', 'us-lecce', 'us-salernitana-1919'
]

bundesliga_teams = [
    '1-fc-heidenheim-1846', '1-fc-koeln', '1-fc-union-berlin', '1-fsv-mainz-05', '1899-hoffenheim', 
    'bayer-leverkusen', 'bayern-muenchen', 'bor-moenchengladbach', 'borussia-dortmund', 'eintracht-frankfurt', 
    'fc-augsburg', 'rb-leipzig', 'sc-freiburg', 'sv-darmstadt-98', 'vfb-stuttgart', 'vfl-bochum', 'vfl-wolfsburg', 
    'werder-bremen'
]



#this is for trying to make application more user friendly so user can enter example "arsenal" instead of the exact "arsenal-fc"
def format_team_name(team_identifier):
    words = team_identifier.replace('-', ' ').split()
    words = [word.capitalize() for word in words if word.lower() not in ['fc', 'cd', 'ac', 'sc', 'ssc', 'ud', 'us']]
    return ' '.join(words)

#maps the teams to team_identifier
def create_team_mapping():
    # the french teams are in the json file but not included on website. However user can still enter the french teams.
    # french teams not included due to style issues. 
    team_identifiers = [
    'arsenal-fc', 'afc-bournemouth', 'aston-villa', 'brentford-fc', 'brighton-hove-albion', 'burnley-fc',
    'chelsea-fc', 'crystal-palace', 'everton-fc', 'fulham-fc', 'liverpool-fc', 'luton-town',
    'manchester-city', 'newcastle-united', 'manchester-united', 'nottingham-forest', 'sheffield-united',
    'tottenham-hotspur', 'west-ham-united', 'wolverhampton-wanderers', 'athletic-bilbao', 'atletico-madrid',
    'ca-osasuna', 'cadiz-cf', 'cd-alaves', 'celta-vigo', 'fc-barcelona', 'getafe-cf', 'girona-fc', 'granada-cf',
    'rayo-vallecano', 'rcd-mallorca', 'real-betis', 'real-madrid', 'real-sociedad', 'sevilla-fc', 'ud-almeria',
    'ud-las-palmas', 'valencia-cf', 'villarreal-cf', 'ac-milan', 'ac-monza', 'acf-fiorentina', 'as-roma', 'atalanta',
    'bologna-fc', 'cagliari-calcio', 'empoli-fc', 'frosinone-calcio', 'genoa-cfc', 'hellas-verona', 'inter', 'juventus',
    'lazio-roma', 'sassuolo-calcio', 'ssc-napoli', 'torino-fc', 'udinese-calcio', 'us-lecce', 'us-salernitana-1919',
    '1-fc-heidenheim-1846', '1-fc-koeln', '1-fc-union-berlin', '1-fsv-mainz-05', '1899-hoffenheim', 'bayer-leverkusen',
    'bayern-muenchen', 'bor-moenchengladbach', 'borussia-dortmund', 'eintracht-frankfurt', 'fc-augsburg', 'rb-leipzig',
    'sc-freiburg', 'sv-darmstadt-98', 'vfb-stuttgart', 'vfl-bochum', 'vfl-wolfsburg', 'werder-bremen', 'as-monaco',
    'clermont-foot-63', 'fc-lorient', 'fc-metz', 'fc-nantes', 'havre-ac', 'lille-osc', 'montpellier-hsc', 'ogc-nice',
    'olympique-lyon', 'olympique-marseille', 'paris-saint-germain', 'rc-lens', 'rc-strasbourg', 'stade-brestois',
    'stade-reims', 'stade-rennais', 'toulouse-fc'
    ]
    
    return {format_team_name(team): team for team in team_identifiers}

# Global variable for team name to identifier mapping
team_name_to_identifier = create_team_mapping()


def load_data():
    try:
        with open('combined_teams.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file is not found

def find_common_players(teams):
    data = load_data()
    # Map user-friendly team names back to identifiers
    team_identifiers = [team_name_to_identifier.get(team, team) for team in teams]

    common_players = set(data.get(team_identifiers[0], []))

    for team in team_identifiers[1:]:
        team_players = set(data.get(team, []))
        common_players.intersection_update(team_players)

    return sorted(list(common_players))

#does nothing might expand on it later
@app.route('/')
def home():
    return "Welcome to the Soccer Data Project!"



# main page - user selects teams
@app.route('/select_teams')
def select_teams():

    # user friendly names
    formatted_premier_league = [format_team_name(team) for team in premier_league_teams]
    formatted_la_liga = [format_team_name(team) for team in la_liga_teams]
    formatted_serie_a = [format_team_name(team) for team in serie_a_teams]
    formatted_bundesliga = [format_team_name(team) for team in bundesliga_teams]
    formatted_teams = [format_team_name(team) for team in team_name_to_identifier.values()]

    #HTML styling and basic front end html
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
            .github-link {
                position: absolute; /* Position the link absolutely relative to its parent */
                top: 10px; 
                right: 10px; 
                padding: 10px 15px;
                font-size: 1rem;
                font-weight: bold;
                color: white;
                background-color: #6E7F80; /* Subtle background color */
                border-radius: 5px;
                text-decoration: none;
                transition: background-color 0.2s, transform 0.2s;
            }

            .github-link:hover {
                background-color: #536872; /* Slightly darker shade on hover */
                transform: translateY(-2px);
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
            <a href="https://github.com/Truexbanan/SoccerClubsProject" target="_blank" class="github-link">Click to view on GitHub</a>
        </header>
        <section>
            {% if error %}
            <div style="color: red; text-align: center;">
            {{ error }}
            </div>
            {% endif %}
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
        ''' + '\n'.join(f'<li>{team}</li>' for team in formatted_premier_league) + '''
    </ul>
</div>

<div class="league-box">
    <h4>LaLiga</h4>
    <ul>
       ''' + '\n'.join(f'<li>{team}</li>' for team in formatted_la_liga) + '''
    </ul>
</div>

<div class="league-box">
    <h4>Serie A</h4>
    <ul>
       ''' + '\n'.join(f'<li>{team}</li>' for team in formatted_serie_a) + '''
    </ul>
</div>

<div class="league-box">
    <h4>Bundesliga</h4>
    <ul>
       ''' + '\n'.join(f'<li>{team}</li>' for team in formatted_bundesliga) + '''
    </ul>
            </div>
        </section>
    </body>
    </html>
    '''

    # if user enters invalid team name

    messages = get_flashed_messages(category_filter=['error'])
    error_message = messages[0] if messages else ""
    
    return render_template_string(html, teams=formatted_teams, error=error_message)

 
 
@app.route('/show_common_players', methods=['POST'])
def show_common_players():
    teams = request.form.getlist('team[]')
    # Normalize input: strip whitespace and convert to title case
    normalized_teams = [team.strip().title() for team in teams]

    # Validate team names
    # if not valid go back to /select_teams and flash error message in HTML code
    invalid_teams = [team for team in normalized_teams if team not in team_name_to_identifier]
    if invalid_teams:
        flash(f"Invalid team name(s): {', '.join(invalid_teams)}. Please check spelling and try again. (teams listed below)", 'error')
        return redirect(url_for('select_teams'))


    # Convert user-friendly names to original identifiers
    team_identifiers = [team_name_to_identifier.get(team, team) for team in normalized_teams]
    common_players = find_common_players(team_identifiers)
    display_team_names = [format_team_name(team) for team in team_identifiers]
    team_names = ", ".join(display_team_names)  # This uses user-friendly names
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
           background: #006644;
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