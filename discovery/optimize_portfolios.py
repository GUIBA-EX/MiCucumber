from pathlib import Path
import json,csv,itertools,functools,collections
import numpy as np
from scan_core import database
p=Path(__file__).resolve().parent
ol=json.loads((p/'oligos.json').read_text());by={x['id']:x for x in ol};index={x['id']:i for i,x in enumerate(ol)};z=np.load(p/'discovery_masks.npz');m=z['coverage'];w=z['weights'];rows=json.loads((p/'rank_pair_order.json').read_text());risks=list(csv.DictReader((p/'fast_risks.tsv').open(),delimiter='\t'));assert len(rows)==len(risks)
for r,a in zip(rows,risks):r.update({k:int(v) for k,v in a.items() if k!='index'})
lookup={(r['F_id'],r['R_id']):r for r in rows};db=database(p/'background.fasta');refs=db[3]
@functools.lru_cache(None)
def hits(k):return json.loads((p/'background_hits'/f'{k}.json').read_text())['hits']
@functools.lru_cache(None)
def residual(F,R,model):
 row=lookup[F,R];threshold=3 if model=='WC' else 2
 if row['WC_le3' if model=='WC' else 'GT_le2']==0:return frozenset()
 fh=hits(F)[model];rh=hits(R)[model];found=set()
 for rec in fh.keys()&rh.keys():
  for fp,fm,f5,fa in fh[rec]:
   if fa or fm>threshold:continue
   for rp,rm,r5,ra in rh[rec]:
    if ra or rm>threshold or not 0<=rp-fp-len(by[F]['sequence'])<=1000:continue
    found.update(refs[int(rec)]['accessions'])
 assert len(found)==row['WC_le3' if model=='WC' else 'GT_le2']
 return frozenset(found)
def cfg(pairs,mode):
 Fs=sorted({a for a,b in pairs});Rs=sorted({b for a,b in pairs});allowed=list(itertools.product(Fs,Rs)) if mode=='pool' else sorted(set(pairs))
 mask=np.zeros(len(w),dtype=bool)
 for a,b in allowed:mask|=m[index[a]]&m[index[b]]
 return Fs,Rs,allowed,mask
def assess(pairs,mode,budget):
 Fs,Rs,allowed,mask=cfg(pairs,mode)
 if len(Fs)>4 or len(Rs)>4:return None
 if mode=='pool':
  mids=[(by[k]['tm_min']+by[k]['tm_max'])/2 for k in Fs+Rs]
  if max(mids)-min(mids)>8:return None
 for a,b in allowed:
  r=lookup[a,b]
  if r['WC_le3']>budget or r['GT_le2']>budget:return None
 counts={model:set().union(*(residual(a,b,model) for a,b in allowed)) for model in ['WC','GT']}
 if any(len(v)>budget for v in counts.values()):return None
 return dict(F_ids=Fs,R_ids=Rs,allowed_pairs=allowed,component_pairs=sorted(set(pairs)),coverage=float(w[mask].sum()),WC3_accessions=sorted(counts['WC']),GT2_accessions=sorted(counts['GT']),WC4_sum_upper_bound=sum(lookup[x]['WC_le4'] for x in allowed),total_degeneracy=sum(by[k]['degeneracy'] for k in Fs+Rs))
solutions=[]
for group in sorted({r['band'] for r in rows}):
 for budget in [0,5]:
  cand=[r for r in rows if r['band']==group and r['WC_le3']<=budget and r['GT_le2']<=budget and float(r['tm_delta'])<=5 and float(r['coverage'])>=.005];cand.sort(key=lambda r:(-float(r['coverage']),r['WC_le4'],r['degeneracy_sum']))
  for mode in ['separate','pool']:
   trajectories=[]
   # Three distinct seed masks; deterministic greedy extension, not global optimum.
   seeds=[];seen_masks=set()
   for r in cand:
    sig=(m[index[r['F_id']]]&m[index[r['R_id']]]).tobytes()
    if sig in seen_masks:continue
    seeds.append(r);seen_masks.add(sig)
    if len(seeds)==3:break
   for seed in seeds:
    pairs=[(seed['F_id'],seed['R_id'])];current=assess(pairs,mode,budget)
    if current is None:continue
    trajectory=[current]
    for size in range(2,5):
     ranked=[]
     for r in cand:
      pair=(r['F_id'],r['R_id'])
      if pair in pairs:continue
      _,_,_,mask=cfg(pairs+[pair],mode);score=float(w[mask].sum())
      if score<=current['coverage']+1e-9:continue
      ranked.append((-score,r['WC_le4'],r['degeneracy_sum'],pair))
     ranked.sort();best=None
     for _,_,_,pair in ranked:
      trial=assess(pairs+[pair],mode,budget)
      if trial is not None:best=trial;pairs.append(pair);break
     if best is None:break
     current=best;trajectory.append(current)
    trajectories.append(trajectory)
   if not trajectories:continue
   for count in range(1,5):
    options=[t[min(count,len(t))-1] for t in trajectories];best=min(options,key=lambda x:(-x['coverage'],len(x['WC3_accessions'])+len(x['GT2_accessions']),x['WC4_sum_upper_bound'],x['total_degeneracy']))
    solutions.append(dict(best,locus=group,mode=mode,budget_per_model=budget,max_component_pairs=count))
   print(group,budget,mode,solutions[-1]['coverage'],solutions[-1]['F_ids'],solutions[-1]['R_ids'],flush=True)
(p/'portfolio_search.json').write_text(json.dumps(solutions,indent=2));print('DONE',len(solutions),flush=True)
