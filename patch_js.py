with open('main.js', 'r', encoding='utf-8') as f:
    js = f.read()

patches = [
    ('timelineSlider.addEventListener("click",', 'if (timelineSlider) timelineSlider.addEventListener("click",'),
    ('playBtn.addEventListener("click",', 'if (playBtn) playBtn.addEventListener("click",'),
    ('volumeSlider.addEventListener("click",', 'if (volumeSlider) volumeSlider.addEventListener("click",'),
    ('lightbox.addEventListener("click",', 'if (lightbox) lightbox.addEventListener("click",'),
    ('videoModal.addEventListener("click",', 'if (videoModal) videoModal.addEventListener("click",'),
    ('ticketModal.addEventListener("click",', 'if (ticketModal) ticketModal.addEventListener("click",'),
    ('contactForm.addEventListener("submit",', 'if (contactForm) contactForm.addEventListener("submit",')
]

for old, new in patches:
    # avoid double patching
    if old in js and new not in js:
        js = js.replace(old, new)

with open('main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("main.js patched for null safety")
