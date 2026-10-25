from pathlib import Path
import json,csv,subprocess,collections
p=Path(__file__).resolve().parent;root=p.parents[1];pool=json.loads((p/'oligos.json').read_text());wanted={(r['side'],r['sequence']):r['id'] for r in pool};sites=p/'sites';sites.mkdir(exist_ok=True)
bg=p/'background.fasta'
if not bg.exists():bg.symlink_to(root/'work/micucumber_terminal/background.fasta')
seen=set();lines=[]
for folder in ['micucumber_aggressive_smxl','micucumber_aggressive']:
 d=root/'work'/folder;old=json.loads((d/'oligos.json').read_text());mapping={r['id']:wanted[r['side'],r['sequence']] for r in old if (r['side'],r['sequence']) in wanted and wanted[r['side'],r['sequence']] not in seen};seen.update(mapping.values())
 with (d/'sites/background_sites.tsv').open() as f:
  for row in csv.reader(f,delimiter='\t'):
   if row[0] in mapping:row[0]=mapping[row[0]];lines.append('\t'.join(row)+'\n')
(p/'reused_background_sites.tsv').write_text(''.join(lines));new=[r for r in pool if r['id'] not in seen];(sites/'oligos.tsv').write_text(''.join(f"{r['id']} {r['side']} {r['sequence']}\n" for r in new));print('reuse',len(seen),'new',len(new),flush=True)
subprocess.run(['c++','-O3','-std=c++17','-pthread',str(root/'work/micucumber_terminal/scan_sites.cpp'),'-o',str(p/'scan_sites')],check=True);subprocess.run([str(p/'scan_sites'),str(sites)],check=True)
