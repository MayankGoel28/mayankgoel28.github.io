#!/usr/bin/env python3

import os
import shutil
import filecmp
import subprocess
import re

# Configuration
OBSIDIAN_VAULT_PATH = "/Users/mayank/resources/notes"
DESTINATION_REPO_PATH = "/Users/mayank/repos/mayankgoel28.github.io"
DESTINATION_FOLDER_NAME = "md_files"
DESTINATION_PATH = os.path.join(DESTINATION_REPO_PATH, DESTINATION_FOLDER_NAME)
GIT_COMMIT_MESSAGE = "Update markdown files from Obsidian"

def find_md_files_with_show(vault_path):
    md_files = []
    for root, _, files in os.walk(vault_path):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                print(f"Scanning: {full_path}")
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if re.search(r'(?<!\\)\\show(?![a-zA-Z])', content):
                        print(f"Found \\show in: {full_path}")
                        md_files.append(full_path)
    return md_files

def file_changed(src, dest):
    if not os.path.exists(dest):
        return True
    return not filecmp.cmp(src, dest, shallow=False)

def copy_images(md_file, vault_path, dest_path):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find image links in [[...]] blocks containing .png or .jpg
    image_paths = []
    for match in re.findall(r'\[\[(.*?)\]\]', content):
        if '.png' in match or '.jpg' in match:
            image_paths.append(match)
    for img_path in image_paths:
        # Remove any possible extra pipes or aliases (e.g., [[image.png|alt text]])
        img_file = img_path.split('|')[0].strip()
        img_full_path = os.path.join(vault_path, img_file)
        if os.path.exists(img_full_path):
            rel_img_path = os.path.relpath(img_full_path, vault_path)
            dest_img_path = os.path.join(dest_path, rel_img_path)
            os.makedirs(os.path.dirname(dest_img_path), exist_ok=True)
            shutil.copy2(img_full_path, dest_img_path)

def main():

    md_files = find_md_files_with_show(OBSIDIAN_VAULT_PATH)
    files_copied = False

    for src_md in md_files:
        rel_path = os.path.relpath(src_md, OBSIDIAN_VAULT_PATH)
        dest_md = os.path.join(DESTINATION_PATH, rel_path)
        os.makedirs(os.path.dirname(dest_md), exist_ok=True)
        if not os.path.exists(dest_md):
            shutil.copy2(src_md, dest_md)
            print(f"Added file {dest_md}")
            files_copied = True
        elif file_changed(src_md, dest_md):
            shutil.copy2(src_md, dest_md)
            print(f"Modified file {dest_md}")
            files_copied = True

    # After all markdown files are copied, always scan all destination md files for image links and copy images
    for root, _, files in os.walk(DESTINATION_PATH):
        for file in files:
            if file.endswith('.md'):
                dest_md = os.path.join(root, file)
                # The corresponding source md file in the vault
                rel_path = os.path.relpath(dest_md, DESTINATION_PATH)
                src_md = os.path.join(OBSIDIAN_VAULT_PATH, rel_path)
                if os.path.exists(src_md):
                    copy_images(src_md, OBSIDIAN_VAULT_PATH, DESTINATION_PATH)

    if files_copied:
        subprocess.run(["git", "-C", DESTINATION_REPO_PATH, "add", DESTINATION_FOLDER_NAME], check=True)
        subprocess.run(["git", "-C", DESTINATION_REPO_PATH, "commit", "-m", GIT_COMMIT_MESSAGE], check=True)
        subprocess.run(["git", "-C", DESTINATION_REPO_PATH, "push"], check=True)


if __name__ == "__main__":
    main()
