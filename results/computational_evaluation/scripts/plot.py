from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parents[1];o=p/'figures';o.mkdir(exist_ok=True)
def rd(n):return list(csv.DictReader((p/'results'/n).open()))
plt.rcParams.update({'font.size':10,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
a=[x for x in rd('panel_comparison.csv') if x['panel']=='common'];fig,ax=plt.subplots(figsize=(9,4));xs=list(range(len(a)))
ax.bar([x-.2 for x in xs],[float(x['coverage_pct']) for x in a],width=.4,label='Compatible (≤2 mismatches, terminal 3 compatible)',color='#3287a8');ax.bar([x+.2 for x in xs],[float(x['exact_pct']) for x in a],width=.4,label='Exact paired match',color='#e7a54c');ax.set_xticks(xs,[x['name'] for x in a]);ax.set(ylabel='Species (%)',ylim=(0,105));ax.legend(fontsize=8,loc='upper left');fig.tight_layout();fig.savefig(o/'common_panel.svg');fig.savefig(o/'common_panel.png',dpi=160);plt.close(fig)
a=[x for x in rd('resolution.csv') if x['panel']=='own'];fig,ax=plt.subplots(figsize=(7,3.8));ax.bar([x['region'] for x in a],[float(x['unique_pct']) for x in a],color=['#51adac','#399da9','#ecb24c','#488ec0','#9867bc']);ax.set(ylim=(0,110),ylabel='Identity-unique representatives (%)')
for i,x in enumerate(a):ax.text(i,float(x['unique_pct'])+1,f"{x['identity_unique_species']}/{x['n']}",ha='center')
fig.tight_layout();fig.savefig(o/'resolution.svg');fig.savefig(o/'resolution.png',dpi=160);plt.close(fig)
a=rd('cv_summary.csv');fig,ax=plt.subplots(figsize=(7,3.8));xs=list(range(len(a)));ax.bar([x-.18 for x in xs],[float(x['coverage_pct']) for x in a],.36,label='Held-out compatible',color='#3287a8');ax.bar([x+.18 for x in xs],[float(x['exact_pct']) for x in a],.36,label='Held-out exact',color='#e7a54c');ax.set_xticks(xs,[x['region'] for x in a]);ax.set(ylim=(0,105),ylabel='Held-out species (%)');ax.legend(fontsize=8);fig.tight_layout();fig.savefig(o/'holdout.svg');fig.savefig(o/'holdout.png',dpi=160);plt.close(fig)
