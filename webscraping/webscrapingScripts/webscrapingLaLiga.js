const puppeteer = require('puppeteer');
const fs = require('fs'); // Import the File System module

(async () => {
    const browser = await puppeteer.launch({
        headless: false, // Set to true if you don't need to see the browser GUI
    });
    const page = await browser.newPage();
    
    const teams = ['athletic-bilbao', 'atletico-madrid','ca-osasuna',
                    'cadiz-cf', 'cd-alaves', 'celta-vigo',
                    'fc-barcelona', 'getafe-cf' , 'girona-fc',
                    'granada-cf', 'rayo-vallecano', 'rcd-mallorca',
                    'real-betis', 'real-madrid', 'real-sociedad',
                    'sevilla-fc','ud-almeria','ud-las-palmas',
                    'valencia-cf', 'villarreal-cf'
                  ]; 
    const teamPlayers = {};

    for (const team of teams) {
        const url = `https://www.worldfootball.net/teams/${team}/10/`;
        await page.goto(url, {
            waitUntil: 'domcontentloaded',
            timeout: 6000000
        });

        const players = await page.$$eval('a[href*="player_summary"]', elements => {
            return elements.map(element => element.innerText);
        });

        teamPlayers[team] = players;
    }

    await browser.close();

    // Write the teamPlayers object to a JSON file
    fs.writeFileSync('LaLiga.json', JSON.stringify(teamPlayers, null, 2), 'utf-8');
    console.log('The LaLiga.json file has been saved!');
})();