import sqlite3
import json
from collections import defaultdict

DB='data.db'
conn=sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur=conn.cursor()
# get counts grouped by variant and event_type for high_margin
cur.execute("SELECT variant, event_type, is_high_margin, COUNT(*) as cnt FROM events GROUP BY variant, event_type, is_high_margin")
rows = cur.fetchall()
summary = defaultdict(lambda: defaultdict(int))
for r in rows:
    variant = r['variant'] or 'unknown'
    event_type = r['event_type']
    is_high = bool(r['is_high_margin'])
    cnt = r['cnt']
    summary[variant][(event_type, is_high)] = cnt

print(json.dumps({v: {f'{k[0]}_high' if k[1] else f'{k[0]}_low': cnt for k,cnt in d.items()} for v,d in summary.items()}, indent=2, ensure_ascii=False))

# Also compute conversion rates for high-margin only
for variant in summary:
    views = summary[variant].get(('view', True), 0)
    converts = summary[variant].get(('convert', True), 0)
    ctr = None
    if views>0:
        ctr = converts / views
    print(f"Variant {variant}: views_high={views}, converts_high={converts}, conv_rate={ctr}")

conn.close()
