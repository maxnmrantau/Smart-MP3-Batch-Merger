# 📋 Changelog

Semua pembaruan dan perubahan pada proyek **Smart MP3 Batch Merger** akan dicatat dalam dokumen ini.

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
