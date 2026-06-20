import glob

html_files = glob.glob('*.html')

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if 'href="contact.html"' not in line and 'href="press.html"' not in line and 'href="tour.html"' not in line:
            new_lines.append(line)

    new_content = '\n'.join(new_lines)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Removed contact, press, and tour links from all HTML files.")
