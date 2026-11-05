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
        s=short(r.Peer_reviewed_citation)
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
    L.append(f"| {r.Change_type} | {r.City} | {r.Change} ({r.Year}) | {r.Outcome} | {eff} | {be} | {r.Design} | {r.Source}. {r.Note} |")
within='\n'.join(L).replace('–','-').replace('—',', ')
bp=pd.read_csv(f'{CUR}/boundary_pairs.csv')
L=['| City and scheme | Outcome | Zone | Year | Area (km²) | Effect (%) | Design | Measured | Source | Note |','|---|---|---|---|---|---|---|---|---|---|']
for _,r in bp.iterrows():
    eff='0 (not significant)' if r.Not_significant=='Y' else f"{r.Effect_pct:+.1f}".replace('-','−')
    L.append(f"| {r.City} {r.Scheme.lower() if r.Scheme[0].islower() else r.Scheme} | {r.Outcome.replace('NO2','NO₂')} | {r.Step_label} | {r.Year} | {r.Zone_km2:,.4g} | {eff} | {r.Design} | {r.Measured_where} | {r.Source} | {r.Note} |")
pairs='\n'.join(L)
cfiles=[EXTRACT / f for f in ('current_charges_cc.csv','current_charges_lez.csv') if (EXTRACT / f).exists()]
cur=pd.concat([pd.read_csv(f) for f in cfiles]) if cfiles else pd.DataFrame()
lab=dict(zip(pd.read_csv(f'{A}/analysis_dataset.csv').Key, pd.read_csv(f'{A}/analysis_dataset.csv').Label))
L=['| Scheme | Status | Current charge | Effective from | Source |','|---|---|---|---|---|']
for _,r in cur.iterrows():
    s=lambda v: '' if pd.isna(v) else str(v)
    L.append(f"| {lab.get(r.Key, r.Key)} | {s(r.Status_2026)} | {s(r.Current_charge)} | {s(r.Effective_from)} | {s(r.Source_title)} ({s(r.Source_type)}), {s(r.Source_URL)} |")
current='\n'.join(L)
# Table S8: inside and outside pairs (Figure 3) and the rows not used
spr=pd.read_csv(f'{A}/spillover_rows.csv'); spp=pd.read_csv(f'{A}/spillover_pairs.csv')
m=lambda v: ('0.0' if abs(v)<0.05 else f"{v:+.1f}".replace('-','−'))
L=['| Scheme phase | Outcome | Inside (%) | Outside (%) | Outside estimate refers to | Design | Years | Source(s) | Rows |','|---|---|---|---|---|---|---|---|---|']
for _,r in spp.iterrows():
    rid=r.Rows_used.replace(';',', ')
    L.append(f"| {r.Label} | {r.Outcome.replace('NO2','NO₂')} | {m(r.Inside_pct)} | {m(r.Outside_pct)} | {r.Outside_type.lower()} | {tiers[int(r.Design_tier)]} | {r.Years} | {cite(r.Rows_used)} | {rid} |")
L+=['','Where the outside estimate was taken, by row:','']
for _,r in spr[spr.Use=='Y'].sort_values('Row').iterrows():
    L.append(f"- Row {r.Row} ({lab.get(r.Phase_key,'German LEZs (pooled)')}): {r.Outside_location}. {r.Note}.")
L+=['','Rows listed but not used:','','| Row | Scheme phase | Inside (%) | Outside (%) | Reason |','|---|---|---|---|---|']
for _,r in spr[spr.Use=='N'].iterrows():
    L.append(f"| {r.Row} | {lab.get(r.Phase_key, r.Phase_key)} | {m(r.Effect_pct)} | {m(r.Spillover_effect_pct)} | {r.Note} |")
spill='\n'.join(L)
# References: full citation for every DOI whose (surname, year) is cited in the SI text or used in Tables S1, S4, S5, S7, S8
def longest(g):
    c=max(g.Peer_reviewed_citation, key=len); return c
bydoi={d: longest(g) for d,g in rows[rows.DOI!='NO-DOI'].groupby('DOI')}
HAND=[
 "Chamberlain, R. C., Fecht, D., Davies, B., & Laverty, A. A. (2023). Health effects of low emission and congestion charging zones: A systematic review. *The Lancet Public Health*, 8(7), e559-e574. https://doi.org/10.1016/S2468-2667(23)00120-2",
 "Holman, C., Harrison, R., & Querol, X. (2015). Review of the efficacy of low emission zones to improve urban air quality in European cities. *Atmospheric Environment*, 111, 161-169. https://doi.org/10.1016/j.atmosenv.2015.04.009",
 "Attard, M. (2013). Understanding the performance of the first five years of the Valletta road pricing scheme. Paper presented at the 13th World Conference on Transport Research (WCTR), Rio de Janeiro, July 2013.",
 "Delgado-Lindeman, M., Cordera, R., Moura, J. L., & Rodriguez, A. (2025). Characteristics and effects of low emission zones in Europe. A systematic literature review. *European Transport Research Review*, 17, 54. https://doi.org/10.1186/s12544-025-00749-2",
 "European Commission, Joint Research Centre. (2024). *GHS Urban Centre Database 2025 (GHS-UCDB R2024A, version 1.2)* [Data set]. Global Human Settlement Layer.",
 "Fensterer, V., Küchenhoff, H., Maier, V., Wichmann, H.-E., Breitner, S., Peters, A., Gu, J., & Cyrys, J. (2014). Evaluation of the impact of low emission zone and heavy traffic ban in Munich (Germany) on the reduction of PM10 in ambient air. *International Journal of Environmental Research and Public Health*, 11(5), 5094-5112. https://doi.org/10.3390/ijerph110505094",
 "Fan, H. S. L. (1995). Car ownership demand and traffic congestion in Singapore's restricted zone. *Journal of the Eastern Asia Society for Transportation Studies*, 1(2), 603-611.",
 "Garritty, C., Gartlehner, G., Nussbaumer-Streit, B., King, V. J., Hamel, C., Kamel, C., Affengruber, L., & Stevens, A. (2021). Cochrane Rapid Reviews Methods Group offers evidence-informed guidance to conduct rapid reviews. *Journal of Clinical Epidemiology*, 130, 13-22. https://doi.org/10.1016/j.jclinepi.2020.10.007",
 "May, A. D., Koh, A., Blackledge, D., & Fioretto, M. (2010). Overcoming the barriers to implementing urban road user charging schemes. *European Transport Research Review*, 2(1), 53-68. https://doi.org/10.1007/s12544-010-0026-1",
 "Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., et al. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. *BMJ*, 372, n71. https://doi.org/10.1136/bmj.n71",
 "Stevens, A., Hersi, M., Garritty, C., Hartling, L., Shea, B. J., Stewart, L. A., Welch, V. A., & Tricco, A. C. (2025). Rapid review method series: Interim guidance for the reporting of rapid reviews. *BMJ Evidence-Based Medicine*, 30(2), 118-123. https://doi.org/10.1136/bmjebm-2024-112899",
 "Tretvik, T. (2007). End of 15 years of urban road user charging in Trondheim, Norway: What now? Paper presented at the 11th World Conference on Transport Research, Berkeley.",
]
def fmt(c, doi):
    c=c.replace('Ouali, L. A. B.','Ait Bihi Ouali, L.')
    mm=re.match(r'^(.*?\(\d{4}[a-z]?\)\.\s*)(.*?)([.?!]\s+)([^.]*?)(,\s*\d.*)$', c)
    if mm: c=f"{mm.group(1)}{mm.group(2)}{mm.group(3)}*{mm.group(4)}*{mm.group(5)}"
    c=c.rstrip('.')+'.'
    return c+('' if doi in ('NO-DOI','nan','') else f' https://doi.org/{doi}')
def cited(text, c):
    sname=short(c); su=sname.split(' (')[0].split(' and ')[0].split(' et al')[0]; y=re.search(r'\((\d{4})',c)
    if not y: return False
    return re.search(re.escape(su)+r'[^;]{0,40}\('+y.group(1), text) is not None
# Table S6: German LEZs lifted 2020 to 2025
gr=pd.read_csv(f'{CUR}/german_lez_removals.csv')
L=['| Zone (state) | Introduced | Lifted | Years | Basis stated by the authority | Source |','|---|---|---|---|---|---|']
for _,r in gr.iterrows():
    L.append(f"| {r.Zone} ({r.State}) | {r.Introduced} | {r.Lifted} | {r.Years:.1f} | {r.Basis} | {r.Source} |")
removals='\n'.join(L); removals_median=f"{gr.Years.median():.1f}"
si=open(TEMPLATES / 'si_template.md').read()
for k,v in dict(S1=S1,S2=S2,sens=sens,terc=terc,pers=pers,pooled=pooled,spill=spill,removals=removals,removals_median=removals_median,sizecat=sizecat,within=within,pairs=pairs,current=current,city=(TABLES / 'cc_city_evidence.md').read_text().strip(),lezcity=(TABLES / 'lez_city_evidence.md').read_text().strip()).items(): si=si.replace(f'@{k}@',v)
# text used to decide which references are cited: everything except Tables S13, S14 and the references block
probe=re.split(r'# Table S13',si)[0]
used=set()
for col in ('Rows_used',):
    pass
for d,c in bydoi.items():
    if cited(probe,c): used.add(d)
for _,r in rows[rows.Row.isin(sum([[int(x) for x in str(v).split(';')] for v in list(ds.Rows_used)+list(spp.Rows_used)],[]))].iterrows():
    if r.DOI!='NO-DOI': used.add(r.DOI)
reflist=[fmt(bydoi[d],d) for d in used]+HAND
import unicodedata
reflist=sorted(set(reflist), key=lambda x: unicodedata.normalize('NFKD', x).encode('ascii','ignore').decode().lower())
si=si.replace('@refs@','\n\n'.join(reflist))
si=si.replace('Attard and Ison (2010, 2015); Attard (2013) (peer-reviewed)','Attard and Ison (2010, peer-reviewed); Attard (2013, conference paper)').replace(' ;',';').replace('Tretvik (2007) (peer-reviewed)','Tretvik (2007, conference paper)')
open(MANUSCRIPT / 'supplementary.md','w').write(si); print(len(si.split()))
si=open(MANUSCRIPT / 'supplementary.md').read()
si=si.replace('Durham is not a UCDB urban centre; its denominator is','Durham is not a UCDB urban centre, so its denominator is')
si=si.replace('(London ULEZ central 2019 and London-wide 2023; the inner London step of 2021 has no peer-reviewed estimate)','(London ULEZ central 2019 and London-wide 2023, with no peer-reviewed estimate for the inner London step of 2021)')
si=si.replace('95% CI -12.7 to 7.4 ug/m3','95% CI −12.7 to 7.4 µg/m³').replace('; ',', ').replace(';',',')
open(MANUSCRIPT / 'supplementary.md','w').write(si)
si=re.sub(r'\| -(\d)', r'| −\1', si); si=si.replace('| +0.0 |','| 0.0 |').replace('| +0.0 (','| 0.0 (')
open(MANUSCRIPT / 'supplementary.md','w').write(si)

def width_hints(md):
    out=[]; block=[]
    def flush():
        if len(block)>=2 and re.match(r'^\|[\s:|-]+\|$', block[1]):
            cells=[[c.strip() for c in ln.strip().strip('|').split('|')] for ln in block]
            n=max(len(c) for c in cells)
            w=[max(min(len(c[i]) if i<len(c) else 0, 34) for j,c in enumerate(cells) if j!=1) for i in range(n)]
            hdr=[len(c) for c in cells[0]]+[0]*n
            w=[max(x, 12, hdr[i]+3) for i,x in enumerate(w)]; tot=sum(w)
            block[1]='|'+'|'.join('-'*max(3,int(round(x/tot*160))) for x in w)+'|'
        out.extend(block); block.clear()
    for ln in md.split('\n'):
        if ln.startswith('|'): block.append(ln)
        else: flush(); out.append(ln)
    flush(); return '\n'.join(out)
si=width_hints(si)
open(MANUSCRIPT / 'supplementary.md','w').write(si)
