"""Validate the downloaded sequence collection and prepare the data-only handoff."""
from pathlib import Path
import csv,gzip,hashlib,json,re,zipfile
from collections import Counter
from Bio import SeqIO
root=Path(__file__).resolve().parents[1];dl=root/'downloads'
requested=set()
for g in ('12S','COI'):
 for suffix,key in [('search','ids'),('aliases','additional_uids')]:
  v=json.loads((dl/f'{g}_{suffix}.json').read_text());requested.update(v[key])
acc=[]
for f in dl.glob('batch*.gz'):
 with gzip.open(f,'rt') as h:acc.extend(line.split()[1] for line in h if line.startswith('VERSION '))
assert len(acc)==len(set(acc))==len(requested)
assert set(acc)==set((root/'downloaded_accessions.txt').read_text().splitlines())
def read(f):
 with f.open() as h:return list(csv.DictReader(h))
audit=read(root/'sequence_audit.csv')
summary={'source':'NCBI Nucleotide','date':'2026-11-04','unique_accessions':len(acc),'genes':{}}
for gene in ['12S','COI']:
 d=root/gene;reps=read(d/'target_panel.csv');meta=[x for x in audit if x['role']=='target' and x['gene']==gene and x['status']=='eligible'];eligible={x['accession'] for x in meta}
 raw=SeqIO.to_dict(SeqIO.parse(d/'all_eligible.fasta','fasta'));assert set(raw)==eligible
 chosen=SeqIO.to_dict(SeqIO.parse(d/'target.fasta','fasta'));assert set(chosen)=={x['accession'] for x in reps};assert len({x['species'] for x in reps})==len(chosen)
 al=SeqIO.to_dict(SeqIO.parse(d/'aligned.fasta','fasta'));aligned_ids={k.removeprefix('_R_') for k in al};anchor=(d/'anchor.txt').read_text().strip();assert aligned_ids==set(chosen)|{anchor};assert len({len(r) for r in al.values()})==1
 for k,r in al.items():
  seq=raw[k.removeprefix('_R_')].seq
  assert str(r.seq).upper().replace('-','')==str(seq.reverse_complement() if k.startswith('_R_') else seq).upper()
 summary['genes'][gene]=dict(eligible=len(raw),representative_species=len(reps),genera=len({x['species'].split()[0] for x in reps}),reference=anchor,length_range=[min(map(len,raw.values())),max(map(len,raw.values()))],source_orders=dict(Counter(x['order'] for x in reps)),alignment_columns=len(next(iter(al.values()))),reverse_oriented=sum(k.startswith('_R_') for k in al),background_representatives=len(read(d/'background_panel.csv')))
 assert eligible=={x['accession'] for x in read(d/'eligible_metadata.csv')}
assert summary==json.loads((root/'summary.json').read_text())
print('PASS: accession counts, taxonomy panels, alignments and sequence restoration')
