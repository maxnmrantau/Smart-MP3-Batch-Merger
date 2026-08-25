@echo off
title Smart MP3 Batch Merger & Randomizer
cd /d "%~dp0"

echo ===================================================
echo   🎵 SMART MP3 BATCH MERGER & RANDOMIZER
echo ===================================================
echo.
echo Memulai server aplikasi lokal di http://localhost:8765 ...
echo.

:: Buka browser secara otomatis setelah 1.5 detik
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:8765"

:: Jalankan server Python
python server.py

pause
