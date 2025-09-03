# This script scans the md_files directory for .md files and writes a JS file with an array of blog filenames.
import os
import json

md_dir = 'md_files'
js_file = 'blog_list.js'

# List all .md files in the directory
files = [f for f in os.listdir(md_dir) if f.endswith('.md')]

# Write to JS file as a JS array
with open(js_file, 'w', encoding='utf-8') as f:
    f.write('const blogFiles = ')
    json.dump(files, f)
    f.write(';')

print(f'Wrote {len(files)} blog files to {js_file}')
