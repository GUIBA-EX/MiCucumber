"""Draw verified paired binding templates. Grey cells explicitly mean no hit."""
from pathlib import Path
import csv,html
p=Path(__file__).resolve().parent
I=dict(A='A',C='C',G='G',T='T',R='AG',Y='CT',S='CG',W='AT',K='GT',M='AC',B='CGT',D='AGT',H='ACT',V='ACG',N='ACGT')
def read(n):return list(csv.DictReader((p/n).open()))
for pair in read('primer_pairs.csv'):
 rows=[r for r in read('representative_templates.csv') if r['name']==pair['name']];W,H=1200,700;s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="100%" height="100%" rx="18" fill="#f7fbff"/>','<g font-family="Arial,sans-serif" fill="#203c4d">',f'<text x="24" y="35" font-size="24">MiCucumber · {pair["name"]} · verified base matching</text>','<text x="24" y="63" font-size="13">Blue: IUPAC-compatible | Orange: mismatch | Grey: no paired hit | Box: terminal 3 nt</text>']
 for k,side in enumerate(['F','R']):
  top=105+k*280;q=pair[side];s.append(f'<text x="24" y="{top}" font-size="17">{side} 5′ → 3′ · AB525437.1 {pair[side+"_start"]}–{pair[side+"_end"]} · {pair["degeneracy_"+side]} variants</text>')
  rr=[dict(label='Primer',template=q)]+[dict(label=r['order']+' · '+(r['organism'] if r['accession'] else 'no covered reference'),template=r[side+'_template']) for r in rows]
  for j,r in enumerate(rr):
   y=top+25+j*27;s.append(f'<text x="24" y="{y+18}" font-size="12">{html.escape(r["label"])}</text>')
   for i,n in enumerate(q):
    t=r['template'][i] if r['template'] else '–';col='#d6edf4' if j==0 or t in I[n] else '#e1e6ea' if not r['template'] else '#ffd0a3';x=550+i*20;s.append(f'<rect x="{x}" y="{y}" width="19" height="25" fill="{col}"/><text x="{x+5}" y="{y+18}" font-size="15">{t}</text>')
  s.append(f'<rect x="{549+(len(q)-3)*20}" y="{top+24}" width="61" height="163" fill="none" stroke="#203c4d" stroke-width="2"/>')
 s+=['<text x="24" y="655" font-size="12">Representative rows use raw templates with verified paired hits; blank orders have no matched template.</text>','<text x="24" y="677" font-size="12">Order labels follow the frozen panel. Representative rows do not summarize all taxa or all within-label variants.</text>','</g></svg>'];(p/f'base_matching_{pair["name"]}.svg').write_text('\n'.join(s)+'\n')
print('Generated verified base matching for ten candidates')
