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

    # Case 5: Mandatory OFF, 10 random, 5 songs per mix
    # P(10, 5) = 10 * 9 * 8 * 7 * 6 = 30,240
    res5 = merger_engine.calculate_combinations(0, 10, 5, mandatory_enabled=False)
    assert res5["valid"] is True, "Mandatory OFF calculation failed"
    assert res5["total_variations"] == 30240, f"Expected 30240, got {res5['total_variations']}"
    print("  [OK] Mandatory OFF (10 Random, 5 Songs per mix): 30,240 variations verified.")

    # Case 6: Loop Mode (Loop 5 songs from 10 random pool to create 15-song playlist with Acak Loop)
    res6 = merger_engine.calculate_combinations(0, 10, 15, mandatory_enabled=False, loop_enabled=True, loop_pool_count=5, loop_order="random")
    assert res6["valid"] is True, "Loop calculation failed"
    assert res6["total_variations"] > 0, "Expected positive variations"
    print(f"  [OK] Loop & Acak Loop (Pool 10, Subset 5, 15 Songs): {res6['total_variations_formatted']} variations verified.")

    # Case 7: Timestamps Generation Test (YouTube & Standard)
    sample_pl = [
        {"filename": "01. Intro Jingle.mp3", "duration": 180.0, "is_mandatory": True},
        {"filename": "02. Lo-Fi Chill Beat.mp3", "duration": 210.0, "is_mandatory": False},
        {"filename": "03. Rain Ambience.mp3", "duration": 240.0, "is_mandatory": False}
    ]
    ts_list = merger_engine.generate_youtube_timestamps(sample_pl, crossfade_sec=2.0)
    assert len(ts_list) == 3
    assert ts_list[0]["timestamp"] == "00:00"
    assert ts_list[0]["title"] == "01. Intro Jingle"
    assert ts_list[1]["timestamp"] == "02:58" # 180 - 2 = 178s = 02:58
    assert ts_list[2]["timestamp"] == "06:26" # 178 + 210 - 2 = 386s = 06:26
    yt_text = merger_engine.format_timestamps_text(ts_list, "youtube")
    assert "00:00 01. Intro Jingle" in yt_text
    print("  [OK] YouTube & Standard Timestamps calculation verified.")


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

        # Test Case: Batch Playlist without mandatory track (Mandatory OFF)
        playlists_no_mand = merger_engine.generate_batch_playlists(
            mandatory_tracks=[],
            random_tracks=r_scanned,
            songs_per_output=4,
            batch_count=2,
            mandatory_enabled=False
        )
        assert len(playlists_no_mand) == 2
        assert len(playlists_no_mand[0]) == 4
        assert not any(t.get("is_mandatory") for t in playlists_no_mand[0])
        print("  [OK] Batch Playlists generated with Mandatory OFF (100% pool songs).")

        # Test Case: Batch Playlist with Loop & Acak Loop (Loop 3 tracks from 5 pool to 8 slots)
        playlists_loop = merger_engine.generate_batch_playlists(
            mandatory_tracks=[],
            random_tracks=r_scanned,
            songs_per_output=8,
            batch_count=2,
            mandatory_enabled=False,
            loop_enabled=True,
            loop_pool_count=3,
            loop_order="random"
        )
        assert len(playlists_loop) == 2
        assert len(playlists_loop[0]) == 8
        unique_in_mix = len(set(t["path"] for t in playlists_loop[0]))
        assert unique_in_mix == 3, f"Expected 3 unique tracks looped, got {unique_in_mix}"
        print(f"  [OK] Looping & Acak Loop generated playlist with {len(playlists_loop[0])} songs from {unique_in_mix} unique subset.")

        # Test Case: Render looped audio mix
        test_out_loop = os.path.join(out_dir, "Test_Merged_Loop.mp3")
        res_loop_info = merger_engine.merge_playlist_to_mp3(
            playlist=playlists_loop[0],
            output_filepath=test_out_loop,
            target_bitrate=320,
            target_sample_rate=44100
        )
        assert os.path.exists(test_out_loop)
        assert res_loop_info["duration"] >= 15.0, f"Expected ~16s, got {res_loop_info['duration']}"
        print(f"  [OK] FFmpeg merged looped playlist into '{os.path.basename(test_out_loop)}' successfully! Duration: {res_loop_info['duration_formatted']}")
        
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
