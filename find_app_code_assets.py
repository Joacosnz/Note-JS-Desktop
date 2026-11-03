import os, re

cache_dir = r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage'

matches = []
for root, dirs, files in os.walk(cache_dir):
    for f in files:
        full = os.path.join(root, f)
        try:
            with open(full, 'rb') as fp:
                head = fp.read(400)
                m = re.search(rb'https://(?:app\.notion\.com|www\.notion\.so)/_assets/([a-zA-Z0-9_\-\.]+)', head)
                if m:
                    asset_name = m.group(1).decode('utf-8', errors='ignore')
                    if any(k in asset_name for k in ['app', 'vendor', 'index', 'main', 'editor', 'block']):
                        matches.append((asset_name, os.path.getsize(full), full))
        except:
            pass

matches.sort(key=lambda x: x[1], reverse=True)
print(f"Found {len(matches)} matching code assets:")
for name, size, full in matches[:25]:
    print(f"  {size/(1024*1024):.2f} MB | {name} | {full}")
