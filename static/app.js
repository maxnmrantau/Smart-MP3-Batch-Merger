/**
 * app.js
 * Comprehensive Frontend controller for Smart MP3 Batch Merger & Randomizer
 * With Zero-Zoom Lock, Anti-Glitch Layout, and Native-Feel Event Interceptors.
 */

// =========================================================================
// Native App Lockdown: Disable Browser Zoom & Gesture Pinch
// =========================================================================
window.addEventListener('wheel', (e) => {
  if (e.ctrlKey) {
    e.preventDefault();
  }
}, { passive: false });

window.addEventListener('keydown', (e) => {
  // Disable Ctrl + Plus, Minus, 0, = (zoom shortcuts)
  if (e.ctrlKey && ['+', '-', '=', '0'].includes(e.key)) {
    e.preventDefault();
  }
});

// Disable trackpad pinch-to-zoom gestures
document.addEventListener('gesturestart', (e) => e.preventDefault());
document.addEventListener('gesturechange', (e) => e.preventDefault());
document.addEventListener('gestureend', (e) => e.preventDefault());

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
  const cancelMergeBtn = document.getElementById('cancelMergeBtn');
  const openOutputFolderBtn = document.getElementById('openOutputFolderBtn');

  // Badges & Chips
  const mandatoryCountBadge = document.getElementById('mandatoryCountBadge');
  const randomCountBadge = document.getElementById('randomCountBadge');
  const mandatoryTrackChips = document.getElementById('mandatoryTrackChips');
  const randomTrackChips = document.getElementById('randomTrackChips');

  // Settings & Sliders
  const songsPerOutputRange = document.getElementById('songsPerOutputRange');
  const songsPerOutputVal = document.getElementById('songsPerOutputVal');
  const songsPerOutputNum = document.getElementById('songsPerOutputNum');
  const songsCompositionHint = document.getElementById('songsCompositionHint');
  const batchCountRange = document.getElementById('batchCountRange');
  const batchCountVal = document.getElementById('batchCountVal');
  const batchCountNum = document.getElementById('batchCountNum');
  const batchHint = document.getElementById('batchHint');
  const crossfadeRange = document.getElementById('crossfadeRange');
  const crossfadeVal = document.getElementById('crossfadeVal');
  const audioQualitySelect = document.getElementById('audioQualitySelect');
  const mandatoryModeBlock = document.getElementById('mandatoryModeBlock');

  // New Feature 2: Mandatory Toggle Elements
  const mandatoryToggle = document.getElementById('mandatoryToggle');
  const mandatoryToggleText = document.getElementById('mandatoryToggleText');
  const positionSettingBlock = document.getElementById('positionSettingBlock');

  // New Feature 1: Loop Controls Elements
  const loopSettingBlock = document.getElementById('loopSettingBlock');
  const loopToggle = document.getElementById('loopToggle');
  const loopToggleText = document.getElementById('loopToggleText');
  const loopBadge = document.getElementById('loopBadge');
  const loopSubpanel = document.getElementById('loopSubpanel');
  const loopDurationInputGroup = document.getElementById('loopDurationInputGroup');
  const loopTargetDurationNum = document.getElementById('loopTargetDurationNum');
  const loopDurationHint = document.getElementById('loopDurationHint');
  const loopPoolCountGroup = document.getElementById('loopPoolCountGroup');
  const loopPoolCountRange = document.getElementById('loopPoolCountRange');
  const loopPoolCountNum = document.getElementById('loopPoolCountNum');
  const loopPoolCountHint = document.getElementById('loopPoolCountHint');
  const loopOrderDesc = document.getElementById('loopOrderDesc');

  // New Feature 3: Summary & Timestamps Elements
  const summaryFormatSelect = document.getElementById('summaryFormatSelect');
  const timestampsModal = document.getElementById('timestampsModal');
  const tsModalTitle = document.getElementById('tsModalTitle');
  const tsModalSubtitle = document.getElementById('tsModalSubtitle');
  const btnCloseTsModal = document.getElementById('btnCloseTsModal');
  const btnCloseTsModalBottom = document.getElementById('btnCloseTsModalBottom');
  const tabBtnTsYt = document.getElementById('tabBtnTsYt');
  const tabBtnTsStd = document.getElementById('tabBtnTsStd');
  const paneTsYt = document.getElementById('paneTsYt');
  const paneTsStd = document.getElementById('paneTsStd');
  const tsYtTextarea = document.getElementById('tsYtTextarea');
  const tsStdTextarea = document.getElementById('tsStdTextarea');
  const btnCopyYtModal = document.getElementById('btnCopyYtModal');
  const btnCopyStdModal = document.getElementById('btnCopyStdModal');

  // Inspector Card
  const totalVariationsDisplay = document.getElementById('totalVariationsDisplay');
  const formulaDescDisplay = document.getElementById('formulaDescDisplay');
  const metricToggleHint = document.getElementById('metricToggleHint');
  const inspectorRandomCount = document.getElementById('inspectorRandomCount');
  const inspectorMandatoryCount = document.getElementById('inspectorMandatoryCount');
  const inspectorBitrate = document.getElementById('inspectorBitrate');
  const inspectorAvgSongDur = document.getElementById('inspectorAvgSongDur');
  const inspectorEstOutputDur = document.getElementById('inspectorEstOutputDur');

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
  // Native Folder Picker & Action Handlers
  // =========================================================================
  let isBrowsingFolder = false;

  async function browseLocalFolder(title = "Pilih Folder") {
    console.log('[browseLocalFolder] Called. isBrowsingFolder =', isBrowsingFolder);
    if (isBrowsingFolder) {
      console.warn('[browseLocalFolder] Already browsing, skipping.');
      return null;
    }
    isBrowsingFolder = true;

    try {
      // Step 1: Tell server to open the dialog (returns immediately — non-blocking)
      console.log('[browseLocalFolder] Sending POST /api/browse-folder...');
      const startResp = await fetch('/api/browse-folder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
      });
      console.log('[browseLocalFolder] Response status:', startResp.status);
      if (!startResp.ok) {
        console.error('[browseLocalFolder] browse-folder failed:', startResp.status);
        return null;
      }

      // Step 2: Poll /api/browse-folder-result every 400ms until the dialog closes
      const MAX_WAIT_MS = 180000; // 3 minutes max
      const POLL_MS = 400;
      const deadline = Date.now() + MAX_WAIT_MS;

      while (Date.now() < deadline) {
        await new Promise(r => setTimeout(r, POLL_MS));
        try {
          const pollResp = await fetch('/api/browse-folder-result', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
          });
          if (!pollResp.ok) continue;
          const data = await pollResp.json();
          if (data.status === 'done') {
            console.log('[browseLocalFolder] Got result:', data.folder);
            return data.folder || null;
          }
          // status === 'pending' — keep polling
        } catch (e) {
          console.warn('[App] poll error:', e);
        }
      }

      console.warn('[browseLocalFolder] Timeout reached.');
      return null;
    } catch (e) {
      console.error("[App] browseLocalFolder error:", e);
      return null;
    } finally {
      isBrowsingFolder = false;
      console.log('[browseLocalFolder] Reset isBrowsingFolder = false');
    }
  }

  async function browseLocalFile(title = "Pilih File Audio") {
    if (isBrowsingFolder) return null;
    isBrowsingFolder = true;

    try {
      const startResp = await fetch('/api/browse-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
      });
      if (!startResp.ok) return null;

      const MAX_WAIT_MS = 180000;
      const POLL_MS = 350;
      const deadline = Date.now() + MAX_WAIT_MS;

      while (Date.now() < deadline) {
        await new Promise(r => setTimeout(r, POLL_MS));
        try {
          const pollResp = await fetch('/api/browse-folder-result', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
          });
          if (!pollResp.ok) continue;
          const data = await pollResp.json();
          if (data.status === 'done') {
            return data.folder || null;
          }
        } catch (e) {
          console.warn('[App] poll error:', e);
        }
      }
      return null;
    } catch (e) {
      console.error("[App] browseLocalFile error:", e);
      return null;
    } finally {
      isBrowsingFolder = false;
    }
  }

  btnPickMandatoryFolder.addEventListener('click', async () => {
    console.log('[UI] btnPickMandatoryFolder clicked');
    addLog('⏳ Membuka dialog pemilihan folder...');
    const folder = await browseLocalFolder("Pilih Folder Lagu Wajib (Mandatory)");
    console.log('[UI] browseLocalFolder returned:', folder);
    if (folder) {
      mandatoryFolderInput.value = folder;
      addLog(`📁 Folder Lagu Wajib diatur: ${folder}`);
      await scanFolders();
    } else {
      addLog('ℹ️ Pemilihan folder dibatalkan.');
    }
  });

  btnPickMandatoryFiles.addEventListener('click', async () => {
    console.log('[UI] btnPickMandatoryFiles clicked');
    addLog('⏳ Membuka dialog pemilihan file lagu...');
    const file = await browseLocalFile("Pilih File Lagu Wajib (Single MP3)");
    if (file) {
      mandatoryFolderInput.value = file;
      addLog(`🎵 File Lagu Wajib dipilih: ${file}`);
      await scanFolders();
    } else {
      // Fallback to browser file picker
      mandatoryFilesPicker.click();
    }
  });

  btnPickRandomFolder.addEventListener('click', async () => {
    console.log('[UI] btnPickRandomFolder clicked');
    addLog('⏳ Membuka dialog pemilihan folder...');
    const folder = await browseLocalFolder("Pilih Folder Pool Lagu Random");
    if (folder) {
      randomFolderInput.value = folder;
      addLog(`📁 Folder Lagu Random diatur: ${folder}`);
      await scanFolders();
    } else {
      addLog('ℹ️ Pemilihan folder dibatalkan.');
    }
  });

  btnPickRandomFiles.addEventListener('click', () => {
    randomFilesPicker.click();
  });

  // Output Folder Picker Trigger
  btnPickOutputFolder.addEventListener('click', async () => {
    console.log('[UI] btnPickOutputFolder clicked');
    addLog('⏳ Membuka dialog pemilihan folder output...');
    const folder = await browseLocalFolder("Pilih Folder Tujuan Output");
    if (folder) {
      outputFolderInput.value = folder;
      addLog(`📁 Folder output diatur: ${folder}`);
    } else {
      addLog('ℹ️ Pemilihan folder dibatalkan.');
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

    try {
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
        if (resp.ok) {
          const data = await resp.json();
          if (data.folder) uploadedFolder = data.folder;
        }
      }

      if (uploadedFolder) {
        if (target === 'mandatory') {
          mandatoryFolderInput.value = uploadedFolder;
        } else {
          randomFolderInput.value = uploadedFolder;
        }
      }

      await scanFolders();
      addLog(`✅ Selesai memuat ${audioFiles.length} lagu ke ${target === 'mandatory' ? 'Lagu Wajib' : 'Lagu Random'}.`);
    } catch (err) {
      console.error("handleBrowserFilesSelected error:", err);
      addLog(`❌ Gagal memproses file audio: ${err.message}`);
    }
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
    const isMandatory = mandatoryToggle ? mandatoryToggle.checked : true;

    // Mandatory tracks UI
    if (!isMandatory) {
      if (mandatoryDropZone) mandatoryDropZone.classList.add('disabled-zone');
      if (mandatoryToggleText) mandatoryToggleText.textContent = 'OFF';
      if (mandatoryCountBadge) mandatoryCountBadge.textContent = 'Dinonaktifkan';
      if (inspectorMandatoryCount) inspectorMandatoryCount.textContent = 'Nonaktif (0 Lagu)';
      if (positionSettingBlock) positionSettingBlock.classList.add('disabled-block');
      if (mandatoryModeBlock) mandatoryModeBlock.style.display = 'none';
      if (mandatoryTrackChips) mandatoryTrackChips.innerHTML = '<span class="track-chip" style="opacity:0.6;">(Lagu Wajib dinonaktifkan — seluruh lagu diambil dari pool acak)</span>';
    } else {
      if (mandatoryDropZone) mandatoryDropZone.classList.remove('disabled-zone');
      if (mandatoryToggleText) mandatoryToggleText.textContent = 'ON';
      if (mandatoryCountBadge) mandatoryCountBadge.textContent = `${scannedData.mandatory_count} Lagu Terdeteksi`;
      if (inspectorMandatoryCount) inspectorMandatoryCount.textContent = `${scannedData.mandatory_count} Lagu`;
      if (positionSettingBlock) positionSettingBlock.classList.remove('disabled-block');
      
      // Toggle mandatory mode block visibility if >1 mandatory tracks
      if (scannedData.mandatory_count > 1) {
        if (mandatoryModeBlock) mandatoryModeBlock.style.display = 'flex';
      } else {
        if (mandatoryModeBlock) mandatoryModeBlock.style.display = 'none';
      }

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

    // Update loop subset slider limits
    if (loopPoolCountRange) {
      const poolMax = Math.max(1, scannedData.random_count || 10);
      loopPoolCountRange.max = poolMax;
      if (loopPoolCountNum) loopPoolCountNum.max = poolMax;
      let curVal = parseInt(loopPoolCountRange.value, 10);
      if (isNaN(curVal) || curVal > poolMax || curVal <= 0) {
        curVal = poolMax;
        loopPoolCountRange.value = curVal;
        if (loopPoolCountNum) loopPoolCountNum.value = curVal;
      }
      if (loopPoolCountHint) {
        loopPoolCountHint.textContent = `Memilih ${curVal} lagu dari pool ${scannedData.random_count || 0} lagu untuk di-loop.`;
      }
    }

    syncSongsPerOutputLimits();
  }

  // =========================================================================
  // Duration & Friendly Format Helpers
  // =========================================================================
  function formatFriendlyDuration(seconds) {
    if (isNaN(seconds) || seconds <= 0) return "0 Menit";
    const totalSec = Math.round(seconds);
    const hours = Math.floor(totalSec / 3600);
    const minutes = Math.round((totalSec % 3600) / 60);

    if (hours > 0) {
      if (minutes >= 60) {
        return `${hours + 1} Jam`;
      }
      if (minutes === 0) {
        return `${hours} Jam`;
      }
      return `${hours} Jam ${minutes} Menit`;
    }
    return `${Math.max(1, minutes)} Menit`;
  }

  function calculateDurationEstimates(songsPerOutput, mandatoryMode, crossfadeSec = 0) {
    const isMandatory = mandatoryToggle ? mandatoryToggle.checked : true;
    const isLoop = loopToggle ? loopToggle.checked : false;
    const loopTargetType = document.querySelector('input[name="loopTargetType"]:checked')?.value || 'count';
    const loopDurationMin = loopTargetDurationNum ? parseFloat(loopTargetDurationNum.value) || 60 : 60;

    const nMandatory = isMandatory ? (scannedData.mandatory_count || 0) : 0;
    const nRandom = scannedData.random_count || 0;

    const mandatoryTracks = isMandatory ? (scannedData.mandatory_tracks || []) : [];
    const randomTracks = scannedData.random_tracks || [];

    const usedMandatory = isMandatory ? ((mandatoryMode === 'all') ? nMandatory : (nMandatory > 0 ? 1 : 0)) : 0;
    const usedRandom = Math.max(0, songsPerOutput - usedMandatory);

    // If no tracks scanned yet, return fallback based on default 3.0 mins (180s)
    if (mandatoryTracks.length === 0 && randomTracks.length === 0) {
      const avgSong = 180;
      let est = songsPerOutput * avgSong;
      if (isLoop && loopTargetType === 'duration') {
        est = loopDurationMin * 60;
      }
      return {
        hasData: false,
        avgDur: est,
        minDur: est * 0.85,
        maxDur: est * 1.15,
        avgSongDur: avgSong,
        suggestedFor1Hour: Math.ceil(3600 / avgSong),
        minSongsForGuaranteed1Hour: Math.ceil(3600 / (avgSong * 0.85))
      };
    }

    // Extract valid durations (> 0)
    const mandDurs = mandatoryTracks.map(t => Number(t.duration) || 0).filter(d => d > 0);
    const randDurs = randomTracks.map(t => Number(t.duration) || 0).filter(d => d > 0).sort((a, b) => a - b);

    const defaultDur = 180;
    const avgMandatorySingle = mandDurs.length > 0
      ? mandDurs.reduce((a, b) => a + b, 0) / mandDurs.length
      : defaultDur;
    const avgRandomSingle = randDurs.length > 0
      ? randDurs.reduce((a, b) => a + b, 0) / randDurs.length
      : defaultDur;

    // 1. Mandatory Duration Contribution
    let mandAvg = 0;
    let mandMin = 0;
    let mandMax = 0;

    if (isMandatory) {
      if (mandatoryMode === 'all') {
        const totalMand = mandDurs.reduce((a, b) => a + b, 0);
        mandAvg = totalMand;
        mandMin = totalMand;
        mandMax = totalMand;
      } else {
        if (mandDurs.length > 0) {
          mandAvg = avgMandatorySingle;
          mandMin = Math.min(...mandDurs);
          mandMax = Math.max(...mandDurs);
        } else {
          mandAvg = defaultDur;
          mandMin = defaultDur;
          mandMax = defaultDur;
        }
      }
    }

    // 2. Random Duration Contribution
    let randAvg = 0;
    let randMin = 0;
    let randMax = 0;

    if (isLoop && loopTargetType === 'duration') {
      const targetSec = loopDurationMin * 60;
      const netRandomNeeded = Math.max(0, targetSec - mandAvg);
      randAvg = netRandomNeeded;
      randMin = netRandomNeeded;
      randMax = netRandomNeeded + avgRandomSingle;
    } else {
      if (usedRandom > 0) {
        if (randDurs.length >= usedRandom) {
          randMin = randDurs.slice(0, usedRandom).reduce((a, b) => a + b, 0);
          randMax = randDurs.slice(-usedRandom).reduce((a, b) => a + b, 0);
          randAvg = usedRandom * avgRandomSingle;
        } else if (randDurs.length > 0) {
          randMin = usedRandom * Math.min(...randDurs);
          randMax = usedRandom * Math.max(...randDurs);
          randAvg = usedRandom * avgRandomSingle;
        } else {
          randMin = usedRandom * defaultDur * 0.85;
          randMax = usedRandom * defaultDur * 1.15;
          randAvg = usedRandom * defaultDur;
        }
      }
    }

    // Deduct crossfade overlap if > 0
    const transitionCount = Math.max(0, songsPerOutput - 1);
    const overlapDeduction = (isLoop && loopTargetType === 'duration') ? 0 : transitionCount * crossfadeSec;

    const totalAvg = Math.max(0, mandAvg + randAvg - overlapDeduction);
    const totalMin = Math.max(0, mandMin + randMin - overlapDeduction);
    const totalMax = Math.max(0, mandMax + randMax - overlapDeduction);

    // Calculate pool-wide average track duration
    const allDurs = [...mandDurs, ...randDurs];
    const overallAvg = allDurs.length > 0 ? (allDurs.reduce((a, b) => a + b, 0) / allDurs.length) : defaultDur;

    // How many songs needed on average to reach 1 hour (3600s)?
    const neededFor1Hour = Math.max(2, Math.ceil(3600 / overallAvg));

    // How many songs needed in worst-case (shortest songs) to guarantee 1 hour?
    let guaranteedSongs1Hour = neededFor1Hour;
    if (randDurs.length > 0) {
      let accumMin = isMandatory ? ((mandatoryMode === 'all') ? mandMin : (mandDurs.length > 0 ? Math.min(...mandDurs) : 0)) : 0;
      let k = isMandatory ? ((mandatoryMode === 'all') ? nMandatory : (nMandatory > 0 ? 1 : 0)) : 0;
      let randIdx = 0;
      while (randIdx < randDurs.length && accumMin - Math.max(0, k - 1) * crossfadeSec < 3600) {
        accumMin += randDurs[randIdx];
        k++;
        randIdx++;
      }
      guaranteedSongs1Hour = Math.max(neededFor1Hour, k);
    }

    return {
      hasData: true,
      avgDur: totalAvg,
      minDur: totalMin,
      maxDur: totalMax,
      avgSongDur: overallAvg,
      suggestedFor1Hour: neededFor1Hour,
      minSongsForGuaranteed1Hour: guaranteedSongs1Hour
    };
  }

  function syncSongsPerOutputLimits() {
    const isMandatory = mandatoryToggle ? mandatoryToggle.checked : true;
    const isLoop = loopToggle ? loopToggle.checked : false;
    const mandatoryMode = document.querySelector('input[name="mandatoryMode"]:checked')?.value || 'all';
    const nMandatory = isMandatory ? (scannedData.mandatory_count || 0) : 0;
    const nRandom = scannedData.random_count || 0;

    let minRequired = 2;
    let maxAllowed = 100; // default initial max when no files loaded

    if (isLoop) {
      minRequired = isMandatory && nMandatory > 0 ? (mandatoryMode === 'all' ? nMandatory + 1 : 2) : 2;
      maxAllowed = 200; // In loop mode, user can request up to 200 songs!
    } else if (isMandatory) {
      if (nMandatory > 0 || nRandom > 0) {
        if (mandatoryMode === 'all') {
          minRequired = Math.max(2, nMandatory + (nRandom > 0 ? 1 : 0));
          maxAllowed = nMandatory + nRandom;
        } else {
          // mandatoryMode === 'one'
          minRequired = (nMandatory > 0 && nRandom > 0) ? 2 : 1;
          maxAllowed = (nMandatory > 0 ? 1 : 0) + nRandom;
        }
        maxAllowed = Math.max(minRequired, maxAllowed);
      }
    } else {
      // Mandatory is OFF, Loop is OFF
      minRequired = 1;
      maxAllowed = Math.max(1, nRandom || 100);
    }

    songsPerOutputRange.min = minRequired;
    songsPerOutputRange.max = maxAllowed;

    if (songsPerOutputNum) {
      songsPerOutputNum.min = minRequired;
      songsPerOutputNum.max = maxAllowed;
    }

    let currentVal = parseInt(songsPerOutputRange.value, 10);
    if (isNaN(currentVal) || currentVal < minRequired) {
      currentVal = minRequired;
      songsPerOutputRange.value = currentVal;
    } else if (currentVal > maxAllowed) {
      currentVal = maxAllowed;
      songsPerOutputRange.value = currentVal;
    }

    if (songsPerOutputNum) songsPerOutputNum.value = currentVal;
    if (songsPerOutputVal) songsPerOutputVal.textContent = `${currentVal} Lagu`;
  }

  // =========================================================================
  // Combinatorics Calculation & Helpers
  // =========================================================================
  function formatCombinatoricsClient(n) {
    if (!n || n === 0 || n === '0') return "0";
    const s = String(n).trim();
    if (s.length <= 6) return Number(s).toLocaleString('id-ID');
    if (s.length <= 9) {
      const v = (Number(s) / 1e6).toFixed(2).replace(/\.?0+$/, '').replace('.', ',');
      return `${v} Juta`;
    }
    if (s.length <= 12) {
      const v = (Number(s) / 1e9).toFixed(2).replace(/\.?0+$/, '').replace('.', ',');
      return `${v} Miliar`;
    }
    if (s.length <= 15) {
      const v = (Number(s) / 1e12).toFixed(2).replace(/\.?0+$/, '').replace('.', ',');
      return `${v} Triliun`;
    }
    if (s.length <= 18) {
      const v = (Number(s) / 1e15).toFixed(2).replace(/\.?0+$/, '').replace('.', ',');
      return `${v} Kuadriliun`;
    }
    const exp = s.length - 1;
    const lead = parseFloat(s.slice(0, 4)) / Math.pow(10, Math.min(3, s.slice(0, 4).length - 1));
    const leadStr = lead.toFixed(2).replace(/\.?0+$/, '').replace('.', ',');
    const superscripts = {
      '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
      '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
    };
    const expStr = String(exp).split('').map(c => superscripts[c] || c).join('');
    return `~${leadStr} × 10${expStr}`;
  }

  function showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        if (toast.parentElement) toast.parentElement.removeChild(toast);
      }, 300);
    }, 3200);
  }

  function toggleCombinatoricsDisplay() {
    if (!totalVariationsDisplay) return;
    const exact = totalVariationsDisplay.dataset.exact;
    const short = totalVariationsDisplay.dataset.short;
    if (!exact || exact === '--' || exact === '0') return;

    const currentView = totalVariationsDisplay.dataset.view || "short";
    if (currentView === "short") {
      totalVariationsDisplay.textContent = exact;
      totalVariationsDisplay.dataset.view = "exact";
      totalVariationsDisplay.classList.add('metric-value-exact');
      if (metricToggleHint) metricToggleHint.textContent = "🔍 Format Ringkas";
      totalVariationsDisplay.title = "Format Lengkap Aktif (Klik untuk kembali ke ringkas)";
    } else {
      totalVariationsDisplay.textContent = short;
      totalVariationsDisplay.dataset.view = "short";
      totalVariationsDisplay.classList.remove('metric-value-exact');
      if (metricToggleHint) metricToggleHint.textContent = "🔍 Klik Detail / Salin";
      totalVariationsDisplay.title = `Total Tepat: ${exact} Variasi Unik (Klik untuk salin / toggle format angka lengkap)`;
    }

    // Copy clean digits to clipboard
    try {
      const rawDigits = exact.replace(/\./g, '');
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(rawDigits).then(() => {
          showToast(`✓ Angka kombinasi (${short}) disalin ke clipboard!`, 'info');
        }).catch(() => {});
      }
    } catch (_) {}
  }

  async function calculateCombinations() {
    syncSongsPerOutputLimits();

    const isMandatory = mandatoryToggle ? mandatoryToggle.checked : true;
    const isLoop = loopToggle ? loopToggle.checked : false;
    const loopTargetType = document.querySelector('input[name="loopTargetType"]:checked')?.value || 'count';
    const loopDurationMin = loopTargetDurationNum ? parseFloat(loopTargetDurationNum.value) || 60 : 60;
    const loopPoolCount = loopPoolCountRange ? parseInt(loopPoolCountRange.value, 10) : 0;
    const loopOrder = document.querySelector('input[name="loopOrder"]:checked')?.value || 'random';

    const positionMode = document.querySelector('input[name="positionMode"]:checked')?.value || 'random';
    const mandatoryMode = document.querySelector('input[name="mandatoryMode"]:checked')?.value || 'all';
    const songsPerOutput = parseInt(songsPerOutputRange.value, 10);
    const crossfadeSec = parseFloat(crossfadeRange.value) || 0;

    const nMandatory = isMandatory ? (scannedData.mandatory_count || 0) : 0;
    const nRandom = scannedData.random_count || 0;

    // Calculate duration estimates
    const durInfo = calculateDurationEstimates(songsPerOutput, mandatoryMode, crossfadeSec);

    // Update inspector stats
    if (inspectorAvgSongDur) {
      inspectorAvgSongDur.textContent = durInfo.hasData
        ? `${Math.floor(durInfo.avgSongDur / 60)}m ${Math.round(durInfo.avgSongDur % 60)}s`
        : "--";
    }
    if (inspectorEstOutputDur) {
      inspectorEstOutputDur.textContent = `~${formatFriendlyDuration(durInfo.avgDur)}`;
    }

    // Update composition hint
    if (!isMandatory && !isLoop) {
      songsCompositionHint.textContent = `Panjang 1 File MP3 = ${songsPerOutput} Lagu Random (Tanpa Lagu Wajib)`;
    } else if (isMandatory && !isLoop) {
      const usedMandatory = (mandatoryMode === 'all') ? nMandatory : (nMandatory > 0 ? 1 : 0);
      const usedRandom = Math.max(0, songsPerOutput - usedMandatory);
      songsCompositionHint.textContent = `Panjang 1 File MP3 = ${usedMandatory} Lagu Wajib + ${usedRandom} Lagu Random (${songsPerOutput} Lagu Total)`;
    } else if (isLoop) {
      if (loopTargetType === 'duration') {
        const estTracks = Math.max(1, Math.round((loopDurationMin * 60) / Math.max(30, durInfo.avgSongDur - crossfadeSec)));
        songsCompositionHint.textContent = `Target Durasi = ~${loopDurationMin} Menit (Estimasi ~${estTracks} Lagu Total dengan Loop ${loopPoolCount} Lagu)`;
      } else {
        const usedMandatory = isMandatory ? ((mandatoryMode === 'all') ? nMandatory : (nMandatory > 0 ? 1 : 0)) : 0;
        songsCompositionHint.textContent = `Panjang 1 File MP3 = ${songsPerOutput} Lagu Total (Loop dari ${loopPoolCount} Lagu Pool${isMandatory ? ' + ' + usedMandatory + ' Wajib' : ''})`;
      }
    }

    if ((isMandatory && nMandatory === 0) || nRandom === 0) {
      totalVariationsDisplay.textContent = "--";
      totalVariationsDisplay.dataset.short = "--";
      totalVariationsDisplay.dataset.exact = "--";
      totalVariationsDisplay.dataset.view = "short";
      totalVariationsDisplay.classList.remove('metric-value-exact');
      if (metricToggleHint) metricToggleHint.textContent = "🔍 Klik Detail / Salin";
      formulaDescDisplay.textContent = isMandatory
        ? "Pilih file/folder lagu wajib dan random untuk menghitung variasi."
        : "Pilih file/folder pool lagu random untuk menghitung variasi.";
      return;
    }

    try {
      const resp = await fetch('/api/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          n_mandatory: isMandatory ? nMandatory : 0,
          n_random: nRandom,
          songs_per_output: songsPerOutput,
          position_mode: positionMode,
          mandatory_mode: mandatoryMode,
          mandatory_enabled: isMandatory,
          loop_enabled: isLoop,
          loop_target_type: loopTargetType,
          loop_pool_count: loopPoolCount,
          loop_order: loopOrder
        })
      });
      const calc = await resp.json();

      if (calc.valid) {
        const shortVal = calc.total_variations_formatted || formatCombinatoricsClient(calc.total_variations);
        const exactVal = calc.total_variations_exact || String(calc.total_variations);

        totalVariationsDisplay.dataset.short = shortVal;
        totalVariationsDisplay.dataset.exact = exactVal;

        if (totalVariationsDisplay.dataset.view === "exact") {
          totalVariationsDisplay.textContent = exactVal;
          totalVariationsDisplay.classList.add('metric-value-exact');
          if (metricToggleHint) metricToggleHint.textContent = "🔍 Format Ringkas";
        } else {
          totalVariationsDisplay.textContent = shortVal;
          totalVariationsDisplay.classList.remove('metric-value-exact');
          if (metricToggleHint) metricToggleHint.textContent = "🔍 Klik Detail / Salin";
        }

        totalVariationsDisplay.title = `Total Tepat: ${exactVal} Variasi Unik (Klik untuk salin / toggle format angka lengkap)`;
        formulaDescDisplay.textContent = `Rumus: ${calc.formula_desc}`;
        formulaDescDisplay.title = `Total Tepat: ${exactVal} Variasi`;
      } else {
        totalVariationsDisplay.textContent = "0";
        totalVariationsDisplay.dataset.short = "0";
        totalVariationsDisplay.dataset.exact = "0";
        totalVariationsDisplay.dataset.view = "short";
        totalVariationsDisplay.classList.remove('metric-value-exact');
        if (metricToggleHint) metricToggleHint.textContent = "🔍 Klik Detail / Salin";
        formulaDescDisplay.textContent = calc.message || "Kombinasi tidak valid.";
      }
    } catch (e) {
      console.error("Error calculating combinations:", e);
    }
  }

  // Settings change events
  songsPerOutputRange.addEventListener('input', (e) => {
    if (songsPerOutputNum) songsPerOutputNum.value = e.target.value;
    if (songsPerOutputVal) songsPerOutputVal.textContent = `${e.target.value} Lagu`;
    calculateCombinations();
  });

  if (songsPerOutputNum) {
    songsPerOutputNum.addEventListener('input', (e) => {
      let val = parseInt(e.target.value, 10);
      if (isNaN(val)) return;
      const min = parseInt(songsPerOutputRange.min, 10) || 2;
      const max = parseInt(songsPerOutputRange.max, 10) || 100;
      val = Math.max(min, Math.min(max, val));
      songsPerOutputRange.value = val;
      if (songsPerOutputVal) songsPerOutputVal.textContent = `${val} Lagu`;
      calculateCombinations();
    });
    songsPerOutputNum.addEventListener('change', (e) => {
      let val = parseInt(e.target.value, 10);
      const min = parseInt(songsPerOutputRange.min, 10) || 2;
      const max = parseInt(songsPerOutputRange.max, 10) || 100;
      if (isNaN(val) || val < min) val = min;
      if (val > max) val = max;
      songsPerOutputNum.value = val;
      songsPerOutputRange.value = val;
      if (songsPerOutputVal) songsPerOutputVal.textContent = `${val} Lagu`;
      calculateCombinations();
    });
  }

  batchCountRange.addEventListener('input', (e) => {
    if (batchCountNum) batchCountNum.value = e.target.value;
    if (batchCountVal) batchCountVal.textContent = `${e.target.value} File`;
    if (batchHint) {
      batchHint.textContent = `Total File MP3 yang Dibuat = ${e.target.value} Buah File MP3 Berbeda`;
    }
  });

  if (batchCountNum) {
    batchCountNum.addEventListener('input', (e) => {
      let val = parseInt(e.target.value, 10);
      if (isNaN(val)) return;
      const min = parseInt(batchCountRange.min, 10) || 1;
      const max = parseInt(batchCountRange.max, 10) || 500;
      val = Math.max(min, Math.min(max, val));
      batchCountRange.value = val;
      if (batchCountVal) batchCountVal.textContent = `${val} File`;
      if (batchHint) {
        batchHint.textContent = `Total File MP3 yang Dibuat = ${val} Buah File MP3 Berbeda`;
      }
    });
    batchCountNum.addEventListener('change', (e) => {
      let val = parseInt(e.target.value, 10);
      const min = parseInt(batchCountRange.min, 10) || 1;
      const max = parseInt(batchCountRange.max, 10) || 500;
      if (isNaN(val) || val < min) val = min;
      if (val > max) val = max;
      batchCountNum.value = val;
      batchCountRange.value = val;
      if (batchCountVal) batchCountVal.textContent = `${val} File`;
      if (batchHint) {
        batchHint.textContent = `Total File MP3 yang Dibuat = ${val} Buah File MP3 Berbeda`;
      }
    });
  }

  crossfadeRange.addEventListener('input', (e) => {
    crossfadeVal.textContent = `${parseFloat(e.target.value).toFixed(1)} Detik`;
    calculateCombinations();
  });

  document.querySelectorAll('input[name="positionMode"]').forEach(el => {
    el.addEventListener('change', calculateCombinations);
  });

  document.querySelectorAll('input[name="mandatoryMode"]').forEach(el => {
    el.addEventListener('change', () => {
      syncSongsPerOutputLimits();
      calculateCombinations();
    });
  });

  // Feature 2: Mandatory Toggle listener
  if (mandatoryToggle) {
    mandatoryToggle.addEventListener('change', () => {
      updateFolderUI();
      calculateCombinations();
    });
  }

  // Feature 1: Loop Controls listeners
  if (loopToggle) {
    loopToggle.addEventListener('change', (e) => {
      const isLoop = e.target.checked;
      if (isLoop) {
        if (loopSubpanel) loopSubpanel.classList.remove('hidden');
        if (loopSettingBlock) loopSettingBlock.classList.add('active');
        if (loopToggleText) loopToggleText.textContent = 'ON';
        if (loopBadge) {
          loopBadge.textContent = 'Aktif';
          loopBadge.className = 'badge badge-accent';
        }
      } else {
        if (loopSubpanel) loopSubpanel.classList.add('hidden');
        if (loopSettingBlock) loopSettingBlock.classList.remove('active');
        if (loopToggleText) loopToggleText.textContent = 'OFF';
        if (loopBadge) {
          loopBadge.textContent = 'Nonaktif';
          loopBadge.className = 'badge';
        }
      }
      syncSongsPerOutputLimits();
      calculateCombinations();
    });
  }

  document.querySelectorAll('input[name="loopTargetType"]').forEach(el => {
    el.addEventListener('change', (e) => {
      const isDuration = e.target.value === 'duration';
      if (loopDurationInputGroup) {
        if (isDuration) {
          loopDurationInputGroup.classList.remove('hidden');
        } else {
          loopDurationInputGroup.classList.add('hidden');
        }
      }
      calculateCombinations();
    });
  });

  if (loopTargetDurationNum) {
    loopTargetDurationNum.addEventListener('input', (e) => {
      const val = parseInt(e.target.value, 10) || 60;
      if (loopDurationHint) {
        loopDurationHint.innerHTML = `Lagu di-loop hingga durasi mencapai minimal <strong>${val} Menit (${(val / 60).toFixed(1)} Jam)</strong>.`;
      }
      calculateCombinations();
    });
  }

  if (loopPoolCountRange) {
    loopPoolCountRange.addEventListener('input', (e) => {
      const val = parseInt(e.target.value, 10);
      if (loopPoolCountNum) loopPoolCountNum.value = val;
      if (loopPoolCountHint) {
        loopPoolCountHint.textContent = `Memilih ${val} lagu dari pool ${scannedData.random_count || 0} lagu untuk di-loop.`;
      }
      calculateCombinations();
    });
  }

  if (loopPoolCountNum) {
    loopPoolCountNum.addEventListener('input', (e) => {
      const max = parseInt(loopPoolCountRange.max, 10) || 10;
      let val = parseInt(e.target.value, 10);
      if (isNaN(val)) return;
      val = Math.max(1, Math.min(max, val));
      loopPoolCountRange.value = val;
      if (loopPoolCountHint) {
        loopPoolCountHint.textContent = `Memilih ${val} lagu dari pool ${scannedData.random_count || 0} lagu untuk di-loop.`;
      }
      calculateCombinations();
    });
  }

  document.querySelectorAll('input[name="loopOrder"]').forEach(el => {
    el.addEventListener('change', (e) => {
      if (loopOrderDesc) {
        if (e.target.value === 'random') {
          loopOrderDesc.innerHTML = '<strong>Acak Loop:</strong> Lagu diacak bebas di setiap putaran dengan proteksi anti-kembar berturut-turut.';
        } else {
          loopOrderDesc.innerHTML = '<strong>Berurutan:</strong> Lagu diulang sesuai urutan siklus teratur (1, 2, 3, 4, 1, 2, 3...).';
        }
      }
      calculateCombinations();
    });
  });

  // Initial calculation on page load
  calculateCombinations();

  // Click to toggle compact / exact view and copy to clipboard
  if (totalVariationsDisplay) {
    totalVariationsDisplay.addEventListener('click', toggleCombinatoricsDisplay);
  }
  if (metricToggleHint) {
    metricToggleHint.addEventListener('click', toggleCombinatoricsDisplay);
  }

  // =========================================================================
  // Merge Execution & Polling
  // =========================================================================
  startMergeBtn.addEventListener('click', async () => {
    if (isMerging) return;

    const isMandatory = mandatoryToggle ? mandatoryToggle.checked : true;
    const isLoop = loopToggle ? loopToggle.checked : false;

    const mandatoryFolder = mandatoryFolderInput.value.trim() || scannedData.mandatory_folder;
    const randomFolder = randomFolderInput.value.trim() || scannedData.random_folder;
    const outputFolder = outputFolderInput.value.trim();

    if (isMandatory && !mandatoryFolder) {
      alert("Lagu Wajib sedang AKTIF. Harap pilih folder/file Lagu Wajib terlebih dahulu, atau matikan switch Lagu Wajib (toggle OFF) jika ingin merge tanpa lagu wajib.");
      return;
    }

    if (!randomFolder) {
      alert("Harap pilih atau masukkan folder/file Pool Lagu Random terlebih dahulu.");
      return;
    }

    const positionMode = document.querySelector('input[name="positionMode"]:checked')?.value || 'random';
    const mandatoryMode = document.querySelector('input[name="mandatoryMode"]:checked')?.value || 'all';
    const songsPerOutput = parseInt(songsPerOutputRange.value, 10);
    const batchCount = parseInt(batchCountRange.value, 10);
    const crossfadeSec = parseFloat(crossfadeRange.value);

    const loopTargetType = document.querySelector('input[name="loopTargetType"]:checked')?.value || 'count';
    const loopDurationMin = loopTargetDurationNum ? parseFloat(loopTargetDurationNum.value) || 60 : 60;
    const loopPoolCount = loopPoolCountRange ? parseInt(loopPoolCountRange.value, 10) : 0;
    const loopOrder = document.querySelector('input[name="loopOrder"]:checked')?.value || 'random';
    const summaryFormat = summaryFormatSelect ? summaryFormatSelect.value : 'both';

    const nMandatory = isMandatory ? (scannedData.mandatory_count || 0) : 0;
    if (isMandatory && mandatoryMode === 'all' && nMandatory > 0 && songsPerOutput < nMandatory) {
      alert(`⚠️ Konfigurasi Tidak Valid:\n\nJumlah lagu per output (${songsPerOutput}) lebih sedikit dari jumlah lagu wajib (${nMandatory}).\n\nSaran Solusi:\n1. Pilih opsi "Ambil 1 Bergilir" (jika ingin 1 file output berisi ${songsPerOutput} lagu campuran),\n   ATAU\n2. Geser slider "Jumlah Lagu per Output" minimal ke ${nMandatory + 1} lagu.`);
      return;
    }
    
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
      mandatory_enabled: isMandatory,
      loop_enabled: isLoop,
      loop_target_type: loopTargetType,
      loop_target_duration_min: loopDurationMin,
      loop_pool_count: loopPoolCount,
      loop_order: loopOrder,
      summary_format: summaryFormat,
      crossfade_sec: crossfadeSec,
      target_bitrate: targetBitrate,
      target_sample_rate: scannedData.detected_sample_rate || 44100
    };

    try {
      startMergeBtn.disabled = true;
      startMergeBtn.innerHTML = `<span>Sedang Memproses...</span>`;
      cancelMergeBtn.classList.remove('hidden');
      cancelMergeBtn.disabled = false;
      cancelMergeBtn.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>
        <span>Batal</span>
      `;
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

  cancelMergeBtn.addEventListener('click', async () => {
    if (!isMerging) return;
    cancelMergeBtn.disabled = true;
    cancelMergeBtn.innerHTML = `
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="2" x2="12" y2="6"></line><line x1="12" y1="18" x2="12" y2="22"></line><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line><line x1="2" y1="12" x2="6" y2="12"></line><line x1="18" y1="12" x2="22" y2="12"></line><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line></svg>
      <span>Membatalkan...</span>
    `;
    addLog("⚠️ Mengirim sinyal pembatalan proses penggabungan...");
    try {
      await fetch('/api/cancel-merge', { method: 'POST' });
    } catch (e) {
      console.error("Cancel merge error:", e);
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
          if (state.cancel_requested) {
            progressStatusText.textContent = "🛑 Menghentikan proses atas permintaan pengguna...";
          }
          if (state.current_track_info) {
            currentTrackPipeline.textContent = state.current_track_info;
          }
        } else {
          if (state.error) {
            if (state.error.includes("dibatalkan") || state.cancel_requested) {
              progressStatusText.textContent = `🛑 Penggabungan dibatalkan.`;
            } else {
              progressStatusText.textContent = `❌ Terjadi kesalahan: ${state.error}`;
            }
            resetMergeUI();
          } else if (state.completed_files && state.completed_files.length > 0) {
            progressStatusText.textContent = `✨ Selesai! Semua ${state.total_files} file berhasil digabungkan.`;
            currentTrackPipeline.textContent = "Semua file telah siap di folder output.";
            resetMergeUI();
          } else {
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
    cancelMergeBtn.classList.add('hidden');
    cancelMergeBtn.disabled = false;
    cancelMergeBtn.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>
      <span>Batal</span>
    `;
  }

  function renderResults(files) {
    if (!files || files.length === 0) return;
    resultsList.innerHTML = '';

    files.forEach(f => {
      const card = document.createElement('div');
      card.className = 'result-item-card';

      const isMandatoryUsed = (f.playlist_details || []).some(t => t.is_mandatory);
      const mandatorySlots = (f.playlist_details || [])
        .map((t, i) => t.is_mandatory ? `#${i + 1}` : null)
        .filter(Boolean)
        .join(', ');

      const badgeText = isMandatoryUsed ? `Slot Wajib di ${mandatorySlots}` : 'Semua Random (Non-Wajib)';
      const badgeColor = isMandatoryUsed ? 'var(--accent-cyan)' : 'var(--accent-purple)';

      card.innerHTML = `
        <div class="result-file-info">
          <div class="result-file-name" title="${f.filename}">${f.filename}</div>
          <div class="result-meta-row">
            <span class="result-dur">⏱️ ${f.duration_formatted}</span>
            <span class="result-bitrate">🎧 ${f.bitrate} kbps</span>
            <span class="badge" style="color: ${badgeColor}">${badgeText}</span>
          </div>
        </div>
        <div class="result-actions">
          <button type="button" class="btn btn-secondary btn-sm play-track-btn" data-path="${encodeURIComponent(f.path)}" data-title="${f.filename}" title="Putar file audio ini">
            ▶️ Putar
          </button>
          <button type="button" class="btn btn-secondary btn-sm btn-yt copy-yt-btn" title="Salin Timestamps YouTube ke Clipboard">
            📋 Salin YT
          </button>
          <button type="button" class="btn btn-secondary btn-sm btn-ts view-ts-btn" title="Lihat Timestamps & Ringkasan Lengkap">
            👁️ Timestamps
          </button>
        </div>
      `;

      card.querySelector('.play-track-btn').addEventListener('click', (e) => {
        const path = decodeURIComponent(e.currentTarget.getAttribute('data-path'));
        const title = e.currentTarget.getAttribute('data-title');
        playAudio(path, title);
      });

      card.querySelector('.copy-yt-btn').addEventListener('click', () => {
        const ytText = f.youtube_timestamps || generateClientYtTimestamps(f.playlist_details);
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(ytText).then(() => {
            showToast(`✓ Timestamps YouTube untuk ${f.filename} disalin ke clipboard!`, 'success');
          }).catch(() => {
            openTimestampsModal(f);
          });
        } else {
          openTimestampsModal(f);
        }
      });

      card.querySelector('.view-ts-btn').addEventListener('click', () => {
        openTimestampsModal(f);
      });

      resultsList.appendChild(card);
    });
  }

  function generateClientYtTimestamps(playlist) {
    if (!playlist || playlist.length === 0) return '';
    let currentSec = 0;
    const lines = [];
    playlist.forEach((track, idx) => {
      const min = Math.floor(currentSec / 60);
      const sec = Math.floor(currentSec % 60);
      const ts = `${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
      const title = (track.filename || `Track ${idx + 1}`).replace(/\.[^/.]+$/, "");
      lines.push(`${ts} ${title}`);
      currentSec += Number(track.duration) || 180;
    });
    return lines.join('\n');
  }

  function openTimestampsModal(fileData) {
    if (!timestampsModal) return;
    if (tsModalTitle) tsModalTitle.textContent = fileData.filename;
    if (tsModalSubtitle) {
      const songCount = fileData.playlist_details ? fileData.playlist_details.length : 0;
      tsModalSubtitle.textContent = `Durasi: ${fileData.duration_formatted} | ${songCount} Lagu | Bitrate: ${fileData.bitrate} kbps`;
    }
    const ytText = fileData.youtube_timestamps || generateClientYtTimestamps(fileData.playlist_details);
    if (tsYtTextarea) tsYtTextarea.value = ytText;
    if (tsStdTextarea) tsStdTextarea.value = fileData.standard_timestamps || '';

    switchTsTab('yt');
    timestampsModal.classList.remove('hidden');
  }

  function closeTimestampsModal() {
    if (timestampsModal) timestampsModal.classList.add('hidden');
  }

  function switchTsTab(tab) {
    if (tab === 'yt') {
      if (tabBtnTsYt) tabBtnTsYt.classList.add('active');
      if (tabBtnTsStd) tabBtnTsStd.classList.remove('active');
      if (paneTsYt) paneTsYt.classList.remove('hidden');
      if (paneTsStd) paneTsStd.classList.add('hidden');
    } else {
      if (tabBtnTsStd) tabBtnTsStd.classList.add('active');
      if (tabBtnTsYt) tabBtnTsYt.classList.remove('active');
      if (paneTsStd) paneTsStd.classList.remove('hidden');
      if (paneTsYt) paneTsYt.classList.add('hidden');
    }
  }

  if (tabBtnTsYt) tabBtnTsYt.addEventListener('click', () => switchTsTab('yt'));
  if (tabBtnTsStd) tabBtnTsStd.addEventListener('click', () => switchTsTab('std'));
  if (btnCloseTsModal) btnCloseTsModal.addEventListener('click', closeTimestampsModal);
  if (btnCloseTsModalBottom) btnCloseTsModalBottom.addEventListener('click', closeTimestampsModal);

  if (btnCopyYtModal) {
    btnCopyYtModal.addEventListener('click', () => {
      if (tsYtTextarea && navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(tsYtTextarea.value).then(() => {
          showToast('✓ Timestamps YouTube disalin ke clipboard!', 'success');
        });
      }
    });
  }

  if (btnCopyStdModal) {
    btnCopyStdModal.addEventListener('click', () => {
      if (tsStdTextarea && navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(tsStdTextarea.value).then(() => {
          showToast('✓ Format biasa disalin ke clipboard!', 'success');
        });
      }
    });
  }

  if (timestampsModal) {
    timestampsModal.addEventListener('click', (e) => {
      if (e.target === timestampsModal) closeTimestampsModal();
    });
  }

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && timestampsModal && !timestampsModal.classList.contains('hidden')) {
      closeTimestampsModal();
    }
  });

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

  // =========================================================================
  // Guide Modal Controller (Tabs & Open/Close)
  // =========================================================================
  const btnOpenGuide = document.getElementById('btnOpenGuide');
  const guideModal = document.getElementById('guideModal');
  const btnCloseGuide = document.getElementById('btnCloseGuide');
  const btnUnderstandGuide = document.getElementById('btnUnderstandGuide');
  const modalTabBtns = document.querySelectorAll('.modal-tabs .tab-btn');
  const modalTabPanes = document.querySelectorAll('.modal-body .tab-pane');

  function openGuideModal() {
    if (guideModal) {
      guideModal.classList.remove('hidden');
    }
  }

  function closeGuideModal() {
    if (guideModal) {
      guideModal.classList.add('hidden');
    }
  }

  if (btnOpenGuide) btnOpenGuide.addEventListener('click', openGuideModal);
  if (btnCloseGuide) btnCloseGuide.addEventListener('click', closeGuideModal);
  if (btnUnderstandGuide) btnUnderstandGuide.addEventListener('click', closeGuideModal);

  // Close when clicking outside modal card on the backdrop
  if (guideModal) {
    guideModal.addEventListener('click', (e) => {
      if (e.target === guideModal) {
        closeGuideModal();
      }
    });
  }

  // Close on ESC key
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && guideModal && !guideModal.classList.contains('hidden')) {
      closeGuideModal();
    }
  });

  // Modal Tab Switching
  modalTabBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const targetTabId = btn.getAttribute('data-tab');
      
      modalTabBtns.forEach(b => b.classList.remove('active'));
      modalTabPanes.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetPane = document.getElementById(targetTabId);
      if (targetPane) {
        targetPane.classList.add('active');
      }
    });
  });
});

