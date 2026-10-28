from pathlib import Path
import csv,json,math,re,collections,xml.etree.ElementTree as ET
p=Path(__file__).resolve().parents[1];project=p.name
assert project in ('MiCucumber','MiLily')
def read(f,delimiter=','):
 with f.open() as h:return list(csv.DictReader(h,delimiter=delimiter))
rows=read(p/'sequences/primer_pairs.csv');names=[r['name'] for r in rows];assert set(names)=={'XS','S','SD','M','MD','L','LD','XL','XLD'} and len(names)==len(set(names))
fa={}
for line in (p/'sequences/primers.fasta').read_text().splitlines():
 if line.startswith('>'):k=line[1:];assert k not in fa;fa[k]=''
 else:fa[k]+=line
assert len(fa)==18
I={'A':'A','C':'C','G':'G','T':'T','R':'AG','Y':'CT','S':'CG','W':'AT','K':'GT','M':'AC','B':'CGT','D':'AGT','H':'ACT','V':'ACG','N':'ACGT'}
cp=p/('results/current/binding_positions.csv' if project=='MiCucumber' else 'results/binding_positions.csv');coords={r['name']:r for r in read(cp)};panel=read(p/'results/species_qc/panel.csv');assert len(panel)==len(set(r['species_key'] for r in panel))==(174 if project=='MiCucumber' else 128)
metrics={r['name']:r for r in read(p/'results/current_primers/comparison.csv')};assert set(metrics)==(set(names) if project=='MiCucumber' else set(names)-{'XS'})
for r in rows:
 name=r['name'];reg=r['region'];c=coords['XS' if name=='XS' else reg+'D']
 for side in ('F','R'):
  q=r[side];assert fa[project+'-'+name+'_'+side]==q;assert math.prod(len(I[x]) for x in q)==int(r['degeneracy_'+side]);assert len(q)==int(c[side+'_end'])-int(c[side+'_start'])+1
  if name.endswith('D') or (name=='XS' and project=='MiCucumber'):assert int(r['degeneracy_'+side])<=8 and set(q[:len(q)//2])<=set('ACGT')
  if name in ('S','M','L','XL'):assert set(q)<=set('ACGT')
 if name=='XS' and project=='MiLily':
  assert (r['F'],r['R'])==('TTGGGGCAACCDCGAAG','CAACATCGAGGTCGCAAAC');ET.parse(p/'figures/base_matching_XS.svg');continue
 d=p/'results/current_primers'/reg;m=metrics[name];v=json.loads((d/(name+'_verification.json')).read_text());assert v['disagreements']==v['background_disagreements']==0
 targets={x['accession'] for x in read(p/'results/species_qc'/('panel_'+reg+'.csv'))};hits=collections.defaultdict(set)
 for x in read(d/(name+'_independent_hits.tsv'),'\t'):
  assert x['name']==name
  for flag in ('exact','le2last3','le2','le3','le4'):
   if x[flag]=='1':hits[x['role'],x['model'],flag].add(x['accession'])
 assert len(hits['target','WC','le2last3']&targets)==int(m['covered_labels']);assert len(hits['target','WC','exact']&targets)==int(m['exact_labels'])
 for model,flag,col in [('WC','le3','WC3'),('GT','le2','GT2'),('WC','le4','WC4'),('WC','le2last3','strict_WC'),('GT','le2last3','strict_GT')]:assert len(hits['background',model,flag])==int(m[col]),(name,col)
 bases=read(d/(name+'_base_matching.csv'));assert bases
 for x in bases:assert x['name']==name and x['primer']==r[x['side']]
 ET.parse(d/('base_matching_'+name+'.svg'))
 if name.endswith('D') or name=='XS':
  thermal=json.loads((d/(name+'_thermal.json')).read_text());assert all(v['structure_max']<55 and abs((v['F_tm_min']+v['F_tm_max']-v['R_tm_min']-v['R_tm_max'])/2)<=5 for v in thermal)
for fn in ('README.md','README.zh-CN.md'):
 f=p/fn;s=f.read_text()
 for r in rows:assert f"| {r['name']} | `{r['F']}` | `{r['R']}` |" in s
 for link in re.findall(r'\]\(([^)]+)\)',s):
  if not link.startswith(('http:','https:','#')):assert (f.parent/link.split('#')[0]).exists(),link
print('PASS:',project,len(rows),'pairs; hits, fixed coordinates, degeneracy, diagrams and bilingual links')
