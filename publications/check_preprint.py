from pathlib import Path
import csv,json,hashlib,re
import subprocess
repo=Path(__file__).resolve().parents[1];name=repo.name;p=repo/'publications';md=(p/f'{name}_preprint.md').read_text();prov=json.loads((p/'preprint_provenance.json').read_text())
from tables import generated_tables
for number,blocks in generated_tables().items():
 for block in blocks:assert block in md,f'Table {number} differs from source CSV'
for gene in ('12S','COI'):
 assert (p/f'figures/{gene}_positions.png').read_bytes()==(repo/f'markers/12S_COI/figures/positions_{gene}.en.png').read_bytes()
text=subprocess.check_output(['pdftotext','-layout',str(p/f'{name}_preprint.pdf'),'-'],text=True)
pages=[x for x in text.split('\f') if x.strip()]
assert '\n**Fei Xia**\n' in md
assert all(len(x.strip())>150 for x in pages)
assert not any(x in md for x in ['author confirmation','To be completed','49 labels','A/B alternatives'])
assert 'Computational assistance' not in md and 'OpenAI Codex' not in md
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
for number in range(5,13):assert f'Figure{number}.' in flat,number
assert 'Computationalassistance' not in flat and 'OpenAICodex' not in flat
diagnostic=repo/'results/anth28s_evaluation/results'
validation=json.loads((diagnostic/'validation.json').read_text());independent=json.loads((diagnostic/'independent_validation.json').read_text())
assert validation['status']==independent['status']=='PASS' and validation['pair_count']==29
for f,d in validation['input_sha256'].items():assert hashlib.sha256((repo/f).read_bytes()).hexdigest()==d,f
assert independent['full_released_score_checks']==87 and independent['threshold_flag_checks']==1578 and independent['identity_recalculation_checks']==465
identities=list(csv.DictReader((diagnostic/'identity_summary.csv').open()));assert len(identities)==15
assert sum(sum(1 for _ in csv.DictReader(f.open())) for f in diagnostic.glob('*_identity.csv'))==130599
lineage=repo/'results/lineage_evaluation'
checks=json.loads((lineage/'comparison_checks.json').read_text())
independent=json.loads((lineage/'independent_checks.json').read_text())
assert checks['status']==independent['status']=='PASS'
assert independent['accession_flag_checks']==170088 and len(independent['assays'])==6
assert all(row['disagreements']==0 for row in independent['assays'])
for f,d in checks['input_sha256'].items():assert hashlib.sha256((repo/f).read_bytes()).hexdigest()==d,f
for scheme in ('SD-Dendrochirotida','LD-Elasipodida'):
 figure=f'figures/base_matching_{scheme}.svg'
 assert figure in md and figure in prov['inputs']
 for file in ('README.md','README.zh-CN.md'):assert figure in (repo/file).read_text()
external=repo/'results/external_panel'
verification=json.loads((external/'verification.json').read_text())
assert verification['status']=='PASS' and verification['assays']==33
prior=set((external/'historical_accessions.txt').read_text().splitlines())
panel=list(csv.DictReader((external/'panel.csv').open()))
assert all(r['accession'].split('.')[0] not in prior for r in panel)
assert len({(r['gene'],r['role'],r['species']) for r in panel})==len(panel)
predictions=list(csv.DictReader((external/'predictions.csv').open()))
assert len(predictions)==verification['independent_strict_and_exact_accession_checks']
groups={}
for r in predictions:
 groups.setdefault((r['gene'],r['assay'],r['role']),[]).append(r)
assert len(groups)==2*verification['assays']-10  # No 12S target references.
for r in csv.DictReader((external/'summary.csv').open()):
 rows=groups.get((r['gene'],r['assay'],r['role']),[])
 n,exact,strict,limited=map(int,(r['evaluable'],r['exact'],r['strict'],r['limited']))
 assert len(rows)==int(r['panel_n']) and 0<=exact<=strict<=limited<=n<=len(rows)
 assert sum(x['evaluable']=='1' for x in rows)==n
 for key in ('exact','strict','limited','strict_GT'):
  if r[key]:assert sum(x[key]=='1' for x in rows)==int(r[key])
result=dict(project=name,author='Fei Xia',pages=len(pages),checks=['source input hashes','artifact hashes','all released primer sequences in PDF and Markdown','all Tables 1–12 against source CSV', 'binding figures against current marker figures', 'common-panel table against CSV','conditional holdout table against CSV','eight diagnostic figures and captions','six independent lineage comparisons','29-assay diagnostic verification','15 barcode matrices and 130599 comparisons','external panel accession exclusion and prediction totals','requested section removed','no near-empty final page'],status='PASS')
(p/'preprint_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(name,'PASS',len(pages),'pages')
