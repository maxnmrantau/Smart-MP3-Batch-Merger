"""
merger_engine.py
Core audio scanning, combinatorics math calculation, batch generation,
and FFmpeg audio processing engine.
Supports standalone portable bundled FFmpeg/FFprobe binaries and system PATH.
"""

import os
import sys
import time
import json
import math
import random
import hashlib
import shutil
import subprocess
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".aac", ".m4a", ".flac", ".ogg", ".wma"}


def get_base_dir() -> str:
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def get_ffprobe_bin() -> str:
    """Finds ffprobe binary from PyInstaller bundle, local directory, or PATH."""
    if hasattr(sys, "_MEIPASS"):
        for p in [os.path.join(sys._MEIPASS, "bin", "ffprobe.exe"), os.path.join(sys._MEIPASS, "ffprobe.exe")]:
            if os.path.isfile(p):
                return p
                
    base = get_base_dir()
    for p in [os.path.join(base, "bin", "ffprobe.exe"), os.path.join(base, "ffprobe.exe")]:
        if os.path.isfile(p):
            return p
            
    if os.path.isfile(r"C:\ffmpeg\bin\ffprobe.exe"):
        return r"C:\ffmpeg\bin\ffprobe.exe"
        
    found = shutil.which("ffprobe")
    return found if found else "ffprobe"


def get_ffmpeg_bin() -> str:
    """Finds ffmpeg binary from PyInstaller bundle, local directory, or PATH."""
    if hasattr(sys, "_MEIPASS"):
        for p in [os.path.join(sys._MEIPASS, "bin", "ffmpeg.exe"), os.path.join(sys._MEIPASS, "ffmpeg.exe")]:
            if os.path.isfile(p):
                return p
                
    base = get_base_dir()
    for p in [os.path.join(base, "bin", "ffmpeg.exe"), os.path.join(base, "ffmpeg.exe")]:
        if os.path.isfile(p):
            return p
            
    if os.path.isfile(r"C:\ffmpeg\bin\ffmpeg.exe"):
        return r"C:\ffmpeg\bin\ffmpeg.exe"
        
    found = shutil.which("ffmpeg")
    return found if found else "ffmpeg"


def get_ffprobe_info(file_path: str) -> Dict[str, Any]:
    """Inspects an audio file using ffprobe to get duration, bitrate, sample rate, etc."""
    ffprobe_cmd = get_ffprobe_bin()
    cmd = [
        ffprobe_cmd,
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        file_path
    ]
    creationflags = 0
    if sys.platform == "win32":
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
    try:
        res = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            creationflags=creationflags
        )
        data = json.loads(res.stdout)
        
        duration = 0.0
        bitrate = 0
        sample_rate = 44100
        channels = 2
        
        format_info = data.get("format", {})
        if "duration" in format_info:
            try:
                duration = float(format_info["duration"])
            except (ValueError, TypeError):
                pass
        if "bit_rate" in format_info:
            try:
                bitrate = int(int(format_info["bit_rate"]) / 1000)
            except (ValueError, TypeError):
                pass
                
        for stream in data.get("streams", []):
            if stream.get("codec_type") == "audio":
                if "sample_rate" in stream:
                    try:
                        sample_rate = int(stream["sample_rate"])
                    except (ValueError, TypeError):
                        pass
                if "channels" in stream:
                    try:
                        channels = int(stream["channels"])
                    except (ValueError, TypeError):
                        pass
                if bitrate == 0 and "bit_rate" in stream:
                    try:
                        bitrate = int(int(stream["bit_rate"]) / 1000)
                    except (ValueError, TypeError):
                        pass
                break
                
        if bitrate <= 0:
            bitrate = 320
            
        return {
            "path": file_path,
            "filename": os.path.basename(file_path),
            "duration": duration,
            "duration_formatted": format_duration(duration),
            "bitrate": bitrate,
            "sample_rate": sample_rate,
            "channels": channels
        }
    except Exception as e:
        return {
            "path": file_path,
            "filename": os.path.basename(file_path),
            "duration": 180.0,
            "duration_formatted": "03:00",
            "bitrate": 320,
            "sample_rate": 44100,
            "channels": 2,
            "note": f"ffprobe error: {str(e)}"
        }


def format_duration(seconds: float) -> str:
    """Formats seconds into MM:SS or HH:MM:SS."""
    sec = int(round(seconds))
    hours = sec // 3600
    minutes = (sec % 3600) // 60
    secs = sec % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def format_timestamp(seconds: float, is_long_format: bool = False) -> str:
    """
    Formats seconds into YouTube-compliant chapter timestamp.
    Starts at 00:00 (or 00:00:00 if is_long_format or hours > 0).
    """
    total_sec = max(0, int(round(seconds)))
    hours = total_sec // 3600
    minutes = (total_sec % 3600) // 60
    secs = total_sec % 60
    if hours > 0 or is_long_format:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def clean_track_title(filename: str) -> str:
    """Removes file extension and cleans up filename for YouTube timestamps."""
    return Path(filename).stem


def generate_youtube_timestamps(
    playlist: List[Dict[str, Any]],
    crossfade_sec: float = 0.0
) -> List[Dict[str, Any]]:
    """Calculates chronological timestamps taking crossfade into account."""
    timestamps = []
    current_sec = 0.0

    total_dur = 0.0
    for i, t in enumerate(playlist):
        d = float(t.get("duration", 0.0))
        if i == 0:
            total_dur += d
        else:
            total_dur += max(0.0, d - crossfade_sec)
    is_long = total_dur >= 3600.0

    for idx, track in enumerate(playlist, start=1):
        clean_title = clean_track_title(track.get("filename", f"Track {idx}"))
        ts_str = format_timestamp(current_sec, is_long_format=is_long)
        track_dur = float(track.get("duration", 0.0))

        timestamps.append({
            "slot": idx,
            "filename": track.get("filename", ""),
            "title": clean_title,
            "start_sec": round(current_sec, 2),
            "timestamp": ts_str,
            "duration": track_dur,
            "duration_formatted": track.get("duration_formatted", format_duration(track_dur)),
            "is_mandatory": bool(track.get("is_mandatory", False))
        })

        current_sec = max(0.0, current_sec + track_dur - crossfade_sec)

    return timestamps


def format_timestamps_text(
    timestamps: List[Dict[str, Any]],
    format_type: str = "youtube"
) -> str:
    """Generates ready-to-copy timestamp text."""
    if format_type == "youtube":
        return "\n".join(f"{t['timestamp']} {t['title']}" for t in timestamps)
    elif format_type == "standard":
        lines = []
        for t in timestamps:
            role = "[WAJIB]" if t.get("is_mandatory") else "[RANDOM]"
            lines.append(f"Slot #{t['slot']:02d} ({t['timestamp']}) {role}: {t['filename']} ({t['duration_formatted']})")
        return "\n".join(lines)
    else:  # "both"
        yt_part = "\n".join(f"{t['timestamp']} {t['title']}" for t in timestamps)
        std_part = "\n".join(f"Slot #{t['slot']:02d} ({t['timestamp']}) {'[WAJIB]' if t.get('is_mandatory') else '[RANDOM]'}: {t['filename']} ({t['duration_formatted']})" for t in timestamps)
        return f"--- TIMESTAMPS YOUTUBE (SIAP COPY KE DESKRIPSI) ---\n{yt_part}\n\n--- DETAIL SLOT BIASA ---\n{std_part}"


def scan_audio_folder(folder_path: str) -> List[Dict[str, Any]]:
    """Scans a directory or a single audio file for supported audio files and inspects metadata."""
    if not folder_path:
        return []
        
    norm_path = os.path.normpath(folder_path.strip().strip('"').strip("'"))
    
    # If a direct file path was provided
    if os.path.isfile(norm_path):
        ext = Path(norm_path).suffix.lower()
        if ext in SUPPORTED_EXTENSIONS:
            info = get_ffprobe_info(norm_path)
            return [info]
        return []
        
    if not os.path.isdir(norm_path):
        return []
        
    audio_files = []
    for entry in sorted(os.scandir(norm_path), key=lambda e: e.name.lower()):
        if entry.is_file():
            ext = Path(entry.name).suffix.lower()
            if ext in SUPPORTED_EXTENSIONS:
                info = get_ffprobe_info(entry.path)
                audio_files.append(info)
                
    return audio_files


def format_combinatorics_display(n: int) -> Dict[str, Any]:
    """
    Formats combinatorics numbers into elegant, compact human-readable strings
    (e.g., 25.200, 14,2 Juta, 3,8 Miliar, 45 Triliun, or ~4,66 × 10⁴⁵ for astronomical scales),
    while preserving the exact integer representation for tooltips and copy actions.
    """
    if not isinstance(n, int) or n <= 0:
        return {
            "short": "0",
            "exact": "0",
            "is_astronomical": False,
            "unit": "Variasi"
        }

    exact_str = f"{n:,}".replace(",", ".")

    # Under 1 Million: exact dot-separated number (e.g. 25.200)
    if n < 1_000_000:
        return {
            "short": exact_str,
            "exact": exact_str,
            "is_astronomical": False,
            "unit": "Variasi"
        }
    # 1 Million to 1 Billion: Juta
    elif n < 1_000_000_000:
        val = n / 1_000_000
        val_str = f"{val:.2f}".rstrip("0").rstrip(".").replace(".", ",")
        return {
            "short": f"{val_str} Juta",
            "exact": exact_str,
            "is_astronomical": False,
            "unit": "Variasi"
        }
    # 1 Billion to 1 Trillion: Miliar
    elif n < 1_000_000_000_000:
        val = n / 1_000_000_000
        val_str = f"{val:.2f}".rstrip("0").rstrip(".").replace(".", ",")
        return {
            "short": f"{val_str} Miliar",
            "exact": exact_str,
            "is_astronomical": False,
            "unit": "Variasi"
        }
    # 1 Trillion to 1 Quadrillion: Triliun
    elif n < 1_000_000_000_000_000:
        val = n / 1_000_000_000_000
        val_str = f"{val:.2f}".rstrip("0").rstrip(".").replace(".", ",")
        return {
            "short": f"{val_str} Triliun",
            "exact": exact_str,
            "is_astronomical": False,
            "unit": "Variasi"
        }
    # 1 Quadrillion to 1 Quintillion: Kuadriliun
    elif n < 1_000_000_000_000_000_000:
        val = n / 1_000_000_000_000_000
        val_str = f"{val:.2f}".rstrip("0").rstrip(".").replace(".", ",")
        return {
            "short": f"{val_str} Kuadriliun",
            "exact": exact_str,
            "is_astronomical": False,
            "unit": "Variasi"
        }
    else:
        # Astronomical scales (>= 10^18): Scientific notation with unicode superscripts
        # e.g. ~4,66 × 10⁴⁵
        s = str(n)
        exp = len(s) - 1
        leading_digits = s[:5] if len(s) >= 5 else s
        raw_mantissa = float(leading_digits) / (10 ** (len(leading_digits) - 1))
        mantissa_rounded = round(raw_mantissa, 2)
        if mantissa_rounded >= 10.0:
            mantissa_rounded = 1.0
            exp += 1
        mantissa_str = f"{mantissa_rounded:.2f}".rstrip("0").rstrip(".").replace(".", ",")
        if mantissa_str == "":
            mantissa_str = "1"

        superscripts = {
            '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
            '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
        }
        exp_str = "".join(superscripts.get(c, c) for c in str(exp))
        short_val = f"~{mantissa_str} × 10{exp_str}"

        return {
            "short": short_val,
            "exact": exact_str,
            "is_astronomical": True,
            "unit": "Variasi (Tak Terbatas)"
        }


def calculate_combinations(
    n_mandatory: int,
    n_random: int,
    songs_per_output: int,
    position_mode: str = "random",  # "start", "end", "random"
    mandatory_mode: str = "all",      # "all", "one"
    mandatory_enabled: bool = True,
    loop_enabled: bool = False,
    loop_target_type: str = "count",
    loop_pool_count: int = 0,
    loop_order: str = "random"
) -> Dict[str, Any]:
    """
    Calculates the exact number of possible unique output combinations/permutations,
    returning both the exact mathematical integer and cleanly formatted strings.
    Supports Mandatory Track ON/OFF and Looping/Random Loop modes.
    """
    if n_random <= 0:
        return {
            "valid": False,
            "total_variations": 0,
            "total_variations_formatted": "0",
            "total_variations_exact": "0",
            "is_astronomical": False,
            "message": "Tidak ada lagu di folder acak (random pool)."
        }

    if mandatory_enabled:
        if n_mandatory <= 0:
            return {
                "valid": False,
                "total_variations": 0,
                "total_variations_formatted": "0",
                "total_variations_exact": "0",
                "is_astronomical": False,
                "message": "Lagu wajib diaktifkan, namun tidak ada file lagu wajib yang terdeteksi."
            }
    else:
        n_mandatory = 0

    if not loop_enabled:
        if mandatory_enabled:
            if mandatory_mode == "all":
                req_mandatory = n_mandatory
                if songs_per_output < req_mandatory:
                    return {
                        "valid": False,
                        "total_variations": 0,
                        "total_variations_formatted": "0",
                        "total_variations_exact": "0",
                        "is_astronomical": False,
                        "message": f"Jumlah lagu per output ({songs_per_output}) lebih sedikit dari jumlah lagu wajib ({req_mandatory})."
                    }
                req_random = songs_per_output - req_mandatory
                if req_random > n_random:
                    return {
                        "valid": False,
                        "total_variations": 0,
                        "total_variations_formatted": "0",
                        "total_variations_exact": "0",
                        "is_astronomical": False,
                        "message": f"Dibutuhkan {req_random} lagu acak per file, tetapi di pool hanya ada {n_random} lagu."
                    }

                random_perms = math.perm(n_random, req_random) if req_random > 0 else 1
                mandatory_perms = math.factorial(req_mandatory)

                if position_mode in ("start", "end"):
                    total_variations = mandatory_perms * random_perms
                    fmt = format_combinatorics_display(total_variations)
                    res_str = f"≈ {fmt['short']} (Tak Terbatas)" if fmt["is_astronomical"] else (f"≈ {fmt['short']}" if total_variations >= 1_000_000_000 else f"= {fmt['exact']}")
                    formula_desc = f"P({n_random}, {req_random}) × {req_mandatory}! {res_str}"
                elif position_mode == "random":
                    slot_combinations = math.comb(songs_per_output, req_mandatory)
                    total_variations = slot_combinations * mandatory_perms * random_perms
                    fmt = format_combinatorics_display(total_variations)
                    res_str = f"≈ {fmt['short']} (Tak Terbatas)" if fmt["is_astronomical"] else (f"≈ {fmt['short']}" if total_variations >= 1_000_000_000 else f"= {fmt['exact']}")
                    formula_desc = f"C({songs_per_output}, {req_mandatory}) × {req_mandatory}! × P({n_random}, {req_random}) {res_str}"

                return {
                    "valid": True,
                    "total_variations": total_variations,
                    "total_variations_formatted": fmt["short"],
                    "total_variations_exact": fmt["exact"],
                    "is_astronomical": fmt["is_astronomical"],
                    "mandatory_per_mix": req_mandatory,
                    "random_per_mix": req_random,
                    "total_songs_per_mix": songs_per_output,
                    "formula_desc": formula_desc,
                    "message": f"Dapat menghasilkan hingga {fmt['short']} variasi file MP3 unik."
                }

            elif mandatory_mode == "one":
                req_mandatory = 1
                if songs_per_output < 1:
                    return {
                        "valid": False,
                        "total_variations": 0,
                        "total_variations_formatted": "0",
                        "total_variations_exact": "0",
                        "is_astronomical": False,
                        "message": "Jumlah lagu per output minimal 1."
                    }
                req_random = songs_per_output - 1
                if req_random > n_random:
                    return {
                        "valid": False,
                        "total_variations": 0,
                        "total_variations_formatted": "0",
                        "total_variations_exact": "0",
                        "is_astronomical": False,
                        "message": f"Dibutuhkan {req_random} lagu acak per file, tetapi di pool hanya ada {n_random} lagu."
                    }

                mandatory_choices = n_mandatory
                random_perms = math.perm(n_random, req_random) if req_random > 0 else 1

                if position_mode in ("start", "end"):
                    total_variations = mandatory_choices * random_perms
                    fmt = format_combinatorics_display(total_variations)
                    res_str = f"≈ {fmt['short']} (Tak Terbatas)" if fmt["is_astronomical"] else (f"≈ {fmt['short']}" if total_variations >= 1_000_000_000 else f"= {fmt['exact']}")
                    formula_desc = f"{n_mandatory} × P({n_random}, {req_random}) {res_str}"
                elif position_mode == "random":
                    total_variations = songs_per_output * mandatory_choices * random_perms
                    fmt = format_combinatorics_display(total_variations)
                    res_str = f"≈ {fmt['short']} (Tak Terbatas)" if fmt["is_astronomical"] else (f"≈ {fmt['short']}" if total_variations >= 1_000_000_000 else f"= {fmt['exact']}")
                    formula_desc = f"{songs_per_output} (slot) × {n_mandatory} × P({n_random}, {req_random}) {res_str}"

                return {
                    "valid": True,
                    "total_variations": total_variations,
                    "total_variations_formatted": fmt["short"],
                    "total_variations_exact": fmt["exact"],
                    "is_astronomical": fmt["is_astronomical"],
                    "mandatory_per_mix": 1,
                    "random_per_mix": req_random,
                    "total_songs_per_mix": songs_per_output,
                    "formula_desc": formula_desc,
                    "message": f"Dapat menghasilkan hingga {fmt['short']} variasi file MP3 unik."
                }
        else:
            # Mandatory is OFF, Loop is OFF
            req_mandatory = 0
            req_random = songs_per_output
            if req_random < 1:
                return {
                    "valid": False,
                    "total_variations": 0,
                    "total_variations_formatted": "0",
                    "total_variations_exact": "0",
                    "is_astronomical": False,
                    "message": "Jumlah lagu per output minimal 1."
                }
            if req_random > n_random:
                return {
                    "valid": False,
                    "total_variations": 0,
                    "total_variations_formatted": "0",
                    "total_variations_exact": "0",
                    "is_astronomical": False,
                    "message": f"Dibutuhkan {req_random} lagu acak per file, tetapi di pool hanya ada {n_random} lagu."
                }

            total_variations = math.perm(n_random, req_random)
            fmt = format_combinatorics_display(total_variations)
            res_str = f"≈ {fmt['short']} (Tak Terbatas)" if fmt["is_astronomical"] else (f"≈ {fmt['short']}" if total_variations >= 1_000_000_000 else f"= {fmt['exact']}")
            formula_desc = f"P({n_random}, {req_random}) {res_str}"

            return {
                "valid": True,
                "total_variations": total_variations,
                "total_variations_formatted": fmt["short"],
                "total_variations_exact": fmt["exact"],
                "is_astronomical": fmt["is_astronomical"],
                "mandatory_per_mix": 0,
                "random_per_mix": req_random,
                "total_songs_per_mix": songs_per_output,
                "formula_desc": formula_desc,
                "message": f"Dapat menghasilkan hingga {fmt['short']} variasi file MP3 unik (Tanpa Lagu Wajib)."
            }

    else:
        # Loop is ENABLED!
        k = loop_pool_count if (0 < loop_pool_count <= n_random) else n_random
        subset_choices = math.comb(n_random, k)

        if mandatory_enabled:
            if mandatory_mode == "all":
                req_mandatory = n_mandatory
                mand_perms = math.factorial(req_mandatory)
            else:
                req_mandatory = 1
                mand_perms = n_mandatory
            req_random = max(1, songs_per_output - req_mandatory)
        else:
            req_mandatory = 0
            mand_perms = 1
            req_random = max(1, songs_per_output)

        if loop_order == "sequential":
            cycle_perms = math.factorial(k)
            pool_perms = subset_choices * cycle_perms
            loop_desc = f"P({n_random}, {k})"
        else:
            if k > 1:
                shuffle_arrangements = k * ((k - 1) ** max(0, req_random - 1))
            else:
                shuffle_arrangements = 1
            pool_perms = subset_choices * shuffle_arrangements
            loop_desc = f"C({n_random}, {k}) × {k}×{max(1, k-1)}^{req_random-1}"

        if mandatory_enabled:
            if position_mode in ("start", "end"):
                total_variations = mand_perms * pool_perms
                formula_desc = f"{mand_perms} (Wajib) × {loop_desc}"
            else:
                slot_comb = math.comb(songs_per_output, req_mandatory)
                total_variations = slot_comb * mand_perms * pool_perms
                formula_desc = f"C({songs_per_output}, {req_mandatory}) × {mand_perms} × {loop_desc}"
        else:
            total_variations = pool_perms
            formula_desc = f"Loop: {loop_desc}"

        fmt = format_combinatorics_display(total_variations)
        res_str = f"≈ {fmt['short']} (Tak Terbatas)" if fmt["is_astronomical"] else (f"≈ {fmt['short']}" if total_variations >= 1_000_000_000 else f"= {fmt['exact']}")
        formula_desc = f"{formula_desc} {res_str}"

        return {
            "valid": True,
            "total_variations": total_variations,
            "total_variations_formatted": fmt["short"],
            "total_variations_exact": fmt["exact"],
            "is_astronomical": fmt["is_astronomical"],
            "mandatory_per_mix": req_mandatory,
            "random_per_mix": req_random,
            "total_songs_per_mix": songs_per_output,
            "formula_desc": formula_desc,
            "message": f"Dapat menghasilkan hingga {fmt['short']} variasi unik dalam mode Loop."
        }


def generate_batch_playlists(
    mandatory_tracks: List[Dict[str, Any]],
    random_tracks: List[Dict[str, Any]],
    songs_per_output: int,
    batch_count: int,
    position_mode: str = "random",
    mandatory_mode: str = "all",
    mandatory_enabled: bool = True,
    loop_enabled: bool = False,
    loop_target_type: str = "count",
    loop_target_duration_sec: float = 3600.0,
    loop_pool_count: int = 0,
    loop_order: str = "random",
    crossfade_sec: float = 0.0
) -> List[List[Dict[str, Any]]]:
    """
    Generates 'batch_count' unique track sequence playlists without duplicates.
    Supports Mandatory Toggle and Looping/Random Loop with target count or duration.
    """
    calc = calculate_combinations(
        n_mandatory=len(mandatory_tracks) if mandatory_enabled else 0,
        n_random=len(random_tracks),
        songs_per_output=songs_per_output,
        position_mode=position_mode,
        mandatory_mode=mandatory_mode,
        mandatory_enabled=mandatory_enabled,
        loop_enabled=loop_enabled,
        loop_target_type=loop_target_type,
        loop_pool_count=loop_pool_count,
        loop_order=loop_order
    )

    if not calc["valid"] or calc["total_variations"] <= 0:
        raise ValueError(calc.get("message", "Konfigurasi tidak valid untuk menghasilkan kombinasi."))

    actual_batch_count = min(batch_count, calc["total_variations"])
    generated_playlists = []
    seen_hashes = set()

    attempts = 0
    max_attempts = max(500, actual_batch_count * 500)

    while len(generated_playlists) < actual_batch_count and attempts < max_attempts:
        attempts += 1

        # 1. Determine mandatory tracks for this mix
        if mandatory_enabled and mandatory_tracks:
            if mandatory_mode == "all":
                chosen_mandatory = list(mandatory_tracks)
                random.shuffle(chosen_mandatory)
            else:
                chosen_mandatory = [random.choice(mandatory_tracks)]
        else:
            chosen_mandatory = []

        # 2. Determine random tracks
        if not loop_enabled:
            req_random = max(0, songs_per_output - len(chosen_mandatory))
            if req_random > 0:
                chosen_random = random.sample(random_tracks, req_random)
            else:
                chosen_random = []
        else:
            # Looping enabled!
            k = loop_pool_count if (0 < loop_pool_count <= len(random_tracks)) else len(random_tracks)
            pool_subset = random.sample(random_tracks, k)

            if loop_target_type == "duration":
                # Duration-based looping
                chosen_random = []
                cur_dur = 0.0
                for i, m in enumerate(chosen_mandatory):
                    d = float(m.get("duration", 180.0))
                    if i == 0:
                        cur_dur += d
                    else:
                        cur_dur += max(0.0, d - crossfade_sec)

                last_path = None
                seq_idx = 0
                cycle_tracks = list(pool_subset)
                random.shuffle(cycle_tracks)
                max_loop_limit = 300

                while (cur_dur < loop_target_duration_sec or len(chosen_random) == 0) and len(chosen_random) < max_loop_limit:
                    if loop_order == "random":
                        candidates = [t for t in pool_subset if t["path"] != last_path] if len(pool_subset) > 1 else pool_subset
                        next_track = random.choice(candidates)
                    else:
                        next_track = cycle_tracks[seq_idx % len(cycle_tracks)]
                        seq_idx += 1

                    chosen_random.append(next_track)
                    last_path = next_track["path"]
                    t_dur = float(next_track.get("duration", 180.0))
                    if len(chosen_random) == 1 and len(chosen_mandatory) == 0:
                        cur_dur += t_dur
                    else:
                        cur_dur += max(0.0, t_dur - crossfade_sec)
            else:
                # Count-based looping
                req_random = max(0, songs_per_output - len(chosen_mandatory))
                chosen_random = []
                if req_random > 0:
                    if loop_order == "random":
                        last_path = None
                        for _ in range(req_random):
                            candidates = [t for t in pool_subset if t["path"] != last_path] if len(pool_subset) > 1 else pool_subset
                            next_track = random.choice(candidates)
                            chosen_random.append(next_track)
                            last_path = next_track["path"]
                    else:
                        cycle_tracks = list(pool_subset)
                        random.shuffle(cycle_tracks)
                        for i in range(req_random):
                            chosen_random.append(cycle_tracks[i % len(cycle_tracks)])

        # 3. Assemble full playlist
        playlist = []
        if chosen_mandatory:
            if position_mode == "start":
                playlist = chosen_mandatory + chosen_random
            elif position_mode == "end":
                playlist = chosen_random + chosen_mandatory
            elif position_mode == "random":
                playlist = list(chosen_random)
                for m_track in chosen_mandatory:
                    insert_idx = random.randint(0, len(playlist))
                    playlist.insert(insert_idx, m_track)
        else:
            playlist = list(chosen_random)

        # 4. Anti-duplicate signature hash
        sig = "|".join([t["path"] for t in playlist])
        sig_hash = hashlib.sha256(sig.encode("utf-8")).hexdigest()

        if sig_hash not in seen_hashes:
            seen_hashes.add(sig_hash)
            tagged_playlist = []
            for track in playlist:
                is_mand = bool(mandatory_enabled and any(track["path"] == m["path"] for m in mandatory_tracks))
                track_copy = dict(track)
                track_copy["is_mandatory"] = is_mand
                tagged_playlist.append(track_copy)
            generated_playlists.append(tagged_playlist)

    if not generated_playlists and attempts >= max_attempts:
        raise ValueError("Gagal menghasilkan playlist unik setelah beberapa percobaan. Coba kurangi jumlah batch atau ubah pengaturan.")

    return generated_playlists
            
    return generated_playlists


def merge_playlist_to_mp3(
    playlist: List[Dict[str, Any]],
    output_filepath: str,
    target_bitrate: int = 320,
    target_sample_rate: int = 44100,
    crossfade_sec: float = 0.0,
    normalize_volume: bool = False,
    cancel_event: Optional[Any] = None,
    proc_holder: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Merges a list of audio files into a single MP3 file using FFmpeg with high efficiency.
    Supports graceful real-time cancellation and active process termination.
    """
    if cancel_event and getattr(cancel_event, "is_set", lambda: False)():
        raise InterruptedError("Proses merge dibatalkan oleh pengguna.")

    ffmpeg_cmd = get_ffmpeg_bin()
    os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
    n = len(playlist)
    if n == 0:
        raise ValueError("Playlist kosong.")
        
    if n == 1:
        cmd = [
            ffmpeg_cmd, "-y",
            "-i", playlist[0]["path"],
            "-c:a", "libmp3lame",
            "-b:a", f"{target_bitrate}k",
            "-ar", str(target_sample_rate),
            output_filepath
        ]
    else:
        input_args = []
        for track in playlist:
            input_args.extend(["-i", track["path"]])
            
        # Standardize each stream to target sample rate and stereo layout
        # to prevent sample rate / channel layout mismatch errors in concat or acrossfade
        resample_filters = []
        for i in range(n):
            resample_filters.append(f"[{i}:a]aformat=sample_rates={target_sample_rate}:channel_layouts=stereo[s{i}]")
        resample_str = ";".join(resample_filters)

        if crossfade_sec > 0 and n > 1:
            filter_parts = [resample_str]
            last_label = "s0"
            for i in range(1, n):
                out_label = f"cf{i}" if i < n - 1 else "outa"
                filter_parts.append(f"[{last_label}][s{i}]acrossfade=d={crossfade_sec}:c1=tri:c2=tri[{out_label}]")
                last_label = out_label
            filter_complex = ";".join(filter_parts)
        else:
            stream_inputs = "".join([f"[s{i}]" for i in range(n)])
            filter_complex = f"{resample_str};{stream_inputs}concat=n={n}:v=0:a=1[outa]"
            
        audio_filters = []
        if normalize_volume:
            audio_filters.append("loudnorm=I=-16:LRA=11:TP=-1.5")
            
        if audio_filters:
            filter_complex += f";[outa]{','.join(audio_filters)}[finala]"
            map_target = "[finala]"
        else:
            map_target = "[outa]"
            
        cmd = [
            ffmpeg_cmd, "-y",
            *input_args,
            "-filter_complex", filter_complex,
            "-map", map_target,
            "-c:a", "libmp3lame",
            "-b:a", f"{target_bitrate}k",
            "-ar", str(target_sample_rate),
            output_filepath
        ]
    
    creationflags = 0
    if sys.platform == "win32":
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=creationflags
    )

    if proc_holder is not None:
        proc_holder["proc"] = proc

    stderr_chunks = []
    def _drain_stderr():
        try:
            for line in iter(proc.stderr.readline, ''):
                if line:
                    stderr_chunks.append(line)
        except Exception:
            pass

    t_err = threading.Thread(target=_drain_stderr, daemon=True)
    t_err.start()

    cancelled = False
    try:
        while True:
            ret = proc.poll()
            if ret is not None:
                break
            if cancel_event and getattr(cancel_event, "is_set", lambda: False)():
                cancelled = True
                try:
                    proc.terminate()
                    proc.wait(timeout=1.5)
                except Exception:
                    try:
                        proc.kill()
                    except Exception:
                        pass
                break
            time.sleep(0.08)
    finally:
        if proc_holder is not None:
            proc_holder["proc"] = None

    t_err.join(timeout=2.0)

    if cancelled:
        if os.path.isfile(output_filepath):
            try:
                os.remove(output_filepath)
            except Exception:
                pass
        raise InterruptedError("Proses merge dibatalkan oleh pengguna.")

    if proc.returncode != 0:
        err_msg = "".join(stderr_chunks[-25:]) if stderr_chunks else "Unknown FFmpeg error"
        raise RuntimeError(f"FFmpeg error: {err_msg}")
        
    return get_ffprobe_info(output_filepath)
