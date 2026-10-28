from pathlib import Path
import csv,json,math,re
p=Path(__file__).resolve().parents[1]
def read(f):
 with f.open() as h:return list(csv.DictReader(h))
rows=read(p/'sequences/primer_pairs.csv'); names=[x['name'] for x in rows]
assert len(names)==len(set(names)) and not any(re.fullmatch(r'(?:S|M|L|XL)[AB]',x) for x in names)
I={'A':'A','C':'C','G':'G','T':'T','R':'AG','Y':'CT','S':'CG','W':'AT','K':'GT','M':'AC','B':'CGT','D':'AGT','H':'ACT','V':'ACG','N':'ACGT'}
fa={}
for line in (p/'sequences/primers.fasta').read_text().splitlines():
 if line.startswith('>'):k=line[1:];assert k not in fa;fa[k]=''
 else:fa[k]+=line
assert len(fa)==2*len(rows)
for r in rows:
 for side in ('F','R'):
  q=r[side];assert fa[r['name']+'_'+side]==q
  assert math.prod(len(I[c]) for c in q)==int(r['degeneracy_'+side])
  if r['name']!='XS':assert int(r['degeneracy_'+side])<=8 and set(q[:len(q)//2])<=set('ACGT')
 if r['name']!='XS':
  verified=read(p/'results/species_refine'/r['region']/'verified_comparison.csv');z=next(x for x in verified if x['name']==r['name']);assert (z['F'],z['R'])==(r['F'],r['R'])
for f in (p/'results/species_refine').glob('*/verification.json'):
 d=json.loads(f.read_text());assert d['disagreements']==d['background_disagreements']==0
with (p/'results/species_qc/panel.csv').open() as h:panel=list(csv.DictReader(h))
assert len(panel)==len({r['species_key'] for r in panel})
for fn in ('README.md','README.zh-CN.md','results/species_refine/README.md'):
 f=p/fn
 for link in re.findall(r'\]\(([^)]+)\)',f.read_text()):
  if not link.startswith(('https:','http:','#')):assert (f.parent/link.split('#')[0]).exists(),(f,link)
print('PASS',len(rows),'current primer pairs; sequences, degeneracy, independent screening and links')
