"""
build_portable_exe.py
Automated build script using PyInstaller to produce a single-file NO-CONSOLE portable Smart_MP3_Merger.exe with custom icon and native WebView2 support.
"""

import os
import sys
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def build_exe():
    print("=" * 60)
    print("MEMULAI PROSES BUILD PORTABLE EXE (NATIVE WEBVIEW2 + CUSTOM ICON)")
    print("=" * 60)
    
    bin_dir = os.path.join(BASE_DIR, "bin")
    ffmpeg_exe = os.path.join(bin_dir, "ffmpeg.exe")
    ffprobe_exe = os.path.join(bin_dir, "ffprobe.exe")
    
    if not os.path.isfile(ffmpeg_exe) or not os.path.isfile(ffprobe_exe):
        print("Menyalin FFmpeg binaries ke folder bin/ ...")
        os.makedirs(bin_dir, exist_ok=True)
        if os.path.isfile(r"C:\ffmpeg\bin\ffmpeg.exe"):
            shutil.copy(r"C:\ffmpeg\bin\ffmpeg.exe", ffmpeg_exe)
        if os.path.isfile(r"C:\ffmpeg\bin\ffprobe.exe"):
            shutil.copy(r"C:\ffmpeg\bin\ffprobe.exe", ffprobe_exe)
            
    static_data = f"{os.path.join(BASE_DIR, 'static')};static"
    ffmpeg_data = f"{ffmpeg_exe};bin"
    ffprobe_data = f"{ffprobe_exe};bin"
    icon_path = os.path.join(BASE_DIR, "app_icon.ico")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--noconsole",
        f"--icon={icon_path}",
        "--name", "Smart_MP3_Merger",
        "--add-data", static_data,
        "--add-data", ffmpeg_data,
        "--add-data", ffprobe_data,
        "--collect-all", "webview",
        "--collect-all", "pythonnet",
        "--collect-all", "clr_loader",
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.filedialog",
        "--hidden-import", "merger_engine",
        "--hidden-import", "server",
        "desktop_app.py"
    ]
    
    print("\nMenjalankan PyInstaller dengan mode GUI Windowed + Custom Icon...")
    res = subprocess.run(cmd, cwd=BASE_DIR)
    
    if res.returncode == 0:
        dist_exe = os.path.join(BASE_DIR, "dist", "Smart_MP3_Merger.exe")
        target_root_exe = os.path.join(BASE_DIR, "Smart_MP3_Merger.exe")
        
        if os.path.isfile(dist_exe):
            shutil.copy(dist_exe, target_root_exe)
            file_size_mb = os.path.getsize(target_root_exe) / (1024 * 1024)
            print("\n" + "=" * 60)
            print(f"[SUKSES] File EXE Portable (Native WebView2) Berhasil Dibuat!")
            print(f"Lokasi: {target_root_exe}")
            print(f"Ukuran: {file_size_mb:.1f} MB")
            print("=" * 60)
        else:
            print("\n[PERINGATAN] File dist tidak ditemukan.")
    else:
        print("\n[GAGAL] Terjadi error saat kompilasi PyInstaller.")


if __name__ == "__main__":
    build_exe()
