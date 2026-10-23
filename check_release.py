"""Check release tables and frozen evidence without rerunning expensive scans."""
from pathlib import Path
import csv,json,hashlib
p=Path(__file__).resolve().parent
q=json.loads((p/'analysis/independent_validation.json').read_text());assert q['status']=='PASS' and q['checks']==386492
assert json.loads((p/'analysis/portfolio_qa.json').read_text())['status']=='PASS'
def rows(n):return list(csv.DictReader((p/n).open(encoding='utf-8-sig')))
a=rows('results/final_separate_pairs.csv');assert len(a)==29
summ=rows('results/apodida_comparison.csv')
for s in summ:
 rr=[x for x in a if x['scheme']==s['scheme']]
 assert len(rr)==int(s['total_pairs'])
 assert len({x['reaction'] for x in rr})==len(rr)
 assert all(set(x[d])<=set('ACGTRYSWKMBDHVN') for x in rr for d in ['F','R'])
 assert int(s['WC3'])<=5 and int(s['GT2'])<=5
for n,h in json.loads((p/'SHA256SUMS.json').read_text()).items():assert hashlib.sha256((p/n).read_bytes()).hexdigest()==h,n
print('PASS: release table counts, sequences, risk bounds, evidence and SHA256')
