import csv,json,re
from collections import defaultdict
from pathlib import Path
root=Path(__file__).resolve().parents[2]; work=root/'work/review'
with (work/'target_inserts.csv').open(newline='') as f: rows=list(csv.DictReader(f))
matches=json.loads((root/'results/species_qc/gbif_matches.json').read_text())
accepted=json.loads((root/'results/species_qc/gbif_accepted.json').read_text())
namefamily={}
for obj in matches:
 r=obj.get('match',{}); name=r.get('canonicalName'); family=r.get('family')
 if name and family:namefamily[name]=family
for r in accepted.values():
 if r.get('species') and r.get('family'):namefamily[r['species']]=r['family']
worms=json.loads((work/'worms_results.json').read_text())
def clean(name):return re.sub(r'\s*\([^)]*\)','',name or '').strip()
filtered=[]
for row in rows:
 if row['assay']=='COI LD':
  name=row['species']; candidates=worms.get(name) or []
  match=next((r for r in candidates if r.get('rank')=='Species' and clean(r.get('scientificname')).casefold()==clean(name).casefold() and r.get('class')=='Holothuroidea'),None)
  if not match:continue
  row['species']=clean(match.get('valid_name') or name);row['genus']=row['species'].split()[0];row['family']=match.get('family') or '';row['order']=match.get('order') or ''
 else:row['family']=namefamily.get(row['species'],row['family'])
 filtered.append(row)
rows=filtered
output=[]; collisions=[]
for assay in sorted({r['assay'] for r in rows}):
 group=defaultdict(list)
 for row in rows:
  if row['assay']==assay and set(row['insert'])<=set('ACGT'):group[row['insert']].append(row)
 for rank in ('species','genus','family'):
  evaluable=unique=0
  for seq,items in group.items():
   labels={r[rank] for r in items if r[rank]}
   if any(not r[rank] for r in items):continue
   evaluable+=1;unique+=len(labels)==1
   if rank=='species' and len(labels)>1:collisions.append({'assay':assay,'insert':seq,'species':' | '.join(sorted(labels)),'records':len(items)})
  output.append({'assay':assay,'rank':rank,'unique':unique,'evaluable':evaluable,'matched_records':sum(len(v) for v in group.values())})
for path,data,fields in [('resolution.csv',output,['assay','rank','unique','evaluable','matched_records']),('collisions.csv',collisions,['assay','insert','species','records'])]:
 with (work/path).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
print(json.dumps(output,ensure_ascii=False,indent=2))
