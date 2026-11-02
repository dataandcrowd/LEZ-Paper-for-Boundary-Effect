"""Tasks 3 and 4: merge effects with zone areas and stringency, then analyse.

Inputs: analysis_rows.csv and headline_by_scheme.csv (build_analysis_rows.py),
agent_outputs/areas.csv, agent_outputs/stringency.csv.
Outputs: analysis_dataset.csv (one row per scheme phase), duration_rows.csv,
results.json (all numbers quoted in the manuscript).
"""
import pandas as pd, numpy as np, json, re
from scipy.stats import spearmanr
W = '/home/claude/work/analysis'; A = '/mnt/user-data/outputs/agent_outputs'
rows = pd.read_csv(f'{W}/analysis_rows.csv')
head = pd.read_csv(f'{W}/headline_by_scheme.csv')
areas = pd.read_csv(f'{A}/areas.csv'); st = pd.read_csv(f'{A}/stringency.csv')

# phase key -> (areas ID, phase substring); stringency (ID, phase substring)
amap = {'LON_CC': (4, 'central zone 2003'), 'LON_WEZ': (5, 'alone'), 'MIL_C': (6, 'Area C'),
        'MIL_ECO': (7, 'Ecopass'), 'NYC': (8, 'Congestion'), 'SIN': (10, 'ALS'), 'STO': (11, 'cordon'),
        'VAL': (13, 'Controlled'), 'AMS': (15, 'truck'), 'BCN': (17, 'ZBE'), 'BERLIN': (20, 'LEZ'),
        'BHM': (21, 'Clean'), 'BRD': (22, 'Clean'), 'GLA': (26, 'LEZ'), 'LON_ULEZ19': (29, 'central 2019'),
        'LON_ULEZ23': (29, 'London-wide'), 'MAD_C': (30, 'Madrid Central'), 'MIL_B': (31, 'Area B'),
        'MUC': (32, 'LEZ'), 'SHF': (37, 'Clean'), 'ROM': (45, 'ZTL'), 'LON_LEZ08': (47, 'LEZ'),
        'LIS': (48, 'Zone 1'), 'ANT': (49, 'LEZ'), 'BRU': (50, 'LEZ'),
        'GOT': (3, 'cordon'), 'BGO': (1, 'ring'), 'OSL': (9, 'ring'), 'TRD': (12, 'ring'), 'DUR': (2, 'Saddler')}
smap = {'LON_CC': (4, 'Central zone launch'), 'LON_WEZ': (5, 'Western'), 'MIL_C': (6, 'Area C launch'),
        'MIL_ECO': (7, 'Ecopass'), 'NYC': (8, 'launch'), 'SIN': (10, 'ALS launch'), 'STO': (11, 'Trial'),
        'VAL': (13, 'CVA'), 'AMS': (15, 'Truck'), 'BCN': (17, 'ZBE'), 'BERLIN': (20, 'stage 1'),
        'BHM': (21, 'Class D'), 'BRD': (22, 'Class C+'), 'GLA': (26, 'Phase 2'), 'LON_ULEZ19': (29, 'Central ULEZ'),
        'LON_ULEZ23': (29, 'London-wide'), 'MAD_C': (30, 'Madrid Central'), 'MIL_B': (31, 'Area B'),
        'MUC': (32, 'LEZ stage 1'), 'SHF': (37, 'Class C'), 'ROM': (45, 'ZTL'), 'LON_LEZ08': (47, 'phases 1 and 2'),
        'LIS': (48, 'Phase 2'), 'ANT': (49, 'launch'), 'BRU': (50, 'launch'),
        'GOT': (3, 'Congestion tax launch'), 'BGO': (1, 'launch'), 'OSL': (9, 'launch'), 'TRD': (12, 'launch'), 'DUR': (2, 'launch')}
label = {'LON_CC': 'London CC', 'LON_WEZ': 'London WEZ', 'MIL_C': 'Milan Area C', 'MIL_ECO': 'Milan Ecopass',
         'NYC': 'New York', 'SIN': 'Singapore ALS', 'STO': 'Stockholm', 'VAL': 'Valletta', 'AMS': 'Amsterdam (trucks)',
         'BCN': 'Barcelona', 'BERLIN': 'Berlin', 'BHM': 'Birmingham', 'BRD': 'Bradford', 'GLA': 'Glasgow',
         'LON_ULEZ19': 'ULEZ 2019', 'LON_ULEZ23': 'ULEZ 2023', 'MAD_C': 'Madrid Central', 'MIL_B': 'Milan Area B',
         'MUC': 'Munich', 'SHF': 'Sheffield', 'ROM': 'Rome', 'LON_LEZ08': 'London LEZ (HGV)', 'LIS': 'Lisbon',
         'ANT': 'Antwerp', 'BRU': 'Brussels', 'GOT': 'Gothenburg', 'BGO': 'Bergen', 'OSL': 'Oslo',
         'TRD': 'Trondheim', 'DUR': 'Durham'}

def pick(df, idx, sub, col='Phase'):
    m = df[(df.ID == idx) & df[col].astype(str).str.contains(sub, case=False, regex=False)]
    return m.iloc[0] if len(m) else None

out = []
for _, h in head.iterrows():
    k = h.Phase_key; a = pick(areas, *amap[k]); s = pick(st, *smap[k])
    zone = a.Zone_area_km2_preferred if a is not None else np.nan
    zmin = a.Zone_area_min_km2 if a is not None else np.nan
    zmax = a.Zone_area_max_km2 if a is not None else np.nan
    zsrc = a.Zone_area_method if a is not None else ''
    if k == 'DUR':  # single street; area from Ieromonachou et al. (2007) Table 1 via extraction note
        zone, zmin, zmax, zsrc = 0.35, 0.35, 0.35, 'secondary: Ieromonachou et al. (2007) Table 1'
    bu = a.Builtup_area_km2 if a is not None else np.nan
    out.append(dict(Key=k, Label=label[k], Type=h.Type, Outcome=h.Outcome, Effect_pct=h.Headline_effect_pct,
                    Effect_min=h.Headline_min, Effect_max=h.Headline_max, Band=h.Band, Years=h.Years_median,
                    Design_tier=int(h.Design_tier), Evidence_tier=h.Evidence_tier, Rows_used=h.Rows_used,
                    Zone_km2=zone, Zone_min=zmin, Zone_max=zmax, Zone_source=zsrc, Builtup_km2=bu,
                    Coverage=zone / bu if pd.notna(zone) and pd.notna(bu) else np.nan,
                    Coverage_min=zmin / bu if pd.notna(zmin) and pd.notna(bu) else np.nan,
                    Coverage_max=zmax / bu if pd.notna(zmax) and pd.notna(bu) else np.nan,
                    Start_year=int(str(s.Phase_start)[:4]) if s is not None and pd.notna(s.Phase_start) else np.nan,
                    Charge_type=s.Charge_type if s is not None else '',
                    Charge_usd=s.Charge_2023USD_PPP if s is not None else np.nan,
                    Fine_usd=s.Fine_2023USD_PPP if s is not None else np.nan,
                    Charge_to_income=s.Charge_to_income if s is not None else np.nan,
                    Cars_covered=s.Cars_covered if s is not None else '',
                    Compliance_pct=s.Compliance_at_launch_pct if s is not None else np.nan))
ds = pd.DataFrame(out)
# Rule: zone area is the area of the zone in which the effect was measured (WEZ alone; Lisbon Zone 1).
# ULEZ 2023 compliance from the peer-reviewed evaluation (Tong et al. 2025: 7.4% non-compliant).
ds.loc[ds.Key == 'LON_ULEZ23', 'Compliance_pct'] = 92.6
ds['Journal_evidence'] = ds.Evidence_tier.eq('journal article')
ds.to_csv(f'{W}/analysis_dataset.csv', index=False)

R = {}
def sp(x, y):
    m = x.notna() & y.notna()
    if m.sum() < 4: return dict(n=int(m.sum()), rho=None, p=None)
    r, p = spearmanr(x[m], y[m]); return dict(n=int(m.sum()), rho=round(float(r), 3), p=round(float(p), 3))
for t, o in [('CC', 'Traffic'), ('LEZ', 'NO2')]:
    g = ds[(ds.Type == t) & (ds.Outcome == o)]
    R[t] = {'n_schemes_with_effect': int(len(g)), 'n_with_area': int(g.Coverage.notna().sum()),
            'coverage_all': sp(g.Coverage, g.Effect_pct), 'km2_all': sp(g.Zone_km2, g.Effect_pct),
            'coverage_journal_only': sp(g[g.Journal_evidence].Coverage, g[g.Journal_evidence].Effect_pct),
            'coverage_counterfactual_only': sp(g[g.Design_tier == 1].Coverage, g[g.Design_tier == 1].Effect_pct),
            'coverage_tier12': sp(g[g.Design_tier <= 2].Coverage, g[g.Design_tier <= 2].Effect_pct),
            'median_effect': float(g.Effect_pct.median()),
            'effect_range': [float(g.Effect_pct.min()), float(g.Effect_pct.max())],
            'coverage_range_pct': [round(float(g.Coverage.min() * 100), 2), round(float(g.Coverage.max() * 100), 1)]}
    if t == 'CC':
        R[t]['charge_to_income_vs_effect'] = sp(g.Charge_to_income, g.Effect_pct)
        R[t]['charge_to_income_vs_coverage'] = sp(g.Charge_to_income, g.Coverage)
    else:
        cars = g[g.Cars_covered == 'Y']; nocar = g[g.Cars_covered == 'N']
        R[t]['cars_covered'] = {'n': int(len(cars)), 'median': float(cars.Effect_pct.median()),
                                'coverage_vs_effect': sp(cars.Coverage, cars.Effect_pct)}
        R[t]['cars_not_covered'] = {'n': int(len(nocar)), 'median': float(nocar.Effect_pct.median()),
                                    'schemes': nocar.Label.tolist()}
        R[t]['compliance_vs_effect'] = sp(g.Compliance_pct, g.Effect_pct)
        R[t]['compliance_vs_coverage'] = sp(g.Compliance_pct, g.Coverage)
        R[t]['start_year_vs_coverage'] = sp(g.Start_year, g.Coverage)
# sensitivity analyses
g = ds[(ds.Type == 'CC') & (ds.Outcome == 'Traffic')]
R['CC']['coverage_excl_durham'] = sp(g[g.Key != 'DUR'].Coverage, g[g.Key != 'DUR'].Effect_pct)
R['CC']['km2_excl_durham'] = sp(g[g.Key != 'DUR'].Zone_km2, g[g.Key != 'DUR'].Effect_pct)
R['CC']['km2_journal_only'] = sp(g[g.Journal_evidence].Zone_km2, g[g.Journal_evidence].Effect_pct)
g = ds[(ds.Type == 'LEZ') & (ds.Outcome == 'NO2')]
R['LEZ']['coverage_cars_counterfactual'] = sp(g[(g.Cars_covered == 'Y') & (g.Design_tier == 1)].Coverage, g[(g.Cars_covered == 'Y') & (g.Design_tier == 1)].Effect_pct)
R['LEZ']['coverage_excl_london_2023'] = sp(g[g.Key != 'LON_ULEZ23'].Coverage, g[g.Key != 'LON_ULEZ23'].Effect_pct)
g = ds[(ds.Type == 'LEZ') & (ds.Outcome == 'NO2')].copy()
alt = g.copy(); i = alt.Key == 'LIS'; alt.loc[i, 'Effect_pct'] = -22.0; alt.loc[i, 'Coverage'] = 25.14 / alt.loc[i, 'Builtup_km2']
NS_ZERO = {'BERLIN', 'LON_LEZ08', 'LON_ULEZ23', 'MIL_B'}  # reported only as not significant, charted as 0
gz = ds[(ds.Type == 'LEZ') & (ds.Outcome == 'NO2') & ~ds.Key.isin(NS_ZERO)]
R['LEZ']['coverage_excl_ns_zero'] = sp(gz.Coverage, gz.Effect_pct)
R['LEZ']['ns_zero_schemes'] = sorted(ds[ds.Key.isin(NS_ZERO)].Label.tolist())
R['LEZ']['coverage_lisbon_zone2'] = sp(alt.Coverage, alt.Effect_pct)
R['LEZ']['coverage_lisbon_zone2_cars'] = sp(alt[alt.Cars_covered == 'Y'].Coverage, alt[alt.Cars_covered == 'Y'].Effect_pct)
g = ds[(ds.Type == 'CC') & (ds.Outcome == 'Traffic')].copy()
alt = g.copy(); i = alt.Key == 'LON_WEZ'; alt.loc[i, 'Zone_km2'] = 38.4; alt.loc[i, 'Coverage'] = 38.4 / alt.loc[i, 'Builtup_km2']
R['CC']['coverage_wez_combined'] = sp(alt.Coverage, alt.Effect_pct); R['CC']['km2_wez_combined'] = sp(alt.Zone_km2, alt.Effect_pct)
R['CC']['km2_excl_durham_singapore'] = sp(g[~g.Key.isin(['DUR', 'SIN'])].Zone_km2, g[~g.Key.isin(['DUR', 'SIN'])].Effect_pct)
# terciles of coverage within type for a simple descriptive table
for t, o in [('CC', 'Traffic'), ('LEZ', 'NO2')]:
    g = ds[(ds.Type == t) & (ds.Outcome == o) & ds.Coverage.notna()].copy()
    g['tercile'] = pd.qcut(g.Coverage.rank(method='first'), 3, labels=['small', 'medium', 'large'])  # ties split by order; charge terciles not reported
    R[t]['by_tercile'] = {str(k): {'n': int(len(v)), 'median_effect': float(v.Effect_pct.median()),
                                   'coverage_pct_range': [round(float(v.Coverage.min() * 100), 2), round(float(v.Coverage.max() * 100), 1)],
                                   'schemes': v.Label.tolist()} for k, v in g.groupby('tercile', observed=True)}

# Duration: all main rows with two or more measurements at different years
m = rows[rows.Analysis_set == 'main'].copy()
dur = []
for k, g in m.groupby('Phase_key'):
    # prefer counterfactual series where it has >= 2 years, else before-after series
    for tier in (1, 2, 3):
        gg = g[g.Design_tier == tier]
        def norm(s):
            s = re.sub(r'\(.*?\)', ' ', str(s))
            s = re.sub(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\b', ' ', s)
            s = re.sub(r'\b(19|20)\d{2}\b|\b\d+ months?\b|\bvs\b|\bto\b|\bin\b|\blevels\b|\bfor external factors\b|\badjusted\b', ' ', s)
            return re.sub(r'[^a-z0-9 ]', ' ', s.lower()).split().__str__()
        gg = gg.assign(Metric=gg.Outcome_metric.map(norm))
        ny = gg.groupby(['DOI', 'Metric']).Years_in_operation_at_measurement.nunique()
        if len(ny) and ny.max() >= 2:
            # one series: a single source and a single metric, the one with the most distinct years
            src, met = ny.idxmax()
            gs = gg[(gg.DOI == src) & (gg.Metric == met)].groupby('Years_in_operation_at_measurement').Effect_pct.median()
            for y, e in gs.items():
                dur.append(dict(Key=k, Label=label[k], Type=g.Type.iloc[0], Outcome=g.Outcome.iloc[0],
                                Years=y, Effect_pct=e, Design_tier=tier, DOI=src))
            break
dr = pd.DataFrame(dur); dr.to_csv(f'{W}/duration_rows.csv', index=False)
pers = []
for k, g in dr.groupby('Key'):
    g = g.sort_values('Years'); e0, e1 = g.Effect_pct.iloc[0], g.Effect_pct.iloc[-1]
    pers.append(dict(Key=k, Label=g.Label.iloc[0], Type=g.Type.iloc[0], first_years=float(g.Years.iloc[0]),
                     last_years=float(g.Years.iloc[-1]), first=float(e0), last=float(e1),
                     ratio=(round(float(e1 / e0), 2) if e0 * e1 > 0 else 'n/a (sign change)') if e0 != 0 else None))
R['persistence'] = pers
# reversal and marginal evidence
R['reversal'] = rows[rows.Analysis_set == 'reversal'][['Scheme', 'Effect_pct', 'Years_in_operation_at_measurement']].to_dict('records')
R['marginal'] = rows[rows.Analysis_set == 'marginal'][['Scheme', 'Outcome', 'Effect_pct']].to_dict('records')
R['pooled'] = rows[rows.Analysis_set == 'pooled'][['Scheme', 'Outcome', 'Effect_pct', 'Years_in_operation_at_measurement', 'Design']].to_dict('records')
R['counts'] = {'effect_rows_total': int(len(rows)), 'main_rows': int((rows.Analysis_set == 'main').sum()),
               'articles': int(rows.DOI.nunique()), 'schemes_with_headline': int(len(ds)),
               'schemes_in_fig1': int(ds.Coverage.notna().sum())}
json.dump(R, open(f'{W}/results.json', 'w'), indent=1, default=str)
pd.set_option('display.width', 250)
print(ds[['Label', 'Type', 'Effect_pct', 'Zone_km2', 'Builtup_km2', 'Coverage', 'Years', 'Design_tier', 'Charge_to_income', 'Cars_covered', 'Compliance_pct']].to_string())
print(json.dumps({k: v for k, v in R.items() if k in ('CC', 'LEZ', 'persistence', 'counts')}, indent=1, default=str))
