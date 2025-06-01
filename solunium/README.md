
```markdown
# 🧪 Selenium Test untuk Web IoT

Project ini berisi pengujian otomatis berbasis **Selenium WebDriver** untuk aplikasi **React Web IoT**. Pengujian mencakup:

- Rendering kartu sensor (suhu, kelembaban, cahaya)
- Navigasi halaman Dashboard dan About

---

## 📁 Struktur Folder

```

solunium/
├── tests/
│   ├── card-rendering.test.js
│   └── navigation.test.js
│   └── dashboard.test.js
├── utils/
│   └── webdriver.js
├── .env
├── package.json
└── README.md

````

---

## ⚙️ Prasyarat

- Node.js dan npm terpasang
- Google Chrome terinstal
- Aplikasi React Web IoT berjalan di `https://web-iot-omega.vercel.app/`

---

## 🚀 Langkah Setup

### 1. Clone dan Masuk ke Folder Test

```bash
git clone https://github.com/ImamAriadi2022/web-iot.git
cd web-iot/solunium
````

> Atau jika menggunakan folder project terpisah, pastikan React app tetap berjalan di `https://web-iot-omega.vercel.app/`.

---

### 2. Instalasi Dependency

```bash
npm init -y
npm install selenium-webdriver chromedriver dotenv mocha --save-dev
```

---

### 3. Buat File `.env`

Buat file `.env` di dalam folder `solunium` dan isi:

```
BASE_URL=https://web-iot-omega.vercel.app/
```

---

### 4. Tambahkan Script `test` di package.json

Edit `package.json`, tambahkan:

```json
"scripts": {
  "test": "mocha tests/*.test.js --timeout 20000"
}
```

---

### 5. Jalankan React App

Buka terminal baru:

```bash
cd ../iot
npm install
npm start
```

Pastikan berjalan di `https://web-iot-omega.vercel.app/`.

---

### 6. Jalankan Pengujian

Buka terminal di folder `solunium`:

```bash
npm test
```

---

## ✅ Yang Diuji

* Halaman Dashboard menampilkan kartu `.card-suhu`, `.card-kelembaban`, `.card-cahaya`
* Navigasi ke halaman About dan kembali ke Dashboard melalui logo atau judul situs

---

## 📌 Tips

* Tambahkan `data-testid` atau `className` unik di komponen React untuk mempermudah seleksi elemen
* Jalankan React dalam mode development (`npm start`) agar pengujian berjalan stabil

---

## 📂 Tambahan

Untuk menambahkan pengujian lain, cukup buat file baru di folder `tests/`, contoh:

```bash
tests/form-input.test.js
tests/authentication.test.js
```

---

## 🧑‍💻 Kontak

Dikembangkan oleh 
1. Imam Ariadi
GitHub: [@ImamAriadi2022](https://github.com/ImamAriadi2022)
2. tambahkan anggota kelompok


