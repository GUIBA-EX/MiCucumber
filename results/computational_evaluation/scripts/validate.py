from pathlib import Path
import csv,json,sys,random
p=Path(__file__).resolve().parents[1];r=p/'results'
def rd(n):return list(csv.DictReader((r/n).open()))
meta=json.loads((r/'manifest.json').read_text());common=set(meta['common_species']);assert len(common)>0
for z in rd('panel_comparison.csv'):
 assert int(z['exact'])<=int(z['covered'])<=int(z['n'])
 if z['panel']=='common':assert int(z['n'])==len(common)
pred=rd('cv_predictions.csv');fold=rd('cv_folds.csv')
for reg in ['XS','S','M','L','XL']:
 v=[x for x in pred if x['region']==reg];assert len(v)==len({x['accession'] for x in v})
 g={}
 for x in v:
  if x['genus'] in g:assert g[x['genus']]==x['fold']
  g[x['genus']]=x['fold']
 assert len([x for x in fold if x['region']==reg])==5
 for x in fold:
  if x['region']==reg:assert int(x['n_train'])+int(x['n_test'])==len(v)
 bars=[x for x in rd('barcodes.csv') if x['region']==reg];counts={}
 for b in bars:counts[b['sequence']]=counts.get(b['sequence'],0)+1
 q=next(x for x in rd('resolution.csv') if x['region']==reg and x['panel']=='own');assert sum(v==1 for v in counts.values())==int(q['identity_unique_species'])
for z in rd('cv_summary.csv'):
 v=[x for x in pred if x['region']==z['region']];assert sum(int(x['covered']) for x in v)==int(z['covered']) and sum(int(x['exact']) for x in v)==int(z['exact'])
print('PASS: denominators, barcode identities, unique held-out species, genus separation, fold sizes and prediction totals')

for reg in ['XS','S','M','L','XL']:
 records={}
 for line in (p/'inputs/results/species_qc/representatives.fasta').open():
  if line.startswith('>'):a=line[1:].split()[0];records[a]=''
  else:records[a]+=line.strip().upper()
 seen={}
 for x in [x for x in pred if x['region']==reg]:
  seq=records[x['accession']]
  if seq in seen:assert seen[seq]==x['fold']
  seen[seq]=x['fold']
print('PASS: identical complete representatives never cross folds')

import hashlib
for f,digest in meta['input_sha256'].items():assert hashlib.sha256((p/'inputs'/f).read_bytes()).hexdigest()==digest
print('PASS: frozen input hashes')
