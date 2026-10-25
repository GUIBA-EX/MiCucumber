from pathlib import Path
import sys,random,collections,functools
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'work/micucumber_terminal'))
from common import *
p0=p;p=root/'work/micucumber_taxon_optimization';out=root/'outputs/MiCucumber_taxon_optimization';out.mkdir(exist_ok=True)
seq={r.id:str(r.seq).upper() for r in SeqIO.parse(p0/'target_aligned.fasta','fasta')};cols=[i for i,b in enumerate(seq['AB525437.1']) if b!='-'];coords=read(root/'outputs/MiCucumber/results/current/binding_positions.csv');current=read(root/'outputs/MiCucumber/sequences/primer_pairs.csv');rev={frozenset(v):k for k,v in I.items() if k!='X'}
labels=sorted({r['organism'] for r in panel});labelids={n:sum(1<<i for i,r in enumerate(panel) if r['organism']==n) for n in labels};orders=sorted({r['order'] for r in panel});orderlabels={o:[j for j,n in enumerate(labels) if next(r for r in panel if r['organism']==n)['order']==o] for o in orders};lw={j:1/len(orders)/len(orderlabels[o]) for o in orders for j in orderlabels[o]}
@functools.lru_cache(None)
def score(bits):
 hit=[j for j,n in enumerate(labels) if bits&labelids[n]];return sum(lw[j] for j in hit),len(hit)/len(labels)
@functools.lru_cache(None)
def pred(q,side,a,b):
 cv=0;ex=0
 for i,x in enumerate(panel):
  s=seq.get(x['accession'],'')[cols[max(0,a-6)]:cols[min(len(cols)-1,b+4)]+1].replace('-','');s=str(Seq(s).reverse_complement()) if side=='R' else s
  for pos in range(len(s)-len(q)+1):
   t=s[pos:pos+len(q)]
   if set(t)<=set('ACGT'):
    mm=[ch not in I[n] for n,ch in zip(q,t)];n=sum(mm)
    if n<=2 and not any(mm[-3:]):cv|=1<<i
    if n==0:ex|=1<<i
 return cv,ex
pool=[];allpairs=[];rng=random.Random(20261025)
existing=[]
for folder in ['micucumber_aggressive','micucumber_aggressive_smxl']:
 existing+=json.loads((root/'work'/folder/'oligos.json').read_text())
for reg in ['S','M','L','XL']:
 c=next(r for r in coords if r['name']==reg+'D');base=next(r for r in current if r['pair_name']==reg+'D');ss={}
 for side in ['F','R']:
  a,b=int(c[side+'_start']),int(c[side+'_end']);counts=[collections.Counter() for _ in range(b-a+1)];templates=collections.defaultdict(list)
  for i,x in enumerate(panel):
   s=seq.get(x['accession'],'')[cols[a-1]:cols[b-1]+1];s=str(Seq(s).reverse_complement()) if side=='R' else s
   if len(s)==b-a+1 and set(s)<=set('ACGT'):
    templates[x['order']].append(s);wt=lw[labels.index(x['organism'])]/sum(y['organism']==x['organism'] for y in panel)
    for j,ch in enumerate(s):counts[j][ch]+=wt
  seeds={r[side] for r in current if r['region']==reg and r['chemistry']!='original'}
  for o,tt in templates.items():
   seeds.add(''.join(collections.Counter(t[j] for t in tt).most_common(1)[0][0] for j in range(b-a+1)))
   seeds.update([q for q,n in collections.Counter(tt).most_common(4)])
  candidates={r['sequence'] for r in existing if r['side']==side and (r['start'],r['end'])==(a,b)}|seeds
  alternatives=[(v/sum(ct.values()),j,ch) for j,ct in enumerate(counts) for ch,v in ct.items()]
  for seed in sorted(seeds):
   if not terminal(seed):continue
   for cap in [8,32,128]:
    for mode in range(3):
     sets=[set(I[ch]) for ch in seed]
     order=sorted(alternatives,key=lambda z:z[0]*(1 if mode==0 else rng.uniform(.2,2.5)),reverse=True)
     for f,j,ch in order:
      if f<.002:continue
      ns=[v|{ch} if k==j else v for k,v in enumerate(sets)];q=''.join(rev[frozenset(v)] for v in ns)
      if deg(q)<=cap and terminal(q):sets=ns
     candidates.add(''.join(rev[frozenset(v)] for v in sets))
  candidates={q for q in candidates if terminal(q) and deg(q)<=128};rr=[]
  for q in sorted(candidates):
   cv,ex=pred(q,side,a,b);rr.append(dict(region=reg,side=side,sequence=q,start=a,end=b,degeneracy=deg(q),cv=cv,ex=ex))
  ranked=sorted(rr,key=lambda r:(score(r['cv'])[0],score(r['ex'])[0],score(r['cv'])[1],-r['degeneracy']),reverse=True)
  selected=ranked[:35]
  # Preserve inexpensive and taxon-specific alternatives, not only overall winners.
  for cap in [1,2,4,8,16,32,64]:selected+= [r for r in ranked if r['degeneracy']<=cap][:3]
  for o in orders:
   om=sum(labelids[n] for n in labels if next(x for x in panel if x['organism']==n)['order']==o)
   selected+=sorted(rr,key=lambda r:(score(r['cv']&om)[0],score(r['ex']&om)[0],-r['degeneracy']),reverse=True)[:2]
  selected+=[r for r in rr if r['sequence']==base[side]]
  unique={r['sequence']:r for r in selected};ss[side]=list(unique.values())
  for r in ss[side]:r['id']=f'T{len(pool):04}';pool.append(r)
  print(reg,side,'generated',len(candidates),'retained',len(ss[side]),flush=True)
 for f,r in itertools.product(ss['F'],ss['R']):
  cv=f['cv']&r['cv'];ex=f['ex']&r['ex'];allpairs.append(dict(region=reg,F=f['sequence'],R=r['sequence'],F_id=f['id'],R_id=r['id'],degeneracy_F=f['degeneracy'],degeneracy_R=r['degeneracy'],pred_order_coverage=100*score(cv)[0],pred_order_exact=100*score(ex)[0],pred_taxon_coverage=100*score(cv)[1],pred_taxon_exact=100*score(ex)[1],cv=cv,ex=ex))
(p/'oligos.json').write_text(json.dumps(pool));(p/'pairs.json').write_text(json.dumps(allpairs));print('POOL',len(pool),'PAIRS',len(allpairs),flush=True)
