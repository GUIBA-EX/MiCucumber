from pathlib import Path
from Bio import SeqIO
from collections import Counter
import csv,json
root=Path(__file__).resolve().parents[2]; work=root/'work/review'
ns={'__file__':str(work/'scan.py')};exec((work/'scan.py').read_text().split('results=[]; insertrows=[]')[0],ns)
scan,assays,meta=ns['scan'],ns['assays'],ns['meta']
aln={r.id.removeprefix('_R_'):r for r in SeqIO.parse(root/'markers/12S_COI/COI/aligned.fasta','fasta')}
anchor=(root/'markers/12S_COI/COI/anchor.txt').read_text().strip()
cols=[i for i,b in enumerate(str(aln[anchor].seq)) if b!='-']
with open(root/'markers/12S_COI/COI/pairs.csv') as f: row=next(r for r in csv.DictReader(f) if r['name']=='LD')
a,b,c,d=[cols[int(row[k])-1] for k in ('F_start','F_end','R_start','R_end')]
with open(root/'markers/12S_COI/COI/target_panel.csv') as f: coimeta=list(csv.DictReader(f))
ids={r['accession'] for r in coimeta if (s:=str(aln[r['accession']].seq).upper()) and len(s)-len(s.lstrip('-'))<=a and len(s.rstrip('-'))>d and set(s[a:b+1]+s[c:d+1])<=set('ACGT-')}
print('COI previous alignment evaluability',len(ids),flush=True)
out=[]
for assay,(gene,fwds,revs) in assays.items():
 if gene=='16S':
  path=root/('results/species_qc/panel_S.csv' if assay in ('16S SD','hol.11') else 'results/species_qc/panel_L.csv')
  with path.open() as f: panel=list(csv.DictReader(f))
  orders={r['accession']:r['order'] for r in panel}; inp=work/'16S_all.fasta'
 else:
  orders={r['accession']:r['order'] for r in coimeta if r['accession'] in ids};inp=root/'markers/12S_COI/COI/target.fasta'
 counts={e:set(scan(assay,gene,fwds,revs,inp,e,'byorder')) for e in range(3)}
 for order in sorted(set(orders.values())|{'ALL'}):
  subset={a for a,o in orders.items() if order=='ALL' or o==order}
  out.append(dict(assay=assay,order=order,n=len(subset),e0=len(subset&counts[0]),e1=len(subset&counts[1]),e2=len(subset&counts[2])))
 # Directly compare newly curated sequences; denominator is explicit.
 ext=root/f'results/external_panel/{gene}_target.fasta'
 found={e:set(scan(assay,gene,fwds,revs,ext,e,'external')) for e in range(3)}
 with open(root/'results/external_panel/predictions.csv') as f:
  rows=list(csv.DictReader(f))
 legacy={'16S SD':'SD-Dendrochirotida','16S LD':'LD-Elasipodida','COI LD':'LD','hol.11':None}[assay]
 evalids={r['accession'] for r in rows if r['gene']==gene and r['assay']==legacy and r['role']=='target' and r['evaluable']=='1'}
 out.append(dict(assay=assay,order='EXTERNAL',n=len(evalids),e0=len(evalids&found[0]),e1=len(evalids&found[1]),e2=len(evalids&found[2])))
with (work/'by_order.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['assay','order','n','e0','e1','e2']);w.writeheader();w.writerows(out)
print(json.dumps(out,indent=2),flush=True)
