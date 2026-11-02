import pandas as pd, openpyxl, re
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment

wb=openpyxl.load_workbook('Boundary_Size_Database_v2.xlsx')
z=wb['Zone_schemes']; F='Arial'; base=Font(name=F); blue=Font(name=F,color='0000FF')
hdr_font=Font(name=F,bold=True,color='FFFFFF'); hdr_fill=PatternFill('solid',fgColor='305496')
cols=[c.value for c in z[1]]; ci={h:i+1 for i,h in enumerate(cols)}
EZ='Emission-based zone (LEZ/CAZ/ZEZ)'; CC='Congestion charge (cordon/area)'

# --- 1. add inventory rows discovered by extraction
last=z.max_row
new=[
('London (LEZ heavy vehicles)','United Kingdom',EZ,'Low Emission Zone for heavy vehicles',2008,'Phase 2 Jan 2012 added LGVs','Almost all of Greater London',1572,'km2','Verify','Greater London area as proxy','Charging','Peer-reviewed evaluations exist (Ellison et al. 2013; Zhai and Wolff 2021)'),
('Lisbon','Portugal',EZ,'Low Emission Zone (two zones)',2011,'Phase 2 Apr 2012, phase 3 Jan 2015','Zone 1 city centre, Zone 2 wider area',None,'','GIS needed','','Penalty-based','Added by extraction'),
('Antwerp','Belgium',EZ,'Low Emission Zone',2017,'','City centre and Linkeroever',None,'','GIS needed','','Penalty-based','Added by extraction'),
('Brussels','Belgium',EZ,'Low Emission Zone (regional)',2018,'Tightened yearly','Whole Brussels-Capital Region',161,'km2','Verify','Region area from extraction note','Penalty-based','Added by extraction'),
]
for k,row in enumerate(new):
    i=last+1+k
    city,ctry,fam,pt,yr,yn,zd,av,u,st,an,ch,fl=row
    vals={'ID':i-1,'Origin':'Added by extraction 2026-11-01','City':city,'Country':ctry,'Policy_family':fam,'Policy_type_recorded':pt,'Year_introduced':yr,'Year_note':yn,'Zone_description':zd,'Area_value':av,'Area_unit':u,'Area_status':st,'Area_note':an,'Charging_mode':ch,'Data_quality_flag':fl}
    for h,v in vals.items():
        c=z.cell(i,ci[h],v if v!='' else None); c.font=base; c.alignment=Alignment(wrap_text=True,vertical='top')
    z.cell(i,ci['Area_value']).font=blue
    z.cell(i,ci['Area_km2'],f'=IF(K{i}="","",IF(L{i}="sq mi",K{i}*2.58999,K{i}))').number_format='0.00'
    z.cell(i,ci['Relative_coverage'],f'=IF(OR(M{i}="",V{i}=""),"",M{i}/V{i})').number_format='0.000'
    ef=get_column_letter(ci['Effect_pct']); el=get_column_letter(ci['Effect_later_pct'])
    z.cell(i,ci['Persistence_ratio'],f'=IF(OR({ef}{i}="",{el}{i}="",{ef}{i}=0),"",{el}{i}/{ef}{i})').number_format='0.00'
    yellow=PatternFill('solid',fgColor='FFFF00')
    for j in range(22,len(cols)+1):
        if j not in (ci['Relative_coverage'],ci['Persistence_ratio']): z.cell(i,j).fill=yellow
z.auto_filter.ref=f'A1:{get_column_letter(len(cols))}{z.max_row}'

# scheme lookup
inv={}
for r in range(2,z.max_row+1):
    inv[r]=(z.cell(r,ci['ID']).value, str(z.cell(r,ci['City']).value), str(z.cell(r,ci['Policy_type_recorded']).value), str(z.cell(r,ci['Year_introduced']).value))
def find(pred):
    for r,(id_,city,pt,yr) in inv.items():
        if pred(city,pt,yr): return id_
    return None
def match(city,scheme):
    s=scheme.lower(); c=city.lower()
    if c=='london':
        if 'ulez' in s: return find(lambda ci_,pt,yr: ci_.strip()=='London' and 'Ultra' in pt)
        if 'lez for heavy' in s: return find(lambda ci_,pt,yr: 'LEZ heavy' in ci_)
        if 'western' in s: return find(lambda ci_,pt,yr: 'Western' in ci_)
        return find(lambda ci_,pt,yr: ci_.strip()=='London' and pt=='Congestion Charge')
    if c=='milan':
        if 'ecopass' in s: return find(lambda ci_,pt,yr: 'Ecopass' in ci_)
        if 'area b' in s: return find(lambda ci_,pt,yr: 'Area B' in ci_)
        return find(lambda ci_,pt,yr: 'Area C' in ci_)
    if c=='singapore': return find(lambda ci_,pt,yr: 'ALS' in ci_)
    if c=='amsterdam': return find(lambda ci_,pt,yr: ci_.strip()=='Amsterdam' and yr.startswith('2009'))
    if c=='madrid': return find(lambda ci_,pt,yr: ci_.strip()=='Madrid')
    if c=='rome': return find(lambda ci_,pt,yr: ci_.strip()=='Rome')
    return find(lambda ci_,pt,yr: ci_.strip().lower()==c)

# --- 2. Effects sheet
cc=pd.read_csv('extract/cc_effects.csv'); cc['Extraction_batch']='Congestion charges (agent, 2026-11-01)'
lez=pd.read_csv('extract/lez_effects.csv'); lez['Extraction_batch']='Emission zones (agent, 2026-11-01)'
e=pd.concat([cc,lez],ignore_index=True)
e['Scheme_ID']=[match(c,s) for c,s in zip(e.City,e.Scheme)]
flagwords=['verify','provisional','secondary summary','own calculation','placeholder','not accessible','full text not','not opened','could not be verified','working paper version','grey']
e['Needs_manual_check']=['Y' if any(w in str(n).lower() for w in flagwords) else 'N' for n in e.Extractor_notes]
e['Counterfactual']=['Y' if d in ('DiD','Synthetic control','RDD','Interrupted time series') else 'N' for d in e.Design]
e.insert(0,'Effect_ID',range(1,len(e)+1))
order=['Effect_ID','Scheme_ID','City','Scheme','Extraction_batch','Outcome_family','Outcome_metric','Effect_pct','Measured_where','Years_in_operation_at_measurement','Design','Counterfactual','Spillover_reported','Spillover_effect_pct','Peer_reviewed_citation','DOI','Stringency_note','Extractor_notes','Needs_manual_check']
e=e[order]
if 'Effects' in wb.sheetnames: del wb['Effects']
es=wb.create_sheet('Effects',2)
for j,h in enumerate(order,1):
    c=es.cell(1,j,h); c.font=hdr_font; c.fill=hdr_fill; c.alignment=Alignment(wrap_text=True,vertical='center')
red=Font(name=F,color='C00000')
for i,row in enumerate(e.itertuples(index=False),2):
    for j,v in enumerate(row,1):
        if isinstance(v,float) and pd.isna(v): v=None
        c=es.cell(i,j,v); c.font=base; c.alignment=Alignment(wrap_text=True,vertical='top')
    if row.Needs_manual_check=='Y': es.cell(i,len(order)).font=red
    if pd.isna(row.Scheme_ID): es.cell(i,2).value='pooled / multi-city'
n=len(e)+1
es.freeze_panes='D2'; es.auto_filter.ref=f'A1:{get_column_letter(len(order))}{n}'
for k,v in {'A':7,'B':9,'C':14,'D':34,'E':16,'F':11,'G':40,'H':9,'I':14,'J':10,'K':16,'L':8,'M':8,'N':9,'O':50,'P':26,'Q':45,'R':60,'S':10}.items(): es.column_dimensions[k].width=v
es.cell(1,2).comment=Comment('ID in Zone_schemes. "pooled / multi-city" rows (German LEZ panels, Dutch five-city study) have no single inventory scheme.','Claude')
es.cell(1,19).comment=Comment('Y = the extracting agent flagged this value as taken from a secondary summary, a working-paper version, an own percentage calculation, or otherwise unverified in the full text. Check against the PDF before use.','Claude')
es.cell(1,12).comment=Comment('Y when Design is DiD, Synthetic control, RDD or Interrupted time series. Before-after and Model-based rows have no untreated control.','Claude')

# --- 3. Summary: effects counts
sm=wb['Summary']
sm.cell(3,7).value='Effect rows (Effects sheet)'; sm.cell(3,8,'Effect rows with counterfactual').font=hdr_font; sm.cell(3,8).fill=hdr_fill; sm.cell(3,8).alignment=Alignment(wrap_text=True)
sm.cell(3,9,'Schemes with at least one effect row').font=hdr_font; sm.cell(3,9).fill=hdr_fill; sm.cell(3,9).alignment=Alignment(wrap_text=True)
for i,fam in enumerate([CC,EZ,'Access restriction (non-price)'],4):
    sm.cell(i,7,f'=SUMPRODUCT((Zone_schemes!$F$2:$F$500=A{i})*COUNTIF(Effects!$B$2:$B$500,Zone_schemes!$A$2:$A$500))')
    sm.cell(i,8,f'=SUMPRODUCT((Zone_schemes!$F$2:$F$500=A{i})*COUNTIFS(Effects!$B$2:$B$500,Zone_schemes!$A$2:$A$500,Effects!$L$2:$L$500,"Y"))')
    sm.cell(i,9,f'=SUMPRODUCT((Zone_schemes!$F$2:$F$500=A{i})*(COUNTIF(Effects!$B$2:$B$500,Zone_schemes!$A$2:$A$500)>0))')
    for j in (7,8,9): sm.cell(i,j).font=base
for j in (7,8,9):
    L=get_column_letter(j); sm.cell(7,j,f'=SUM({L}4:{L}6)').font=Font(name=F,bold=True)
sm.cell(15,1,'Effect rows total'); sm.cell(15,2,'=COUNTA(Effects!$A$2:$A$500)')
sm.cell(16,1,'Effect rows not matched to a single scheme (pooled / multi-city)'); sm.cell(16,2,'=COUNTIF(Effects!$B$2:$B$500,"pooled / multi-city")')
sm.cell(17,1,'Effect rows flagged Needs_manual_check'); sm.cell(17,2,'=COUNTIF(Effects!$S$2:$S$500,"Y")')
for r in (15,16,17):
    for j in (1,2): sm.cell(r,j).font=base
sm.column_dimensions['H'].width=14; sm.column_dimensions['I'].width=14

# --- 4. README additions
rd=wb['README']; r0=rd.max_row+2
lines=[('Version 3 (1 Nov 2026): effect-size extraction',True),
('New sheet "Effects": one row per scheme-measurement from peer-reviewed ex-post evaluations, extracted by two research agents (congestion charges; emission zones). All DOIs were checked against Crossref on 1 Nov 2026. Scheme_ID links to Zone_schemes; pooled multi-city panels have no single scheme.',False),
('Needs_manual_check = Y marks values the extracting agent took from a secondary summary, a working-paper version or an own percentage calculation. Check these against the article PDF before analysis. Counterfactual = Y marks designs with an untreated control.',False),
('Four inventory rows added at the end of Zone_schemes because evaluations exist: London LEZ for heavy vehicles (2008), Lisbon, Antwerp, Brussels.',False),
('Known issues to resolve by hand: (1) London Western Extension estimates conflict (Ouali et al. 2021 DiD -5% vs Ding et al. 2022 RDD -31%). (2) Milan Area C figures from Gibson and Carnovale (2015) and Beria (2016) are from secondary summaries. (3) Antwerp and Brussels NO2 values are crude differences from an author summary. (4) Stockholm years in operation count from Jan 2006 although charging was off Aug 2006 to Jul 2007. (5) Rows for charge increases (Stockholm 2016, Milan 2023) are marginal effects, not scheme effects. (6) Positive Effect_pct for WEZ and Trondheim removal rows means traffic rose after removal.',False),
('The orange extraction columns in Zone_schemes are now superseded by the Effects sheet and can be left blank.',False)]
for k,(t,b) in enumerate(lines):
    c=rd.cell(r0+k,1,t); c.font=Font(name=F,bold=b); c.alignment=Alignment(wrap_text=True,vertical='top')
rd['A1'].value='Boundary size database: working version 3'
wb.save('Boundary_Size_Database_v3.xlsx')
print(len(e),'effect rows;', (e.Scheme_ID.isna()).sum(),'unmatched;', (e.Needs_manual_check=='Y').sum(),'flagged')
print(e[e.Scheme_ID.isna()].City.unique())
