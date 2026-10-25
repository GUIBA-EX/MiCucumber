from pathlib import Path
import csv,json,math,zipfile,hashlib,re,collections
repo=Path(__file__).resolve().parents[1];p=repo/'results/taxon_optimization';read=lambda f:list(csv.DictReader(f.open()));pairs=read(p/'primer_pairs.csv');coords=read(repo/'results/current/binding_positions.csv');by=read(p/'by_order.csv');metrics=read(p/'verified_comparison.csv');assert len(pairs)==10
I=dict(A='A',C='C',G='G',T='T',R='AG',Y='CT',S='CG',W='AT',K='GT',M='AC',B='CGT',D='AGT',H='ACT',V='ACG',N='ACGT')
for r in pairs:
 group=[c for c in coords if c['region']==r['region']];assert len(group)==4
 for c in group:assert all(c[k]==r[k] for k in ['F_start','F_end','R_start','R_end'])
 for side in ['F','R']:
  q=r[side];assert len(q)==int(r[side+'_end'])-int(r[side+'_start'])+1;assert math.prod(len(I[c]) for c in q)==int(r['degeneracy_'+side])
 d=[x for x in by if x['name']==r['name']];assert len(d)==5 and next(x for x in d if x['order']=='Apodida')['covered_labels']=='0'
 m=next(x for x in metrics if x['name']==r['name']);assert math.isclose(sum(100*int(x['covered_labels'])/int(x['labels']) for x in d)/5,float(m['order_coverage_pct']),abs_tol=1e-8)
for t in read(p/'thermal.csv'):
 assert float(t['structure_max'])<55 and abs((float(t['F_tm_min'])+float(t['F_tm_max'])-float(t['R_tm_min'])-float(t['R_tm_max']))/2)<=5
v=json.loads((p/'verification.json').read_text());assert v['target_checks']==7020 and v['background_set_checks']==40 and v['disagreements']==0
for l in re.findall(r'\]\(([^)]+)\)',(p/'README.md').read_text()):assert (p/l).exists(),l
with zipfile.ZipFile(p/'reproduction_sources.zip') as z:
 assert z.testzip() is None
 h=json.loads((p/'input_manifest.json').read_text())
 for n,d in h.items():assert hashlib.sha256(z.read(n)).hexdigest()==d,n
print('PASS: ten candidates, fixed ordinary/A/B/D endpoints, five-order macro scores, thermal gates, independent checks, report links and frozen input hashes')

policy=json.loads((repo/'results/current/D_selection_policy.json').read_text())
for reg in ['S','M','L','XL']:
 eligible=[r for r in metrics if r['region']==reg and max(int(r['WC3']),int(r['GT2']))<=100 and max(int(r['strict_WC']),int(r['strict_GT']))<=20]
 best=max(eligible,key=lambda r:(round(float(r['order_coverage_pct']),8),-int(r['degeneracy_F'])-int(r['degeneracy_R']),float(r['order_exact_pct'])))
 assert policy['selected'][reg+'D']==best['name']
 current=next(r for r in read(repo/'sequences/primer_pairs.csv') if r['pair_name']==reg+'D')
 assert (current['F'],current['R'])==(best['F'],best['R'])
print('PASS: current four D assays reproduce the declared selection policy')
