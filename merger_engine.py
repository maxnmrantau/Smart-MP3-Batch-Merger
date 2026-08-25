"""
merger_engine.py
Core audio scanning, combinatorics math calculation, batch generation,
and FFmpeg audio processing engine.
Supports standalone portable bundled FFmpeg/FFprobe binaries and system PATH.
"""

import os
import sys
import json
import math
import random
import hashlib
import shutil
import subprocess
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
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
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
    sec = int(seconds)
    hours = sec // 3600
    minutes = (sec % 3600) // 60
    secs = sec % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def scan_audio_folder(folder_path: str) -> List[Dict[str, Any]]:
    """Scans a directory for all supported audio files and inspects metadata."""
    if not folder_path or not os.path.isdir(folder_path):
        return []
        
    audio_files = []
    for entry in sorted(os.scandir(folder_path), key=lambda e: e.name.lower()):
        if entry.is_file():
            ext = Path(entry.name).suffix.lower()
            if ext in SUPPORTED_EXTENSIONS:
                info = get_ffprobe_info(entry.path)
                audio_files.append(info)
                
    return audio_files


def calculate_combinations(
    n_mandatory: int,
    n_random: int,
    songs_per_output: int,
    position_mode: str = "random", # "start", "end", "random"
    mandatory_mode: str = "all"     # "all", "one"
) -> Dict[str, Any]:
    """
    Calculates the exact number of possible unique output combinations/permutations.
    """
    if n_mandatory <= 0:
        return {
            "valid": False,
            "total_variations": 0,
            "message": "Tidak ada lagu wajib yang terdeteksi."
        }
    if n_random <= 0:
        return {
            "valid": False,
            "total_variations": 0,
            "message": "Tidak ada lagu di folder acak (random pool)."
        }
        
    if mandatory_mode == "all":
        req_mandatory = n_mandatory
        if songs_per_output < req_mandatory:
            return {
                "valid": False,
                "total_variations": 0,
                "message": f"Jumlah lagu per output ({songs_per_output}) lebih sedikit dari jumlah lagu wajib ({req_mandatory})."
            }
        req_random = songs_per_output - req_mandatory
        if req_random > n_random:
            return {
                "valid": False,
                "total_variations": 0,
                "message": f"Dibutuhkan {req_random} lagu acak per file, tetapi di pool hanya ada {n_random} lagu."
            }
            
        random_perms = math.perm(n_random, req_random) if req_random > 0 else 1
        mandatory_perms = math.factorial(req_mandatory)
        
        if position_mode in ("start", "end"):
            total_variations = mandatory_perms * random_perms
            formula_desc = f"P({n_random}, {req_random}) × {req_mandatory}! = {total_variations:,}"
        elif position_mode == "random":
            slot_combinations = math.comb(songs_per_output, req_mandatory)
            total_variations = slot_combinations * mandatory_perms * random_perms
            formula_desc = f"C({songs_per_output}, {req_mandatory}) × {req_mandatory}! × P({n_random}, {req_random}) = {total_variations:,}"
            
        return {
            "valid": True,
            "total_variations": total_variations,
            "mandatory_per_mix": req_mandatory,
            "random_per_mix": req_random,
            "total_songs_per_mix": songs_per_output,
            "formula_desc": formula_desc,
            "message": f"Dapat menghasilkan hingga {total_variations:,} variasi file MP3 unik."
        }
        
    elif mandatory_mode == "one":
        req_mandatory = 1
        if songs_per_output < 1:
            return {
                "valid": False,
                "total_variations": 0,
                "message": "Jumlah lagu per output minimal 1."
            }
        req_random = songs_per_output - 1
        if req_random > n_random:
            return {
                "valid": False,
                "total_variations": 0,
                "message": f"Dibutuhkan {req_random} lagu acak per file, tetapi di pool hanya ada {n_random} lagu."
            }
            
        mandatory_choices = n_mandatory
        random_perms = math.perm(n_random, req_random) if req_random > 0 else 1
        
        if position_mode in ("start", "end"):
            total_variations = mandatory_choices * random_perms
            formula_desc = f"{n_mandatory} × P({n_random}, {req_random}) = {total_variations:,}"
        elif position_mode == "random":
            total_variations = songs_per_output * mandatory_choices * random_perms
            formula_desc = f"{songs_per_output} (slot) × {n_mandatory} × P({n_random}, {req_random}) = {total_variations:,}"
            
        return {
            "valid": True,
            "total_variations": total_variations,
            "mandatory_per_mix": 1,
            "random_per_mix": req_random,
            "total_songs_per_mix": songs_per_output,
            "formula_desc": formula_desc,
            "message": f"Dapat menghasilkan hingga {total_variations:,} variasi file MP3 unik."
        }


def generate_batch_playlists(
    mandatory_tracks: List[Dict[str, Any]],
    random_tracks: List[Dict[str, Any]],
    songs_per_output: int,
    batch_count: int,
    position_mode: str = "random",
    mandatory_mode: str = "all"
) -> List[List[Dict[str, Any]]]:
    """
    Generates 'batch_count' unique track sequence playlists without duplicates.
    """
    calc = calculate_combinations(
        len(mandatory_tracks),
        len(random_tracks),
        songs_per_output,
        position_mode,
        mandatory_mode
    )
    
    if not calc["valid"] or calc["total_variations"] <= 0:
        raise ValueError(calc.get("message", "Konfigurasi tidak valid untuk menghasilkan kombinasi."))
        
    actual_batch_count = min(batch_count, calc["total_variations"])
    generated_playlists = []
    seen_hashes = set()
    
    attempts = 0
    max_attempts = actual_batch_count * 500
    
    while len(generated_playlists) < actual_batch_count and attempts < max_attempts:
        attempts += 1
        
        if mandatory_mode == "all":
            chosen_mandatory = list(mandatory_tracks)
            random.shuffle(chosen_mandatory)
        else:
            chosen_mandatory = [random.choice(mandatory_tracks)]
            
        req_random = songs_per_output - len(chosen_mandatory)
        if req_random > 0:
            chosen_random = random.sample(random_tracks, req_random)
        else:
            chosen_random = []
            
        playlist = []
        if position_mode == "start":
            playlist = chosen_mandatory + chosen_random
        elif position_mode == "end":
            playlist = chosen_random + chosen_mandatory
        elif position_mode == "random":
            playlist = list(chosen_random)
            for m_track in chosen_mandatory:
                insert_idx = random.randint(0, len(playlist))
                playlist.insert(insert_idx, m_track)
                
        sig = "|".join([t["path"] for t in playlist])
        sig_hash = hashlib.sha256(sig.encode("utf-8")).hexdigest()
        
        if sig_hash not in seen_hashes:
            seen_hashes.add(sig_hash)
            tagged_playlist = []
            for track in playlist:
                is_mand = any(track["path"] == m["path"] for m in mandatory_tracks)
                track_copy = dict(track)
                track_copy["is_mandatory"] = is_mand
                tagged_playlist.append(track_copy)
            generated_playlists.append(tagged_playlist)
            
    return generated_playlists


def merge_playlist_to_mp3(
    playlist: List[Dict[str, Any]],
    output_filepath: str,
    target_bitrate: int = 320,
    target_sample_rate: int = 44100,
    crossfade_sec: float = 0.0,
    normalize_volume: bool = False
) -> Dict[str, Any]:
    """
    Merges a list of audio files into a single MP3 file using FFmpeg with high efficiency.
    """
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
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {res.stderr}")
        return get_ffprobe_info(output_filepath)
        
    input_args = []
    for track in playlist:
        input_args.extend(["-i", track["path"]])
        
    if crossfade_sec > 0 and n > 1:
        filter_parts = []
        last_label = "0:a"
        for i in range(1, n):
            out_label = f"a{i}" if i < n - 1 else "outa"
            filter_parts.append(f"[{last_label}][{i}:a]acrossfade=d={crossfade_sec}:c1=tri:c2=tri[{out_label}]")
            last_label = out_label
        filter_complex = ";".join(filter_parts)
    else:
        stream_inputs = "".join([f"[{i}:a]" for i in range(n)])
        filter_complex = f"{stream_inputs}concat=n={n}:v=0:a=1[outa]"
        
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
    
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {res.stderr}")
        
    return get_ffprobe_info(output_filepath)
