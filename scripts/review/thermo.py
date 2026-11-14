from itertools import product
from pathlib import Path
import csv,primer3
work=Path(__file__).resolve().parents[2]/'work/review'
items=[('16S SD','F','TAAGAAAGACGARAAGACCCTRTC'),('16S SD','R','GAGAAGATGACGCTGTTATCCCTR'),('16S SD','R-supp','AAGGAGATTACGCTGTTATCCCTG'),('16S LD','F','AGACTTGTATGAAYGGCRAAACMT'),('16S LD','F-supp','AAACTAGTATGAATGGCTTTTCAT'),('16S LD','R','CGCTGTTATCCCTGCRGT'),('COI LD','F','AAAATGCGAACYCCAGGARTWAC'),('COI LD','R','GGTTCTTGCTTWCCTCTRTARTG'),('hol.11','F','AGACGAGAAGACCCTGTC'),('hol.11','R','CAATCCAACATCGAGGTC')]
codes={'A':'A','C':'C','G':'G','T':'T','R':'AG','Y':'CT','M':'AC','W':'AT','K':'GT','S':'CG','B':'CGT','D':'AGT','H':'ACT','V':'ACG','N':'ACGT'}
rows=[]
for name,role,seq in items:
 vals=[primer3.calc_tm(''.join(x),mv_conc=50,dv_conc=1.5,dntp_conc=.6,dna_conc=50) for x in product(*(codes[b] for b in seq))]
 rows.append(dict(assay=name,oligo=role,sequence=seq,variants=len(vals),tm_min=round(min(vals),2),tm_max=round(max(vals),2)))
with (work/'oligo_tm.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(rows)
