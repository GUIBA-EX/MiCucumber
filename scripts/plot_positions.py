"""Render current reference coordinates directly from the canonical CSV."""
from pathlib import Path
import csv,html
P=Path(__file__).resolve().parents[1];rows=list(csv.DictReader((P/'results/current/binding_positions.csv').open()));W=1450;H=190+len(rows)*57
colors=dict(XS='#65a544',S='#13aaba',M='#d18d15',L='#2779ef',XL='#922bde');xx=lambda n:160+(int(n)-750)*2.35
s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="100%" height="100%" fill="#f7fbff"/>','<g font-family="Arial,sans-serif" fill="#203c4d">','<text x="30" y="38" font-size="26">MiCucumber · current binding positions</text>','<text x="30" y="67" font-size="15">AB525437.1 · extracted ungapped 16S · 1-based inclusive · spans include primers</text>']
for n in range(750,1251,50):
 x=xx(n);s.extend([f'<line x1="{x}" x2="{x}" y1="95" y2="{H-85}" stroke="#dce8ee"/>',f'<text x="{x}" y="{H-60}" text-anchor="middle" font-size="14">{n}</text>'])
for j,r in enumerate(rows):
 y=115+57*j;c=colors[r['region']];fs,fe,rs,re=[int(r[k]) for k in ['F_start','F_end','R_start','R_end']]
 s.extend([f'<text x="30" y="{y+6}" font-size="19" fill="{c}">{html.escape(r["name"])}</text>',f'<line x1="{xx(fe)}" x2="{xx(rs)}" y1="{y}" y2="{y}" stroke="{c}" stroke-width="3" opacity=".4"/>'])
 for a,b in [(fs,fe),(re,rs)]:
  d=1 if b>a else -1;x1,x2=xx(a),xx(b);s.append(f'<path d="M{x1},{y} H{x2}" stroke="{c}" stroke-width="7"/><path d="M{x2-8*d},{y-7} L{x2},{y} L{x2-8*d},{y+7}" fill="none" stroke="{c}" stroke-width="3"/>')
 s.extend([f'<text x="{(xx(fe)+xx(rs))/2}" y="{y-9}" text-anchor="middle" font-size="14">{r["reference_span_bp"]} bp</text>',f'<text x="{xx(fs)}" y="{y+23}" font-size="12">F {fs}–{fe}</text>',f'<text x="{xx(re)}" y="{y+23}" text-anchor="end" font-size="12">R {rs}–{re}</text>'])
s+=['<text x="30" y="'+str(H-25)+'" font-size="14">XS is a single fixed assay. S–XL ordinary/A/B/D share coordinates within each region. Product lengths vary among taxa.</text>','</g></svg>'];(P/'figures/binding_positions.svg').write_text('\n'.join(s)+'\n')
