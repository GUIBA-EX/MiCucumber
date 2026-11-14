"""Download the two named-species UNIQ rRNA members of the versioned MIDORI2 archive.
HTTP range requests avoid downloading unrelated mitochondrial gene files.
"""
import urllib.request,zipfile,io,json,hashlib,time,struct,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]/'work/review/midori';ROOT.mkdir(parents=True,exist_ok=True)
url='https://zenodo.org/records/22685701/files/MIDORI2_GB273_SINTAX.zip';size=422357811
class Remote(io.RawIOBase):
 def __init__(self):self.pos=0
 def seekable(self):return True
 def seek(self,n,w=0):self.pos=n if w==0 else self.pos+n if w==1 else size+n;return self.pos
 def tell(self):return self.pos
 def read(self,n=-1):
  n=min(n if n>=0 else size-self.pos,size-self.pos)
  if n<=0:return b''
  start=self.pos;end=start+n-1
  req=urllib.request.Request(url+f'?range_start={start}',headers={'Range':f'bytes={start}-{end}'})
  for attempt in range(4):
   try:
    with urllib.request.urlopen(req,timeout=90) as h:
     if h.status!=206:raise RuntimeError('Server did not honour range: '+str(h.status))
     b=h.read();assert len(b)==n,(len(b),n)
    self.pos+=n;return b
   except Exception:
    if attempt==3:raise
    time.sleep(2)
r=Remote();z=zipfile.ZipFile(r);members=[n for n in z.namelist() if '/uniq/' in n and ('_CO1_' in n or '_lrRNA_' in n)];print(members,flush=True);assert len(members)==2
manifest=[]
for name in members:
 out=ROOT/Path(name).name
 if not out.exists():out.write_bytes(z.read(name))
 manifest.append(dict(archive=url,member=name,bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),download_date='2026-11-12'))
 print(name,out.stat().st_size,flush=True)
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
