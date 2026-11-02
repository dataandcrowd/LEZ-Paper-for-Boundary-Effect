---
title: "Supplementary Information: Does Zone Size Matter? A Rapid Review of Ex-post Evaluations of Urban Congestion Charges and Low Emission Zones"
date: "Draft 4 (rapid review), 3 November 2026"
---

# S1. Inventory and search

**Inventory.** The starting point was a hand-compiled database of 65 urban road charging and access regulation schemes (Congestion Charging Database, compiled by Rose [full name and acknowledgement to add]). Rows were kept if they defined a bounded area that vehicles are charged or restricted for entering or circulating in. Removed: 20 linear motorway, expressway or bridge tolls, two point-based gantry charges (Singapore ERP, Dubai Salik), three plans or packages without a zone restriction (Derby, Nottingham, Southampton), two licence-plate rationing schemes without a bounded zone (Mexico City Hoy No Circula, Bogotá Pico y Placa) and one duplicate (Utrecht). Added because peer-reviewed evaluations exist: Stockholm, Gothenburg, Singapore Area Licensing Scheme, Valletta, Durham, Oslo, Milan Ecopass, London Western Extension, Rome, London LEZ for heavy vehicles, Lisbon, Antwerp, Brussels. Result: 50 zone-based schemes. Oxford's temporary congestion charge (from 29 October 2025, £5 a day for cars passing six charge points) was excluded because it charges at points rather than on entry to a bounded zone, and its pilot Zero Emission Zone has council monitoring only. Errors corrected in the source database are listed in the README of the deposited workbook (for example, the Beijing zone description had been copied from Berlin).

**Search.** This is a rapid review (Garritty et al., 2021). For each of the 50 schemes, one reviewer searched Google Scholar, Crossref and publisher sites in October and November 2026, combining the scheme name (and local name) with evaluation, traffic, air quality, NO2, PM10, difference-in-differences and synthetic control. Reference lists of Chamberlain et al. (2023), Holman et al. (2015) and Delgado-Lindeman et al. (2025) were screened. Working papers, preprints and agency reports were not used as effect sources except where flagged in Table S1. Every DOI was resolved through Crossref. Values first taken from secondary summaries were checked against the full texts for Milan Area C (Gibson & Carnovale, 2015, Beria, 2016), Antwerp and Brussels (Bruyneel et al., 2025) and the London Western Extension (Ding et al., 2022). Values for Barcelona (abstract and an institutional summary), Tassinari (2024), Danielis et al. (2012) and Givoni (2012) were taken from abstracts, working-paper or conference versions and are flagged in the extraction files.

**Extraction.** One row per scheme, outcome and measurement time. Fields: outcome metric, percentage change (negative = reduction), measurement location, years in operation at the midpoint of the evaluation window, design, spillover, citation and DOI. Where only an absolute change was reported, the percentage was computed against the baseline mean stated in the paper and flagged. Full extraction: 115 rows from 61 sources, 57 with a DOI (deposited files cc_effects.csv and lez_effects.csv).

# S2. Eligibility and departures from a systematic review

| Element | Include | Exclude |
|---|---|---|
| Population | Not applicable (the units are schemes, not people); any urban population | |
| Concept (intervention) | Urban schemes with a bounded zone that vehicles are charged or restricted for entering or circulating in: cordon or area congestion charges, toll rings, low emission zones, clean air zones, zero emission zones, limited traffic zones with emission or permit rules | Linear motorway, bridge or tunnel tolls; point-based gantry charging without a single boundary; licence-plate rationing without a zone; parking charges alone; national vehicle taxes |
| Outcomes | Ex-post quantitative change in traffic volume (crossings, counts, vehicle-km) or ambient pollutant concentration or emissions (NO2, NOx, PM10, PM2.5, black carbon) attributable to the scheme | Health outcomes without an exposure or traffic estimate; acceptability, revenue or equity outcomes only |
| Design | Any ex-post design: difference-in-differences, synthetic control, regression discontinuity in time, interrupted time series, before-after with or without reference sites, model-based attribution using observed data | Ex-ante or purely simulated scenarios; stated-preference studies |
| Context | Any country, 1975 to the search date | |
| Source | Peer-reviewed journal articles and refereed conference papers, any language with an English abstract | Working papers, preprints, theses, agency and council reports (recorded separately as grey literature, not charted as effect sources) |


Departures from a systematic review, following Garritty et al. (2021): (1) a scheme-by-scheme search of one academic search engine and Crossref replaced bibliographic database searches, (2) one reviewer searched, screened and charted, with full-text checks of key estimates, (3) no risk-of-bias tool was applied, and design type is reported as a descriptor, and (4) no meta-analysis was undertaken.

# S3. Charting and synthesis rules

Primary outcome: traffic volume for congestion charges (cordon crossings preferred, otherwise vehicle-km inside the zone) and NO₂ inside the zone for LEZs. PM10, PM2.5, black carbon and air quality rows for charges are secondary. Excluded from the headline set: spatial-contrast designs (Ding et al., 2022, which compares roads just inside and outside the Western Extension boundary and has no baseline year) and pooled multi-city estimates without a single zone size (German and Dutch panels, Table S8). The London Western Extension (2007 to 2011) was a temporary enlargement of the London charge and is analysed as an enlargement (Table S4, Figure 2) rather than as a separate scheme. Enlargements were included in Table S4 only where the original and the enlarged zone were evaluated on the same outcome (traffic or NO₂). Charge or rule changes, suspensions and removals are listed in Table S5, where the outcome is the one reported for the change (traffic, NO₂ or PM10).

Design types (charted as descriptors, not as a quality score): (1) untreated control group or natural experiment (difference-in-differences, synthetic control, regression discontinuity in time, interrupted time series with a control or natural experiment, namely Gibson and Carnovale 2015, Maranzano et al. 2020, Atkinson et al. 2009); (2) before-after adjusted for external factors without a control (interrupted time series without control, for example Börjesson and Kristoffersson 2018, Bryant et al. 2025, Hajmohammadi and Heydecker 2022); (3) before-after, raw or against a reference site; (4) model-based. Headline estimate per scheme phase: earliest duration band (under 1.5 years, 1.5 to under 4, 4 or more), then best design tier, then the median if several remain. Years in operation is the midpoint of the evaluation window, or the window end for cumulative trend estimates (Antwerp, Brussels). Persistence ratio: latest divided by earliest estimate for one metric from one source, for schemes with two or more measurement times.

Phases: schemes whose boundary changed were split into phases (the London ULEZ at its 2019 launch in central London and after its 2023 expansion to all of London, with no peer-reviewed estimate for the 2021 expansion to inner London). London's Low Emission Zone for heavy vehicles (from 2008) is a separate scheme from the ULEZ, giving 30 scheme phases. Rome's limited traffic zone is permit-based and is grouped with LEZs. Estimates reported only as not significant without a point estimate were charted as zero (Berlin NO₂, Gu et al., 2022; Milan Area B, Maranzano et al., 2020; London LEZ for heavy vehicles, Wood et al., 2015; 2023 ULEZ expansion, Tong et al., 2025, whose point estimates appear only in their supplementary tables and should be extracted). Other non-significant estimates kept their reported point values (Munich, Sheffield, Bradford).

Zone area rule: the area of the zone in which the effect was measured. This gives Lisbon Zone 1 (0.68 km²) for the Zone 1 NO₂ estimate. In Table S4 the enlarged zone is shown at its total area (38.4 km² for the London charge with the Western Extension, 25.14 km² for Lisbon Zones 1 and 2), although the London estimate was measured in the added 17 km² only. Table S9 shows the alternatives. Rome's −18% is paired with the 6 km² limited traffic zone. Cesaroni et al. (2012) report −4.13 and −2.99 µg/m³ for the two zones without labelling them in the abstract, and the pairing with the inner zone is inferred from their exposure results.

Size categories: street (under 1 km²), city centre (1 to under 10 km²), inner city (10 to under 50 km²), whole city (50 to under 500 km²) and metropolitan (500 km² or more), using the zone area defined above. The thresholds separate the orders of magnitude present in the data and are descriptive. Medians are reported with and without estimates charted as zero (Table S3). No estimates were pooled, because most categories hold five or fewer schemes and few sources report standard errors.

# S4. Size and stringency

Zone area: preferred value from the evaluation article, otherwise official documents, otherwise computed from an official boundary polygon (London Datastore, MTA, Glasgow City Council, Bradford Council, Lisbon City Council) or OpenStreetMap (Amsterdam 2008 truck zone, Antwerp) in an equal-area projection (EPSG:3035 or EPSG:27700). The range of published values is shown as horizontal bars in Figures S1 and S2. Denominator: urban centre area (field GC_UCA_KM2_2025) in GHS-UCDB R2024A version 1.2. Durham is not a UCDB urban centre; its denominator is the GHS-SMOD R2023A dense urban cluster (13 km²), a different definition. Bradford lies inside the Leeds urban centre. The UCDB epoch is 2025 rather than the year each scheme began. No area could be recovered for the Bergen, Oslo and Trondheim toll rings as first introduced, or for Gothenburg. Charges and fines: local amount at launch inflated to 2023 with national CPI and divided by the 2023 PPP conversion factor (World Bank WDI). Charge relative to income: charge divided by one day's 2023 GDP per capita at PPP. Compliance at launch: share of entering, detected or registered vehicles meeting the standard at the start of the phase, from peer-reviewed or official monitoring sources, except Milan Ecopass (working paper, flagged). Four official zone areas (Birmingham, Sheffield, Munich, Milan Area B) were carried from the source database and not yet traced to the original document, and Madrid Central's 4.72 km² is the city council figure quoted in a preprint.

# Table S1. Headline estimates and sources

@S1@

# Table S2. Zone areas, urban centre areas, charge and compliance sources

@S2@

# Table S3. Headline effects by zone size category

Median headline effect (%) by size category. Estimates reported only as not significant are charted as zero. Control is the number of schemes with an untreated control group or natural experiment.

@sizecat@

# Table S4. Original and enlarged zones in the same city (Figure 2)

@pairs@

# Table S5. Changes in charges or rules, suspensions and removals within a fixed boundary

@within@

# Table S6. German LEZs lifted between 2020 and 2025

| Zone (state) | Lifted | Basis stated in the official notice or report | Source type |
|---|---|---|---|
| Balingen (Baden-Württemberg) | November 2020 | State agency (LUBW) assessment confirming no limit exceedance | Press |
| Erfurt (Thuringia) | 2021 | Not stated in the source | NGO press release |
| Heidelberg, Karlsruhe, Pfinztal (Baden-Württemberg) | 2023 | LUBW assessment that no new exceedance would follow removal | Official |
| Schwäbisch Gmünd, Wendlingen am Neckar, Urbach, Ilsfeld (Baden-Württemberg) | 2023 | Air quality reports | Trade association, press |
| Heidenheim, Heilbronn, Herrenberg, Leonberg/Hemmingen (Baden-Württemberg) | 1 January 2024 | Ongoing monitoring below limit values | Official |
| Hannover (Lower Saxony) | 22 February 2024 | Not stated in the source | Press |
| Tübingen, Reutlingen, Ulm (Baden-Württemberg) | 2024 | LUBW assessment that the zones' effect on concentrations in 2024 was very small | Official |
| Neu-Ulm (Bavaria) | 2024 | Not stated in the source | Press |
| Mannheim, Mühlacker (Baden-Württemberg) | 1 August 2024 | Monitoring below limit values | Official |
| Freiburg im Breisgau (Baden-Württemberg) | 22 April 2025 | Not stated in the source | Press |
| Mainz (Rhineland-Palatinate) | 1 October 2025 | Improved air quality | Official |

Twenty-two zones in total. The Umweltbundesamt listed 37 remaining German LEZs at the time of access. We found no peer-reviewed ex-post evaluation of any of these removals in Google Scholar or Crossref searches combining Umweltzone, Aufhebung, low emission zone, removal and abolition.

# Table S7. Persistence ratios

@pers@

# Table S8. Pooled multi-city estimates (not in Figure 1)

@pooled@

# Table S9. Spearman rank correlations of headline effect with zone size or stringency

A positive ρ means larger values go with effects closer to zero (smaller reductions). Effect is negative for a reduction. These are descriptive, and p values are shown for reference only. Table S10 groups the LEZ estimates by coverage tercile instead.

@sens@

# Table S10. LEZ headline effects by coverage tercile

@terc@

# Figure S1

![Figure S1. Headline effect against relative zone coverage (zone area as a share of the urban centre, log scale). (A) Congestion charges, change in traffic. (B) Low emission zones, change in NO₂ inside the zone. Filled markers have an untreated control group or natural experiment. Squares in (A) rest on conference papers, council data or a non-indexed journal, and triangles in (B) are zones that exempt private cars. Horizontal bars show the range of reported or computed zone areas. Dashed arrows join phases of the same city with different boundaries.](../figures/figS1_effect_vs_coverage.png)

# Figure S2

![Figure S2. Headline effect against absolute zone area (km², log scale). Markers as in Figure S1.](../figures/figS2_effect_vs_area_km2.png)

# Figure S3

![Figure S3. Reported effect against years in operation for schemes with repeated estimates from the same source. Each line is one metric from one source. Munich's later estimates follow stricter stages. Filled markers have an untreated control group or natural experiment.](../figures/figS3_effect_vs_years.png)

# S5. Known limitations of the data

1. Single-reviewer searching, screening and charting is the main departure from a systematic review. Key estimates were checked against the full texts (S1), but a second reviewer has not verified the full extraction.
2. Six of the 13 charging schemes rest on conference papers, council data or a non-indexed journal, and all six are before-after comparisons. Both charges in the street category (Durham, Valletta) are among them.
3. Headline estimates mix measurement locations within each type (cordon crossings and vehicle-km for charges, roadside and background monitors for LEZs).
4. Several LEZ estimates come from modelled residential exposure (Antwerp, Brussels) or emissions models (Rome).
5. The London Western Extension has two conflicting estimates. The difference-in-differences estimate (−5%, Ait Bihi Ouali et al., 2021) is used and the spatial regression discontinuity (−31%, Ding et al., 2022) is excluded as not a change estimate.
6. Stockholm years in operation are counted from January 2006, although charging was suspended from August 2006 to July 2007.
7. Milan Area C's headline (−14.5%) is the court-suspension natural experiment (Gibson & Carnovale, 2015). Beria (2016) reports −31.1% against the Ecopass year 2011, with city-wide traffic about 7% lower over the same period.
8. Compliance at launch is known for five LEZs only. Brussels (99.5%) refers to the Brussels-registered fleet, and the Milan Ecopass figure comes from a working paper.
9. The urban centre denominator is the 2025 epoch, not the year each scheme began. Durham is not a UCDB urban centre and uses a GHS-SMOD dense urban cluster instead.
10. Within-city contrasts mix outcomes and designs. Munich's change from stage 1 to stage 3 coincides with more years in operation, and the Milan Ecopass to Area C change (Beria, 2016) is a raw comparison during which city-wide traffic also fell by about 7%.
11. The list of lifted German LEZs (Table S6) is compiled from official notices and press reports and may be incomplete.

# References cited only in the Supplementary Information

Fan, H. S. L. (1995). Car ownership demand and traffic congestion in Singapore's restricted zone. *Journal of the Eastern Asia Society for Transportation Studies*, 1(2), 603-611.

Zhai, M., & Wolff, H. (2021). Air pollution and urban road transport: Evidence from the world's largest low-emission zone in London. *Environmental Economics and Policy Studies*, 23, 721-748. https://doi.org/10.1007/s10018-021-00307-9

Grey sources for Table S6 (accessed 3 November 2026): Regierungspräsidium Stuttgart, press release of 29 December 2023 on lifting the Heidenheim, Heilbronn, Herrenberg and Leonberg/Hemmingen zones. Regierungspräsidium Karlsruhe, Luftreinhalteplan Fortschreibung 2022 (Heidelberg, Karlsruhe, Pfinztal) and public notice of 31 May 2024 (Mannheim, Mühlacker). Regierungspräsidium Tübingen, Luftreinhalteplan Tübingen, 3. Fortschreibung (April 2024), with corresponding updates for Reutlingen and Ulm. Umweltbundesamt, Umweltzonen in Deutschland (Mannheim and Mühlacker lifted 1 August 2024, 37 zones remaining). Landeshauptstadt Mainz, Umweltzone (lifted 1 October 2025). Deutsche Umwelthilfe, press release of 20 July 2022 (Erfurt). VWE (2024), Abolition of some German environmental zones (Schwäbisch Gmünd, Wendlingen am Neckar, Urbach, Ilsfeld, Tübingen, Reutlingen, Ulm). kfz-auskunft.de, Informatives zu Umweltzonen (Hannover, Freiburg). AutoScout24, Umweltzonen in Deutschland (Neu-Ulm). auto motor und sport, Wegfall der Umweltzonen (Balingen).

Attard, M., & Ison, S. G. (2010). The implementation of road user charging and the lessons learnt: The case of Valletta, Malta. *Journal of Transport Geography*, 18(1), 14-22. https://doi.org/10.1016/j.jtrangeo.2009.05.009

Delgado-Lindeman, M., et al. (2025). Characteristics and effects of low emission zones in Europe. A systematic literature review. *European Transport Research Review*, 17. https://doi.org/10.1186/s12544-025-00749-2

Phang, S. Y., & Toh, R. S. (1997). From manual to electronic road congestion pricing: The Singapore experience and experiment. *Transportation Research Part E: Logistics and Transportation Review*, 33(2), 97-106. https://doi.org/10.1016/S1366-5545(97)00006-9

Phang, S. Y., & Toh, R. S. (2004). Road congestion pricing in Singapore: 1975 to 2003. *Transportation Journal*, 43(2), 16-25.

Santos, G., & Fraser, G. (2006). Road pricing: Lessons from London. *Economic Policy*, 21(46), 264-310. https://doi.org/10.1111/j.1468-0327.2006.00159.x

Bruyneel, L., Cox, B., Stauffer, A., Vandenthoren, L., Fierens, F., Nawrot, T. S., & Horemans, C. (2025). Positive impact of the introduction of low-emission zones in Antwerp and Brussels on air quality, socio-economic disparities and health: A quasi-experimental study. *Environment International*, 199, 109515. https://doi.org/10.1016/j.envint.2025.109515

Ding, H., Li, H., & Sze, N. N. (2022). Effects of the abolishment of London western charging zone on traffic flow and vehicle emissions. *International Journal of Sustainable Transportation*, 16(6), 558-569. https://doi.org/10.1080/15568318.2021.1914790

Full citations for every effect estimate, including those cited only in S3 (Atkinson et al., 2009, Bryant et al., 2025, Cesaroni et al., 2012, Hajmohammadi and Heydecker, 2022, Maranzano et al., 2020, Tassinari, 2024), are given in the deposited extraction files (cc_effects.csv and lez_effects.csv), and those used as headline estimates also in Table S1.
