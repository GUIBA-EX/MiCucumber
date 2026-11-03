"""Check alternate locus spellings and retrieve additional unique records."""
from pathlib import Path
import json,urllib.request as req,urllib.parse as u,gzip,time
root=Path(__file__).resolve().parents[1]/'downloads';old=set()
for g in ['12S','COI']:old.update(json.loads((root/(g+'_search.json')).read_text())['ids'])
def api(action,**kw):
 for i in range(5):
  try:
   with req.urlopen('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'+action+'.fcgi?'+u.urlencode(dict(db='nuccore',**kw)),timeout=100) as f:return f.read()
  except Exception:
   if i==4:raise
   time.sleep(2**i)
extra=set()
for gene,terms in [('12S','rrnS[Title] OR s-rRNA[Title] OR mitochondrial small subunit[Title] OR mitochondrial genome[Title]'),('COI','COX1[Title] OR COXI[Title] OR MT-CO1[Title] OR MT-CO1[Gene] OR cytochrome c oxidase subunit 1[Title] OR cytochrome c oxidase subunit one[Title] OR cytochrome oxidase subunit one[Title]')]:
 q=f'Holothuroidea[Organism] AND ({terms})';ids=[];off=0
 while True:
  z=json.loads(api('esearch',term=q,retstart=off,retmax=5000,retmode='json'))['esearchresult'];ids+=z['idlist'];off+=len(z['idlist'])
  if off>=int(z['count']):break
  assert z['idlist']
 new=set(ids)-old;extra.update(new);(root/(gene+'_aliases.json')).write_text(json.dumps(dict(query=q,count=len(ids),additional_uids=sorted(new)),indent=2));print(gene,len(new),flush=True);time.sleep(.4)
extra=sorted(extra,key=int)
for i in range(0,len(extra),150):
 chunk=extra[i:i+150];out=root/f'batch_extra_{i:05}.gb.gz';data=api('efetch',id=','.join(chunk),rettype='gb',retmode='text');assert data.count(b'\n//')==len(chunk);out.write_bytes(gzip.compress(data));time.sleep(.4)
