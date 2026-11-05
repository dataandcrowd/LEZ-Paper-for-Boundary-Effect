# Does Zone Size Matter? (Transport Findings rapid review)

Rapid review of ex-post evaluations of urban congestion charges and low emission zones, asking how traffic and NO₂ effects differ by zone (boundary) size.

## Where to look first

| If you want to... | Open |
|---|---|
| Read or edit the paper | `output/manuscript/manuscript_body.md` (edit this), `output/manuscript/manuscript.docx` (built from it) |
| See the figures | `output/figures/` (Figures 1 to 3, Supplementary Figures S1 to S3) |
| Check what is left before submission | `output/notes/submission_todo.md` |
| Find the DOI of every included study, and the full texts still needed | `output/notes/doi_list.md` |
| Look at the data | `data/database/Boundary_Size_Database_v3.xlsx` |

## Folders

```
data/
  raw/          Source database (Congestion Charging Database, Rose)
  extraction/   Extracted effect estimates, zone areas and charge or compliance data
  curated/      Hand-curated tables: within-city boundary pairs (Figure 2), rule changes (Table S5) and inside-outside pairs (Figure 3, Table S8)
  database/     Combined workbook (schemes, effects, excluded schemes)
  reference/    Zone polygons, World Bank price data, search export
  literature/   Full-text PDFs used for checking (do not share publicly)
code/
  1 to 8        Analysis pipeline, run in order (see below)
  paths.py      Folder locations used by every script
  templates/    Supplementary Information template
  setup/        One-time scripts that built the extraction files and database (kept for the record)
output/
  manuscript/   Manuscript and Supplementary Information (Markdown and Word)
  figures/      Figures 1 to 3, Supplementary Figures S1 to S3
  tables/       Table 1
  analysis/     Intermediate analysis files and results.json
  notes/        Submission to-do list and search protocol
```

## Rebuilding everything

From the repository root:

```
sh code/run_all.sh
```

This runs, in order:

1. `1_build_analysis_rows.py` assigns each estimate to an analysis set, design tier and duration band.
2. `2_merge_and_analyse.py` joins zone areas and stringency, picks one headline estimate per scheme phase and writes `results.json`.
3. `3_figures_supplementary.py` draws Supplementary Figures S1 to S3 and writes Table 1.
4. `4_figures_main.py` draws Figures 1 to 3.
5. `5_make_table1.py` adds size categories to Table 1.
6. `6_city_evidence.py` lists every estimate by city (Supplementary Tables S13 and S14).
7. `7_make_si.py` builds the Supplementary Information from the template.
8. `8_build_manuscript.py` inserts Table 1 into the manuscript and builds the Word files (needs pandoc and python-docx), with 8 pt table text and landscape pages for the supplementary tables.

Requires Python 3 with pandas, numpy, scipy, matplotlib, openpyxl and adjustText (`pip install pandas numpy scipy matplotlib openpyxl adjustText`), and pandoc for the Word files.

The scripts in `code/setup/` were run once during data collection and still contain the paths of the original working environment. They are not part of `run_all.sh`.
