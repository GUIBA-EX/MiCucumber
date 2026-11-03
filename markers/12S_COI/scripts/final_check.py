"""Check exported pairs by exhaustive seed-and-extend matching on both strands."""
import csv,hashlib,json,re,zipfile
from collections import Counter,defaultdict
from functools import lru_cache
from pathlib import Path
from Bio import SeqIO
from chemistry import I,deg,terminal,thermal
root=Path(__file__).resolve().parents[1]
def rows(p,sep=','):
 with p.open() as f:return list(csv.DictReader(f,delimiter=sep))
def fasta(p):
 seqs=list(SeqIO.parse(p,'fasta'));d={x.id:str(x.seq).upper() for x in seqs};assert len(d)==len(seqs);return d
comp=str.maketrans('ACGT','TGCA')
@lru_cache(None)
def pattern(q,reverse,gt,k):
 sets=[set(I[b]) for b in q]
 for chars in sets:
  if gt:
   if 'G' in chars:chars.add('A')
   if 'T' in chars:chars.add('C')
 if reverse:sets=[set(''.join(c).translate(comp)) for c in sets[::-1]]
 seeds=[]
 for j in range(k+1):
  a=j*len(q)//(k+1);b=(j+1)*len(q)//(k+1)
  seeds.append((a,re.compile('(?='+''.join('['+''.join(sorted(c))+']' for c in sets[a:b])+')')))
 return sets,seeds
def sites(s,q,rev,gt,k):
 sets,seeds=pattern(q,rev,gt,k)
 starts={m.start()-a for a,rg in seeds for m in rg.finditer(s)}
 for i in starts:
  if i<0 or i+len(q)>len(s):continue
  t=s[i:i+len(q)]
  if set(t)-set('ACGT'):continue
  bad=[j for j,c in enumerate(t) if c not in sets[j]]
  if len(bad)<=k:yield i,len(bad),all(j>=3 if rev else j<len(q)-3 for j in bad)
def flags(s,f,r,target,gt):
 k=2 if target or gt else 3;ans=[False]*3
 for strand in (s,s.translate(comp)[::-1]):
  fs=list(sites(strand,f,False,gt,k))
  if not fs:continue
  for j,m,t in sites(strand,r,True,gt,k):
   for i,n,u in fs:
    gap=j-i-len(f);span=j+len(r)-i
    if (gap<50 or not 100<=span<=500) if target else not 0<=gap<=1000:continue
    ans[0]|=max(m,n)==0;ans[1]|=max(m,n)<=2 and t and u;ans[2]=True
 return ans
allpairs=rows(root/'candidates.csv');export=fasta(root/'primers.fasta');assert allpairs and len(export)==2*len(allpairs)
report=[]
for gene in ('12S','COI'):
 d=root/gene;panel=rows(d/'target_panel.csv');target=fasta(d/'target.fasta');bg=fasta(d/'background.fasta');al={k.removeprefix('_R_'):v for k,v in fasta(d/'aligned.fasta').items()};ref=al[(d/'anchor.txt').read_text().strip()];cols=[i for i,c in enumerate(ref) if c!='-'];pairs=rows(d/'pairs.csv');assert pairs==[x for x in allpairs if x['gene']==gene];assert len({x['species'] for x in panel})==len(target)==len(panel)
 ids={(f,r):i for i,f,r in (line.split() for line in (d/'verification/independent_primers.tsv').read_text().splitlines())}
 ids.update({(z['F'],z['R']):z['name'] for z in pairs if z['name'].endswith('D')})
 keep={ids[z['F'],z['R']] for z in pairs};arch={}
 for x in rows(d/'verification/independent_hits.tsv','\t'):
  if x['name'] in keep:arch[x['name'],x['role'],x['model'],x['accession']]=x
 for z in pairs:
  f,r=z['F'],z['R'];key=ids[f,r];a,b,c,e=[int(z[k]) for k in ('F_start','F_end','R_start','R_end')];assert len(f)==b-a+1 and len(r)==e-c+1 and int(z['span'])==e-a+1
  assert all(export[f"{gene}_{z['name']}_{k}"]==z[k] for k in 'FR')
  assert max(deg(f),deg(r))<=8 and all(terminal(v) for v in [f,r]);assert thermal(f,r)[0]
  mate=next(y for y in pairs if y['window']==z['window'] and y['name']!=z['name']);assert all(z[k]==mate[k] for k in ('F_start','F_end','R_start','R_end'))
  if not z['name'].endswith('D'):assert deg(f)*deg(r)==1 and all(u in I[v] for k in 'FR' for u,v in zip(z[k],mate[k]))
  t=Counter();checks=0
  for role,library in [('target',target),('background',bg)]:
   for acc,s in library.items():
    if role=='target':
     v=al[acc];start,end=cols[a-1],cols[e-1];ok=bool(v[:start+1].strip('-')) and bool(v[end:].strip('-')) and set(v[start:cols[b-1]+1]+v[cols[c-1]:end+1])<=set('ACGT-')
     t['evaluable']+=ok
    for model in (['WC'] if role=='target' else ['WC','GT']):
     ex,strict,broad=flags(s,f,r,role=='target',model=='GT');old=arch.get((key,role,model,acc),{})
     exp=[old.get(k)=='1' for k in ['exact','le2last3','le3' if role=='background' and model=='WC' else 'le2']]
     assert [ex,strict,broad]==exp,(gene,z['name'],role,acc,model);checks+=1
     if role=='target' and ok:t['covered']+=strict;t['exact']+=ex
     if role=='background':t[model]+=strict;t['WC3' if model=='WC' else 'GT2']+=broad
  assert all(t[k]==int(z[k]) for k in ['evaluable','covered','exact','WC','GT','WC3','GT2'])
  report.append(dict(gene=gene,name=z['name'],record_model_checks=checks,**t));print(gene,z['name'],checks,flush=True)
(root/'final_check.json').write_text(json.dumps(dict(status='PASS',pairs=report),indent=2))
