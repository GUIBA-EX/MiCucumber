import hashlib,json,time,urllib.parse,urllib.request,urllib.error,sys
from pathlib import Path
API='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
def request(method, **params):
 url=API+method+'.fcgi?'+urllib.parse.urlencode(dict(db='nuccore',**params))
 for i in range(4):
  try:
   with urllib.request.urlopen(url,timeout=30) as r: return r.read()
  except (urllib.error.URLError,TimeoutError) as e:
   if i==3:raise
   time.sleep(2+3*i)
def search():
 groups={'target_mito':'Holothuroidea','Echinoidea':'Echinoidea','Asteroidea':'Asteroidea',
         'Ophiuroidea':'Ophiuroidea','Crinoidea':'Crinoidea','Gastropoda':'Gastropoda','Malacostraca':'Malacostraca',
         'Anthozoa':'Anthozoa','Nemertea':'Nemertea','Actinopteri':'Actinopteri'}
 filters={k:f'{taxon}[Organism] AND 2026[Create Date] AND mitochondrion[Title] AND complete genome[Title]' for k,taxon in groups.items()}
 filters['target_16S']='Holothuroidea[Organism] AND 2026[Create Date] AND (16S[Title] OR "large subunit ribosomal RNA"[Title])'
 targets='Holothuroidea[Organism]'
 years='(2026[Create Date] OR 2025[Create Date] OR 2024[Create Date])'
 filters.update({
  'target_mito_all':targets+' AND mitochondrion[Title] AND complete genome[Title]',
  'target_16S_extended':targets+' AND '+years+' AND (16S[Title] OR "large subunit ribosomal RNA"[Title])',
  'target_12S':targets+' AND (12S[Title] OR "small subunit ribosomal RNA"[Title])',
  'target_mito_broad':targets+' AND (mitochondrial[Title] OR mitochondrion[Title]) AND (complete[Title] OR genome[Title])',
  'target_COI_all':targets+' AND (COI[Title] OR CO1[Title] OR COX1[Title] OR cytochrome oxidase[Title])',
  'target_COI':targets+' AND '+years+' AND (COI[Title] OR CO1[Title] OR "cytochrome c oxidase subunit I"[Title] OR "cytochrome oxidase subunit 1"[Title])',
 })
 for group in ('Echinoidea','Asteroidea','Ophiuroidea','Crinoidea'):
  filters[group+'_all']=f'{groups[group]}[Organism] AND mitochondrion[Title] AND complete genome[Title]'
  filters[group+'_extended']=f'{groups[group]}[Organism] AND {years} AND mitochondrion[Title] AND complete genome[Title]'
 for k,term in filters.items():
  p=Path(k+'.json')
  if p.exists() and json.loads(p.read_text()).get('query')==term: continue
  x=json.loads(request('esearch',term=term,retmode='json',retmax=3500 if k=='target_COI_all' else 1300 if k=='target_mito_broad' else 400,idtype='acc',sort='date'))['esearchresult']
  assert x['querytranslation'],(k,x)
  p.write_text(json.dumps(dict(query=term,**x),indent=2)+'\n')
  print(k,x['count'],x['idlist'][:4],flush=True)
  time.sleep(.45)
def fetch():
 exclusions=set(Path('historical_accessions.txt').read_text().splitlines())
 ids={}
 for f in Path().glob('*.json'):
  x=json.loads(f.read_text())
  if not isinstance(x,dict) or 'query' not in x or not x.get('querytranslation'): continue
  group=f.stem
  candidates=[a for a in x['idlist'] if a.split('.')[0] not in exclusions and not a.startswith(('NC_','GH','GO','GR','HS','HO','JI','JK'))]
  for a in candidates[:(220 if group.startswith('target') else 65)]:
   ids.setdefault(a,[]).append(group)
 Path('candidate_sources.json').write_text(json.dumps(ids,indent=2)+'\n')
 for i in range(0,len(ids),45):
  batch=list(ids)[i:i+45]
  key=hashlib.sha256(','.join(batch).encode()).hexdigest()[:12]
  filename=Path(f'genbank_{key}.gb')
  if not filename.exists():
   data=request('efetch',id=','.join(batch),rettype='gbwithparts',retmode='text')
   assert data.startswith(b'LOCUS'),data[:150]
   filename.write_bytes(data)
  print('batch',i,len(batch),flush=True)
  time.sleep(.4)
if __name__=='__main__': (search if sys.argv[1]=='search' else fetch)()
