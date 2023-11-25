# Club Cross-Check

## Project Overview

Club Cross-Check is an innovative full-stack web application designed to connect soccer enthusiasts with detailed information about players who have played for multiple clubs in Europe's top four leagues: Bundesliga (Germany), Premier League (England), La Liga (Spain), and Serie A (Italy). This tool is invaluable for fans, researchers, and journalists alike, offering a unique perspective on player careers across these competitive leagues.

## Key Features

- **Comprehensive Data Collection:** Automated web scraping from [worldfootball.net](https://www.worldfootball.net) to compile an extensive database of players.
- **Multi-League Integration:** Covers Germany's Bundesliga, England's Premier League, Spain's La Liga, and Italy's Serie A.
- **Player Cross-Reference:** Ability to select multiple clubs and view a list of players who have played for each of them.
- **User-Friendly Interface:** Simple, intuitive web UI for selecting teams and displaying results.

## Technologies Used

- **Web Scraping:** JavaScript (Puppeteer) for data extraction, initially attempted with Python's BeautifulSoup.
- **Backend Development:** Python with Flask, handling data processing and server-side logic.
- **Frontend Development:** HTML, CSS, and JavaScript for building the user interface.
- **Data Storage:** JSON files used for storing scraped data.
- **Hosting and Deployment:** AWS EC2 for hosting, with Route 53 for domain management.

## How It Works

### Data Scraping and Processing

- **Web Scraping Scripts:**
  - Four JavaScript scripts, one for each league, scrape player data from team pages.
  - Utilizes Puppeteer for navigating and extracting data from web pages.
  - Each script generates a JSON file containing team names and associated players.

- **Data Aggregation:**
  - A Python script consolidates these JSON files into a single file, creating a unified database of approximately 68,000 players.

### Backend Development

- **Flask Application:**
  - Manages routing and server-side logic.
  - Includes endpoints for team selection and displaying common players.

- **Data Handling:**
  - The Flask app reads the combined JSON file to serve player data.
  - Implements functions to identify common players among selected teams.

### Frontend Interface

- **Dynamic Web Pages:**
  - Users select teams via a clean, responsive web interface.
  - Interactive elements allow the addition of more teams to the query.

- **Results Display:**
  - The application displays a list of players common to the selected teams.
  - Offers a user-friendly format, including team names and player lists.

### Deployment on AWS

- **AWS EC2 Instance:**
  - The Flask application is hosted on an Ubuntu server on AWS EC2.
  - Gunicorn serves as the WSGI HTTP server to handle requests.

- **Nginx Integration:**
  - Nginx acts as a reverse proxy, routing requests to the Gunicorn server.
  - Ensures efficient handling of web traffic and enhances security.

- **Domain Management:**
  - AWS Route 53 is used for domain name management, linking to the EC2 server.

## Accessing the Application

Visit [Club Cross Check](http://clubcrosscheck.com/) to explore the application. Select teams from the provided lists and discover players who have shared their talents across these top European clubs.

## Feedback and Contributions

We welcome your feedback and contributions. Please visit our [GitHub repository](https://github.com/Truexbanan/SoccerClubsProject) for more information on contributing to the project, reporting issues, or suggesting improvements.

## License

This project is licensed under the MIT License - see the LICENSE file in the GitHub repository for details.
