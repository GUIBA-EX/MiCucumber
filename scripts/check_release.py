"""Validate the terminal-constrained release against raw paired-product evidence."""
from pathlib import Path
import csv,json,hashlib,zipfile,re,math,itertools,collections,subprocess
p=Path(__file__).resolve().parents[1];I=dict(A='A',C='C',G='G',T='T',R='AG',Y='CT',S='CG',W='AT',K='GT',M='AC',B='CGT',D='AGT',H='ACT',V='ACG',N='ACGT')
def rows(f):return list(csv.DictReader(f.open()))
a=rows(p/'sequences/primer_pairs.csv');assert len(a)==17
expected={reg+s for reg in ['S','M','L','XL'] for s in ['D','','A+'+reg+'B']}|{'MiCucumber-S-original'};assert {r['scheme'] for r in a}==expected
fasta={};key=None
for line in (p/'sequences/primers.fasta').read_text().splitlines():
 if line.startswith('>'):key=line[1:];assert key not in fasta;fasta[key]=''
 else:fasta[key]+=line
assert len(fasta)==34
for r in a:
 for side in ['F','R']:
  q=r[side];assert fasta[f"{r['pair_name']}|{side}|{r['pair_id']}"]==q
  assert int(r['degeneracy_'+side])==math.prod(len(I[c]) for c in q)
  if r['chemistry']=='ordinary':assert set(q)<=set('ACGT')
  if r['chemistry']!='original':
   for s in map(''.join,itertools.product(*(I[c] for c in q))):
    assert len(set(s[-3:]))>1 and any(c in 'GC' for c in s[-3:])
    assert 1<=sum(c in 'GC' for c in s[-5:])<=4 and not any(c*5 in s for c in 'ACGT')
 if r['chemistry']=='original':assert r['F']=='GWWAGACGARAAGACCCTG' and r['R']=='CCCTRCGGTAACTWTTTCYG'
for reg in ['S','M','L','XL']:assert rows(p/f'sequences/MiCucumber-{reg}.csv')==[r for r in a if r['region']==reg]
sel=json.loads((p/'results/terminal_optimization/selection.json').read_text());sd={r['name']:r for r in sel};pairs=rows(p/'results/current/primer_pairs.csv');assert len(pairs)==17
for r in pairs:
 if r['name']!='S-original':assert (r['F'],r['R'])==(sd[r['name']]['F'],sd[r['name']]['R'])
assert {r['name']:(r['F'],r['R']) for r in pairs}=={('S-original' if r['chemistry']=='original' else r['pair_name']):(r['F'],r['R']) for r in a}
h=collections.defaultdict(set)
for r in csv.DictReader((p/'results/terminal_optimization/independent_hits.tsv').open(),delimiter='\t'):
 for flag in ['exact','le2last3','le2','le3','le4']:
  if r[flag]=='1':h[r['name'],r['role'],r['model'],flag].add(r['accession'])
panel=rows(p/'results/matching/panel.csv');weights={r['accession']:float(r['weight']) for r in panel};nw={r['accession']:float(r['weight']) for r in panel if r['order']!='Apodida'};comp=rows(p/'results/current/comparison.csv');assert len(comp)==13 and comp==rows(p/'results/comparison.csv')
for r in comp:
 pp=[x for x in pairs if x['scheme']==r['scheme']];assert len(pp)==int(r['pairs'])
 def union(role,model,flag):return set().union(*(h[x['name'],role,model,flag] for x in pp))
 for flag,col in [('le2last3','coverage_pct'),('exact','exact_pct')]:
  hit=union('target','WC',flag)
  assert math.isclose(100*sum(nw.get(x,0) for x in hit)/sum(nw.values()),float(r[col]),abs_tol=1e-8)
  assert math.isclose(100*sum(weights.get(x,0) for x in hit)/sum(weights.values()),float(r['all_target_'+col]),abs_tol=1e-8)
 for model,flag,col in [('WC','le3','WC3'),('GT','le2','GT2'),('WC','le4','WC4')]:assert len(union('background',model,flag))==int(r[col])
 if r['scheme']!='S-original':
  limit={'SD':50,'LD':20}.get(r['scheme'],5);assert int(r['WC3'])<=limit and int(r['GT2'])<=limit
for r in rows(p/'results/terminal_optimization/thermal.csv'):
 assert float(r['structure_max'])<55
 assert abs((float(r['F_tm_min'])+float(r['F_tm_max'])-float(r['R_tm_min'])-float(r['R_tm_max']))/2)<=5
v=json.loads((p/'results/terminal_optimization/verification.json').read_text());assert v['checks']==11200 and v['disagreements']==0 and v['background_checks']==32 and v['background_disagreements']==0
# Read frozen source reference to check the map independently of rendered text.
with zipfile.ZipFile(p/'results/terminal_optimization/reproduction_sources.zip') as z:
 assert z.testzip() is None
 lines=z.read('work/micucumber_terminal/target_aligned.fasta').decode().splitlines()
ref='';collect=False
for line in lines:
 if line.startswith('>'):collect=line[1:].split()[0]=='AB525437.1'
 elif collect:ref+=line.upper().replace('-','')
assert ref
coords=rows(p/'results/current/binding_positions.csv');assert len(coords)==16 and {r['name'] for r in coords}==set(sd)
for r in coords:
 for side in ['F','R']:
  a0,b=int(r[side+'_start']),int(r[side+'_end']);q=sd[r['name']][side];assert b-a0+1==len(q)
  t=ref[a0-1:b]
  if side=='R':t=t.translate(str.maketrans('ACGT','TGCA'))[::-1]
  assert t==r[side+'_reference_5to3'] and q==r[side+'_sequence']
  assert sum(c not in I[n] for n,c in zip(q,t))==int(r[side+'_reference_mismatches'])
 assert int(r['reference_span_bp'])==int(r['R_end'])-int(r['F_start'])+1
for reg in ['S','M','L','XL']:
 group=[r for r in coords if r['name'] in {reg,reg+'A',reg+'B',reg+'D'}]
 assert len(group)==4
 assert len({tuple(r[k] for k in ['F_start','F_end','R_start','R_end']) for r in group})==1,reg
 assert (sd[reg+'A']['F'],sd[reg+'A']['R'])!=(sd[reg+'B']['F'],sd[reg+'B']['R']),reg
for r in rows(p/'results/current/joint_locus.csv'):
 q=next(x for x in coords if x['name']==r['region'])
 assert all(r[k]==q[k] for k in ['F_start','F_end','R_start','R_end','reference_span_bp'])
manifest=json.loads((p/'SHA256SUMS.json').read_text())
for name,digest in manifest.items():assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest,name
for doc in [p/n for n in manifest if n.endswith('.md')]:
 for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
  if not link.startswith(('http:','https:','#')):assert (doc.parent/link.split('#')[0]).exists(),(doc,link)
for link in re.findall(r'(?:href|src)="([^"]+)"',(p/'report.html').read_text()):assert (p/link).exists(),link
print('PASS: 13 portfolios, 17 pairs, 34 sequences, all-variant terminal rules, both thermal scenarios, raw metrics, 16 reference intervals, original control, links and hashes')
