"""Insert Table 1 into the manuscript text and build the Word files with pandoc.

Edit output/manuscript/manuscript_body.md, not manuscript.md (which is overwritten here).
"""
import shutil, subprocess
from paths import MANUSCRIPT, TABLES, ROOT

body = (MANUSCRIPT / 'manuscript_body.md').read_text()
(MANUSCRIPT / 'manuscript.md').write_text(body.replace('{TABLE1}', (TABLES / 'table1_rr.md').read_text()))
if shutil.which('pandoc'):
    for name in ('manuscript', 'supplementary'):
        subprocess.run(['pandoc', f'{name}.md', '-o', f'{name}.docx', f'--resource-path=.:{ROOT / "output"}'],
                       cwd=MANUSCRIPT, check=True)
    print('Built manuscript.docx and supplementary.docx')
else:
    print('pandoc not found: manuscript.md written, Word files not rebuilt')
