import re

fpath = r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage\614a0024a405b02cc875d3e091267a8eb895f9ee\f051f901-b7c0-4aef-9d87-cb031eb4c66b\ef0ca39f9c8a3890_0'
with open(fpath, 'rb') as fp:
    raw = fp.read()
text = raw.decode('utf-8', errors='ignore')

# Search for "bulleted_list" in text
matches = [m.start() for m in re.finditer(r'"bulleted_list"', text)]
print(f"Found {len(matches)} occurrences of 'bulleted_list'")

for idx in matches[:10]:
    start = max(0, idx - 150)
    end = min(len(text), idx + 250)
    print("--------------------------------------------------")
    print(text[start:end])
