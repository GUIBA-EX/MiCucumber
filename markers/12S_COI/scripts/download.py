from pathlib import Path
import urllib.parse as u, urllib.request as req, json,time,gzip
from Bio import SeqIO
from io import StringIO
root=Path(__file__).resolve().parents[1]/'downloads';root.mkdir(exist_ok=True)
def api(action,**kw):
 url='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'+action+'.fcgi?'+u.urlencode(dict(db='nuccore',**kw))
 for i in range(5):
  try:
   with req.urlopen(url,timeout=90) as f:return f.read()
  except Exception as e:
   print(str(e),flush=True)
   if i==4:raise
   time.sleep(2**i)
genes={'12S':'12S[Title] OR rrnS[Gene] OR rns[Gene] OR small subunit ribosomal RNA[Title]','COI':'COI[Title] OR CO1[Title] OR COXI[Title] OR COX1[Gene] OR COI[Gene] OR cytochrome c oxidase subunit I[Title] OR cytochrome oxidase subunit 1[Title] OR cytochrome oxidase subunit I[Title]'}
ids=set()
for g,terms in genes.items():
 q=f'Holothuroidea[Organism] AND ({terms} OR mitochondrial genome[Title] OR mitogenome[Title] OR (mitochondrion[Filter] AND 10000:100000[SLEN]))'
 path=root/(g+'_search.json')
 if not path.exists():
  entries=[];off=0
  while True:
   v=json.loads(api('esearch',term=q,retstart=off,retmax=5000,retmode='json'))['esearchresult'];entries+=v['idlist'];off+=len(v['idlist'])
   if off>=int(v['count']):break
   if not v['idlist']:raise ValueError('incomplete search')
   time.sleep(.4)
  path.write_text(json.dumps(dict(query=q,count=int(v['count']),ids=entries),indent=2))
 v=json.loads(path.read_text());ids.update(v['ids']);print(g,v['count'],flush=True)
ids=sorted(ids,key=int)
for i in range(0,len(ids),150):
 chunk=ids[i:i+150];dest=root/f'batch_{i:06}.gb.gz'
 if dest.exists():continue
 data=api('efetch',id=','.join(chunk),rettype='gb',retmode='text')
 if data.count(b'\n//')!=len(chunk):raise ValueError((i,'batch count'))
 dest.write_bytes(gzip.compress(data));print(i+len(chunk),'/',len(ids),flush=True);time.sleep(.4)
