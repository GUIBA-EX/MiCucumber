"""Frozen-window species comparison, primer-free barcode identity and genus-blocked CV.
Run: python3 scripts/analyze.py
Python standard library only. No external database access.
"""
from pathlib import Path
import argparse,csv,json,collections,random,hashlib,sys,functools
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]/'inputs');args=ap.parse_args();repo=args.repo.resolve();out=Path(__file__).resolve().parents[1];res=out/'results';res.mkdir(exist_ok=True)
def rows(p,sep=','):return list(csv.DictReader(p.open(),delimiter=sep))
def save(name,rr):
 if not rr:return
 with (res/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
def fa(p):
 d={}
 for l in p.open():
  if l.startswith('>'):k=l[1:].split()[0];d[k]=''
  else:d[k]+=l.strip().upper()
 return d
I=dict(A='A',C='C',G='G',T='T',R='AG',Y='CT',S='CG',W='AT',K='GT',M='AC',B='CGT',D='AGT',H='ACT',V='ACG',N='ACGT');REV={frozenset(v):k for k,v in I.items()};rc=lambda s:s.translate(str.maketrans('ACGTRYMKSWBDHVN','TGCAYRKMSWVHDBN'))[::-1]
al=fa(repo/'results/species_qc/curated_alignment.fasta');ref=al['AB525437.1'];cols=[i for i,b in enumerate(ref) if b!='-']
coords={r['locus']:r for r in rows(repo/'figures/current_region_coordinates.csv')}
for reg in ['XS','S','M','L','XL']:
 path=repo/f'results/species_qc/panel_{reg}.csv'
 if path.exists():continue
 valid=[]
 for x in rows(repo/'results/species_qc/panel.csv'):
  sq=al[x['accession']];first=next((i for i,ch in enumerate(sq) if ch!='-'),len(sq));last=next((len(sq)-1-i for i,ch in enumerate(reversed(sq)) if ch!='-'),-1);ok=True
  for side in ['F','R']:
   aa,bb=int(coords[reg][side+'_start']),int(coords[reg][side+'_end']);a,b=cols[aa-1],cols[bb-1];t=sq[a:b+1];ok &= first<=a and last>=b and sum(ch in 'ACGT' for ch in t)>=.9*(bb-aa+1) and all(ch in 'ACGT-' for ch in t)
  if ok:valid.append(x)
 with path.open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(valid[0]));w.writeheader();w.writerows(valid)
pan={r:rows(repo/f'results/species_qc/panel_{r}.csv') for r in ['XS','S','M','L','XL']};common=set.intersection(*[{x['accession'] for x in v} for v in pan.values()]);pairs=rows(repo/'sequences/primer_pairs.csv');coords={r['locus']:r for r in rows(repo/'figures/current_region_coordinates.csv')};hits={}
for p in pairs:
 path=repo/f"results/current_primers/{p['region']}/{p['name']}_independent_hits.tsv"
 hits[p['name']]={x['accession']:x for x in rows(path,'\t') if x['role']=='target' and x['model']=='WC'} if path.exists() else {}
sys.path.insert(0,str(repo/'scripts/species_screening'));from xs_raw_helpers import scan
raw=fa(repo/'results/species_qc/representatives.fasta')
for p in pairs:
 if hits[p['name']]:continue
 for x in pan[p['region']]:
  cv=ex=False
  for sq in [raw[x['accession']],rc(raw[x['accession']])]:
   for fp,fm,fl in scan(sq,p['F']):
    for rp,rm,rl in scan(sq,p['R'],reverse=True):
     inner=rp-fp-len(p['F']);total=rp+len(p['R'])-fp
     if inner<20 or total<70 or total>500:continue
     cv |= not fl and not rl;ex |= fm==rm==0
  hits[p['name']][x['accession']]={'le2last3':str(int(cv)),'exact':str(int(ex))}
save('new_curated_XS_hits.csv',[dict(name=p['name'],accession=a,le2last3=h['le2last3'],exact=h['exact']) for p in pairs if p['region']=='XS' for a,h in hits[p['name']].items()])
comparison=[];orderrows=[];barrows=[];resol=[];collisions=[];templates={};unique={}
for reg,panel in pan.items():
 c=coords[reg];fs,fe,rs,re=[int(c[k]) for k in ['F_start','F_end','R_start','R_end']];bars={};templates[reg]={}
 for x in panel:
  a=x['accession'];s=al[a];f=s[cols[fs-1]:cols[fe-1]+1].replace('-','');r=rc(s[cols[rs-1]:cols[re-1]+1].replace('-',''));templates[reg][a]=(f,r)
  bar=s[cols[fe-1]+1:cols[rs-1]].replace('-','')
  if bar and set(bar)<=set('ACGT'):bars[a]=bar;barrows.append(dict(region=reg,accession=a,species=x['organism'],order=x['order'],length=len(bar),sequence=bar))
 groups=collections.defaultdict(list)
 for x in panel:
  if x['accession'] in bars:groups[bars[x['accession']]].append(x)
 unique[reg]={x['accession'] for group in groups.values() if len(group)==1 for x in group}
 for b,gg in groups.items():
  if len(gg)>1:collisions.append(dict(region=reg,n_species=len(gg),species='; '.join(x['organism'] for x in gg),accessions=';'.join(x['accession'] for x in gg),sequence=b))
 for label,ids in [('own',set(bars)),('common',common&set(bars))]:
  lens=[len(bars[a]) for a in ids];u=ids&unique[reg];resol.append(dict(region=reg,panel=label,n=len(ids),identity_unique_species=len(u),unique_pct=100*len(u)/len(ids),insert_min=min(lens),insert_max=max(lens),identity_groups=len({bars[a] for a in ids})))
 for p in [p for p in pairs if p['region']==reg]:
  h=hits[p['name']]
  for label,ids in [('own',{x['accession'] for x in panel}),('common',common)]:
   cv={a for a in ids if h.get(a,{}).get('le2last3')=='1'};ex={a for a in ids if h.get(a,{}).get('exact')=='1'};comparison.append(dict(name=p['name'],region=reg,panel=label,n=len(ids),covered=len(cv),coverage_pct=100*len(cv)/len(ids),exact=len(ex),exact_pct=100*len(ex)/len(ids),covered_identity_unique=len(cv&unique[reg]),covered_identity_unique_pct=100*len(cv&unique[reg])/len(ids)))
   for o in sorted({x['order'] for x in panel if x['accession'] in ids}):
    oo={x['accession'] for x in panel if x['order']==o}&ids;orderrows.append(dict(name=p['name'],panel=label,order=o,n=len(oo),covered=len(cv&oo),exact=len(ex&oo)))
save('panel_comparison.csv',comparison);save('by_order.csv',orderrows);save('barcodes.csv',barrows);save('resolution.csv',resol);save('barcode_collisions.csv',collisions)
# Genus-blocked CV: reference windows frozen a priori to this test; sequence selection is retrained.
# No released D/ordinary sequence, global oligo pool or background ranking seeds training.
def deg(q):
 v=1
 for b in q:v*=len(I[b])
 return v
@functools.lru_cache(maxsize=300000)
def match(q,t):return len(q)==len(t) and set(t)<=set('ACGT') and sum(b not in I[a] for a,b in zip(q,t))<=2 and all(b in I[a] for a,b in zip(q[-3:],t[-3:]))
@functools.lru_cache(maxsize=300000)
def exact(q,t):return len(q)==len(t) and all(b in I[a] for a,b in zip(q,t))
def candidates(tt,L):
 good=[t for t in tt if len(t)==L and set(t)<=set('ACGT')];freq=collections.Counter(good);cand=set()
 if not good:return []
 def allowed(q):return deg(q)<=8 and any(b in 'GC' for b in q[-3:]) and not any(b*5 in q for b in 'ACGT')
 for seed,_ in [(q,n) for q,n in freq.most_common() if allowed(q)][:24]:
  if not allowed(seed):continue
  q=seed;cand.add(q)
  for _ in range(3):
   options=[]
   for j in range(L//2,L):
    for b in sorted({t[j] for t in good}):
     z=q[:j]+REV[frozenset(I[q[j]]+b)]+q[j+1:]
     if z!=q and allowed(z):options.append(z)
   score=lambda z:(sum(n for t,n in freq.items() if match(z,t)),sum(n for t,n in freq.items() if exact(z,t)),-deg(z),z)
   if not options:break
   z=max(options,key=score)
   if score(z)<=score(q):break
   q=z;cand.add(q)
 return sorted(cand)
sys.path.insert(0,str(repo/'scripts/species_screening'));from xs_raw_helpers import scan
raw=fa(repo/'results/species_qc/representatives.fasta')
def rawhit(f,r,s,reg):
 cv=ex=False
 for t in [s,rc(s)]:
  for fp,fm,fl in scan(t,f):
   for rp,rm,rl in scan(t,r,reverse=True):
    inner=rp-fp-len(f);total=rp+len(r)-fp
    if inner<(20 if reg=='XS' else 50) or total<(70 if reg=='XS' else 150) or total>500:continue
    cv|=not fl and not rl;ex|=fm==rm==0
 return int(cv),int(ex)
cvrows=[];foldrows=[]
for reg,panel in pan.items():
 genus={x['accession']:x['organism'].split()[0] for x in panel};genera=sorted(set(genus.values()));parent={g:g for g in genera}
 def find(g):
  while parent[g]!=g:g=parent[g]
  return g
 seen={}
 for x in panel:
  a=x['accession'];g=genus[a];seq=raw[a]
  if seq in seen:parent[find(g)]=find(seen[seq])
  else:seen[seq]=g
 clusters=sorted({find(g) for g in genera});rng=random.Random(20261030);rng.shuffle(clusters);cm={g:i%5 for i,g in enumerate(clusters)};foldmap={g:cm[find(g)] for g in genera};c=coords[reg];lf=int(c['F_end'])-int(c['F_start'])+1;lr=int(c['R_end'])-int(c['R_start'])+1
 for fold in range(5):
  train=[x for x in panel if foldmap[genus[x['accession']]]!=fold];test=[x for x in panel if foldmap[genus[x['accession']]]==fold];tt=[]
  for x in train:
   sq=al[x['accession']];sides=[]
   for side,L in [('F',lf),('R',lr)]:
    aa=int(c[side+'_start']);bb=int(c[side+'_end']);seg=sq[max(0,cols[aa-1]-5):cols[bb-1]+6].replace('-','');seg=rc(seg) if side=='R' else seg
    sides.append([seg[j:j+L] for j in range(len(seg)-L+1) if set(seg[j:j+L])<=set('ACGT')])
   tt.append(sides)
  fc=candidates([z for t in tt for z in t[0]],lf);rr=candidates([z for t in tt for z in t[1]],lr)
  if not fc or not rr:
   foldrows.append(dict(region=reg,fold=fold,n_train=len(train),n_test=len(test),n_train_genera=len(set(genus[x['accession']] for x in train)),n_test_genera=len(set(genus[x['accession']] for x in test)),F='',R='',deg_F=0,deg_R=0,train_covered=0,train_exact=0))
   for x in test:cvrows.append(dict(region=reg,fold=fold,accession=x['accession'],species=x['organism'],order=x['order'],genus=genus[x['accession']],covered=0,exact=0))
   continue
  fbits={q:(sum(1<<i for i,(ff,rrr) in enumerate(tt) if any(match(q,t) for t in ff)),sum(1<<i for i,(ff,rrr) in enumerate(tt) if any(exact(q,t) for t in ff))) for q in fc}
  rbits={q:(sum(1<<i for i,(ff,rrr) in enumerate(tt) if any(match(q,t) for t in rrr)),sum(1<<i for i,(ff,rrr) in enumerate(tt) if any(exact(q,t) for t in rrr))) for q in rr}
  score=lambda pair:((fbits[pair[0]][0]&rbits[pair[1]][0]).bit_count(),(fbits[pair[0]][1]&rbits[pair[1]][1]).bit_count(),-deg(pair[0])-deg(pair[1]),pair)
  f,r=max(((f,r) for f in fc for r in rr),key=score);foldrows.append(dict(region=reg,fold=fold,n_train=len(train),n_test=len(test),n_train_genera=len(set(genus[x['accession']] for x in train)),n_test_genera=len(set(genus[x['accession']] for x in test)),F=f,R=r,deg_F=deg(f),deg_R=deg(r),train_covered=score((f,r))[0],train_exact=score((f,r))[1]))
  for x in test:
   cv,ex=rawhit(f,r,raw[x['accession']],reg);cvrows.append(dict(region=reg,fold=fold,accession=x['accession'],species=x['organism'],order=x['order'],genus=genus[x['accession']],covered=cv,exact=ex))
  print(reg,fold,len(test),flush=True)
save('cv_folds.csv',foldrows);save('cv_predictions.csv',cvrows);save('cv_summary.csv',[dict(region=reg,n=len(v),covered=sum(x['covered'] for x in v),coverage_pct=100*sum(x['covered'] for x in v)/len(v),exact=sum(x['exact'] for x in v),exact_pct=100*sum(x['exact'] for x in v)/len(v)) for reg in pan for v in [[x for x in cvrows if x['region']==reg]]])
files=['sequences/primer_pairs.csv','results/species_qc/curated_alignment.fasta','results/species_qc/representatives.fasta']+[f'results/species_qc/panel_{r}.csv' for r in pan]
(res/'manifest.json').write_text(json.dumps(dict(seed=20261030,common_species=sorted(common),input_sha256={f:hashlib.sha256((repo/f).read_bytes()).hexdigest() for f in files},cv_scope='Genus-blocked, sequence selection retrained; coordinates previously discovered on full data. Not an external validation of window discovery. CV candidate chemistry/background not screened; not replacement recommendations.',resolution_scope='Exact barcode identity among available one-species representatives; not empirical identification accuracy or within-species validation.'),indent=2))
