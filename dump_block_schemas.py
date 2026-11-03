import sqlite3, json

db_path = r'C:\Users\Joaco\AppData\Roaming\Notion\notion.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute("SELECT DISTINCT type FROM block")
types = [r[0] for r in cur.fetchall()]

schema_dump = {}

for t in sorted(types):
    cur.execute("""
        SELECT id, space_id, type, properties, format, content, parent_id, parent_table, alive, crdt_format_version, crdt_data
        FROM block 
        WHERE type = ? 
        ORDER BY LENGTH(COALESCE(properties, '')) DESC 
        LIMIT 3
    """, (t,))
    rows = cur.fetchall()
    
    samples = []
    for r in rows:
        samples.append({
            "type": r[2],
            "properties": json.loads(r[3]) if r[3] else None,
            "format": json.loads(r[4]) if r[4] else None,
            "content": json.loads(r[5]) if r[5] else None,
            "parent_table": r[7],
            "crdt_format_version": r[9],
            "crdt_data": json.loads(r[10]) if r[10] else None
        })
    schema_dump[t] = samples

with open("notion_block_schemas_extracted.json", "w", encoding="utf-8") as f:
    json.dump(schema_dump, f, indent=2, ensure_ascii=False)

print(f"Dumped detailed schemas for {len(schema_dump)} block types from notion.db to notion_block_schemas_extracted.json")
