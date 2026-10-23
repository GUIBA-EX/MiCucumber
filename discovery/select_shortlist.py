from pathlib import Path
import csv,json,collections
p=Path(__file__).resolve().parent
rows=json.loads((p/'rank_pair_order.json').read_text());risk=list(csv.DictReader((p/'fast_risks.tsv').open(),delimiter='\t'));assert len(rows)==len(risk)
for i,(r,a) in enumerate(zip(rows,risk)):
 assert int(a['index'])==i
 r.update({k:int(v) for k,v in a.items() if k!='index'});r['strict_gate']=r['WC_le3']==r['GT_le2']==0
with (p/'screened_pairs_fast.tsv').open('w') as f:
 fields=sorted(set().union(*(r.keys() for r in rows)));w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(rows)
sel=[];summary={}
for group in ['v4_local','short','medium','long']:
 rr=[r for r in rows if r['band']!='baseline' and (r['v4_local']=='True' if group=='v4_local' else r['band']==group)]
 good=[r for r in rr if r['strict_gate']];pool=good or rr
 best=max(float(r['coverage']) for r in pool)
 rankings=[sorted(pool,key=lambda r:(r['WC_le3']+r['GT_le2'],-float(r['coverage']),r['WC_le4'],-float(r['exact']),int(r['degeneracy_sum']))),sorted([r for r in pool if float(r['coverage'])>=best-.10],key=lambda r:(r['WC_le3']+r['GT_le2'],r['WC_le4'],-float(r['coverage']),int(r['degeneracy_sum'])))]
 chosen=[]
 for rank in rankings:
  n=0
  for r in rank:
   if any(r['F']==s['F'] and r['R']==s['R'] for s in chosen):continue
   chosen.append(r);n+=1
   if n==4:break
 for j,r in enumerate(chosen,1):sel.append(dict(r,name=f'MC_{group}_{j}',group=group))
 summary[group]=dict(n_pairs=len(rr),n_strict_pass=len(good),best_discovery_coverage=best,shortlist=len(chosen))
(p/'shortlist_fast.json').write_text(json.dumps(sel,indent=2));(p/'shortlist_summary.json').write_text(json.dumps(summary,indent=2));(p/'baseline_risks.json').write_text(json.dumps([r for r in rows if r['band']=='baseline'],indent=2));print(json.dumps(summary,indent=2))
