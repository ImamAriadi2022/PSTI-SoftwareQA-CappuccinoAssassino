const { Builder } = require('selenium-webdriver');

async function getDriver(browser = 'chrome') {
  return await new Builder().forBrowser(browser).build();
}

module.exports = getDriver;
