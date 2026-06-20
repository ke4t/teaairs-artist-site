import glob

html_files = glob.glob('*.html')

old_style = 'style="height: 80px; vertical-align: middle;"'
new_style = 'style="height: 160px; vertical-align: middle;"'

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace(old_style, new_style)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Increased logo size in all HTML files.")
