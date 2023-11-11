const puppeteer = require('puppeteer');
const fs = require('fs'); // Import the File System module

(async () => {
    const browser = await puppeteer.launch({
        headless: false, // Set to true if you don't need to see the browser GUI
    });
    const page = await browser.newPage();
    
    const teams = ['ac-milan', 'ac-monza','acf-fiorentina',
                   'as-roma', 'atalanta', 'bologna-fc',
                   'cagliari-calcio', 'empoli-fc' , 'frosinone-calcio',
                   'genoa-cfc', 'hellas-verona', 'inter',
                   'juventus', 'lazio-roma', 'sassuolo-calcio',
                   'ssc-napoli','torino-fc','udinese-calcio',
                   'us-lecce', 'us-salernitana-1919'
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
    fs.writeFileSync('SeriaA.json', JSON.stringify(teamPlayers, null, 2), 'utf-8');
    console.log('The SeriaA.json file has been saved!');
})();