"""
export_csv.py 
"""
import csv
import pathlib
import sqlite3
import sys

if len(sys.argv) < 2:
    sys.exit(__doc__)

src = sys.argv[1]
out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "csv_out")
out.mkdir(parents=True, exist_ok=True)

if src.lower().endswith(".sql"):
    conn = sqlite3.connect(":memory:")
    with open(src, encoding="utf-8") as f:
        conn.executescript(f.read())
else:
    conn = sqlite3.connect(src)

tables = [r[0] for r in conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]

for t in tables:
    cur = conn.execute('SELECT * FROM "%s"' % t)
    headers = [d[0] for d in cur.description]
    path = out / (t.lower() + ".csv")
    count = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        for row in cur:
            w.writerow(["" if v is None else v for v in row])
            count += 1
    print("%-24s %4d rows -> %s" % (t, count, path))

print("\nTables exported:", len(tables))

