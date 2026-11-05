"""Tables of every estimate of traffic and air quality, city by city: congestion charges (Supplementary Table S13) and low emission zones (Table S14).

All values come from output/analysis/analysis_rows.csv, which is built from data/extraction.
"""
import re
import pandas as pd
from paths import ANALYSIS, TABLES

r = pd.read_csv(ANALYSIS / 'analysis_rows.csv')
order_out = {'Traffic': 0, 'Fleet': 1, 'NO2': 2, 'NOx': 3, 'PM10': 4, 'PM2.5': 5, 'CO': 6, 'Black carbon': 7, 'Other AQ': 8}
design = {1: 'Control or natural experiment', 2: 'Adjusted before-after', 3: 'Before-after', 4: 'Model-based'}
use = {'main': 'Headline candidate', 'secondary': 'Secondary', 'marginal': 'Change to an existing scheme',
       'reversal': 'Removal or suspension', 'excluded': 'Not charted'}

def short(c):
    c = str(c).replace('Ouali, L. A. B.', 'Ait Bihi Ouali, L.')
    y = re.search(r'\((\d{4})', c); y = y.group(1) if y else ''
    au = c.split('(')[0]
    fam = [x.strip() for x in re.split(r'[,&]', au) if x.strip() and not x.strip().endswith('.') and x.strip() != '...']
    s = fam[0] if len(fam) == 1 else (f'{fam[0]} and {fam[1]}' if len(fam) == 2 else (f'{fam[0]} et al.' if fam else au.strip()))
    return f'{s} ({y})'

def effect(x):
    if pd.isna(x.Effect_pct):
        n = str(x.Extractor_notes).lower()
        return 'not significant' if 'not significant' in n or 'not statistically' in n else 'direction only'
    return f'{x.Effect_pct:+.1f}'.replace('-', '−')

def build(cc, city_order, stem):
    cc['City_order'] = cc.City.map({c: i for i, c in enumerate(city_order)}).fillna(99)
    cc['Out_order'] = cc.Outcome.map(order_out).fillna(9)
    cc = cc.sort_values(['City_order', 'Scheme', 'Out_order', 'Years_in_operation_at_measurement'])
    out = pd.DataFrame({
        'City': cc.City, 'Scheme': cc.Scheme, 'Outcome': cc.Outcome.replace({'NO2': 'NO₂', 'NOx': 'NOₓ'}),
        'Measure': cc.Outcome_metric, 'Effect (%)': cc.apply(effect, axis=1),
        'Years in operation': cc.Years_in_operation_at_measurement.map(lambda v: '' if pd.isna(v) else f'{v:.1f}'),
        'Design': cc.Design_tier.map(design), 'Use in this review': cc.Analysis_set.map(use),
        'Source': cc.Peer_reviewed_citation.map(short) + cc.DOI.map(lambda d: '' if d == 'NO-DOI' else f', doi:{d}')})
    out.to_csv(TABLES / f'{stem}.csv', index=False)
    md = '| ' + ' | '.join(out.columns) + ' |\n|' + '---|' * len(out.columns) + '\n'
    md += '\n'.join('| ' + ' | '.join(str(v) for v in row) + ' |' for row in out.values) + '\n'
    (TABLES / f'{stem}.md').write_text(md)

    # compact summary by city and outcome (counts and range of reported percentage changes)
    s = cc[cc.Effect_pct.notna() & cc.Analysis_set.isin(['main', 'secondary'])]
    summ = s.groupby(['City', 'Outcome']).Effect_pct.agg(['count', 'min', 'median', 'max']).round(1)
    summ.to_csv(TABLES / f'{stem}_summary.csv')
    print(len(out), 'rows'); print(summ.to_string())


build(r[r.Type == 'CC'].copy(), ['London', 'Stockholm', 'Gothenburg', 'Milan', 'Singapore', 'New York', 'Oslo', 'Bergen',
                                  'Trondheim', 'Valletta', 'Durham'], 'cc_city_evidence')
build(r[r.Type == 'LEZ'].copy(), ['London', 'Birmingham', 'Bradford', 'Glasgow', 'Sheffield', 'Amsterdam', 'Rotterdam',
                                   'Netherlands (five cities incl. Amsterdam and Utrecht)', 'Antwerp', 'Brussels', 'Ghent',
                                   'Berlin', 'Munich', 'Stuttgart', 'German LEZs (pooled)', 'Lisbon', 'Madrid', 'Barcelona',
                                   'Seville', 'Milan', 'Rome', 'Seoul', 'Tokyo (Greater Tokyo)'], 'lez_city_evidence')
