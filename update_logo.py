import glob

html_files = glob.glob('*.html')

old_logo = '<a href="index.html" class="logo" id="nav-logo">Tea</a>'
new_logo = '<a href="index.html" class="logo" id="nav-logo"><img src="assets/logo.png" alt="ON AIR" style="height: 40px; vertical-align: middle; border-radius: 4px;"></a>'

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace(old_logo, new_logo)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated logo in all HTML files.")
