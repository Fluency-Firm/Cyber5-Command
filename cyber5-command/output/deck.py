#!/usr/bin/env python3
"""Cyber5 Command leadership deck builder.

Usage:
    python deck.py spec.json out.pdf [--preview DIR]

Builds a 16:9 PDF from a JSON spec, so every deck has the same layout whichever
model or agency runs it. Needs matplotlib (and numpy). With --preview, it also
writes one PNG per slide to DIR so the slides can be checked by eye before sending.

Spec format:
{
  "source": "Meta Ads MCP · <account> · <attribution> · <run_at>",   # footer on every slide
  "brand": {"accent": "#2563eb", "accent_light": "#93c5fd", "font": "DejaVu Sans"},  # optional
  "slides": [ <slide>, ... ]          # at most 6
}

Every slide has "type", "title" (the finding, as a sentence) and optional "subtitle".
Slide types and their extra keys:
  stats    "stats": [{"value": "B", "label": "Grade", "tone": "accent|bad|warn|good|ink"}, ...] (2–4),
           "note": "short paragraph"
  hbars    "bars": [{"label": "Signal [30]", "value": 100}, ...], "max": 100, "line": 80,
           "thresholds": [80, 60]   # >= first: good, >= second: warn, else bad
  vbars    "categories": [...], "series": [{"name": "Share of spend", "values": [...]}, ...] (1–2),
           "unit": "%"
  twobars  "left": {"title": "...", "categories": [...], "values": [...]},
           "right": {...}, "unit": "%"
  heatmap  "rows": [...], "cols": [...], "values": [[...], ...], "outline": [[row, col], ...]
  lines    "categories": [...], "series": [{"name": "Actual", "values": [...], "dashed": false}, ...] (1–3),
           "unit": "$", "ticks": label every Nth category (default 1),
           "shade": [{"from": i, "to": j, "label": "..."}]   # e.g. a delivery gap
  table   "header": [...], "rows": [[...], ...], "widths": [fractions summing to about 1],
           "footnote": "optional line under the table"
Numbers must be the same ones shown in chat. This script never computes findings.
"""
import json, sys, os, textwrap

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]
    preview = sys.argv[sys.argv.index('--preview') + 1] if '--preview' in sys.argv else None
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker
    from matplotlib.backends.backend_pdf import PdfPages
    from matplotlib.patches import Rectangle
    import numpy as np

    b = spec.get('brand', {})
    INK, MUTED, GRID = '#1f2328', '#6b7280', '#e5e7eb'
    ACC, ACC2 = b.get('accent', '#2563eb'), b.get('accent_light', '#93c5fd')
    TONE = {'accent': ACC, 'bad': '#dc2626', 'warn': '#d97706', 'good': '#16a34a', 'ink': INK}
    plt.rcParams.update({'font.family': b.get('font', 'DejaVu Sans'), 'text.color': INK,
                         'xtick.color': MUTED, 'ytick.color': MUTED, 'axes.edgecolor': GRID})
    warnings = []
    slides = spec['slides']
    if len(slides) > 6:
        warnings.append(f'{len(slides)} slides; the limit is 6. Only the first 6 were built.')
        slides = slides[:6]
    esc = lambda s: str(s).replace('$', r'\$')

    def frame(s, i):
        f = plt.figure(figsize=(13.333, 7.5)); f.patch.set_facecolor('white')
        tl = textwrap.wrap(s['title'], 58)
        if len(tl) > 2: warnings.append(f'slide {i}: title runs to {len(tl)} lines; shorten it')
        f.text(0.05, 0.90, esc('\n'.join(tl[:3])), fontsize=24, weight='bold', va='top')
        y = 0.90 - 0.065 * min(len(tl), 3) - 0.01
        if s.get('subtitle'):
            f.text(0.05, y, esc('\n'.join(textwrap.wrap(s['subtitle'], 150))), fontsize=12, color=MUTED, va='top')
        f.text(0.05, 0.03, esc(spec.get('source', '')), fontsize=8.5, color=MUTED)
        return f

    def clean(ax, keep_left=False):
        ax.spines[['top', 'right'] + ([] if keep_left else ['left'])].set_visible(False)

    with PdfPages(out) as pdf:
        for i, s in enumerate(slides, 1):
            f = frame(s, i); t = s['type']
            if t == 'stats':
                st = s['stats']; w = 0.9 / len(st)
                for k, x in enumerate(st):
                    f.text(0.05 + k * w, 0.56, esc(x['value']), fontsize=46, weight='bold', color=TONE.get(x.get('tone', 'accent'), ACC))
                    f.text(0.05 + k * w, 0.49, esc('\n'.join(textwrap.wrap(x['label'], 28))), fontsize=12, color=MUTED, va='top')
                if s.get('note'):
                    f.text(0.05, 0.36, esc('\n'.join(textwrap.wrap(s['note'], 120))), fontsize=13, va='top')
            elif t == 'hbars':
                ax = f.add_axes([0.17, 0.12, 0.77, 0.58]); bars = s['bars'][::-1]
                th = s.get('thresholds', [80, 60]); mx = s.get('max', 100)
                cols = [TONE['good'] if v['value'] >= th[0] else TONE['warn'] if v['value'] >= th[1] else TONE['bad'] for v in bars]
                bb = ax.barh([v['label'] for v in bars], [v['value'] for v in bars], color=cols, height=0.55)
                if s.get('line') is not None: ax.axvline(s['line'], ls='--', color=MUTED, lw=1)
                ax.set_xlim(0, mx * 1.05)
                for r, v in zip(bb, bars): ax.text(v['value'] + mx * 0.01, r.get_y() + r.get_height() / 2, f"{v['value']:g}", va='center', fontsize=13, weight='bold')
                clean(ax, True); ax.tick_params(labelsize=13)
            elif t == 'vbars':
                ax = f.add_axes([0.08, 0.12, 0.86, 0.58]); cats = s['categories']; ser = s['series']; x = np.arange(len(cats))
                wd = 0.72 / len(ser); u = s.get('unit', '')
                for k, se in enumerate(ser):
                    bb = ax.bar(x + (k - (len(ser) - 1) / 2) * wd, se['values'], wd, color=[ACC2, ACC][k % 2] if len(ser) > 1 else ACC, label=se['name'])
                    for r, v in zip(bb, se['values']): ax.text(r.get_x() + r.get_width() / 2, v * 1.01, f'{v:g}{u}', ha='center', va='bottom', fontsize=11)
                ax.set_xticks(x, cats); ax.tick_params(labelsize=12); ax.set_yticks([]); clean(ax)
                if len(ser) > 1: ax.legend(frameon=False, fontsize=12, loc='upper left')
            elif t == 'twobars':
                u = s.get('unit', '')
                for k, side in enumerate(['left', 'right']):
                    d = s[side]; ax = f.add_axes([0.06 + k * 0.49, 0.14, 0.42, 0.52])
                    ax.bar(d['categories'], d['values'], color=ACC)
                    for j, v in enumerate(d['values']): ax.text(j, v * 1.02, f'{v:g}{u}', ha='center', va='bottom', fontsize=12, weight='bold')
                    ax.set_title(esc(d['title']), loc='left', fontsize=12, color=MUTED); ax.set_yticks([]); clean(ax); ax.tick_params(labelsize=11)
            elif t == 'heatmap':
                ax = f.add_axes([0.08, 0.14, 0.86, 0.56]); M = np.array(s['values'], dtype=float)
                ax.imshow(M, aspect='auto', cmap='Blues'); hi = np.nanmax(M)
                for r in range(M.shape[0]):
                    for c in range(M.shape[1]):
                        ax.text(c, r, f'{M[r, c]:.0f}', ha='center', va='center', fontsize=9, color='white' if M[r, c] > hi * 0.6 else INK)
                for r, c in s.get('outline', []): ax.add_patch(Rectangle((c - 0.5, r - 0.5), 1, 1, fill=False, ec=TONE['bad'], lw=2))
                ax.set_yticks(range(len(s['rows'])), s['rows']); ax.set_xticks(range(len(s['cols'])), s['cols']); ax.tick_params(labelsize=11)
            elif t == 'lines':
                ax = f.add_axes([0.09, 0.14, 0.80, 0.54]); cats = s['categories']; x = np.arange(len(cats)); u = s.get('unit', '')
                fmt = lambda v: f'${v:,.0f}' if u == '$' else f'{v:,.0f}{u}'
                for sh in s.get('shade', []):
                    ax.axvspan(sh['from'] - 0.5, sh['to'] + 0.5, color=TONE['bad'], alpha=0.12, lw=0)
                    ax.text((sh['from'] + sh['to']) / 2, 1.01, esc(sh.get('label', '')), transform=ax.get_xaxis_transform(), ha='center', va='bottom', fontsize=10, color=TONE['bad'])
                cl = [ACC, MUTED, ACC2]
                for k, se in enumerate(s['series'][:3]):
                    ax.plot(x, se['values'], color=cl[k], lw=2.4 if k == 0 else 1.8, ls='--' if se.get('dashed') else '-', label=esc(se['name']))
                    ax.annotate(esc(fmt(se['values'][-1])), (x[-1], se['values'][-1]), xytext=(6, 0), textcoords='offset points', va='center', fontsize=11, color=cl[k], weight='bold', annotation_clip=False)
                n = int(s.get('ticks', 1)); ax.set_xticks(x[::n], [esc(c) for c in cats[::n]]); ax.tick_params(labelsize=10)
                ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: esc(f'${v/1000:,.0f}K' if u == '$' else f'{v:,.0f}{u}')))
                ax.set_xlim(-0.5, len(cats) - 0.5); clean(ax, True); ax.grid(axis='y', color=GRID, lw=0.8)
                ax.legend(frameon=False, fontsize=11, loc='upper left')
            elif t == 'table':
                widths = s['widths']; fs = 11
                chars = [max(8, int(w * 118)) for w in widths]
                rows = [['\n'.join(textwrap.wrap(esc(c), n)) or '' for c, n in zip(r, chars)] for r in s['rows']]
                lines = [max(c.count('\n') + 1 for c in r) for r in rows]
                total = 1 + sum(lines)
                if total > 14: warnings.append(f'slide {i}: table needs {total} lines; cut rows or text')
                ax = f.add_axes([0.05, 0.12, 0.9, 0.62]); ax.axis('off')
                tb = ax.table(cellText=rows, colLabels=[esc(h) for h in s['header']], colWidths=widths, loc='upper left', cellLoc='left')
                tb.auto_set_font_size(False); tb.set_fontsize(fs)
                for (r, c), cell in tb.get_celld().items():
                    cell.set_edgecolor(GRID); cell.PAD = 0.02
                    cell.set_height(0.09 if r == 0 else 0.08 * lines[r - 1])
                    if r == 0: cell.set_text_props(weight='bold'); cell.set_facecolor('#f3f4f6')
                if s.get('footnote'): f.text(0.05, 0.08, esc(s['footnote']), fontsize=11, color=MUTED)
            else:
                warnings.append(f'slide {i}: unknown type "{t}"; left blank')
            pdf.savefig(f)
            if preview:
                os.makedirs(preview, exist_ok=True); f.savefig(os.path.join(preview, f'slide-{i}.png'), dpi=60)
            plt.close(f)
    print(f'built {out} ({len(slides)} slides)')
    for w in warnings: print('WARNING:', w)

if __name__ == '__main__':
    main()
