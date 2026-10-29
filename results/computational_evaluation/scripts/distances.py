from pathlib import Path
import csv,collections
p=Path(__file__).resolve().parents[1]/'results';groups=collections.defaultdict(list)
for x in csv.DictReader((p/'barcodes.csv').open()):groups[x['region']].append(x)
def edit(a,b):
 m=len(a);vp=~0;vn=0;d=m;top=1<<(m-1);eq={c:sum(1<<i for i,x in enumerate(a) if x==c) for c in 'ACGT'}
 for c in b:
  e=eq.get(c,0);z=(((e&vp)+vp)^vp)|e|vn;hp=vn|~(z|vp);hn=vp&z
  d+=bool(hp&top)-bool(hn&top);hp=(hp<<1)|1;hn<<=1;vp=hn|~(z|hp);vn=z&hp
 return d
assert edit('ACGT','ACGT')==0 and edit('ACGT','AGT')==1 and edit('A','T')==1
out=[]
for reg,rr in groups.items():
 best={x['accession']:(10**9,[]) for x in rr}
 for i,x in enumerate(rr):
  for y in rr[i+1:]:
   d=edit(x['sequence'],y['sequence'])
   for a,b in [(x,y),(y,x)]:
    prev,ids=best[a['accession']]
    if d<prev:best[a['accession']]=(d,[b['accession']])
    elif d==prev:ids.append(b['accession'])
 for x in rr:out.append(dict(region=reg,accession=x['accession'],species=x['species'],nearest_edit_distance=best[x['accession']][0],nearest_accessions=';'.join(best[x['accession']][1])))
 print(reg,'done',flush=True)
with (p/'nearest_neighbors.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
