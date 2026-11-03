from pathlib import Path
import csv,json,sys,itertools,shutil,subprocess,collections,tempfile
from Bio import SeqIO
from chemistry import expand,thermal,deg
p=Path(__file__).resolve().parents[1];g=sys.argv[1];d=p/g
def read(path,delim=','):
 with path.open() as f:return list(csv.DictReader(f,delimiter=delim))
def write(path,rs):
 with path.open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
def band(span):
 return next(k for k,n in [('XS',185),('S',210),('M',250),('L',350),('XL',470)] if span<=n)
al={x.id.removeprefix('_R_'):str(x.seq).upper() for x in SeqIO.parse(d/'aligned.fasta','fasta')};anchor=(d/'anchor.txt').read_text().strip();cols=[i for i,c in enumerate(al[anchor]) if c!='-'];panel=read(d/'target_panel.csv')
def evaluable(q):
 a,b,c,e=[cols[int(q[k])-1] for k in ('F_start','F_end','R_start','R_end')];return {x['accession'] for x in panel if (s:=al[x['accession']]) and len(s)-len(s.lstrip('-'))<=a and len(s.rstrip('-'))>e and set(s[a:b+1]+s[c:e+1])<=set('ACGT-')}
def score(q,h):
 ids=evaluable(q);r=[i for i in h if i['role']=='target' and i['accession'] in ids];bg=[i for i in h if i['role']=='background'];return dict(evaluable=len(ids),covered=sum(i['le2last3']=='1' for i in r),exact=sum(i['exact']=='1' for i in r),**{k:sum(i['model']==model and i[col]=='1' for i in bg) for k,model,col in [('WC','WC','le2last3'),('GT','GT','le2last3'),('WC3','WC','le3'),('GT2','GT','le2')]})
def groups(path):
 out=collections.defaultdict(list)
 with path.open() as f:
  for r in csv.DictReader(f,delimiter='\t'):out[r['name']].append(r)
 return out
def ok(q):return max(q['WC'],q['GT'])<=10 and max(q['WC3'],q['GT2'])<=50
pool=[]
for src in [d,p/"extended"/g]:
 h=groups(src/'independent_hits.tsv')
 for q in json.loads((src/'candidates.json').read_text()):
  if max(q['deg_F'],q['deg_R'])==1:continue
  q.update(score(q,h[q['id']]))
  if ok(q) and q["covered"]>0:pool.append(q)
 del h
chosen={};allpairs=[]
for b in ['XS','S','M','L','XL']:
 candidates=[q for q in pool if band(q['span'])==b]
 if not candidates:continue
 if g=="12S":candidates=[q for q in candidates if q["covered"]>=0.80*max(x["covered"] for x in candidates)]
 if g=="COI":candidates=[q for q in candidates if q["evaluable"]>=0.95*max(x["evaluable"] for x in candidates)]
 best=max(candidates,key=lambda q:(q['exact'],q['covered'],-q['GT']) if g=='12S' else (q['covered'],q['exact'],q['evaluable'],-q['GT']))
 chosen[b]=best;allpairs.append((b+'D',best['F'],best['R']))
 for i,(f,r) in enumerate(itertools.product(expand(best['F']),expand(best['R']))):
  if thermal(f,r)[0]:allpairs.append((b+'_'+str(i),f,r))
v=d/'verification';v.mkdir(exist_ok=True)
for n in ['target.fasta','background.fasta']:shutil.copy(d/n,v/n)
(v/'independent_primers.tsv').write_text(''.join('\t'.join(t)+'\n' for t in allpairs))
with tempfile.TemporaryDirectory() as tmp, (v/'run.log').open('w') as f:
 exe=Path(tmp)/'scan';subprocess.run(['c++','-O3','-std=c++17',str(p/'scripts/raw_scan.cpp'),'-o',str(exe)],check=True);subprocess.run([str(exe),str(v)],stderr=f,check=True)
hh=groups(v/'independent_hits.tsv');results=[];detail=[]
for b,q in chosen.items():
 choices=[]
 for k,f,r in allpairs:
  if k!=b+'D' and not k.startswith(b+'_'):continue
  z=dict(gene=g,window=b,name=k,F=f,R=r,deg_F=deg(f),deg_R=deg(r),**{x:q[x] for x in ['F_start','F_end','R_start','R_end','span']},**score(q,hh[k]));choices.append(z)
 plain=max([z for z in choices if '_' in z['name']],key=lambda z:(z['covered'],z['exact'],-z['GT']));mix=next(z for z in choices if z['name']==b+'D')
 for z in [plain,mix]:
  hits=hh[z['name']];z['name']=b if z is plain else b+'D';results.append(z)
  detail.extend(dict(name=z['name'],role=h['role'],model=h['model'],accession=h['accession'],exact=h['exact'],covered=h['le2last3']) for h in hits if h['le2last3']=='1')
write(d/'pairs.csv',results);write(d/'hits.csv',detail)
(d/'primers.fasta').write_text(''.join(f">{g}_{z['name']}_{k}\n{z[k]}\n" for z in results for k in 'FR'));print(g,[(z['name'],z['evaluable'],z['covered'],z['exact'],z['GT']) for z in results],flush=True)
