require('dotenv').config();
const { By, until } = require('selenium-webdriver');
const { expect } = require('chai');
const getDriver = require('../utils/webdriver');

console.log('BASE_URL:', process.env.BASE_URL);

const GAUGE_LABELS = [
  'Humidity', 'Temperature', 'Rainfall',
  'Wind Speed', 'Irradiation', 'Wind Direction'
];

const FILTER_LABELS = [
  '1 Hari Terakhir', '7 Hari Terakhir', '1 Bulan Terakhir'
];

const TABLE_HEADERS = [
  'Timestamp', 'Humidity (%)', 'Temperature (°C)', 'Rainfall (mm)',
  'Wind Speed (km/h)', 'Irradiation (W/m²)', 'Wind Direction'
];

// Helper: cari h1/h2 yang mengandung judul (case-insensitive)
function mainTitleXpath(label) {
  return `//*[self::h1 or self::h2][contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"${label.toLowerCase()}")]`;
}

function labelXpath(tag, label) {
  return `//${tag}[normalize-space(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'))="${label.toLowerCase()}"]`;
}

describe('Dashboard Web IoT - Kalimantan Station 1', function () {
  this.timeout(45000);
  let driver;
  const stationUrl = process.env.BASE_URL + '/kalimantan/station1';

  before(async () => {
    driver = await getDriver();
    try { await driver.get(stationUrl);
    } catch (error) {
        console.error ("error saat driver.get:", error.message);
    }
    await driver.wait(
      until.elementLocated(By.xpath(mainTitleXpath('Environment Status'))),
      25000,
      "Judul utama 'Environment Status' (h1/h2) tidak ditemukan setelah 25 detik."
    );
  });

  after(async () => {
    if (driver) await driver.quit();
  });

  it('Harus menampilkan judul utama dashboard "Environment Status"', async () => {
    const title = await driver.wait(
      until.elementLocated(By.xpath(mainTitleXpath('Environment Status'))),
      10000
    );
    expect((await title.getText()).toLowerCase()).to.include('environment status');
  });

  it('Harus menampilkan semua gauge utama dengan label yang benar', async () => {
    for (const label of GAUGE_LABELS) {
      const el = await driver.wait(
        until.elementLocated(By.xpath(`//h5[normalize-space(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'))="${label.toLowerCase()}"]`)),
        10000,
        `Gauge dengan label '${label}' tidak ditemukan`
      );
      expect((await el.getText()).toLowerCase()).to.equal(label.toLowerCase());
    }
  });

  it('Harus menampilkan tombol filter sesuai label UI', async () => {
    for (const label of FILTER_LABELS) {
      const btn = await driver.wait(
        until.elementLocated(By.xpath(labelXpath('button', label))),
        10000,
        `Tombol filter '${label}' tidak ditemukan`
      );
      expect((await btn.getText()).toLowerCase()).to.equal(label.toLowerCase());
    }
  });

  it('Harus menampilkan tabel status dengan header yang benar', async () => {
    for (const header of TABLE_HEADERS) {
      const th = await driver.wait(
        until.elementLocated(By.xpath(labelXpath('th', header))),
        10000,
        `Header tabel '${header}' tidak ditemukan`
      );
      expect((await th.getText()).toLowerCase()).to.equal(header.toLowerCase());
    }
  });

// ...existing code...

it('Harus menampilkan chart (svg) di dashboard', async function () {
  // Tunggu elemen chart SVG muncul
  const chart = await driver.wait(
    until.elementLocated(By.css('svg')),
    20000,
    "Elemen chart (svg) tidak ditemukan"
  );
  expect(await chart.isDisplayed()).to.be.true;
});

// ...existing code...

  // Test tombol "Download Data" dihapus karena hanya ada di halaman /kalimantan/download
});