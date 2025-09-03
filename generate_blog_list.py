
import os
import re
import markdown

md_dir = 'md_files'
index_file = 'index.html'

# List all .md files in the directory
files = [f for f in os.listdir(md_dir) if f.endswith('.md')]
files.sort()

# Convert each .md file to .html
for md_file in files:
    md_path = os.path.join(md_dir, md_file)
    html_file = os.path.splitext(md_file)[0] + '.html'
    html_path = os.path.join(md_dir, html_file)
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    html_body = markdown.markdown(md_text)
    # Simple HTML wrapper
    html_full = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{os.path.splitext(md_file)[0]}</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
<div class="blog-content">
{html_body}
</div>
</body>
</html>'''
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_full)

# Generate the HTML for the blog list (link to .html files)
blog_links = [
    f'                <li><a href="{md_dir}/{os.path.splitext(f)[0].replace(" ", "%20")}.html">{os.path.splitext(f)[0]}</a></li>'
    for f in files
]
blog_html = '\n'.join(blog_links) if blog_links else '                <li>No blogs found.</li>'

# Read the index.html file
with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the contents of the blogs-list <ul>
new_html = re.sub(
    r'(<ul id="blogs-list">)(.*?)(</ul>)',
    rf'\1\n{blog_html}\n            \3',
    html,
    flags=re.DOTALL
)

# Write back to index.html
with open(index_file, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f'Converted {len(files)} markdown files to HTML and updated blog list in {index_file}.')