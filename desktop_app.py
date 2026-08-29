"""
desktop_app.py
Dedicated Native Desktop Window launcher for Smart MP3 Batch Merger using pywebview (Microsoft WebView2).
Opens the application as a standalone native desktop software window.
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

HOST = "127.0.0.1"
PORT = 8765
APP_URL = f"http://{HOST}:{PORT}"


def is_server_running(url: str = APP_URL) -> bool:
    """Checks if the local server is already running and healthy."""
    try:
        req = urllib.request.Request(f"{url}/api/status", headers={"User-Agent": "MP3MergerDesktop"})
        with urllib.request.urlopen(req, timeout=1.0) as resp:
            return resp.status == 200
    except Exception:
        return False


def ensure_server() -> str:
    """Starts internal server thread if not active and waits until ready."""
    if not is_server_running(APP_URL):
        server.start_server_in_thread(host=HOST, port=PORT)
        for _ in range(60):  # Wait up to 6 seconds (reliable even after cold PC boot)
            time.sleep(0.1)
            if is_server_running(APP_URL):
                break
    return APP_URL


def launch_native_webview():
    """Launches the dedicated native desktop window via pywebview (Edge WebView2)."""
    import webview
    
    app_url = ensure_server()
    
    # Configure and create the native OS window
    webview.create_window(
        title="Smart MP3 Batch Merger & Randomizer",
        url=app_url,
        width=1340,
        height=880,
        min_size=(1000, 680),
        resizable=True,
        zoomable=False,
        text_select=True,
        confirm_close=False,
        background_color="#0F172A"  # Matches dark slate theme to avoid white flash
    )
    
    # Start WebView2 engine
    webview.start(gui="edgechromium", private_mode=False)


def launch_fallback_browser():
    """Fallback launcher using Edge App Mode if pywebview is unavailable."""
    app_url = ensure_server()
    
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe")
    ]
    
    browser_exe = ""
    for path in candidates:
        if os.path.isfile(path):
            browser_exe = path
            break
            
    if not browser_exe:
        for name in ["msedge", "chrome", "brave"]:
            found = shutil.which(name)
            if found:
                browser_exe = found
                break
                
    temp_profile = os.path.join(os.environ.get("TEMP", os.path.expanduser("~")), "MP3_Merger_Desktop_Profile")
    os.makedirs(temp_profile, exist_ok=True)
    
    if browser_exe:
        cmd = [
            browser_exe,
            f"--app={app_url}",
            "--window-size=1340,880",
            f"--user-data-dir={temp_profile}",
            "--no-first-run",
            "--no-default-browser-check",
            "--no-proxy-server",
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
        webbrowser.open(app_url)


def launch_desktop_window():
    """Tries launching via pywebview Native WebView2 first; falls back to Edge App mode if needed."""
    try:
        launch_native_webview()
    except Exception as e:
        print(f"[Launcher] pywebview native launch encountered error, fallback: {e}")
        launch_fallback_browser()


if __name__ == "__main__":
    launch_desktop_window()
