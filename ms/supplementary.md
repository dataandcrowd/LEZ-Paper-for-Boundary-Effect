---
title: "Supplementary Information: Does Zone Size Matter? A Scoping Review"
date: "Draft 3 (scoping review), 2 November 2026"
---

# S1. Inventory and search protocol

**Inventory.** The starting point was a hand-compiled database of 65 urban road charging and access regulation schemes (Congestion Charging Database, compiled by Rose [full name and acknowledgement to add]). Rows were kept if they defined a bounded area that vehicles are charged or restricted for entering or circulating in. Removed: 20 linear motorway, expressway or bridge tolls, two point-based gantry charges (Singapore ERP, Dubai Salik), three plans or packages without a zone restriction (Derby, Nottingham, Southampton), two licence-plate rationing schemes without a bounded zone (Mexico City Hoy No Circula, Bogotá Pico y Placa) and one duplicate (Utrecht). Added because peer-reviewed evaluations exist: Stockholm, Gothenburg, Singapore Area Licensing Scheme, Valletta, Durham, Oslo, Milan Ecopass, London Western Extension, Rome, London LEZ for heavy vehicles, Lisbon, Antwerp, Brussels. Result: 50 zone-based schemes. Errors corrected in the source database are listed in the README of the deposited workbook (for example, the Beijing zone description had been copied from Berlin).

**Scheme-by-scheme search (completed).** For each of the 50 schemes, searches were run in October and November 2026 in Google Scholar, Crossref and publisher sites combining the scheme name (and local name) with evaluation, traffic, air quality, NO2, PM10, difference-in-differences and synthetic control. Reference lists of Chamberlain et al. (2023), Holman et al. (2015) and Delgado-Lindeman et al. (2025) were screened. Working papers, preprints and agency reports were excluded as effect sources. Every DOI was resolved through Crossref. Values first taken from secondary summaries were checked against the full texts for Milan Area C (Gibson & Carnovale, 2015, Beria, 2016), Antwerp and Brussels (Bruyneel et al., 2025) and the London Western Extension (Ding et al., 2022). Values for Barcelona (abstract and an institutional summary), Tassinari (2024), Danielis et al. (2012) and Givoni (2012) were taken from abstracts, working-paper or conference versions and are flagged in the extraction files.

**Database search (to be run after protocol registration).** See S2.

**Extraction.** One row per scheme, outcome and measurement time. Fields: outcome metric, percentage change (negative = reduction), measurement location, years in operation at the midpoint of the evaluation window, design, spillover, citation and DOI. Where only an absolute change was reported, the percentage was computed against the baseline mean stated in the paper and flagged. Full extraction: 115 rows from 61 sources (deposited files cc_effects.csv and lez_effects.csv).

# S2. Search strategy, selection and charting protocol

### Eligibility (Population, Concept, Context)

| Element | Include | Exclude |
|---|---|---|
| Population | Not applicable (the units are schemes, not people); any urban population | |
| Concept (intervention) | Urban schemes with a bounded zone that vehicles are charged or restricted for entering or circulating in: cordon or area congestion charges, toll rings, low emission zones, clean air zones, zero emission zones, limited traffic zones with emission or permit rules | Linear motorway, bridge or tunnel tolls; point-based gantry charging without a single boundary; licence-plate rationing without a zone; parking charges alone; national vehicle taxes |
| Outcomes | Ex-post quantitative change in traffic volume (crossings, counts, vehicle-km) or ambient pollutant concentration or emissions (NO2, NOx, PM10, PM2.5, black carbon) attributable to the scheme | Health outcomes without an exposure or traffic estimate; acceptability, revenue or equity outcomes only |
| Design | Any ex-post design: difference-in-differences, synthetic control, regression discontinuity in time, interrupted time series, before-after with or without reference sites, model-based attribution using observed data | Ex-ante or purely simulated scenarios; stated-preference studies |
| Context | Any country, 1975 to the search date | |
| Source | Peer-reviewed journal articles and refereed conference papers, any language with an English abstract | Working papers, preprints, theses, agency and council reports (recorded separately as grey literature, not charted as effect sources) |

### 2. Information sources

- Scopus (primary database)
- TRID (Transport Research International Documentation)
- Web of Science Core Collection (sensitivity check of Scopus coverage)
- Supplementary: scheme-by-scheme searches in Google Scholar for each of the 50 inventory schemes (first 50 results per query), backward citation searching of included studies, and the reference lists of Holman et al. (2015), Chamberlain et al. (2023) and the 2025 European Transport Research Review review of European LEZs (doi:10.1186/s12544-025-00749-2).

### 3. Search strings

#### Scopus (TITLE-ABS-KEY)

```
TITLE-ABS-KEY(
  ( "congestion charg*" OR "congestion pric*" OR "congestion tax*" OR "road pric*"
    OR "cordon pric*" OR "cordon charg*" OR "area licens*" OR "toll ring*" OR "toll cordon*"
    OR "low emission zone*" OR "low-emission zone*" OR "ultra low emission zone*"
    OR "clean air zone*" OR "zero emission zone*" OR "zero-emission zone*"
    OR "environmental zone*" OR umweltzone* OR "milieuzone*" OR "limited traffic zone*"
    OR "zona a traffico limitato" OR "zona de bajas emisiones" OR "zone a faibles emissions"
    OR "urban vehicle access regulation*" OR "urban access regulation*" )
  AND
  ( evaluat* OR impact* OR effect* OR "ex post" OR "ex-post" OR "natural experiment"
    OR "difference-in-difference*" OR "difference in difference*" OR "synthetic control"
    OR "regression discontinuity" OR "interrupted time series" OR "before and after"
    OR "before-and-after" OR "quasi-experiment*" )
  AND
  ( traffic OR "vehicle km*" OR "vehicle kilomet*" OR "vehicle entr*" OR "air quality"
    OR "air pollution" OR "nitrogen dioxide" OR no2 OR nox OR pm10 OR "pm2.5"
    OR "particulate matter" OR "black carbon" OR "elemental carbon" OR emission* )
)
AND PUBYEAR > 1974
AND ( LIMIT-TO ( DOCTYPE , "ar" ) OR LIMIT-TO ( DOCTYPE , "cp" ) )
```

#### TRID (keyword search, all fields)

```
("congestion charging" OR "congestion pricing" OR "congestion tax" OR "cordon pricing"
 OR "toll ring" OR "area licensing" OR "low emission zone" OR "clean air zone"
 OR "zero emission zone" OR "limited traffic zone" OR "urban access regulation")
AND (evaluation OR impact OR "before and after" OR "natural experiment")
```
Filters: record type = articles and conference papers; publication year 1975 onwards.

#### Web of Science (Topic)

Same three blocks as Scopus, with TS= and the same truncations; document types Article and Proceedings Paper.

Record the date, database, exact string and number of hits for each search in the table below.

| Source | Date run | Hits | After de-duplication |
|---|---|---|---|
| Scopus | [to fill] | [to fill] | |
| TRID | [to fill] | [to fill] | |
| Web of Science | [to fill] | [to fill] | |
| Scheme-by-scheme Google Scholar | Oct to Nov 2026 | [to fill] | |
| Citation searching | [to fill] | [to fill] | |

### 4. Selection

1. Export all records from Scopus, TRID and Web of Science (RIS) and import them into Covidence, which removes duplicates on import. Record the number of duplicates removed.
2. Title and abstract screening against section 1 by two reviewers working independently in Covidence (two votes required per record). Conflicts are resolved by discussion, with a third person if needed. Report agreement (Cohen's kappa) from the Covidence conflict record. If a second reviewer is not available for the whole set, one reviewer screens all records and the second screens a random 20% sample, and the protocol will be amended before screening starts.
3. Full-text screening by two reviewers independently in Covidence, recording one exclusion reason per study from a fixed list (wrong intervention, no ex-post estimate, simulation or ex-ante only, wrong outcome, grey literature, duplicate estimate, full text not available).
4. Studies already identified in the scheme-by-scheme search (61 sources, 115 estimates) are added to Covidence as records from "other sources" so that they pass through the same full-text step. Report how many were found by the database search, how many only by supplementary searching, and how many new studies the database search added. The PRISMA flow counts are taken from Covidence.

### 5. Data charting

Charting is done in a Covidence extraction template that mirrors the Effects sheet of data/Boundary_Size_Database_v3.xlsx (scheme, outcome metric, effect, measurement location, years in operation, design, spillover, citation, DOI) plus the scheme-level fields (zone area and its source, urban centre area, charge or fine, compliance at launch). One reviewer charts in Covidence and a second verifies a 20% sample and every value taken from a secondary summary. Zone area is charted as reported in the evaluation, and separately from official sources or polygons, so the review can report how often evaluations state the size of the zone they evaluate.

### 6. Synthesis

Descriptive evidence map: number of schemes in the inventory with at least one ex-post evaluation, by scheme type and region; distribution of designs, outcomes, measurement locations and years in operation; reporting of zone area and spillover. Descriptive patterns of headline effect against zone size (relative coverage and km²) and against years in operation, shown in figures and summarised with medians and Spearman rank correlations without inferential claims. Critical appraisal is not required for scoping reviews (JBI); design type is charted as a descriptor of the evidence base.

### 7. Protocol registration

Register a short protocol on OSF before running the database searches (title, objectives and questions, eligibility, information sources, search strings, selection, charting, synthesis). Note in the manuscript that the scheme-by-scheme search was run before registration.


# S3. Charting and synthesis rules

Primary outcome: traffic volume for congestion charges (cordon crossings preferred, otherwise vehicle-km inside the zone) and NO₂ inside the zone for LEZs. PM10, PM2.5, black carbon and air quality rows for charges are secondary. Analysed separately rather than in the main set: spatial-contrast designs (Ding et al., 2022, which compares roads just inside and outside the Western Extension boundary and has no baseline year), marginal changes to existing schemes (Stockholm 2016 and Milan 2023 charge increases, Singapore 1989 evening extension, Munich 2023 diesel ban), removals (Trondheim 2005, +11.3% in former charged hours in the raw comparison while county traffic grew 5.2%, Meland et al., 2010) and pooled multi-city estimates without a single zone size (German and Dutch panels).

Design types (charted as descriptors, not as a quality score): (1) untreated control group or natural experiment (difference-in-differences, synthetic control, regression discontinuity in time, interrupted time series with a control or natural experiment, namely Gibson and Carnovale 2015, Maranzano et al. 2020, Atkinson et al. 2009); (2) before-after adjusted for external factors without a control (interrupted time series without control, for example Börjesson and Kristoffersson 2018, Bryant et al. 2025, Hajmohammadi and Heydecker 2022); (3) before-after, raw or against a reference site; (4) model-based. Headline estimate per scheme phase: earliest duration band (under 1.5 years, 1.5 to under 4, 4 or more), then best design tier, then the median if several remain. Years in operation is the midpoint of the evaluation window, or the window end for cumulative trend estimates (Antwerp, Brussels). Persistence ratio: latest divided by earliest estimate for one metric from one source, for schemes with two or more measurement times.

Phases: schemes whose boundary changed were split into phases (London ULEZ central 2019 and London-wide 2023; the inner London step of 2021 has no peer-reviewed estimate), giving 30 scheme phases. Rome's limited traffic zone is permit-based and is grouped with LEZs. Estimates reported only as not significant without a point estimate were charted as zero (Berlin NO₂, Gu et al., 2022; Milan Area B, Maranzano et al., 2020; London LEZ for heavy vehicles, Wood et al., 2015; London-wide ULEZ, Tong et al., 2025, whose point estimates appear only in their supplementary tables and should be extracted). Other non-significant estimates kept their reported point values (Munich, Sheffield, Bradford).

Zone area rule: the area of the zone in which the effect was measured. This gives the Western Extension alone (17 km²) rather than the combined charged zone (38.4 km²), and Lisbon Zone 1 (0.68 km²) for the Zone 1 NO₂ estimate. Table S3 shows the alternatives. Rome's −18% is paired with the 6 km² limited traffic zone. Cesaroni et al. (2012) report −4.13 and −2.99 µg/m³ for the two zones without labelling them in the abstract, and the pairing with the inner zone is inferred from their exposure results.

# S4. Size and stringency

Zone area: preferred value from the evaluation article, otherwise official documents, otherwise computed from an official boundary polygon (London Datastore, MTA, Glasgow City Council, Bradford Council, Lisbon City Council) or OpenStreetMap (Amsterdam 2008 truck zone, Antwerp) in an equal-area projection (EPSG:3035 or EPSG:27700). The range of published values is shown as horizontal bars in Figures 1 and S1. Denominator: urban centre area (field GC_UCA_KM2_2025) in GHS-UCDB R2024A version 1.2. Durham is not a UCDB urban centre; its denominator is the GHS-SMOD R2023A dense urban cluster (13 km²), a different definition. Bradford lies inside the Leeds urban centre. The UCDB epoch is 2025 rather than the year each scheme began. No area could be recovered for the Bergen, Oslo and Trondheim toll rings as first introduced, or for Gothenburg. Charges and fines: local amount at launch inflated to 2023 with national CPI and divided by the 2023 PPP conversion factor (World Bank WDI). Charge relative to income: charge divided by one day's 2023 GDP per capita at PPP. Compliance at launch: share of entering, detected or registered vehicles meeting the standard at the start of the phase, from peer-reviewed or official monitoring sources, except Milan Ecopass (working paper, flagged). Four official zone areas (Birmingham, Sheffield, Munich, Milan Area B) were carried from the source database and not yet traced to the original document, and Madrid Central's 4.72 km² is the city council figure quoted in a preprint.

# Table S1. Headline estimates and sources

| Scheme | Outcome metric used | Effect (%) | Design | Source(s) | Evidence tier |
|---|---|---|---|---|---|
| Bergen | Traffic across toll ring in initial period | -6.5 | Before-after | Ieromonachou et al. (2007), doi:10.18757/ejtir.2007.7.1.3371 | secondary citation in journal review |
| Durham | Vehicles entering the Saddler Street charging zone per day | -85.0 | Before-after | May et al. (2010), doi:10.1007/s12544-010-0026-1 | council monitoring reported in journal review |
| Gothenburg | Median of 2 estimates, e.g. Traffic across cordon during charged hours 2013 vs 2012 | -11.4 | Before-after | Börjesson and Kristoffersson (2015), doi:10.1016/j.tra.2015.03.011 and Börjesson and Kristoffersson (2018), doi:10.1016/j.tra.2017.11.001 | journal article |
| London CC | Median of 2 estimates, e.g. Vehicle-km inside zone during charging hours (all vehicles) 2003 vs 2002 | -11.8 | Before-after | Givoni (2012), doi:10.1177/0042098011417017 and Green et al. (2016), doi:10.1016/j.jpubeco.2015.10.005 | journal article |
| London WEZ | Total motor vehicle AADF flows inside WEZ after introduction (Feb 2007) | -5.0 | Control or natural experiment | Ait Bihi Ouali et al. (2021), doi:10.1371/journal.pone.0253881 | journal article |
| Milan Area C | Daily vehicle entries into Area C attributable to the charge (natural experiment: court suspension 25 Jul to 17 Sep 2012, sign reversed) | -14.5 | Control or natural experiment | Gibson and Carnovale (2015), doi:10.1016/j.jue.2015.06.005 | journal article |
| Milan Ecopass | Median of 2 estimates, e.g. Vehicles entering the Ecopass zone (8 km2) nine months after launch vs pre-period | -17.6 | Before-after | Rotaris et al. (2010), doi:10.1016/j.tra.2010.03.008 and Danielis et al. (2012), doi:10.3280/EFE2012-002004 | journal article |
| New York | Overall vehicle entries into the CRZ Jan to Jun 2025 vs 2024 | -11.0 | Before-after | Fraser et al. (2025), doi:10.1038/s44407-025-00037-2 | journal article |
| Oslo | Traffic across toll cordon in first year | -4.0 | Before-after | Ieromonachou et al. (2005) | conference paper citing thesis |
| Singapore ALS | Inbound traffic (all vehicles) entering Restricted Zone during morning restricted hours immediately after ALS | -44.0 | Before-after | Fan (1995) | journal article without DOI (JEASTS 1995) |
| Stockholm | Traffic across cordon in charged hours adjusted to 2005 levels for external factors (employment, car ownership, fuel price) in 2006 | -21.4 | Adjusted before-after | Börjesson and Kristoffersson (2018), doi:10.1016/j.tra.2017.11.001 | journal article |
| Trondheim | Traffic across toll ring during charged hours after introduction | -10.0 | Before-after | Tretvik (2007) | conference paper (WCTR 2007) |
| Valletta | Morning peak traffic on St Anne Street (main approach) 2008 vs 2003 surveys | -25.0 | Before-after | Attard (2013) | conference paper (WCTR 2013) |
| Amsterdam (trucks) | Traffic contribution (roadside minus background) NO2 inside LEZ, adjusted for wind and traffic | -4.9 | Before-after | Panteliadis et al. (2014), doi:10.1016/j.atmosenv.2013.12.035 | journal article |
| Antwerp | Modelled annual residential NO2 inside LEZ, differential trend vs 10 Flemish control cities, cumulative 2016 to 2022 | -12.2 | Control or natural experiment | Bruyneel et al. (2025), doi:10.1016/j.envint.2025.109515 | journal article |
| Barcelona | NO2 at traffic stations inside ZBE vs synthetic control, 2020 to 2022 | -15.8 | Control or natural experiment | dos Santos et al. (2026), doi:10.1016/j.aeaoa.2026.100428 | journal article |
| Berlin | NO2 at traffic and background sites, GAMM | 0.0 | Before-after | Gu et al. (2022), doi:10.1016/j.jenvman.2021.114048 | journal article |
| Birmingham | Roadside NO2 inside CAZ vs augmented synthetic control, first year | -3.4 | Control or natural experiment | Liu et al. (2023), doi:10.1007/s10640-023-00794-2 | journal article |
| Bradford | City NO2 level change at Clean Air Plan implementation, ITS | -27.0 | Adjusted before-after | Bryant et al. (2025), doi:10.1016/j.envres.2025.120988 | journal article |
| Brussels | Modelled annual residential NO2 inside LEZ, differential trend vs Flemish and Walloon control cities, cumulative 2017 to 2022 | -13.3 | Control or natural experiment | Bruyneel et al. (2025), doi:10.1016/j.envint.2025.109515 | journal article |
| Glasgow | Median of 2 estimates, e.g. NO2 at High Street roadside, core weekdays, Aug-Sep 2022 vs Aug-Sep 2023 | -20.5 | Before-after | Shin et al. (2024), doi:10.32866/001c.123382 | journal article |
| Lisbon | Annual mean NO2, Zone 1 (city centre), 2009 to 2016 | -12.0 | Before-after | Santos et al. (2019), doi:10.1016/j.jhazmat.2018.11.061 | journal article |
| London LEZ (HGV) | Modelled annual NO2 at children's addresses, first three years | 0.0 | Before-after | Wood et al. (2015), doi:10.1371/journal.pone.0109121 | journal article |
| Madrid Central | Median of 2 estimates, e.g. NO2 at Plaza del Carmen (urban background, only station inside zone), DiD vs stations outside M30 and regional controls | -28.6 | Control or natural experiment | Salas et al. (2021), doi:10.1016/j.trd.2020.102689 and Gómez-Losada and Pires (2024), doi:10.1016/j.uclim.2024.101995 | journal article |
| Milan Area B | NO2 and NOx, unobserved components intervention model with neighbouring-city counterfactual, to Sep 2019 | 0.0 | Control or natural experiment | Maranzano et al. (2020), doi:10.3390/ijerph17031088 | journal article |
| Munich | NO2 at traffic sites, GAMM | 2.4 | Before-after | Gu et al. (2022), doi:10.1016/j.jenvman.2021.114048 | journal article |
| Rome | Additional modelled NO2 reduction in the two LEZs beyond citywide trend | -18.0 | Model | Cesaroni et al. (2012), doi:10.1136/oem.2010.063750 | journal article |
| Sheffield | De-weathered NO2 inside CAZ, DiD vs outside sites | 2.5 | Control or natural experiment | Williams et al. (2025), doi:10.1088/2515-7620/adf52f | journal article |
| ULEZ 2019 | Median of 5 estimates, e.g. Roadside NO2 vs synthetic control, 3 months | -19.0 | Control or natural experiment | Tong et al. (2025), doi:10.1038/s44407-025-00030-9 and Prieto-Rodriguez et al. (2022), doi:10.1016/j.tranpol.2022.10.010 | journal article |
| ULEZ 2023 | NO2 vs synthetic control, 3 months | 0.0 | Control or natural experiment | Tong et al. (2025), doi:10.1038/s44407-025-00030-9 | journal article |

# Table S2. Zone areas, urban centre areas, charge and compliance sources

| Scheme | Zone (km²), preferred (min to max) | Zone area source | Urban centre (km²) | Charge or fine source | Compliance at launch (%) and source |
|---|---|---|---|---|---|
| Bergen |  | not available | 50 | Ieromonachou et al. (2007) EJTIR 7(1) (peer-reviewed) |  |
| Durham | 0.35 (0.35 to 0.35) | secondary: Ieromonachou et al. (2007) Table 1 | 13 | Ieromonachou et al. (2007) EJTIR 7(1); level unchanged later is grey (peer-reviewed) |  |
| Gothenburg |  | not available | 191 | Börjesson and Kristoffersson (2015) (peer-reviewed) |  |
| London CC | 21.4 (21 to 22) | computed from polygon (official TfL/GLA polygon, EPSG:3035 equal-area = 21.38 km2) | 1649 | Santos and Fraser (2006) Economic Policy 21(46) (peer-reviewed) |  |
| London WEZ | 17 (17 to 17) | reported in peer-reviewed article | 1649 | Stringency notes (GBP 8 single zone); level matches Santos and Fraser (2006) for 2005 rise (peer-reviewed) |  |
| Milan Area C | 8.2 (7.95 to 8.2) | reported in peer-reviewed article | 785 | Beria (2016); resident and service rates from ITF-OECD Milan paper (grey, peer-reviewed) |  |
| Milan Ecopass | 8.2 (7.95 to 8.2) | reported in peer-reviewed article | 785 | Rotaris et al. (2010) Transp Res A 44(5); class table also in Danielis et al. Ecopass working paper (units.it) (grey, peer-reviewed) | 58, Danielis, Rotaris and Marcucci working paper "Ecopass 3 years later" Table 3 (AMAT official counts) (working paper) |
| New York | 23.8 (23.8 to 28.5) | computed from polygon (official MTA geofence, local Lambert azimuthal equal-area) | 3031 | MTA (official) |  |
| Oslo |  | not available | 244 | Ieromonachou et al. (2007) EJTIR 7(1) gives NOK 11; ERSA 2005 conference paper gives NOK 10 (grey, peer-reviewed) |  |
| Singapore ALS | 6 (5.59 to 6.7) | reported in academic book (no peer-reviewed article with the figure found) | 438 | National Library Board Singapore Infopedia "Area Licensing Scheme"; Phang and Toh (1997, 2004) (official, peer-reviewed) |  |
| Stockholm | 30 (24 to 47) | reported in peer-reviewed article | 339 | Börjesson et al. (2012); Börjesson and Kristoffersson (2018) (peer-reviewed) |  |
| Trondheim |  | not available | 57 | Tretvik (2007, conference paper) |  |
| Valletta | 0.8 (0.8 to 0.84) | reported in peer-reviewed article | 100 | Attard and Ison (2010, peer-reviewed); Attard (2013, conference paper) |  |
| Amsterdam (trucks) | 47.2 (47.2 to 65.6) | computed from polygon (OSM current milieuzone polygon minus Noord district, local LAEA) | 308 | Dutch Parliament letter Kamerstuk 31305 nr. 87 (fine raised to EUR 150 on 1 May 2008) (official) |  |
| Antwerp | 22.9 (22.9 to 22.9) | computed from polygon (OSM relation, local LAEA) | 327 | VRT News (31 Jan 2018) |  |
| Barcelona | 95 (94.7 to 95) | reported in official document | 438 | 3Cat public broadcaster report on Barcelona ordinance |  |
| Berlin | 88 (87.2 to 88) | reported in official document | 681 | Bundestag Wissenschaftliche Dienste WD 8-056/21 (EUR 40 before May 2014); sticker mapping 35. BImSchV Annex 2 (official) |  |
| Birmingham | 7.77 (7.68 to 7.77) | reported in official document | 685 | Birmingham City Council CAZ six-month report (official) | 79.8, Birmingham City Council CAZ six-month report (2022) (official) |
| Bradford | 22 (22 to 24.2) | computed from polygon (official council polygon, EPSG:27700 and EPSG:3035) | 321 | Scheme table (council tariff) (grey) | 96.4, Bryant et al. (2025) (peer-reviewed) |
| Brussels | 161.4 (158.3 to 162.4) | reported in official document | 235 | Bruxelles Environnement, Évaluation de la LEZ 2018 (official) | 99.5, Bruxelles Environnement, Évaluation de la LEZ 2018 (official) |
| Glasgow | 3.06 (3.06 to 3.08) | computed from polygon (official council polygon, EPSG:27700 and EPSG:3035) | 309 | Glasgow City Council |  |
| Lisbon | 0.68 (0.68 to 0.68) | computed from polygon (official CML polygon, local LAEA; matches CML AREA_M2) | 426 | Ferreira et al. (2015) Atmospheric Environment for standards; fine not found (peer-reviewed) |  |
| London LEZ (HGV) | 1528.4 (1528.4 to 1572) | computed from polygon (official TfL/GLA polygon, EPSG:27700) | 1649 | TfL |  |
| Madrid Central | 4.72 (4.47 to 4.72) | reported in official document | 680 | Stringency notes; fine amount not independently verified (grey) |  |
| Milan Area B | 128.29 (119.8 to 130.8) | reported in official document | 785 | Quattroruote guide (fine EUR 83); rules: Varesenews 2019 (grey, news) |  |
| Munich | 44 (44 to 44.6) | reported in official document | 345 | Bundestag WD 8-056/21 (official) |  |
| Rome | 6 (5.1 to 6) | reported in peer-reviewed article | 467 | Not verified |  |
| Sheffield | 2.33 (2.33 to 2.37) | reported in official document | 219 | Scheme table and notes (grey) |  |
| ULEZ 2019 | 21.4 (21 to 22) | computed from polygon (official TfL/GLA polygon, EPSG:3035) | 1649 | TfL (official) | 60.9, Tong et al. (2025) (peer-reviewed) |
| ULEZ 2023 | 1528.8 (1528.8 to 1572) | computed from polygon (official TfL/GLA polygon, EPSG:3035) | 1649 | TfL (official) | 92.6, Tong et al. (2025), entering vehicles |

# Table S3. Sensitivity analyses (Spearman rank correlation of headline effect with size or stringency)

A positive ρ means larger values go with effects closer to zero (smaller reductions). Effect is negative for a reduction. p values are shown for reference only and are not interpreted, given the descriptive aim of the review.

| Analysis | Congestion charges (traffic) | Low emission zones (NO₂) |
|---|---|---|
| Relative coverage, all (main) | ρ = -0.577, n = 9, p = 0.104 | ρ = 0.371, n = 17, p = 0.142 |
| Absolute area (km²), all | ρ = 0.678, n = 9, p = 0.045 | ρ = 0.334, n = 17, p = 0.19 |
| Relative coverage, journal evidence only | ρ = -0.754, n = 6, p = 0.084 | ρ = 0.371, n = 17, p = 0.142 |
| Absolute area, journal evidence only | ρ = -0.058, n = 6, p = 0.913 | |
| Relative coverage, control or natural experiment only | n/a | ρ = 0.176, n = 9, p = 0.651 |
| Relative coverage, control or adjusted designs | n/a | ρ = 0.231, n = 10, p = 0.521 |
| Relative coverage, excluding Durham | ρ = -0.467, n = 8, p = 0.243 | |
| Absolute area, excluding Durham | ρ = 0.539, n = 8, p = 0.168 | |
| Absolute area, excluding Durham and Singapore | ρ = 0.342, n = 7, p = 0.452 | |
| Western Extension with combined zone area (38.4 km²), coverage | ρ = -0.31, n = 9, p = 0.417 | |
| Western Extension with combined zone area, km² | ρ = 0.812, n = 9, p = 0.008 | |
| Relative coverage, LEZs covering private cars | | ρ = 0.47, n = 13, p = 0.105 |
| Relative coverage, LEZs covering cars, control only | | ρ = 0.491, n = 8, p = 0.217 |
| Relative coverage, excluding four estimates reported only as not significant and charted as zero | | ρ = 0.159, n = 13, p = 0.603 |
| Relative coverage, excluding London-wide ULEZ | | ρ = 0.319, n = 16, p = 0.229 |
| Lisbon Zone 2 effect (−22%) with Zone 2 area (25.14 km²) | | ρ = 0.425, n = 17, p = 0.089 |
| As above, LEZs covering cars | | ρ = 0.613, n = 13, p = 0.026 |
| Charge relative to income vs effect | ρ = -0.181, n = 13, p = 0.553 | |
| Charge relative to income vs coverage | ρ = -0.226, n = 9, p = 0.559 | |
| Compliance at launch vs effect | | ρ = -0.1, n = 5, p = 0.873 |
| Compliance at launch vs coverage | | ρ = 0.6, n = 5, p = 0.285 |
| Start year vs coverage | | ρ = -0.117, n = 17, p = 0.654 |

# Table S4. LEZ headline effects by coverage tercile

| Tercile | n | Median effect (%) | Coverage range (%) | Schemes |
|---|---|---|---|---|
| small | 6 | -15.0 | 0.16 to 1.3 | Birmingham, Glasgow, Lisbon, Madrid Central, Rome, Sheffield |
| medium | 5 | -12.2 | 1.3 to 12.9 | Antwerp, Berlin, Bradford, ULEZ 2019, Munich |
| large | 6 | -2.45 | 15.32 to 92.7 | Amsterdam (trucks), Barcelona, Brussels, London LEZ (HGV), ULEZ 2023, Milan Area B |

# Table S5. Persistence ratios

| Scheme | First (years, effect %) | Last (years, effect %) | Ratio |
|---|---|---|---|
| Gothenburg | 0.5, -10.9 | 2.5, -9.6 | 0.88 |
| London CC | 0.5, -11.6 | 3.5, -14.0 | 1.21 |
| ULEZ 2019 | 0.1, -19.6 | 0.5, -17.8 | 0.91 |
| Milan Ecopass | 0.5, -21.0 | 2.3, -16.0 | 0.76 |
| Munich | 1.0, 2.4 | 5.0, -10.0 | n/a (sign change) |
| Stockholm | 0.5, -21.4 | 5.5, -22.3 | 1.04 |

# Table S6. Pooled multi-city estimates (not in Figure 1)

| Estimate | Outcome | Effect (%) | Years | Design |
|---|---|---|---|---|
| German LEZ stage 1 (2008 cohort) | PM10 | -9.0 | 0.4 | DiD |
| German LEZs stages 1 to 3 (2008 to 2012) | PM10 | -4.0 | 2.0 | DiD |
| German LEZs stages 2 and 3 | NO2 | -3.4 | 2.0 | DiD |
| German LEZs stage 1 and stage 2 (25 cities, 2008 to 2009) | PM10 | -7.0 | 1.0 | DiD |
| German LEZs stage 1 (17 cities, 2008 to 2009) | NO2 | -4.0 | 1.0 | DiD |
| German LEZs stage 1 (19 cities, 2008 to 2009) | PM10 | -1.0 | 1.0 | DiD |
| German LEZs (58 zones, 2008 to 2016) | NO2 | -5.3 | 4.0 | DiD |
| German LEZs (58 zones, 2008 to 2016) | PM10 | -5.8 | 4.0 | DiD |
| German LEZs (43 cities, 2008 to 2016) | PM10 | -3.0 | 4.0 | DiD |
| German LEZs (58 zones, 2008 to 2018) | NO2 | -9.8 | 0.1 | RDD |
| German LEZs (58 zones, 2008 to 2018) | PM10 | -11.6 | 0.1 | RDD |
| Dutch truck LEZs and local traffic policies (2007 to 2008) | Black carbon | 0.0 | 2.0 | DiD |

# Table S7. Marginal changes and removals (not in Figure 1)

| Change | Outcome | Effect (%) |
|---|---|---|
| Stockholm congestion tax (2016 charge increase and bypass extension) | Traffic | -5.1 |
| Milan Area C (Oct 2023 charge increase) | Traffic | -5.3 |
| Singapore Area Licensing Scheme (1989 evening extension) | Traffic | -44.0 |
| Munich selective diesel ban within LEZ (Feb 2023) | NO2 | -5.8 |
| Munich selective diesel ban within LEZ (Feb 2023) | NO2 | -9.4 |
| Trondheim toll ring (removed Dec 2005) (removal) | Traffic | 11.3 |

# Figure S1

![Figure S1. Headline effect against absolute zone area (km², log scale). Markers as in Figure 1.](../figures/figS1_effect_vs_area_km2.png)

# S5. PRISMA-ScR checklist

| Item | Reported in |
|---|---|
| 1 Title | Title (identifies the report as a scoping review) |
| 2 Structured summary | Abstract (Findings format limits the abstract to 100 words and unstructured text) |
| 3 Rationale | Section 1 |
| 4 Objectives | Section 1, questions 1 to 3 |
| 5 Protocol and registration | Section 2, OSF registration [to add] |
| 6 Eligibility criteria | Section 2 and S2 (Eligibility) |
| 7 Information sources | Section 2 and S2 (Information sources), dates [to add] |
| 8 Search | S2 (Search strings) |
| 9 Selection of sources of evidence | S2 (Selection) |
| 10 Data charting process | Section 2 and S2 (Data charting) |
| 11 Data items | S1 (Extraction), S3, deposited extraction files |
| 12 Critical appraisal (optional) | Not undertaken; design type charted as a descriptor (S3) |
| 13 Synthesis of results | Section 2 (Synthesis) and S2 (Synthesis) |
| 14 Selection of sources of evidence | Flow counts [to add after database search]; inventory flow in S1 |
| 15 Characteristics of sources of evidence | Section 3.1, Table 1, Table S1 |
| 16 Critical appraisal within sources | Not applicable (item 12) |
| 17 Results of individual sources | Table 1, Table S1, deposited extraction files |
| 18 Synthesis of results | Section 3, Figures 1 and 2, Tables S3 to S7 |
| 19 Summary of evidence | Section 3.4 |
| 20 Limitations | Section 3.4 and S6 |
| 21 Conclusions | Section 3.4 |
| 22 Funding | [to add] |

# S6. Known limitations of the data

1. Six of the 13 charging schemes rest on conference papers, council data or a non-indexed journal, and all six are before-after comparisons. The absolute-area association for charges depends on three of them.
2. Headline estimates mix measurement locations within each type (cordon crossings and vehicle-km for charges, roadside and background monitors for LEZs).
3. Several LEZ estimates come from modelled residential exposure (Antwerp, Brussels) or emissions models (Rome).
4. The London Western Extension has two conflicting estimates. The difference-in-differences estimate (−5%, Ait Bihi Ouali et al., 2021) is used and the spatial regression discontinuity (−31%, Ding et al., 2022) is excluded as not a change estimate.
5. Stockholm years in operation are counted from January 2006, although charging was suspended from August 2006 to July 2007.
6. Milan Area C's headline (−14.5%) is the court-suspension natural experiment (Gibson & Carnovale, 2015). Beria (2016) reports −31.1% against the Ecopass year 2011, with city-wide traffic about 7% lower over the same period.
7. Compliance at launch is known for five LEZs only. Brussels (99.5%) refers to the Brussels-registered fleet, and the Milan Ecopass figure comes from a working paper.
8. The urban centre denominator is the 2025 epoch, not the year each scheme began. Durham is not a UCDB urban centre and uses a GHS-SMOD dense urban cluster instead.

# References cited only in the Supplementary Information

Arksey, H., & O'Malley, L. (2005). Scoping studies: Towards a methodological framework. *International Journal of Social Research Methodology*, 8(1), 19-32. https://doi.org/10.1080/1364557032000119616

Attard, M., & Ison, S. G. (2010). The implementation of road user charging and the lessons learnt: The case of Valletta, Malta. *Journal of Transport Geography*, 18(1), 14-22. https://doi.org/10.1016/j.jtrangeo.2009.05.009

Cervero, R. (1998). *The transit metropolis: A global inquiry*. Island Press.

Delgado-Lindeman, M., et al. (2025). Characteristics and effects of low emission zones in Europe. A systematic literature review. *European Transport Research Review*, 17. https://doi.org/10.1186/s12544-025-00749-2

Eliasson, J., Hultkrantz, L., Nerhagen, L., & Smidfelt Rosqvist, L. (2009). The Stockholm congestion-charging trial 2006: Overview of effects. *Transportation Research Part A: Policy and Practice*, 43(3), 240-250. https://doi.org/10.1016/j.tra.2008.09.007

Phang, S. Y., & Toh, R. S. (1997). From manual to electronic road congestion pricing: The Singapore experience and experiment. *Transportation Research Part E: Logistics and Transportation Review*, 33(2), 97-106. https://doi.org/10.1016/S1366-5545(97)00006-9

Phang, S. Y., & Toh, R. S. (2004). Road congestion pricing in Singapore: 1975 to 2003. *Transportation Journal*, 43(2), 16-25.

Santos, G., & Fraser, G. (2006). Road pricing: Lessons from London. *Economic Policy*, 21(46), 264-310. https://doi.org/10.1111/j.1468-0327.2006.00159.x

Ait Bihi Ouali, L., Musuuga, D., & Graham, D. J. (2021). Quantifying responses to changes in the jurisdiction of a congestion charge: A study of the London western extension. *PLOS ONE*, 16(7), e0253881. https://doi.org/10.1371/journal.pone.0253881

Beria, P. (2016). Effectiveness and monetary impact of Milan's road charge, one year after implementation. *International Journal of Sustainable Transportation*, 10(7), 657-669. https://doi.org/10.1080/15568318.2015.1083638

Bruyneel, L., Cox, B., Stauffer, A., Vandenthoren, L., Fierens, F., Nawrot, T. S., & Horemans, C. (2025). Positive impact of the introduction of low-emission zones in Antwerp and Brussels on air quality, socio-economic disparities and health: A quasi-experimental study. *Environment International*, 199, 109515. https://doi.org/10.1016/j.envint.2025.109515

Ding, H., Li, H., & Sze, N. N. (2022). Effects of the abolishment of London western charging zone on traffic flow and vehicle emissions. *International Journal of Sustainable Transportation*, 16(6), 558-569. https://doi.org/10.1080/15568318.2021.1914790

Meland, S., Tretvik, T., & Welde, M. (2010). The effects of removing the Trondheim toll cordon. *Transport Policy*, 17(6), 475-485. https://doi.org/10.1016/j.tranpol.2010.05.001

Arksey and O'Malley (2005) is cited in the protocol (S2). Full citations for every effect estimate, including Atkinson et al. (2009), Bryant et al. (2025), Cesaroni et al. (2012), Hajmohammadi and Heydecker (2022), Maranzano et al. (2020), Tassinari (2024) and the 2025 European Transport Research Review systematic review (doi:10.1186/s12544-025-00749-2), are given in Table S1 and in the deposited extraction files.
