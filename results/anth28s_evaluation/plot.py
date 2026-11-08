"""Publication figures for the frozen diagnostic tables (matplotlib/numpy)."""
import csv,collections
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch,Rectangle
from matplotlib.ticker import MaxNLocator
from matplotlib.lines import Line2D
P=Path(__file__).resolve().parent;R=P/'results';F=P/'figures';F.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','savefig.facecolor':'white'})
def read(n):return list(csv.DictReader((R/n).open()))
def export(fig,n):
    fig.savefig(F/(n+'.png'),dpi=190,bbox_inches='tight');fig.savefig(F/(n+'.svg'),bbox_inches='tight');plt.close(fig)
summary=read('mismatch_summary.csv');barcodes=read('barcodes.csv')
genes=('16S','12S','COI');colors=['#164b5a','#4d9da3','#bbdedd']
fig,axes=plt.subplots(3,2,figsize=(10,8.7),gridspec_kw={'width_ratios':[1.25,1]},layout='constrained')
for row,gene in enumerate(genes):
    names=list(dict.fromkeys(r['name'] for r in summary if r['gene']==gene));x=np.arange(len(names))
    for col,role in enumerate(('target','background')):
        ax=axes[row,col];prior=np.zeros(len(names))
        for k in (0,1,2):
            v=[next(r for r in summary if r['gene']==gene and r['role']==role and r['name']==n and r['threshold']==str(k) and r['terminal3_required']=='0') for n in names]
            y=np.array([float(r['percent'] if role=='target' else r['matched']) for r in v])
            ax.bar(x,y-prior,bottom=prior,color=colors[k],width=.72);prior=y
        strict=[next(r for r in summary if r['gene']==gene and r['role']==role and r['name']==n and r['threshold']=='2' and r['terminal3_required']=='1') for n in names]
        ax.scatter(x,[float(r['percent'] if role=='target' else r['matched']) for r in strict],color='#cf7833',marker='D',s=25,zorder=4)
        ax.set_xticks(x,names);ax.set_title(f"{gene} | {'Target compatibility' if role=='target' else 'Background susceptibility'}",loc='left',fontweight='bold')
        ax.set_ylabel('Evaluable species (%)' if role=='target' else 'Reference records');ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
        if role=='target':
            ax.set_ylim(0,112)
            for i,r in enumerate(strict):ax.text(i,104,r['n'],ha='center',fontsize=7,color='#667875')
        else:
            ax.set_ylim(0,max(1.2,float(max(prior))*1.2));ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax.text(.98,.94,f"N = {strict[0]['n']} records",transform=ax.transAxes,ha='right',va='top',color='#667875',fontsize=8)
legend=[Patch(color=c,label=l) for c,l in zip(colors,['0 mismatches','Additional at 1 mismatch','Additional at 2 mismatches'])]+[Line2D([],[],color='#cf7833',marker='D',linestyle='',label='≤2 mismatches + terminal-three compatibility')]
fig.legend(handles=legend,loc='outside lower center',ncol=2,frameon=False)
fig.suptitle('Paired-primer mismatch sensitivity | Watson–Crick pairing',fontsize=14,fontweight='bold')
export(fig,'mismatch_sensitivity')

for gene in genes:
    fig,axes=plt.subplots(2,3,figsize=(9.5,7),layout='constrained');images=[]
    for ax,window in zip(axes.flat,('XS','S','M','L','XL')):
        rr=[r for r in barcodes if r['gene']==gene and r['window']==window];n=len(rr);matrix=np.eye(n)*100
        for r in read(f'{gene}_{window}_identity.csv'):
            i,j=int(r['i']),int(r['j']);matrix[i,j]=matrix[j,i]=float(r['identity_pct'])
        im=ax.imshow(matrix,vmin=0,vmax=100,cmap='YlGnBu',interpolation='nearest',rasterized=True);images.append(im)
        ticks=[];labels=[]
        start=0
        for i in range(1,n+1):
            if i==n or rr[i]['order']!=rr[start]['order']:
                ticks.append((start+i-1)/2);labels.append(rr[start]['order'] if i-start>=8 else '');start=i
                previous=0 if len(ticks)==1 else next(j for j in range(i) if rr[j]['order']==rr[i-1]['order'])
                ax.add_patch(Rectangle((previous-.5,previous-.5),i-previous,i-previous,fill=False,edgecolor='#202e35',lw=.9))
        start=0
        for i in range(1,n+1):
            if i==n or rr[i]['genus']!=rr[start]['genus'] or rr[i]['order']!=rr[start]['order']:
                if i-start>1:ax.add_patch(Rectangle((start-.5,start-.5),i-start,i-start,fill=False,edgecolor='white',lw=.45,linestyle='--'))
                start=i
        ax.set_xticks([]);ax.set_yticks(ticks,labels,fontsize=9);ax.set_title(f'{window} | n = {n}',loc='left',fontweight='bold')
    axes.flat[5].axis('off')
    axes.flat[5].text(.02,.98,'Primer-free aligned inserts\n\nSorted by source order,\ngenus and species\n\nBlack boxes: orders\nWhite dashed boxes: genera\nOrders with n < 8 not labelled\n\nSingle gaps: differences\nDouble gaps: excluded\nAmbiguous inserts: excluded\n\nSeparate window panels;\ndenominators differ.',va='top',fontsize=9,linespacing=1.35)
    fig.colorbar(images[0],ax=list(axes.flat[:5]),label='Aligned nucleotide identity (%)',shrink=.55,pad=.02)
    fig.suptitle(f'{gene} | Barcode sequence identity by taxonomic group',fontweight='bold',fontsize=13)
    export(fig,f'identity_{gene}')

# Between-species identities stratified by taxonomic relationship (not a barcoding-gap test).
fig,axes=plt.subplots(1,3,figsize=(10,4.4),layout='constrained');relcolors=['#1b7178','#c8943d','#7a74ad']
for ax,gene in zip(axes,genes):
    for i,window in enumerate(('XS','S','M','L','XL')):
        rr=read(f'{gene}_{window}_identity.csv')
        for j,relation in enumerate(('same_genus','same_order_other_genus','different_order')):
            vals=[float(r['identity_pct']) for r in rr if r['relationship']==relation]
            if not vals:continue
            box=ax.boxplot([vals],positions=[i+(j-1)*.24],widths=.2,showfliers=False,patch_artist=True,manage_ticks=False,whis=(5,95))
            box['boxes'][0].set(facecolor=relcolors[j],edgecolor=relcolors[j]);box['medians'][0].set(color='white')
    ax.set_xticks(range(5),('XS','S','M','L','XL'));ax.set_title(gene,loc='left',fontweight='bold');ax.set_ylim(0,101);ax.grid(axis='y',alpha=.15)
axes[0].set_ylabel('Between-species aligned identity (%)')
fig.legend(handles=[Patch(color=c,label=l) for c,l in zip(relcolors,['Same genus','Same order, different genus','Different order'])],loc='outside lower center',ncol=3,frameon=False)
fig.suptitle('Barcode similarity across taxonomic levels\nBoxes: quartiles; whiskers: 5–95%',fontweight='bold')
export(fig,'identity_distributions')

fig,axes=plt.subplots(1,3,figsize=(10,5.8),layout='constrained')
for ax,gene in zip(axes,genes):
    names=list(dict.fromkeys(r['name'] for r in summary if r['gene']==gene));rr=read(f'{gene}_lengths.csv')
    for i,n in enumerate(names):
        for delta,role,color in [(-.15,'target','#21848b'),(.15,'background','#cf7833')]:
            vals=[int(r['span']) for r in rr if r['name']==n and r['role']==role and r['threshold']=='2']
            if not vals:continue
            lo,q1,med,q3,hi=np.percentile(vals,[0,25,50,75,100]);yy=i+delta
            ax.plot([lo,hi],[yy,yy],color=color,lw=1,alpha=.8);ax.plot([q1,q3],[yy,yy],color=color,lw=5,solid_capstyle='butt');ax.scatter([med],[yy],color='white',edgecolor=color,s=18,zorder=4)
    ax.set_yticks(range(len(names)),names);ax.invert_yaxis();ax.set_title(gene,loc='left',fontweight='bold');ax.set_xlabel('Predicted complete product (bp)');ax.grid(axis='x',alpha=.15)
fig.legend(handles=[Line2D([],[],color='#21848b',lw=4,label='Target records'),Line2D([],[],color='#cf7833',lw=4,label='Background records')],loc='outside lower center',ncol=2,frameon=False)
fig.suptitle('Product lengths | ≤2 mismatches per primer; no terminal constraint\nLine: full range; thick segment: quartiles; circle: median\nEach accession/span counted once',fontsize=11,fontweight='bold')
export(fig,'product_lengths')
print('Created 6 figures in PNG and SVG')
