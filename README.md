<img width="1326" height="873" alt="image" src="https://github.com/user-attachments/assets/e36faf16-abeb-43f5-a939-394b6a424508" />


# 🎵 Smart MP3 Batch Merger & Randomizer

<p align="center">
  <img src="static/icon.png" width="120" height="120" alt="Smart MP3 Merger Logo" style="border-radius: 20px;">
</p>

<p align="center">
  <strong>Intelligent Audio Combinatorics & Batch Randomizer Engine</strong><br>
  <em>Versi 2.2.0 — Ditenagai oleh Python, FFmpeg 8.1, Native Microsoft WebView2, dan Modern Dark Glassmorphism 3-Column Studio UI.</em>
</p>

<p align="center">
  <a href="https://github.com/maxnmrantau/Smart-MP3-Batch-Merger/releases/tag/v2.2.0"><img src="https://img.shields.io/badge/Download-v2.2.0%20Portable%20EXE-00f2fe?style=for-the-badge&logo=windows" alt="Download EXE"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.2.0-00f2fe.svg" alt="Version 2.2.0">
  <img src="https://img.shields.io/badge/GUI-Native%20WebView2-10b981.svg" alt="Native WebView2">
  <img src="https://img.shields.io/badge/Layout-3--Column%20Zero--Scroll-a855f7.svg" alt="3-Column Studio Layout">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License MIT">
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

Aplikasi dirancang sangat intuitif dengan arsitektur **3-Column Pro Studio Dashboard**:

```
┌─────────────────────────┐    ┌──────────────────────────┐    ┌─────────────────────────┐
│  KOLOM 1: INPUT FOLDER  │    │   KOLOM 2: PENGATURAN    │    │  KOLOM 3: LIVE STUDIO   │
│  - Folder Lagu Wajib    │ ──>│  - Aturan & Posisi Wajib │ ──>│  - Live Combinatorics   │
│  - Folder Pool Acak     │    │  - Target Lagu (Dinamis) │    │  - Start Merge & Batal  │
│  - Folder Output        │    │  - Kalkulator Durasi Riil│    │  - Player & Explorer    │
└─────────────────────────┘    └──────────────────────────┘    └─────────────────────────┘
```

### Kolom 1: Input Lagu Wajib, Pool Acak, & Folder Output
* **Lagu Wajib (Mandatory):** Lagu yang **pasti masuk** ke dalam setiap file hasil gabungan (contoh: Lagu Utama, Jingle Identitas, atau Lagu Pembuka).
  * Klik tombol **"Pilih Folder Wajib"** untuk memilih folder lagu utama Anda.
* **Pool Lagu Random (Acak):** Kumpulan seluruh lagu yang akan diacak untuk mengisi sisa durasi file audio.
  * Klik tombol **"Pilih Folder Pool"** untuk memilih folder koleksi lagu acak Anda.
* *Metode Alternatif:* Anda juga bisa mengklik *"Pilih File Lagu"* untuk memilih file audio tunggal secara langsung, atau cukup tarik (*Drag & Drop*) file ke dalam kotak.
* **Folder Output:** Tentukan folder tujuan penyimpanan file hasil gabungan.

---

### Kolom 2: Mengatur Aturan, Durasi Cerdas, & Komposisi
Pilih bagaimana Lagu Wajib dan lagu acak akan disusun:
1. **Posisi Lagu Wajib:**
   * *Di Awal (Intro):* Lagu wajib selalu diletakkan pada urutan pertama (#1).
   * *Di Akhir (Outro):* Lagu wajib diletakkan pada urutan lagu paling terakhir.
   * *Posisi Acak:* Lagu wajib selalu masuk, namun posisinya diacak alami di antara lagu lain.
2. **Mode Jika Lagu Wajib > 1 File:**
   * *Semua Wajib Masuk:* Seluruh lagu wajib akan dimasukkan ke dalam setiap file output.
   * *Ambil 1 Bergilir (Rotasi):* Mengambil 1 lagu wajib bergantian pada setiap file output.
3. **Panjang Lagu per Output (Kapasitas Slider Dinamis):**
   * Bebas menentukan jumlah lagu (bisa 30, 56, hingga 100+ lagu mengikuti jumlah lagu di pool).
   * Tersedia **kotak input angka presisi** di samping slider untuk mengetik angka target secara langsung.
4. **⏱️ Kalkulator Durasi Riil & Jaminan 1 Jam+ (Safety Badge):**
   * Menghitung durasi riil dari metadata setiap file (`ffprobe`).
   * Menampilkan estimasi durasi rata-rata serta **Rentang Acak (Min – Max)** untuk mengantisipasi skenario lagu pendek vs lagu panjang.
   * **Badge Jaminan 1 Jam+:** Memberi kepastian apakah kombinasi dijamin &ge; 1 Jam, mepet target, atau di bawah 1 jam (lengkap dengan saran jumlah lagu tambahan).
5. **Target Jumlah File Batch, Crossfade, & Kualitas Audio:**
   * Tentukan jumlah batch file MP3 unik yang dibuat.
   * Atur transisi *Crossfade* (0.0 – 5.0 detik) dan Bitrate (`Auto`, `320k`, `256k`, `192k`).

---

### Kolom 3: Live Combinatorics Inspector & Eksekusi Merge
1. **🧮 Live Combinatorics Inspector:**
   * Menghitung total variasi kombinasi unik secara *real-time*.
   * Diformat ringkas dengan satuan resmi (Juta, Miliar, Triliun) dan notasi eksponensial superskrip matematis ($\sim 4,66 \times 10^{45}$) untuk angka astronomis.
   * Arahkan kursor untuk melihat angka lengkap, atau klik tombol **`🔍 Klik Detail / Salin`** untuk *toggle* angka utuh dan menyalin ke clipboard.
2. **Mulai Proses Merge (Batch):**
   * Klik tombol hijau besar **"Mulai Proses Merge (Batch)"**.
   * Pantau proses secara *live* melalui **Progress Bar**, daftar lagu yang sedang dirender, dan log streaming.
   * Tombol **"Batal"** tersedia kapan saja untuk membatalkan proses dengan aman.
3. **Hasil & Audio Player:**
   * Putar langsung file MP3 hasil gabungan di pemutar audio bawaan (*built-in preview player*).
   * Klik **"Buka Folder Hasil"** untuk langsung menuju Windows Explorer.

---

## 🧮 Live Combinatorics & Jaminan 100% Anti-Duplikat

Aplikasi dilengkapi mesin kalkulator kombinatorika yang menghitung variasi unik secara *real-time*:

$$\text{Variasi Unik} = P(n, k) = \frac{n!}{(n - k)!}$$

* **Contoh Nyata:** Jika Anda memiliki **2 Lagu Wajib** dan **56 Lagu Random**, lalu membuat file gabungan berisi **28 Lagu**, sistem dapat menghasilkan hingga $\mathbf{\sim 4,66 \times 10^{45}}$ variasi unik (secara praktis tak terbatas).
* **Proteksi Anti-Duplikasi:** Setiap urutan lagu diverifikasi menggunakan *cryptographic hashing* untuk menjamin **tidak akan pernah ada 2 file MP3 dengan susunan lagu yang sama persis** dalam satu batch.

---

## 🌟 Apa yang Baru di Versi 2.2.0? (New in v2.2.0)

1. **🎛️ Tata Letak Pro Studio 3-Kolom Fullscreen (Zero-Scroll & No Empty Margins)**:
   * Tata letak dirombak menjadi 3 kolom terorganisir penuh (*Step 1: Input*, *Step 2: Settings & Duration*, *Step 3: Inspector, Run & Player*).
   * Mengisi penuh layar (`100vh`) tanpa ruang kosong dan tanpa scroll di resolusi desktop/laptop standar.
2. **🔓 Penghapusan Batas 20 Lagu (Kapasitas Slider Dinamis)**:
   * Slider target lagu kini terbuka dinamis sesuai total lagu di pool (30, 40, 56, 100+ lagu).
3. **⏱️ Kalkulator Durasi Riil & Prediksi Rentang Acak (Min – Max)**:
   * Durasi dihitung langsung dari durasi eksak setiap lagu (`ffprobe`), bukan asumsi statis 3,5 menit.
   * Menampilkan rentang acak min-max untuk memprediksi durasi file saat terambil lagu-lagu pendek maupun panjang.
4. **🛡️ Indikator Jaminan Target 1 Jam (Safety Margin Badge)**:
   * Badge pintar yang memastikan apakah file dipastikan $\ge$ 1 Jam, mepet target, atau butuh lagu tambahan.
5. **⌨️ Input Angka Presisi Langsung (Direct Numeric Input)**:
   * Input teks angka di samping slider lagu dan batch untuk pengetikan angka target instan.
6. **🔢 Formatter Notasi Kompak Kalkulator Kombinatorika Unik**:
   * Angka astronomis puluhan digit diformat elegan dengan superskrip matematis ($\sim 4,66 \times 10^{45}$) serta tooltip, tombol *toggle* detail, dan otomatis salin ke clipboard dengan notifikasi toast.

---

## 🌟 Riwayat Versi Sebelumnya (Previous Releases)

### Versi 2.1.0:
* **⚡ Anti-Stuck FFmpeg Render Engine**: Menghilangkan *pipe buffer deadlock* Windows yang sebelumnya membuat proses render macet di 0%.
* **🎚️ Universal Audio Resampling**: Mendukung pencampuran otomatis berbagai format file (`.wav`, `.mp3`, `.m4a`, dll.) tanpa error konfigurasi.
* **🎵 Input 1 Lagu Langsung (Single File)**: Pengenalan file audio tunggal langsung tanpa folder.
* **🪟 Dialog Windows Explorer Instan & Selalu Terdepan**: Dialog pemilihan folder `-topmost` non-blocking.
* **🛑 Tombol Batal Real-Time**: Pembatalan proses batch merge aman kapan saja.
* **🧠 Smart UI Auto-Adjust**: Slider otomatis menyesuaikan batas minimal saat mode *"Semua Wajib Masuk"* aktif.

---

## 🚀 Cara Menjalankan (Getting Started)

### 1. Menggunakan File Portable EXE (Siap Pakai - Disarankan):
Unduh file **`Smart_MP3_Merger.exe`** dari halaman [GitHub Releases v2.2.0](https://github.com/maxnmrantau/Smart-MP3-Batch-Merger/releases/tag/v2.2.0) lalu klik ganda untuk menjalankannya. Tidak memerlukan instalasi Python apa pun.

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
├── static/                      # Antarmuka Modern Glassmorphism (v2.1.0)
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
