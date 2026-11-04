"""Task 4: Figure 1 (effect vs relative coverage, two panels), Figure 2 (effect vs years in
operation), Figure S1 (effect vs absolute zone area), Table 1 (inventory)."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from adjustText import adjust_text
from paths import ANALYSIS, FIGURES, TABLES
W = str(ANALYSIS); F = str(FIGURES); T = str(TABLES)
ds = pd.read_csv(f'{W}/analysis_dataset.csv'); dr = pd.read_csv(f'{W}/duration_rows.csv')
plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 9, 'axes.edgecolor': '#52514e',
                     'axes.labelcolor': '#0b0b0b', 'xtick.color': '#52514e', 'ytick.color': '#52514e',
                     'axes.spines.top': False, 'axes.spines.right': False})
BLUE, ORANGE, INK, MUTED, GRID = '#2a78d6', '#eb6834', '#0b0b0b', '#52514e', '#e6e5e1'

def panel(ax, g, colour, title, xcol, xmin, xmax, xlabel, joins):
    ax.axhline(0, color=MUTED, lw=0.8, zorder=1)
    ax.grid(axis='y', color=GRID, lw=0.6, zorder=0)
    texts = []
    for _, r in g.iterrows():
        x = r[xcol]
        if pd.isna(x): continue
        if r.Key == 'LON_LEZ08': x = x * 0.62  # nudge left: same area as ULEZ 2023, would be hidden
        lo, hi = r[xmin], r[xmax]
        if pd.notna(lo) and pd.notna(hi) and hi > lo:
            ax.plot([lo, hi], [r.Effect_pct] * 2, color=colour, lw=1.2, alpha=0.6, zorder=2)
        filled = r.Design_tier == 1
        marker = 's' if (r.Type == 'CC' and not r.Journal_evidence) else ('^' if r.Cars_covered == 'N' else 'o')
        ax.scatter(x, r.Effect_pct, s=46, marker=marker, facecolor=colour if filled else 'white',
                   edgecolor=colour, linewidth=1.6, zorder=4)
        if xcol == 'Coverage' and r.Key == 'LON_ULEZ23':
            ax.text(x * 1.12, r.Effect_pct + 1.3, r.Label, fontsize=7.5, color=INK, ha='right', zorder=5); continue
        if xcol == 'Coverage' and r.Key == 'LON_LEZ08':
            ax.annotate(r.Label, xy=(x, r.Effect_pct), xytext=(x * 0.9, r.Effect_pct + 5.0), fontsize=7.5, color=INK,
                        ha='right', arrowprops=dict(arrowstyle='-', color='#a8a7a2', lw=0.5), zorder=5); continue
        if xcol == 'Coverage' and r.Key == 'MIL_B':
            ax.annotate(r.Label, xy=(x, r.Effect_pct), xytext=(x * 1.12, r.Effect_pct - 2.3), fontsize=7.5, color=INK,
                        ha='left', arrowprops=dict(arrowstyle='-', color='#a8a7a2', lw=0.5), zorder=5); continue
        texts.append(ax.text(x, r.Effect_pct, r.Label, fontsize=7.5, color=INK, zorder=5))
    for a, b in joins:
        ra, rb = g[g.Key == a], g[g.Key == b]
        if len(ra) and len(rb):
            ax.annotate('', xy=(rb[xcol].iloc[0], rb.Effect_pct.iloc[0]), xytext=(ra[xcol].iloc[0], ra.Effect_pct.iloc[0]),
                        arrowprops=dict(arrowstyle='->', color=MUTED, lw=0.9, ls='--', shrinkA=5, shrinkB=5), zorder=3)
    if r.Type == 'LEZ' and xcol == 'Coverage': ax.set_ylim(-31, 6.5)
    ax.set_xscale('log'); ax.set_title(title, loc='left', fontsize=10, color=INK, fontweight='bold')
    ax.set_xlabel(xlabel)
    adjust_text(texts, ax=ax, expand=(1.15, 1.4), arrowprops=dict(arrowstyle='-', color='#a8a7a2', lw=0.5))

def fig_scatter(xcol, xmin, xmax, xlabel, fname, scale=1.0):
    d = ds.copy(); d[xcol] = d[xcol] * scale; d[xmin] = d[xmin] * scale; d[xmax] = d[xmax] * scale
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), sharey=False)
    cc = d[(d.Type == 'CC') & (d.Outcome == 'Traffic')]; lz = d[(d.Type == 'LEZ') & (d.Outcome == 'NO2')]
    panel(axes[0], cc, BLUE, 'A. Congestion charges: traffic', xcol, xmin, xmax, xlabel, [('LON_CC', 'LON_WEZ')])
    panel(axes[1], lz, ORANGE, 'B. Low emission zones: NO$_2$', xcol, xmin, xmax, xlabel, [('LON_ULEZ19', 'LON_ULEZ23')])
    axes[0].set_ylabel('Reported change (%)')
    axes[1].set_ylabel('Reported change (%)')
    from matplotlib.lines import Line2D
    h = [Line2D([], [], marker='o', ls='', mfc=MUTED, mec=MUTED, label='Control group or natural experiment'),
         Line2D([], [], marker='o', ls='', mfc='white', mec=MUTED, mew=1.6, label='Adjusted or raw before-after, or model'),
         Line2D([], [], marker='s', ls='', mfc='white', mec=MUTED, mew=1.6, label='Conference, council or non-indexed source (A)'),
         Line2D([], [], marker='^', ls='', mfc='white', mec=MUTED, mew=1.6, label='Private cars not covered (B)'),
         Line2D([], [], color=MUTED, lw=0.9, ls='--', label='Same city, boundary changed')]
    fig.legend(handles=h, loc='lower center', ncol=3, frameon=False, fontsize=8, bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.1, 1, 1)); fig.savefig(f'{F}/{fname}.png', dpi=300); fig.savefig(f'{F}/{fname}.pdf'); plt.close(fig)

fig_scatter('Coverage', 'Coverage_min', 'Coverage_max', 'Zone area as share of urban centre area (%, log scale)', 'figS1_effect_vs_coverage', scale=100)
fig_scatter('Zone_km2', 'Zone_min', 'Zone_max', 'Zone area (km$^2$, log scale)', 'figS2_effect_vs_area_km2')

# Figure 2: effect against years in operation
fig, ax = plt.subplots(figsize=(6.4, 4.4))
ax.axhline(0, color=MUTED, lw=0.8); ax.grid(axis='y', color=GRID, lw=0.6)
for k, g in dr.groupby('Key'):
    g = g.sort_values('Years'); c = BLUE if g.Type.iloc[0] == 'CC' else ORANGE
    filled = g.Design_tier.iloc[0] == 1
    ax.plot(g.Years, g.Effect_pct, color=c, lw=2, zorder=2)
    ax.scatter(g.Years, g.Effect_pct, s=40, facecolor=c if filled else 'white', edgecolor=c, linewidth=1.6, zorder=3)
    ax.text(g.Years.iloc[-1] + 0.12, g.Effect_pct.iloc[-1], g.Label.iloc[0], fontsize=8, va='center', color=INK)
ax.set_xlabel('Years in operation at measurement'); ax.set_ylabel('Reported change (%)')
ax.set_xlim(0, 7.2)
from matplotlib.lines import Line2D
h = [Line2D([], [], color=BLUE, lw=2, label='Congestion charge: traffic'),
     Line2D([], [], color=ORANGE, lw=2, label='Low emission zone: NO$_2$'),
     Line2D([], [], marker='o', ls='', mfc=MUTED, mec=MUTED, label='Control group or natural experiment'),
     Line2D([], [], marker='o', ls='', mfc='white', mec=MUTED, mew=1.6, label='Adjusted or raw before-after')]
ax.legend(handles=h, frameon=False, fontsize=8, loc='upper right')
fig.tight_layout(); fig.savefig(f'{F}/figS3_effect_vs_years.png', dpi=300); fig.savefig(f'{F}/figS3_effect_vs_years.pdf'); plt.close(fig)

# Table 1
t = ds.copy()
t['Zone (km2)'] = t.Zone_km2.map(lambda v: '' if pd.isna(v) else (f'{v:.2f}' if v < 1 else (f'{v:.1f}' if v < 100 else f'{v:,.0f}')))
t['Coverage (%)'] = (t.Coverage * 100).map(lambda v: '' if pd.isna(v) else f'{v:.1f}')
t['Effect (%)'] = t.Effect_pct.map(lambda v: f'{v:+.1f}'.replace('-', '\u2212') if v != 0 else '0.0')
t['Years'] = t.Years.map(lambda v: f'{v:.1f}')
t['Design'] = t.Design_tier.map({1: 'Control', 2: 'Adjusted before-after', 3: 'Before-after', 4: 'Model'})
unit = {'VAL': ' per hour', 'STO': ' per crossing', 'GOT': ' per crossing', 'OSL': ' per crossing', 'BGO': ' per crossing',
        'TRD': ' per crossing', 'DUR': ' per exit', 'SHF': ' (vans, taxis)', 'BRD': ' (vans, taxis)', 'MIL_ECO': ' (middle band)',
        'LON_LEZ08': ' (lorries)'}
t['Charge or fine at launch (2023 USD PPP)'] = [(f'{c:.0f}' + unit.get(k, '')) if pd.notna(c) else (f'fine {f:.0f}' if pd.notna(f) else '')
                                      for c, f, k in zip(t.Charge_usd, t.Fine_usd, t.Key)]
# Current (2026) charge or status, from data/extraction/current_charges_*.csv (local currency, checked November 2026)
from paths import EXTRACT
cur = pd.concat([pd.read_csv(EXTRACT / f) for f in ('current_charges_cc.csv', 'current_charges_lez.csv') if (EXTRACT / f).exists()] or [pd.DataFrame(columns=['Key'])])
def current(k):
    r = cur[cur.Key == k]
    if r.empty: return ''
    return str(r.iloc[0].Table_text)
t['Current charge or status (2026)'] = t.Key.map(current)
t['Compliant at launch (%)'] = t.Compliance_pct.map(lambda v: '' if pd.isna(v) else f'{v:.1f}'.rstrip('0').rstrip('.'))
names = {'London CC': 'London Congestion Charge', 'London WEZ': 'London Western Extension', 'London ULEZ (2019)': 'London ULEZ (2019, central London)',
         'London ULEZ expansion (2023)': 'London ULEZ expansion to all of London (2023)', 'London LEZ (HGV)': 'London LEZ (heavy vehicles)', 'Singapore ALS': 'Singapore',
         'Sheffield': 'Sheffield (no cars)', 'Bradford': 'Bradford (no cars)', 'Amsterdam (trucks)': 'Amsterdam (trucks only)'}
t['Scheme'] = t.Label.replace(names)
t['Type'] = t.Type.map({'CC': 'Charge', 'LEZ': 'LEZ'})
t = t.sort_values(['Type', 'Coverage'])
cols = ['Scheme', 'Type', 'Start_year', 'Zone (km2)', 'Coverage (%)', 'Effect (%)', 'Years', 'Design', 'Charge or fine at launch (2023 USD PPP)', 'Compliant at launch (%)', 'Current charge or status (2026)']
out = t[cols].rename(columns={'Start_year': 'Start'})
out.to_csv(f'{T}/table1.csv', index=False)
md = '| ' + ' | '.join(c.replace('km2', 'km\u00b2') for c in out.columns) + ' |\n|' + '---|' * len(out.columns) + '\n'
for _, r in out.iterrows():
    md += '| ' + ' | '.join('' if (isinstance(v, float) and pd.isna(v)) else str(int(v)) if isinstance(v, float) else str(v) for v in r) + ' |\n'
open(f'{T}/table1.md', 'w').write(md)
print(md)
