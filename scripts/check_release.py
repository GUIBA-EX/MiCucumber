"""Validate current exports and exact sequence/metric preservation from the frozen prior commit."""
from pathlib import Path
import csv,json,hashlib,zipfile,io,re
from collections import Counter
from naming import normalize, current
p=Path(__file__).resolve().parents[1]
def rows(path):return list(csv.DictReader(path.open()))
def zrows(z,name):return list(csv.DictReader(io.StringIO(z.read(name).decode('utf-8-sig'))))
a=rows(p/'sequences/primer_pairs.csv');assert len(a)==17
schemes={r['scheme'] for r in a};expected={region+suffix for region in ['S','M','L','XL'] for suffix in ['D','','A+'+region+'B']}|{'MiCucumber-S-original'}
assert schemes==expected
fasta={}
for line in (p/'sequences/primers.fasta').read_text().splitlines():
 if line.startswith('>'):
  key=line[1:];assert key not in fasta;fasta[key]=''
 else:fasta[key]+=line
assert len(fasta)==34
for s in schemes:
 rr=[r for r in a if r['scheme']==s];assert len(rr)==int(rr[0]['pairs']);assert len({r['reaction'] for r in rr})==len(rr)
for r in a:
 for d in ['F','R']:
  assert fasta[f"{r['pair_name']}|{d}|{r['pair_id']}"]==r[d]
  assert set(r[d])<=set('ACGT' if r['chemistry']=='ND' else 'ACGTRYSWKMBDHVN')
 if r['chemistry']=='original':assert r['F']=='GWWAGACGARAAGACCCTG' and r['R']=='CCCTRCGGTAACTWTTTCYG'
 else:assert r['scheme']==r['region']+('D' if r['chemistry']=='D' else ('A+'+r['region']+'B' if r['pairs']=='2' else ''))
for reg in ['S','M','L','XL']:assert rows(p/f'sequences/MiCucumber-{reg}.csv')==[r for r in a if r['region']==reg]
combined=rows(p/'results/comparison.csv');assert len(combined)==26
assert Counter(r['scheme'] for r in combined)==Counter({s:2 for s in schemes})
for r in combined:
 assert 0<=float(r['exact_pct'])<=float(r['coverage_pct'])<=100
 assert 0<=float(r['non_Apodida_exact_pct'])<=float(r['non_Apodida_coverage_pct'])<=100
 if r['chemistry']!='original':assert int(r['WC_le3'])<=5 and int(r['GT_le2'])<=5
# All current row values originate from the preserved source snapshot; only identifiers differ.
with zipfile.ZipFile(p/'archive/pre-renaming-14f156f.zip') as z:
 assert z.testzip() is None
 for old,new in [('compact','degenerate'),('nondegenerate','nondegenerate')]:
  for name in ['primer_pairs.csv','comparison.csv','missed_taxa.csv','offtargets.csv']:
   assert current(normalize(zrows(z,f'results/{old}/{name}')))==rows(p/f'results/{new}/{name}'),(old,name)
 expectedseq=[]
 for old in ['compact','nondegenerate']:
  for r in current(normalize(zrows(z,f'results/{old}/primer_pairs.csv'))):expectedseq.append((r['scheme'],r['reaction'],r['F'],r['R']))
 assert expectedseq==[(r['scheme'],r['reaction'],r['F'],r['R']) for r in a]
 mappings=rows(p/'docs/name_mapping.csv');assert len(mappings)==17
 for m,r in zip(mappings,a):
  assert m['new_scheme']==r['scheme'] and m['new_pair_id']==r['pair_id']
  for side in ['F','R']:assert hashlib.sha256(r[side].encode()).hexdigest()==m[side+'_sha256']
for zpath in (p/'reproducibility/frozen').glob('*.zip'):
 with zipfile.ZipFile(zpath) as z:assert z.testzip() is None,zpath
for doc in p.rglob('*.md'):
 for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
  if not link.startswith(('http:','https:','#')):assert (doc.parent/link.split('#')[0]).exists(),(doc,link)
for link in re.findall(r'(?:href|src)="([^"]+)"',(p/'report.html').read_text()):assert (p/link).exists(),link
assert json.loads((p/'results/rename_validation.json').read_text())['sequence_changes']==0
q=json.loads((p/'results/reproduction_checks.json').read_text());assert q['degenerate']=='PASS' and q['nondegenerate']=='PASS'
for name,h in json.loads((p/'SHA256SUMS.json').read_text()).items():assert hashlib.sha256((p/name).read_bytes()).hexdigest()==h,name
print('PASS: 13 portfolios, 17 paired rows, 34 sequence strings, source invariance, risks, links, archive integrity and SHA256')
