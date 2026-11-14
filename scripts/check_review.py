from pathlib import Path
import csv,re,json,hashlib
root=Path(__file__).resolve().parents[1]
def read(path):
 with (root/path).open(newline='') as f:return list(csv.DictReader(f))
def find(rows,**kwargs):return next(r for r in rows if all(r[k]==str(v) for k,v in kwargs.items()))
main=(root/'publications/submission/MiCucumber_revision.md').read_text()
counts=read('results/complementarity/by_order.csv');coi=read('results/complementarity/coi_worms_coverage.csv');bg=read('results/specificity/midori_summary.csv');resolution=read('results/resolution/resolution.csv')
for assay,n,exact,one,two in [('16S SD',174,1,46,155),('16S LD',174,29,66,99),('hol.11',174,122,161,163)]:
 r=find(counts,assay=assay,order='ALL');assert [int(r[k]) for k in ('n','e0','e1','e2')]==[n,exact,one,two]
r=find(coi,order='ALL');assert [int(r[k]) for k in ('n','e0','e1','e2')]==[274,10,58,118]
for assay,target,other in [('16S SD',177,7),('16S LD',115,45),('COI LD',121,0),('hol.11',193,49352)]:
 r=find(bg,assay=assay,mismatches=2);assert (int(r['target']),int(r['nontarget']))==(target,other)
for assay,n,d in [('16S SD',473,483),('16S LD',338,346),('COI LD',666,683),('hol.11',516,525)]:
 r=find(resolution,assay=assay,rank='species');assert (int(r['unique']),int(r['evaluable']))==(n,d)
seq={};name=None
for line in (root/'sequences/detailed_assays.fasta').read_text().splitlines():
 if line.startswith('>'):name=line[1:];assert name not in seq;seq[name]=''
 else:seq[name]+=line.strip()
assert len(seq)==8 and all(s in main for s in seq.values())
all_rows=read('sequences/all_testing_primers.csv')
assert len(all_rows)==61 and len({r['id'] for r in all_rows})==61
all_fasta={};current=None
for line in (root/'sequences/all_testing_primers.fasta').read_text().splitlines():
 if line.startswith('>'):current=line[1:];assert current not in all_fasta;all_fasta[current]=''
 else:all_fasta[current]+=line.strip()
assert all_fasta=={r['id']:r['sequence_5to3'] for r in all_rows}
assert sum(bool(r['supplement']) for r in all_rows)==3
assert set(seq.values()) <= set(all_fasta.values())
assert seq['16S-SD_F']==all_fasta['MiCucumber-16S-SD_F']
assert seq['16S-SD_R']==all_fasta['MiCucumber-16S-SD_R']
for filename in ("README.md", "README.zh-CN.md"):
 text=(root/filename).read_text()
 assert all(primer in text for primer in seq.values()), filename
 assert "figures/MiCucumber_overview_current.png" in text, filename
assert "funding and competing interests" not in main.lower()
assert len(read('publications/submission/supplementary_primers.csv'))==29
for f in ['README.md','README.zh-CN.md','publications/submission/MiCucumber_revision.md','publications/submission/Supplementary.md']:
 p=root/f
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if link.startswith(('https://','http://','#','mailto:')):continue
  assert (p.parent/link.split('#')[0]).exists(),(f,link)
for file in ['MiCucumber_revision.pdf','Supplementary.pdf']:
 assert (root/'publications/submission'/file).read_bytes().startswith(b'%PDF-')
assert main.count('**Table ')==3 and sum(main.count('**Fig. '+str(n)+'**') for n in (1,2,3))==3
print('PASS: matching, taxonomy panels, MIDORI2 hits, reference resolution, primer sequences and document links')

supp=(root/'publications/submission/Supplementary.md').read_text()
assert all(supp.count('**Fig. S'+str(n)+'**')==1 for n in range(1,6))
for text in (main,supp,(root/'publications/submission/Cover_letter.md').read_text()):
 assert 'xf@g.ecc.u-tokyo.ac.jp' in text and 'Fei Xia' in text
 assert not any(x in text for x in ('Xinming Liu','liuxm@gxtcmu.edu.cn','Guangxi University'))
reps=read('publications/submission/figures/Fig1_representatives.csv')
assert len(reps)==len({r['accession'] for r in reps})==31
assert len({r['order'] for r in reps})==7 and len({r['family'] for r in reps})==21
ordinary=read('results/visualization/16S_S/target_matches.csv')
assert [int(r['matched_species']) for r in ordinary]==[5,26,110]
print('PASS: authorship, figure numbering, representative accessions and ordinary S counts')
