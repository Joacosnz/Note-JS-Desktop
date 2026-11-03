import re

fpath = r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage\5381cb7d7f0d31a6afec904154068ba9f06028a5\28dc48d6-277e-469e-8ff4-6ad673ba27ca\44dd6ef580e46afc_0'
with open(fpath, 'rb') as fp:
    raw = fp.read()
text = raw.decode('utf-8', errors='ignore')

matches = [m.start() for m in re.finditer(r'bulleted_list', text)]
print(f"Found {len(matches)} occurrences of 'bulleted_list'")

for idx in matches[:10]:
    start = max(0, idx - 150)
    end = min(len(text), idx + 250)
    print("--------------------------------------------------")
    print(text[start:end])
