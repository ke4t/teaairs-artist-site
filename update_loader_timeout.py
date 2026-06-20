import glob

html_files = glob.glob('*.html')

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # The inline script currently has: }, 2000);
    new_content = content.replace('}, 2000);\n  </script>', '}, 1000);\n  </script>')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Updated inline loader timeout to 1000ms in all HTML files.")
