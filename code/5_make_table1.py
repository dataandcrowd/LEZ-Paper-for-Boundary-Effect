# Adds the size category column to Table 1 and orders rows by type and zone area.
from paths import TABLES
W = str(TABLES)
lines = open(f'{W}/table1.md').read().strip().split('\n')
def cat(z):
    try: z = float(z.replace(',', ''))
    except ValueError: return 'Not recovered'
    return 'Street' if z < 1 else 'City centre' if z < 10 else 'Inner city' if z < 50 else 'Whole city' if z < 500 else 'Metropolitan'
hdr = [c.strip() for c in lines[0].strip('|').split('|')]
rows = [[c.strip() for c in l.strip('|').split('|')] for l in lines[2:]]
for r in rows: r.insert(4, cat(r[3]))
hdr.insert(4, 'Size category')
def area(r):
    try: return float(r[3].replace(',', ''))
    except ValueError: return 1e9
rows.sort(key=lambda r: (r[1] != 'Charge', area(r)))
out = ['| ' + ' | '.join(hdr) + ' |', '|' + '---|' * len(hdr)] + ['| ' + ' | '.join(r) + ' |' for r in rows]
open(f'{W}/table1_rr.md', 'w').write('\n'.join(out) + '\n')
print(len(rows), 'rows')
