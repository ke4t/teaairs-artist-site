import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Current order is:
# 1. Main box (ends after waveform)
# 2. Playlist box
# 3. Controls box

# We want:
# 1. Main box (contains waveform AND controls)
# 2. Playlist box

# Step A: Find the Controls box and extract it.
controls_start = html.find('<div class="player-controls-wrapper player-card glass-card">')
controls_end_search = html.find('</div>', html.find('<div class="volume-slider"', controls_start))
# The volume slider contains <div class="volume-progress"> and <div class="volume-handle">. So we need to find its end.
# Actually, the controls box ends right before the closing divs of the column wrapper.
# Let's be precise.
# It starts at controls_start.
# Let's count divs from controls_start to find its end.
divs = 0
pos = controls_start
while pos < len(html):
    if html[pos:pos+4] == "<div":
        divs += 1
    elif html[pos:pos+6] == "</div>":
        divs -= 1
        if divs == 0:
            controls_end = pos + 6
            break
    pos += 1

controls_block = html[controls_start:controls_end]
# Remove it from html
html = html[:controls_start] + html[controls_end:]

# Step B: Modify controls block (remove player-card glass-card)
controls_block = controls_block.replace(
    '<div class="player-controls-wrapper player-card glass-card">',
    '<div class="player-controls-wrapper">'
)

# Step C: Find where to insert it. We want it INSIDE the main box at the bottom.
# Currently, the main box ends just before <!-- Playlist -->
playlist_start = html.find('<!-- Playlist -->')
# Just before playlist_start, there is the closing </div> of the main box.
# Let's find that </div>.
main_box_close = html.rfind('</div>', 0, playlist_start)

# Insert the controls block right BEFORE main_box_close
html = html[:main_box_close] + "\n          " + controls_block + "\n" + html[main_box_close:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("done")
