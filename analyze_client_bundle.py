import re

files_to_check = [
    r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage\614a0024a405b02cc875d3e091267a8eb895f9ee\f051f901-b7c0-4aef-9d87-cb031eb4c66b\8cbceebc64912dc2_1',
    r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage\614a0024a405b02cc875d3e091267a8eb895f9ee\f051f901-b7c0-4aef-9d87-cb031eb4c66b\ef0ca39f9c8a3890_0'
]

for fpath in files_to_check:
    print(f"\n================ Scanning: {fpath} ================")
    with open(fpath, 'rb') as fp:
        raw = fp.read()
    
    # Clean non-ascii or find UTF-8 text
    text = raw.decode('utf-8', errors='ignore')
    print(f"File text length: {len(text)} chars")
    
    # 1. Look for block type definitions/enums
    # Often formatted as: {page:"page",text:"text",header:"header",...} or [ "page", "text", "header", ... ]
    m_enum = re.findall(r'(\b[a-zA-Z_$0-9]+\s*=\s*\{(?=[^}]*\"bulleted_list\")[^}]+\})', text)
    if m_enum:
        print(f"Found {len(m_enum)} enum candidates matching bulleted_list:")
        for e in m_enum[:5]:
            print("  Enum:", e[:300])

    # 2. Look for schema or default properties definitions
    m_schemas = re.findall(r'(\b[a-zA-Z_$0-9]+\s*=\s*\{(?=[^}]*bulleted_list:[^}]*properties)[^}]+\})', text)
    if m_schemas:
        print(f"Found {len(m_schemas)} schema candidates:")
        for s in m_schemas[:5]:
            print("  Schema:", s[:300])

    # 3. Look for function createBlock / makeBlock / newBlock
    m_func = re.findall(r'(function\s+(?:createBlock|makeBlock|buildBlock|newBlock|createEmptyBlock)[^{]*\{[^}]{0,500}\})', text)
    if m_func:
        print(f"Found {len(m_func)} factory functions:")
        for fn in m_func[:5]:
            print("  Factory:", fn[:200])

    # 4. Search for transaction operations list
    ops_matches = re.findall(r'(\b(?:set|update|listAfter|listBefore|listRemove)\b[^\n,;]{0,50})', text)
    print(f"Operation keywords count: {len(ops_matches)}")
