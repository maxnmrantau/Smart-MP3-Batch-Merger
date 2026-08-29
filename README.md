<img width="1326" height="873" alt="image" src="https://github.com/user-attachments/assets/e36faf16-abeb-43f5-a939-394b6a424508" />


# 🎵 Smart MP3 Batch Merger & Randomizer

<p align="center">
  <img src="static/icon.png" width="120" height="120" alt="Smart MP3 Merger Logo" style="border-radius: 20px;">
</p>

<p align="center">
  <strong>Intelligent Audio Combinatorics & Batch Randomizer Engine</strong><br>
  <em>Versi 2.0.0 — Ditenagai oleh Python, FFmpeg 8.1, Native Microsoft WebView2, dan Modern Dark Glassmorphism UI.</em>
</p>

<p align="center">
  <a href="https://github.com/maxnmrantau/Smart-MP3-Batch-Merger/releases/tag/v2.0.0"><img src="https://img.shields.io/badge/Download-v2.0.0%20Portable%20EXE-00f2fe?style=for-the-badge&logo=windows" alt="Download EXE"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0.0-00f2fe.svg" alt="Version 2.0.0">
  <img src="https://img.shields.io/badge/GUI-Native%20WebView2-10b981.svg" alt="Native WebView2">
  <img src="https://img.shields.io/badge/License-MIT-a855f7.svg" alt="License MIT">
  <img src="https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue.svg" alt="Windows 10/11">
  <img src="https://img.shields.io/badge/RAM%20Usage-~50MB-green.svg" alt="RAM Safe">
</p>

---

## 🎯 Untuk Apa Aplikasi Ini? (Use Cases & Kegunaan)

**Smart MP3 Batch Merger & Randomizer** adalah software desktop modern yang dirancang untuk **menggabungkan (*merge*) dan mengacak (*randomize*) ratusan file audio secara massal (*batch*) secara otomatis** dengan menerapkan aturan kombinasi cerdas dan proteksi 100% anti-duplikat.

### Masalah yang Diselesaikan:
Jika Anda ingin membuat 20, 50, atau 100 file audio kompilasi panjang (misalnya untuk video YouTube Lo-Fi/Podcast/Mixtape), menggabungkan lagu secara manual di software editing audio (DAW) membutuhkan waktu berjam-jam dan rentan menghasilkan susunan lagu yang terduplikasi. 

Aplikasi ini mengotomatiskan seluruh proses tersebut hanya dalam **sekali klik**.

### 🎧 Skenario Penggunaan Nyata:
1. **Kreator Konten Video & Podcast (YouTube, TikTok, IG Reels):**
   * Membuat 30 video audio kompilasi di mana setiap file **harus diawali dengan lagu Intro/Jingle/Lagu Wajib yang sama**, namun lagu-lagu pengiring berikutnya diacak dari koleksi lagu tanpa ada urutan yang kembar.
2. **Pengelola Musik Cafe, Restoran, Gym & Retail Store:**
   * Menghasilkan playlist musik harian berdurasi panjang (misal: 10 file audio masing-masing berisi 10 lagu) agar pengunjung dan staf tidak bosan mendengar urutan lagu yang sama setiap hari.
3. **DJ & Musisi / Mixtape Creator:**
   * Meracik variasi mixtape cepat dengan efek transisi *crossfade* halus antar lagu.
4. **Sound Engineer & Batch Producer:**
   * Memproduksi variasi audio massal dengan preservasi kualitas bitrate asli (*lossless*).

---

## 📖 Cara Menggunakan Aplikasi (Step-by-Step Guide)

Aplikasi dirancang sangat intuitif dengan 4 langkah mudah:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐     ┌──────────────────┐
│ 1. Input Lagu   │ ──> │ 2. Aturan Wajib  │ ──> │ 3. Komposisi    │ ──> │ 4. Output & Run  │
│ (Wajib & Pool)  │     │ (Intro/Outro/Mix)│     │ (Panjang & Fade)│     │ (Start Merge)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘     └──────────────────┘
```

### Langkah 1: Input Lagu Wajib & Lagu Random
* **Lagu Wajib (Mandatory):** Lagu yang **pasti masuk** ke dalam setiap file hasil gabungan (contoh: Lagu Utama, Jingle Identitas, atau Lagu Pembuka).
  * Klik tombol **"Pilih Folder Wajib"** untuk memilih folder lagu utama Anda.
* **Pool Lagu Random (Acak):** Kumpulan seluruh lagu yang akan diacak untuk mengisi sisa durasi file audio.
  * Klik tombol **"Pilih Folder Pool"** untuk memilih folder koleksi lagu acak Anda.
* *Metode Alternatif:* Anda juga bisa mengklik *"Pilih File Lagu"* untuk memilih beberapa file MP3 sekaligus, atau cukup tarik (*Drag & Drop*) file MP3 langsung ke dalam kotak.

---

### Langkah 2: Mengatur Aturan & Posisi Lagu Wajib
Pilih bagaimana Lagu Wajib akan ditempatkan di dalam setiap file output:
* **Di Awal (Intro):** Lagu wajib selalu diletakkan pada urutan pertama (#1) di setiap file MP3.
* **Di Akhir (Outro):** Lagu wajib selalu diletakkan pada urutan lagu paling terakhir.
* **Posisi Acak:** Lagu wajib dipastikan selalu ada di dalam file, namun posisinya diacak secara alami di antara lagu-lagu lain.
* **Mode Jika Lagu Wajib > 1 File:**
  * *Semua Wajib Masuk:* Seluruh lagu wajib akan dimasukkan ke dalam setiap file output.
  * *Ambil 1 Bergilir (Rotasi):* Mengambil 1 lagu wajib secara bergantian pada setiap file output (File 1 = Lagu A, File 2 = Lagu B, dst).

---

### Langkah 3: Mengatur Komposisi, Target Batch, & Kualitas
Gunakan slider interaktif untuk menyesuaikan hasil:
1. **Panjang Lagu per Output:** Tentukan berapa total lagu dalam 1 file MP3 gabungan (contoh: 5 lagu = 1 Lagu Wajib + 4 Lagu Random).
2. **Target Jumlah File Output (Batch):** Tentukan berapa banyak file MP3 unik yang ingin Anda buat (contoh: 10 buah file MP3).
3. **Efek Transisi (Crossfade):**
   * `0.0 Detik`: Menggabungkan secara instan (*blazing fast concatenation*).
   * `1.0 – 5.0 Detik`: Memberikan efek fade-in/fade-out halus antar lagu.
4. **Kualitas Audio (Bitrate):**
   * *Auto - Match Source Quality (Disarankan):* Memindai bitrate lagu sumber dan mempertahankan kejernihan suara aslinya.
   * Pilihan manual: `320 kbps`, `256 kbps`, atau `192 kbps`.

---

### Langkah 4: Menentukan Folder Penyimpanan & Memulai Merge
1. Pada bagian **"3. Folder Penyimpanan Hasil"**, klik **"Pilih Folder Output"** dan pilih folder tempat Anda ingin menyimpan file MP3 hasil gabungan.
2. Klik tombol hijau besar **"Mulai Proses Merge (Batch)"**.
3. Pantau proses secara *live* melalui **Progress Bar**, daftar urutan lagu yang sedang diproses, dan log konsol streaming.
4. Setelah selesai:
   * Putar langsung hasil file MP3 di pemutar audio bawaan (*built-in preview player*).
   * Klik tombol **"Buka Folder Hasil"** untuk langsung membuka foldernya di Windows Explorer.
   * Buka file `playlist_summary.txt` di folder output untuk melihat laporan lengkap urutan lagu di setiap file.

---

## 🧮 Live Combinatorics & Jaminan 100% Anti-Duplikat

Aplikasi dilengkapi mesin kalkulator kombinatorika yang menghitung variasi unik secara *real-time*:

$$\text{Variasi Unik} = P(n, k) = \frac{n!}{(n - k)!}$$

* **Contoh Nyata:** Jika Anda memiliki **1 Lagu Wajib** dan **10 Lagu Random**, lalu ingin membuat file output berisi **5 Lagu**, sistem dapat menghasilkan hingga **25.200 variasi file MP3 yang berbeda**.
* **Proteksi Anti-Duplikasi:** Setiap urutan lagu diverifikasi menggunakan *cryptographic hashing (MD5/SHA-256)* untuk menjamin **tidak akan pernah ada 2 file MP3 dengan susunan lagu yang sama persis** dalam satu batch.

---

## 🌟 Apa yang Baru di Versi 2.0.0? (New in v2.0.0)

1. 🪟 **Native Microsoft WebView2 Desktop Window (`pywebview`)**:
   * Menjadi aplikasi desktop murni tanpa membuka jendela browser luar (`msedge.exe`).
   * Bebas dari pesan error browser offline (*ERR_CONNECTION_REFUSED*) saat PC baru dinyalakan (*cold boot*).
   * Penggunaan RAM sangat hemat (**~40–60 MB**) dan didukung akselerasi GPU DirectX.

2. 🛡️ **Clean Workspace Architecture (Bebas Folder Otomatis)**:
   * Aplikasi tidak lagi membuat folder-folder baru secara otomatis saat startup. Direktori kerja tempat file `.exe` berada tetap 100% bersih.

3. 📖 **Tombol & Modal Panduan Interaktif Terpadu**:
   * Tombol **"Panduan"** di pojok kanan atas dengan 4 tab interaktif (*Alur Kerja*, *Panduan Folder Manual*, *Mode Lagu*, dan *Tips Kualitas Audio*).

4. ⚡ **Binding IPv4 Eksplisit & Toleransi Startup Adaptif**:
   * Mengikat server internal ke `127.0.0.1:8765` untuk mencegah konflik IPv6 `[::1]`.

---

## 🚀 Cara Menjalankan (Getting Started)

### 1. Menggunakan File Portable EXE (Siap Pakai - Disarankan):
Unduh file **`Smart_MP3_Merger.exe`** dari halaman [GitHub Releases](https://github.com/maxnmrantau/Smart-MP3-Batch-Merger/releases/tag/v2.0.0) lalu klik ganda untuk menjalankannya. Tidak memerlukan instalasi Python apa pun.

### 2. Menjalankan dari Source Code (Python):
```bash
# Clone repository
git clone https://github.com/maxnmrantau/Smart-MP3-Batch-Merger.git
cd Smart-MP3-Batch-Merger

# Install dependensi
pip install pywebview

# Jalankan Desktop App Native
python desktop_app.py

# Atau jalankan Web Server Lokal
python server.py
```

### 3. Kompilasi Ulang ke File Portable EXE:
```bash
python build_portable_exe.py
```

---

## 📂 Struktur File Project

```
MP3 Merger/
├── app_icon.ico                 # Icon aplikasi Windows
├── build_portable_exe.py        # Script kompilasi PyInstaller EXE
├── CHANGELOG.md                 # Catatan riwayat versi & perubahan
├── create_icon.py               # Generator icon PNG & ICO
├── desktop_app.py               # Wrapper aplikasi desktop native (Microsoft WebView2)
├── folder_picker.py             # Dialog folder Windows Explorer native
├── merger_engine.py             # Inti engine audio FFmpeg & matematika permutasi
├── README.md                    # Dokumentasi lengkap proyek
├── run.bat                      # Launcher Web App lokal
├── server.py                    # Multi-threaded backend HTTP server & REST API
├── Smart MP3 Merger Desktop.bat # Launcher Desktop App
├── static/                      # Antarmuka Modern Glassmorphism (v2.0.0)
│   ├── app.js                   # Logika interaktif frontend & modal panduan
│   ├── favicon.ico              # Favicon
│   ├── icon.png                 # Icon logo resolusi tinggi
│   ├── index.html               # Struktur UI & Modal Panduan
│   └── style.css                # Desain dark glassmorphism & responsive modal
└── test_engine.py               # Unit test otomatis untuk matematika & FFmpeg
```

---

## 📄 Lisensi
Didistribusikan di bawah lisensi MIT. Silakan gunakan dan modifikasi secara bebas untuk kebutuhan pribadi maupun komersial.
