import glob

html_files = glob.glob('*.html')

desktop_new = '''      <div class="desktop-socials">
        <a href="https://tiktok.com/@teaairs" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="TikTok"><i class="fab fa-tiktok"></i></a>
        <a href="https://instagram.com/teaairs" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
        <a href="https://teaonair.com" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="Website"><i class="fas fa-globe"></i></a>
        <a href="https://www.youtube.com/@Teaairs" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
        <a href="https://soundcloud.com/teaonair" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="SoundCloud"><i class="fab fa-soundcloud"></i></a>
        <a href="https://x.com/teaonair" target="_blank" rel="noopener noreferrer" class="social-icon" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
      </div>'''

mobile_new = '''    <div class="mobile-socials">
      <a href="https://tiktok.com/@teaairs" class="social-icon"><i class="fab fa-tiktok"></i></a>
      <a href="https://instagram.com/teaairs" class="social-icon"><i class="fab fa-instagram"></i></a>
      <a href="https://teaonair.com" class="social-icon"><i class="fas fa-globe"></i></a>
      <a href="https://www.youtube.com/@Teaairs" class="social-icon"><i class="fab fa-youtube"></i></a>
      <a href="https://soundcloud.com/teaonair" class="social-icon"><i class="fab fa-soundcloud"></i></a>
      <a href="https://x.com/teaonair" class="social-icon"><i class="fab fa-twitter"></i></a>
    </div>'''

footer_new = '''        <div class="footer-socials">
          <a href="https://tiktok.com/@teaairs" class="footer-icon"><i class="fab fa-tiktok"></i></a>
          <a href="https://instagram.com/teaairs" class="footer-icon"><i class="fab fa-instagram"></i></a>
          <a href="https://teaonair.com" class="footer-icon"><i class="fas fa-globe"></i></a>
          <a href="https://www.youtube.com/@Teaairs" class="footer-icon"><i class="fab fa-youtube"></i></a>
          <a href="https://soundcloud.com/teaonair" class="footer-icon"><i class="fab fa-soundcloud"></i></a>
          <a href="https://x.com/teaonair" class="footer-icon"><i class="fab fa-twitter"></i></a>
        </div>'''

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Desktop replacement
    start_d = content.find('<div class="desktop-socials">')
    if start_d != -1:
        end_d = content.find('</div>', start_d) + 6
        content = content[:start_d] + desktop_new + content[end_d:]

    # Mobile replacement
    start_m = content.find('<div class="mobile-socials">')
    if start_m != -1:
        end_m = content.find('</div>', start_m) + 6
        content = content[:start_m] + mobile_new + content[end_m:]

    # Footer replacement
    start_f = content.find('<div class="footer-socials">')
    if start_f != -1:
        end_f = content.find('</div>', start_f) + 6
        content = content[:start_f] + footer_new + content[end_f:]

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated all HTML files.")
