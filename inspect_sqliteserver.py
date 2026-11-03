with open(r'C:\Users\Joaco\AppData\Local\Temp\rea-extracted-bbb5eea6-b4a8-423f-ae8b-d1f2104cf88e\.webpack\main\SqliteServer.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(|([a-zA-Z0-9_$]+)\s*=\s*function|class\s+([a-zA-Z0-9_$]+)', text)
found = set()
for m in matches:
    for name in m:
        if name and len(name) > 2:
            found.add(name)
print("Functions/classes:", list(found)[:40])

# Search for mentions of "block" or "transaction"
print("\nMentions of 'block':")
for line in text.split('\n'):
    if 'block' in line.lower() or 'transaction' in line.lower():
        print(line[:150])
