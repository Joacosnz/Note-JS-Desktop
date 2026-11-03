import os, re

cache_dir = r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage'

bundles = []
for root, dirs, files in os.walk(cache_dir):
    for f in files:
        full = os.path.join(root, f)
        try:
            with open(full, 'rb') as fp:
                head = fp.read(400)
                m = re.search(rb'https://www\.notion\.so/_assets/([^\x00-\x1f\s"]+)', head)
                if m:
                    url = m.group(0).decode('utf-8', errors='ignore')
                    size = os.path.getsize(full)
                    bundles.append((url, size, full))
        except:
            pass

bundles.sort(key=lambda x: x[1], reverse=True)
print(f"Total asset bundles identified: {len(bundles)}")
for url, size, path in bundles[:25]:
    fname = url.split('/')[-1]
    print(f"{size/(1024*1024):.2f} MB | {fname} | {path}")
