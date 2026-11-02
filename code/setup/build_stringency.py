import json, csv
# ---------- conversion factors (World Bank WDI, downloaded 2026-11-02, lastupdated 2026-10-08) ----------
def load(ind):
    d = json.load(open(f'/tmp/wb/{ind}.json'))
    out = {}
    for r in d[1]:
        if r['value'] is not None:
            out.setdefault(r['countryiso3code'], {})[int(r['date'])] = r['value']
    return out
CPI = load('FP.CPI.TOTL'); PPP = load('PA.NUS.PPP'); GDP = load('NY.GDP.PCAP.PP.CD')
# US 2025 CPI missing in WDI: BLS CPI-U (CPIAUCNS via FRED), mean of 11 published months (Oct 2025 not published).
US_CPIU_2023 = 304.7015833; US_CPIU_2025 = 321.943
ISO = {'GBP':'GBR','SEK':'SWE','NOK':'NOR','SGD':'SGP','USD':'USA'}
def iso_for(cur, country): return country if cur == 'EUR' else ISO[cur]

def convert(amount, cur, year, country):
    c = iso_for(cur, country)
    if c == 'USA' and year == 2025:
        infl = US_CPIU_2023 / US_CPIU_2025; cpi_txt = f'US CPI-U 2025 (11-month mean)={US_CPIU_2025:.3f}, 2023={US_CPIU_2023:.3f} (BLS via FRED)'
    else:
        infl = CPI[c][2023] / CPI[c][year]; cpi_txt = f'{c} CPI(2010=100) {year}={CPI[c][year]:.3f}, 2023={CPI[c][2023]:.3f} (WDI FP.CPI.TOTL)'
    ppp = PPP[c][2023]; gdp = GDP[c][2023]
    usd = amount * infl / ppp
    return usd, infl, ppp, gdp, c, cpi_txt

COLS = 'ID,City,Phase,Phase_start,Charge_type,Charge_local,Charge_daily_max_local,Currency,Charge_year,Charge_2023USD_PPP,Fine_local,Fine_2023USD_PPP,Charge_to_income,Cars_covered,Emission_standard,Compliance_at_launch_pct,Compliance_basis,Exemptions_major,Charge_source,Compliance_source,Conversion_notes'.split(',')

# country = ISO3 used for EUR-area CPI/PPP/GDP
R = []
def add(**k): R.append(k)

# ---- Congestion charges ----
add(ID=1,City='Bergen',country='NOR',Phase='Toll ring launch',Phase_start='1986-01',Charge_type='Per-crossing charge',Charge_local=5,Currency='NOK',Charge_year=1986,Cars_covered='Y',
    Exemptions_major='Inbound only; Mon to Fri 06:00 to 22:00; trucks NOK 10; no daily maximum reported',
    Charge_source='Ieromonachou et al. (2007) EJTIR 7(1) [peer-reviewed]')
add(ID=2,City='Durham',country='GBR',Phase='Road user charge launch',Phase_start='2002-10',Charge_type='Per-crossing charge',Charge_local=2,Currency='GBP',Charge_year=2002,Cars_covered='Y',
    Exemptions_major='Charged per exit Mon to Sat 10:00 to 16:00 on a single street; residents, blue badge and service vehicles exempt (exemptions grey)',
    Charge_source='Ieromonachou et al. (2007) EJTIR 7(1) [peer-reviewed]; level unchanged later is grey')
add(ID=3,City='Gothenburg',country='SWE',Phase='Congestion tax launch',Phase_start='2013-01',Charge_type='Per-crossing charge',Charge_local=18,Charge_daily_max_local=60,Currency='SEK',Charge_year=2013,Cars_covered='Y',
    Exemptions_major='SEK 8/13/18 by time of day; weekdays 06:00 to 18:29; multi-passage rule (one charge within 60 min); Backa exemption from 2018',
    Charge_source='Börjesson and Kristoffersson (2015) [peer-reviewed]')
add(ID=3,City='Gothenburg',country='SWE',Phase='Charge increase',Phase_start='2015-01',Charge_type='Per-crossing charge',Charge_local=22,Charge_daily_max_local=60,Currency='SEK',Charge_year=2015,Cars_covered='Y',
    Exemptions_major='Peak SEK 18 to 22, off-peak SEK 8 to 9; daily maximum assumed unchanged at SEK 60 (not restated in source)',
    Charge_source='Börjesson and Kristoffersson (2018) [peer-reviewed]')
for ph,start,amt,yr,src,ex in [
    ('Central zone launch','2003-02',5,2003,'Santos and Fraser (2006) Economic Policy 21(46) [peer-reviewed]','Residents 90% discount; motorcycles, taxis, blue badge holders exempt; 07:00 to 18:30 weekdays'),
    ('Charge increase','2005-07',8,2005,'Santos and Fraser (2006) Economic Policy 21(46) [peer-reviewed]','As launch'),
    ('Charge increase','2011-01',10,2011,'Green et al. (2016) J Public Econ 133 [peer-reviewed]','As launch; WEZ removed 24 Dec 2010'),
    ('Charge increase','2014-06',11.5,2014,'TfL [official, not peer-reviewed]','As launch'),
    ('Charge increase and hours extension','2020-06',15,2020,'TfL [official, not peer-reviewed]','Residents 90% discount; hours extended to 07:00 to 22:00 daily (temporary Covid change)')]:
    add(ID=4,City='London',country='GBR',Phase=ph,Phase_start=start,Charge_type='Daily charge',Charge_local=amt,Currency='GBP',Charge_year=yr,Cars_covered='Y',Exemptions_major=ex,Charge_source=src)
add(ID=5,City='London (Western Extension)',country='GBR',Phase='Western Extension',Phase_start='2007-02',Charge_type='Daily charge',Charge_local=8,Currency='GBP',Charge_year=2007,Cars_covered='Y',
    Exemptions_major='Single zone with original area; WEZ residents 90% discount; removed 24 Dec 2010',
    Charge_source='Stringency notes (GBP 8 single zone); level matches Santos and Fraser (2006) [peer-reviewed] for 2005 rise')
add(ID=6,City='Milan (Area C)',country='ITA',Phase='Area C launch',Phase_start='2012-01',Charge_type='Daily charge',Charge_local=5,Currency='EUR',Charge_year=2012,Cars_covered='Y',
    Emission_standard='Access ban: Euro 4 diesel / Euro 1 petrol minimum (Euro 0 petrol and Euro 0 to 3 diesel banned)',
    Exemptions_major='Residents 40 free entries per year then EUR 2; service vehicles EUR 3',
    Charge_source='Beria (2016); Beria and Boggio (2013) [peer-reviewed]; resident and service rates from ITF-OECD Milan paper [grey]')
add(ID=6,City='Milan (Area C)',country='ITA',Phase='Charge increase',Phase_start='2023-10',Charge_type='Daily charge',Charge_local=7.5,Currency='EUR',Charge_year=2023,Cars_covered='Y',
    Emission_standard='Access ban tightened over time (diesel Euro 4 banned from 2017); 2023 minimum not verified',
    Exemptions_major='Residents EUR 3 after free entries; service vehicles EUR 4.50 (scheme table, grey)',
    Charge_source='Moulin and Urbano (2025) Transport Policy 165 [peer-reviewed]')
add(ID=7,City='Milan (Ecopass)',country='ITA',Phase='Ecopass launch',Phase_start='2008-01',Charge_type='Daily charge',Charge_local=5,Currency='EUR',Charge_year=2008,Cars_covered='Y',
    Emission_standard='Differentiated charge: free for petrol Euro 3+ and diesel Euro 4 with DPF; EUR 2 petrol Euro 1 to 2; EUR 5 petrol Euro 0 and diesel Euro 1 to 3; EUR 10 diesel Euro 0',
    Compliance_at_launch_pct=58,Compliance_basis='Entering traffic, 2007 pre-launch: 42% of entering vehicles were in tolled classes (23% in 2008, 16% in 2009); Beria (2016) reported c. 20% then 14% tolled',
    Exemptions_major='Charge EUR 2/5/10 by class (EUR 5 class shown as standard car value); residents annual pass EUR 50/125/250; multi-entry rebates',
    Charge_source='Rotaris et al. (2010) Transp Res A 44(5) [peer-reviewed]; class table also in Danielis et al. Ecopass working paper (units.it) [grey]',
    Compliance_source='Danielis, Rotaris and Marcucci working paper "Ecopass 3 years later" Table 3 (AMAT official counts) [working paper; flag weaker]')
add(ID=8,City='New York',country='USA',Phase='Congestion Relief Zone launch',Phase_start='2025-01',Charge_type='Daily charge',Charge_local=9,Currency='USD',Charge_year=2025,Cars_covered='Y',
    Exemptions_major='Peak 05:00 to 21:00 weekdays (09:00 to 21:00 weekends); USD 2.25 overnight; charged once per day for cars; low-income (<USD 60k) 50% discount after 10 trips per month; disability exemptions',
    Charge_source='MTA [official, not peer-reviewed]')
add(ID=9,City='Oslo',country='NOR',Phase='Toll ring launch',Phase_start='1990-02',Charge_type='Per-crossing charge',Charge_local=11,Currency='NOK',Charge_year=1990,Cars_covered='Y',
    Exemptions_major='Inbound only, all days and hours; NOK 10 in another source; NOK 15 by 2004',
    Charge_source='Ieromonachou et al. (2007) EJTIR 7(1) [peer-reviewed] gives NOK 11; ERSA 2005 conference paper gives NOK 10 [grey]')
for ph,start,amt,yr,ex in [
    ('ALS launch','1975-06',3,1975,'Morning peak only; buses, motorcycles, commercial vehicles, car pools (4+ occupants) exempt; company cars SGD 6; monthly licence SGD 60'),
    ('Charge increase','1980-03',5,1980,'Company cars SGD 10; exemptions as launch'),
    ('Evening peak extension, charge cut','1989-06',3,1989,'Evening peak added; company cars SGD 6; motorcycles SGD 1; taxi, motorcycle and car pool exemptions removed by end 1989')]:
    add(ID=10,City='Singapore (ALS)',country='SGP',Phase=ph,Phase_start=start,Charge_type='Daily charge',Charge_local=amt,Currency='SGD',Charge_year=yr,Cars_covered='Y',Exemptions_major=ex,
        Charge_source='National Library Board Singapore Infopedia "Area Licensing Scheme" [official]; Phang and Toh (1997, 2004) [peer-reviewed, full text not opened]')
add(ID=11,City='Stockholm',country='SWE',Phase='Trial',Phase_start='2006-01',Charge_type='Per-crossing charge',Charge_local=20,Charge_daily_max_local=60,Currency='SEK',Charge_year=2006,Cars_covered='Y',
    Exemptions_major='SEK 10/15/20 by time of day 06:30 to 18:29 weekdays; alternative-fuel cars, taxis, motorcycles exempt (grey); Lidingö traffic exemption',
    Charge_source='Börjesson et al. (2012); Börjesson and Kristoffersson (2018) [peer-reviewed]')
add(ID=11,City='Stockholm',country='SWE',Phase='Permanent scheme',Phase_start='2007-08',Charge_type='Per-crossing charge',Charge_local=20,Charge_daily_max_local=60,Currency='SEK',Charge_year=2007,Cars_covered='Y',
    Exemptions_major='Same tariff as trial',Charge_source='Börjesson et al. (2012) [peer-reviewed]')
add(ID=11,City='Stockholm',country='SWE',Phase='Charge increase and Essingeleden extension',Phase_start='2016-01',Charge_type='Per-crossing charge',Charge_local=35,Charge_daily_max_local=105,Currency='SEK',Charge_year=2016,Cars_covered='Y',
    Exemptions_major='SEK 11 to 35 by time of day; Essingeleden bypass charged',Charge_source='Börjesson and Kristoffersson (2018) [peer-reviewed]')
add(ID=12,City='Trondheim',country='NOR',Phase='Toll ring launch',Phase_start='1991-10',Charge_type='Per-crossing charge',Charge_local=10,Currency='NOK',Charge_year=1991,Cars_covered='Y',
    Exemptions_major='Inbound Mon to Fri 06:00 to 17:00; heavy vehicles double; tag discounts; cordon removed Dec 2005',
    Charge_source='Tretvik (2007) [peer-reviewed book chapter per notes]')
add(ID=13,City='Valletta',country='MLT',Phase='CVA launch',Phase_start='2007-05',Charge_type='Time-based charge',Charge_local=0.82,Charge_daily_max_local=6.52,Currency='EUR',Charge_year=2007,Cars_covered='Y',
    Exemptions_major='First 30 min free then EUR 0.82 per hour (Charge_local is per hour); max EUR 6.52 per day; Valletta residents exempt (grey); replaced annual V-licence',
    Charge_source='Attard and Ison (2010, 2015); Attard (2013) [peer-reviewed]')
# ---- LEZ / CAZ ----
add(ID=15,City='Amsterdam',country='NLD',Phase='Truck LEZ',Phase_start='2009',Charge_type='Penalty (ban with fine)',Fine_local=150,Currency='EUR',Charge_year=2009,Cars_covered='N',
    Emission_standard='Heavy goods vehicles: Euro 0 to II excluded unless retrofitted (Euro III minimum); cars not covered',
    Exemptions_major='Temporary exemptions for trucks with no certified filter available',
    Charge_source='Dutch Parliament letter Kamerstuk 31305 nr. 87 (fine raised to EUR 150 on 1 May 2008) [official]')
add(ID=17,City='Barcelona',country='ESP',Phase='ZBE Rondes (fines from Sep 2020)',Phase_start='2020-01',Charge_type='Penalty (ban with fine)',Fine_local=100,Currency='EUR',Charge_year=2020,Cars_covered='Y',
    Emission_standard='DGT label required: Euro 4 diesel / Euro 3 petrol',
    Exemptions_major='Weekdays 07:00 to 20:00; fines EUR 100 to 500 (+30% repeat); up to 10 day authorisations per year at EUR 2; moratoria vans to Apr 2021, HGVs to Jul 2021; low-income self-employed',
    Charge_source='3Cat public broadcaster report on Barcelona ordinance [news; grey]')
add(ID=20,City='Berlin',country='DEU',Phase='LEZ stage 1 (red, yellow, green allowed)',Phase_start='2008-01',Charge_type='Penalty (ban with fine)',Fine_local=40,Currency='EUR',Charge_year=2008,Cars_covered='Y',
    Emission_standard='Euro 2 diesel (or Euro 1 with DPF) / Euro 1 petrol with catalyst',
    Exemptions_major='Sticker EUR 5; fine EUR 40 plus 1 penalty point; individual hardship exemptions',
    Charge_source='Bundestag Wissenschaftliche Dienste WD 8-056/21 (EUR 40 before May 2014) [official]; sticker mapping 35. BImSchV Annex 2 [legal]')
add(ID=20,City='Berlin',country='DEU',Phase='LEZ green only (German stage 3)',Phase_start='2010-01',Charge_type='Penalty (ban with fine)',Fine_local=40,Currency='EUR',Charge_year=2010,Cars_covered='Y',
    Emission_standard='Euro 4 diesel (or Euro 3 with DPF) / Euro 1 petrol with catalyst',
    Compliance_at_launch_pct=87,Compliance_basis='Private vehicles (fleet basis): green-only rule excluded about 13% of private vehicles',
    Exemptions_major='Individual hardship exemptions; Berlin skipped a separate yellow stage',
    Charge_source='Bundestag WD 8-056/21 [official]; 35. BImSchV [legal]',Compliance_source='Wolff (2014) [peer-reviewed], as supplied by caller and notes; not re-checked')
add(ID=21,City='Birmingham',country='GBR',Phase='Class D CAZ launch',Phase_start='2021-06',Charge_type='Daily charge',Charge_local=8,Currency='GBP',Charge_year=2021,Cars_covered='Y',
    Emission_standard='Euro 6 diesel / Euro 4 petrol',
    Compliance_at_launch_pct=79.8,Compliance_basis='Unique vehicles entering zone, June 2021 (cars 81.8%; LGV 63.3%; HGV 90.6%)',
    Exemptions_major='HGVs and buses GBP 50; charge paused first two weeks; temporary exemptions for some zone residents and lower-paid in-zone workers (detail grey)',
    Charge_source='Birmingham City Council CAZ six-month report [official]',Compliance_source='Birmingham City Council CAZ six-month report (2022) [official monitoring]')
add(ID=22,City='Bradford',country='GBR',Phase='Class C+ CAZ launch',Phase_start='2022-09',Charge_type='Daily charge',Charge_local=9,Currency='GBP',Charge_year=2022,Cars_covered='N',
    Emission_standard='Vans and taxis: Euro 6 diesel / Euro 4 petrol; HGV and bus Euro VI; private cars not covered',
    Compliance_at_launch_pct=96.4,Compliance_basis='Vehicles driving in the zone just before launch (3.6% non-compliant)',
    Exemptions_major='Main class shown is vans/minibuses GBP 9; taxis GBP 7; HGV and bus GBP 50; private cars not charged',
    Charge_source='Scheme table (council tariff) [grey]',Compliance_source='Bryant et al. (2025) [peer-reviewed]')
add(ID=26,City='Glasgow',country='GBR',Phase='Phase 1 (local service buses only)',Phase_start='2018-12',Charge_type='Penalty (ban with fine)',Currency='GBP',Cars_covered='N',
    Emission_standard='Local service buses (share of services Euro VI); cars not covered',
    Exemptions_major='Enforced via bus operator registration, no driver fine',
    Charge_source='Glasgow City Council / Callaghan (2026) SAQ presentation [official]; fine not applicable')
add(ID=26,City='Glasgow',country='GBR',Phase='Phase 2 (all vehicles, enforced)',Phase_start='2023-06',Charge_type='Penalty (ban with fine)',Fine_local=60,Currency='GBP',Charge_year=2023,Cars_covered='Y',
    Emission_standard='Euro 6 diesel / Euro 4 petrol',
    Exemptions_major='Penalty halved if paid within 14 days; doubles for repeat entry within 90 days up to a cap; zone residents exempt to June 2024',
    Charge_source='Glasgow City Council [official; grey per notes]')
for ph,start,comp,basis,csrc,ex in [
    ('Central ULEZ','2019-04',60.9,'Vehicles entering central zone, March 2019 (39.1% non-compliant)','Tong et al. (2025) [peer-reviewed], per caller and notes','Central zone residents 100% discount to Oct 2022; disabled-class vehicles grace to 2025; 24/7 operation; HGV GBP 100'),
    ('Inner London expansion','2021-10',86.9,'Unique vehicles detected in whole ULEZ (central plus inner), 12 to 20 Oct 2021 (cars 89.0%)','GLA/TfL Inner London ULEZ One Year Report (2023) [official monitoring]','Resident discount ended; disabled-class grace to 2025; scrappage scheme'),
    ('London-wide expansion','2023-08',90.9,'Vehicles detected in outer London, June 2023 pre-launch baseline; 92.6% (7.4% non-compliant) also reported in the study cited by earlier agents','GLA London-wide ULEZ first month report (2023) [official monitoring]','Expanded scrappage scheme; disabled-class grace to Oct 2027 (grey); 24/7')]:
    add(ID=29,City='London',country='GBR',Phase=ph,Phase_start=start,Charge_type='Daily charge',Charge_local=12.5,Currency='GBP',Charge_year=int(start[:4]),Cars_covered='Y',
        Emission_standard='Euro 6 diesel / Euro 4 petrol',Compliance_at_launch_pct=comp,Compliance_basis=basis,Exemptions_major=ex,
        Charge_source='Stringency notes; TfL [official]',Compliance_source=csrc)
add(ID=30,City='Madrid',country='ESP',Phase='Madrid Central',Phase_start='2018-11',Charge_type='Penalty (ban with fine)',Fine_local=90,Currency='EUR',Charge_year=2018,Cars_covered='Y',
    Emission_standard='Non-residents: DGT B label minimum, Euro 4 diesel / Euro 3 petrol (B and C label only to park; ECO and 0 free)',
    Exemptions_major='Residents and their guests exempt; fines from 16 Mar 2019 after warning period',
    Charge_source='Stringency notes [grey]; fine amount not independently verified')
add(ID=30,City='Madrid',country='ESP',Phase='Madrid 360 city-wide ZBE',Phase_start='2022-01',Charge_type='Penalty (ban with fine)',Currency='EUR',Cars_covered='Y',
    Emission_standard='Phased ban on unlabelled vehicles (Euro 4 diesel / Euro 3 petrol); applied first to non-Madrid-registered cars',
    Exemptions_major='Phased by vehicle domicile and ring (M-30) to 2025; fine not verified',
    Charge_source='Not verified; separate row as flagged in scheme table')
add(ID=31,City='Milan (Area B)',country='ITA',Phase='Area B phase 1',Phase_start='2019-02',Charge_type='Penalty (ban with fine)',Fine_local=83,Currency='EUR',Charge_year=2019,Cars_covered='Y',
    Emission_standard='Euro 4 diesel / Euro 1 petrol (Euro 0 petrol and Euro 0 to 3 diesel banned)',
    Exemptions_major='Weekdays 07:30 to 19:30; 50 free days in first year, then 25 (residents) or 5 (others); EUR 55.10 if paid within 5 days',
    Charge_source='Quattroruote guide (fine EUR 83) [grey]; rules: Varesenews 2019 [news]')
for ph,start,std,comp,basis,csrc,fine,yr,fsrc,ex in [
    ('LEZ stage 1','2008-10','Euro 2 diesel (or Euro 1 with DPF) / Euro 1 petrol with catalyst',None,'','',40,2008,'Bundestag WD 8-056/21 [official]','Combined with HDV transit ban (Feb 2008); sticker about EUR 6'),
    ('LEZ stage 2 (yellow and green)','2010-10','Euro 3 diesel (or Euro 2 with DPF) / Euro 1 petrol with catalyst',None,'','',40,2010,'Bundestag WD 8-056/21 [official]','Hardship exemptions'),
    ('LEZ stage 3 (green only)','2012-10','Euro 4 diesel (or Euro 3 with DPF) / Euro 1 petrol with catalyst',None,'','',40,2012,'Bundestag WD 8-056/21 [official]','Hardship exemptions'),
    ('Selective diesel ban (Euro 4 and older)','2023-02','Euro 5 diesel / Euro 1 petrol with catalyst',95,'Personal vehicles registered in Munich (registered fleet): ban affected about 5% (28% of heavy commercial vehicles)','Leibinger et al. (2024) [peer-reviewed]',100,2023,'German Bußgeldkatalog as amended Nov 2021 (EUR 100) [legal; secondary web source]','Many exemptions (residents, trades, delivery); enforcement unclear')]:
    add(ID=32,City='Munich',country='DEU',Phase=ph,Phase_start=start,Charge_type='Penalty (ban with fine)',Fine_local=fine,Currency='EUR',Charge_year=yr,Cars_covered='Y',
        Emission_standard=std,Compliance_at_launch_pct=comp,Compliance_basis=basis,Compliance_source=csrc,Exemptions_major=ex,Charge_source=fsrc)
add(ID=37,City='Sheffield',country='GBR',Phase='Class C CAZ launch',Phase_start='2023-02',Charge_type='Daily charge',Charge_local=10,Currency='GBP',Charge_year=2023,Cars_covered='N',
    Emission_standard='Vans and taxis: Euro 6 diesel / Euro 4 petrol; HGV and bus Euro VI; private cars not covered',
    Exemptions_major='Main class shown is vans and taxis GBP 10; HGV and bus GBP 50; private cars not charged',
    Charge_source='Scheme table and notes [grey]')
add(ID=45,City='Rome',country='ITA',Phase='ZTL historic centre (permit)',Phase_start='2001',Charge_type='Permit',Currency='EUR',Cars_covered='Y',
    Emission_standard='Separate LEZ rules excluded pre-Euro 1 vehicles in two zones 2001 to 2005 (grey)',
    Exemptions_major='Residents and authorised categories hold permits; permit fee and fine not verified',
    Charge_source='Not verified')
add(ID=47,City='London (LEZ heavy vehicles)',country='GBR',Phase='LEZ phases 1 and 2',Phase_start='2008-02',Charge_type='Daily charge',Charge_local=200,Currency='GBP',Charge_year=2008,Cars_covered='N',
    Emission_standard='HGV Euro III PM (over 12 t Feb 2008; over 3.5 t, buses and coaches Jul 2008); cars not covered',
    Exemptions_major='Main class HGV GBP 200 per day; cars not covered',
    Charge_source='TfL [official; grey per notes]')
add(ID=47,City='London (LEZ heavy vehicles)',country='GBR',Phase='LEZ phases 3 and 4',Phase_start='2012-01',Charge_type='Daily charge',Charge_local=200,Currency='GBP',Charge_year=2012,Cars_covered='N',
    Emission_standard='HGV Euro IV PM; large vans and minibuses Euro 3 PM (GBP 100)',
    Exemptions_major='Vans and minibuses GBP 100; cars not covered',
    Charge_source='TfL [official; grey per notes]')
for ph,start,std in [
    ('Phase 1 (Zone 1)','2011-07','Zone 1: Euro 1 minimum (all fuels)'),
    ('Phase 2 (Zones 1 and 2)','2012-04','Zone 1: Euro 2 / Zone 2: Euro 1 (all fuels)'),
    ('Phase 3','2015-01','Zone 1: Euro 3 / Zone 2: Euro 2 (all fuels)')]:
    add(ID=48,City='Lisbon',country='PRT',Phase=ph,Phase_start=start,Charge_type='Penalty (ban with fine)',Currency='EUR',Cars_covered='Y',Emission_standard=std,
        Exemptions_major='Weekdays daytime; residents, historic vehicles and emergency vehicles exempt (grey); enforcement reported as sporadic; fine not verified',
        Charge_source='Ferreira et al. (2015) Atmospheric Environment [peer-reviewed] for standards; fine not found')
add(ID=49,City='Antwerp',country='BEL',Phase='LEZ launch',Phase_start='2017-02',Charge_type='Penalty (ban with fine)',Fine_local=125,Currency='EUR',Charge_year=2017,Cars_covered='Y',
    Emission_standard='Euro 4 diesel (or Euro 3 with DPF) / Euro 1 petrol',
    Exemptions_major='Fine EUR 125 first offence, raised to EUR 150 in 2018; registration required for foreign vehicles',
    Charge_source='VRT News (31 Jan 2018) [news; grey]')
add(ID=50,City='Brussels',country='BEL',Phase='LEZ launch',Phase_start='2018-01',Charge_type='Penalty (ban with fine)',Fine_local=350,Currency='EUR',Charge_year=2018,Cars_covered='Y',
    Emission_standard='Euro 2 diesel / no petrol restriction in 2018 (petrol restrictions began Jan 2019)',
    Compliance_at_launch_pct=99.5,Compliance_basis='Brussels-registered fleet: 2,344 vehicles (0.5%) concerned in 2018',
    Exemptions_major='Warnings Jul to Sep 2018, fines from 1 Oct 2018; 3-month gap between fines; 2018 fines only to Belgian vehicles',
    Charge_source='Bruxelles Environnement, Évaluation de la LEZ 2018 [official]',Compliance_source='Bruxelles Environnement, Évaluation de la LEZ 2018 [official monitoring]')

# ---------- compute ----------
print(f"{'ID':>3} {'City':28} {'Phase':38} {'amt':>7} {'cur':4} {'yr':5} {'CPIratio':>8} {'PPP23':>8} {'USD23PPP':>9} {'GDPpc/365':>9} {'ratio':>6}")
rows = []
for r in R:
    out = {c: r.get(c, '') for c in COLS}
    notes = []
    amt = r.get('Charge_local'); fine = r.get('Fine_local'); val = amt if amt is not None and amt != '' else fine
    if val not in (None, ''):
        usd, infl, ppp, gdp, c, cpi_txt = convert(val, r['Currency'], r['Charge_year'], r['country'])
        daily_gdp = gdp / 365
        ratio = usd / daily_gdp
        if amt not in (None, ''):
            out['Charge_2023USD_PPP'] = round(usd, 2); out['Charge_to_income'] = round(ratio, 4)
        else:
            out['Fine_2023USD_PPP'] = round(usd, 2)
        notes.append(f"{val} {r['Currency']} x CPI ratio {infl:.4f} [{cpi_txt}] / PPP2023 {ppp:.4f} LCU per intl $ (WDI PA.NUS.PPP) = {usd:.2f}")
        notes.append(f"GDP pc PPP 2023 {c} = {gdp:,.0f} intl $ (WDI NY.GDP.PCAP.PP.CD); per day {daily_gdp:.2f}; {'charge' if amt not in (None,'') else 'fine (not in Charge_to_income)'} to income = {ratio:.4f}")
        mx = r.get('Charge_daily_max_local')
        if mx not in (None, ''):
            usdmx = mx * infl / ppp
            notes.append(f"daily max {mx} {r['Currency']} = {usdmx:.2f} 2023 USD PPP; max to income = {usdmx/daily_gdp:.4f}")
        print(f"{r['ID']:>3} {r['City'][:28]:28} {r['Phase'][:38]:38} {val:>7} {r['Currency']:4} {r['Charge_year']:5} {infl:8.4f} {ppp:8.4f} {usd:9.2f} {daily_gdp:9.2f} {ratio:6.3f}{'  (fine)' if amt in (None,'') else ''}")
    else:
        notes.append('No verified amount; not converted')
    out['Conversion_notes'] = '; '.join(notes)
    for c in COLS:
        if out[c] is None: out[c] = ''
    rows.append(out)
with open('/mnt/user-data/outputs/agent_outputs/stringency.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(rows)
print(len(rows), 'rows written')
# factor table
print('\nFactors used:')
for c in ['GBR','SWE','NOR','SGP','USA','ITA','MLT','NLD','ESP','DEU','PRT','BEL']:
    print(c, 'CPI2023', round(CPI[c][2023],3), 'PPP2023', round(PPP[c][2023],4), 'GDPpcPPP2023', round(GDP[c][2023]), 'per day', round(GDP[c][2023]/365,2))
