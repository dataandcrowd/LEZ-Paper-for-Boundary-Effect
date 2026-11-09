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

# Table 3: zones lifted or suspended (charges from removals_charges.csv, German LEZs from german_lez_removals.csv)
import pandas as pd
from paths import CURATED
ch = pd.read_csv(CURATED / 'removals_charges.csv'); gr = pd.read_csv(CURATED / 'german_lez_removals.csv')
yr = lambda s: str(s).split()[-1]
L = ['| Scheme | In operation | Years | Basis for removal, or change after removal | Evaluated after removal |', '|---|---|---|---|---|']
for _, r in ch.iterrows():
    y = '2-month suspension' if r.Years < 1 else f'{r.Years:g}'
    L.append(f'| {r.Scheme} | {r.Operated} | {y} | {r.After_removal} ({r.Source}) | Yes |')
bw = gr[gr.State == 'Baden-Württemberg']
L.append(f"| German LEZs, Baden-Württemberg ({len(bw)} zones) | {min(int(yr(v)) for v in bw.Introduced)} to {max(int(yr(v)) for v in bw.Introduced)}, lifted {min(int(yr(v)) for v in bw.Lifted)} to {max(int(yr(v)) for v in bw.Lifted)} | median {bw.Years.median():.1f} (range {bw.Years.min():.1f} to {bw.Years.max():.1f}) | Measured NO₂ below a threshold of 33 to 36 µg/m³ for about three years, set from the largest rise expected without the zone (LUBW, 2020). Balingen was lifted earlier, on a worst-case rise of about 3 µg/m³ | No |")
for z, txt in [('Hannover', 'Forecast NO₂ for 2024 of 33 µg/m³ with the zone and 34 without'),
               ('Neu-Ulm', 'Modelled rise without the zone at most 0.7 µg/m³ NO₂'),
               ('Erfurt', 'Annulled by the Thüringen Higher Administrative Court'),
               ('Mainz', 'Limits clearly met in 2024, no figure given')]:
    r = gr[gr.Zone == z].iloc[0]
    L.append(f'| German LEZ, {z} ({r.State}) | {yr(r.Introduced)} to {yr(r.Lifted)} | {r.Years:.1f} | {txt} | No |')
open(f'{W}/table3_removals.md', 'w').write('\n'.join(L) + '\n')
print('table3_removals.md', len(L) - 2, 'rows')
