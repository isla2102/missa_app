const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('C:/Users/imsup/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true
  });
  const page = await browser.newPage();
  await page.goto(pathToFileURL(path.resolve('prototype/index.html')).href);
  await page.waitForTimeout(300);

  const htmlBefore = await page.locator('[data-js="season-modal-body"]').innerHTML();
  console.log('클릭 전 HTML:', htmlBefore);

  await page.evaluate(() => {
    document.querySelector('[data-js="liturgical-season"]').click();
  });
  await page.waitForTimeout(300);

  const htmlAfter = await page.locator('[data-js="season-modal-body"]').innerHTML();
  console.log('클릭 후 HTML:', htmlAfter);

  await browser.close();
})();
