#!/bin/sh
# Rebuild every analysis output, figure, table and manuscript file from data/.
# Run from the repository root:  sh code/run_all.sh
set -e
cd "$(dirname "$0")"
for s in 1_build_analysis_rows 2_merge_and_analyse 3_figures_supplementary 4_figures_main 5_make_table1 6_make_si 7_build_manuscript; do
  echo "== $s"; python3 "$s.py"
done
