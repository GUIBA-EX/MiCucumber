"""Independent regex-seed verification of sampled raw scans, including 1-mismatch tests.
No C++ scanner functions or released matching functions are imported.
"""
import csv,json,re,zipfile
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1];R=P/'results'
I=dict(A='A',C='C',G='G',T='T',R='AG',Y='CT',S='CG',W='AT',K='GT',M='AC',B='CGT',D='AGT',H='ACT',V='ACG',N='ACGT')
def read(p):return list(csv.DictReader(p.open()))
def fa(text):
 d={}
 for l in text.splitlines():
  if l.startswith('>'):k=l[1:].split()[0];d[k]=''
  else:d[k]+=l.strip().upper()
 return d
rc=lambda s:s.translate(str.maketrans('ACGT','TGCA'))[::-1]
def sites(s,q,reverse=False):
 sets=[set(I[c]) for c in q]
 if reverse:sets=[{rc(c) for c in z} for z in sets[::-1]]
 starts=set()
 for i in range(3):
  a,b=i*len(q)//3,(i+1)*len(q)//3
  pattern='(?='+''.join('['+''.join(sorted(z))+']' for z in sets[a:b])+')'
  starts.update(m.start()-a for m in re.finditer(pattern,s))
 for start in starts:
  if start<0 or start+len(q)>len(s):continue
  t=s[start:start+len(q)]
  if set(t)-set('ACGT'):continue
  bad=[j for j,c in enumerate(t) if c not in sets[j]]
  if len(bad)<=2:yield start,len(bad),not any(j<3 if reverse else j>=len(q)-3 for j in bad)
def scan(seq,p,gene,role):
 best=strict=3;lengths=[set(),set(),set()]
 for strand in (seq,rc(seq)):
  fs=list(sites(strand,p['F']))
  for j,n,t in sites(strand,p['R'],True):
   for i,m,u in fs:
    gap=j-i-len(p['F']);span=j+len(p['R'])-i
    small=gene=='16S' and p['window']=='XS'
    if role=='background':ok=0<=gap<=1000
    else:ok=gap>=(20 if small else 50) and (70 if small else 150 if gene=='16S' else 100)<=span<=500
    if not ok:continue
    k=max(m,n);best=min(best,k)
    if t and u:strict=min(strict,k)
    for z in range(k,3):lengths[z].add(span)
 return best,strict,lengths
count=0
for gene in ('16S','12S','COI'):
 if gene=='16S':
  pairs=read(ROOT/'sequences/primer_pairs.csv')
  for p in pairs:p['window']=p['region']
  target=fa((ROOT/'results/species_qc/representatives.fasta').read_text())
  with zipfile.ZipFile(ROOT/'reproducibility/frozen/xs_inputs.zip') as z:bg=fa(z.read('background.fasta').decode())
 else:
  d=ROOT/f'markers/12S_COI/{gene}';pairs=read(d/'pairs.csv');target=fa((d/'target.fasta').read_text());bg=fa((d/'background.fasta').read_text())
 hh=read(R/f'{gene}_hits.csv');lookup={(r['name'],r['role'],r['accession']):r for r in hh}
 for p in pairs:
  for role,lib in [('target',target),('background',bg)]:
   positives=sorted({r['accession'] for r in hh if r['name']==p['name'] and r['role']==role});negatives=sorted(set(lib)-set(positives))
   for a in positives[:3]+negatives[:3]:
    best,strict,sizes=scan(lib[a],p,gene,role);old=lookup.get((p['name'],role,a),{})
    assert (best,strict)==(int(old.get('min_max_mismatches',3)),int(old.get('min_max_terminal_compatible',3))),(gene,p['name'],role,a)
    # Every threshold is checked, with and without the terminal-three requirement.
    count+=6
summary=read(R/'identity_summary.csv');barcodes=read(R/'barcodes.csv');identities=0
for r in summary:
 group=[b for b in barcodes if b['gene']==r['gene'] and b['window']==r['window']]
 pairs=read(R/f"{r['gene']}_{r['window']}_identity.csv")
 assert len(pairs)==len(group)*(len(group)-1)//2
 for p in pairs[::max(1,len(pairs)//30)]:
  a,b=group[int(p['i'])]['aligned'],group[int(p['j'])]['aligned']
  columns=[(x,y) for x,y in zip(a,b) if (x,y)!=('-','-')]
  identity=100*sum(x==y for x,y in columns)/len(columns)
  assert abs(identity-float(p['identity_pct']))<1e-10
  identities+=1
result=dict(status='PASS',method='independent Python regex-seed paired scan; deterministic hits and non-hits for every primer and both roles',threshold_flag_checks=count,identity_recalculation_checks=identities,full_released_score_checks=len(read(R/'released_score_checks.csv')))
(R/'independent_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
