import re

with open('main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the entire audio logic section to be robust
# We will find the start and end of the audio logic
start_marker = '// --- AUDIO PLAYER & ENGINE ---'
end_marker = '// --- PHOTO LIGHTBOX GALLERY ---'

start_idx = js.find(start_marker)
end_idx = js.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_audio_logic = '''// --- AUDIO PLAYER & ENGINE ---
const playBtn = document.getElementById("player-play-btn");
const prevBtn = document.getElementById("player-prev-btn");
const nextBtn = document.getElementById("player-next-btn");
const trackTitle = document.getElementById("player-track-title");
const currentTimeLabel = document.getElementById("player-current-time");
const totalDurationLabel = document.getElementById("player-total-duration");
const timelineSlider = document.getElementById("player-timeline-slider");
const timelineProgress = document.getElementById("player-timeline-progress");
const timelineHandle = document.getElementById("player-timeline-handle");
const volumeSlider = document.getElementById("player-volume-slider");
const volumeProgress = document.getElementById("player-volume-progress");
const volumeHandle = document.getElementById("player-volume-handle");

let globalAudio = new Audio("assets/keep the vibe lit.mp3");
globalAudio.volume = 0.8;

if (playBtn) {
  playBtn.addEventListener("click", () => {
    if (globalAudio.paused) {
      globalAudio.play().then(() => {
        playBtn.innerHTML = '<i class="fas fa-pause"></i>';
        startWaveform();
      }).catch(e => console.error("Audio play failed:", e));
    } else {
      globalAudio.pause();
      playBtn.innerHTML = '<i class="fas fa-play"></i>';
      stopWaveform();
    }
  });
}

globalAudio.addEventListener('timeupdate', () => {
  if (isDraggingTimeline) return; // Don't update UI if dragging
  const current = globalAudio.currentTime;
  const duration = globalAudio.duration || 0;
  
  const currentMins = Math.floor(current / 60);
  const currentSecs = Math.floor(current % 60).toString().padStart(2, '0');
  if (currentTimeLabel) currentTimeLabel.textContent = `${currentMins}:${currentSecs}`;
  
  if (duration > 0) {
    const durMins = Math.floor(duration / 60);
    const durSecs = Math.floor(duration % 60).toString().padStart(2, '0');
    if (totalDurationLabel) totalDurationLabel.textContent = `${durMins}:${durSecs}`;
    
    const durLabelHTML = document.getElementById("vibe-lit-dur");
    if (durLabelHTML) durLabelHTML.textContent = `${durMins}:${durSecs}`;

    const percent = (current / duration) * 100;
    if (timelineProgress) timelineProgress.style.width = `${percent}%`;
    if (timelineHandle) timelineHandle.style.left = `${percent}%`;
  }
});

globalAudio.addEventListener('ended', () => {
  globalAudio.currentTime = 0;
  globalAudio.pause();
  if (playBtn) playBtn.innerHTML = '<i class="fas fa-play"></i>';
  stopWaveform();
});

// Timeline Drag Logic
let isDraggingTimeline = false;

function updateTimelineFromEvent(e) {
  if (!timelineSlider || !globalAudio.duration) return;
  const rect = timelineSlider.getBoundingClientRect();
  let percent = (e.clientX - rect.left) / rect.width;
  percent = Math.max(0, Math.min(1, percent));
  
  if (timelineProgress) timelineProgress.style.width = `${percent * 100}%`;
  if (timelineHandle) timelineHandle.style.left = `${percent * 100}%`;
  
  return percent * globalAudio.duration;
}

if (timelineSlider) {
  timelineSlider.addEventListener("mousedown", (e) => {
    isDraggingTimeline = true;
    updateTimelineFromEvent(e);
  });
  window.addEventListener("mousemove", (e) => {
    if (isDraggingTimeline) updateTimelineFromEvent(e);
  });
  window.addEventListener("mouseup", (e) => {
    if (isDraggingTimeline) {
      isDraggingTimeline = false;
      globalAudio.currentTime = updateTimelineFromEvent(e);
    }
  });
}

// Volume Drag Logic
let isDraggingVolume = false;

function updateVolumeFromEvent(e) {
  if (!volumeSlider) return;
  const rect = volumeSlider.getBoundingClientRect();
  let percent = (e.clientX - rect.left) / rect.width;
  percent = Math.max(0, Math.min(1, percent));
  
  globalAudio.volume = percent;
  if (volumeProgress) volumeProgress.style.width = `${percent * 100}%`;
  if (volumeHandle) volumeHandle.style.left = `${percent * 100}%`;
  
  const volIcon = document.getElementById("volume-icon");
  if (volIcon) {
    if (percent === 0) volIcon.className = "fas fa-volume-mute";
    else if (percent < 0.5) volIcon.className = "fas fa-volume-down";
    else volIcon.className = "fas fa-volume-up";
  }
}

if (volumeSlider) {
  volumeSlider.addEventListener("mousedown", (e) => {
    isDraggingVolume = true;
    updateVolumeFromEvent(e);
  });
  window.addEventListener("mousemove", (e) => {
    if (isDraggingVolume) updateVolumeFromEvent(e);
  });
  window.addEventListener("mouseup", (e) => {
    if (isDraggingVolume) {
      isDraggingVolume = false;
      updateVolumeFromEvent(e);
    }
  });
}

// Waveform visualizer fake animation
let waveTimer;
function startWaveform() {
  const bars = document.querySelectorAll(".wave-bar");
  if (!bars.length) return;
  
  clearInterval(waveTimer);
  waveTimer = setInterval(() => {
    bars.forEach(bar => {
      bar.style.height = `${Math.random() * 100}%`;
    });
  }, 100);
}

function stopWaveform() {
  clearInterval(waveTimer);
  const bars = document.querySelectorAll(".wave-bar");
  bars.forEach(bar => {
    bar.style.height = '10%';
  });
}

'''
    js = js[:start_idx] + new_audio_logic + js[end_idx:]

    with open('main.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("main.js audio logic updated with dragging support.")
else:
    print("Could not find markers.")
