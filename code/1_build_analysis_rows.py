"""Task 3: select and classify effect rows for the boundary-size analysis.

Rules (documented in docs/analysis_rules.md):
- Primary outcome by scheme type: congestion charges (CC) -> traffic volume;
  emission zones (LEZ) -> NO2 concentration. PM10 for LEZs is a secondary outcome.
- Location: CC prefer cordon crossings, else inside-zone traffic; LEZ inside zone only.
- Excluded from the main set (kept in separate sets):
  * spatial contrast designs (Ding et al. 2022 spatial RDD),
  * marginal changes to an existing scheme (charge increases, extensions to new
    time windows, tightening inside an existing LEZ),
  * removals or suspensions (kept as 'reversal' evidence),
  * pooled multi-city estimates (no single zone size; kept as a reference band),
  * rows with no numeric effect.
- Design tier: 1 = untreated control or natural experiment (DiD, synthetic control,
  RDD in time, ITS with a control or natural experiment), 2 = adjusted before-after
  (ITS without control), 3 = before-after (raw or reference site), 4 = model-based.
- Evidence source tier: journal article vs conference or council data reported in
  a peer-reviewed review (Singapore, Valletta, Oslo, Bergen, Trondheim 1991, Durham).
- Duration band from years in operation at measurement: short < 1.5, medium 1.5 to < 4,
  long >= 4.
- Headline estimate per scheme phase (Figure 1): rows in the main set, earliest
  duration band available, best design tier available within it, median if several.
"""
import pandas as pd, numpy as np, re, sys
from paths import EXTRACT, ANALYSIS
cc = pd.read_csv(EXTRACT / 'cc_effects.csv'); cc['Type'] = 'CC'
lz = pd.read_csv(EXTRACT / 'lez_effects.csv'); lz['Type'] = 'LEZ'
# Rows from the November 2026 peer-reviewed search are appended last so that earlier row numbers stay stable.
upd = pd.read_csv(EXTRACT / 'cc_effects_update_2026-11.csv'); upd['Type'] = 'CC'
updl = pd.read_csv(EXTRACT / 'lez_effects_update_2026-11.csv'); updl['Type'] = 'LEZ'
d = pd.concat([cc, lz, upd, updl], ignore_index=True)
d.insert(0, 'Row', range(1, len(d) + 1))

def key(r):
    s = r.Scheme.lower(); c = r.City.lower()
    if r.Type == 'CC':
        if 'western' in s: return 'LON_WEZ'
        if c == 'london': return 'LON_CC'
        if c == 'stockholm': return 'STO'
        if c == 'gothenburg': return 'GOT'
        if 'ecopass' in s: return 'MIL_ECO'
        if 'area c' in s: return 'MIL_C'
        if c == 'singapore': return 'SIN'
        return {'valletta': 'VAL', 'oslo': 'OSL', 'bergen': 'BGO', 'trondheim': 'TRD',
                'durham': 'DUR', 'new york': 'NYC'}[c]
    if 'street-specific' in s: return 'STREET_BAN'
    if 'm-30' in s: return 'MAD_ZBE'
    if c.startswith('tokyo'): return 'TOK'
    if c == 'seoul': return 'SEO_GTZ' if 'green transport' in s else 'SEO_LEZ'
    if 'ulez central' in s: return 'LON_ULEZ19'
    if 'ulez greater' in s: return 'LON_ULEZ23'
    if 'lez for heavy' in s: return 'LON_LEZ08'
    if 'german' in c: return 'DE_POOL'
    if 'european' in c: return 'EU_POOL'
    if 'netherlands' in c: return 'NL_POOL'
    return {'berlin': 'BERLIN', 'munich': 'MUC', 'birmingham': 'BHM', 'sheffield': 'SHF',
            'bradford': 'BRD', 'glasgow': 'GLA', 'madrid': 'MAD_C', 'barcelona': 'BCN',
            'milan': 'MIL_B', 'rome': 'ROM', 'lisbon': 'LIS', 'amsterdam': 'AMS',
            'antwerp': 'ANT', 'brussels': 'BRU', 'ghent': 'GHE', 'rotterdam': 'ROT', 'stuttgart': 'STU',
            'seville': 'SEV', 'leipzig': 'LEI', 'darmstadt': 'STREET_BAN', 'hamburg': 'STREET_BAN'}[c]

d['Scheme_key'] = d.apply(key, axis=1)

def fam(o):
    o = str(o)
    if o == 'Traffic': return 'Traffic'
    if o in ('NO2',): return 'NO2'
    if o in ('PM10',): return 'PM10'
    return o
d['Outcome'] = d.Outcome_family.map(fam)
# CC air-quality rows: classify pollutant from metric text
for i, r in d[(d.Type == 'CC') & (d.Outcome == 'Air quality')].iterrows():
    m = str(r.Outcome_metric)
    d.at[i, 'Outcome'] = ('NO2' if 'NO2' in m else 'NOx' if 'NOx' in m else 'PM2.5' if 'PM2.5' in m else
                          'PM10' if 'PM10' in m else 'CO' if m.startswith('CO ') or ' CO ' in m else
                          'Black carbon' if 'black carbon' in m.lower() else 'Other AQ')

# Design tier: 1 = untreated control group or natural experiment; 2 = before-after adjusted
# for external factors without a control (interrupted time series without control);
# 3 = raw or reference-site before-after; 4 = model-based.
tier = {'DiD': 1, 'Synthetic control': 1, 'RDD': 1, 'Interrupted time series': 2,
        'Before-after': 3, 'Model-based': 4}
d['Design_tier'] = d.Design.map(tier)
ITS_WITH_CONTROL = {'10.1016/j.jue.2015.06.005',   # Gibson and Carnovale: court-suspension natural experiment
                    '10.3390/ijerph17031088',      # Maranzano et al.: neighbouring-city counterfactual
                    '10.1016/j.atmosenv.2009.07.023'}  # Atkinson et al.: control zone
d.loc[(d.Design == 'Interrupted time series') & d.DOI.isin(ITS_WITH_CONTROL), 'Design_tier'] = 1
ev = {'SIN': 'journal article without DOI (JEASTS 1995)', 'VAL': 'conference paper (WCTR 2013)',
      'OSL': 'conference paper citing thesis', 'BGO': 'secondary citation in journal review',
      'DUR': 'council monitoring reported in journal review'}
d['Evidence_tier'] = [ev.get(k, 'journal article') if not (k == 'TRD' and 'removed' not in s.lower()) else 'conference paper (WCTR 2007)'
                      for k, s in zip(d.Scheme_key, d.Scheme)]

yrs = d.Years_in_operation_at_measurement
d['Duration_band'] = np.select([yrs < 1.5, yrs < 4], ['short', 'medium'], 'long')

# Traffic rows kept out of the headline set although measured inside the zone or at the cordon
SECONDARY_DOI = {
    '10.1177/1087724X04268569': 'restates TfL monitoring already charted from Givoni (2012)',
    '10.1007/s11116-017-9853-4': '24-hour count from the same city counts as Borjesson and Kristoffersson (2015)',
    '10.32866/001c.155761': 'ride-hailing trips only, not total traffic',
    '10.1016/j.cstp.2014.07.001': 'parked vehicles as a proxy for traffic',
}
# Schemes whose traffic evidence originates in grey literature (decision of 4 November 2026)
EXCLUDED_SCHEMES = {
    'DUR': 'excluded: the traffic estimate originates in council monitoring (cited in May et al. 2010)',
    'VAL': 'excluded: the traffic estimate originates in a conference paper, and the peer-reviewed source uses parked cars as a proxy',
}
EXCLUDED_SCHEMES['STREET_BAN'] = 'excluded: street-specific diesel ban, not a bounded zone'
EXCLUDED_DOI = {'10.1016/j.atmosenv.2024.120326': 'excluded: before and after periods fall in different seasons, and the authors do not attribute the change to the zone'}
SECONDARY_DOI['10.1016/S2468-2667(18)30202-0'] = 'trend over 2006 to 2013, not attributed to the LEZ by the authors'
# Schemes found in the November 2026 search that are not in the 50-scheme inventory (no verified zone area yet)
OUTSIDE_INVENTORY = {'MAD_ZBE', 'TOK', 'SEO_LEZ', 'SEO_GTZ', 'GHE', 'ROT', 'STU', 'SEV', 'LEI'}
set_, why = [], []
for _, r in d.iterrows():
    s = r.Scheme.lower(); m = str(r.Outcome_metric).lower(); n = str(r.Extractor_notes).lower()
    if r.Scheme_key in EXCLUDED_SCHEMES:
        set_.append('excluded'); why.append(EXCLUDED_SCHEMES[r.Scheme_key]); continue
    if r.DOI in EXCLUDED_DOI:
        set_.append('excluded'); why.append(EXCLUDED_DOI[r.DOI]); continue
    if pd.isna(r.Effect_pct):
        set_.append('excluded'); why.append('no numeric effect'); continue
    if r.DOI == '10.1080/15568318.2021.1914790':
        set_.append('excluded'); why.append('spatial contrast design (inside vs outside boundary), not a change estimate'); continue
    if 'removed' in s or 'abolition' in m or (r.Effect_pct > 10 and r.Type == 'CC' and r.Outcome == 'Traffic'):
        set_.append('reversal'); why.append('scheme removal: traffic change after charge withdrawn'); continue
    if r.DOI in SECONDARY_DOI and r.Type == 'CC' and r.Outcome == 'Traffic':
        set_.append('secondary'); why.append(SECONDARY_DOI[r.DOI]); continue
    if any(k in s for k in ['charge increase', '2016 charge', 'evening extension', 'selective diesel ban',
                            'rush-hour charge', 'end of green-vehicle exemption', 'tightened rules']):
        set_.append('marginal'); why.append('marginal change to an existing scheme'); continue
    if r.Scheme_key in OUTSIDE_INVENTORY:
        set_.append('secondary'); why.append('scheme or stage outside the 50-scheme inventory, not in Figure 1'); continue
    if r.DOI in SECONDARY_DOI:
        set_.append('secondary'); why.append(SECONDARY_DOI[r.DOI]); continue
    if r.Scheme_key in ('DE_POOL', 'NL_POOL', 'EU_POOL'):
        set_.append('pooled'); why.append('pooled multi-city estimate, no single zone size'); continue
    if r.Type == 'CC':
        if r.Outcome == 'Traffic' and r.Measured_where in ('Cordon crossing', 'Inside zone'):
            set_.append('main'); why.append('CC traffic'); continue
        if r.Outcome == 'Traffic':
            set_.append('secondary'); why.append(f'CC traffic measured {str(r.Measured_where).lower()}'); continue
        set_.append('secondary'); why.append('CC air quality (secondary outcome)'); continue
    if r.Outcome == 'NO2' and r.Measured_where == 'Inside zone':
        set_.append('main'); why.append('LEZ NO2 inside zone'); continue
    if r.Outcome == 'PM10' and r.Measured_where == 'Inside zone':
        set_.append('secondary'); why.append('LEZ PM10 (secondary outcome)'); continue
    set_.append('secondary'); why.append(f'LEZ {r.Outcome} {r.Measured_where} (secondary)')
d['Analysis_set'] = set_; d['Set_reason'] = why

# London Givoni and Green rows: vehicle-km inside zone (CC), keep; Green et al. duplicates Givoni-type quantity
# Phase key: ULEZ, LEZ stages share boundary within city except ULEZ19 vs ULEZ23 (separate keys already)
d['Phase_key'] = d.Scheme_key

def headline(g):
    g = g[g.Analysis_set == 'main']
    if g.empty: return None
    order = {'short': 0, 'medium': 1, 'long': 2}
    b = min(g.Duration_band, key=lambda x: order[x]); g = g[g.Duration_band == b]
    t = g.Design_tier.min(); g = g[g.Design_tier == t]
    return pd.Series({'Type': g.Type.iloc[0], 'Outcome': g.Outcome.iloc[0],
                      'Headline_effect_pct': float(np.median(g.Effect_pct)),
                      'Headline_min': g.Effect_pct.min(), 'Headline_max': g.Effect_pct.max(),
                      'N_rows': len(g), 'Band': b, 'Design_tier': int(t),
                      'Years_median': float(np.median(g.Years_in_operation_at_measurement)),
                      'Evidence_tier': g.Evidence_tier.iloc[0],
                      'Rows_used': ';'.join(map(str, g.Row))})
h = d.groupby('Phase_key').apply(headline).dropna(how='all').reset_index()
d.to_csv(ANALYSIS / 'analysis_rows.csv', index=False)
h.to_csv(ANALYSIS / 'headline_by_scheme.csv', index=False)
print(d.Analysis_set.value_counts().to_string())
print(h.to_string())
