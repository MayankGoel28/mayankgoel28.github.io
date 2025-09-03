#!/bin/bash

set -e

python3 obsidian_to_gh.py
python3 generate_blog_list.py
git add .
git commit -m "updated blogs"
git push
