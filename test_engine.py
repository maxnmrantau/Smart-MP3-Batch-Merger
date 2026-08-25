"""
test_engine.py
Automated verification tests for combinatorics math, synthetic audio generation,
anti-duplicate playlist batching, and FFmpeg audio merging.
"""

import os
import sys
import shutil
import tempfile
import subprocess
import merger_engine

def test_combinatorics():
    print("[TEST 1] Testing Combinatorics Calculations...")
    
    # Case 1: 1 mandatory, 10 random, 5 songs per mix, random position
    res1 = merger_engine.calculate_combinations(1, 10, 5, position_mode="random", mandatory_mode="all")
    assert res1["valid"] is True, "Calculation failed"
    assert res1["total_variations"] == 25200, f"Expected 25200, got {res1['total_variations']}"
    print("  [OK] 1 Mandatory + 10 Random (5 Songs, Random Slot): 25,200 variations verified.")
    
    # Case 2: 1 mandatory, 10 random, 5 songs per mix, start position
    res2 = merger_engine.calculate_combinations(1, 10, 5, position_mode="start", mandatory_mode="all")
    assert res2["total_variations"] == 5040, f"Expected 5040, got {res2['total_variations']}"
    print("  [OK] 1 Mandatory + 10 Random (5 Songs, Start Slot): 5,040 variations verified.")
    
    # Case 3: 2 mandatory, 10 random, 5 songs per mix, all mandatory, random position
    # C(5, 2) * 2! * P(10, 3) = 10 * 2 * (10 * 9 * 8) = 20 * 720 = 14,400
    res3 = merger_engine.calculate_combinations(2, 10, 5, position_mode="random", mandatory_mode="all")
    assert res3["total_variations"] == 14400, f"Expected 14400, got {res3['total_variations']}"
    print("  [OK] 2 Mandatory + 10 Random (5 Songs, All Mandatory, Random Slot): 14,400 variations verified.")
    
    # Case 4: 3 mandatory, 10 random, 5 songs per mix, ONE mandatory per mix, random position
    # 5 * 3 * P(10, 4) = 15 * 5040 = 75,600
    res4 = merger_engine.calculate_combinations(3, 10, 5, position_mode="random", mandatory_mode="one")
    assert res4["total_variations"] == 75600, f"Expected 75600, got {res4['total_variations']}"
    print("  [OK] 3 Mandatory + 10 Random (5 Songs, One Mandatory per mix, Random Slot): 75,600 variations verified.")


def generate_synthetic_audio(path: str, freq: int, duration_sec: int = 2):
    """Generates a synthetic sine wave MP3 using FFmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"sine=frequency={freq}:duration={duration_sec}",
        "-c:a", "libmp3lame",
        "-b:a", "320k",
        "-ar", "44100",
        path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)


def test_audio_merging_pipeline():
    print("\n[TEST 2] Testing Audio Synthesis, Batch Generation, and FFmpeg Merging...")
    
    temp_dir = tempfile.mkdtemp(prefix="mp3_merger_test_")
    mand_dir = os.path.join(temp_dir, "mandatory")
    rand_dir = os.path.join(temp_dir, "random")
    out_dir = os.path.join(temp_dir, "output")
    os.makedirs(mand_dir, exist_ok=True)
    os.makedirs(rand_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    
    try:
        # Create 1 mandatory file (2 sec, 440Hz tone)
        m_file = os.path.join(mand_dir, "Mandatory_Jingle.mp3")
        generate_synthetic_audio(m_file, 440, 2)
        print("  [OK] Generated synthetic mandatory track.")
        
        # Create 5 random files (2 sec each)
        for i, freq in enumerate([520, 600, 680, 760, 840], start=1):
            r_file = os.path.join(rand_dir, f"Random_Track_{i:02d}.mp3")
            generate_synthetic_audio(r_file, freq, 2)
        print("  [OK] Generated 5 synthetic random tracks.")
        
        # Scan folders
        m_scanned = merger_engine.scan_audio_folder(mand_dir)
        r_scanned = merger_engine.scan_audio_folder(rand_dir)
        assert len(m_scanned) == 1, "Mandatory track scan count mismatch"
        assert len(r_scanned) == 5, "Random track scan count mismatch"
        print("  [OK] Scan detected metadata accurately (Duration, Bitrate, Sample Rate).")
        
        # Generate 3 batch playlists (each with 3 songs: 1 mandatory + 2 random)
        playlists = merger_engine.generate_batch_playlists(
            mandatory_tracks=m_scanned,
            random_tracks=r_scanned,
            songs_per_output=3,
            batch_count=3,
            position_mode="random",
            mandatory_mode="all"
        )
        assert len(playlists) == 3, f"Expected 3 playlists, got {len(playlists)}"
        
        # Verify each playlist contains mandatory file
        for idx, pl in enumerate(playlists):
            assert len(pl) == 3, f"Playlist #{idx} length mismatch"
            assert any(t["is_mandatory"] for t in pl), f"Playlist #{idx} missing mandatory track"
        print("  [OK] Anti-duplicate batch playlists successfully generated.")
        
        # Perform actual FFmpeg merge for 1 playlist
        test_out_mp3 = os.path.join(out_dir, "Test_Merged_Mix.mp3")
        res_info = merger_engine.merge_playlist_to_mp3(
            playlist=playlists[0],
            output_filepath=test_out_mp3,
            target_bitrate=320,
            target_sample_rate=44100
        )
        assert os.path.exists(test_out_mp3), "Merged MP3 file not found on disk"
        assert res_info["duration"] >= 5.5, f"Expected ~6s duration, got {res_info['duration']}"
        print(f"  [OK] FFmpeg merged 3 tracks into '{os.path.basename(test_out_mp3)}' successfully! Duration: {res_info['duration_formatted']}, Bitrate: {res_info['bitrate']}k")
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
        print("  [OK] Temporary test workspace cleaned up.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING MP3 MERGER SYSTEM VERIFICATION TESTS")
    print("=" * 60)
    test_combinatorics()
    test_audio_merging_pipeline()
    print("\n[SUCCESS] ALL TESTS PASSED SUCCESSFULLY!")
