import re, os

target_files = [
    r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage\614a0024a405b02cc875d3e091267a8eb895f9ee\0ef0d4c3-949e-4c78-b7ee-2b91d9aa0c77\5573a581c7bd5f6a_0',
    r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage\5381cb7d7f0d31a6afec904154068ba9f06028a5\28dc48d6-277e-469e-8ff4-6ad673ba27ca\34070e4cac3243af_0'
]

for tf in target_files:
    if not os.path.exists(tf):
        continue
    print(f"\n=================== Inspecting {os.path.basename(tf)} ===================")
    with open(tf, 'rb') as fp:
        raw = fp.read()
    text = raw.decode('utf-8', errors='ignore')
    print(f"File length: {len(text)} chars")
    
    # Search for block definitions
    matches = [m.start() for m in re.finditer(r'bulleted_list', text)]
    print(f"Found {len(matches)} occurrences of 'bulleted_list'")
    
    for idx in matches[:5]:
        snippet = text[max(0, idx - 150):min(len(text), idx + 250)]
        print(f"--- Snippet at {idx} ---")
        print(snippet.strip())
