from pathlib import Path
import csv,json,hashlib,re
from pypdf import PdfReader
repo=Path(__file__).resolve().parents[1];name=repo.name;p=repo/'publications';md=(p/f'{name}_preprint.md').read_text();pdf=PdfReader(p/f'{name}_preprint.pdf');text='\n'.join(x.extract_text() for x in pdf.pages);prov=json.loads((p/'preprint_provenance.json').read_text())
assert pdf.metadata.author=='Fei Xia' and '\nFei Xia\n' in md
assert all(len(x.extract_text())>500 for x in pdf.pages)
assert not any(x in md for x in ['author confirmation','To be completed','49 labels','A/B alternatives'])
for f,d in prov['inputs'].items():assert hashlib.sha256((repo/f).read_bytes()).hexdigest()==d,f
for f,d in prov['artifacts'].items():assert hashlib.sha256((p/f).read_bytes()).hexdigest()==d,f
flat=re.sub(r'\s+','',text)
for x in csv.DictReader((repo/'sequences/primer_pairs.csv').open()):
 for side in ['F','R']:assert x[side] in md and x[side] in flat,(x['name'],side)
n=prov['common_species']
for x in csv.DictReader((repo/'results/computational_evaluation/results/panel_comparison.csv').open()):
 if x['panel']=='common':assert f"| {x['name']} | {x['covered']}/{n} | {x['exact']}/{n} | {x['covered_identity_unique']}/{n} |" in md
for x in csv.DictReader((repo/'results/computational_evaluation/results/cv_summary.csv').open()):assert f"| {x['region']} | {x['n']} | {x['covered']} ({float(x['coverage_pct']):.2f}%) | {x['exact']} ({float(x['exact_pct']):.2f}%) |" in md
for cap,rel in re.findall(r'!\[(.*?)\]\((.*?)\)',md):assert (p/rel).exists()
result=dict(project=name,author=pdf.metadata.author,pages=len(pdf.pages),checks=['source input hashes','artifact hashes','all released primer sequences in PDF and Markdown','common-panel table against CSV','conditional holdout table against CSV','figure files','no near-empty final page'],status='PASS')
(p/'preprint_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(name,'PASS',len(pdf.pages),'pages')
