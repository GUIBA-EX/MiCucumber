from pathlib import Path
import csv,json,collections,math,re
p=Path(__file__).resolve().parents[1]
def rows(f):return list(csv.DictReader(f.open()))
d=p/'results' if p.name=='MiLily' else p/'results/terminal_optimization'
h=collections.defaultdict(set)
for r in csv.DictReader((d/'independent_hits.tsv').open(),delimiter='\t'):
 if r['role']=='target' and r['model']=='WC':
  for k in ['exact','le2last3']:
   if r[k]=='1':h[r['name'],k].add(r['accession'])
co=rows(d/'binding_positions.csv');pairs=rows(d/'primer_pairs.csv');comp={x['scheme']:x for x in rows(d/'comparison.csv')};ab=rows(p/'results/ab_complementarity/summary.csv');search={x['region']:x for x in rows(p/'results/ab_complementarity/reselection.csv')}
for a in ab:
 reg=a['region'];g=[r for r in co if r['region']==reg];assert len(g)==4 and len({tuple(x[k] for k in ['F_start','F_end','R_start','R_end']) for x in g})==1
 for side in ['A','B']:
  assert float(a['coverage_'+side+'_unique'])+float(a['exact_'+side+'_unique'])>0
  other='B' if side=='A' else 'A'
  for mode,k in [('coverage','le2last3'),('exact','exact')]:
   if float(a[mode+'_'+side+'_unique'])>1e-8:assert h[reg+side,k]-h[reg+other,k]
 c=comp[reg+'A+'+reg+'B'];old=search[reg]
 for mode,col in [('coverage','coverage_pct'),('exact','exact_pct')]:
  assert math.isclose(float(c[col]),float(a[mode+'_union']),abs_tol=1e-8)
  assert math.isclose(float(c[col]),float(old[col]),abs_tol=1e-8)
  assert float(c[col])+1e-8>=float(old['previous_'+mode])
 assert int(c['WC3'])<=5 and int(c['GT2'])<=5
for f in ['README.md','README.zh-CN.md']:
 s=(p/f).read_text();assert s.startswith('![')
 for x in comp.values():
  line=next(l for l in s.splitlines() if l.startswith('| '+x['scheme']+' |'))
  assert f"{float(x['coverage_pct']):.2f}" in line and f"{float(x['exact_pct']):.2f}" in line
 if len(pairs)==16:
  for x in pairs:assert f"| {x['name']} | `{x['F']}` | `{x['R']}` |" in s
print('PASS: mutual A/B contribution, fixed coordinates, non-decreasing metrics, background gates, bilingual README values and sequences')
