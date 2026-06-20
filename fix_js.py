with open('main.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if i <= 122: # 0-indexed, so lines 1-123
        new_lines.append(line)
        continue
    
    if i >= 554: # 0-indexed, so lines 555-end
        new_lines.append(line)
        continue

# Now we insert the audio logic between index 122 and 554.
audio_logic = '''
// --- AUDIO PLAYER & ENGINE ---
const playBtn = document.getElementById("player-play-btn");
const prevBtn = document.getElementById("player-prev-btn");
const nextBtn = document.getElementById("player-next-btn");
const trackTitle = document.getElementById("player-track-title");
const currentTimeLabel = document.getElementById("player-current-time");
const totalDurationLabel = document.getElementById("player-total-duration");
const timelineSlider = document.getElementById("player-timeline-slider");
const timelineProgress = document.getElementById("player-timeline-progress");
const volumeSlider = document.getElementById("player-volume-slider");
const volumeProgress = document.getElementById("player-volume-progress");

let globalAudio = new Audio();
if (trackList && trackList.length > 0) {
  globalAudio.src = trackList[0].src;
}
globalAudio.volume = volume;

if (playBtn) {
  playBtn.addEventListener("click", () => {
    if (isPlaying) {
      pauseTrack();
    } else {
      playTrack();
    }
  });
}

function playTrack() {
  if (!globalAudio.src) return;
  globalAudio.play().then(() => {
    isPlaying = true;
    if (playBtn) playBtn.innerHTML = '<i class="fas fa-pause"></i>';
    startWaveform();
  }).catch(e => console.error(e));
}

function pauseTrack() {
  globalAudio.pause();
  isPlaying = false;
  if (playBtn) playBtn.innerHTML = '<i class="fas fa-play"></i>';
  stopWaveform();
}

globalAudio.addEventListener('timeupdate', () => {
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
  }
});

globalAudio.addEventListener('ended', () => {
  pauseTrack();
  globalAudio.currentTime = 0;
});

if (timelineSlider) {
  timelineSlider.addEventListener("click", (e) => {
    const rect = timelineSlider.getBoundingClientRect();
    const percent = (e.clientX - rect.left) / rect.width;
    if (globalAudio.duration) {
      globalAudio.currentTime = percent * globalAudio.duration;
    }
  });
}

if (volumeSlider) {
  volumeSlider.addEventListener("click", (e) => {
    const rect = volumeSlider.getBoundingClientRect();
    let percent = (e.clientX - rect.left) / rect.width;
    percent = Math.max(0, Math.min(1, percent));
    globalAudio.volume = percent;
    if (volumeProgress) volumeProgress.style.width = `${percent * 100}%`;
    
    // Update volume icon
    const volIcon = document.getElementById("volume-icon");
    if (volIcon) {
      if (percent === 0) volIcon.className = "fas fa-volume-mute";
      else if (percent < 0.5) volIcon.className = "fas fa-volume-down";
      else volIcon.className = "fas fa-volume-up";
    }
  });
}

// Waveform visualizer fake animation
let waveTimer;
function startWaveform() {
  const bars = document.querySelectorAll(".wave-bar");
  if (!bars.length) return;
  
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

new_lines.insert(123, audio_logic)

with open('main.js', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("main.js fixed")
