import os, re

cache_dir = r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage'

found_files = []
for root, dirs, files in os.walk(cache_dir):
    for f in files:
        full = os.path.join(root, f)
        size = os.path.getsize(full)
        if size > 100000: # > 100 KB
            found_files.append((full, size))

print(f"Found {len(found_files)} cached files in CacheStorage")

# Look for block types list or block schema
block_types_pattern = re.compile(b'(bulleted_list|numbered_list|header_4|sub_sub_header|table_row|to_do|callout|quote|equation|column_list)')

matching_files = []
for full, size in found_files:
    try:
        with open(full, 'rb') as fp:
            data = fp.read()
            matches = block_types_pattern.findall(data)
            if len(set(matches)) >= 5:
                matching_files.append((full, size, len(set(matches)), len(matches)))
                print(f"File {os.path.basename(full)}: {len(set(matches))} distinct types, {len(matches)} occurrences, size {size/(1024*1024):.2f} MB")
    except Exception as e:
        pass

print(f"Total matching files: {len(matching_files)}")
