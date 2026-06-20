import glob

html_files = glob.glob('*.html')

new_socials = '''      <div class="social-icons">
        <a href="https://tiktok.com/@teaairs" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="TikTok"><i class="fab fa-tiktok"></i></a>
        <a href="https://instagram.com/teaairs" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
        <a href="https://x.com/teaonair" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
        <a href="https://www.youtube.com/@Teaairs" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
        <a href="https://soundcloud.com/teaonair" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="SoundCloud"><i class="fab fa-soundcloud"></i></a>
      </div>'''

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    start_idx = content.find('<div class="social-icons">')
    if start_idx != -1:
        end_idx = content.find('</div>', start_idx) + 6
        content = content[:start_idx] + new_socials + content[end_idx:]

        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Updated social icons in all HTML files.")
