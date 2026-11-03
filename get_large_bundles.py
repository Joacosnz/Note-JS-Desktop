import os, re

cache_dir = r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage'

large_files = []
for root, dirs, files in os.walk(cache_dir):
    for f in files:
        full = os.path.join(root, f)
        try:
            sz = os.path.getsize(full)
            if sz > 2 * 1024 * 1024: # > 2 MB
                with open(full, 'rb') as fp:
                    head = fp.read(400)
                    m = re.search(rb'https://[^\x00-\x1f\s"]+', head)
                    url = m.group(0).decode('utf-8', errors='ignore') if m else "unknown"
                    large_files.append((sz, url, full))
        except:
            pass

large_files.sort(key=lambda x: x[0], reverse=True)
print(f"Total >2MB bundles: {len(large_files)}")
for sz, url, path in large_files:
    print(f"{sz / (1024*1024):.2f} MB | {url} | {path}")
