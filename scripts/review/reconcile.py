import csv,json,re
from pathlib import Path
from Bio import SeqIO
from collections import defaultdict,Counter
root=Path(__file__).resolve().parents[2]; work=root/'work/review'; db=json.loads((work/'worms_results.json').read_text())
def clean(n):return re.sub(r'\s*\([^)]*\)','',n or '').strip()
def match(name):
 items=db.get(name) or []
 for x in items:
  if x.get('rank')=='Species' and clean(x.get('scientificname')).casefold()==clean(name).casefold() and x.get('class')=='Holothuroidea':
   return dict(species=clean(x.get('valid_name') or name),genus=x.get('genus') or name.split()[0],family=x.get('family') or '',order=x.get('order') or '',status=x.get('status') or '',aphia=x.get('valid_AphiaID'))
 return None
aln={r.id.removeprefix('_R_'):r for r in SeqIO.parse(root/'markers/12S_COI/COI/aligned.fasta','fasta')}
anchor=(root/'markers/12S_COI/COI/anchor.txt').read_text().strip();cols=[i for i,b in enumerate(str(aln[anchor].seq)) if b!='-']
with open(root/'markers/12S_COI/COI/pairs.csv') as f:p=next(r for r in csv.DictReader(f) if r['name']=='LD')
a,b,c,d=[cols[int(p[k])-1] for k in ('F_start','F_end','R_start','R_end')]
with open(root/'markers/12S_COI/COI/target_panel.csv') as f: panel=list(csv.DictReader(f))
avail=[];unresolved=[]
for r in panel:
 s=str(aln[r['accession']].seq).upper(); eligible=len(s)-len(s.lstrip('-'))<=a and len(s.rstrip('-'))>d and set(s[a:b+1]+s[c:d+1])<=set('ACGT-')
 if not eligible:continue
 info=match(r['species'])
 if info:avail.append((r,info))
 else:unresolved.append(r['species'])
unique={}
for r,info in sorted(avail,key=lambda x:(-int(x[0]['length']),x[0]['accession'])):unique.setdefault(info['species'],(r,info))
print('raw evaluable',len(avail)+len(unresolved),'species resolved',len(avail),'unique',len(unique),'unresolved',unresolved,flush=True)
accessionmap={r['accession']:info for r,info in unique.values()}
ns={'__file__':str(work/'scan.py')};exec((work/'scan.py').read_text().split('results=[]; insertrows=[]')[0],ns)
_,fwds,revs=ns['assays']['COI LD']; inp=root/'markers/12S_COI/COI/target.fasta'
hits={e:set(ns['scan']('COI LD','COI',fwds,revs,inp,e,'worms')) for e in range(3)}
summary=[]
for order in sorted({x['order'] for x in accessionmap.values()}|{'ALL'}):
 ids={a for a,t in accessionmap.items() if order=='ALL' or t['order']==order}
 summary.append(dict(order=order,n=len(ids),**{f'e{e}':len(ids&hits[e]) for e in hits}))
with (work/'coi_worms_panel.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['accession','species','genus','family','order','status','aphia']);w.writeheader();w.writerows({'accession':a,**v} for a,v in accessionmap.items())
with (work/'coi_worms_coverage.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['order','n','e0','e1','e2']);w.writeheader();w.writerows(summary)
print(json.dumps(summary,indent=2),flush=True)
