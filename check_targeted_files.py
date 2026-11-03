import os, re

cache_dir = r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage'
target_names = [
    '34070e4cac3243af_0', '34070e4cac3243af_1',
    'f7403da35655f340_0', 'f7403da35655f340_1',
    '5573a581c7bd5f6a_0', '48300fcaedf2f7c3_0',
    'b9b3f92e4c8cee9b_0', '432239e27a797a60_0'
]

found = []
for root, dirs, files in os.walk(cache_dir):
    for f in files:
        if f in target_names:
            full = os.path.join(root, f)
            with open(full, 'rb') as fp:
                head = fp.read(400)
                m = re.search(rb'https://[^\x00-\x1f\s"]+', head)
                url = m.group(0).decode('utf-8', errors='ignore') if m else "unknown"
                found.append((f, url, full))

for f, url, full in found:
    print(f"{f} -> {url}")
