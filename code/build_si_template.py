import re
old=open('si_template_scoping_v3.md').read()
inv=old[old.index('**Inventory.**'):old.index('**Scheme-by-scheme search')]
inv=inv.replace('Result: 50 zone-based schemes.','Result: 50 zone-based schemes. Oxford\'s temporary congestion charge (from 29 October 2025, £5 a day for cars passing six charge points) was excluded because it charges at points rather than on entry to a bounded zone, and its pilot Zero Emission Zone has council monitoring only.')
elig=old[old.index('| Element | Include | Exclude |'):old.index('### 2. Information sources')]
s3=old[old.index('# S3. Charting and synthesis rules'):old.index('# S4. Size and stringency')]
s3=s3.replace("Analysed separately rather than in the main set: spatial-contrast designs (Ding et al., 2022, which compares roads just inside and outside the Western Extension boundary and has no baseline year), marginal changes to existing schemes (Stockholm 2016 and Milan 2023 charge increases, Singapore 1989 evening extension, Munich 2023 diesel ban), removals (Trondheim 2005, +11.3% in former charged hours in the raw comparison while county traffic grew 5.2%, Meland et al., 2010) and pooled multi-city estimates without a single zone size (German and Dutch panels).",
"Excluded from the headline set: spatial-contrast designs (Ding et al., 2022, which compares roads just inside and outside the Western Extension boundary and has no baseline year) and pooled multi-city estimates without a single zone size (German and Dutch panels, Table S7). Boundary enlargements, charge or rule changes, suspensions and removals were compiled as within-city contrasts (Table S4) rather than as headline estimates. For these contrasts the outcome is the one reported for the change (traffic, NO₂ or PM10), and the earlier effect is shown only where the same or a comparable source reports it.")
assert 'Excluded from the headline set' in s3
s3=s3.replace("Table S3 shows the alternatives.","Table S8 shows the alternatives.")
s3=s3.rstrip()+"""

Size categories: street (under 1 km²), city centre (1 to under 10 km²), inner city (10 to under 50 km²), whole city (50 to under 500 km²) and metropolitan (500 km² or more), using the zone area defined above. The thresholds separate the orders of magnitude present in the data and are descriptive. Medians are reported with and without estimates charted as zero (Table S3). No estimates were pooled, because most categories hold five or fewer schemes and few sources report standard errors.

"""
s4=old[old.index('# S4. Size and stringency'):old.index('# Table S1.')].replace('horizontal bars in Figures 1 and S1','horizontal bars in Figures S1 and S2')
s6=old[old.index('# S6. Known limitations of the data'):old.index('# References cited only')].replace('# S6. Known limitations of the data','# S5. Known limitations of the data')
s6=s6.replace("1. Six of the 13 charging schemes rest on conference papers, council data or a non-indexed journal, and all six are before-after comparisons. The absolute-area association for charges depends on three of them.",
"1. Single-reviewer searching, screening and charting is the main departure from a systematic review. Key estimates were checked against the full texts (S1), but a second reviewer has not verified the full extraction.\n2. Six of the 13 charging schemes rest on conference papers, council data or a non-indexed journal, and all six are before-after comparisons. Both charges in the street category (Durham, Valletta) are among them.")
out=[];n=0
for l in s6.rstrip().split('\n'):
    m=re.match(r'^(\d+)\. ',l)
    if m: n+=1; l=f'{n}. '+l[m.end():]
    out.append(l)
s6='\n'.join(out)+f"\n{n+1}. Within-city contrasts mix outcomes and designs. Munich's change from stage 1 to stage 3 coincides with more years in operation, and the Milan Ecopass to Area C change (Beria, 2016) is a raw comparison during which city-wide traffic also fell by about 7%.\n{n+2}. The list of lifted German LEZs (Table S5) is compiled from official notices and press reports and may be incomplete.\n\n"
refs=old[old.index('# References cited only'):]
for drop in ["Arksey, H., & O'Malley, L. (2005)","Meland, S., Tretvik, T., & Welde, M. (2010)","Ait Bihi Ouali, L., Musuuga, D., & Graham, D. J. (2021)","Beria, P. (2016)"]:
    refs='\n\n'.join(p for p in refs.split('\n\n') if not p.startswith(drop))
refs=refs.replace("Arksey and O'Malley (2005) is cited in the protocol (S2). ","")
add="""Fan, H. S. L. (1995). Car ownership demand and traffic congestion in Singapore's restricted zone. *Journal of the Eastern Asia Society for Transportation Studies*, 1(2), 603-611.

Zhai, M., & Wolff, H. (2021). Air pollution and urban road transport: Evidence from the world's largest low-emission zone in London. *Environmental Economics and Policy Studies*, 23, 721-748. https://doi.org/10.1007/s10018-021-00307-9

Grey sources for Table S5 (accessed 3 November 2026): Regierungspräsidium Stuttgart, press release of 29 December 2023 on lifting the Heidenheim, Heilbronn, Herrenberg and Leonberg/Hemmingen zones. Regierungspräsidium Karlsruhe, Luftreinhalteplan Fortschreibung 2022 (Heidelberg, Karlsruhe, Pfinztal) and public notice of 31 May 2024 (Mannheim, Mühlacker). Regierungspräsidium Tübingen, Luftreinhalteplan Tübingen, 3. Fortschreibung (April 2024), with corresponding updates for Reutlingen and Ulm. Umweltbundesamt, Umweltzonen in Deutschland (Mannheim and Mühlacker lifted 1 August 2024, 37 zones remaining). Landeshauptstadt Mainz, Umweltzone (lifted 1 October 2025). Deutsche Umwelthilfe, press release of 20 July 2022 (Erfurt). VWE (2024), Abolition of some German environmental zones (Schwäbisch Gmünd, Wendlingen am Neckar, Urbach, Ilsfeld, Tübingen, Reutlingen, Ulm). kfz-auskunft.de, Informatives zu Umweltzonen (Hannover, Freiburg). AutoScout24, Umweltzonen in Deutschland (Neu-Ulm). auto motor und sport, Wegfall der Umweltzonen (Balingen).
"""
refs=refs.replace("# References cited only in the Supplementary Information\n\n","# References cited only in the Supplementary Information\n\n"+add+"\n")
ger="""| Zone (state) | Lifted | Basis stated in the official notice or report | Source type |
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

Twenty-two zones in total. The Umweltbundesamt listed 37 remaining German LEZs at the time of access. We found no peer-reviewed ex-post evaluation of any of these removals in Google Scholar or Crossref searches combining Umweltzone, Aufhebung, low emission zone, removal and abolition."""
T=f"""---
title: "Supplementary Information: Does Zone Size Matter? A Rapid Review of Ex-post Evaluations of Urban Congestion Charges and Low Emission Zones"
date: "Draft 4 (rapid review), 3 November 2026"
---

# S1. Inventory and search

{inv}**Search.** This is a rapid review (Garritty et al., 2021). For each of the 50 schemes, one reviewer searched Google Scholar, Crossref and publisher sites in October and November 2026, combining the scheme name (and local name) with evaluation, traffic, air quality, NO2, PM10, difference-in-differences and synthetic control. Reference lists of Chamberlain et al. (2023), Holman et al. (2015) and Delgado-Lindeman et al. (2025) were screened. Working papers, preprints and agency reports were not used as effect sources except where flagged in Table S1. Every DOI was resolved through Crossref. Values first taken from secondary summaries were checked against the full texts for Milan Area C (Gibson & Carnovale, 2015, Beria, 2016), Antwerp and Brussels (Bruyneel et al., 2025) and the London Western Extension (Ding et al., 2022). Values for Barcelona (abstract and an institutional summary), Tassinari (2024), Danielis et al. (2012) and Givoni (2012) were taken from abstracts, working-paper or conference versions and are flagged in the extraction files.

**Extraction.** One row per scheme, outcome and measurement time. Fields: outcome metric, percentage change (negative = reduction), measurement location, years in operation at the midpoint of the evaluation window, design, spillover, citation and DOI. Where only an absolute change was reported, the percentage was computed against the baseline mean stated in the paper and flagged. Full extraction: 115 rows from 58 sources (deposited files cc_effects.csv and lez_effects.csv).

# S2. Eligibility and departures from a systematic review

{elig}
Departures from a systematic review, following Garritty et al. (2021): (1) a scheme-by-scheme search of one academic search engine and Crossref replaced bibliographic database searches, (2) one reviewer searched, screened and charted, with full-text checks of key estimates, (3) no risk-of-bias tool was applied, and design type is reported as a descriptor, and (4) no meta-analysis was undertaken.

{s3}{s4}# Table S1. Headline estimates and sources

@S1@

# Table S2. Zone areas, urban centre areas, charge and compliance sources

@S2@

# Table S3. Headline effects by zone size category

Median headline effect (%) by size category. Estimates reported only as not significant are charted as zero. Control is the number of schemes with an untreated control group or natural experiment.

@sizecat@

# Table S4. Changes within the same city

@within@

# Table S5. German LEZs lifted between 2020 and 2025

{ger}

# Table S6. Persistence ratios

@pers@

# Table S7. Pooled multi-city estimates (not in Figure 1)

@pooled@

# Table S8. Spearman rank correlations of headline effect with zone size or stringency

A positive ρ means larger values go with effects closer to zero (smaller reductions). Effect is negative for a reduction. These are descriptive, and p values are shown for reference only.

@sens@

# Table S9. LEZ headline effects by coverage tercile

@terc@

# Figure S1

![Figure S1. Headline effect against relative zone coverage (zone area as a share of the urban centre, log scale). (A) Congestion charges, change in traffic. (B) Low emission zones, change in NO₂ inside the zone. Filled markers have an untreated control group or natural experiment. Squares in (A) rest on conference papers, council data or a non-indexed journal, and triangles in (B) are zones that exempt private cars. Horizontal bars show the range of reported or computed zone areas. Dashed arrows join phases of the same city with different boundaries.](../figures/figS1_effect_vs_coverage.png)

# Figure S2

![Figure S2. Headline effect against absolute zone area (km², log scale). Markers as in Figure S1.](../figures/figS2_effect_vs_area_km2.png)

# Figure S3

![Figure S3. Reported effect against years in operation for schemes with repeated estimates from the same source. Each line is one metric from one source. Munich's later estimates follow stricter stages. Filled markers have an untreated control group or natural experiment.](../figures/figS3_effect_vs_years.png)

{s6}{refs}"""
assert not re.search(r'[{}]',T)
open('si_template.md','w').write(T); print(len(T.split()))
