with open('main.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.startswith('const trackList = ['):
        skip = True
        new_lines.append('const trackList = [\n')
        new_lines.append('  { id: "vibe_lit", title: "Keep The Vibe Lit", durationStr: "0:00", src: "assets/keep the vibe lit.mp3" }\n')
        new_lines.append('];\n')
        continue
    if skip and '];' in line:
        skip = False
        continue
    if skip:
        continue
        
    if line.strip() == '// --- AUDIO PLAYER & SYNTHESIZER ENGINE ---':
        skip = True
        continue
    if line.strip() == '// --- PHOTO LIGHTBOX GALLERY ---':
        skip = False
        
        # Insert new audio logic
        new_lines.append('// --- AUDIO PLAYER & SYNTHESIZER ENGINE ---\n')
        new_lines.append('''
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
globalAudio.src = trackList[0].src;
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
    
    // update track-len in html
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
\n''')
        new_lines.append(line)
        continue
        
    if not skip:
        new_lines.append(line)

with open('main.js', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("main.js rewritten with HTML5 Audio")
