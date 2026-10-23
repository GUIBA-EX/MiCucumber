from pathlib import Path
import json,csv,collections,statistics
import numpy as np
from Bio import SeqIO
from scan_core import database,flexible_hits,rc,B
p=Path(__file__).resolve().parent
meta={r['accession']:r for r in csv.DictReader((p/'metadata.tsv').open(),delimiter='\t')}
al={r.id.removeprefix('_R_'):str(r.seq).upper() for r in SeqIO.parse(p/'target_aligned.fasta','fasta')}
assert len(al)==1846
ref='AB525437.1';coords=[i for i,c in enumerate(al[ref]) if c!='-']
def named(s):
 t=s.split();return len(t)==2 and t[0][0].isupper() and t[1].islower() and t[1].isalpha() and t[1] not in ['sp','cf','aff']
sel=json.loads((p/'shortlist_fast.json').read_text())
for b in json.loads((p/'baselines.json').read_text()):
 sel.append(dict(b,left=956 if b['name']=='MiCucumber_v4' else 827,right=1159 if b['name']=='MiCucumber_v4' else 1163,group='baseline'))
left=min(int(s['left']) for s in sel);right=max(int(s['right']) for s in sel)
def panel(l,r):
 kept=[];seen=set();excluded=collections.Counter()
 for k,a in sorted(al.items()):
  if not named(meta[k]['organism']):excluded['unnamed']+=1;continue
  ss=a[coords[l]:coords[r-1]+1]
  if a[coords[l]]=='-' or a[coords[r-1]]=='-':excluded['endpoint_gap']+=1;continue
  if set(ss)-set('ACGT-'):excluded['ambiguous']+=1;continue
  key=meta[k]['organism'],ss.replace('-','')
  if key in seen:excluded['duplicate_haplotype']+=1;continue
  seen.add(key);kept.append(k)
 return kept,dict(excluded)
common,ex=panel(left,right);(p/'common_panel.json').write_text(json.dumps(dict(ids=common,left=left,right=right,exclusions=ex),indent=2))
db=database(p/'target.fasta');arr,offsets,ends,refs,prefix=db;cache={}
def get(q,side):
 key=(q,side)
 if key not in cache:cache[key]=flexible_hits(db,q,side,2,False)
 return cache[key]
rows=[];detail=[]
for s in sel:
 F,R=s['F'],s['R'];fh=get(F,'F');rh=get(R,'R');found={};rp=rc(R)
 for rec in fh.keys()&rh.keys():
  for f,fm,f5,fa in fh[rec]:
   for r,rm,r5,ra in rh[rec]:
    total=r+len(R)-f;inner=r-f-len(F)
    if not(150<=total<=500 and inner>=50) or fa or ra:continue
    f3=all(arr[offsets[rec]+f+j]&B[F[j]] for j in range(len(F)-3,len(F)))
    r3=all(arr[offsets[rec]+r+j]&B[rp[j]] for j in range(3))
    for acc in refs[rec]['accessions']:
     d=found.setdefault(acc,dict(exact=False,le2last3=False,le2=False,sizes=set()))
     d['exact']|=fm==rm==0;d['le2']=True;d['le2last3']|=bool(f3 and r3)
     if f3 and r3:d['sizes'].add(total)
 for pn,ids in [('common',common),('own_region',panel(int(s['left']),int(s['right']))[0])]:
  ct=collections.Counter(meta[k]['organism'] for k in ids);metrics=collections.Counter();sizes=[]
  for k in ids:
   d=found.get(k,dict(exact=False,le2last3=False,le2=False,sizes=set()));w=1/len(ct)/ct[meta[k]['organism']]
   for metric in ['exact','le2last3','le2']:metrics[metric]+=w*d[metric]
   sizes.extend(d['sizes']);detail.append(dict(name=s['name'],panel=pn,accession=k,organism=meta[k]['organism'],weight=w,**{x:d[x] for x in ['exact','le2last3','le2']},sizes=','.join(map(str,sorted(d['sizes'])))))
  rows.append(dict(name=s['name'],group=s['group'],panel=pn,n_labels=len(ct),n_haplotypes=len(ids),**{x+'_pct':100*metrics[x] for x in ['exact','le2last3','le2']},product_min=min(sizes) if sizes else '',product_median=statistics.median(sizes) if sizes else '',product_max=max(sizes) if sizes else ''))
 print(s['name'],rows[-2:],flush=True)
for name,data in [('target_summary.tsv',rows),('target_detail.tsv',detail)]:
 with (p/name).open('w') as f:w=csv.DictWriter(f,fieldnames=list(data[0]),delimiter='\t');w.writeheader();w.writerows(data)
