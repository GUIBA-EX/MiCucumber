import csv,subprocess
from collections import defaultdict
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from Bio import SeqIO
root=Path(__file__).resolve().parents[2];w=root/'work/review';out=w/'figures';out.mkdir(exist_ok=True)
def read(n):
 with (w/n).open(newline='') as f:return list(csv.DictReader(f))
fig,axes=plt.subplots(2,1,figsize=(9,3.2),constrained_layout=True)
for ax,(gene,spans,xlim) in zip(axes,[('16S',[('16S SD',954,977,1156,1179),('16S LD',868,891,1152,1169)],(830,1220)),('COI',[('COI LD',508,530,778,800)],(470,840))]):
 for j,(name,a,b,c,d) in enumerate(spans):
  y=len(spans)-j;ax.plot([a,d],[y,y],color='#68a8a0',lw=2);ax.arrow(a,y,b-a,0,width=.04,head_width=.22,head_length=5,length_includes_head=True,color='#167b74');ax.arrow(d,y,c-d,0,width=.04,head_width=.22,head_length=5,length_includes_head=True,color='#d4871c');ax.text((b+c)/2,y+.14,f'{d-a+1} bp',ha='center',fontsize=8)
 ax.set_yticks(range(1,len(spans)+1),[x[0] for x in reversed(spans)]);ax.set_xlim(*xlim);ax.set_ylim(.5,len(spans)+.6);ax.set_xlabel(f'{gene} reference position (1-based)');ax.spines[['top','right','left']].set_visible(False);ax.tick_params(axis='y',length=0)
fig.savefig(out/'figure1_positions.png',dpi=250);plt.close(fig)
orders=read('by_order.csv');coi=read('coi_worms_coverage.csv');names=['16S SD','16S LD','COI LD','hol.11']; fig,axes=plt.subplots(2,2,figsize=(9,7),constrained_layout=True)
for ax,name in zip(axes.flat,names):
 data=[r for r in (coi if name=='COI LD' else orders) if (name=='COI LD' or r['assay']==name) and r['order'] not in ('ALL','EXTERNAL')];x=np.arange(len(data));width=.25
 for i,(col,label) in enumerate([('e0','0'),('e1','≤1'),('e2','≤2')]):ax.bar(x+(i-1)*width,[100*int(r[col])/int(r['n']) for r in data],width,label=label)
 ax.set_xticks(x,[r['order'] for r in data],rotation=45,ha='right',fontsize=7);ax.set_ylim(0,105);ax.set_title(name);ax.set_ylabel('Species matched (%)');ax.spines[['top','right']].set_visible(False)
axes[0,0].legend(title='Mismatches per primer',fontsize=7,title_fontsize=7);fig.savefig(out/'figure2_coverage.png',dpi=250);plt.close(fig)
insert=read('target_inserts.csv');coipanel={r['accession']:r for r in read('coi_worms_panel.csv')};fig,axes=plt.subplots(1,3,figsize=(12,4.3),constrained_layout=True)
for ax,assay in zip(axes,['16S SD','16S LD','COI LD']):
 entries=[]
 for r in insert:
  if r['assay']!=assay or r['panel']!='1' or set(r['insert'])-set('ACGT'):continue
  if assay=='COI LD':
   if r['accession'] not in coipanel:continue
   r.update({k:coipanel[r['accession']][k] for k in ('species','order')})
  entries.append(r)
 entries.sort(key=lambda r:(r['order'],r['species'],r['accession'])); fa=w/f'{assay}_matrix_input.fasta'
 with fa.open('w') as f:
  for i,r in enumerate(entries):f.write(f'>{i}\n{r["insert"]}\n')
 aligned=w/f'{assay}_matrix_aligned.fasta'
 with aligned.open('w') as f:subprocess.run([__import__('os').environ.get('MAFFT', '/home/yasuda2/miniforge3/envs/geneminer2/bin/mafft'),'--quiet','--auto','--thread','4',str(fa)],stdout=f,check=True)
 seqs={int(r.id):str(r.seq).upper() for r in SeqIO.parse(aligned,'fasta')};arr=np.array([list(seqs[i]) for i in range(len(entries))]);n=len(arr);matrix=np.empty((n,n))
 for i in range(n):
  valid=(arr!='-')&(arr[i]!='-'); denom=valid.sum(axis=1); matrix[i]=np.divide(((arr==arr[i])&valid).sum(axis=1),denom,out=np.zeros(n),where=denom>0)
 img=ax.imshow(matrix,vmin=.5,vmax=1,cmap='viridis',interpolation='nearest'); groups=defaultdict(list)
 for i,r in enumerate(entries):groups[r['order']].append(i)
 for ids in groups.values():ax.axhline(ids[0]-.5,color='white',lw=.25);ax.axvline(ids[0]-.5,color='white',lw=.25)
 ax.set_yticks([sum(ids)/len(ids) for ids in groups.values()],[o for o in groups],fontsize=6);ax.set_xticks([]);ax.set_title(f'{assay} (n={n})')
fig.colorbar(img,ax=axes,shrink=.68,label='Pairwise identity (gap-excluded)');fig.savefig(out/'figure3_identity.png',dpi=250);plt.close(fig)
