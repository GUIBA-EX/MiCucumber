from pathlib import Path
import csv
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
from PIL import Image

src=Path(__file__).resolve().parents[1]
root=src/'publications/submission/figures'
out=root
arial=Path('/System/Library/Fonts/Supplemental/Arial.ttf')
if arial.exists(): font_manager.fontManager.addfont(str(arial))
plt.rcParams.update({'font.family':'Arial','font.size':8.4,'axes.titlesize':9.5,
                     'axes.labelsize':8.4,'xtick.labelsize':8,'ytick.labelsize':8,
                     'legend.fontsize':8,'ps.fonttype':42,'hatch.linewidth':0.65})
def read(name):
    with (src/'results'/name).open(newline='') as f:
        return list(csv.DictReader(f))
def export(fig,number,fmt):
    if fmt=='eps':
        fig.savefig(out/f'Fig{number}.eps',format='eps')
    else:
        fig.savefig(out/f'Fig{number}.tif',dpi=600,pil_kwargs={'compression':'tiff_lzw'})
        with Image.open(out/f'Fig{number}.tif') as im:
            assert im.info['dpi']==(600.0,600.0)
            print('TIFF',im.size,im.info['dpi'])
    fig.savefig(root/f'Fig{number}.png',dpi=200)
    plt.close(fig)

from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle, Patch
alignment={}
for entry in (src/'results/species_qc/curated_alignment.fasta').read_text().split('>')[1:]:
    header,*lines=entry.splitlines()
    alignment[header.split()[0]]=''.join(lines).upper()
reference=alignment['AB525437.1']
coords=[i for i,c in enumerate(reference) if c!='-']
left,right=coords[760-1],coords[1250-1]+1
panel=read('species_qc/panel_S.csv')
import json
taxonomy={}
for record in json.loads((src/'results/species_qc/gbif_matches.json').read_text()):
    match=record.get('match',{})
    if match.get('family'):
        taxonomy[record['name']]=match
        if match.get('canonicalName'):taxonomy[match['canonicalName']]=match
for record in json.loads((src/'results/species_qc/gbif_accepted.json').read_text()).values():
    if record.get('species'):taxonomy[record['species']]=record
order_names=['Apodida','Dendrochirotida','Elasipodida','Holothuriida','Molpadida','Persiculida','Synallactida']
chosen=[]
for order in order_names:
    groups=defaultdict(list)
    for record in panel:
        if record['order']!=order:continue
        tax=taxonomy.get(record['organism'],{})
        family=tax.get('family','Unresolved family')
        genus=tax.get('genus') or record['organism'].split()[0]
        seq=alignment[record['accession']][coords[830-1]:coords[1200-1]+1]
        record={**record,'family':family,'genus':genus,
                'unambiguous_bases':sum(c in 'ACGT' for c in seq)}
        groups[family].append(record)
    selected=[]
    for family in sorted(groups):
        candidates=sorted(groups[family],key=lambda r:(-r['unambiguous_bases'],r['organism'],r['accession']))
        selected.append(candidates.pop(0))
        groups[family]=candidates
    target=max(4,len(groups))
    while len(selected)<target:
        changed=False
        for family in sorted(groups):
            used={r['genus'] for r in selected}
            candidates=sorted(groups[family],key=lambda r:(r['genus'] in used,-r['unambiguous_bases'],r['organism'],r['accession']))
            if not candidates:continue
            pick=candidates[0]
            selected.append(pick)
            groups[family].remove(pick)
            changed=True
            if len(selected)>=target:break
        if not changed:break
    chosen.extend(sorted(selected,key=lambda r:(r['family'],r['genus'],r['organism'],r['accession'])))
fields=['order','family','genus','organism','accession','unambiguous_bases']
with (out/'Fig1_representatives.csv').open('w',newline='') as handle:
    writer=csv.DictWriter(handle,fieldnames=fields,extrasaction='ignore')
    writer.writeheader();writer.writerows(chosen)
print('Fig1 representatives',len(chosen),dict((o,sum(r['order']==o for r in chosen)) for o in order_names))
allarr=np.array([list(alignment[r['accession']][left:right]) for r in panel])
freq={base:(allarr==base).mean(axis=0) for base in 'ACGT'}
shown=np.array([list(alignment[r['accession']][left:right]) for r in chosen])
values=np.full(shown.shape,4)
for i,row in enumerate(shown):
    for j,base in enumerate(row):
        if base in freq:
            f=freq[base][j]
            values[i,j]=0 if f==1 else 1 if f>=.8 else 2 if f>=.6 else 3
# Group headers create breathing room without changing the alignment columns.
display_rows=[]
labels=[]
row_records=[]
header_rows=[]
source_index=0
for order in order_names:
    header_rows.append(len(display_rows))
    display_rows.append(np.full(values.shape[1],4))
    labels.append(order)
    row_records.append(None)
    for record in [r for r in chosen if r['order']==order]:
        display_rows.append(values[source_index])
        labels.append(record['organism'])
        row_records.append(record)
        source_index+=1
fig=plt.figure(figsize=(210/25.4,297/25.4))
grid=fig.add_gridspec(2,1,height_ratios=[3.3,14],hspace=.06)
top=fig.add_subplot(grid[0])
ax=fig.add_subplot(grid[1])
fig.subplots_adjust(left=.265,right=.985,top=.97,bottom=.10)
colors=['#151515','#783789','#ed5260','#faf5a0','#ffffff']
ax.imshow(display_rows,cmap=ListedColormap(colors),vmin=0,vmax=4,aspect='auto',interpolation='nearest')
ax.set_yticks([])
label_x=(.018-.265)/(.985-.265)
for index,label in enumerate(labels):
    if index in header_rows:
        ax.axhspan(index-.5,index+.5,xmin=label_x,xmax=1,color='#f2f4f5',lw=0,clip_on=False)
        ax.text(label_x,index,label,transform=ax.get_yaxis_transform(),ha='left',va='center',
                fontsize=10,fontweight='bold',color='#20262b',clip_on=False)
    else:
        record=row_records[index]
        ax.text(label_x,index-.18,label,transform=ax.get_yaxis_transform(),ha='left',va='center',
                fontsize=8.3,fontstyle='italic',color='#20262b',clip_on=False)
        ax.text(label_x,index+.23,record['accession'],transform=ax.get_yaxis_transform(),ha='left',va='center',
                fontsize=6.8,color='#69747b',clip_on=False)
ticks=(800,900,1000,1100,1200)
ax.set_xticks([coords[x-1]-left for x in ticks],ticks,fontsize=9)
ax.tick_params(axis='x',length=3,color='#a8afb5')
ax.set_xlabel('16S position on AB525437.1 (1-based)',fontsize=10,labelpad=9)
ax.spines[['top','right','left']].set_visible(False)
ax.spines['bottom'].set_color('#a8afb5')
ax.spines['bottom'].set_linewidth(.6)
top.set_xlim(ax.get_xlim())
top.set_ylim(-.55,4.7)
coordinate_rows=list(csv.DictReader((src/'figures/current_region_coordinates.csv').open()))
for y,record in zip(range(4,-1,-1),coordinate_rows):
    label=record['locus']
    a,b,c,d=[int(record[k]) for k in ('F_start','F_end','R_start','R_end')]
    top.plot([coords[a-1]-left,coords[d-1]-left],[y,y],color='#c9d9b8',lw=1.4,zorder=1)
    for u,v,col,direction in [(a,b,'#165b3a','F'),(d,c,'#81b54c','R')]:
        top.annotate('',(coords[v-1]-left,y),(coords[u-1]-left,y),
                     arrowprops=dict(arrowstyle='-|>',color=col,lw=2.2),zorder=2)
        top.text((coords[u-1]+coords[v-1])/2-left,y+.20,direction,
                 ha='center',fontsize=9,fontweight='bold',color=col)
    top.text((coords[b-1]+coords[c-1])/2-left,y+.15,f'{d-a+1} bp',
             ha='center',fontsize=9,color='#56616a')
top.set_yticks(range(4,-1,-1),[r['locus'] for r in coordinate_rows],fontsize=11,fontweight='bold')
top.set_xticks([])
top.spines[:].set_visible(False)
top.tick_params(length=0,pad=7)
fig.legend(handles=[Patch(facecolor=c,edgecolor='#aab0b4' if i==4 else 'none',
                         linewidth=.5,label=l)
                    for i,(c,l) in enumerate(zip(colors,['100%','80–<100%','60–<80%','<60%','Gap / ambiguous']))],
           loc='lower center',bbox_to_anchor=(.5,.015),ncol=5,frameon=False,
           fontsize=8.5,title='Nucleotide frequency across the reference panel',
           title_fontsize=10,handlelength=1.4,columnspacing=1.3)
fig.savefig(out/'Fig1_A4.pdf',format='pdf')
export(fig,1,'eps')

orders=read('complementarity/by_order.csv')+list(csv.DictReader((src/'results/visualization/16S_S/by_order.csv').open()))
coi=read('complementarity/coi_worms_coverage.csv')
fig,axes=plt.subplots(3,2,figsize=(174/25.4,225/25.4),layout='constrained')
for panel,(ax,name) in enumerate(zip(axes.flat,['16S S','16S SD','16S LD','COI LD','hol.11'])):
    data=[r for r in (coi if name=='COI LD' else orders)
          if (name=='COI LD' or r['assay']==name) and r['order'] not in ('ALL','EXTERNAL')]
    x=np.arange(len(data))
    for i,(key,label,color) in enumerate(zip(('e0','e1','e2'),('0','≤1','≤2'),('#5c01a6','#b12a90','#e9c83d'))):
        ax.barh(x+(i-1)*.25,[100*int(r[key])/int(r['n']) for r in data],.23,
               label=label,color=color,edgecolor='white',linewidth=.3)
    ax.set_yticks(x,[r['order'] for r in data],fontsize=7.5)
    ax.invert_yaxis()
    ax.set(xlim=(0,103),title=f'{chr(65+panel)}  {name}',xlabel='Species matched (%)')
    ax.set_xticks([0,25,50,75,100])
    ax.set_axisbelow(True)
    ax.grid(axis='x',color='#e3e9ed',linewidth=.5)
    ax.spines[['top','right','left']].set_visible(False)
    ax.tick_params(axis='y',length=0)
axes[-1,-1].axis('off')
fig.legend(*axes[0,0].get_legend_handles_labels(),title='Mismatches per primer',loc='outside lower center',ncol=3,frameon=False)
export(fig,2,'eps')

def fasta(path):
    records={}
    for entry in path.read_text().split('>')[1:]:
        key,*lines=entry.splitlines()
        records[int(key)]= ''.join(lines).upper()
    return records
insert=read('resolution/target_inserts.csv')+list(csv.DictReader((src/'results/visualization/16S_S/target_inserts.csv').open()))
coipanel={r['accession']:r for r in read('complementarity/coi_worms_panel.csv')}
fig,axes=plt.subplots(2,2,figsize=(174/25.4,185/25.4))
fig.subplots_adjust(left=.17,right=.98,top=.94,bottom=.22,hspace=.65,wspace=.65)
sd_data=None
for ax,assay in zip(axes.flat,['16S S','16S LD','COI LD','16S SD']):
    entries=[]
    for r in insert:
        if r['assay']!=assay or r['panel']!='1' or set(r['insert'])-set('ACGT'):
            continue
        if assay=='COI LD':
            if r['accession'] not in coipanel:
                continue
            r={**r,**{k:coipanel[r['accession']][k] for k in ('species','order')}}
        entries.append(r)
    entries.sort(key=lambda r:(r['order'],r['species'],r['accession']))
    seqs=fasta(src/('results/visualization/16S_S' if assay=='16S S' else 'results/visualization')/f'{assay}_matrix_aligned.fasta')
    assert all(seqs[i].replace('-','')==r['insert'].upper() for i,r in enumerate(entries))
    indices=sorted(range(len(entries)),key=lambda i:(entries[i]['order'],entries[i]['family'],entries[i]['genus'],entries[i]['species']))
    arr=np.array([list(seqs[i]) for i in indices])
    entries=[entries[i] for i in indices]
    rows=[]
    for query in arr:
        valid=(arr!='-')&(query!='-')
        denom=valid.sum(axis=1)
        rows.append(np.divide(((arr==query)&valid).sum(axis=1),denom,out=np.zeros(len(arr)),where=denom>0))
    if assay=='16S SD':
        sd_data=(entries,np.array(rows))
        ax.axis('off')
        continue
    img=ax.imshow(rows,vmin=.5,vmax=1,cmap='plasma',interpolation='nearest')
    for rank,lw,style in [('family',1,'-'),('genus',.5,'--')]:
        groups=defaultdict(list)
        for i,r in enumerate(entries):
            key=(r['order'],r['family'],r[rank])
            groups[key].append(i)
        ticks=[];labels=[]
        for key,ids in groups.items():
            if not key[-1]: continue
            start=ids[0]-.5; size=len(ids)
            ax.add_patch(Rectangle((start,start),size,size,fill=False,edgecolor='black',lw=lw,linestyle=style))
            if rank=='family' and size>=max(3,len(entries)*.05):
                ticks.append(sum(ids)/len(ids));labels.append(key[-1])
        if rank=='family':
            ax.set_yticks(ticks,labels,fontsize=8.5)
            ax.set_xticks(ticks,labels,fontsize=6.8,rotation=90)
    ax.set_title(f'{assay} · n = {len(entries)}',fontsize=9)
cax=fig.add_axes([.18,.055,.5,.012])
fig.colorbar(img,cax=cax,orientation='horizontal',label='Pairwise identity (gap excluded)')
fig.savefig(root/'supp_other_identity.png',dpi=300)
fig.savefig(out/'FigS5.tif',dpi=600,pil_kwargs={'compression':'tiff_lzw'})
plt.close(fig)
entries,matrix=sd_data
order_names=sorted({r['order'] for r in entries})
fig,axes=plt.subplots(3,2,figsize=(174/25.4,228/25.4))
fig.subplots_adjust(left=.17,right=.98,top=.96,bottom=.19,hspace=.82,wspace=.68)
for ax,order in zip(axes.flat,order_names):
    ids=[i for i,r in enumerate(entries) if r['order']==order]
    subset=[entries[i] for i in ids]
    img=ax.imshow(100*matrix[np.ix_(ids,ids)],vmin=50,vmax=100,cmap='plasma',interpolation='nearest')
    for rank,lw,style in [('family',1.1,'-'),('genus',.6,'--')]:
        groups=defaultdict(list)
        for j,r in enumerate(subset): groups[(r['family'],r[rank])].append(j)
        ticks=[];labels=[]
        for key,indices in groups.items():
            if not key[-1]:continue
            start=indices[0]-.5
            ax.add_patch(Rectangle((start,start),len(indices),len(indices),fill=False,edgecolor='black',lw=lw,linestyle=style))
            if rank=='family' and (len(indices)>=max(2,len(ids)*.08) or len(ids)<=4):
                ticks.append(sum(indices)/len(indices));labels.append(key[-1])
        if rank=='family':
            ax.set_yticks(ticks,labels,fontsize=6.5)
            ax.set_xticks(ticks,labels,fontsize=6.5,rotation=90)
    ax.set_title(f'{order} (n = {len(ids)})',fontsize=9)
cax=fig.add_axes([.28,.045,.5,.012])
fig.colorbar(img,cax=cax,orientation='horizontal',label='Pairwise identity (%)')
export(fig,3,'tif')
