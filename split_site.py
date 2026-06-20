import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract sections
def extract_section(html, section_id):
    pattern = f'(<section id="{section_id}".*?</section>)'
    match = re.search(pattern, html, re.DOTALL)
    if match:
        return match.group(1)
    return ""

music_sec = extract_section(html, 'music')
videos_sec = extract_section(html, 'videos')
bio_sec = extract_section(html, 'bio')
photos_sec = extract_section(html, 'photos')

# We'll replace the main content area (which contains all sections) with a placeholder
# The sections are currently sequential in index.html
all_sections_pattern = f'(<section id="music".*?</section>\\s*<section id="videos".*?</section>\\s*<section id="bio".*?</section>\\s*<section id="photos".*?</section>)'
match_all = re.search(all_sections_pattern, html, re.DOTALL)

if match_all:
    template = html.replace(match_all.group(1), '{{CONTENT}}')
else:
    # If the regex fails, we can do it manually by replacing each section
    template = html
    template = template.replace(videos_sec, '')
    template = template.replace(bio_sec, '')
    template = template.replace(photos_sec, '')
    template = template.replace(music_sec, '{{CONTENT}}')

# Generate new pages
pages = {
    'index.html': music_sec,
    'videos.html': videos_sec,
    'bio.html': bio_sec,
    'photos.html': photos_sec
}

for filename, content in pages.items():
    page_html = template.replace('{{CONTENT}}', content)
    
    # Update navigation links
    page_html = page_html.replace('href="#music"', 'href="index.html"')
    page_html = page_html.replace('href="#videos"', 'href="videos.html"')
    page_html = page_html.replace('href="#bio"', 'href="bio.html"')
    page_html = page_html.replace('href="#photos"', 'href="photos.html"')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(page_html)

print("Split completed successfully!")
