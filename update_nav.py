import glob

html_files = glob.glob('*.html')

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content.replace('href="music.html"', 'href="index.html"')
    
    if content != new_content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)

print("Updated links to point to the new index.html")
