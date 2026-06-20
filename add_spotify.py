import glob

html_files = glob.glob('*.html')

search_str = '<div class="social-icons">'
replace_str = '<div class="social-icons">\n        <a href="https://open.spotify.com/track/1YS2tI17qriwyfXfqdGBRe?si=c55e0b6168884ac3" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="Spotify"><i class="fab fa-spotify"></i></a>'

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # ensure we don't add it multiple times if run twice
    if 'fa-spotify' not in content:
        content = content.replace(search_str, replace_str)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Added Spotify button to all HTML files.")
