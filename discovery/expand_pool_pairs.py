from pathlib import Path
import json,csv,numpy as np,shutil
p=Path(__file__).resolve().parent
for n in ['discovery_pairs.tsv','rank_pair_order.json','fast_risks.tsv']:
 if not (p/('initial_'+n)).exists():shutil.copy2(p/n,p/('initial_'+n))
ol=json.loads((p/'oligos.json').read_text());z=np.load(p/'discovery_masks.npz');w=z['weights'];m=z['coverage'];e=z['exact'];rows=[]
for i,f in enumerate(ol):
 if f['side']!='F':continue
 for j,r in enumerate(ol):
  if r['side']!='R' or r['locus']!=f['locus']:continue
  rows.append(dict(F_id=f['id'],R_id=r['id'],F=f['sequence'],R=r['sequence'],left=f['left'],right=r['right'],reference_total=r['right']-f['left'],band=f['locus'],v4_local=f['locus']=='MiCucumber-v4opt',coverage=float(w[m[i]&m[j]].sum()),exact=float(w[e[i]&e[j]].sum()),degeneracy_sum=f['degeneracy']+r['degeneracy'],tm_delta=abs((f['tm_min']+f['tm_max']-r['tm_min']-r['tm_max'])/2)))
with (p/'discovery_pairs.tsv').open('w') as f:wr=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');wr.writeheader();wr.writerows(rows)
print('all same-locus cross-pairs',len(rows))
