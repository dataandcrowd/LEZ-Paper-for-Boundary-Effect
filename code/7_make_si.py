import pandas as pd, json, re
from paths import ANALYSIS, CURATED, EXTRACT, TEMPLATES, MANUSCRIPT, TABLES
A=str(ANALYSIS); G=str(EXTRACT); CUR=str(CURATED)
ds=pd.read_csv(f'{A}/analysis_dataset.csv'); rows=pd.read_csv(f'{A}/analysis_rows.csv'); R=json.load(open(f'{A}/results.json'))
st=pd.read_csv(f'{G}/stringency.csv')
tiers={1:'Control or natural experiment',2:'Adjusted before-after',3:'Before-after',4:'Model'}
def short(c):
    c=c.replace('Ouali, L. A. B.','Ait Bihi Ouali, L.')
    au=c.split('(')[0].strip().rstrip(','); y=re.search(r'\((\d{4})',c); y=y.group(1) if y else ''
    toks=[x.strip() for x in re.split(r'[,&]',au) if x.strip()]
    fam=[x for x in toks if not x.endswith('.') and x != '...']
    if not fam: return f'{au} ({y})'
    s=fam[0] if len(fam)==1 else (f'{fam[0]} and {fam[1]}' if len(fam)==2 else f'{fam[0]} et al.')
    return f'{s} ({y})'
def cite(rid):
    sub=rows[rows.Row.isin([int(x) for x in str(rid).split(';')])]
    out=[]
    for _,r in sub.iterrows():
        s=short(r.Peer_reviewed_citation)+('' if r.DOI=='NO-DOI' else f', doi:{r.DOI}')
        if s not in out: out.append(s)
    return ' and '.join(out)
L=['| Scheme | Outcome metric used | Effect (%) | Design | Source(s) | Evidence tier |','|---|---|---|---|---|---|']
for _,r in ds.sort_values(['Type','Label']).iterrows():
    met=rows[rows.Row.isin([int(x) for x in str(r.Rows_used).split(';')])].Outcome_metric.iloc[0]
    if int(r.N_rows if 'N_rows' in r else 1)>1 or ';' in str(r.Rows_used): met=f"Median of {len(str(r.Rows_used).split(';'))} estimates, e.g. {met}"
    L.append(f"| {r.Label} | {met} | {r.Effect_pct:.1f} | {tiers[int(r.Design_tier)]} | {cite(r.Rows_used)} | {r.Evidence_tier} |")
S1='\n'.join(L)
smap={'LON_CC':(4,'Central zone launch'),'LON_WEZ':(5,'Western'),'MIL_C':(6,'Area C launch'),'MIL_ECO':(7,'Ecopass'),'NYC':(8,'launch'),'SIN':(10,'ALS launch'),'STO':(11,'Trial'),'VAL':(13,'CVA'),'AMS':(15,'Truck'),'BCN':(17,'ZBE'),'BERLIN':(20,'stage 1'),'BHM':(21,'Class D'),'BRD':(22,'Class C+'),'GLA':(26,'Phase 2'),'LON_ULEZ19':(29,'Central ULEZ'),'LON_ULEZ23':(29,'London-wide'),'MAD_C':(30,'Madrid Central'),'MIL_B':(31,'Area B'),'MUC':(32,'LEZ stage 1'),'SHF':(37,'Class C'),'ROM':(45,'ZTL'),'LON_LEZ08':(47,'phases 1 and 2'),'LIS':(48,'Phase 2'),'ANT':(49,'launch'),'BRU':(50,'launch'),'GOT':(3,'Congestion tax launch'),'BGO':(1,'launch'),'OSL':(9,'launch'),'TRD':(12,'launch'),'DUR':(2,'launch')}
def clean(s):
    s=str(s)
    tags=sorted(set(x.strip().split(',')[0].split(' ')[0].lower() for x in re.findall(r'\[([^\]]*)\]?',s)))
    s=re.sub(r'\[[^\]]*\]?','',s)
    s=s.replace('per caller and notes','').replace('Stringency notes;','').replace('Beria and Boggio (2013);','').replace('Beria and Boggio (2013)','')
    s=re.sub(r'\s*;\s*;',';',s); s=re.sub(r'\s+',' ',s).strip(' ;,')
    keep=[x for x in tags if x in ('peer-reviewed','official','grey','news','working')]
    return s+(f" ({', '.join('working paper' if x=='working' else x for x in keep)})" if keep else '')
def srow(k):
    i,s=smap[k]; m=st[(st.ID==i)&st.Phase.astype(str).str.contains(s,case=False,regex=False)]
    return m.iloc[0] if len(m) else None
L=['| Scheme | Zone (km²), preferred (min to max) | Zone area source | Urban centre (km²) | Charge or fine source | Compliance at launch (%) and source |','|---|---|---|---|---|---|']
for _,r in ds.sort_values(['Type','Label']).iterrows():
    z='' if pd.isna(r.Zone_km2) else f"{r.Zone_km2:g} ({r.Zone_min:g} to {r.Zone_max:g})"
    zs=str(r.Zone_source).replace('computed by agent from polygon','computed from polygon') if pd.notna(r.Zone_source) else ''
    s=srow(r.Key); cs=(clean(s.Charge_source)[:200] if s is not None and pd.notna(s.Charge_source) else '')
    if r.Key=='LON_ULEZ23': comp='92.6, Tong et al. (2025), entering vehicles'
    elif pd.notna(r.Compliance_pct) and s is not None:
        comp=f"{r.Compliance_pct:g}, {clean(s.Compliance_source)[:160]}"
    else: comp=''
    L.append(f"| {r.Label} | {z} | {zs} | {'' if pd.isna(r.Builtup_km2) else int(r.Builtup_km2)} | {cs} | {comp} |")
S2='\n'.join(L).replace('–','-').replace('—',', ')
def f(d): return 'n/a' if d['rho'] is None else f"ρ = {d['rho']}, n = {d['n']}, p = {d['p']}"
C,Lz=R['CC'],R['LEZ']
sens=f"""| Analysis | Congestion charges (traffic) | Low emission zones (NO₂) |
|---|---|---|
| Relative coverage, all (main) | {f(C['coverage_all'])} | {f(Lz['coverage_all'])} |
| Absolute area (km²), all | {f(C['km2_all'])} | {f(Lz['km2_all'])} |
| Relative coverage, journal evidence only | {f(C['coverage_journal_only'])} | {f(Lz['coverage_journal_only'])} |
| Absolute area, journal evidence only | {f(C['km2_journal_only'])} | |
| Relative coverage, control or natural experiment only | {f(C['coverage_counterfactual_only'])} | {f(Lz['coverage_counterfactual_only'])} |
| Relative coverage, control or adjusted designs | {f(C['coverage_tier12'])} | {f(Lz['coverage_tier12'])} |
| Relative coverage, excluding Durham | {f(C['coverage_excl_durham'])} | |
| Absolute area, excluding Durham | {f(C['km2_excl_durham'])} | |
| Absolute area, excluding Durham and Singapore | {f(C['km2_excl_durham_singapore'])} | |
| Relative coverage, LEZs covering private cars | | {f(Lz['cars_covered']['coverage_vs_effect'])} |
| Relative coverage, LEZs covering cars, control only | | {f(Lz['coverage_cars_counterfactual'])} |
| Relative coverage, excluding four estimates reported only as not significant and charted as zero | | {f(Lz['coverage_excl_ns_zero'])} |
| Relative coverage, excluding the 2023 ULEZ expansion | | {f(Lz['coverage_excl_london_2023'])} |
| Lisbon Zone 2 effect (−22%) with Zone 2 area (25.14 km²) | | {f(Lz['coverage_lisbon_zone2'])} |
| As above, LEZs covering cars | | {f(Lz['coverage_lisbon_zone2_cars'])} |
| Charge relative to income vs effect | {f(C['charge_to_income_vs_effect'])} | |
| Charge relative to income vs coverage | {f(C['charge_to_income_vs_coverage'])} | |
| Compliance at launch vs effect | | {f(Lz['compliance_vs_effect'])} |
| Compliance at launch vs coverage | | {f(Lz['compliance_vs_coverage'])} |
| Start year vs coverage | | {f(Lz['start_year_vs_coverage'])} |"""
terc='\n'.join(['| Tercile | n | Median effect (%) | Coverage range (%) | Schemes |','|---|---|---|---|---|']+[f"| {k} | {v['n']} | {v['median_effect']} | {v['coverage_pct_range'][0]} to {v['coverage_pct_range'][1]} | {', '.join(v['schemes'])} |" for k,v in Lz['by_tercile'].items()])
pers='\n'.join(['| Scheme | First (years, effect %) | Last (years, effect %) | Ratio |','|---|---|---|---|']+[f"| {p['Label']} | {p['first_years']}, {p['first']} | {p['last_years']}, {p['last']} | {p['ratio']} |" for p in R['persistence']])
pooled='\n'.join(['| Estimate | Outcome | Effect (%) | Years | Design |','|---|---|---|---|---|']+[f"| {p['Scheme']} | {p['Outcome']} | {p['Effect_pct']} | {p['Years_in_operation_at_measurement']} | {p['Design']} |" for p in R['pooled']])
SC=R['size_categories']
L=['| Type | Size category | n | Median (%) | Median without zeros (%) | Control | Schemes (effect %) |','|---|---|---|---|---|---|---|']
for typ,lab in [('CC','Charge (traffic)'),('LEZ','LEZ (NO₂)')]:
    for k,v in SC[typ].items():
        k2=k.replace('-',' to ')
        mz='' if v['median_excl_ns_zero'] is None else f"{v['median_excl_ns_zero']:.1f}".replace('-','−')
        L.append(f"| {lab} | {k2} | {v['n']} | {v['median']:.1f}".replace('-','−')+f" | {mz} | {v['n_control']} | {', '.join(s.replace('-','−') for s in v['schemes'])} |")
sizecat='\n'.join(L)
wc=pd.read_csv(f'{CUR}/within_city.csv'); wc=wc[~wc.Change_type.str.startswith('Zone enlarged')]
L=['| Change type | City | Change (year) | Outcome | Effect (%) | Earlier effect (%) | Design | Source |','|---|---|---|---|---|---|---|---|']
for _,r in wc.iterrows():
    eff=('0 (not significant)' if r.Not_significant=='Y' and r.Effect_pct==0 else f"{r.Effect_pct:+.1f}".replace('-','−')+(' (not significant)' if r.Not_significant=='Y' else ''))
    be='' if pd.isna(r.Before_effect_pct) else f"{r.Before_effect_pct:+.1f}".replace('-','−')+f" ({r.Before_label})"
    doi='' if r.DOI=='NO-DOI' else f", doi:{r.DOI}"
    L.append(f"| {r.Change_type} | {r.City} | {r.Change} ({r.Year}) | {r.Outcome} | {eff} | {be} | {r.Design} | {r.Source}{doi}. {r.Note} |")
within='\n'.join(L).replace('–','-').replace('—',', ')
bp=pd.read_csv(f'{CUR}/boundary_pairs.csv')
L=['| City and scheme | Outcome | Zone | Year | Area (km²) | Effect (%) | Design | Measured | Source | Note |','|---|---|---|---|---|---|---|---|---|---|']
for _,r in bp.iterrows():
    eff='0 (not significant)' if r.Not_significant=='Y' else f"{r.Effect_pct:+.1f}".replace('-','−')
    L.append(f"| {r.City} {r.Scheme.lower() if r.Scheme[0].islower() else r.Scheme} | {r.Outcome.replace('NO2','NO₂')} | {r.Step_label} | {r.Year} | {r.Zone_km2:,.4g} | {eff} | {r.Design} | {r.Measured_where} | {r.Source}, doi:{r.DOI} | {r.Note} |")
pairs='\n'.join(L)
cfiles=[EXTRACT / f for f in ('current_charges_cc.csv','current_charges_lez.csv') if (EXTRACT / f).exists()]
cur=pd.concat([pd.read_csv(f) for f in cfiles]) if cfiles else pd.DataFrame()
lab=dict(zip(pd.read_csv(f'{A}/analysis_dataset.csv').Key, pd.read_csv(f'{A}/analysis_dataset.csv').Label))
L=['| Scheme | Status | Current charge | Effective from | Source |','|---|---|---|---|---|']
for _,r in cur.iterrows():
    s=lambda v: '' if pd.isna(v) else str(v)
    L.append(f"| {lab.get(r.Key, r.Key)} | {s(r.Status_2026)} | {s(r.Current_charge)} | {s(r.Effective_from)} | {s(r.Source_title)} ({s(r.Source_type)}), {s(r.Source_URL)} |")
current='\n'.join(L)
si=open(TEMPLATES / 'si_template.md').read()
for k,v in dict(S1=S1,S2=S2,sens=sens,terc=terc,pers=pers,pooled=pooled,sizecat=sizecat,within=within,pairs=pairs,current=current,city=(TABLES / 'cc_city_evidence.md').read_text().strip(),lezcity=(TABLES / 'lez_city_evidence.md').read_text().strip()).items(): si=si.replace(f'@{k}@',v)
si=si.replace('Attard and Ison (2010, 2015); Attard (2013) (peer-reviewed)','Attard and Ison (2010, peer-reviewed); Attard (2013, conference paper)').replace(' ;',';').replace('Tretvik (2007) (peer-reviewed)','Tretvik (2007, conference paper)')
open(MANUSCRIPT / 'supplementary.md','w').write(si); print(len(si.split()))
si=open(MANUSCRIPT / 'supplementary.md').read()
si=si.replace('Durham is not a UCDB urban centre; its denominator is','Durham is not a UCDB urban centre, so its denominator is')
si=si.replace('(London ULEZ central 2019 and London-wide 2023; the inner London step of 2021 has no peer-reviewed estimate)','(London ULEZ central 2019 and London-wide 2023, with no peer-reviewed estimate for the inner London step of 2021)')
si=si.replace('95% CI -12.7 to 7.4 ug/m3','95% CI −12.7 to 7.4 µg/m³').replace('; ',', ').replace(';',',')
open(MANUSCRIPT / 'supplementary.md','w').write(si)
