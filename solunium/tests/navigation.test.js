require('dotenv').config();
const { By, until } = require('selenium-webdriver');
const { expect } = require('chai');
const getDriver = require('../utils/webdriver');

describe('Navigasi di Web IoT', function () {
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

  it('Klik logo atau judul kembali ke dashboard utama', async () => {
    let logo;
    try {
      logo = await driver.wait(until.elementLocated(By.css('a.logo, .site-title, .navbar-brand')), 10000);
    } catch {
      logo = await driver.wait(until.elementLocated(By.xpath("//*[contains(text(),'Environment Status Station 2')]")), 10000);
    }
    await logo.click();

    const currentUrl = await driver.getCurrentUrl();
    expect(currentUrl).to.include('/kalimantan/station1');

    const title = await driver.wait(
      until.elementLocated(By.xpath("//*[contains(text(),'Environment Status Station 2')]")),
      10000
    );
    expect((await title.getText()).toLowerCase()).to.include('environment status station 2');
  });

  it('Navigasi ke halaman Download', async () => {
    // Cari link Download Data di sidebar/menu
    const downloadNav = await driver.wait(
      until.elementLocated(By.xpath("//a[contains(@href,'/kalimantan/download')]")),
      10000
    );
    await downloadNav.click();

    // Pastikan tombol download muncul
    const downloadBtn = await driver.wait(
      until.elementLocated(By.xpath("//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'download data')]")),
      10000
    );
    expect((await downloadBtn.getText()).toLowerCase()).to.include('download data');
  });
});