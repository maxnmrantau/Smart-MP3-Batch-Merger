"""
desktop_app.py
Dedicated Native Desktop Window launcher for Smart MP3 Batch Merger.
Opens the application as a standalone desktop software window (no browser tabs/address bar, no console window, strictly locked scale).
"""

import os
import sys
import time
import shutil
import urllib.request
import subprocess
import threading
from pathlib import Path

# Ensure UTF-8 output on Windows console if console is attached
if sys.platform == "win32":
    try:
        if sys.stdout is not None:
            sys.stdout.reconfigure(encoding='utf-8')
        if sys.stderr is not None:
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import server

PORT = 8765
APP_URL = f"http://localhost:{PORT}"


def is_server_running() -> bool:
    """Checks if the local server is already running and healthy."""
    try:
        req = urllib.request.Request(f"{APP_URL}/api/status", headers={"User-Agent": "MP3MergerDesktop"})
        with urllib.request.urlopen(req, timeout=0.8) as resp:
            return resp.status == 200
    except Exception:
        return False


def ensure_server():
    """Starts internal server thread if not active."""
    if not is_server_running():
        server.start_server_in_thread()
        for _ in range(30):
            time.sleep(0.1)
            if is_server_running():
                break


def find_desktop_browser_executable() -> str:
    """Finds the path to Edge or Chrome to run in dedicated standalone App Mode."""
    candidates = [
        # Microsoft Edge (Standard on all Windows 10/11)
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
        # Google Chrome
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        # Brave Browser
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe")
    ]
    
    for path in candidates:
        if os.path.isfile(path):
            return path
            
    for name in ["msedge", "chrome", "brave"]:
        found = shutil.which(name)
        if found:
            return found
            
    return ""


def launch_desktop_window():
    """Launches the dedicated standalone Desktop Window with strict no-zoom & no-pinch lockdown."""
    ensure_server()
    
    browser_exe = find_desktop_browser_executable()
    temp_profile = os.path.join(os.environ.get("TEMP", os.path.expanduser("~")), "MP3_Merger_Desktop_Profile")
    os.makedirs(temp_profile, exist_ok=True)
    
    if browser_exe:
        cmd = [
            browser_exe,
            f"--app={APP_URL}",
            "--window-size=1340,880",
            f"--user-data-dir={temp_profile}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-pinch",
            "--disable-features=TouchpadAndWheelScrollLatching,OverscrollHistoryNavigation",
            "--overscroll-history-navigation=0"
        ]
        
        creationflags = 0
        if sys.platform == "win32":
            creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
            
        proc = subprocess.Popen(cmd, creationflags=creationflags)
        proc.wait()
    else:
        import webbrowser
        webbrowser.open(APP_URL)


if __name__ == "__main__":
    launch_desktop_window()
