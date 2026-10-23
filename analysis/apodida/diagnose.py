from pathlib import Path
import sys,csv,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from Bio import SeqIO
from scan_core import rc

import primer3
p=Path(__file__).resolve().parents[1];al={r.id.removeprefix('_R_'):str(r.seq).upper() for r in SeqIO.parse(p/'target_aligned.fasta','fasta')};tax=list(csv.DictReader((p/'target_taxonomy.tsv').open(),delimiter='\t'));ids=[r['accession'] for r in tax if r['order']=='Apodida'];coords=[i for i,c in enumerate(al['AB525437.1']) if c!='-'];out=[]
for s in json.loads((p/'final_selected.json').read_text())[:4]:
 for k in ids:
  for d in ['F','R']:
   a,b=(int(s['left']),int(s['left'])+len(s[d])) if d=='F' else (int(s['right'])-len(s[d]),int(s['right']))
   q=al[k][coords[a]:coords[b-1]+1].replace('-','');q=rc(q) if d=='R' else q
   valid=18<=len(q)<=40 and set(q)<=set('ACGT')
   out.append(dict(locus=s['label'],accession=k,side=d,sequence=q,length=len(q),AAAA='AAAA' in q,Tm=primer3.calc_tm(q,mv_conc=50,dv_conc=1.5,dntp_conc=.6,dna_conc=50) if valid else '',hairpin=primer3.calc_hairpin(q,mv_conc=50,dv_conc=1.5,dntp_conc=.6,dna_conc=50).tm if valid else ''))
with (p/'apodida/diagnostic.tsv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(out[0]),delimiter='\t');w.writeheader();w.writerows(out)
print('Apodida records',len(ids));print(json.dumps([r for r in out if r['Tm']!=''],indent=2))
