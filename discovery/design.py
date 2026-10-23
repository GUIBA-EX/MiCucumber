"""Taxon-balanced aligned discovery; final whole-sequence validation is separate."""
from pathlib import Path
import sys,json,csv,collections,itertools,functools,hashlib,re,time
import numpy as np
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Data.IUPACData import ambiguous_dna_values as I
p=Path(__file__).resolve().parent

import primer3
meta={r['accession']:r for r in csv.DictReader((p/'metadata.tsv').open(),delimiter='\t')}
al={r.id.removeprefix('_R_'):str(r.seq).upper() for r in SeqIO.parse(p/'full_aligned.fasta','fasta')}
ref='AB525437.1';coords=[i for i,c in enumerate(al[ref]) if c!='-']
def named(s):
 t=s.split();return len(t)==2 and t[0][0].isupper() and t[1].islower() and t[1].isalpha() and t[1] not in ['sp','cf','aff']
ids=[k for k in al if named(meta[k]['organism'])];ct=collections.Counter(meta[k]['organism'] for k in ids);weights=np.array([1/ct[meta[k]['organism']]/len(ct) for k in ids])
(p/'discovery_panel.json').write_text(json.dumps(dict(reference=ref,ids=ids,n_labels=len(ct),weighting='equal label, then unique full-sequence haplotypes',held_out=False),indent=2))
inv={frozenset(v):k for k,v in I.items() if k!='X'}
def rc(s):return str(Seq(s).reverse_complement())
@functools.lru_cache(None)
def thermal(q):
 vs=[''.join(x) for x in itertools.product(*(I[c] for c in q))]
 tm=[primer3.calc_tm(s,mv_conc=50,dv_conc=1.5,dntp_conc=.6,dna_conc=50) for s in vs]
 if min(tm)<50 or max(tm)>73 or max(tm)-min(tm)>10:return None
 hp=max(primer3.calc_hairpin(s,mv_conc=50,dv_conc=1.5,dntp_conc=.6,dna_conc=50).tm for s in vs)
 if hp>55:return None
 return dict(tm_min=min(tm),tm_max=max(tm),hairpin_max=hp)
oligos=[];masks=[];exact=[];seen=set();reject=collections.Counter()
for side in ['F','R']:
 for anchor in range(650,1351,3):
  for L in [20,22,24,26,28,30]:
   l,r=(anchor,anchor+L) if side=='F' else (anchor-L,anchor)
   ts=[al[k][coords[l]:coords[r-1]+1].replace('-','') for k in ids]
   if side=='R':ts=[rc(t) for t in ts]
   valid=np.array([len(t)==L and set(t)<=set('ACGT') for t in ts])
   support=weights[valid].sum()
   if support<.75:reject['alignment_support']+=1;continue
   mat=np.array([list(t) if v else list('N'*L) for t,v in zip(ts,valid)])
   freqs=np.array([[weights[(mat[:,i]==x)&valid].sum()/support for x in 'ACGT'] for i in range(L)])
   for threshold in [.03,.07,.12,.20,.30]:
    bs=[{x for x,v in zip('ACGT',row) if v>=threshold} or {'ACGT'[row.argmax()]} for row in freqs]
    for lock in [0,3]:
     bb=[set(x) for x in bs]
     if lock:
      for j in range(L-lock,L):bb[j]={'ACGT'[freqs[j].argmax()]}
     q=''.join(inv[frozenset(x)] for x in bb)
     if (side,q,l,r) in seen:continue
     seen.add((side,q,l,r));deg=int(np.prod([len(x) for x in bb]))
     if deg>32:reject['degeneracy']+=1;continue
     if any(all('A' in x for x in bb[i:i+4]) for i in range(L-3)):reject['polyA']+=1;continue
     mis=np.column_stack([~np.isin(mat[:,j],list(I[c])) for j,c in enumerate(q)])
     m=valid&(mis.sum(1)<=2)&~mis[:,-3:].any(1);e=valid&~mis.any(1)
     coverage=float(weights[m].sum())
     if coverage<.40:reject['coverage']+=1;continue
     th=thermal(q)
     if th is None:reject['thermal']+=1;continue
     key=f'{side}{len(oligos):05d}';oligos.append(dict(id=key,side=side,sequence=q,left=l,right=r,degeneracy=deg,coverage=coverage,exact=float(weights[e].sum()),**th));masks.append(m);exact.append(e)
  if (anchor-650)%150==0:print(side,anchor,'retained',len(oligos),'thermal_evaluated',thermal.cache_info().misses,flush=True)
 print('SIDE DONE',side,len(oligos),flush=True)
(p/'oligos.json').write_text(json.dumps(oligos,indent=2));np.savez_compressed(p/'discovery_masks.npz',coverage=np.array(masks),exact=np.array(exact),weights=weights)
# Rank all pairs at homologous loci. No pooling, every pair is explicit.
F=[(i,x) for i,x in enumerate(oligos) if x['side']=='F'];R=[(i,x) for i,x in enumerate(oligos) if x['side']=='R'];rows=[]
for i,f in F:
 for j,r in R:
  total=r['right']-f['left']
  if not 150<=total<=500 or r['left']<=f['right']:continue
  delta=abs((f['tm_min']+f['tm_max']-r['tm_min']-r['tm_max'])/2)
  if delta>5:continue
  cov=float(weights[masks[i]&masks[j]].sum())
  if cov<.35:continue
  band='short' if total<250 else 'medium' if total<350 else 'long'
  v4=abs(f['left']-956)<=18 and abs(r['right']-1159)<=18
  rows.append(dict(F_id=f['id'],R_id=r['id'],F=f['sequence'],R=r['sequence'],left=f['left'],right=r['right'],reference_total=total,band=band,v4_local=v4,coverage=cov,exact=float(weights[exact[i]&exact[j]].sum()),degeneracy_sum=f['degeneracy']+r['degeneracy'],tm_delta=delta))
rows.sort(key=lambda x:(-x['coverage'],-x['exact'],x['degeneracy_sum'],x['tm_delta']))
with (p/'discovery_pairs.tsv').open('w') as out:
 w=csv.DictWriter(out,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
summary=dict(oligos=len(oligos),pairs=len(rows),bands=dict(collections.Counter(r['band'] for r in rows)),v4_pairs=sum(r['v4_local'] for r in rows),rejections=dict(reject),status='discovery_only_not_specificity_validated')
(p/'design_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary),flush=True)
