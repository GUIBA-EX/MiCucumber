"""Local length/degeneracy refinement of promising v4 R binding site; explicit pairs."""
from pathlib import Path
import json,csv,itertools,sys,functools
import numpy as np
from Bio import SeqIO
from Bio.Data.IUPACData import ambiguous_dna_values as I
from scan_core import rc,database,flexible_hits
p=Path(__file__).resolve().parent

import primer3
al={r.id.removeprefix('_R_'):str(r.seq).upper() for r in SeqIO.parse(p/'full_aligned.fasta','fasta')};panel=json.loads((p/'discovery_panel.json').read_text());ids=panel['ids'];coords=[i for i,c in enumerate(al[panel['reference']]) if c!='-'];weights=np.load(p/'discovery_masks.npz')['weights'];inv={frozenset(v):k for k,v in I.items() if k!='X'}
old=json.loads((p/'oligos.json').read_text());lookup={x['id']:x for x in old};short=[s for s in json.loads((p/'shortlist_fast.json').read_text()) if s['group']=='v4_local'];Fids=sorted({s['F_id'] for s in short});Fmask={x['id']:np.load(p/'discovery_masks.npz')['coverage'][i] for i,x in enumerate(old) if x['id'] in Fids};db=database(p/'background.fasta');cache={k:json.loads((p/'background_hits'/f'{k}.json').read_text()) for k in Fids};out=[];ol=[];seen=set()
@functools.lru_cache(None)
def thermo(q):
 vs=[''.join(v) for v in itertools.product(*(I[c] for c in q))];ts=[primer3.calc_tm(v,mv_conc=50,dv_conc=1.5,dntp_conc=.6,dna_conc=50) for v in vs]
 if min(ts)<50 or max(ts)>73 or max(ts)-min(ts)>10:return None
 hp=max(primer3.calc_hairpin(v,mv_conc=50,dv_conc=1.5,dntp_conc=.6,dna_conc=50).tm for v in vs)
 if hp>55:return None
 return min(ts),max(ts),hp
for right in range(1156,1165):
 for L in range(25,37):
  left=right-L;tt=[rc(al[k][coords[left]:coords[right-1]+1].replace('-','')) for k in ids];valid=np.array([len(t)==L and set(t)<=set('ACGT') for t in tt]);support=weights[valid].sum()
  if support<.75:continue
  mat=np.array([list(t) if ok else list('N'*L) for t,ok in zip(tt,valid)]);freq=np.array([[weights[(mat[:,i]==b)&valid].sum()/support for b in 'ACGT'] for i in range(L)])
  for threshold in [.03,.07,.12,.20,.30]:
   bs=[{b for b,v in zip('ACGT',row) if v>=threshold} or {'ACGT'[row.argmax()]} for row in freq]
   for lock in [0,3]:
    bb=[set(x) for x in bs]
    if lock:
     for j in range(L-3,L):bb[j]={'ACGT'[freq[j].argmax()]}
    q=''.join(inv[frozenset(x)] for x in bb)
    if q in seen:continue
    seen.add(q);deg=int(np.prod([len(x) for x in bb]))
    if deg>32 or any(all('A' in x for x in bb[i:i+4]) for i in range(L-3)):continue
    mm=np.column_stack([~np.isin(mat[:,j],list(I[c])) for j,c in enumerate(q)]);mask=valid&(mm.sum(1)<=2)&~mm[:,-3:].any(1)
    if weights[mask].sum()<.60:continue
    th=thermo(q)
    if th is None:continue
    key=f'RR{len(ol):04d}';rh={model:flexible_hits(db,q,'R',limit,wobble) for model,limit,wobble in [('WC',4,False),('GT',2,True)]};ol.append(dict(id=key,sequence=q,left=left,right=right,degeneracy=deg,tm_min=th[0],tm_max=th[1],hairpin=th[2]))
    for fid in Fids:
     f=lookup[fid];cov=float(weights[mask&Fmask[fid]].sum())
     if cov<.5 or abs((th[0]+th[1]-f['tm_min']-f['tm_max'])/2)>5:continue
     row=dict(F_id=fid,R_id=key,F=f['sequence'],R=q,left=f['left'],right=right,coverage=cov,reference_total=right-f['left'])
     for model in ['WC','GT']:
      fh=cache[fid]['hits'][model];risk={k:set() for k in ['le2','le3','le4','ambiguous']}
      for rec,rs in rh[model].items():
       for fp,fm,f5,fa in fh.get(str(rec),[]):
        for rp,rm,r5,ra in rs:
         if not 0<=rp-fp-len(f['sequence'])<=1000:continue
         keys=['ambiguous'] if fa or ra else [f'le{k}' for k in [2,3,4] if fm<=k and rm<=k]
         for k in keys:risk[k].update(db[3][rec]['accessions'])
      row.update({model+'_'+k:len(v) for k,v in risk.items()})
     out.append(row)
    if len(ol)%10==0:print('R variants',len(ol),'pairs',len(out),flush=True)
(p/'v4_refined_oligos.json').write_text(json.dumps(ol,indent=2));out.sort(key=lambda r:(r['WC_le3']+r['GT_le2'],-r['coverage'],r['WC_le4']));(p/'v4_refined_pairs.json').write_text(json.dumps(out,indent=2));print('DONE',len(ol),len(out),'strict',sum(r['WC_le3']==r['GT_le2']==0 for r in out),flush=True);print(out[:3],flush=True)
