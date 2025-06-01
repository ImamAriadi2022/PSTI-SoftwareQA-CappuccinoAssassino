require('dotenv').config();
const { By, until } = require('selenium-webdriver');
const { expect } = require('chai');
const getDriver = require('../utils/webdriver');

console.log('BASE_URL:', process.env.BASE_URL);

// Helper: cari h1/h2/h3 yang mengandung judul (case-insensitive)
function mainTitleXpath(label) {
  return `//*[self::h1 or self::h2 or self::h3][contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"${label.toLowerCase()}")]`;
}

describe('Navigasi di Web IoT - Kalimantan Station 1', function () {
  this.timeout(40000);
  let driver;
  const stationUrl = process.env.BASE_URL.replace(/\/$/, '') + '/kalimantan/station1';
  const downloadPagePath = process.env.BASE_URL.replace(/\/$/, '') + '/kalimantan/download';   

  before(async () => {
    driver = await getDriver();
    try { await driver.get(stationUrl);
    } catch (error) {
        console.error ("error saat driver.get:", error.message);
    }
    await driver.wait(
      until.elementLocated(By.xpath(mainTitleXpath('Environment Status'))),
      20000,
      "Judul utama 'Environment Status' tidak ditemukan pada setup awal navigasi."
    );
  });

  after(async () => {
    if (driver) await driver.quit();
  });

 it('Navigasi ke halaman Download melalui sidebar', async () => {
  // Pastikan sidebar terbuka: cek logo sidebar muncul, jika tidak klik tombol toggle
  let sidebarLogo;
  try {
    sidebarLogo = await driver.findElement(By.xpath("//img[@alt='Logo']"));
    if (!(await sidebarLogo.isDisplayed())) throw new Error();
  } catch {
    // Klik tombol toggle sidebar (ikon FaBars)
    const toggleBtn = await driver.findElement(By.css("div[style*='position: fixed'] svg"));
    await toggleBtn.click();
    await driver.wait(until.elementLocated(By.xpath("//img[@alt='Logo']")), 5000);
    await new Promise(res => setTimeout(res, 500)); // delay agar sidebar benar-benar terbuka
  }

  // Cari link download di sidebar (lebih fleksibel)
  const downloadNav = await driver.wait(
    until.elementLocated(By.xpath(`//nav//a[contains(@href,'/kalimantan/download')]`)),
    15000,
    "Link navigasi 'Download' di sidebar tidak ditemukan"
  );
  await downloadNav.click();

  // Tunggu path URL berubah ke /kalimantan/download (SPA friendly)
  await driver.wait(async () => {
    const url = await driver.getCurrentUrl();
    return url.includes('/kalimantan/download');
  }, 15000, "URL tidak berubah ke halaman download setelah klik navigasi download.");

  // Verifikasi judul halaman download (h1/h2/h3)
  const downloadPageTitle = await driver.wait(
    until.elementLocated(By.xpath(mainTitleXpath('Download Data'))),
    10000,
    "Judul halaman download tidak ditemukan"
  );
  expect((await downloadPageTitle.getText()).toLowerCase()).to.include('download data');

  // Verifikasi tombol download data
  const downloadBtn = await driver.wait(
    until.elementLocated(By.xpath("//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'download data')]")),
    10000,
    "Tombol 'Download Data' di halaman Download tidak ditemukan"
  );
  expect((await downloadBtn.getText()).toLowerCase()).to.include('download data');
});
});