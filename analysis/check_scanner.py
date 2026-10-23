"""Independent exhaustive position checks on synthetic/real small records."""
from pathlib import Path
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.Data.IUPACData import ambiguous_dna_values as I
import random,json,tempfile
from scan_core import database,flexible_hits
p=Path(__file__).resolve().parent;random.seed(261024)
qs=['GWWAGACGARAAGACCCTG','CCCTRCGGTAACTWTTTCYG','GACCGTGCWAAGGTAGCATAATMAYTTGT']
records=[]
for i,q in enumerate(qs):
 s=''.join(random.choice(I[c]) for c in q)
 records.extend([(f'exact{i}','ACGT'*15+s+'TCGA'*10),(f'reverse{i}','GCTA'*12+str(Seq(s).reverse_complement())+'AACC'*10),(f'ambiguous{i}','CCCC'+s[:8]+'N'+s[9:]+'GGGG')])
records.extend((r.id,str(r.seq)) for r in list(SeqIO.parse(p/'background.fasta','fasta'))[:5])
f=p/'scanner_test.fasta';f.write_text(''.join(f'>{k}\n{s}\n' for k,s in records));db=database(f)
seqmap={k:s for k,s in records};checks=0
for q in qs:
 for side in ['F','R']:
  for wobble,limit in [(False,4),(True,2)]:
   actual=flexible_hits(db,q,side,limit,wobble)
   pr=q if side=='F' else str(Seq(q).reverse_complement())
   allowed=[]
   for c in pr:
    bs=set(I[c])
    if wobble:
     if side=='F':
      if 'G' in bs:bs.add('A')
      if 'T' in bs:bs.add('C')
     else:
      if 'C' in bs:bs.add('T')
      if 'A' in bs:bs.add('G')
    allowed.append(bs)
   for rec,ref in enumerate(db[3]):
    raw=seqmap[ref['accessions'][0]];canon=min(raw,str(Seq(raw).reverse_complement()));s=canon if ref['orientation']=='+' else str(Seq(canon).reverse_complement());expected=[]
    for pos in range(len(s)-len(q)+1):
     t=s[pos:pos+len(q)];mm=[not bool(set(I[c])&a) for c,a in zip(t,allowed)]
     if sum(mm)<=limit:expected.append((pos,sum(mm),sum(mm[-5:] if side=='F' else mm[:5]),sum(c not in 'ACGT' for c in t)))
    assert sorted(actual.get(rec,[]))==expected,(q,side,wobble,rec)
    checks+=1
(p/'scanner_test_result.json').write_text(json.dumps(dict(status='PASS',record_primer_model_checks=checks,scope='independent exhaustive windows on synthetic and 5 real background records; not final-candidate full-database audit'),indent=2));print('PASS',checks)
