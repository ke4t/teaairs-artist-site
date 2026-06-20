import glob

html_files = glob.glob('*.html')

search_str = '''<div id="site-loader" class="active">
  <img src="assets/logo.png" alt="TEA Loading" class="loading-logo flash">
</div>'''

replace_str = '''<div id="site-loader" class="active">
  <img src="assets/logo.png" alt="TEA Loading" class="loading-logo flash">
</div>
  <script>
    setTimeout(() => {
      const loader = document.getElementById("site-loader");
      if (loader) loader.classList.remove("active");
    }, 2000);
  </script>'''

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # ensure we don't duplicate
    if '<script>\n    setTimeout(() => {\n      const loader = document.getElementById("site-loader");' not in content:
        content = content.replace(search_str, replace_str)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Inlined loading screen script in all HTML files.")
