import re

with open(r'C:\Users\Joaco\AppData\Local\Temp\rea-extracted-bbb5eea6-b4a8-423f-ae8b-d1f2104cf88e\.webpack\main\index.js', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

print("index.js size:", len(content))

keywords = ['bulleted_list', 'numbered_list', 'header_4', 'sub_sub_header', 'table_row', 'column_list', 'collection_view', 'to_do', 'callout', 'quote']
for kw in keywords:
    matches = [m.start() for m in re.finditer(re.escape(kw), content)]
    print(f"Keyword '{kw}': {len(matches)} occurrences")
    for idx in matches[:3]:
        snippet = content[max(0, idx - 100):min(len(content), idx + 150)]
        print(f"   Snippet: {snippet}\n")
