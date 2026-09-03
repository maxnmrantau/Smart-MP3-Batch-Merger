"""
server.py
Lightweight multi-threaded Python web server for the Smart MP3 Batch Merger application.
Supports direct local path scanning, HTML5 browser uploads, and Windows Explorer shortcuts.
Works both standalone (.py) and compiled (PyInstaller .exe).
"""

import os
import sys

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import json
import time
import queue
import urllib.parse
import threading
import subprocess
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, Any, List

import merger_engine

PORT = 8765

if getattr(sys, 'frozen', False):
    # Running in PyInstaller bundle
    RUNNING_DIR = os.path.dirname(sys.executable)
    BUNDLE_DIR = getattr(sys, '_MEIPASS', RUNNING_DIR)
    STATIC_DIR = os.path.join(BUNDLE_DIR, "static")
    BASE_DIR = RUNNING_DIR
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, "static")

# Workspace input folders for browser-selected files
WORKSPACE_INPUTS_DIR = os.path.join(BASE_DIR, "workspace_inputs")
WORKSPACE_MANDATORY_DIR = os.path.join(WORKSPACE_INPUTS_DIR, "mandatory")
WORKSPACE_RANDOM_DIR = os.path.join(WORKSPACE_INPUTS_DIR, "random")
WORKSPACE_OUTPUT_DIR = os.path.join(BASE_DIR, "output_merged_tracks")

os.makedirs(WORKSPACE_MANDATORY_DIR, exist_ok=True)
os.makedirs(WORKSPACE_RANDOM_DIR, exist_ok=True)
os.makedirs(WORKSPACE_OUTPUT_DIR, exist_ok=True)

# Global state for merge background task
merge_cancel_event = threading.Event()
merge_proc_holder: Dict[str, Any] = {"proc": None}
merge_task_state = {
    "is_running": False,
    "cancel_requested": False,
    "current_index": 0,
    "total_files": 0,
    "current_filename": "",
    "current_track_info": "",
    "progress_percent": 0,
    "completed_files": [],
    "logs": [],
    "error": None
}
state_lock = threading.Lock()

# Global state for async (non-blocking) folder dialog
_folder_dialog_lock = threading.Lock()
_folder_dialog_state = {
    "running": False,   # True while dialog is open
    "result": None,     # None = not done yet, "" = cancelled, "path" = selected
}


def _run_folder_dialog_sync(title: str) -> str:
    """Runs native Windows folder dialog using Tkinter topmost as primary, with PowerShell topmost fallback."""
    # 1. Primary: Tkinter with topmost window (instant, native, zero delay)
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes("-topmost", 1)
        root.focus_force()
        folder = filedialog.askdirectory(title=title)
        root.destroy()
        if folder and os.path.isdir(folder):
            return os.path.normpath(folder)
        return ""  # User cancelled
    except Exception as e:
        print(f"[FolderDialog] Tkinter error, trying PowerShell: {e}")

    # 2. Fallback: PowerShell with TopMost form
    if sys.platform == "win32":
        try:
            ps_script = (
                'Add-Type -AssemblyName System.Windows.Forms; '
                '$d = New-Object System.Windows.Forms.FolderBrowserDialog; '
                f'$d.Description = "{title}"; '
                '$d.ShowNewFolderButton = $true; '
                '$top = New-Object System.Windows.Forms.Form; '
                '$top.TopMost = $true; '
                '$top.StartPosition = "CenterScreen"; '
                'if ($d.ShowDialog($top) -eq [System.Windows.Forms.DialogResult]::OK) {{ Write-Output $d.SelectedPath }}; '
                '$top.Dispose()'
            )
            creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_script],
                capture_output=True,
                text=True,
                creationflags=creationflags,
                timeout=120
            )
            if res.returncode == 0:
                selected = res.stdout.strip()
                if selected and os.path.isdir(selected):
                    return os.path.normpath(selected)
                return ""
        except Exception as e:
            print(f"[FolderDialog] PowerShell error: {e}")

    return ""


def _start_folder_dialog_thread(title: str):
    """Launches the folder dialog in a background thread so the HTTP server stays responsive."""
    global _folder_dialog_state
    with _folder_dialog_lock:
        if _folder_dialog_state["running"]:
            return  # already open
        _folder_dialog_state["running"] = True
        _folder_dialog_state["result"] = None

    def _worker():
        global _folder_dialog_state
        result = _run_folder_dialog_sync(title)
        with _folder_dialog_lock:
            _folder_dialog_state["result"] = result
            _folder_dialog_state["running"] = False

    t = threading.Thread(target=_worker, daemon=True)
    t.start()


def _run_file_dialog_sync(title: str = "Pilih File Audio") -> str:
    """Runs native Windows file picker dialog using Tkinter topmost window."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes("-topmost", 1)
        root.focus_force()
        file_path = filedialog.askopenfilename(
            title=title,
            filetypes=[
                ("Audio Files (*.mp3, *.wav, *.m4a, *.aac, *.flac, *.ogg)", "*.mp3;*.wav;*.m4a;*.aac;*.flac;*.ogg;*.wma"),
                ("All Files (*.*)", "*.*")
            ]
        )
        root.destroy()
        if file_path and os.path.isfile(file_path):
            return os.path.normpath(file_path)
        return ""
    except Exception as e:
        print(f"[FileDialog] Tkinter error: {e}")
        return ""


def _start_file_dialog_thread(title: str = "Pilih File Audio"):
    """Launches the file dialog in a background thread so the HTTP server stays responsive."""
    global _folder_dialog_state
    with _folder_dialog_lock:
        if _folder_dialog_state["running"]:
            return
        _folder_dialog_state["running"] = True
        _folder_dialog_state["result"] = None

    def _worker():
        global _folder_dialog_state
        result = _run_file_dialog_sync(title)
        with _folder_dialog_lock:
            _folder_dialog_state["result"] = result
            _folder_dialog_state["running"] = False

    t = threading.Thread(target=_worker, daemon=True)
    t.start()


def background_merge_worker(config: Dict[str, Any]):
    """Background worker thread that runs the batch merging process."""
    global merge_task_state
    
    merge_cancel_event.clear()
    with state_lock:
        merge_task_state["is_running"] = True
        merge_task_state["cancel_requested"] = False
        merge_task_state["current_index"] = 0
        merge_task_state["total_files"] = 0
        merge_task_state["progress_percent"] = 0
        merge_task_state["completed_files"] = []
        merge_task_state["logs"] = []
        merge_task_state["error"] = None
        
    try:
        mandatory_folder = config.get("mandatory_folder", "") or WORKSPACE_MANDATORY_DIR
        random_folder = config.get("random_folder", "") or WORKSPACE_RANDOM_DIR
        output_folder = config.get("output_folder", "") or WORKSPACE_OUTPUT_DIR
        songs_per_output = int(config.get("songs_per_output", 5))
        batch_count = int(config.get("batch_count", 5))
        position_mode = config.get("position_mode", "random")
        mandatory_mode = config.get("mandatory_mode", "all")
        crossfade_sec = float(config.get("crossfade_sec", 0.0))
        target_bitrate = int(config.get("target_bitrate", 320))
        target_sample_rate = int(config.get("target_sample_rate", 44100))
        output_prefix = config.get("output_prefix", "Mix_Merged")
        
        # 1. Scan folders
        mandatory_tracks = merger_engine.scan_audio_folder(mandatory_folder)
        random_tracks = merger_engine.scan_audio_folder(random_folder)
        
        if not mandatory_tracks:
            raise ValueError(f"Tidak ada file audio ditemukan di Folder Lagu Wajib: {mandatory_folder}")
        if not random_tracks:
            raise ValueError(f"Tidak ada file audio ditemukan di Folder Lagu Random: {random_folder}")
            
        os.makedirs(output_folder, exist_ok=True)
        
        # 2. Generate batch playlists
        playlists = merger_engine.generate_batch_playlists(
            mandatory_tracks=mandatory_tracks,
            random_tracks=random_tracks,
            songs_per_output=songs_per_output,
            batch_count=batch_count,
            position_mode=position_mode,
            mandatory_mode=mandatory_mode
        )
        
        total_batches = len(playlists)
        with state_lock:
            merge_task_state["total_files"] = total_batches
            merge_task_state["logs"].append(f"Berhasil merancang {total_batches} kombinasi playlist unik anti-duplikat.")
            
        summary_log_lines = [
            "=" * 70,
            f" SMART MP3 MERGER - SUMMARY BATCH REPORT",
            f" Tanggal & Waktu: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f" Total File Dihasilkan: {total_batches} File",
            f" Posisi Lagu Wajib: {position_mode.upper()} | Mode: {mandatory_mode.upper()}",
            f" Bitrate Output: {target_bitrate} kbps | Crossfade: {crossfade_sec}s",
            "=" * 70,
            ""
        ]
        
        # 3. Process each playlist sequentially to keep RAM minimal (~50MB)
        for idx, pl in enumerate(playlists, start=1):
            if merge_cancel_event.is_set():
                raise InterruptedError("Proses merge dibatalkan oleh pengguna.")

            out_name = f"{output_prefix}_{idx:02d}_{songs_per_output}Songs.mp3"
            out_path = os.path.join(output_folder, out_name)
            
            with state_lock:
                merge_task_state["current_index"] = idx
                merge_task_state["current_filename"] = out_name
                merge_task_state["progress_percent"] = int(((idx - 1) / total_batches) * 100)
                track_names = [f"#{i+1}: {t['filename']}{' (WAJIB)' if t.get('is_mandatory') else ''}" for i, t in enumerate(pl)]
                merge_task_state["current_track_info"] = " -> ".join(track_names)
                merge_task_state["logs"].append(f"[{idx}/{total_batches}] Memproses '{out_name}' ({len(pl)} lagu)...")
                
            # Perform merge with FFmpeg
            file_info = merger_engine.merge_playlist_to_mp3(
                playlist=pl,
                output_filepath=out_path,
                target_bitrate=target_bitrate,
                target_sample_rate=target_sample_rate,
                crossfade_sec=crossfade_sec,
                cancel_event=merge_cancel_event,
                proc_holder=merge_proc_holder
            )
            
            # Record summary line
            summary_log_lines.append(f"[{idx:02d}] {out_name} (Durasi: {file_info['duration_formatted']}, Bitrate: {file_info['bitrate']}k)")
            for s_idx, s_track in enumerate(pl, start=1):
                role_tag = "[WAJIB]" if s_track.get("is_mandatory") else "[RANDOM]"
                summary_log_lines.append(f"     Slot #{s_idx} {role_tag}: {s_track['filename']} ({s_track['duration_formatted']})")
            summary_log_lines.append("-" * 50)
            
            with state_lock:
                merge_task_state["completed_files"].append({
                    "index": idx,
                    "filename": out_name,
                    "path": out_path,
                    "duration": file_info["duration"],
                    "duration_formatted": file_info["duration_formatted"],
                    "bitrate": file_info["bitrate"],
                    "playlist_details": pl
                })
                merge_task_state["progress_percent"] = int((idx / total_batches) * 100)
                merge_task_state["logs"].append(f"[OK] Selesai: '{out_name}' ({file_info['duration_formatted']})")
                
        # Write summary file to output folder
        summary_path = os.path.join(output_folder, "playlist_summary.txt")
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("\n".join(summary_log_lines))
            
        with state_lock:
            merge_task_state["logs"].append(f"[OK] Laporan urutan lagu disimpan di: {os.path.basename(summary_path)}")
            merge_task_state["progress_percent"] = 100
            
    except InterruptedError:
        with state_lock:
            merge_task_state["error"] = "Proses dibatalkan oleh pengguna."
            merge_task_state["logs"].append("🛑 [BATAL] Penggabungan audio dihentikan atas permintaan pengguna.")
    except Exception as e:
        with state_lock:
            merge_task_state["error"] = str(e)
            merge_task_state["logs"].append(f"[ERROR] Terjadi kesalahan: {str(e)}")
    finally:
        with state_lock:
            merge_task_state["is_running"] = False
            merge_task_state["cancel_requested"] = False
        merge_cancel_event.clear()
        merge_proc_holder["proc"] = None


class AppRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler serving API requests and static assets."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)
        
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        # Prevent browser from caching static files so code changes take effect immediately
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
        
    def _send_json(self, data: Any, status_code: int = 200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        
    def _parse_post_json(self) -> Dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        if not body:
            return {}
        try:
            return json.loads(body)
        except Exception:
            return {}
            
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path == "/api/status":
            with state_lock:
                self._send_json(merge_task_state)
            return
            
        elif path == "/api/defaults":
            self._send_json({
                "mandatory_folder": WORKSPACE_MANDATORY_DIR,
                "random_folder": WORKSPACE_RANDOM_DIR,
                "output_folder": WORKSPACE_OUTPUT_DIR
            })
            return
            
        elif path == "/api/audio-preview":
            query = urllib.parse.parse_qs(parsed.query)
            file_path = query.get("path", [""])[0]
            if file_path and os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.send_header("Content-Length", str(file_size))
                self.send_header("Accept-Ranges", "bytes")
                self.end_headers()
                with open(file_path, "rb") as f:
                    while chunk := f.read(64 * 1024):
                        self.wfile.write(chunk)
                return
            else:
                self.send_error(404, "File audio tidak ditemukan")
                return
                
        # Serve static assets
        super().do_GET()
        
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path == "/api/browse-folder":
            # Non-blocking: launch dialog in background thread and return immediately.
            # Browser then polls /api/browse-folder-result.
            data = self._parse_post_json()
            title = data.get("title", "Pilih Folder")
            with _folder_dialog_lock:
                already_running = _folder_dialog_state["running"]
            if not already_running:
                _start_folder_dialog_thread(title)
            self._send_json({"status": "opening"})
            return

        if path == "/api/browse-file":
            # Non-blocking: launch native file picker dialog in background thread.
            data = self._parse_post_json()
            title = data.get("title", "Pilih File Audio")
            with _folder_dialog_lock:
                already_running = _folder_dialog_state["running"]
            if not already_running:
                _start_file_dialog_thread(title)
            self._send_json({"status": "opening"})
            return

        if path == "/api/browse-folder-result":
            # Returns the dialog result; "pending" while dialog is still open.
            with _folder_dialog_lock:
                running = _folder_dialog_state["running"]
                result = _folder_dialog_state["result"]
            if running or result is None:
                self._send_json({"status": "pending"})
            else:
                # Clear result so next call to browse works fresh
                with _folder_dialog_lock:
                    _folder_dialog_state["result"] = None
                self._send_json({"status": "done", "folder": result})
            return
            
        elif path == "/api/upload-files":
            query = urllib.parse.parse_qs(parsed.query)
            target = query.get("target", ["mandatory"])[0]
            filename = query.get("filename", ["audio.mp3"])[0]
            
            save_dir = WORKSPACE_MANDATORY_DIR if target == "mandatory" else WORKSPACE_RANDOM_DIR
            os.makedirs(save_dir, exist_ok=True)
            
            safe_filename = os.path.basename(filename)
            out_file_path = os.path.join(save_dir, safe_filename)
            
            content_length = int(self.headers.get("Content-Length", 0))
            with open(out_file_path, "wb") as f:
                bytes_left = content_length
                while bytes_left > 0:
                    chunk = self.rfile.read(min(bytes_left, 64 * 1024))
                    if not chunk:
                        break
                    f.write(chunk)
                    bytes_left -= len(chunk)
                    
            self._send_json({
                "status": "uploaded",
                "folder": save_dir,
                "filename": safe_filename,
                "path": out_file_path
            })
            return
            
        elif path == "/api/clear-folder":
            data = self._parse_post_json()
            target = data.get("target", "mandatory")
            clear_dir = WORKSPACE_MANDATORY_DIR if target == "mandatory" else WORKSPACE_RANDOM_DIR
            os.makedirs(clear_dir, exist_ok=True)
            for f in os.listdir(clear_dir):
                fp = os.path.join(clear_dir, f)
                if os.path.isfile(fp):
                    try:
                        os.remove(fp)
                    except Exception:
                        pass
            self._send_json({"status": "cleared", "folder": clear_dir})
            return
            
        elif path == "/api/scan-folders":
            data = self._parse_post_json()
            mandatory_folder = data.get("mandatory_folder", "").strip() or WORKSPACE_MANDATORY_DIR
            random_folder = data.get("random_folder", "").strip() or WORKSPACE_RANDOM_DIR
            
            mandatory_tracks = merger_engine.scan_audio_folder(mandatory_folder)
            random_tracks = merger_engine.scan_audio_folder(random_folder)
            
            all_bitrates = [t["bitrate"] for t in mandatory_tracks + random_tracks if t.get("bitrate")]
            detected_bitrate = max(all_bitrates) if all_bitrates else 320
            
            all_sample_rates = [t["sample_rate"] for t in mandatory_tracks + random_tracks if t.get("sample_rate")]
            detected_sample_rate = max(all_sample_rates) if all_sample_rates else 44100
            
            self._send_json({
                "mandatory_folder": mandatory_folder,
                "mandatory_count": len(mandatory_tracks),
                "mandatory_tracks": mandatory_tracks,
                "random_folder": random_folder,
                "random_count": len(random_tracks),
                "random_tracks": random_tracks,
                "detected_bitrate": detected_bitrate,
                "detected_sample_rate": detected_sample_rate,
                "total_pool_tracks": len(mandatory_tracks) + len(random_tracks)
            })
            return
            
        elif path == "/api/calculate":
            data = self._parse_post_json()
            n_mandatory = int(data.get("n_mandatory", 0))
            n_random = int(data.get("n_random", 0))
            songs_per_output = int(data.get("songs_per_output", 5))
            position_mode = data.get("position_mode", "random")
            mandatory_mode = data.get("mandatory_mode", "all")
            
            result = merger_engine.calculate_combinations(
                n_mandatory=n_mandatory,
                n_random=n_random,
                songs_per_output=songs_per_output,
                position_mode=position_mode,
                mandatory_mode=mandatory_mode
            )
            self._send_json(result)
            return
            
        elif path == "/api/start-merge":
            with state_lock:
                if merge_task_state["is_running"]:
                    self._send_json({"error": "Proses merge sebelumnya masih berjalan."}, status_code=400)
                    return
                    
            config = self._parse_post_json()
            worker_thread = threading.Thread(target=background_merge_worker, args=(config,), daemon=True)
            worker_thread.start()
            self._send_json({"status": "started", "message": "Proses merge batch telah dimulai."})
            return
            
        elif path == "/api/cancel-merge":
            with state_lock:
                if merge_task_state["is_running"]:
                    merge_task_state["cancel_requested"] = True
                    merge_cancel_event.set()
                    proc = merge_proc_holder.get("proc")
                    if proc and proc.poll() is None:
                        try:
                            proc.terminate()
                        except Exception:
                            pass
                    merge_task_state["logs"].append("⚠️ Permintaan pembatalan diterima. Menghentikan proses...")
                    self._send_json({"status": "cancelling", "message": "Proses pembatalan dikirim."})
                    return
            self._send_json({"status": "idle", "message": "Tidak ada proses yang sedang berjalan."})
            return
            
        elif path == "/api/open-output-folder":
            data = self._parse_post_json()
            folder_path = data.get("folder", "").strip() or WORKSPACE_OUTPUT_DIR
            folder_path = os.path.abspath(folder_path)
            os.makedirs(folder_path, exist_ok=True)
            
            try:
                if sys.platform == "win32":
                    os.startfile(folder_path)
                elif sys.platform == "darwin":
                    subprocess.run(["open", folder_path])
                else:
                    subprocess.run(["xdg-open", folder_path])
                self._send_json({"status": "opened", "path": folder_path})
            except Exception as e:
                self._send_json({"error": str(e)}, status_code=500)
            return
            
        self.send_error(404, "Endpoint not found")


HOST = "127.0.0.1"
PORT = 8765


def start_server_in_thread(host: str = HOST, port: int = PORT):
    """Starts the HTTP server inside a background thread (for single-exe operation)."""
    os.makedirs(STATIC_DIR, exist_ok=True)
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, AppRequestHandler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd


def start_server(host: str = HOST, port: int = PORT):
    os.makedirs(STATIC_DIR, exist_ok=True)
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, AppRequestHandler)
    print("=" * 60)
    print("SMART MP3 BATCH MERGER SERVER BERJALAN")
    print(f"Buka URL di Browser: http://{host}:{port}")
    print("=" * 60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nMematikan server...")
        httpd.shutdown()


if __name__ == "__main__":
    start_server()
