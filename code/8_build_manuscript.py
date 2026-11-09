"""Insert Table 1 into the manuscript text and build the Word files with pandoc.

Edit output/manuscript/manuscript_body.md, not manuscript.md (which is overwritten here).
"""
import shutil, subprocess
from paths import MANUSCRIPT, TABLES, ROOT

body = (MANUSCRIPT / 'manuscript_body.md').read_text()
(MANUSCRIPT / 'manuscript.md').write_text(body.replace('{TABLE1}', (TABLES / 'table1_cc.md').read_text()).replace('{TABLE2}', (TABLES / 'table2_lez.md').read_text()).replace('{TABLE3}', (TABLES / 'table3_removals.md').read_text()))
if shutil.which('pandoc'):
    for name in ('manuscript', 'supplementary'):
        subprocess.run(['pandoc', f'{name}.md', '-o', f'{name}.docx', f'--resource-path=.:{ROOT / "output"}'],
                       cwd=MANUSCRIPT, check=True)
    # Word post-processing: small table font, landscape pages for the supplementary tables
    from docx import Document
    from docx.shared import Pt
    from docx.enum.section import WD_ORIENT
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    for name in ('manuscript', 'supplementary'):
        d = Document(MANUSCRIPT / f'{name}.docx')
        for t in d.tables:
            for row in t.rows:
                for cell in row.cells:
                    for par in cell.paragraphs:
                        par.paragraph_format.space_after = Pt(0)
                        for run in par.runs: run.font.size = Pt(8)
        if name == 'supplementary':
            def section_break(par, landscape):
                # start a new section at this paragraph
                pPr = par._p.get_or_add_pPr(); sect = OxmlElement('w:sectPr')
                pg = OxmlElement('w:pgSz')
                if landscape: pg.set(qn('w:w'), '16838'); pg.set(qn('w:h'), '11906'); pg.set(qn('w:orient'), 'landscape')
                else: pg.set(qn('w:w'), '11906'); pg.set(qn('w:h'), '16838')
                mar = OxmlElement('w:pgMar')
                for k in ('top', 'right', 'bottom', 'left'): mar.set(qn('w:' + k), '1134')
                for k in ('header', 'footer'): mar.set(qn('w:' + k), '709')
                mar.set(qn('w:gutter'), '0')
                sect.append(pg); sect.append(mar); pPr.append(sect)
            paras = d.paragraphs
            first_table = next(i for i, p in enumerate(paras) if p.text.startswith('Table S1.'))
            first_fig = next(i for i, p in enumerate(paras) if p.text.startswith('Figure S1') or p.text.startswith('# Figure S1'))
            # the paragraph before a section start carries the sectPr of the preceding section
            section_break(paras[first_table - 1], landscape=False)
            section_break(paras[first_fig - 1], landscape=True)
            # final section (document level) stays portrait; set its size explicitly
            from docx.shared import Mm
            sec = d.sections[-1]; sec.orientation = WD_ORIENT.PORTRAIT; sec.page_width = Mm(210); sec.page_height = Mm(297)
        d.save(MANUSCRIPT / f'{name}.docx')
    print('Built manuscript.docx and supplementary.docx')
else:
    print('pandoc not found: manuscript.md written, Word files not rebuilt')
