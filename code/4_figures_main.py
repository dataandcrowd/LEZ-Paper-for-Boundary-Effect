"""Rapid review figures.
Figure 1: headline effect by zone size category, congestion charges (traffic) and LEZs (NO2).
Figure 2: within-city changes to zone or rules (enlarged, rules changed, suspended or removed).
Figure 3: change inside and outside the zone where the same study reported both.
"""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from paths import ANALYSIS, CURATED, FIGURES
W = str(FIGURES)
plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 9, 'axes.edgecolor': '#52514e',
                     'axes.labelcolor': '#0b0b0b', 'xtick.color': '#52514e', 'ytick.color': '#52514e',
                     'axes.spines.top': False, 'axes.spines.right': False})
BLUE, ORANGE, INK, MUTED, GRID = '#2a78d6', '#eb6834', '#0b0b0b', '#52514e', '#e6e5e1'
NSZ = {'BERLIN', 'LON_LEZ08', 'LON_ULEZ23', 'MIL_B'}

ds = pd.read_csv(ANALYSIS / 'analysis_dataset.csv')
cats = ['Small (<10 km²)', 'Medium (10-50 km²)', 'Large (≥50 km²)']
short = {'Small (<10 km²)': 'Small\n(<10 km²)', 'Medium (10-50 km²)': 'Medium\n(10 to 50 km²)', 'Large (≥50 km²)': 'Large\n(≥50 km²)'}
# label offsets (points) for the not-significant diamonds, which sit close to zero in the large category
NS_OFF = {'BERLIN': ((-6, 15), 'right'), 'MIL_B': ((-6, -15), 'right'), 'LON_LEZ08': ((-4, -16), 'left'), 'LON_ULEZ23': ((-4, 16), 'left')}
from adjustText import adjust_text
fig, axes = plt.subplots(1, 2, figsize=(10, 4.9), gridspec_kw={'width_ratios': [2.3, 3.6]})
for ax, (t, o, col, title, clist) in zip(axes, [('CC', 'Traffic', BLUE, 'A. Congestion charges: traffic', cats[:2]),
                                               ('LEZ', 'NO2', ORANGE, 'B. Low emission zones: NO$_2$', cats)]):
    g = ds[(ds.Type == t) & (ds.Outcome == o) & ds.Size_category.notna() & (ds.Size_category != '')]
    ax.axhline(0, color=MUTED, lw=0.8, zorder=1); ax.grid(axis='y', color=GRID, lw=0.6, zorder=0)
    texts = []; ticklabs = []; px = []; py = []
    ncat = len(clist)
    for i, c in enumerate(clist):
        h = g[g.Size_category == c].sort_values('Zone_km2')  # left to right by zone area within each class
        mtxt = '' if h.empty else '\nmedian ' + f'{h.Effect_pct.median():+.0f}%'.replace('-', '−').replace('+0%', '0%')
        ticklabs.append(short[c] + f'\nn = {len(h)}' + mtxt)
        if h.empty: continue
        xs = i + (np.linspace(-0.3, 0.3, len(h)) if len(h) > 1 else np.array([0.0]))
        for x, (_, r) in zip(xs, h.iterrows()):
            mk = 'D' if r.Key in NSZ else 'o'
            ax.scatter(x, r.Effect_pct, s=46, marker=mk, facecolor=col if r.Design_tier == 1 else 'white',
                       edgecolor=col, linewidth=1.5, zorder=4)
            lab = r.Label.replace(' (trucks)', '').replace('London LEZ (HGV)', 'London LEZ (lorries)').replace('Singapore ALS', 'Singapore').replace('London CC', 'London').replace('London ULEZ (2019)', 'ULEZ (2019, central)').replace('London ULEZ expansion (2023)', 'ULEZ expansion (2023)')
            px.append(x); py.append(r.Effect_pct)
            if r.Key in NS_OFF:
                off, ha = NS_OFF[r.Key]
                ax.annotate(lab, (x, r.Effect_pct), xytext=off, textcoords='offset points', ha=ha, va='center', fontsize=7, color=MUTED, zorder=5,
                            arrowprops=dict(arrowstyle='-', color='#a8a7a2', lw=0.5, shrinkA=0, shrinkB=4))
            else:
                texts.append(ax.text(x, r.Effect_pct, lab, fontsize=7, color=MUTED, zorder=5))
    ax.set_xticks(range(ncat)); ax.set_xticklabels(ticklabs, fontsize=8)
    ax.set_xlim(-0.6, ncat - 0.4)
    ax.set_title(title, loc='left', fontsize=10, color=INK, fontweight='bold')
    ax.set_ylabel('Reported change inside zone (%)')
    adjust_text(texts, x=px, y=py, ax=ax, expand=(1.4, 2.0), only_move={'text': 'xy', 'static': 'xy', 'explode': 'xy', 'pull': 'xy'}, arrowprops=dict(arrowstyle='-', color='#a8a7a2', lw=0.5))
axes[1].set_ylim(-32, 6)
h = [     Line2D([], [], marker='o', ls='', mfc=MUTED, mec=MUTED, label='Control group or natural experiment'),
     Line2D([], [], marker='o', ls='', mfc='white', mec=MUTED, mew=1.6, label='Before-after or model'),
     Line2D([], [], marker='D', ls='', mfc='white', mec=MUTED, mew=1.4, label='Not significant (at 0 if no point estimate)')]
fig.legend(handles=h, loc='lower center', ncol=4, frameon=False, fontsize=8, bbox_to_anchor=(0.5, -0.01))
fig.tight_layout(rect=(0, 0.06, 1, 1)); fig.savefig(f'{W}/fig1_size_categories.png', dpi=300); fig.savefig(f'{W}/fig1_size_categories.pdf'); plt.close(fig)

# Figure 2: same city, different boundary size (traffic and NO2 only), one panel per city
bp = pd.read_csv(CURATED / 'boundary_pairs.csv')
titles = {1: 'A. London congestion charge\n(traffic)', 2: 'B. London Ultra Low Emission Zone\n(NO$_2$)', 3: 'C. Lisbon low emission zone\n(NO$_2$)'}
fig, axes = plt.subplots(1, 3, figsize=(9.2, 3.9), sharey=True)
for ax, (pair, g) in zip(axes, bp.groupby('Pair')):
    g = g.sort_values('Step'); col = BLUE if g.Outcome.iloc[0] == 'Traffic' else ORANGE
    ax.axhline(0, color=MUTED, lw=0.8, zorder=1); ax.grid(axis='y', color=GRID, lw=0.6, zorder=0)
    ax.annotate('', xy=(1, g.Effect_pct.iloc[1]), xytext=(0, g.Effect_pct.iloc[0]), zorder=2,
                arrowprops=dict(arrowstyle='-|>', color='#a8a7a2', lw=1.3, shrinkA=8, shrinkB=8))
    for x, (_, r) in enumerate(g.iterrows()):
        mk = 'D' if r.Not_significant == 'Y' else 'o'
        ax.scatter(x, r.Effect_pct, s=70, marker=mk, facecolor=col if r.Design_tier == 1 else 'white',
                   edgecolor=col, linewidth=1.8, zorder=4)
        v = f'{r.Effect_pct:+.0f}%'.replace('-', '\u2212') + (' (n.s.)' if r.Not_significant == 'Y' else '')
        ax.annotate(v, (x, r.Effect_pct), xytext=(10, 0), textcoords='offset points', va='center', fontsize=8.5, color=INK)
    ax.set_xticks([0, 1])
    ax.set_xticklabels([f"{r.Step_label}\n{r.Zone_km2:,.4g} km² ({r.Year})" for _, r in g.iterrows()], fontsize=7.6)
    ax.set_xlim(-0.45, 1.6); ax.set_title(titles[pair], loc='left', fontsize=9.5, color=INK, fontweight='bold')
axes[0].set_ylim(-26, 4); axes[0].set_ylabel('Reported change inside zone (%)')
h = [Line2D([], [], marker='o', ls='', mfc=MUTED, mec=MUTED, label='Control group'),
     Line2D([], [], marker='o', ls='', mfc='white', mec=MUTED, mew=1.6, label='Before-after'),
     Line2D([], [], marker='D', ls='', mfc=MUTED, mec=MUTED, label='Not significant')]
fig.legend(handles=h, frameon=False, fontsize=8, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.02))
fig.tight_layout(rect=(0, 0.06, 1, 1)); fig.savefig(f'{W}/fig2_boundary_size_within_city.png', dpi=300, bbox_inches='tight')
fig.savefig(f'{W}/fig2_boundary_size_within_city.pdf', bbox_inches='tight'); plt.close(fig)

# Figure 3: inside versus outside the zone, same study (spillover_pairs.csv from 2_merge_and_analyse.py)
sp = pd.read_csv(ANALYSIS / 'spillover_pairs.csv')
where = {'Bypass road': 'bypass road', 'Rest of city': 'rest of city', 'City-wide index': 'city-wide index',
         'Adjacent belt': 'adjacent area', 'Border strip': 'within 500 m of border'}
fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.0), sharex=True, gridspec_kw={'width_ratios': [4, 5]})
for ax, (t, col, title) in zip(axes, [('CC', BLUE, 'A. Congestion charges: traffic'), ('LEZ', ORANGE, 'B. Low emission zones: NO$_2$')]):
    g = sp[sp.Type == t].sort_values('Inside_pct', ascending=False).reset_index(drop=True)
    ax.axvline(0, color=MUTED, lw=0.8, zorder=1); ax.grid(axis='x', color=GRID, lw=0.6, zorder=0)
    labs = []
    for y, r in g.iterrows():
        fc = col if r.Design_tier == 1 else 'white'
        ax.plot([r.Inside_pct, r.Outside_pct], [y, y], color='#a8a7a2', lw=1.3, zorder=2)
        ax.scatter(r.Inside_pct, y, s=64, marker='o', facecolor=fc, edgecolor=col, linewidth=1.6, zorder=4)
        ax.scatter(r.Outside_pct, y, s=58, marker='s', facecolor=fc, edgecolor=col, linewidth=1.6, zorder=4)
        lo, hi = sorted([(r.Inside_pct, 'in'), (r.Outside_pct, 'out')])
        for (v, _), dx, ha in [(lo, -9, 'right'), (hi, 9, 'left')]:
            ax.annotate(f'{v:+.0f}%'.replace('-', '\u2212'), (v, y), xytext=(dx, 0), textcoords='offset points',
                        va='center', ha=ha, fontsize=8, color=INK, zorder=5)
        lab = r.Label.replace('London ULEZ (2019)', 'London ULEZ (2019, central)')
        labs.append(f'{lab}\noutside: {where[r.Outside_type]}')
    ax.set_yticks(range(len(g))); ax.set_yticklabels(labs, fontsize=7.8); ax.invert_yaxis()
    ax.set_ylim(len(g) - 0.4, -0.6)
    ax.set_title(title, loc='left', fontsize=10, color=INK, fontweight='bold')
    ax.set_xlabel('Reported change (%)')
axes[0].set_xlim(-46, 36)
h = [Line2D([], [], marker='o', ls='', mfc='#a8a7a2', mec=MUTED, label='Circle: inside zone'),
     Line2D([], [], marker='s', ls='', mfc='#a8a7a2', mec=MUTED, label='Square: outside zone'),
     Line2D([], [], marker='o', ls='', mfc=MUTED, mec=MUTED, label='Filled: control group'),
     Line2D([], [], marker='o', ls='', mfc='white', mec=MUTED, mew=1.6, label='Open: before-after')]
fig.legend(handles=h, frameon=False, fontsize=8, loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.02))
fig.tight_layout(rect=(0, 0.07, 1, 1)); fig.savefig(f'{W}/fig3_inside_outside.png', dpi=300, bbox_inches='tight')
fig.savefig(f'{W}/fig3_inside_outside.pdf', bbox_inches='tight'); plt.close(fig)
print('ok')
