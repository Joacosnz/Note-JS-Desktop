import re

fpath = r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage\614a0024a405b02cc875d3e091267a8eb895f9ee\f051f901-b7c0-4aef-9d87-cb031eb4c66b\8cbceebc64912dc2_1'
with open(fpath, 'rb') as fp:
    raw = fp.read()
text = raw.decode('utf-8', errors='ignore')

matches = set(re.findall(r'newBlock\.([a-zA-Z0-9_\.]+)', text))
print(f"Total newBlock entries found: {len(matches)}")
grouped = {}
for m in sorted(matches):
    parts = m.split('.')
    btype = parts[0]
    prop = '.'.join(parts[1:])
    if btype not in grouped:
        grouped[btype] = []
    grouped[btype].append(prop)

for btype, props in sorted(grouped.items()):
    print(f"Block: {btype:25} -> {', '.join(props[:4])}")
