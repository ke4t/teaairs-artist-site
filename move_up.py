import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Extract controls wrapper
controls_start = html.find('<div class="player-controls-wrapper">')
# Controls wrapper ends at the next '</div>\n        </div>' which marks the end of the player-card?
# No, let's just count divs
pos = controls_start
divs = 0
while pos < len(html):
    if html[pos:pos+4] == "<div":
        divs += 1
    elif html[pos:pos+6] == "</div>":
        divs -= 1
        if divs == 0:
            controls_end = pos + 6
            break
    pos += 1

controls_html = html[controls_start:controls_end]

# Remove controls from html
html = html[:controls_start] + html[controls_end:]

# 2. Insert controls BEFORE waveform-container
waveform_idx = html.find('<div class="waveform-container" id="waveform-visualizer">')
html = html[:waveform_idx] + controls_html + "\n\n          " + html[waveform_idx:]

# 3. Clean up the wave-bars, there's a rogue </div> inside them at line 186.
# Let's replace the whole waveform-container with a clean one
clean_waveform = '<div class="waveform-container" id="waveform-visualizer">\n' + \
                 '              <div class="wave-bar"></div>\n' * 50 + \
                 '          </div>'

# Regex to find the broken waveform container and replace it
# It starts at `<div class="waveform-container" id="waveform-visualizer">`
# and ends right before the closing of player-card (which is the next </div> after the wave-bars).
# Wait, let's just find the start of waveform-container, and remove all wave-bars and rogue </div>s.
# We can do this easily:
wf_start = html.find('<div class="waveform-container" id="waveform-visualizer">')
# Find the next </div> that is followed by the playlist (or just the end of the player-card)
player_playlist_start = html.find('<!-- Playlist -->')
# We replace everything from wf_start up to the last </div> before player_playlist_start
last_div_before_playlist = html.rfind('</div>', 0, player_playlist_start)

# Wait, if we replace all of that, we will also replace the closing </div> of player-card.
# The correct replacement:
html = html[:wf_start] + clean_waveform + '\n        </div>\n          \n        ' + html[player_playlist_start:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done")
