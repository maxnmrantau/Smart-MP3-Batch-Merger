## 🚀 Smart MP3 Batch Merger v2.3.0 (Loop Engine, YouTube Timestamps & Flexible Mandatory Edition)

Pembaruan besar versi **v2.3.0** menghadirkan serangkaian fitur mutakhir untuk kreator konten audio YouTube, DJ, dan produser musik: sistem pengulangan cerdas (**Fitur Loop & Acak Loop**), kendali fleksibel **Sakelar ON/OFF Lagu Wajib**, generator **Timestamps Otomatis YouTube & Format Standar**, serta pemolesan antarmuka Pro Studio yang lebih ringkas dan bebas batas layar (*zero boundary overflow*).

---

### ✨ Apa yang Baru di Versi 2.3.0:

#### 1. 🔁 Fitur Putar Ulang (Loop) & Acak Loop (Random Shuffle)
* **Kompilasi Audio Berdurasi Panjang:** Ulangi lagu-lagu dalam koleksi Anda untuk menghasilkan mixtape atau video kompilasi YouTube berdurasi 1 jam, 2 jam, atau durasi kustom lainnya secara instan.
* **Seleksi Parsial Lagu Pool (Subset Selection):** Pengguna bebas menentukan berapa lagu yang ingin di-loop dari total koleksi pool (contoh: punya 10 lagu dan ingin me-loop 5 lagu saja, atau seluruh 10 lagu).
* **Mode Target Fleksibel:**
  - *Target Durasi Waktu:* Tentukan target waktu minimal per file (misal 60 menit), sistem otomatis menghitung dan mengulang lagu hingga target waktu terpenuhi.
  - *Target Jumlah Lagu:* Tentukan target total jumlah lagu yang ingin diputar dalam satu file gabungan.
* **Dua Pilihan Mode Urutan Pengulangan:**
  - *🎲 Acak Loop (Shuffle):* Lagu diacak bebas di setiap putaran dengan proteksi *anti-consecutive duplicate* cerdas (tidak akan ada lagu yang sama diputar berturut-turut).
  - *🔁 Berurutan (Siklus):* Lagu diulang secara teratur mengikuti urutan siklus alaminya ($1, 2, 3, \dots, 1, 2, 3$).

#### 2. 🔘 Sakelar ON / OFF Lagu Wajib (Mandatory Toggle Switch)
* **Pengacakan Murni Tanpa Lagu Wajib:** Anda kini dapat menggabungkan audio langsung dari Pool Acak tanpa harus menyertakan file lagu wajib atau lagu pembuka.
* **Adaptasi UI Otomatis:** Ketika toggle di-set ke **OFF**, area input Lagu Wajib dan opsi posisinya dinonaktifkan secara anggun, dan komposisi file otomatis dialihkan menjadi 100% lagu acak.
* **Fleksibilitas Penuh:** Hidupkan kembali switch ke **ON** kapan saja Anda ingin menyertakan lagu wajib (Intro, Outro, atau Posisi Acak).

#### 3. ⏱️ Generator Timestamps Format YouTube & Standar
* **Kompensasi Crossfade Presisi:** Menghitung waktu menit/detik (*start timestamps*) secara otomatis dan akurat dalam format bab YouTube (`00:00 Judul Lagu` atau `00:00:00` untuk durasi $\ge 1$ jam) dengan memperhitungkan waktu transisi *crossfade*.
* **Tombol Sekali Klik Salin YouTube ("📋 Salin YT"):** Tombol cepat pada setiap item hasil untuk menyalin seluruh timestamps bab video YouTube langsung ke clipboard.
* **Modal Pratinjau Interaktif ("👁️ Timestamps"):** Dialog pratinjau yang menampilkan dua tab: *Format YouTube* dan *Format Biasa* (nomor slot, durasi tiap trek, dan waktu kumulatif).
* **File Laporan Otomatis di Folder Output:**
  - `youtube_timestamps.txt`: Siap langsung di-*copy-paste* ke kolom deskripsi video YouTube.
  - `playlist_summary.txt`: Laporan komprehensif batch untuk dokumentasi audio.

#### 4. 🎨 Pemolesan Antarmuka & Perbaikan Layout (Zero Boundary Overflow)
* **Penghapusan Kotak Kalkulator Durasi Redundan:** Menghapus kotak kalkulator estimasi durasi redundan di Kolom 2 sehingga tata letak jauh lebih ringkas dan leluasa.
* **Bebas Elemen Terpotong:** Menambahkan auto-scrolling fleksibel dengan slim custom scrollbar pada Kolom 2, memastikan seluruh menu (termasuk *Format Laporan Timestamps & Summary*) tampil utuh tanpa ada yang terpotong di berbagai resolusi layar maupun laptop dengan skala display Windows 125%/150%.

---

### 📦 Cara Menjalankan:
Unduh file **`Smart_MP3_Merger.exe`** di bawah ini, lalu klik ganda untuk langsung menjalankannya. Tidak memerlukan instalasi Python, FFmpeg, atau runtime tambahan (100% Standalone Portable).

