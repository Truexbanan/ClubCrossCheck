import requests
from bs4 import BeautifulSoup

def get_players(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'
    }

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Use the correct CSS selector to find all player names
        # This selector targets "a" tags inside "td" tags with the class "hell" and "dunkel"
        player_links = soup.select('td.hell a, td.dunkel a')
        print(f"Number of player links found: {len(player_links)}")

        # Extract and print the player names
        for link in player_links:
            print(link.get_text())
        
        # Check for a 'next' link and if found, call `get_players` recursively
        next_link = soup.find('a', string='Next »')
        if next_link and 'href' in next_link.attrs:
            next_url = next_link.attrs['href']
            print(f"Fetching next page: {next_url}")
            get_players(next_url)
    else:
        print(f"Failed to retrieve content, status code: {response.status_code}")

# Starting URL of the team's player list page
start_url = 'https://www.worldfootball.net/teams/liverpool-fc/'
get_players(start_url)