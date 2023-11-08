const puppeteer = require('puppeteer');

(async() => {
    let Browser = await puppeteer.launch({
        headless: false,
    });
    
    let pages = await Browser.pages();
    let page = pages[0];
    
    await page.goto('https://www.worldfootball.net/teams/liverpool-fc/10/', {
    waitUntil: 'domcontentloaded',
    timeout: 60000 // Increases timeout to 60 seconds
});
    //scroll to bottom
    
    //get array of player
    const elements = await page.$$eval('a[href*="player_summary"]', elements => {
        return elements.map(element => element.innerText);
    });
    
    console.log(elements);
})();