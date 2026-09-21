const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`file://${path.resolve('index.html')}`);

  // Try to start game and check for errors
  await page.evaluate(() => {
    // Click play
    const canvas = document.getElementById('game');
    const evt = new MouseEvent('click', {
      clientX: canvas.getBoundingClientRect().left + 117,
      clientY: canvas.getBoundingClientRect().top + 453,
    });
    canvas.dispatchEvent(evt);
  });

  await page.waitForTimeout(1000);

  const errors = [];
  page.on('pageerror', err => {
    errors.push(err.message);
  });

  await page.waitForTimeout(2000);

  if (errors.length > 0) {
    console.error('Errors found:', errors);
    process.exit(1);
  } else {
    console.log('No errors found during gameplay start.');
  }

  await browser.close();
})();
