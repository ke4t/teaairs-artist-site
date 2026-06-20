import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Wrap the entire player side in player-column-wrapper
html = html.replace(
    '<!-- Custom Interactive Audio Player -->\n        <div class="player-card glass-card" id="player-container">',
    '<!-- Custom Interactive Audio Player -->\n        <div class="player-column-wrapper" style="display: flex; flex-direction: column; gap: 1rem;">\n          <div class="player-card glass-card" id="player-container">'
)

# 2. Close player-card after waveform.
# The waveform ends at line 205 with `          </div>`
html = re.sub(
    r'(<div class="wave-bar"></div>\s*){20}</div>',
    r'\g<0>\n          </div>',
    html
)

# 3. Modify player-playlist to have player-card glass-card
html = html.replace(
    '<div class="player-playlist">',
    '<div class="player-playlist player-card glass-card">'
)

# 4. Modify player-controls-wrapper to have player-card glass-card
html = html.replace(
    '<div class="player-controls-wrapper">',
    '<div class="player-controls-wrapper player-card glass-card">'
)

# 5. Add closing div for player-column-wrapper at the end of the right column
html = re.sub(
    r'          </div>\n        </div>\n      </div>\n  </section>',
    '          </div>\n          </div>\n        </div>\n      </div>\n  </section>',
    html
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("HTML modified successfully")
