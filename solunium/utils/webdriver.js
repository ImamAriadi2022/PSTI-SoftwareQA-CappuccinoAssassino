const { Builder } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');

async function getDriver(browser = 'chrome') {
  if (browser === 'chrome') {
    let options = new chrome.Options();
    options.addArguments('--headless=new'); // gunakan mode headless baru
    options.addArguments('--no-sandbox');
    options.addArguments('--disable-dev-shm-usage');
    return await new Builder().forBrowser('chrome').setChromeOptions(options).build();
  }
  return await new Builder().forBrowser(browser).build();
}

module.exports = getDriver;