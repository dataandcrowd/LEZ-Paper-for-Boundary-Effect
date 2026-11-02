# Search strategy and screening protocol (scoping review)

Draft, 2 November 2026. Framework: JBI scoping review methodology (Peters et al., 2020) and Arksey and O'Malley (2005); reporting: PRISMA-ScR (Tricco et al., 2018).

## 1. Eligibility (Population, Concept, Context)

| Element | Include | Exclude |
|---|---|---|
| Concept (intervention) | Urban schemes with a bounded zone that vehicles are charged or restricted for entering or circulating in: cordon or area congestion charges, toll rings, low emission zones, clean air zones, zero emission zones, limited traffic zones with emission or permit rules | Linear motorway, bridge or tunnel tolls; point-based gantry charging without a single boundary; licence-plate rationing without a zone; parking charges alone; national vehicle taxes |
| Outcomes | Ex-post quantitative change in traffic volume (crossings, counts, vehicle-km) or ambient pollutant concentration or emissions (NO2, NOx, PM10, PM2.5, black carbon) attributable to the scheme | Health outcomes without an exposure or traffic estimate; acceptability, revenue or equity outcomes only |
| Design | Any ex-post design: difference-in-differences, synthetic control, regression discontinuity in time, interrupted time series, before-after with or without reference sites, model-based attribution using observed data | Ex-ante or purely simulated scenarios; stated-preference studies |
| Context | Any country, 1975 to the search date | |
| Source | Peer-reviewed journal articles and refereed conference papers, any language with an English abstract | Working papers, preprints, theses, agency and council reports (recorded separately as grey literature, not charted as effect sources) |

## 2. Information sources

- Scopus (primary database)
- TRID (Transport Research International Documentation)
- Web of Science Core Collection (sensitivity check of Scopus coverage)
- Supplementary: scheme-by-scheme searches in Google Scholar for each of the 50 inventory schemes (first 50 results per query), backward citation searching of included studies, and the reference lists of Holman et al. (2015), Chamberlain et al. (2023) and the 2025 European Transport Research Review review of European LEZs (doi:10.1186/s12544-025-00749-2).

## 3. Search strings

### Scopus (TITLE-ABS-KEY)

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

### TRID (keyword search, all fields)

```
("congestion charging" OR "congestion pricing" OR "congestion tax" OR "cordon pricing"
 OR "toll ring" OR "area licensing" OR "low emission zone" OR "clean air zone"
 OR "zero emission zone" OR "limited traffic zone" OR "urban access regulation")
AND (evaluation OR impact OR "before and after" OR "natural experiment")
```
Filters: record type = articles and conference papers; publication year 1975 onwards.

### Web of Science (Topic)

Same three blocks as Scopus, with TS= and the same truncations; document types Article and Proceedings Paper.

Record the date, database, exact string and number of hits for each search in the table below.

| Source | Date run | Hits | After de-duplication |
|---|---|---|---|
| Scopus | [to fill] | [to fill] | |
| TRID | [to fill] | [to fill] | |
| Web of Science | [to fill] | [to fill] | |
| Scheme-by-scheme Google Scholar | Oct to Nov 2026 | [to fill] | |
| Citation searching | [to fill] | [to fill] | |

## 4. Selection

1. Export all records from Scopus, TRID and Web of Science (RIS) and import them into Covidence, which removes duplicates on import. Record the number of duplicates removed.
2. Title and abstract screening against section 1 by two reviewers working independently in Covidence (two votes required per record). Conflicts are resolved by discussion, with a third person if needed. Report agreement (Cohen's kappa) from the Covidence conflict record. If a second reviewer is not available for the whole set, one reviewer screens all records and the second screens a random 20% sample, and the protocol will be amended before screening starts.
3. Full-text screening by two reviewers independently in Covidence, recording one exclusion reason per study from a fixed list (wrong intervention, no ex-post estimate, simulation or ex-ante only, wrong outcome, grey literature, duplicate estimate, full text not available).
4. Studies already identified in the scheme-by-scheme search (61 sources, 115 estimates) are added to Covidence as records from "other sources" so that they pass through the same full-text step. Report how many were found by the database search, how many only by supplementary searching, and how many new studies the database search added. The PRISMA flow counts are taken from Covidence.

## 5. Data charting

Charting is done in a Covidence extraction template that mirrors the Effects sheet of data/Boundary_Size_Database_v3.xlsx (scheme, outcome metric, effect, measurement location, years in operation, design, spillover, citation, DOI) plus the scheme-level fields (zone area and its source, urban centre area, charge or fine, compliance at launch). One reviewer charts in Covidence and a second verifies a 20% sample and every value taken from a secondary summary. Zone area is charted as reported in the evaluation, and separately from official sources or polygons, so the review can report how often evaluations state the size of the zone they evaluate.

## 6. Synthesis

Descriptive evidence map: number of schemes in the inventory with at least one ex-post evaluation, by scheme type and region; distribution of designs, outcomes, measurement locations and years in operation; reporting of zone area and spillover. Descriptive patterns of headline effect against zone size (relative coverage and km²) and against years in operation, shown in figures and summarised with medians and Spearman rank correlations without inferential claims. Critical appraisal is not required for scoping reviews (JBI); design type is charted as a descriptor of the evidence base.

## 7. Protocol registration

Register a short protocol on OSF before running the database searches (title, objectives and questions, eligibility, information sources, search strings, selection, charting, synthesis). Note in the manuscript that the scheme-by-scheme search was run before registration.

## References

Arksey, H., & O'Malley, L. (2005). Scoping studies: Towards a methodological framework. International Journal of Social Research Methodology, 8(1), 19-32. https://doi.org/10.1080/1364557032000119616

Peters, M. D. J., Marnie, C., Tricco, A. C., Pollock, D., Munn, Z., Alexander, L., McInerney, P., Godfrey, C. M., & Khalil, H. (2020). Updated methodological guidance for the conduct of scoping reviews. JBI Evidence Synthesis, 18(10), 2119-2126. https://doi.org/10.11124/JBIES-20-00167

Tricco, A. C., Lillie, E., Zarin, W., O'Brien, K. K., Colquhoun, H., Levac, D., Moher, D., Peters, M. D. J., Horsley, T., Weeks, L., Hempel, S., Akl, E. A., Chang, C., McGowan, J., Stewart, L., Hartling, L., Aldcroft, A., Wilson, M. G., Garritty, C., ... Straus, S. E. (2018). PRISMA Extension for Scoping Reviews (PRISMA-ScR): Checklist and explanation. Annals of Internal Medicine, 169(7), 467-473. https://doi.org/10.7326/M18-0850
