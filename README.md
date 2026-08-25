# 🎵 Smart MP3 Batch Merger & Randomizer

<p align="center">
  <img src="static/icon.png" width="120" height="120" alt="Smart MP3 Merger Logo" style="border-radius: 20px;">
</p>

<p align="center">
  <strong>Intelligent Audio Combinatorics & Batch Randomizer Engine</strong><br>
  Ditenagai oleh Python, FFmpeg 8.1, dan Antarmuka Modern Dark Glassmorphism.
</p>

---

## ✨ Fitur Utama (Key Features)

1. **Dual Mode Input (Folder & File Pickers)**:
   * **Pilih Folder Wajib & Random**: Buka folder secara instan lewat dialog browser native.
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

5. **⚡ Hemat Memori (RAM Safe: ~50MB)**:
   * Pemrosesan streaming FFmpeg memastikan pemakaian RAM sangat ringan dan stabil tanpa lonjakan memori.

6. **📁 Pemutar Audio & Shortcut Windows Explorer**:
   * Built-in player untuk mendengarkan lagu hasil merge secara instan.
   * Tombol *Buka di Explorer* untuk langsung membuka folder output di Windows.

7. **📦 Tersedia 2 Mode: Desktop App & Web App**:
   * **Desktop App**: Jendela software mandiri dengan custom icon, terkunci anti-zoom, dan bebas glitch.
   * **Web App**: Berjalan di browser lokal (`http://localhost:8765`).

---

## 🚀 Cara Menjalankan (Getting Started)

### Prasyarat:
* Python 3.10+ terpasang di sistem.
* [FFmpeg](https://ffmpeg.org/) terpasang dan terdaftar di PATH (atau diletakkan di folder `bin/`).

### 1. Menjalankan Versi Desktop App:
Klik ganda file:
```bash
Smart MP3 Merger Desktop.bat
```
*(Atau jalankan `python desktop_app.py` di terminal).*

### 2. Menjalankan Versi Web Browser:
Klik ganda file:
```bash
run.bat
```
Lalu buka browser Anda di: `http://localhost:8765`

### 3. Membuat Portable EXE Mandiri (`Smart_MP3_Merger.exe`):
Jika Anda ingin mengemas seluruh aplikasi menjadi 1 file `.exe` portable tanpa butuh Python/FFmpeg di PC lain:
```bash
python build_portable_exe.py
```
Hasil executable akan otomatis dibuat di folder utama sebagai `Smart_MP3_Merger.exe`.

---

## 📂 Struktur File Project

```
MP3 Merger/
├── app_icon.ico                 # Icon aplikasi Windows
├── build_portable_exe.py        # Script otomatis kompilasi PyInstaller EXE
├── create_icon.py               # Generator icon PNG & ICO
├── desktop_app.py               # Wrapper aplikasi desktop native (Edge WebView2)
├── folder_picker.py             # Dialog folder Windows Explorer native
├── merger_engine.py             # Inti engine audio FFmpeg & matematika permutasi
├── run.bat                      # Launcher Web App lokal
├── server.py                    # Multi-threaded backend HTTP server & REST API
├── Smart MP3 Merger Desktop.bat # Launcher Desktop App
├── static/                      # Antarmuka Modern Glassmorphism
│   ├── app.js                   # Logika interaktif frontend & event interceptors
│   ├── favicon.ico              # Favicon
│   ├── icon.png                 # Icon logo resolusi tinggi
│   ├── index.html               # Struktur UI
│   └── style.css                # Desain dark glassmorphism
└── test_engine.py               # Unit test otomatis untuk matematika & FFmpeg
```

---

## 📄 Lisensi
Didistribusikan di bawah lisensi MIT.
