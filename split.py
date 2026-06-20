import re
import os

html_file = 'index.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the sections we are looking for
section_ids = ['hero', 'music', 'videos', 'tour', 'bio', 'photos', 'press', 'contact']

# We need to find the start of the first section and the end of the last section to get top and bottom wrappers
first_section_match = re.search(r'\s*<!-- Hero Section -->\s*<section id="hero"', content)
if not first_section_match:
    first_section_match = re.search(r'<section id="hero"', content)

last_section_end = content.find('<!-- Footer -->')
if last_section_end == -1:
    last_section_end = content.rfind('</section>') + 10

top_wrapper = content[:first_section_match.start()]
bottom_wrapper = content[last_section_end:]

sections_content = content[first_section_match.start():last_section_end]

# Extract each section
sections = {}
for i, sid in enumerate(section_ids):
    start_str = f'<section id="{sid}"'
    start_idx = sections_content.find(start_str)
    
    # Also grab the comment before it if possible
    comment_search = sections_content.rfind('<!--', 0, start_idx)
    if comment_search != -1 and sections_content[comment_search:start_idx].strip().startswith('<!--'):
        start_idx = comment_search

    if i < len(section_ids) - 1:
        next_sid = section_ids[i+1]
        end_idx = sections_content.find(f'<section id="{next_sid}"')
        
        # also find the comment before next section
        next_comment = sections_content.rfind('<!--', 0, end_idx)
        if next_comment != -1 and sections_content[next_comment:end_idx].strip().startswith('<!--'):
            end_idx = next_comment
    else:
        end_idx = len(sections_content)
        
    sec_html = sections_content[start_idx:end_idx]
    sections[sid] = sec_html

# Function to fix links in HTML
def fix_links(html_string):
    # Fix links to standard sections
    for link in section_ids:
        if link == 'hero':
            html_string = html_string.replace(f'href="#{link}"', 'href="index.html"')
        else:
            html_string = html_string.replace(f'href="#{link}"', f'href="{link}.html"')
    return html_string

# Write out each page
for sid, sec_html in sections.items():
    page_content = top_wrapper + sec_html + bottom_wrapper
    page_content = fix_links(page_content)
    
    filename = 'index.html' if sid == 'hero' else f'{sid}.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(page_content)
    print(f'Created {filename}')
