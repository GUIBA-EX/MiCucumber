from pathlib import Path
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Data.IUPACData import ambiguous_dna_values as codes
import csv,random
root=Path(__file__).resolve().parents[2];work=root/'work/review';ns={'__file__':str(work/'scan.py')};exec((work/'scan.py').read_text().split('results=[]; insertrows=[]')[0],ns);assays=ns['assays']
meta={}
for gene in ('16S','COI'):
 # MIDORI normalized reference file order is deterministic by species name.
 for r in SeqIO.parse(work/'midori'/f'{gene}_one_per_species.fasta','fasta'):meta[(gene,r.id)]=str(r.seq).upper()
def candidates(primer,seq):
 return [i for i in range(len(seq)-len(primer)+1) if sum(t not in codes[p] for p,t in zip(primer,seq[i:i+len(primer)]))<=2]
def matches(seq,gene,fwds,revs):
 for s in (seq,str(Seq(seq).reverse_complement())):
  for fwd in fwds:
   ff=candidates(fwd,s)
   for rev in revs:
    rc=str(Seq(rev).reverse_complement());rr=candidates(rc,s)
    for a in ff:
     for b in rr:
      length=b+len(rc)-a;insert=b-a-len(fwd)
      if insert>=50 and (150 if gene=='16S' else 100)<=length<=500:return True
 return False
# Regenerate MIDORI id-to-species table by sorted names from headers in full source.
import gzip,re
names={}
for gene,file in [('16S','MIDORI2_UNIQ_NUC_GB273_lrRNA_SINTAX.fasta.gz'),('COI','MIDORI2_UNIQ_NUC_GB273_CO1_SINTAX.fasta.gz')]:
 species=set()
 with gzip.open(work/'midori'/file,'rt') as f:
  for r in SeqIO.parse(f,'fasta'):
   fields=dict(re.findall(r'(?:tax=|,)([kpcofgs]):([^,;]+)',r.description)); n=re.sub(r'_\d+$','',fields.get('s','')).strip()
   if n and n.lower() not in ('unclassified','unknown') and ' sp.' not in n:species.add(n)
 names.update({(gene,n):f'{gene}_{i}' for i,n in enumerate(sorted(species),1)})
with (work/'midori_hits.csv').open() as f:rows=list(csv.DictReader(f))
rng=random.Random(1848);checks=0
for assay in assays:
 rows2=[r for r in rows if r['assay']==assay and r['mismatches']=='2' and r['target']=='False']
 for r in rng.sample(rows2,min(25,len(rows2))):
  gene,fwds,revs=assays[assay]; sid=names[(gene,r['species'])];seq=meta[(gene,sid)]
  assert matches(seq,gene,fwds,revs),(assay,r['species']);checks+=1
print(f'PASS: {checks} independently rechecked MIDORI2 non-target hits')
