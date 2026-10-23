"""Whole-sequence both-strand WC/GT screening inherited from MiStar; checkpointed."""
from pathlib import Path
import json,sys,concurrent.futures,os,time,hashlib
p=Path(__file__).resolve().parent
sys.path.insert(0,str(p))
from scan_core import database,flexible_hits
DB=None
def init():
 global DB
 DB=database(p/'background.fasta')
def run(item):
 key,side,q=item;f=p/'background_hits'/f'{key}.json'
 if f.exists():return key,'cached'
 data={}
 for model,limit,wobble in [('WC',4,False),('GT',2,True)]:
  data[model]=flexible_hits(DB,q,side,limit,wobble)
 temp=f.with_suffix('.tmp');temp.write_text(json.dumps(dict(id=key,side=side,sequence=q,hits=data)));temp.replace(f)
 return key,'computed'
if __name__=='__main__':
 (p/'background_hits').mkdir(exist_ok=True)
 ol=json.loads((p/'oligos.json').read_text());tasks=[(x['id'],x['side'],x['sequence']) for x in ol]
 for b in json.loads((p/'baselines.json').read_text()):
  tasks.extend((b['name']+'_'+side,side,b[side]) for side in ['F','R'])
 start=time.time()
 with concurrent.futures.ProcessPoolExecutor(max_workers=4,initializer=init) as ex:
  for i,(key,status) in enumerate(ex.map(run,tasks),1):
   if i%25==0 or i==len(tasks):print(i,'/',len(tasks),key,status,'seconds',round(time.time()-start),flush=True)
 (p/'background_screen_complete.json').write_text(json.dumps(dict(count=len(tasks),seconds=time.time()-start,background_sha256=hashlib.sha256((p/'background.fasta').read_bytes()).hexdigest(),models={'WC':4,'GT':2},both_strands=True)))
