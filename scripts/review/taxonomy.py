import csv,json,time,urllib.parse,urllib.request
from pathlib import Path
root=Path(__file__).resolve().parents[2]; work=root/'work/review'
with (root/'markers/12S_COI/COI/eligible_metadata.csv').open() as f:names=sorted({r['species'] for r in csv.DictReader(f) if r['species']})
cache=work/'worms_results.json'; data=json.loads(cache.read_text()) if cache.exists() else {}
for offset in range(0,len(names),25):
 chunk=[n for n in names[offset:offset+25] if n not in data]
 if not chunk:continue
 params=urllib.parse.urlencode({'scientificnames[]':chunk,'marine_only':'false'},doseq=True)
 url='https://www.marinespecies.org/rest/AphiaRecordsByMatchNames?'+params
 for attempt in range(4):
  try:
   with urllib.request.urlopen(url,timeout=90) as r: results=json.load(r)
   assert len(results)==len(chunk)
   for name,items in zip(chunk,results):data[name]=items or []
   cache.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');break
  except Exception as exc:
   print('retry',offset,str(exc),flush=True);time.sleep(3*(attempt+1))
 else:raise RuntimeError('WoRMS unavailable at batch '+str(offset))
 print(len(data),'/',len(names),flush=True);time.sleep(0.3)
