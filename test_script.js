const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch();

    for (const file of ['index.html', 'chancla_bomb.html']) {
        const page = await browser.newPage();
        page.on('console', msg => {
            if (msg.type() === 'error') {
                console.error(`[Error in ${file}]`, msg.text());
                process.exit(1);
            }
        });

        await page.goto(`file://${__dirname}/${file}`);
        await page.waitForTimeout(2000); // give it some time to run and trigger errors if any
        await page.close();
        console.log(`[OK] ${file}`);
    }

    await browser.close();
})();
