# 📋 Changelog

Semua pembaruan dan perubahan pada proyek **Smart MP3 Batch Merger** akan dicatat dalam dokumen ini.

---

## [v2.1.0] - 2026-09-03

### 🚀 Pembaruan & Peningkatan (Stability & Performance Release):

#### 1. ⚡ Perbaikan Total Deadlock Rendering FFmpeg (Anti-Stuck)
- Memperbaiki masalah kritis di mana proses rendering audio berhenti/membeku (*stuck*) di status `[1/N] Memproses...`.
- Masalah disebabkan oleh OS Pipe Buffer `stderr` Windows (4 KB) yang penuh saat proses penggabungan. Ditambahkan *asynchronous background stderr reader thread* yang menguras saluran output FFmpeg secara berkelanjutan, membuat proses render berjalan pada kecepatan 100% tanpa henti.

#### 2. 🎚️ Auto-Resampling Audio Universal (Dukungan Penuh WAV, MP3, AAC, FLAC)
- Mengintegrasikan filter konversi format audio `aformat=sample_rates=...:channel_layouts=stereo` otomatis sebelum proses penggabungan/crossfade.
- Menjamin kelancaran penggabungan antar berbagai format file audio yang memiliki resolusi sample rate atau channel berbeda (misalnya mencampur WAV 48 kHz stereo dengan MP3 44.1 kHz) tanpa error *concat parameter mismatch*.

#### 3. 🎵 Dukungan Penuh Input 1 Lagu Langsung (Single Audio File)
- Mesin pemindai audio kini secara cerdas mengenali file audio tunggal langsung (misal: `D:\Music\Intro.mp3`) tanpa harus dimasukkan ke dalam folder terpisah.
- Tombol **"Pilih File Lagu"** kini memanggil Windows File Open Dialog native (`-topmost`) yang instan dan langsung menghubungkan file lokal tanpa proses unggah yang lambat.

#### 4. 🪟 Dialog Pemilihan Folder Native Windows Instan & Selalu Terdepan
- Menggantikan skrip dialog lama dengan implementasi Tkinter native Windows berkecepatan tinggi (0.05 detik) dengan atribut `-topmost` dan `focus_force()`.
- Jendela pemilihan folder dan file kini selalu muncul di baris paling depan (di atas aplikasi) dan tidak lagi tersembunyi di balik browser atau taskbar.
- Mengeliminasi pembekuan antarmuka (*UI freeze*) dengan arsitektur *non-blocking async-polling*.

#### 5. 🛑 Tombol Batal Real-Time (`Batal`)
- Menambahkan tombol pembatalan interaktif saat proses *batch merging* sedang berjalan.
- Menghentikan proses FFmpeg yang aktif secara aman, membersihkan file sementara, dan mengembalikan UI ke status siap pakai tanpa menimbulkan file korup atau aplikasi crash.

#### 6. 🧠 Smart UI Auto-Adjust & Validasi Cerdas
- Slider **"Jumlah Lagu per Output File"** kini otomatis menyesuaikan batas minimalnya secara dinamis saat mode *"Semua Wajib Masuk"* aktif.
- Mencegah kontradiksi matematika yang membingungkan (misalnya memasukkan 7 lagu wajib ke dalam 1 file yang berkapasitas 3 lagu) dengan peringatan instruksi yang ramah dan solutif sebelum proses dimulai.

#### 7. 🛠️ Pemulihan Pintasan F12 & Klik Kanan (Developer Tools)
- Mengaktifkan kembali tombol **F12** dan klik kanan (*Inspect element*) sehingga pengguna dan pengembang dapat memeriksa log konsol browser dengan bebas saat mendiagnosis sistem.

---

## [v2.0.0] - 2026-08-29

### 🚀 Pembaruan Utama (Major Highlights):

#### 1. 🪟 Migrasi ke Native Microsoft WebView2 (`pywebview`)
- Menggantikan peluncur browser eksternal (`msedge.exe --app`) dengan **Native Windows WebView2 Runtime** murni menggunakan pustaka `pywebview`.
- Menghilangkan masalah layar error *"Tidak terhubung ke jaringan / ERR_CONNECTION_REFUSED"* yang sering terjadi pasca-booting/shutdown PC.
- Penggunaan memori (RAM) jauh lebih hemat (**~40–60 MB**) dan rendering antarmuka 60 FPS dengan akselerasi GPU DirectX.

#### 2. 🛡️ Clean Workspace Architecture (Bebas Folder Otomatis)
- Menghapus pembuatan folder otomatis (`workspace_inputs` & `output_merged_tracks`) saat startup aplikasi.
- Folder tempat file `Smart_MP3_Merger.exe` berada tetap 100% rapi dan bersih. Folder hanya dibuat secara *on-demand* saat pengguna benar-benar mengeksekusi operasi terkait.

#### 3. 📖 Tombol & Modal Panduan Interaktif Terpadu
- Menambahkan tombol **"Panduan"** di sudut kanan atas header antarmuka.
- Modal interaktif *Dark Glassmorphism* dengan 4 tab komprehensif:
  - 🚀 **4 Langkah Penggunaan**: Alur kerja step-by-step dari input hingga export.
  - 📁 **Panduan Folder Manual**: Instruksi pengaturan folder input/output mandiri.
  - ⚙️ **Mode & Aturan Lagu**: Panduan intro/outro/acak, giliran rotasi, dan rumus anti-duplikasi.
  - 💡 **Tips & Kualitas Audio**: Informasi fitur *Auto Match Source Quality* & efek *Crossfade*.

#### 4. 🏷️ Label Versi Antarmuka (`v2.0.0`)
- Menambahkan lencana versi modern di header aplikasi dan dokumen pendukung.

#### 5. ⚡ Toleransi Startup & Binding IPv4 Eksplisit
- Mengikat server backend lokal secara eksplisit ke `127.0.0.1:8765` untuk mencegah konflik resolusi IPv6 `[::1]`.
- Menambahkan jeda toleransi adaptif hingga 6 detik saat startup untuk memastikan kelancaran saat *cold boot*.

---

## [v1.0.0] - 2026-08-25

### ✨ Fitur Awal:
- **Dual Mode Input**: Dukungan input via Folder Picker, Upload File MP3 banyak sekaligus, dan Drag-and-Drop.
- **Live Combinatorics Inspector**: Perhitungan variasi permutasi & kombinasi $P(n, k)$ dan $C(n, k)$ secara *real-time*.
- **100% Unique Batch Guarantee**: Jaminan anti-duplikat urutan lagu dengan cryptographic hashing.
- **Audio Processing**: Penggabungan audio berbasis FFmpeg 8.1 dengan auto bitrate detection dan transisi crossfade.
- **Built-in Player**: Pemutar audio terintegrasi dan shortcut pembuka folder Windows Explorer.
- **Kompilator Portable**: Script `build_portable_exe.py` untuk menghasilkan single executable mandiri.
