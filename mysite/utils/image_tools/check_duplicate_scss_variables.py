import os
import re
from collections import defaultdict

root_dir = '../..'
excluded_files = []

# Matches scss properties like: beginner-icon: img('wiki/Beginner_Class_Icon.png')
property_pattern = re.compile(r'^\s*([\w-]+)\s*:\s*img\((\'|")(wiki|data)/[^"\')\s]+?\.(png|gif)(\'|")\)\s*,?')

var_definitions = defaultdict(list)

for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if not filename.endswith('.scss') or filename in excluded_files:
            continue
        file_path = os.path.join(dirpath, filename)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for lineno, line in enumerate(f, 1):
                    match = property_pattern.match(line)
                    if match:
                        var_name = match.group(1)
                        var_definitions[var_name].append((file_path, lineno, line.strip()))
        except:
            continue

for var, occurrences in var_definitions.items():
    if len(occurrences) > 1:
        print(f'DUPLICATE: {var}')
        for file_path, lineno, content in occurrences:
            print(f'\t{file_path}:{lineno} | {content}')
        print()
