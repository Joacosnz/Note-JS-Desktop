import re

bundle_path = r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage\5381cb7d7f0d31a6afec904154068ba9f06028a5\28dc48d6-277e-469e-8ff4-6ad673ba27ca\34070e4cac3243af_0'

with open(bundle_path, 'rb') as fp:
    raw = fp.read()
text = raw.decode('utf-8', errors='ignore')

# Search for transaction operations: command: "set", "listAfter", "update"
# or saveTransactions
for term in ['saveTransactions', 'buildBlock', 'makeBlock', 'createBlock', '"listAfter"', '"set"', '"update"']:
    matches = [m.start() for m in re.finditer(re.escape(term), text)]
    print(f"Term {term}: {len(matches)} matches")
    for idx in matches[:2]:
        print(f"Snippet around {term}:")
        print(text[max(0, idx - 100):min(len(text), idx + 200)])
