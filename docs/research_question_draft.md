# Does boundary size matter? Research question (draft v3, 31 Oct 2026)

Target journal: Transport Findings (Findings Press), article type "Synthesis". Sections are "1. Questions", "2. Methods", "3. Findings". 1,000 words main text, abstract 100 words or fewer (no acronyms), at most 3 figures and 3 tables, SI allowed but must not be needed to understand the paper. US$150 on acceptance. The journal prefers American spelling (check before submission).

## Research question (v3)

Among peer-reviewed ex-post evaluations of urban congestion charges and low emission zones, does the reported effect scale with the share of the urban area the zone covers, and does the relationship depend on how long the scheme has been in operation?

Possible numbered form for the Questions section:
1. Is the reported effect of congestion charges and LEZs associated with zone size (relative coverage of the built-up area; absolute km2 as a sensitivity check)?
2. Does the association differ between price-based schemes (congestion charges) and standard-based schemes (LEZs)?
3. Does the size relationship change with years in operation?

## Hypotheses (directional, by scheme type)

- Congestion charges: smaller cordons show larger percentage reductions in in-zone traffic, because small zones are easier to drive around (Singapore ALS about 6 km2 and about -44%; London 21 km2 and about -18%; Stockholm about 35 km2 and about -20%).
- LEZs: larger relative coverage is associated with larger NO2 reductions, because a larger zone forces more fleet renewal, with diminishing returns once compliance is already high (London ULEZ: central zone 2019 effective, Greater London step 2023 no detectable effect; Tong et al. 2025, npj Clean Air, doi:10.1038/s44407-025-00030-9, to verify).
- Duration: charge effects on traffic largely sustained (Stockholm, Borjesson et al. 2012, Transport Policy 20, 1-12); LEZ effects shrink against the counterfactual as fleets renew anyway; Milan pollution effects decayed within days (Percoco 2013, TR-D).

Headline message if supported: size matters, but in opposite directions for price-based and standard-based schemes.

## Design decisions

- Size: relative coverage (zone area / built-up area) as main measure, absolute km2 as sensitivity. Areas computed from official polygons; where sources disagree (Stockholm 24 to 47 km2) show the range as an error bar.
- Outcomes kept separate by scheme type: traffic (cordon crossings or in-zone traffic) for charges, roadside NO2 for LEZs. Never on one axis.
- Measurement location coded (inside zone / cordon / outside spillover / network) and held constant or stratified.
- Duration coded as years in operation at the time each effect was measured (no first-year anchor). Used as a stratifier (short, medium, long operation) and, where a scheme has two or more measurements, a persistence ratio (later effect / earlier effect). Not a continuous regressor (collinear with size and start year).
- Stringency reported alongside size: charge level relative to income, fleet compliance at launch, start year. Spearman correlations with size in SI.
- Evidence: peer-reviewed ex-post evaluations with a counterfactual or control. Expected analysable N about 20 to 25 (6 to 8 charges, 12 to 18 LEZs) out of 48 inventory schemes. Descriptive evidence map plus rank correlations within each scheme type; weighted meta-regression only if N allows (model: Fearnley and Veisten 2026, Transport Findings, doi:10.32866/001c.166736, which used log area in km2 as a moderator).
- COVID-period evaluations (2020 to 2021) flagged or excluded. Nested and sequential schemes (ULEZ steps, Milan) treated as non-independent.
- Drop Bogota (Pico y Placa) and Mexico City (Hoy No Circula): no bounded zone.

## Figures and tables (plan)

- Figure 1: effect against log relative coverage, two panels (charges: traffic; LEZs: NO2). Marker shape for design quality, error bars for area range, lines joining within-city contrasts (London central zone vs Western Extension; ULEZ 1 to 3; Milan Area C inside Area B). Ecopass vs Area C labelled as a price contrast at fixed size.
- Figure 2: slope chart of effect against years in operation for schemes with repeated measurements.
- Table 1: condensed inventory (area, coverage, start year, stringency, outcome, location, effect, design, source).
- Optional: PRISMA-style flow figure.

## Main reviewer risks and pre-emption

1. Apples and oranges, correlation only: separate panels, one outcome per type, state that the study is descriptive, lean on within-city contrasts.
2. Size standing in for stringency, timing, compliance: stringency in Table 1, correlations in SI, ULEZ 2023 null used openly.
3. Not replicable, too few cases: documented search with counts, database deposited with a DOI (Zenodo or OSF), polygon sources, analysable N vs inventory N. Gap: existing reviews (Chamberlain et al. 2023, Lancet Public Health; Holman, Harrison and Querol 2015, Atmospheric Environment) do not treat zone geometry as a variable.

## Notes from the evidence so far

- Glasgow: traffic stable, weekday NO2 down 9 to 13% at Hope Street (Shin et al. 2024, Findings, doi:10.32866/001c.123382). Residents exempt until June 2024. Use as an illustration of the fleet mechanism, not as proof that size matters.
- Madrid Central: peer-reviewed studies report NO2 reductions and positive spillover (Salas et al. 2021, TR-D 91, 102689; Lebrusan and Toutouh 2020, doi:10.1007/s11869-020-00938-z). Do not describe Madrid as ineffective.
- London congestion returned to pre-charge levels by about 2007 while traffic stayed lower (TfL 2008, grey literature; find a peer-reviewed source).

## Files

- data/Boundary_Size_Database_v2.xlsx: scheme inventory (46 schemes; Bogota and Mexico City moved to Excluded) with relative coverage, stringency and duration columns added. Extraction columns still blank.
- docs/findings_review_template.md: how published Findings syntheses are written.
