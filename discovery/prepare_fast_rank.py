from pathlib import Path
import json,csv
from scan_core import database
p=Path(__file__).resolve().parent;db=database(p/'background.fasta');files=sorted((p/'background_hits').glob('*.json'));idx={f.stem:i for i,f in enumerate(files)};rows=list(csv.DictReader((p/'discovery_pairs.tsv').open(),delimiter='\t'))
for b in json.loads((p/'baselines.json').read_text()):rows.append(dict(name=b['name'],F_id=b['name']+'_F',R_id=b['name']+'_R',F=b['F'],R=b['R'],band='baseline',v4_local=False))
(p/'rank_pair_order.json').write_text(json.dumps(rows))
with (p/'rank_input.txt').open('w') as out:
 out.write(f'{len(files)} {len(db[3])//2}\n');out.write(' '.join(str(len(db[3][j]['accessions'])) for j in range(0,len(db[3]),2))+'\n')
 for i,f in enumerate(files):
  d=json.loads(f.read_text());out.write(f'{i} {len(d["sequence"])}\n')
  for model in ['WC','GT']:
   h=d['hits'][model];out.write(str(sum(len(v) for v in h.values()))+'\n')
   for rec in sorted(h,key=int):
    for pos,mm,m5,amb in h[rec]:out.write(f'{rec} {pos} {mm} {amb}\n')
 out.write(str(len(rows))+'\n')
 for r in rows:out.write(f'{idx[r["F_id"]]} {idx[r["R_id"]]}\n')
print('prepared',len(rows),flush=True)
