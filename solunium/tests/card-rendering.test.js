require('dotenv').config();
const { By, until } = require('selenium-webdriver');
const { expect } = require('chai');
const getDriver = require('../utils/webdriver');

describe('Rendering Kartu Dashboard', function () {
  this.timeout(20000);
  let driver;

  before(async () => {
    driver = await getDriver();
    await driver.get(process.env.BASE_URL + '/kalimantan/station1');
    await driver.sleep(2000);
  });

  after(async () => {
    if (driver) await driver.quit();
  });

  const cards = [
    'Humidity',
    'Temperature',
    'Windspeed',
    'Rainfall',
    'Irradiation',
    'Wind Direction',
    'Water Temperature'
  ];

  cards.forEach(label => {
    it(`Kartu ${label} muncul`, async () => {
      const card = await driver.wait(
        until.elementLocated(By.xpath(`//h5[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), "${label.toLowerCase()}")]/ancestor::div[contains(@class,'text-center')]`)),
        10000
      );
      const text = await card.getText();
      expect(text.toLowerCase()).to.include(label.toLowerCase());
    });
  });
});