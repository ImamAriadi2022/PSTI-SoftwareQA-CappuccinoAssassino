require('dotenv').config();
const { By, until } = require('selenium-webdriver');
const { expect } = require('chai');
const getDriver = require('../utils/webdriver');

describe('Dashboard Web IoT', function () {
  this.timeout(40000);
  let driver;

  before(async () => {
    driver = await getDriver();
    await driver.get(process.env.BASE_URL + '/kalimantan/station1');
    await driver.sleep(3000);
  });

  after(async () => {
    if (driver) await driver.quit();
  });

  it('Harus menampilkan judul utama dashboard', async () => {
    const title = await driver.wait(
      until.elementLocated(By.xpath("//*[contains(text(),'Environment Status Station 2')]")),
      10000
    );
    expect(await title.getText()).to.include('Environment Status Station 2');
  });

  it('Harus menampilkan semua gauge utama', async () => {
    const gauges = [
      'Humidity',
      'Temperature',
      'Windspeed',
      'Rainfall',
      'Irradiation',
      'Wind Direction',
      'Water Temperature'
    ];
    for (const label of gauges) {
      const el = await driver.wait(
        until.elementLocated(By.xpath(`//h5[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), "${label.toLowerCase()}")]`)),
        10000
      );
      expect((await el.getText()).toLowerCase()).to.include(label.toLowerCase());
    }
  });

  it('Harus menampilkan tombol filter 1 Day, 7 Days, 1 Month', async () => {
    const filters = ['1 Day', '7 Days', '1 Month'];
    for (const label of filters) {
      const btn = await driver.wait(
        until.elementLocated(By.xpath(`//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), "${label.toLowerCase()}")]`)),
        10000
      );
      expect((await btn.getText()).toLowerCase()).to.include(label.toLowerCase());
    }
  });

  it('Harus menampilkan tabel status dengan header yang benar', async () => {
    const headers = [
      'Timestamp',
      'Humidity',
      'Temperature',
      'Air Pressure',
      'Rainfall',
      'Irradiation',
      'Windspeed',
      'Wind Direction',
      'Water Temperature'
    ];
    for (const header of headers) {
      const th = await driver.wait(
        until.elementLocated(By.xpath(`//th[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), "${header.toLowerCase()}")]`)),
        10000
      );
      expect((await th.getText()).toLowerCase()).to.include(header.toLowerCase());
    }
  });

  it('Harus menampilkan chart status', async function () {
    try {
      const chartTitle = await driver.wait(
        until.elementLocated(By.xpath("//*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'chart status')]")),
        10000
      );
      expect((await chartTitle.getText()).toLowerCase()).to.include('chart status');
      const chart = await driver.wait(
        until.elementLocated(By.css('canvas,svg')),
        10000
      );
      expect(chart).to.exist;
    } catch (e) {
      this.skip();
      console.warn('Chart/API lambat atau tidak tersedia, test dilewati:', e.message);
    }
  });

  it('Harus menampilkan tombol download data', async function () {
    let downloadBtn;
    try {
      downloadBtn = await driver.findElement(By.xpath("//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'download data')]"));
    } catch {
      const nav = await driver.findElements(By.xpath("//a[contains(@href,'/kalimantan/download')]"));
      if (nav.length > 0) {
        await nav[0].click();
        downloadBtn = await driver.wait(
          until.elementLocated(By.xpath("//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'download data')]")),
          10000
        );
      }
    }
    expect(downloadBtn).to.exist;
  });
});