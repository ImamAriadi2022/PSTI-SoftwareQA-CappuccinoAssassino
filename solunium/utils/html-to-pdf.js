const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(__dirname, '../mochawesome-report/mochawesome.html'), {waitUntil: 'networkidle0'});
  await page.pdf({ path: 'mochawesome-report/report.pdf', format: 'A4' });
  await browser.close();
})();