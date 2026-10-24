"""Check nondegenerate exports, original v4 preservation, risks and frozen hashes."""
from pathlib import Path
import csv,json,hashlib,zipfile,re
p=Path(__file__).resolve().parent;d=p/'results/nondegenerate'
def rows(n):return list(csv.DictReader((d/n).open()))
a=rows('primer_pairs.csv');assert len(a)==13
assert len({r['scheme'] for r in a})==9
for r in a:
 if r['version']=='original-v4':
  assert r['F']=='GWWAGACGARAAGACCCTG' and r['R']=='CCCTRCGGTAACTWTTTCYG'
 else:assert set(r['F']+r['R'])<=set('ACGT')
for r in rows('comparison.csv'):
 assert len([x for x in a if x['scheme']==r['scheme']])==int(r['count'])
 assert 0<=float(r['exact_pct'])<=float(r['coverage_pct'])<=100
 if r['locus']!='original-v4':assert int(r['WC_le3'])<=5 and int(r['GT_le2'])<=5
for r in rows('thermodynamics.csv'):assert float(r['structure_max'])<55
assert len(rows('candidate_scores.csv'))==2644
q=json.loads((d/'validation.json').read_text());assert q['status']=='PASS' and q['target_boolean_checks']==31428 and q['original_v4_unchanged']
assert json.loads((d/'reproduction_check.json').read_text())['status']=='PASS'
for n,h in json.loads((d/'SHA256SUMS.json').read_text()).items():assert hashlib.sha256((d/n).read_bytes()).hexdigest()==h,n
with zipfile.ZipFile(d/'reproducibility.zip') as z:
 assert z.testzip() is None
 for n,h in json.loads(z.read('SHA256SUMS.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
for n in re.findall(r'href="([^"]+)"',(d/'report.html').read_text()):assert (d/n).exists(),n
print('PASS: eight ACGT-only portfolios, unchanged v4, risk/thermal bounds, reproduction evidence, links and hashes')
