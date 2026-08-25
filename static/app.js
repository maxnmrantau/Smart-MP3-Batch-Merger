/**
 * app.js
 * Comprehensive Frontend controller for Smart MP3 Batch Merger & Randomizer
 * With Zero-Zoom Lock, Anti-Glitch Layout, and Native-Feel Event Interceptors.
 */

// =========================================================================
// Native App Lockdown: Disable Browser Zoom, Gesture Pinch, & Context Menu
// =========================================================================
window.addEventListener('wheel', (e) => {
  if (e.ctrlKey) {
    e.preventDefault();
  }
}, { passive: false });

window.addEventListener('keydown', (e) => {
  // Disable Ctrl + Plus, Minus, 0, =, F11, F12, Ctrl+R
  if (e.ctrlKey && ['+', '-', '=', '0', 'r', 'R'].includes(e.key)) {
    e.preventDefault();
  }
  if (['F11', 'F12'].includes(e.key)) {
    e.preventDefault();
  }
});

// Disable trackpad pinch-to-zoom gestures
document.addEventListener('gesturestart', (e) => e.preventDefault());
document.addEventListener('gesturechange', (e) => e.preventDefault());
document.addEventListener('gestureend', (e) => e.preventDefault());

// Disable right-click menu on non-input areas
document.addEventListener('contextmenu', (e) => {
  if (!['INPUT', 'TEXTAREA'].includes(e.target.tagName)) {
    e.preventDefault();
  }
});

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements - Inputs
  const mandatoryFolderInput = document.getElementById('mandatoryFolderInput');
  const randomFolderInput = document.getElementById('randomFolderInput');
  const outputFolderInput = document.getElementById('outputFolderInput');

  // Pickers & Buttons - Mandatory
  const mandatoryFolderPicker = document.getElementById('mandatoryFolderPicker');
  const mandatoryFilesPicker = document.getElementById('mandatoryFilesPicker');
  const btnPickMandatoryFolder = document.getElementById('btnPickMandatoryFolder');
  const btnPickMandatoryFiles = document.getElementById('btnPickMandatoryFiles');
  const btnScanMandatoryPath = document.getElementById('btnScanMandatoryPath');
  const mandatoryDropZone = document.getElementById('mandatoryDropZone');

  // Pickers & Buttons - Random Pool
  const randomFolderPicker = document.getElementById('randomFolderPicker');
  const randomFilesPicker = document.getElementById('randomFilesPicker');
  const btnPickRandomFolder = document.getElementById('btnPickRandomFolder');
  const btnPickRandomFiles = document.getElementById('btnPickRandomFiles');
  const btnScanRandomPath = document.getElementById('btnScanRandomPath');
  const randomDropZone = document.getElementById('randomDropZone');

  // Pickers & Buttons - Output Folder
  const outputFolderPicker = document.getElementById('outputFolderPicker');
  const btnPickOutputFolder = document.getElementById('btnPickOutputFolder');
  const btnOpenOutputFolderDirect = document.getElementById('btnOpenOutputFolderDirect');

  const startMergeBtn = document.getElementById('startMergeBtn');
  const openOutputFolderBtn = document.getElementById('openOutputFolderBtn');

  // Badges & Chips
  const mandatoryCountBadge = document.getElementById('mandatoryCountBadge');
  const randomCountBadge = document.getElementById('randomCountBadge');
  const mandatoryTrackChips = document.getElementById('mandatoryTrackChips');
  const randomTrackChips = document.getElementById('randomTrackChips');

  // Settings & Sliders
  const songsPerOutputRange = document.getElementById('songsPerOutputRange');
  const songsPerOutputVal = document.getElementById('songsPerOutputVal');
  const songsCompositionHint = document.getElementById('songsCompositionHint');
  const batchCountRange = document.getElementById('batchCountRange');
  const batchCountVal = document.getElementById('batchCountVal');
  const batchHint = document.getElementById('batchHint');
  const crossfadeRange = document.getElementById('crossfadeRange');
  const crossfadeVal = document.getElementById('crossfadeVal');
  const audioQualitySelect = document.getElementById('audioQualitySelect');
  const mandatoryModeBlock = document.getElementById('mandatoryModeBlock');

  // Inspector Card
  const totalVariationsDisplay = document.getElementById('totalVariationsDisplay');
  const formulaDescDisplay = document.getElementById('formulaDescDisplay');
  const inspectorRandomCount = document.getElementById('inspectorRandomCount');
  const inspectorMandatoryCount = document.getElementById('inspectorMandatoryCount');
  const inspectorBitrate = document.getElementById('inspectorBitrate');

  // Progress & Logs
  const progressContainer = document.getElementById('progressContainer');
  const progressStatusText = document.getElementById('progressStatusText');
  const progressPercentText = document.getElementById('progressPercentText');
  const progressBarFill = document.getElementById('progressBarFill');
  const currentTrackPipeline = document.getElementById('currentTrackPipeline');
  const logConsole = document.getElementById('logConsole');

  // Results & Player
  const resultsList = document.getElementById('resultsList');
  const mainAudioPlayer = document.getElementById('mainAudioPlayer');
  const playerTrackTitle = document.getElementById('playerTrackTitle');

  // State
  let scannedData = {
    mandatory_folder: '',
    mandatory_count: 0,
    mandatory_tracks: [],
    random_folder: '',
    random_count: 0,
    random_tracks: [],
    detected_bitrate: 320,
    detected_sample_rate: 44100
  };
  let isMerging = false;
  let statusPollInterval = null;

  // Initialize Defaults
  fetch('/api/defaults')
    .then(r => r.json())
    .then(data => {
      if (data.output_folder && !outputFolderInput.value) {
        outputFolderInput.value = data.output_folder;
      }
    })
    .catch(() => {});

  // =========================================================================
  // HTML5 Picker Click Handlers (Mandatory & Random)
  // =========================================================================
  btnPickMandatoryFolder.addEventListener('click', () => {
    mandatoryFolderPicker.click();
  });

  btnPickMandatoryFiles.addEventListener('click', () => {
    mandatoryFilesPicker.click();
  });

  btnPickRandomFolder.addEventListener('click', () => {
    randomFolderPicker.click();
  });

  btnPickRandomFiles.addEventListener('click', () => {
    randomFilesPicker.click();
  });

  // Output Folder Picker Trigger
  btnPickOutputFolder.addEventListener('click', () => {
    outputFolderPicker.click();
  });

  outputFolderPicker.addEventListener('change', (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const sampleFile = e.target.files[0];
      const relPath = sampleFile.webkitRelativePath || "";
      const folderName = relPath.split('/')[0] || "Custom_Output_Folder";
      addLog(`📁 Folder output diatur: ${folderName}`);
    }
  });

  // Handle Files Selected via Browser Picker
  mandatoryFolderPicker.addEventListener('change', (e) => {
    handleBrowserFilesSelected(e.target.files, 'mandatory');
  });

  mandatoryFilesPicker.addEventListener('change', (e) => {
    handleBrowserFilesSelected(e.target.files, 'mandatory');
  });

  randomFolderPicker.addEventListener('change', (e) => {
    handleBrowserFilesSelected(e.target.files, 'random');
  });

  randomFilesPicker.addEventListener('change', (e) => {
    handleBrowserFilesSelected(e.target.files, 'random');
  });

  async function handleBrowserFilesSelected(fileList, target) {
    if (!fileList || fileList.length === 0) return;

    const audioFiles = Array.from(fileList).filter(f => {
      const ext = '.' + f.name.split('.').pop().toLowerCase();
      return ['.mp3', '.wav', '.aac', '.m4a', '.flac', '.ogg', '.wma'].includes(ext);
    });

    if (audioFiles.length === 0) {
      alert("Tidak ada file audio (.mp3, .wav, .m4a, dll) yang ditemukan pada pilihan Anda.");
      return;
    }

    addLog(`Mengunggah ${audioFiles.length} file audio ke slot ${target === 'mandatory' ? 'Lagu Wajib' : 'Lagu Random'}...`);

    // Clear old workspace folder for this target
    await fetch('/api/clear-folder', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target })
    });

    // Upload each audio file
    let uploadedFolder = '';
    for (const file of audioFiles) {
      const resp = await fetch(`/api/upload-files?target=${target}&filename=${encodeURIComponent(file.name)}`, {
        method: 'POST',
        body: file
      });
      const data = await resp.json();
      if (data.folder) uploadedFolder = data.folder;
    }

    if (target === 'mandatory') {
      mandatoryFolderInput.value = uploadedFolder;
    } else {
      randomFolderInput.value = uploadedFolder;
    }

    await scanFolders();
    addLog(`✅ Selesai memuat ${audioFiles.length} lagu ke ${target === 'mandatory' ? 'Lagu Wajib' : 'Lagu Random'}.`);
  }

  // =========================================================================
  // Drag and Drop Zone Handlers
  // =========================================================================
  function setupDragAndDrop(dropZone, target) {
    ['dragenter', 'dragover'].forEach(eventName => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add('drag-over');
      });
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('drag-over');
      });
    });

    dropZone.addEventListener('drop', (e) => {
      const files = e.dataTransfer.files;
      if (files && files.length > 0) {
        handleBrowserFilesSelected(files, target);
      }
    });
  }

  setupDragAndDrop(mandatoryDropZone, 'mandatory');
  setupDragAndDrop(randomDropZone, 'random');

  // =========================================================================
  // Direct Path Scan Buttons & Input Listeners
  // =========================================================================
  btnScanMandatoryPath.addEventListener('click', scanFolders);
  btnScanRandomPath.addEventListener('click', scanFolders);

  let scanDebounce = null;
  function handlePathInput() {
    clearTimeout(scanDebounce);
    scanDebounce = setTimeout(() => {
      scanFolders();
    }, 400);
  }

  mandatoryFolderInput.addEventListener('input', handlePathInput);
  mandatoryFolderInput.addEventListener('paste', handlePathInput);
  randomFolderInput.addEventListener('input', handlePathInput);
  randomFolderInput.addEventListener('paste', handlePathInput);

  // =========================================================================
  // Folder Scanner & Inspector Updates
  // =========================================================================
  async function scanFolders() {
    const mandatoryFolder = mandatoryFolderInput.value.trim();
    const randomFolder = randomFolderInput.value.trim();

    try {
      const resp = await fetch('/api/scan-folders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mandatory_folder: mandatoryFolder,
          random_folder: randomFolder
        })
      });
      scannedData = await resp.json();
      updateFolderUI();
      await calculateCombinations();
    } catch (e) {
      console.error("Error scanning folders:", e);
    }
  }

  function updateFolderUI() {
    // Mandatory tracks UI
    mandatoryCountBadge.textContent = `${scannedData.mandatory_count} Lagu Terdeteksi`;
    inspectorMandatoryCount.textContent = `${scannedData.mandatory_count} Lagu`;
    mandatoryTrackChips.innerHTML = '';
    scannedData.mandatory_tracks.slice(0, 8).forEach(t => {
      const chip = document.createElement('span');
      chip.className = 'track-chip';
      chip.innerHTML = `🎵 ${t.filename} <span class="chip-dur">${t.duration_formatted}</span>`;
      mandatoryTrackChips.appendChild(chip);
    });
    if (scannedData.mandatory_count > 8) {
      const moreChip = document.createElement('span');
      moreChip.className = 'track-chip';
      moreChip.textContent = `+${scannedData.mandatory_count - 8} lagu lainnya...`;
      mandatoryTrackChips.appendChild(moreChip);
    }

    // Random tracks UI
    randomCountBadge.textContent = `${scannedData.random_count} Lagu Terdeteksi`;
    inspectorRandomCount.textContent = `${scannedData.random_count} Lagu`;
    randomTrackChips.innerHTML = '';
    scannedData.random_tracks.slice(0, 8).forEach(t => {
      const chip = document.createElement('span');
      chip.className = 'track-chip';
      chip.innerHTML = `🎵 ${t.filename} <span class="chip-dur">${t.duration_formatted}</span>`;
      randomTrackChips.appendChild(chip);
    });
    if (scannedData.random_count > 8) {
      const moreChip = document.createElement('span');
      moreChip.className = 'track-chip';
      moreChip.textContent = `+${scannedData.random_count - 8} lagu lainnya...`;
      randomTrackChips.appendChild(moreChip);
    }

    // Bitrate display
    inspectorBitrate.textContent = `Auto (${scannedData.detected_bitrate} kbps)`;

    // Toggle mandatory mode block visibility if >1 mandatory tracks
    if (scannedData.mandatory_count > 1) {
      mandatoryModeBlock.style.display = 'flex';
    } else {
      mandatoryModeBlock.style.display = 'none';
    }
  }

  // =========================================================================
  // Combinatorics Calculation
  // =========================================================================
  async function calculateCombinations() {
    const positionMode = document.querySelector('input[name="positionMode"]:checked')?.value || 'random';
    const mandatoryMode = document.querySelector('input[name="mandatoryMode"]:checked')?.value || 'all';
    const songsPerOutput = parseInt(songsPerOutputRange.value, 10);

    const nMandatory = scannedData.mandatory_count;
    const nRandom = scannedData.random_count;

    if (nMandatory === 0 || nRandom === 0) {
      totalVariationsDisplay.textContent = "--";
      formulaDescDisplay.textContent = "Pilih file/folder lagu wajib dan random untuk menghitung variasi.";
      return;
    }

    // Update composition hint
    const usedMandatory = (mandatoryMode === 'all') ? nMandatory : 1;
    const usedRandom = Math.max(0, songsPerOutput - usedMandatory);
    songsCompositionHint.textContent = `Panjang 1 File MP3 = ${usedMandatory} Lagu Wajib + ${usedRandom} Lagu Random (Durasi ~${songsPerOutput * 3.5 | 0} Menit)`;

    try {
      const resp = await fetch('/api/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          n_mandatory: nMandatory,
          n_random: nRandom,
          songs_per_output: songsPerOutput,
          position_mode: positionMode,
          mandatory_mode: mandatoryMode
        })
      });
      const calc = await resp.json();

      if (calc.valid) {
        totalVariationsDisplay.textContent = Number(calc.total_variations).toLocaleString('id-ID');
        formulaDescDisplay.textContent = `Rumus: ${calc.formula_desc}`;
      } else {
        totalVariationsDisplay.textContent = "0";
        formulaDescDisplay.textContent = calc.message || "Kombinasi tidak valid.";
      }
    } catch (e) {
      console.error("Error calculating combinations:", e);
    }
  }

  // Settings change events
  songsPerOutputRange.addEventListener('input', (e) => {
    songsPerOutputVal.textContent = `${e.target.value} Lagu`;
    calculateCombinations();
  });

  batchCountRange.addEventListener('input', (e) => {
    batchCountVal.textContent = `${e.target.value} File`;
    if (batchHint) {
      batchHint.textContent = `Total File MP3 yang Dibuat = ${e.target.value} Buah File MP3 Berbeda`;
    }
  });

  crossfadeRange.addEventListener('input', (e) => {
    crossfadeVal.textContent = `${parseFloat(e.target.value).toFixed(1)} Detik`;
  });

  document.querySelectorAll('input[name="positionMode"]').forEach(el => {
    el.addEventListener('change', calculateCombinations);
  });

  document.querySelectorAll('input[name="mandatoryMode"]').forEach(el => {
    el.addEventListener('change', calculateCombinations);
  });

  // =========================================================================
  // Merge Execution & Polling
  // =========================================================================
  startMergeBtn.addEventListener('click', async () => {
    if (isMerging) return;

    const mandatoryFolder = mandatoryFolderInput.value.trim() || scannedData.mandatory_folder;
    const randomFolder = randomFolderInput.value.trim() || scannedData.random_folder;
    const outputFolder = outputFolderInput.value.trim();

    if (!mandatoryFolder || !randomFolder) {
      alert("Harap pilih atau masukkan folder/file Lagu Wajib dan Lagu Random terlebih dahulu.");
      return;
    }

    const positionMode = document.querySelector('input[name="positionMode"]:checked')?.value || 'random';
    const mandatoryMode = document.querySelector('input[name="mandatoryMode"]:checked')?.value || 'all';
    const songsPerOutput = parseInt(songsPerOutputRange.value, 10);
    const batchCount = parseInt(batchCountRange.value, 10);
    const crossfadeSec = parseFloat(crossfadeRange.value);
    
    let targetBitrate = 320;
    if (audioQualitySelect.value === 'auto') {
      targetBitrate = scannedData.detected_bitrate || 320;
    } else {
      targetBitrate = parseInt(audioQualitySelect.value, 10);
    }

    const config = {
      mandatory_folder: mandatoryFolder,
      random_folder: randomFolder,
      output_folder: outputFolder,
      songs_per_output: songsPerOutput,
      batch_count: batchCount,
      position_mode: positionMode,
      mandatory_mode: mandatoryMode,
      crossfade_sec: crossfadeSec,
      target_bitrate: targetBitrate,
      target_sample_rate: scannedData.detected_sample_rate || 44100
    };

    try {
      startMergeBtn.disabled = true;
      startMergeBtn.innerHTML = `<span>Sedang Memproses...</span>`;
      progressContainer.classList.remove('hidden');
      isMerging = true;

      const resp = await fetch('/api/start-merge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config)
      });
      const data = await resp.json();

      if (resp.ok) {
        startStatusPolling();
      } else {
        alert(data.error || "Gagal memulai proses merge.");
        resetMergeUI();
      }
    } catch (e) {
      console.error("Error starting merge:", e);
      resetMergeUI();
    }
  });

  function startStatusPolling() {
    if (statusPollInterval) clearInterval(statusPollInterval);

    statusPollInterval = setInterval(async () => {
      try {
        const resp = await fetch('/api/status');
        const state = await resp.json();

        // Update progress bar smoothly
        progressBarFill.style.width = `${state.progress_percent}%`;
        progressPercentText.textContent = `${state.progress_percent}%`;

        if (state.is_running) {
          progressStatusText.textContent = `Memproses file ${state.current_index} dari ${state.total_files}...`;
          if (state.current_track_info) {
            currentTrackPipeline.textContent = state.current_track_info;
          }
        } else {
          if (state.error) {
            progressStatusText.textContent = `❌ Terjadi kesalahan: ${state.error}`;
            resetMergeUI();
          } else if (state.completed_files && state.completed_files.length > 0) {
            progressStatusText.textContent = `✨ Selesai! Semua ${state.total_files} file berhasil digabungkan.`;
            currentTrackPipeline.textContent = "Semua file telah siap di folder output.";
            resetMergeUI();
          }
        }

        // Update logs smoothly
        if (state.logs && state.logs.length > 0) {
          logConsole.innerHTML = state.logs.map(l => `<div class="log-entry">${l}</div>`).join('');
          logConsole.scrollTop = logConsole.scrollHeight;
        }

        // Update completed results list
        if (state.completed_files && state.completed_files.length > 0) {
          renderResults(state.completed_files);
        }

        if (!state.is_running && !isMerging) {
          clearInterval(statusPollInterval);
        }
      } catch (e) {
        console.error("Polling error:", e);
      }
    }, 500);
  }

  function resetMergeUI() {
    isMerging = false;
    startMergeBtn.disabled = false;
    startMergeBtn.innerHTML = `
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
      <span>Mulai Proses Merge (Batch)</span>
    `;
  }

  function renderResults(files) {
    if (!files || files.length === 0) return;
    resultsList.innerHTML = '';

    files.forEach(f => {
      const card = document.createElement('div');
      card.className = 'result-item-card';

      const mandatorySlots = (f.playlist_details || [])
        .map((t, i) => t.is_mandatory ? `#${i + 1}` : null)
        .filter(Boolean)
        .join(', ');

      card.innerHTML = `
        <div class="result-file-info">
          <div class="result-file-name">${f.filename}</div>
          <div class="result-meta-row">
            <span class="result-dur">⏱️ ${f.duration_formatted}</span>
            <span class="result-bitrate">🎧 ${f.bitrate} kbps</span>
            <span class="badge" style="color: var(--accent-cyan)">Slot Wajib di ${mandatorySlots || 'N/A'}</span>
          </div>
        </div>
        <div class="result-actions">
          <button type="button" class="btn btn-secondary btn-sm play-track-btn" data-path="${encodeURIComponent(f.path)}" data-title="${f.filename}">
            ▶️ Putar
          </button>
        </div>
      `;

      card.querySelector('.play-track-btn').addEventListener('click', (e) => {
        const path = decodeURIComponent(e.currentTarget.getAttribute('data-path'));
        const title = e.currentTarget.getAttribute('data-title');
        playAudio(path, title);
      });

      resultsList.appendChild(card);
    });
  }

  function playAudio(filePath, title) {
    playerTrackTitle.textContent = title;
    mainAudioPlayer.src = `/api/audio-preview?path=${encodeURIComponent(filePath)}`;
    mainAudioPlayer.play();
  }

  function addLog(text) {
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    entry.textContent = text;
    logConsole.appendChild(entry);
    logConsole.scrollTop = logConsole.scrollHeight;
  }

  // Open output folder in Windows Explorer
  async function openOutputFolder() {
    const outputFolder = outputFolderInput.value.trim();
    addLog(`Membuka folder output di Windows Explorer...`);
    try {
      const res = await fetch('/api/open-output-folder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folder: outputFolder })
      });
      const data = await res.json();
      if (data.status) {
        addLog(`📂 Windows Explorer dibuka.`);
      }
    } catch (e) {
      console.error("Error opening output folder:", e);
    }
  }

  openOutputFolderBtn.addEventListener('click', openOutputFolder);
  btnOpenOutputFolderDirect.addEventListener('click', openOutputFolder);
});
