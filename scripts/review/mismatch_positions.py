import csv
from collections import Counter
from pathlib import Path
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Data.IUPACData import ambiguous_dna_values
root=Path(__file__).resolve().parents[2]; work=root/'work/review'
aln={r.id.removeprefix('_R_'):str(r.seq).upper() for r in SeqIO.parse(root/'results/species_qc/curated_alignment.fasta','fasta')}
with open(root/'results/species_qc/panel_S.csv') as f:ids=[r['accession'] for r in csv.DictReader(f)]
coords=next(r for r in csv.DictReader(open(root/'figures/current_region_coordinates.csv')) if r['locus']=='S')
ref=aln[coords['reference']];cols=[i for i,c in enumerate(ref) if c!='-']
pair=next(r for r in csv.DictReader(open(root/'sequences/primer_pairs.csv')) if r['name']=='SD')
result=[]
for side in ('F','R'):
 primer=pair[side];lo,hi=[int(coords[f'{side}_{x}']) for x in ('start','end')];a=cols[max(0,lo-1-15)];b=cols[min(len(cols)-1,hi-1+15)]+1;best=[];ties=0
 for acc in ids:
  s=aln[acc][a:b].replace('-','')
  if side=='R':s=str(Seq(s).reverse_complement())
  options=[]
  for j in range(len(s)-len(primer)+1):
   segment=s[j:j+len(primer)]
   if set(segment)-set('ACGT'):continue
   score=sum(x not in ambiguous_dna_values[y] for x,y in zip(segment,primer));options.append((score,j,segment))
  if not options:continue
  options.sort();ties+=sum(x[0]==options[0][0] for x in options)>1;best.append(options[0][2])
 for i,base in enumerate(primer):
  result.append(dict(oligo=side,position=i+1,base=base,evaluable=len(best),mismatches=sum(s[i] not in ambiguous_dna_values[base] for s in best),counts=';'.join(f'{x}:{n}' for x,n in sorted(Counter(s[i] for s in best).items())),tied_best_records=ties,window_flank_bp=15))
with (work/'sd_position_mismatch.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
print(sorted(result,key=lambda x:x['mismatches'],reverse=True)[:6])
