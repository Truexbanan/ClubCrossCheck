const puppeteer = require('puppeteer');
const fs = require('fs'); // Import the File System module

(async () => {
    const browser = await puppeteer.launch({
        headless: false, // Set to true if you don't need to see the browser GUI
    });
    const page = await browser.newPage();
    
    const teams = ['arsenal-fc', 'afc-bournemouth','aston-villa',
                   'brentford-fc', 'brighton-hove-albion', 'burnley-fc',
                   'chelsea-fc', 'crystal-palace' , 'everton-fc',
                   'fulham-fc', 'liverpool-fc', 'luton-town',
                   'manchester-city', 'newcastle-united', 'manchester-united',
                   'nottingham-forest','sheffield-united','tottenham-hotspur',
                   'west-ham-united', 'wolverhampton-wanderers'
                ]; // Add more team names as needed
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
    fs.writeFileSync('teamPlayers.json', JSON.stringify(teamPlayers, null, 2), 'utf-8');
    console.log('The teamPlayers.json file has been saved!');
})();