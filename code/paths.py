"""Folder locations used by every script. Paths are relative to the repository root."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
EXTRACT = ROOT / 'data' / 'extraction'      # effect, area and stringency extraction files
CURATED = ROOT / 'data' / 'curated'         # hand-curated within-city tables
DATABASE = ROOT / 'data' / 'database'
ANALYSIS = ROOT / 'output' / 'analysis'     # intermediate analysis files and results.json
FIGURES = ROOT / 'output' / 'figures'
TABLES = ROOT / 'output' / 'tables'
MANUSCRIPT = ROOT / 'output' / 'manuscript'
TEMPLATES = ROOT / 'code' / 'templates'
for p in (ANALYSIS, FIGURES, TABLES, MANUSCRIPT):
    p.mkdir(parents=True, exist_ok=True)
