import pathlib,csv,json,collections,numpy as np,itertools,sys,time
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Data.IUPACData import ambiguous_dna_values as codes
p=pathlib.Path(__file__).parent
B={b:sum({'A':1,'C':2,'G':4,'T':8}[x] for x in bases) for b,bases in codes.items()}
def rc(s):return str(Seq(s).reverse_complement())
def database(path):
 groups=collections.defaultdict(list)
 for r in SeqIO.parse(path,'fasta'):
  s=str(r.seq).upper();canonical=min(s,rc(s));groups[canonical].append(r.id)
 seqs=[];refs=[]
 for s,ids in groups.items():
  for ori,t in [('+',s),('-',rc(s))]:seqs.append(t);refs.append(dict(accessions=ids,orientation=ori))
 chunks=[];offsets=[];ends=[];off=0
 for s in seqs:
  offsets.append(off);off+=len(s);ends.append(off);chunks.append(np.array([B.get(c,15) for c in s]+[0]*40,dtype=np.uint8));off+=40
 arr=np.concatenate(chunks);amb=~np.isin(arr,[0,1,2,4,8]);prefix=np.concatenate([[0],np.cumsum(amb,dtype=np.int32)])
 return arr,np.array(offsets),np.array(ends),refs,prefix

def flexible_hits(db,primer,side,limit=4,wobble=False):
 arr,offsets,ends,refs,prefix=db;pr=primer if side=='F' else rc(primer);L=len(pr);n=len(arr)-L+1;masks=[]
 for c in pr:
  bs=set(codes[c])
  if wobble:
   if side=='F':
    if 'G' in bs:bs.add('A')
    if 'T' in bs:bs.add('C')
   else:
    if 'C' in bs:bs.add('T')
    if 'A' in bs:bs.add('G')
  masks.append(sum(B[b] for b in bs))
 tail=list(range(L-7,L)) if side=='F' else list(range(7));mis=np.zeros(n,dtype=np.uint8)
 for i in tail:mis+=(arr[i:i+n]&masks[i])==0
 idx=np.flatnonzero(mis<=limit);vals=mis[idx]
 for i in range(L):
  if i not in tail:vals+=(arr[idx+i]&masks[i])==0
 ok=vals<=limit;idx=idx[ok];vals=vals[ok];record=np.searchsorted(offsets,idx,side='right')-1;ok=idx+L<=ends[record];idx=idx[ok];vals=vals[ok];record=record[ok]
 m5=np.zeros(len(idx),dtype=np.uint8)
 for i in (range(L-5,L) if side=='F' else range(5)):m5+=(arr[idx+i]&masks[i])==0
 out=collections.defaultdict(list)
 for rec,pos,mm,mm5,amb in zip(record,idx-offsets[record],vals,m5,prefix[idx+L]-prefix[idx]):out[int(rec)].append((int(pos),int(mm),int(mm5),int(amb)))
 return dict(out)