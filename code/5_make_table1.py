# Splits the scheme table into Table 1 (congestion charges, traffic) and Table 2 (LEZs, NO2),
# adds the size class and orders rows by zone area within each table.
from paths import TABLES
W = str(TABLES)
lines = open(f'{W}/table1.md').read().strip().split('\n')
def cat(z):
    try: z = float(z.replace(',', ''))
    except ValueError: return 'Not recovered'
    return 'Small' if z < 10 else 'Medium' if z < 50 else 'Large'
def area(r):
    try: return float(r['Zone (km²)'].replace(',', ''))
    except ValueError: return 1e9
hdr = [c.strip() for c in lines[0].strip('|').split('|')]
rows = [dict(zip(hdr, [c.strip() for c in l.strip('|').split('|')])) for l in lines[2:]]
for r in rows: r['Size class'] = cat(r['Zone (km²)']); r['Measured after (years)'] = r['Years']
cols = {'Charge': ['Scheme', 'Start', 'Zone (km²)', 'Size class', 'Effect (%)', 'Measured after (years)', 'Design',
                   'Charge or fine at launch (2023 USD PPP)', 'Current charge or status (2026)'],
        'LEZ': ['Scheme', 'Start', 'Zone (km²)', 'Size class', 'Effect (%)', 'Measured after (years)', 'Design',
                'Charge or fine at launch (2023 USD PPP)', 'Compliant at launch (%)', 'Current charge or status (2026)']}
rename = {'Effect (%)': {'Charge': 'Traffic change (%)', 'LEZ': 'NO₂ change (%)'}}
for typ, fname in [('Charge', 'table1_cc.md'), ('LEZ', 'table2_lez.md')]:
    sub = sorted([r for r in rows if r['Type'] == typ], key=area)
    h = [rename.get(c, {}).get(typ, c) for c in cols[typ]]
    out = ['| ' + ' | '.join(h) + ' |', '|' + '---|' * len(h)] + ['| ' + ' | '.join(r[c] for c in cols[typ]) + ' |' for r in sub]
    open(f'{W}/{fname}', 'w').write('\n'.join(out) + '\n')
    print(fname, len(sub), 'rows')
