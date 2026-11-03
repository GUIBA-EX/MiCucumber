from pathlib import Path
from io import StringIO
from Bio import SeqIO
from Bio.Seq import Seq
import gzip,csv,re,collections,sys,json
root=Path(__file__).resolve().parents[1]; cache=Path(sys.argv[1]); mode=sys.argv[2] if len(sys.argv)>2 else 'final'
def classify(label,mito=False):
 t=label.lower()
 if re.search(r'\b(cox1|coxi|co1|coi|mt-co1)\b|cytochrome (?:c )?oxidase (?:subunit |subunit-)?(?:i|1)\b',t):return 'COI'
 if ('12s' in t or mito) and '18s' not in t and re.search(r'\b(12s|rrns|rns|s-rrna|ssu)\b|small subunit ribosomal|small ribosomal subunit',t):return '12S'
def writecsv(p,rows):
 with p.open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
files=[(x,True) for x in sorted((root/'downloads').glob('batch*.gz'))] if mode=='final' else [(x,True) for x in sorted(cache.glob('*_Holothuroidea_*.gb')) if x.name.startswith(('12S','COI'))]
files += [(x,False) for x in sorted(cache.glob('*.gb')) if x.name.startswith(('12S','COI')) and '_Holothuroidea_' not in x.name]
seen=set();audit=[];data=collections.defaultdict(dict);accessions=set()
def records(handle,target):
 lines=[]
 for line in handle:
  lines.append(line)
  if not line.startswith('//'):continue
  block=''.join(lines).lstrip();lines=[]
  size=int(re.search(r'^LOCUS\s+\S+\s+(\d+)',block).group(1))
  if size>100000:
   acc=re.search(r'^VERSION\s+(\S+)',block,re.M).group(1)
   if target:accessions.add(acc)
   audit.append(dict(accession=acc,species='',gene='',role='target' if target else 'background',order='',lineage='',source='',location='',length=size,ambiguous='',status='large_scaffold'));continue
  yield SeqIO.read(StringIO(block),'genbank')
for file,target in files:
 print('read',file.name,flush=True)
 op=gzip.open(file,'rt') if file.suffix=='.gz' else file.open()
 with op:
  for rec in records(op,target):
   role='target' if target else 'background'
   if (role,rec.id) in seen:continue
   seen.add((role,rec.id));tax=rec.annotations.get('taxonomy',[]);org=rec.annotations.get('organism','');ss={}
   if target:accessions.add(rec.id)
   if rec.id.startswith(('XM_','XR_','NM_')) or re.search(r'methyltransferase|assembly factor|pseudogene|nuclear mitochondrial',rec.description,re.I):
    audit.append(dict(accession=rec.id,species=org,gene='',role=role,order='',lineage=';'.join(tax),source='',location='',length=len(rec),ambiguous='',status='nuclear_or_pseudogene'));continue
   if not rec.seq.defined:
    audit.append(dict(accession=rec.id,species=org,gene='',role=role,order='',lineage=';'.join(tax),source='',location='',length=len(rec),ambiguous='',status='undefined_sequence'));continue
   mito='mitochond' in rec.description.lower() or any('mitochond' in str(f.qualifiers.get('organelle','')).lower() for f in rec.features if f.type=='source')
   for f in rec.features:
    if f.type not in ('gene','CDS','rRNA'):continue
    g=classify(' '.join(f.qualifiers.get('gene',[])+f.qualifiers.get('product',[])),mito)
    if not g or (g=='12S' and f.type=='CDS'):continue
    if g not in ss or f.type!='gene':
     ss[g]=(str(f.extract(rec.seq)).upper(),str(f.location),f.type,int(f.qualifiers.get('codon_start',['1'])[0])-1)
   for g in ['12S','COI']:
    if g not in ss and classify(rec.description,mito)==g and len(rec)<(1400 if g=='12S' else 1650) and not re.search(r'tRNA|transfer RNA|16S|18S|subunit II\b|pseudogene|mRNA|protein|methyltrans|assembly|binding',rec.description,re.I):
     ss[g]=(str(rec.seq).upper(),'whole_record','title',0)
   for g,(s,loc,source,frame) in ss.items():
    ok='eligible';amb=sum(b not in 'ACGT' for b in s)
    conflicting=(source in ('gene','title') and any(other.type=='tRNA' and (source=='title' or any(str(f.location)==loc and len(set(f.location).intersection(other.location))>=20 for f in rec.features if f.type=='gene')) for other in rec.features))
    if conflicting:ok='overlapping_tRNA_annotation'
    elif ('Holothuroidea' in tax)!=target:ok='taxonomy_conflict'
    elif not 120<=len(s)<=(1400 if g=='12S' else 1700):ok='length'
    elif amb>.05*len(s):ok='ambiguity'
    elif g=='COI' and source=='CDS' and '*' in str(Seq(s[frame:frame+((len(s)-frame)//3)*3]).translate(table=9))[:-1]:ok='internal_stop'
    if re.search(r'pseudogene|nuclear mitochondrial',rec.description,re.I):ok='pseudogene'
    row=dict(accession=rec.id,species=org,gene=g,role=role,order=next((x for x in reversed(tax) if x in {'Apodida','Dendrochirotida','Elasipodida','Holothuriida','Molpadida','Persiculida','Synallactida','Aspidochirotida','Dactylochirotida'}),'unassigned') if target else next((x for x in reversed(tax) if x.endswith(('ida','oida')) or x=='Camarodonta'),'unassigned'),lineage=';'.join(tax),source=source,location=loc,length=len(s),ambiguous=amb,status=ok)
    audit.append(row)
    if ok=='eligible':data[g,role][rec.id]=(row,s)
   if not ss:audit.append(dict(accession=rec.id,species=org,gene='',role=role,order='',lineage=';'.join(tax),source='',location='',length=len(rec),ambiguous='',status='no_supported_gene'))
for g in ['12S','COI']:
 d=root/g;d.mkdir(exist_ok=True)
 for role in ['target','background']:
  dr=data[g,role];groups=collections.defaultdict(list)
  for a,(r,s) in dr.items():
   if re.fullmatch(r'[A-Z][a-z-]+ (?:\([A-Z][a-z-]+\) )?[a-z-]+',r['species']):groups[r['species']].append(a)
  reps=[min(aa,key=lambda a:(-len(dr[a][1]),dr[a][0]['ambiguous'],not a.startswith('NC_'),a)) for aa in groups.values()]
  (d/(role+'.fasta')).write_text(''.join(f'>{a}\n{dr[a][1]}\n' for a in sorted(reps)))
  writecsv(d/(role+'_panel.csv'),[dr[a][0] for a in sorted(reps)])
  if role=='target':
   anchor='AB525437.1' if 'AB525437.1' in dr else max(reps,key=lambda a:len(dr[a][1]))
   (d/'anchor.txt').write_text(anchor+'\n')
   (d/'align_input.fasta').write_text(''.join(f'>{a}\n{dr[a][1]}\n' for a in [anchor]+[a for a in sorted(reps) if a!=anchor]))
  if role=='target':(d/'all_eligible.fasta').write_text(''.join(f'>{a}\n{s}\n' for a,(r,s) in dr.items()))
  print(g,role,len(dr),len(reps),flush=True)
writecsv(root/'sequence_audit.csv',audit)
(root/'downloaded_accessions.txt').write_text('\n'.join(sorted(accessions))+'\n')
