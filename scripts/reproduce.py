"""Reproduce frozen computations and normalize current exports without changing source evidence."""
from pathlib import Path
import argparse,csv,json,subprocess,sys,zipfile,math
from naming import normalize
ROOT=Path(__file__).resolve().parents[1]
def read(path):return list(csv.DictReader(path.open()))
def write(path,rows):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def equal(actual,expected):
 a,b=read(actual),read(expected);assert len(a)==len(b),(actual,len(a),len(b))
 for x,y in zip(a,b):
  assert x.keys()==y.keys(),(actual,x.keys(),y.keys())
  for k in x:
   if k.endswith('_pct'):assert math.isclose(float(x[k]),float(y[k]),abs_tol=1e-8),(actual,k,x[k],y[k])
   else:assert x[k]==y[k],(actual,k,x[k],y[k])
def run(args,cwd):subprocess.run([str(x) for x in args],check=True,cwd=cwd)
def main():
 a=argparse.ArgumentParser();a.add_argument('mode',choices=['degenerate','nondegenerate','round2']);a.add_argument('--work-dir',type=Path,default=ROOT/'reproduction-work');args=a.parse_args()
 work=args.work_dir.resolve()/args.mode
 if work.exists() and any(work.iterdir()):raise SystemExit('Use a fresh --work-dir; existing reproduction files are not overwritten.')
 work.mkdir(parents=True,exist_ok=True)
 bundle={'degenerate':'degenerate_selection.zip','nondegenerate':'nondegenerate_design.zip','round2':'round2_reference_validation.zip'}[args.mode]
 with zipfile.ZipFile(ROOT/'reproducibility/frozen'/bundle) as z:
  for n in z.namelist():assert (work/n).resolve().is_relative_to(work)
  z.extractall(work)
 result=work/'current-results';result.mkdir(exist_ok=True)
 if args.mode=='nondegenerate':
  run([sys.executable,work/'run_reproduction.py'],work)
  source=work/'rebuild/results'
  for path in source.glob('*.csv'):write(result/path.name,normalize(read(path)))
  for path in source.glob('*.json'):(result/path.name).write_text(json.dumps(normalize(json.loads(path.read_text())),indent=2)+'\n')
  for n in ['primer_pairs.csv','comparison.csv']:equal(result/n,ROOT/'results/nondegenerate'/n)
 elif args.mode=='degenerate':
  run([sys.executable,work/'work/micucumber_compact/optimize.py'],work)
  source=work/'outputs/MiCucumber_compact';data=work/'work/micucumber_round2/optimization'
  schemes={s['name']:s for s in json.loads((source/'schemes.json').read_text())};pairs={s['name']:s for s in json.loads((data/'shortlist_fast.json').read_text())}
  chosen=[schemes[f'MiCucumber-{loc}_N{n}_B5_T{2 if n==2 and loc in ("v4opt","M") else 1}'] for loc in ['v4opt','S','M','L'] for n in [1,2]]
  comparisons=read(source/'all_tradeoffs.csv');seq=[];summary=[]
  for s in chosen:
   summary.extend(r for r in comparisons if r['scheme']==s['name'])
   for j,n in enumerate(s['pair_names'],1):seq.append(dict(version=s['locus'],pairs=str(s['count']),reaction=str(j),pair_id=n,F=pairs[n]['F'],R=pairs[n]['R'],scheme=s['name']))
  write(result/'primer_pairs.csv',normalize(seq));write(result/'comparison.csv',normalize(summary))
  (result/'selection.json').write_text(json.dumps(normalize(chosen),indent=2)+'\n')
  for n in ['primer_pairs.csv','comparison.csv']:equal(result/n,ROOT/'results/degenerate'/n)
 else:
  run([sys.executable,work/'run_revalidation.py'],work)
  print('PASS: frozen round-two reference validation. Intermediate evidence retains historical source identifiers.')
  return
 with (result/'primers.fasta').open('w') as f:
  for r in read(result/'primer_pairs.csv'):
   for d in ('F','R'):f.write(f">{r['scheme']}|PCR{r['reaction']}|{d}|{r['pair_id']}\n{r[d]}\n")
 print('PASS: current names, primer sequences and comparison metrics reproduced:',result)
if __name__=='__main__':main()
