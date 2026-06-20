import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update synth indicator text
html = html.replace(
    '<span class="synth-indicator" id="synth-status"><i class="fas fa-microchip"></i> Live Synthesizer Engine Ready</span>',
    '<span class="synth-indicator" id="synth-status" style="color: #00ffcc;"><i class="fas fa-headphones"></i> Audio Player Ready</span>'
)

# Update track title/artist
html = html.replace(
    '<span class="track-title" id="player-track-title">Umbra (Intro)</span>',
    '<span class="track-title" id="player-track-title">Keep The Vibe Lit</span>'
)

# Update playlist tracks
old_playlist = '''<ul class="playlist-tracks" id="playlist-tracks">
              <li class="track-item active" data-index="0" data-src="umbra" data-duration="3:12">
                <span class="track-number">01</span>
                <span class="track-name">Umbra (Intro)</span>
                <span class="track-len">3:12</span>
              </li>
              <li class="track-item" data-index="1" data-src="eclipse" data-duration="4:05">
                <span class="track-number">02</span>
                <span class="track-name">Eclipse (Title Track)</span>
                <span class="track-len">4:05</span>
              </li>
              <li class="track-item" data-index="2" data-src="neonsoul" data-duration="3:45">
                <span class="track-number">03</span>
                <span class="track-name">Neon Soul</span>
                <span class="track-len">3:45</span>
              </li>
              <li class="track-item" data-index="3" data-src="vortex" data-duration="4:22">
                <span class="track-number">04</span>
                <span class="track-name">Vortex</span>
                <span class="track-len">4:22</span>
              </li>
              <li class="track-item" data-index="4" data-src="corona" data-duration="3:58">
                <span class="track-number">05</span>
                <span class="track-name">Corona (Outro)</span>
                <span class="track-len">3:58</span>
              </li>
            </ul>'''

new_playlist = '''<ul class="playlist-tracks" id="playlist-tracks">
              <li class="track-item active" data-index="0" data-src="vibe_lit" data-duration="0:00">
                <span class="track-number">01</span>
                <span class="track-name">Keep The Vibe Lit</span>
                <span class="track-len" id="vibe-lit-dur">0:00</span>
              </li>
            </ul>'''

html = html.replace(old_playlist, new_playlist)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html updated")
