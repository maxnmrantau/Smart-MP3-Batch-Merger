# 📋 Changelog

Semua pembaruan dan perubahan pada proyek **Smart MP3 Batch Merger** akan dicatat dalam dokumen ini.

---

## [v2.3.0] - 2026-11-10

### 🚀 Fitur Baru & Peningkatan:

#### 1. 🔁 Fitur Putar Ulang (Loop) & Acak Loop (Random Shuffle)
- Menambahkan opsi **Loop** yang memungkinkan kumpulan lagu diputar berulang untuk mencapai durasi panjang (misal video kompilasi YouTube 1 jam / 2 jam) atau jumlah lagu tertentu dari koleksi pool yang terbatas.
- **Pilih Jumlah Lagu yang Di-loop:** Pengguna bebas memilih berapa lagu dari pool yang ingin di-loop (misal punya 10 lagu dan ingin me-loop 5 lagu saja, atau seluruh 10 lagu).
- **Mode Target Durasi vs Jumlah Lagu:** Mendukung penentuan target berdasarkan jumlah lagu (misal 25 lagu) atau target durasi waktu (misal 60 menit, 120 menit).
- **Acak Loop (Smart Shuffle) vs Berurutan (Sequential):** 
  - *Acak Loop:* Urutan pengulangan diacak alami dengan proteksi cerdas *anti-consecutive duplicate* (tidak ada lagu yang sama berbunyi berturut-turut).
  - *Berurutan:* Lagu diulang secara teratur mengikuti urutan siklus aslinya.

#### 2. 🔘 Sakelar ON / OFF Lagu Wajib (Mandatory Toggle)
- Menambahkan switch toggle ON/OFF untuk fitur Lagu Wajib.
- Ketika di-set **OFF**, pengguna dapat melakukan penggabungan dan pengacakan audio murni dari Pool Acak tanpa memerlukan file lagu wajib atau lagu pembuka.
- Area input folder Lagu Wajib dan opsi posisi wajib otomatis dinonaktifkan secara elegan ketika fitur ini dimatikan.
- Ketika di-set **ON**, Lagu Wajib berfungsi normal seperti sebelumnya.

#### 3. ⏱️ Generator Timestamps Format YouTube & Format Biasa
- **Format Timestamps YouTube:** Secara otomatis menghitung waktu mulai (*start timestamp*) setiap lagu dalam format `00:00 Judul Lagu` atau `00:00:00` (untuk durasi $\ge 1$ jam) dengan memperhitungkan efek transisi *crossfade*.
- **Tombol Sekali Klik Salin YouTube ("📋 Salin YT"):** Tersedia pada setiap item daftar file hasil, memungkinkan pengguna langsung menyalin timestamps siap tempel ke kolom deskripsi YouTube.
- **Modal Timestamps Interaktif ("👁️ Timestamps"):** Menampilkan pratinjau tab untuk format YouTube dan format detail biasa lengkap dengan tombol salin.
- **File Ekspor Otomatis di Folder Output:**
  - `youtube_timestamps.txt`: Berisi timestamps siap copy-paste ke YouTube untuk setiap file hasil dalam batch.
  - `playlist_summary.txt`: Laporan komprehensif mencakup ringkasan batch, format YouTube, dan rincian slot biasa.
- **Pilihan Preferensi Format:** Tersedia dropdown pengaturan di Kolom 2 untuk memilih format laporan yang diinginkan.

#### 4. 🎨 Pembaruan & Penataan Tata Letak (UI Layout Polish)
- **Penghapusan Kalkulator Durasi Redundan:** Menghapus kotak kalkulator estimasi durasi redundan di Kolom 2 agar tata letak pengaturan jauh lebih ringkas, leluasa, dan bebas distorsi.
- **Pencegahan Elemen Terpotong (Zero Boundary Overflow):**
  - Mengaktifkan `overflow-y: auto` dengan slim custom scrollbar pada kartu Kolom 2, memastikan seluruh menu (termasuk *Format Laporan Timestamps & Summary*) dapat diakses secara utuh di semua resolusi layar.
  - Menyelaraskan jarak flexbox menjadi `gap: 10px` teratur dan konsisten.
- **Executable Standalone Siap Pakai:** Mengompilasi ulang [`Smart_MP3_Merger.exe`](file:///d:/CODING/AI%20STUDIO/Mp3%20Merger/Smart_MP3_Merger.exe) (110.0 MB).

---

## [v2.2.0] - 2026-09-09

### 🚀 Fitur Baru & Peningkatan Durasi Cerdas:

#### 1. 🔓 Penghapusan Batas 20 Lagu (Kapasitas Slider Dinamis)
- Slider **"Jumlah Lagu per Output File"** kini terbuka secara dinamis mengikuti total lagu yang tersedia di pool (bisa 30, 40, 56, hingga 100+ lagu).
- Pengguna tidak lagi terkunci pada batas maksimal 20 lagu.

#### 2. ⏱️ Kalkulator Durasi Riil & Prediksi Rentang Acak (Min – Max)
- Menghapus asumsi statis 3,5 menit per lagu.
- Durasi kini dihitung langsung dari **metadata durasi nyata setiap lagu** hasil inspeksi `ffprobe`.
- Menampilkan **Rentang Acak (Min – Max)**: memprediksi durasi terendah (skenario lagu-lagu pendek terpilih) hingga durasi tertinggi (skenario lagu-lagu panjang terpilih).

#### 3. 🛡️ Indikator Jaminan Target 1 Jam (Safety Margin Badge)
- Badge status pintar yang memberi kepastian langsung apakah variasi acak yang dibuat sudah **100% dijamin &ge; 1 Jam**, mepet target, atau di bawah 1 jam, lengkap dengan saran jumlah lagu tambahan yang diperlukan.

#### 4. ⌨️ Input Angka Langsung (Direct Numeric Input)
- Menambahkan kotak input angka presisi di samping slider lagu dan batch, memungkinkan pengguna mengetik angka target secara langsung (misal ketik `33` atau `35`) tanpa harus menggeser slider mouse.

#### 5. 🧮 Live Inspector Durasi Pool & File Output
- Menambahkan metrik baru pada kartu Live Inspector di panel kanan: **Rata-rata Durasi Lagu Pool** dan **Estimasi Durasi per File Output**.

#### 6. 🎛️ Tata Letak Pro Studio 3-Kolom Fullscreen (Zero-Scroll & No Empty Margins)
- Mengubah arsitektur antarmuka menjadi 3 kolom terorganisir penuh (*Step 1: Input & Folder*, *Step 2: Pengaturan & Durasi*, *Step 3: Inspector, Eksekusi & Hasil*).
- Menghilangkan ruang kosong samping dan bawah layar dengan layout fleksibel `100vh`, sehingga semua kontrol penting terlihat rapi tanpa perlu scroll di layar laptop/desktop.

#### 7. 🔢 Formatter Notasi Kompak Kalkulator Kombinatorika Unik
- Mengatasi angka kemungkinan unik astronomis (hingga puluhan digit) agar tidak meluber keluar dari kartu.
- Menampilkan format ringkas dengan satuan resmi (Juta, Miliar, Triliun) serta notasi eksponensial matematis dengan superskrip (misal `~4,66 × 10⁴⁵`).
- Menyediakan tooltip angka utuh saat kursor diarahkan, tombol interaktif `🔍 Klik Detail / Salin` untuk toggle tampilan angka presisi, dan fitur otomatis salin ke clipboard dengan notifikasi toast melayang.

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
