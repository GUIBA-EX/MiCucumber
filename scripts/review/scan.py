from pathlib import Path
from collections import defaultdict, Counter
from Bio import SeqIO
from Bio.Seq import Seq
import csv, json, subprocess, zipfile
root=Path(__file__).resolve().parents[2]; work=root/'work/review'; work.mkdir(parents=True,exist_ok=True)
cut=__import__('os').environ.get('CUTADAPT', '/home/yasuda2/miniforge3/envs/ipyrad/bin/cutadapt')
assays={
 '16S SD':('16S',['TAAGAAAGACGARAAGACCCTRTC'],['GAGAAGATGACGCTGTTATCCCTR','AAGGAGATTACGCTGTTATCCCTG']),
 '16S LD':('16S',['AGACTTGTATGAAYGGCRAAACMT','AAACTAGTATGAATGGCTTTTCAT'],['CGCTGTTATCCCTGCRGT']),
 'COI LD':('COI',['AAAATGCGAACYCCAGGARTWAC'],['GGTTCTTGCTTWCCTCTRTARTG']),
 'hol.11':('16S',['AGACGAGAAGACCCTGTC'],['CAATCCAACATCGAGGTC'])}
with zipfile.ZipFile(root/'reproducibility/frozen/xs_inputs.zip') as z:
 (work/'16S_all.fasta').write_bytes(z.read('target.fasta'))
def scan(name, gene, fwds, revs, infile, e, context):
 hits={}; n=0
 for fwd in fwds:
  for rev in revs:
   rc=str(Seq(rev).reverse_complement()); adapter=f'{fwd};min_overlap={len(fwd)};required...{rc};min_overlap={len(rc)};required'
   out=work/f'tmp_{context}_{name}_{e}_{n}.fasta'; n+=1
   subprocess.run([cut,'-j','4','-g',adapter,'-e',str(e),'--no-indels','--revcomp','--discard-untrimmed','-o',str(out),str(infile)],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,check=True)
   for rec in SeqIO.parse(out,'fasta'):
    seq=str(rec.seq).upper(); total=len(seq)+len(fwd)+len(rev)
    low=150 if gene=='16S' else 100
    if 50<=len(seq) and low<=total<=500:
     hits.setdefault(rec.id,seq)
   out.unlink()
 return hits
def rows(path):
 with open(root/path,newline='') as f:return list(csv.DictReader(f))
def write(path, data, fields):
 with (work/path).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
audit={r['accession']:r for r in rows('results/species_qc/sequence_audit.csv')}
coimeta={r['accession']:r for r in rows('markers/12S_COI/COI/eligible_metadata.csv')}
meta={}
for a,r in audit.items():
 name=r['accepted_name'];
 if name:meta[('16S',a)]={'species':name,'order':r['order'],'genus':name.split()[0]}
for a,r in coimeta.items():
 name=r['species']; lin=r['lineage'].split(';'); fam=next((x for x in lin if x.endswith('idae')),'')
 meta[('COI',a)]={'species':name,'order':r['order'],'genus':name.split()[0],'family':fam}
# Exact accepted-name taxonomy from the frozen GBIF matches.
for rec in json.loads((root/'results/species_qc/gbif_matches.json').read_text()):
 name=rec.get('name',''); result=rec.get('match',rec)
 if not isinstance(result,dict):continue
 family=result.get('family','')
 if family:
  for key,val in meta.items():
   if key[0]=='16S' and val['species']==name:val['family']=family
results=[]; insertrows=[]
for name,(gene,fwds,revs) in assays.items():
 inp=work/'16S_all.fasta' if gene=='16S' else root/'markers/12S_COI/COI/all_eligible.fasta'
 panel=root/('results/species_qc/panel_S.csv' if name in ('16S SD','hol.11') else 'results/species_qc/panel_L.csv') if gene=='16S' else root/'markers/12S_COI/COI/target_panel.csv'
 with panel.open(newline='') as f: panelids={r['accession'] for r in csv.DictReader(f)}
 for e in range(3):
  found=scan(name,gene,fwds,revs,inp,e,'target')
  selected=panelids & set(found)
  results.append(dict(assay=name,mismatches=e,panel_records=len(panelids),matched_records=len(selected),matched_species=len({meta[(gene,a)]['species'] for a in selected if (gene,a) in meta})))
  if e==2:
   for acc,seq in found.items():
    if (gene,acc) not in meta:continue
    m=meta[(gene,acc)];insertrows.append(dict(assay=name,accession=acc,species=m['species'],genus=m['genus'],family=m.get('family',''),order=m['order'],insert=seq,length=len(seq),panel=int(acc in panelids)))
 print(name,flush=True)
write('target_matches.csv',results,['assay','mismatches','panel_records','matched_records','matched_species'])
write('target_inserts.csv',insertrows,['assay','accession','species','genus','family','order','insert','length','panel'])
print(json.dumps(results),flush=True)
