<img width="1326" height="873" alt="image" src="https://github.com/user-attachments/assets/b0193715-ed12-48df-9d83-90475c8a5c4b" />


# 🎵 Smart MP3 Batch Merger & Randomizer

<p align="center">
  <img src="static/icon.png" width="120" height="120" alt="Smart MP3 Merger Logo" style="border-radius: 20px;">
</p>

<p align="center">
  <strong>Intelligent Audio Combinatorics & Batch Randomizer Engine</strong><br>
  <em>Versi 2.0.0 — Ditenagai oleh Python, FFmpeg 8.1, Native Microsoft WebView2, dan Modern Dark Glassmorphism UI.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0.0-00f2fe.svg" alt="Version 2.0.0">
  <img src="https://img.shields.io/badge/GUI-Native%20WebView2-10b981.svg" alt="Native WebView2">
  <img src="https://img.shields.io/badge/License-MIT-a855f7.svg" alt="License MIT">
  <img src="https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue.svg" alt="Windows 10/11">
</p>

---

## 🌟 Apa yang Baru di Versi 2.0.0? (New in v2.0.0)

1. 🪟 **Native Microsoft WebView2 Desktop Window (`pywebview`)**:
   * Antarmuka aplikasi kini berjalan sebagai software desktop *native* mandiri tanpa membuka browser eksternal.
   * Bebas dari layar error browser offline (*ERR_CONNECTION_REFUSED*) saat PC baru dinyalakan (*cold boot*).
   * Konsumsi RAM super hemat (**hanya ~40–60 MB**) dan akselerasi GPU 60 FPS.

2. 🛡️ **Clean Workspace Architecture (Bebas Folder Otomatis)**:
   * Aplikasi tidak lagi membuat folder otomatis di sekitar file `.exe` saat pertama kali dibuka.
   * Folder kerja dan direktori Anda tetap 100% rapi dan bersih. Folder hanya dibuat *on-demand* saat diperlukan.

3. 📖 **Tombol & Modal Panduan Interaktif Terpadu**:
   * Tombol **"Panduan"** di pojok kanan atas dengan 4 tab interaktif: *4 Langkah Penggunaan*, *Panduan Folder Manual*, *Mode & Aturan Lagu*, serta *Tips & Kualitas Audio*.

4. ⚡ **Binding IPv4 Eksplisit & Proteksi Startup**:
   * Komunikasi server lokal menggunakan `127.0.0.1:8765` untuk mencegah masalah resolusi IPv6 `[::1]`.

---

## ✨ Fitur Utama (Key Features)

1. **Dual Mode Input (Folder & File Pickers)**:
   * **Pilih Folder Wajib & Random**: Buka folder secara instan lewat dialog native.
   * **Pilih Banyak File Lagu Sekaligus**: Upload beberapa file MP3 sekaligus.
   * **Drag & Drop**: Cukup tarik file/folder dari Windows Explorer ke dalam aplikasi.
   * **Direct Path Scanning**: Ketik/paste path folder manual dan klik Scan.

2. **🧮 Live Combinatorics Inspector**:
   * Menghitung kemungkinan variasi unik secara *real-time* dengan rumus permutasi & kombinasi $P(n, k)$ dan $C(n, k)$.
   * Contoh: **1 Lagu Wajib + 10 Lagu Random = 25.200 Variasi Unik** (untuk output 5 lagu per file).
   * Algoritma hashing cerdas menjamin **100% Anti-Duplikat** dalam setiap batch.

3. **⚙️ Pengaturan Fleksibel Posisi & Mode**:
   * **Posisi Lagu Wajib**: *Di Awal (Intro)*, *Di Akhir (Outro)*, atau *Posisi Acak*.
   * **Mode Lagu Wajib (>1 File)**: *Semua Wajib Masuk* vs *Ambil 1 Bergilir*.
   * **Slider Interaktif**: Jumlah lagu per output file (panjang 1 mix) dan target jumlah file output (berapa buah file MP3 dibuat).
   * **Efek Transisi (Crossfade)**: Slider 0.0s – 5.0s fade-in/fade-out halus antar lagu.

4. **🎧 Auto Quality Matcher (Lossless Quality)**:
   * Memindai bitrate asli lagu sumber via FFprobe dan menyesuaikan output secara otomatis (hingga 320 kbps) agar kualitas suara tetap jernih dan original.

5. **⚡ Hemat Memori (RAM Safe: ~40–60MB)**:
   * Pemrosesan streaming FFmpeg memastikan pemakaian RAM sangat ringan dan stabil tanpa lonjakan memori.

6. **📁 Pemutar Audio & Shortcut Windows Explorer**:
   * Built-in player untuk mendengarkan lagu hasil merge secara instan.
   * Tombol *Buka di Explorer* untuk langsung membuka folder output di Windows.

---

## 🚀 Cara Menjalankan (Getting Started)

### 1. Menjalankan File Portable EXE (Paling Direkomendasikan):
Unduh dan klik ganda:
```bash
Smart_MP3_Merger.exe
```
*Tidak memerlukan instalasi Python atau software tambahan apa pun di komputer.*

### 2. Menjalankan dari Source Code (Development):
```bash
# Install dependensi
pip install -r requirements.txt   # atau pip install pywebview

# Jalankan Desktop App (Native WebView2)
python desktop_app.py

# Atau jalankan Web App Server
python server.py
```

### 3. Kompilasi Ulang File EXE Portable:
```bash
python build_portable_exe.py
```

---

## 📂 Struktur File Project

```
MP3 Merger/
├── app_icon.ico                 # Icon aplikasi Windows
├── build_portable_exe.py        # Script otomatis kompilasi PyInstaller EXE
├── CHANGELOG.md                 # Catatan riwayat versi & perubahan
├── create_icon.py               # Generator icon PNG & ICO
├── desktop_app.py               # Wrapper aplikasi desktop native (Microsoft WebView2)
├── folder_picker.py             # Dialog folder Windows Explorer native
├── merger_engine.py             # Inti engine audio FFmpeg & matematika permutasi
├── README.md                    # Dokumentasi utama proyek
├── run.bat                      # Launcher Web App lokal
├── server.py                    # Multi-threaded backend HTTP server & REST API
├── Smart MP3 Merger Desktop.bat # Launcher Desktop App
├── static/                      # Antarmuka Modern Glassmorphism (v2.0.0)
│   ├── app.js                   # Logika interaktif frontend, modal panduan, & audio player
│   ├── favicon.ico              # Favicon
│   ├── icon.png                 # Icon logo resolusi tinggi
│   ├── index.html               # Struktur UI (Header v2.0.0, Modal Panduan)
│   └── style.css                # Desain dark glassmorphism & responsive modal
└── test_engine.py               # Unit test otomatis untuk matematika & FFmpeg
```

---

## 📄 Lisensi
Didistribusikan di bawah lisensi MIT.
