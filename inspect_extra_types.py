import re, json

bundle_path = r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage\5381cb7d7f0d31a6afec904154068ba9f06028a5\28dc48d6-277e-469e-8ff4-6ad673ba27ca\34070e4cac3243af_0'

with open(bundle_path, 'rb') as fp:
    raw = fp.read()
text = raw.decode('utf-8', errors='ignore')

types_to_find = ['to_do', 'quote', 'callout', 'table_of_contents', 'bookmark', 'transclusion_container', 'button', 'factory', 'file', 'video', 'audio', 'pdf']

for t in types_to_find:
    # Look for format or properties defaults: {type: "to_do", properties: ...}
    # or d.toDo
    matches = [m.start() for m in re.finditer(re.escape(f'"{t}"'), text)]
    print(f"Type '{t}': {len(matches)} occurrences")
    for idx in matches[:2]:
        snippet = text[max(0, idx - 80):min(len(text), idx + 180)]
        print(f"  Snippet: {snippet.strip()}")
