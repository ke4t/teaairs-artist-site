import glob

html_files = glob.glob('*.html')

loader_html = '''<div id="site-loader" class="active">
  <img src="assets/logo.png" alt="TEA Loading" class="loading-logo flash">
</div>'''

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Don't add twice
    if 'id="site-loader"' not in content:
        # find body tag
        body_idx = content.find('<body>')
        if body_idx != -1:
            body_end = body_idx + len('<body>')
            content = content[:body_end] + '\n  ' + loader_html + content[body_end:]
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)

print("Added initial loading screen to all HTML files.")
