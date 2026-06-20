import glob

html_files = glob.glob('*.html')

old_style = 'style="height: 40px; vertical-align: middle; border-radius: 4px;"'
new_style = 'style="height: 80px; vertical-align: middle; border-radius: 4px;"'

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace(old_style, new_style)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated logo size in all HTML files.")
