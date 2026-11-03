import sqlite3
import json

db_path = r'C:\Users\Joaco\AppData\Roaming\Notion\notion.db'
con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("Tables in notion.db:")
for t in tables:
    cur.execute(f'SELECT count(*) FROM "{t}"')
    cnt = cur.fetchone()[0]
    print(f"  {t}: {cnt} rows")

print("\n--- Detailed Block Types and Schema Breakdown ---")
cur.execute("SELECT type, count(*) as c FROM block GROUP BY type ORDER BY c DESC")
types_count = cur.fetchall()
print(f"Total block types found: {len(types_count)}")
for t, c in types_count:
    print(f"  - {t}: {c} instances")
