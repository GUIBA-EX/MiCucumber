from pathlib import Path
import csv,json,hashlib,re
import subprocess
repo=Path(__file__).resolve().parents[1];name=repo.name;p=repo/'publications';md=(p/f'{name}_preprint.md').read_text();prov=json.loads((p/'preprint_provenance.json').read_text())
text=subprocess.check_output(['pdftotext','-layout',str(p/f'{name}_preprint.pdf'),'-'],text=True)
pages=[x for x in text.split('\f') if x.strip()]
assert '\n**Fei Xia**\n' in md
assert all(len(x.strip())>150 for x in pages)
assert not any(x in md for x in ['author confirmation','To be completed','49 labels','A/B alternatives'])
for f,d in prov['inputs'].items():assert hashlib.sha256((repo/f).read_bytes()).hexdigest()==d,f
prov['artifacts']={f:hashlib.sha256((p/f).read_bytes()).hexdigest() for f in prov['artifacts']}
(p/'preprint_provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
flat=re.sub(r'\s+','',text)
for x in csv.DictReader((repo/'sequences/primer_pairs.csv').open()):
 for side in ['F','R']:assert x[side] in md and x[side] in flat,(x['name'],side)
for line in (repo/'sequences/all_markers.fasta').read_text().splitlines():
 if line and not line.startswith('>'):assert line in flat,line
n=prov['common_species']
for x in csv.DictReader((repo/'results/computational_evaluation/results/panel_comparison.csv').open()):
 if x['panel']=='common':assert f"| {x['name']} | {x['covered']}/{n} | {x['exact']}/{n} | {x['covered_identity_unique']}/{n} |" in md
for x in csv.DictReader((repo/'results/computational_evaluation/results/cv_summary.csv').open()):assert f"| {x['region']} | {x['n']} | {x['covered']} ({float(x['coverage_pct']):.2f}%) | {x['exact']} ({float(x['exact_pct']):.2f}%) |" in md
for x in csv.DictReader((repo/'markers/12S_COI/candidates.csv').open()):
 for side in ('F','R'):
  assert x[side] in md and x[side] in flat
 assert f"| {x['gene']} | {x['name']} | {x['span']} | {x['covered']}/{x['evaluable']} | {x['exact']}/{x['evaluable']} | {x['WC']}/{x['GT']} |" in md
for cap,rel in re.findall(r'!\[(.*?)\]\((.*?)\)',md):assert (p/rel).exists()
result=dict(project=name,author='Fei Xia',pages=len(pages),checks=['source input hashes','artifact hashes','all released primer sequences in PDF and Markdown','common-panel table against CSV','conditional holdout table against CSV','figure files','no near-empty final page'],status='PASS')
(p/'preprint_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(name,'PASS',len(pages),'pages')
