import os, re

target_files = [
    r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage\614a0024a405b02cc875d3e091267a8eb895f9ee\f051f901-b7c0-4aef-9d87-cb031eb4c66b\8cbceebc64912dc2_1',
    r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage\5381cb7d7f0d31a6afec904154068ba9f06028a5\28dc48d6-277e-469e-8ff4-6ad673ba27ca\d2e6fffcbe93e976_1',
    r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage\5381cb7d7f0d31a6afec904154068ba9f06028a5\28dc48d6-277e-469e-8ff4-6ad673ba27ca\34070e4cac3243af_0'
]

keywords = ['slashCommand', 'quickMenu', 'insertBlock', 'newBlock', 'createEmptyBlock', 'initBlock']

for path in target_files:
    fname = os.path.basename(path)
    print(f"\nScanning {fname} ({os.path.getsize(path)/(1024*1024):.2f} MB)...")
    with open(path, 'rb') as fp:
        raw = fp.read()
    text = raw.decode('utf-8', errors='ignore')
    for kw in keywords:
        matches = [m.start() for m in re.finditer(re.escape(kw), text, re.IGNORECASE)]
        if matches:
            print(f"  Keyword '{kw}': {len(matches)} matches")
            for idx in matches[:2]:
                print(f"    Snippet: {text[max(0, idx - 80):min(len(text), idx + 180)].strip()}\n")
