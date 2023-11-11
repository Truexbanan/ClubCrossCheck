const puppeteer = require('puppeteer');
const fs = require('fs'); // Import the File System module

(async () => {
    const browser = await puppeteer.launch({
        headless: false, // Set to true if you don't need to see the browser GUI
    });
    const page = await browser.newPage();
    
    const teams = [ 'as-monaco', 'clermont-foot-63','fc-lorient',
                    'fc-metz', 'fc-nantes', 'havre-ac',
                    'lille-osc', 'montpellier-hsc' , 'ogc-nice',
                    'olympique-lyon', 'olympique-marseille', 'paris-saint-germain',
                    'rc-lens', 'rc-strasbourg', 'stade-brestois',
                    'stade-reims','stade-rennais','toulouse-fc'
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
    fs.writeFileSync('Ligue1.json', JSON.stringify(teamPlayers, null, 2), 'utf-8');
    console.log('The Ligue1.json file has been saved!');
})();