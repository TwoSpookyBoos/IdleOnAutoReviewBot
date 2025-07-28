import re
import os
from urllib.parse import unquote

wiki_pattern = re.compile(r'wiki/[^"\')\s]+?\.png')
data_pattern = re.compile(r'data/[^"\')\s]+?\.png')

root_dir = './mysite'
image_dir = './mysite/static/imgs'

excluded_files = ['image_fetcher.js', 'image-mapping.css']

USE_PATTERN = wiki_pattern

for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename in excluded_files:
            continue
        file_path = os.path.join(dirpath, filename)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    for match in USE_PATTERN.findall(line):
                        decoded_match = unquote(match)
                        if not os.path.isfile(os.path.join(image_dir, decoded_match)):
                            print(f'MISSING: {decoded_match} in {file_path}')
        except:
            continue
