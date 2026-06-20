import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's extract the components.
# 1. Start of right column wrapper
col_start_idx = html.find('<div class="player-column-wrapper"')

# 2. End of right column wrapper (it ends right before </section>)
section_end_idx = html.find('</section>')
# Find the exact html block for the right column
right_col_html = html[col_start_idx:section_end_idx]

# We know the right column contains:
# - player-column-wrapper
#   - player-card
#     - header
#     - now playing
#     - waveform
#   - controls (wait, this is currently inside waveform?)
#   - playlist

# Let's just use string replacement on index.html to fix the missing </div>.
# Right after the last wave-bar, we need a </div>.
# Let's find: '<div class="wave-bar"></div>\n          \n          <div class="player-controls-wrapper">'
html = html.replace(
    '<div class="wave-bar"></div>\n          \n          <div class="player-controls-wrapper">',
    '<div class="wave-bar"></div>\n          </div>\n          \n          <div class="player-controls-wrapper">'
)

# And now we have one EXTRA opening div (since we added a closing div).
# Actually we added a closing div, so now we have one EXTRA closing div overall.
# We need to remove a closing div from the end of the file.
# The end of the file currently is:
#           </div>
#         </div>
#       </div>
#   </section>
# Let's change it to:
#         </div>
#       </div>
#   </section>

html = re.sub(
    r'          </div>\n        </div>\n      </div>\n  </section>',
    '        </div>\n      </div>\n  </section>',
    html
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done")
