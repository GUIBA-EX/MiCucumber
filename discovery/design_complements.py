"""Same-coordinate taxon-specific and consensus variants to recover missed taxa."""
from pathlib import Path
import json,csv,sys,itertools,collections,functools
import numpy as np
from Bio import SeqIO
from Bio.Data.IUPACData import ambiguous_dna_values as I
from scan_core import rc
p=Path(__file__).resolve().parent;out=p/'same_locus'
import primer3
al={r.id.removeprefix('_R_'):str(r.seq).upper() for r in SeqIO.parse(p/'target_aligned.fasta','fasta')};panel=json.loads((p/'common_panel.json').read_text());ids=panel['ids'];meta={r['accession']:r for r in csv.DictReader((p/'metadata.tsv').open(),delimiter='\t')};cnt=collections.Counter(meta[k]['organism'] for k in ids);w=np.array([1/len(cnt)/cnt[meta[k]['organism']] for k in ids]);ref='AB525437.1';coords=[i for i,c in enumerate(al[ref]) if c!='-'];inv={frozenset(v):k for k,v in I.items() if k!='X'};loci=json.loads((p/'final_selected.json').read_text())[:4]
@functools.lru_cache(None)
def thermal(q):
 vs=[''.join(t) for t in itertools.product(*(I[c] for c in q))];tm=[primer3.calc_tm(t,mv_conc=50,dv_conc=1.5,dntp_conc=.6,dna_conc=50) for t in vs]
 if min(tm)<50 or max(tm)>73 or max(tm)-min(tm)>10:return None
 hp=max(primer3.calc_hairpin(t,mv_conc=50,dv_conc=1.5,dntp_conc=.6,dna_conc=50).tm for t in vs)
 if hp>55:return None
 return dict(tm_min=min(tm),tm_max=max(tm),hairpin_max=hp)
allol=[];masks=[];exacts=[];pairs=[]
for seed in loci:
 group=seed['label'];si={};left=int(seed['left']);right=int(seed['right'])
 for side in ['F','R']:
  L=len(seed[side]);a,b=(left,left+L) if side=='F' else (right-L,right)
  ts=[al[k][coords[a]:coords[b-1]+1].replace('-','') for k in ids]
  if side=='R':ts=[rc(t) for t in ts]
  valid=np.array([len(t)==L and set(t)<=set('ACGT') for t in ts]);mat=np.array([list(t) if ok else list('N'*L) for t,ok in zip(ts,valid)]);queries={seed[side]:'seed'}
  for t,ok in zip(ts,valid):
   if abs(len(t)-L)<=4 and 18<=len(t)<=36 and set(t)<=set('ACGT'):queries[t]='concrete_observed'
  groups=collections.defaultdict(list)
  for j,k in enumerate(ids):
   if valid[j]:groups[meta[k]['organism'].split()[0]].append(j)
  groups['ALL']=list(np.flatnonzero(valid))
  for gn,ix in groups.items():
   for threshold in [.03,.1,.2,.3]:
    freq=np.array([[sum(w[j] for j in ix if mat[j,k]==c)/sum(w[ix]) for c in 'ACGT'] for k in range(L)])
    bs=[{c for c,v in zip('ACGT',row) if v>=threshold} or {'ACGT'[row.argmax()]} for row in freq];q=''.join(inv[frozenset(x)] for x in bs);queries[q]='consensus_'+gn
  si[side]=[]
  for q,origin in sorted(queries.items()):
   qlen=len(q);validq=np.array([len(t)==qlen and set(t)<=set('ACGT') for t in ts]);matq=np.array([list(t) if ok else list('N'*qlen) for t,ok in zip(ts,validq)]);deg=int(np.prod([len(I[c]) for c in q]))
   if deg>32 or any(all('A' in I[c] for c in q[j:j+4]) for j in range(qlen-3)):continue
   mis=np.column_stack([~np.isin(matq[:,j],list(I[c])) for j,c in enumerate(q)]);m=validq&(mis.sum(1)<=2)&~mis[:,-3:].any(1);e=validq&~mis.any(1)
   if w[m].sum()<.005:continue
   th=thermal(q)
   if th is None:continue
   key=f'SL{len(allol):04d}';i=len(allol);allol.append(dict(id=key,side=side,sequence=q,left=a,right=b,locus=group,origin=origin,degeneracy=deg,coverage=float(w[m].sum()),exact=float(w[e].sum()),**th));masks.append(m);exacts.append(e);si[side].append(i)
 for fi in si['F']:
  for ri in si['R']:
   f,r=allol[fi],allol[ri];coverage=float(w[masks[fi]&masks[ri]].sum())
   if coverage<.005 or abs((f['tm_min']+f['tm_max']-r['tm_min']-r['tm_max'])/2)>5:continue
   pairs.append(dict(F_id=f['id'],R_id=r['id'],F=f['sequence'],R=r['sequence'],left=left,right=right,reference_total=right-left,band=group,v4_local=group=='MiCucumber-v4opt',coverage=coverage,exact=float(w[exacts[fi]&exacts[ri]].sum()),degeneracy_sum=f['degeneracy']+r['degeneracy']))
 print(group,'F',len(si['F']),'R',len(si['R']),'cumulative pairs',len(pairs),flush=True)
(out/'oligos.json').write_text(json.dumps(allol,indent=2));np.savez_compressed(out/'discovery_masks.npz',coverage=np.array(masks),exact=np.array(exacts),weights=w);(out/'baselines.json').write_text('[]')
with (out/'discovery_pairs.tsv').open('w') as f:wr=csv.DictWriter(f,fieldnames=list(pairs[0]),delimiter='\t');wr.writeheader();wr.writerows(pairs)
(out/'design_manifest.json').write_text(json.dumps(dict(n_oligos=len(allol),n_pairs=len(pairs),panel_ids=ids,held_out=False,scope='same exact binding coordinates per locus; observed concrete and genus/all consensus variants; discovery panel now includes all common eligible records',non_target_preference='minimize, small residual allowed, report all models; no absolute wet-lab specificity claim'),indent=2))
