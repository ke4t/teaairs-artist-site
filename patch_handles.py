import re

with open('main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the URI encoding in trackList
js = js.replace('"assets/keep the vibe lit.mp3"', 'encodeURI("assets/keep the vibe lit.mp3")')

# Fix timeline slider handle
js = js.replace(
    'if (timelineProgress) timelineProgress.style.width = `${percent}%`;',
    'if (timelineProgress) timelineProgress.style.width = `${percent}%`;\n    const timelineHandle = document.getElementById("player-timeline-handle");\n    if (timelineHandle) timelineHandle.style.left = `${percent}%`;'
)

# Fix volume slider handle
js = js.replace(
    'if (volumeProgress) volumeProgress.style.width = `${percent * 100}%`;',
    'if (volumeProgress) volumeProgress.style.width = `${percent * 100}%`;\n    const volumeHandle = document.getElementById("player-volume-handle");\n    if (volumeHandle) volumeHandle.style.left = `${percent * 100}%`;'
)

# Add drag support for sliders? Or just click is fine.

with open('main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("main.js patched with handle updates and encodeURI")
