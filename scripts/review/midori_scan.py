from pathlib import Path
from Bio import SeqIO
from collections import Counter
import csv,gzip,json,re,hashlib,subprocess
root=Path(__file__).resolve().parents[2];work=root/'work/review';db=work/'midori'
ns={'__file__':str(work/'scan.py')};exec((work/'scan.py').read_text().split('results=[]; insertrows=[]')[0],ns)
scan,assays=ns['scan'],ns['assays']

def one_species(gene,filename):
 best={}; total=0;missing=0
 with gzip.open(db/filename,'rt') as f:
  for rec in SeqIO.parse(f,'fasta'):
   total+=1; text=rec.description
   fields=dict(re.findall(r'(?:tax=|,)([kpcofgs]):([^,;]+)',text))
   species=fields.get('s',''); species=re.sub(r'_\d+$','',species).strip()
   if not species or species.lower() in ('unclassified','unknown') or ' sp.' in species:missing+=1;continue
   seq=str(rec.seq).upper()
   if species not in best or len(seq)>len(best[species][0]):best[species]=(seq,fields,text.split(';')[0])
 fasta=db/f'{gene}_one_per_species.fasta'; metadata={}
 with fasta.open('w') as out:
  for i,(species,(seq,fields,acc)) in enumerate(sorted(best.items()),1):
   key=f'{gene}_{i}';metadata[key]=dict(species=species,phylum=fields.get('p',''),class_=fields.get('c',''),target='Holothuroidea' in fields.get('c',''),accession=acc)
   out.write(f'>{key}\n{seq}\n')
 print(gene,'records',total,'excluded_without_named_species',missing,'species',len(best),flush=True)
 return fasta,metadata,{'records':total,'excluded_without_named_species':missing,'named_species':len(best),'sha256_gz':hashlib.file_digest((db/filename).open('rb'),'sha256').hexdigest()}
files={'16S':'MIDORI2_UNIQ_NUC_GB273_lrRNA_SINTAX.fasta.gz','COI':'MIDORI2_UNIQ_NUC_GB273_CO1_SINTAX.fasta.gz'}
reference={gene:one_species(gene,path) for gene,path in files.items()}
result=[];members=[]
for assay,(gene,fwd,rev) in assays.items():
 fasta,metadata,summary=reference[gene]
 for e in range(3):
  found=scan(assay,gene,fwd,rev,fasta,e,'midori'); target=sum(metadata[k]['target'] for k in found)
  result.append(dict(assay=assay,mismatches=e,target=target,nontarget=len(found)-target,total=len(found),pct_target=round(100*target/len(found),2) if found else ''))
  for k,seq in found.items():members.append(dict(assay=assay,mismatches=e,**metadata[k],insert_length=len(seq)))
  print(assay,e,result[-1],flush=True)
for name,data,fields in [('midori_summary.csv',result,['assay','mismatches','target','nontarget','total','pct_target']),('midori_hits.csv',members,['assay','mismatches','species','phylum','class_','target','accession','insert_length'])]:
 with (work/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
(work/'midori_input_summary.json').write_text(json.dumps({g:r[2] for g,r in reference.items()},indent=2)+'\n')
