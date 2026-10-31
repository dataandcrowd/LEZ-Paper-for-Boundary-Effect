import pandas as pd, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment

src='/mnt/user-data/uploads/3038f38c-Congestion_Charging_Database_-_Rose.xlsx'
d=pd.read_excel(src).dropna(how='all')
def s(v):
    return '' if pd.isna(v) else str(v).strip()

CC='Congestion charge (cordon/area)'; EZ='Emission-based zone (LEZ/CAZ/ZEZ)'; AR='Access restriction (non-price)'
# idx: (family, year, year_note, area_value, unit, status, area_note, charging, flag)
inc={
0:(CC,2003,'',21,'km2','Reported','Original central zone; Western Extension 2007-2010 listed separately','Charging',''),
1:(EZ,2019,'Expanded Oct 2021 (North/South Circular) and Aug 2023 (all boroughs)',1572,'km2','Verify','Value is Greater London area as proxy for 2023 boundary; outer boundary excludes M25. Each expansion is a separate size step','Charging','Three boundary sizes over time: code each phase as its own row if effects are extracted by phase'),
2:(EZ,2024,'Enforcement start',None,'','GIS needed','','Penalty-based',''),
3:(EZ,2021,'',1.2,'sq mi','Reported','','Charging','Class C (no private cars)'),
4:(EZ,2021,'',3,'sq mi','Reported','','Charging','Class D (includes private cars)'),
5:(EZ,2022,'',9.35,'sq mi','Reported','','Charging','Class C+ (no private cars)'),
6:(EZ,2022,'',None,'','GIS needed','','Charging','Class D'),
7:(EZ,2022,'Grace period to Jun 2024',1.2,'sq mi','Reported','','Penalty-based','Policy type recorded as "Charging Clean Air Zone" but Edinburgh is a Scottish LEZ (penalty-based). Corrected family'),
9:(EZ,2022,'Grace period to May 2024',None,'','GIS needed','','Penalty-based',''),
10:(EZ,2022,'Year in DB; enforcement start to verify',0.94,'sq mi','Reported','','Charging',''),
12:(EZ,2021,'',1.1,'sq mi','Reported','','Charging','Class B (no private cars)'),
13:(EZ,2023,'',0.9,'sq mi','Reported','','Charging','Class C (no private cars)'),
15:(EZ,2020,'',None,'','GIS needed','','Non-charging','Bus-only CAZ; consider excluding from car-traffic outcomes'),
16:(EZ,2022,'Pilot zone',None,'','GIS needed','Pilot covers a handful of streets','Charging','Very small pilot; useful low-end size anchor'),
17:(EZ,2018,'Phase 1 buses 2018; all vehicles enforced Jun 2023',None,'','GIS needed','','Penalty-based','Two phases with different vehicle scope'),
19:(EZ,2018,'',26,'km2','Verify','Freight-only zone','Non-charging','Freight-only; outcome not comparable with car-traffic zones'),
21:(CC,2012,'Successor to Ecopass (2008) on the same boundary',8.2,'km2','Reported','4.5% of municipal area','Charging','Same boundary as Ecopass, different pricing: useful contrast'),
22:(EZ,2019,'',128.29,'km2','Reported','72% of municipal area','Penalty-based','Nested with Area C: two sizes in one city'),
23:(EZ,2020,'',95,'km2','Verify','ZBE Rondes area spans several municipalities; confirm figure','Penalty-based',''),
24:(EZ,2018,'Madrid Central 2018; city-wide ZBE 2021-22',574,'km2','Verify','Figure appears to be the city-wide ZBE, not Madrid Central (2018, c. 4.7 km2). Split into two rows when extracting','Penalty-based','Year and area refer to different schemes'),
25:(EZ,2016,'Progressive tightening 2021-2025',105,'km2','Verify','105 km2 is the area of the City of Paris, but description refers to the Metropole du Grand Paris ZFE-m (inside A86). Check which boundary','Penalty-based','Area and description inconsistent'),
26:(EZ,2009,'',None,'','GIS needed','Inside A10 ring','Penalty-based',''),
27:(EZ,2025,'',None,'','GIS needed','Inside A10 ring; DB city name misspelt "Amterdam"','Penalty-based','Zero-emission zone for vans and trucks; check vehicle scope'),
28:(EZ,2025,'',13,'km2','Reported','','Penalty-based','Zero-emission freight zone'),
29:(EZ,2025,'LEZ older; ZEZ for vans/trucks 2025',None,'','GIS needed','','Penalty-based','Duplicate entry (DB row 45) removed'),
30:(EZ,2008,'',88,'km2','Reported','Inside S-Bahn ring','Penalty-based',''),
31:(EZ,2008,'',207,'km2','Verify','Whole municipality used as proxy','Penalty-based',''),
32:(EZ,2008,'Progressive tightening 2008-2012',44,'km2','Reported','14% of city area','Penalty-based',''),
34:(CC,1986,'DB gives 2012; toll ring dates from 1986, time-differentiated charges from 2016',None,'','GIS needed','','Charging','Year in DB likely wrong; originally a revenue toll ring'),
35:(CC,1991,'DB gives 2010; toll ring dates from 1991, restructured 2010',None,'','GIS needed','','Charging','Year in DB likely wrong'),
38:(CC,2025,'',11,'sq mi','Verify','Manhattan at or below 60th St excluding FDR Drive and West Side Highway; compute from MTA geofence polygon (data.ny.gov)','Charging',''),
41:(EZ,2017,'',None,'','Verify','DB description ("S-Bahn ring road, approx. 88 km2") is identical to Berlin and appears copied in error','Penalty-based','ERROR: zone description copied from Berlin'),
42:(EZ,2024,'',37,'km2','Reported','','Penalty-based',''),
45:(EZ,2021,'',0.14,'km2','Reported','Kota Tua area','Penalty-based','Very small; useful low-end size anchor'),
46:(AR,1989,'',None,'','GIS needed','Whole city plus 18 municipalities','Penalty-based','Licence-plate restriction, not a bounded zone in the same sense'),
47:(AR,None,'Year missing in DB (Pico y Placa from 1998)',307,'km2','Verify','','Penalty-based','Licence-plate restriction; year missing'),
48:(AR,1999,'',1,'sq mi','Verify','','Penalty-based',''),
49:(AR,1995,'',None,'','GIS needed','No zone description in DB','Penalty-based','Zone definition missing'),
64:(AR,2021,'',None,'','GIS needed','DB gives "520 m", a street length, not an area','Non-charging','Car-free street; length not area'),
}
exc={
8:'Single-street traffic management measure, no bounded charging or restriction zone',
11:'Non-charging package of measures, no bounded zone restriction',
14:'Local NO2 plan without a zone restriction',
18:'Point-based gantry charging (ERP), no single boundary; its predecessor ALS (1975 cordon) added instead',
20:'Point-based road tolls (Salik gates)',
33:'Linear expressway toll',36:'Linear motorway toll network',37:'Linear toll motorway',39:'Linear toll motorways',40:'Linear toll motorway',
43:'Duplicate of Utrecht (DB row 31)',44:'Linear expressway toll',50:'Linear tolled expressways',51:'Linear toll expressway',52:'Linear toll expressway',
53:'Linear toll motorway',54:'National linear toll network',55:'National linear toll network',56:'Linear toll concession',57:'Linear cross-border toll concession',
58:'National linear toll network',59:'Bridge and road tolls',60:'Linear toll motorway',61:'Bridge and expressway tolls',62:'Regional tolled bridges',63:'Toll plazas on national roads',
}
assert set(inc)|set(exc)==set(d.index) and not set(inc)&set(exc)

added=[
('Stockholm','Sweden',CC,'Congestion tax (cordon)',2006,'Trial Jan-Jul 2006, permanent Aug 2007; Essingeleden added 2016','Inner city cordon, 18 control points',None,'','Verify','Reported figures vary from 24 to 47 km2 across sources (c. 35 km2 in KTH CTS working paper). Compute from polygon','Charging','Core cordon case; key peer-reviewed evaluations exist'),
('Gothenburg','Sweden',CC,'Congestion tax (cordon)',2013,'','Most of the city centre plus some through routes; Backa exemption from 2018',None,'','GIS needed','','Charging','Core cordon case; larger zone than Stockholm'),
('Singapore (ALS)','Singapore',CC,'Area Licensing Scheme (cordon)',1975,'Replaced by ERP in 1998',"CBD 'Restricted Zone'",6,'km2','Verify','6 km2 at launch, later 7.25 km2; one source gives 5.59 km2','Charging','Historic anchor case'),
('Valletta','Malta',CC,'Controlled Vehicular Access (time-based charge)',2007,'Replaced V-licence',"Valletta peninsula",0.8,'km2','Reported','Attard and Ison (2010), Journal of Transport Geography 18, 14-22','Charging','Smallest charged zone with peer-reviewed evaluation'),
('Durham','United Kingdom',CC,'Road user charge (single street)',2002,'','Saddler Street, peninsula',None,'','GIS needed','To verify','Charging','Very small zone; check eligibility'),
('Oslo','Norway',CC,'Toll ring',1990,'Time-differentiated and environmental charges added later','Toll ring around central Oslo',None,'','GIS needed','To verify','Charging','Originally revenue-raising'),
('Milan (Ecopass)','Italy',CC,'Pollution charge (cordon)',2008,'Replaced by Area C in 2012','Cerchia dei Bastioni',8.2,'km2','Reported','Same boundary as Area C','Charging','Same boundary as Area C, emission-based pricing'),
('London (Western Extension)','United Kingdom',CC,'Congestion Charge extension',2007,'Removed Jan 2011','Western extension of central zone',None,'','GIS needed','Approximately doubled the charged area; to verify','Charging','Within-city size change (added then removed)'),
('Rome','Italy',AR,'Limited Traffic Zone (ZTL, permit-based)',2001,'Electronic enforcement from 2001','Historic centre',None,'','GIS needed','To verify','Permit-based','Permit-based access restriction'),
]

wb=openpyxl.Workbook()
F='Arial'
hdr_font=Font(name=F,bold=True,color='FFFFFF'); hdr_fill=PatternFill('solid',fgColor='305496')
ext_fill=PatternFill('solid',fgColor='C65911'); yellow=PatternFill('solid',fgColor='FFFF00')
red=Font(name=F,color='C00000'); base=Font(name=F); blue=Font(name=F,color='0000FF')
thin=Side(style='thin',color='BFBFBF')

# README
r=wb.active; r.title='README'
lines=[
('Boundary size database: working version',True),
('Research question: Does the size of a charged or restricted urban zone matter for its reported effect?',False),
('Target: Transport Findings (Findings Press). Prepared 31 Oct 2026 from "Congestion Charging Database - Rose.xlsx" (65 rows).',False),
('',False),
('Inclusion rule',True),
('Included: schemes with a bounded area that vehicles are charged or restricted for entering or circulating in (cordon/area congestion charges, LEZ, CAZ, ZEZ, area-wide access restrictions).',False),
('Excluded: linear motorway, expressway and bridge tolls; point-based gantry charging; plans or packages without a zone restriction; duplicates. See sheet "Excluded" for the reason per row.',False),
('',False),
('Sheets',True),
('Zone_schemes: one row per scheme. Blue columns are cleaned database fields. Orange columns are blank and are for effect-size extraction.',False),
('Excluded: rows removed from the original file and why.',False),
('Summary: counts by policy family and area status (formulas, update automatically).',False),
('',False),
('Legend',True),
('Area_value (blue text) is the figure as reported in the source. Area_km2 is a formula: sq mi x 2.58999, km2 unchanged. Do not type into Area_km2.',False),
('Area_status: Reported = figure given and plausible; Verify = figure given but suspect or inconsistent; GIS needed = no usable figure, compute from the official boundary polygon.',False),
('Red text in Data_quality_flag marks a likely error in the original file.',False),
('Orange columns (yellow cells) are to be filled from peer-reviewed ex-post evaluations only. One row per scheme and outcome; duplicate the row if a scheme has several outcomes or phases.',False),
('',False),
('Extraction fields (orange)',True),
('Outcome_family: Traffic (congestion charges) or Air quality (emission zones). Keep the two families separate in analysis.',False),
('Outcome_metric: e.g. vehicles crossing cordon, vehicle-km inside zone, NO2 annual mean at roadside monitors.',False),
('Effect_pct: percentage change, negative = reduction. Measured_where: Inside zone / Cordon crossing / Outside zone (spillover) / Network-wide.',False),
('Months_after_start: time between start and measurement. Design: Before-after / DiD / Synthetic control / RDD / Interrupted time series / Model-based.',False),
('',False),
('Example row (format only; numbers and DOI must be checked against the paper before use)',True),
('Gothenburg | Traffic | Vehicles crossing cordon, charged hours | -12 | Cordon crossing | 12 | Before-after | Y | | Borjesson and Kristoffersson (2015), Transportation Research Part A | [look up DOI] |',False),
('',False),
('Main changes from the original file',True),
('26 rows removed: 20 linear tolls, 2 point-based charges, 3 plans or packages without a zone restriction, 1 duplicate (Utrecht).',False),
('Areas standardised to km2 via formula; units recorded separately.',False),
('Errors flagged: Beijing zone description copied from Berlin; Edinburgh recorded as charging CAZ (it is a penalty-based LEZ); Paris area (105 km2 = City of Paris) inconsistent with Metropole description; Madrid year and area refer to different schemes; Bergen and Trondheim start years likely wrong.',False),
('Nine core cases added that were missing: Stockholm, Gothenburg, Singapore ALS, Valletta, Durham, Oslo, Milan Ecopass, London Western Extension, Rome ZTL. Fields for these are from quick checks and marked Verify or GIS needed where unconfirmed.',False),
('Within-city size contrasts worth noting: London central zone vs Western Extension (added 2007, removed 2011); Milan Area C (8.2 km2) nested inside Area B (128 km2); London ULEZ in three boundary steps; Milan Ecopass vs Area C (same boundary, different pricing).',False),
('Reported impacts from the original file are not carried over: almost all were goals rather than measured effects. They remain in the original file.',False),
]
for i,(t,b) in enumerate(lines,1):
    c=r.cell(i,1,t); c.font=Font(name=F,bold=b,size=13 if i==1 else 11); c.alignment=Alignment(wrap_text=True,vertical='top')
r.column_dimensions['A'].width=140

# Zone_schemes
z=wb.create_sheet('Zone_schemes')
cols=['ID','Origin','Rose_DB_row','City','Country','Policy_family','Policy_type_recorded','Year_introduced','Year_note',
'Zone_description','Area_value','Area_unit','Area_km2','Area_status','Area_note','Charging_mode','Vehicle_classes','Pricing_or_penalty','Operation_hours','Data_quality_flag','Original_source',
'Outcome_family','Outcome_metric','Effect_pct','Measured_where','Months_after_start','Design','Spillover_reported','Spillover_effect_pct','Peer_reviewed_citation','DOI','Extractor_notes']
NEXT=21
for j,h in enumerate(cols,1):
    c=z.cell(1,j,h); c.font=hdr_font; c.fill=ext_fill if j>NEXT else hdr_fill; c.alignment=Alignment(wrap_text=True,vertical='center')
rows=[]
for idx in sorted(inc):
    fam,yr,yn,av,u,st,an,ch,fl=inc[idx]; o=d.loc[idx]
    rows.append(['Rose DB',idx+2,s(o['City']),s(o['Country']),fam,s(o['Policy Type']),yr,yn,s(o['Zone Description']),av,u,st,an,ch,s(o['Vehicle Classes Affected']),s(o['Pricing/Restriction Type']),s(o['Operation Hours']),fl,s(o['Source/Reference'])])
for a in added:
    city,ctry,fam,pt,yr,yn,zd,av,u,st,an,ch,fl=a
    rows.append(['Added 2026-10-31','',city,ctry,fam,pt,yr,yn,zd,av,u,st,an,ch,'','','',fl,''])
famorder={CC:0,EZ:1,AR:2}
rows.sort(key=lambda x:(famorder[x[4]],x[2]))
for i,row in enumerate(rows,2):
    vals=[i-1]+row
    for j,v in enumerate(vals,1):
        col=j if j<13 else j+1  # leave col 13 for formula
        if j>=13: pass
    # write explicitly
    out=vals[:12]+[None]+vals[12:]
    for j,v in enumerate(out,1):
        if j==13: continue
        c=z.cell(i,j,v if v!='' else None); c.font=base; c.alignment=Alignment(wrap_text=True,vertical='top')
    z.cell(i,11).font=blue
    z.cell(i,13,f'=IF(K{i}="","",IF(L{i}="sq mi",K{i}*2.58999,K{i}))').number_format='0.00'
    z.cell(i,13).font=base
    if out[19] and ('ERROR' in out[19] or 'wrong' in out[19] or 'inconsistent' in out[19] or 'different schemes' in out[19] or 'Corrected' in out[19]):
        z.cell(i,20).font=red
    for j in range(NEXT+1,len(cols)+1):
        z.cell(i,j).fill=yellow; z.cell(i,j).font=base
    for j in range(1,len(cols)+1): z.cell(i,j).border=Border(bottom=thin)
last=len(rows)+1
z.cell(1,13).comment=Comment('Formula: sq mi x 2.58999 = km2. 1 sq mi = 2.58999 km2 (exact to 5 d.p.).','Claude')
widths={'A':5,'B':14,'C':8,'D':18,'E':14,'F':22,'G':26,'H':9,'I':30,'J':40,'K':9,'L':7,'M':9,'N':11,'O':40,'P':13,'Q':30,'R':30,'S':22,'T':38,'U':30}
for k,v in widths.items(): z.column_dimensions[k].width=v
for j in range(NEXT+1,len(cols)+1): z.column_dimensions[get_column_letter(j)].width=18
z.freeze_panes='E2'; z.auto_filter.ref=f'A1:{get_column_letter(len(cols))}{last}'
dvs=[('L',['km2','sq mi']),('N',['Reported','Verify','GIS needed']),('V',['Traffic','Air quality','Other']),
('Y',['Inside zone','Cordon crossing','Outside zone (spillover)','Network-wide']),
('AA',['Before-after','DiD','Synthetic control','RDD','Interrupted time series','Model-based']),('AB',['Y','N'])]
for col,opts in dvs:
    dv=DataValidation(type='list',formula1='"'+','.join(opts)+'"',allow_blank=True); z.add_data_validation(dv); dv.add(f'{col}2:{col}{last+200}')

# Excluded
e=wb.create_sheet('Excluded')
for j,h in enumerate(['Rose_DB_row','City','Country','Policy_type_recorded','Reason'],1):
    c=e.cell(1,j,h); c.font=hdr_font; c.fill=hdr_fill
for i,idx in enumerate(sorted(exc),2):
    o=d.loc[idx]
    for j,v in enumerate([idx+2,s(o['City']) or '(not recorded)',s(o['Country']),s(o['Policy Type']),exc[idx]],1):
        c=e.cell(i,j,v); c.font=base; c.alignment=Alignment(wrap_text=True,vertical='top')
for k,v in {'A':10,'B':22,'C':22,'D':40,'E':70}.items(): e.column_dimensions[k].width=v
e.freeze_panes='A2'

# Summary
sm=wb.create_sheet('Summary')
R=f'$2:$500'
sm['A1']='Counts (formulas on Zone_schemes)'; sm['A1'].font=Font(name=F,bold=True,size=12)
heads=['Policy family','Schemes','Area Reported','Area Verify','Area GIS needed','With Area_km2','With effect extracted']
for j,h in enumerate(heads,1):
    c=sm.cell(3,j,h); c.font=hdr_font; c.fill=hdr_fill; c.alignment=Alignment(wrap_text=True)
for i,fam in enumerate([CC,EZ,AR],4):
    sm.cell(i,1,fam)
    sm.cell(i,2,f'=COUNTIF(Zone_schemes!$F$2:$F$500,A{i})')
    sm.cell(i,3,f'=COUNTIFS(Zone_schemes!$F$2:$F$500,A{i},Zone_schemes!$N$2:$N$500,"Reported")')
    sm.cell(i,4,f'=COUNTIFS(Zone_schemes!$F$2:$F$500,A{i},Zone_schemes!$N$2:$N$500,"Verify")')
    sm.cell(i,5,f'=COUNTIFS(Zone_schemes!$F$2:$F$500,A{i},Zone_schemes!$N$2:$N$500,"GIS needed")')
    sm.cell(i,6,f'=COUNTIFS(Zone_schemes!$F$2:$F$500,A{i},Zone_schemes!$K$2:$K$500,"<>")')
    sm.cell(i,7,f'=COUNTIFS(Zone_schemes!$F$2:$F$500,A{i},Zone_schemes!$X$2:$X$500,"<>")')
sm.cell(7,1,'Total').font=Font(name=F,bold=True)
for j in range(2,8):
    L=get_column_letter(j); sm.cell(7,j,f'=SUM({L}4:{L}6)').font=Font(name=F,bold=True)
sm.cell(9,1,'Excluded rows'); sm.cell(9,2,'=COUNTA(Excluded!$A$2:$A$500)')
sm.cell(10,1,'Original rows (check: included from Rose DB + excluded = 65)'); sm.cell(10,2,'=COUNTIF(Zone_schemes!$B$2:$B$500,"Rose DB")+B9')
sm.cell(12,1,'Smallest Area_km2'); sm.cell(12,2,'=MIN(Zone_schemes!$M$2:$M$500)')
sm.cell(13,1,'Largest Area_km2'); sm.cell(13,2,'=MAX(Zone_schemes!$M$2:$M$500)')
sm.cell(12,2).number_format=sm.cell(13,2).number_format='0.00'
for row in sm.iter_rows(min_row=4,max_row=13):
    for c in row:
        if c.font.name!=F or not c.font.bold: c.font=Font(name=F,bold=c.font.bold)
sm.column_dimensions['A'].width=52
for L in 'BCDEFG': sm.column_dimensions[L].width=13
wb.save('/home/claude/work/Boundary_Size_Database_v1.xlsx')
print(len(rows),'included;',len(exc),'excluded')
