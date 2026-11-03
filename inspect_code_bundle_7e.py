import re

bundle_path = r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage\614a0024a405b02cc875d3e091267a8eb895f9ee\f051f901-b7c0-4aef-9d87-cb031eb4c66b\7e56f42ac1d88f74_1'

with open(bundle_path, 'rb') as fp:
    raw = fp.read()
text = raw.decode('utf-8', errors='ignore')

print(f"Loaded bundle 7e56... length: {len(text)}")

# Search for mentions of block schema, createBlock, block types
for term in ['"bulleted_list"', 'createBlock', 'buildBlock', 'type:"header"', '"transclusion_container"', '"table_of_contents"']:
    matches = [m.start() for m in re.finditer(re.escape(term), text)]
    print(f"Term '{term}': {len(matches)} occurrences")
    for idx in matches[:3]:
        snippet = text[max(0, idx - 100):min(len(text), idx + 200)]
        print(f"   Snippet: {snippet.strip()}\n")
