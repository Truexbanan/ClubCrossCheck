const puppeteer = require('puppeteer');
const fs = require('fs'); // Import the File System module

(async () => {
    const browser = await puppeteer.launch({
        headless: false, // Set to true if you don't need to see the browser GUI
    });
    const page = await browser.newPage();
    
    const teams = [
                   '1-fc-heidenheim-1846', '1-fc-koeln','1-fc-union-berlin',
                   '1-fsv-mainz-05', '1899-hoffenheim', 'bayer-leverkusen',
                   'bayern-muenchen', 'bor-moenchengladbach' , 'borussia-dortmund',
                   'eintracht-frankfurt', 'fc-augsburg', 'rb-leipzig',
                   'sc-freiburg', 'sv-darmstadt-98', 'vfb-stuttgart',
                   'vfl-bochum','vfl-wolfsburg','werder-bremen'

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
    fs.writeFileSync('Bundesliga.json', JSON.stringify(teamPlayers, null, 2), 'utf-8');
    console.log('The Bundesliga.json file has been saved!');
})();