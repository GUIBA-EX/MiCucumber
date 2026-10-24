"""Reproduce XS from frozen original FASTA using two independent full scans."""
from pathlib import Path
import argparse,csv,json,zipfile,subprocess,collections,math
from xs_raw_helpers import fa,rc,scan
P=Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
 if any(out.iterdir()):raise SystemExit('Use an empty output directory.')
 with zipfile.ZipFile(P/'reproducibility/frozen/xs_inputs.zip') as z:
  assert set(z.namelist())=={'target.fasta','background.fasta','panel.csv'};z.extractall(out)
 x=json.loads((P/'results/xs/selection.json').read_text());F,R=x['F'],x['R'];(out/'independent_primers.tsv').write_text(f'XS\t{F}\t{R}\n')
 exe=out/'independent_scan';subprocess.run(['c++','-O3','-std=c++17',str(P/'scripts/xs_independent_scan.cpp'),'-o',str(exe)],check=True);subprocess.run([str(exe),str(out)],check=True)
 h=collections.defaultdict(set)
 for r in csv.DictReader((out/'independent_hits.tsv').open(),delimiter='\t'):
  for flag in ['exact','le2last3','le2','le3','le4']:
   if r[flag]=='1':h[r['role'],r['model'],flag].add(r['accession'])
 panel=list(csv.DictReader((out/'panel.csv').open()));ids={r['accession'] for r in panel};metrics={}
 for flag,col in [('le2last3','coverage_pct'),('exact','exact_pct')]:
  for alltarget in [False,True]:
   rows=[r for r in panel if alltarget or r['order']!='Apodida'];metrics[('all_target_' if alltarget else '')+col]=100*sum(float(r['weight']) for r in rows if r['accession'] in h['target','WC',flag])/sum(float(r['weight']) for r in rows)
 for key,model,flag in [('WC3','WC','le3'),('GT2','GT','le2'),('WC4','WC','le4'),('strict_background_WC','WC','le2last3'),('strict_background_GT','GT','le2last3'),('exact_background_WC','WC','exact'),('exact_background_GT','GT','exact')]:metrics[key]=len(h['background',model,flag])
 expected=json.loads((P/'results/xs/assessment.json').read_text())
 for k,v in metrics.items():assert math.isclose(v,expected[k],abs_tol=1e-8),(k,v,expected[k])
 actual=collections.defaultdict(set)
 for role in ['target','background']:
  for acc,s in fa(out/(role+'.fasta')).items():
   if role=='target' and acc not in ids:continue
   for model in (['WC'] if role=='target' else ['WC','GT']):
    ex=False;cv=False
    for seq in [s,rc(s)]:
     ff=scan(seq,F,False,2,model=='GT');rr=scan(seq,R,True,2,model=='GT')
     for fp,fm,fl in ff:
      for rp,rm,rl in rr:
       inner=rp-fp-len(F);total=rp+len(R)-fp
       if role=='target':valid=inner>=20 and 70<=total<=500
       else:valid=0<=inner<=1000
       if not valid:continue
       ex|=fm==0 and rm==0;cv|=not fl and not rl
    if ex:actual[role,model,'exact'].add(acc)
    if cv:actual[role,model,'le2last3'].add(acc)
  print(role+' Python scan complete',flush=True)
 for flag in ['exact','le2last3']:
  assert actual['target','WC',flag]&ids==h['target','WC',flag]&ids,flag
  for model in ['WC','GT']:assert actual['background',model,flag]==h['background',model,flag],(model,flag)
 result=dict(name='XS',metrics=metrics,target_checks=len(ids)*2,background_checks=4,disagreements=0);(out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
