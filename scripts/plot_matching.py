"""Plot pair-level matching on the frozen common panel; reproduce CSV and figures."""
from pathlib import Path
import csv,collections
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
p=Path(__file__).resolve().parents[1];out=p/'results/matching'
def read(f):return list(csv.DictReader(f.open()))
def write(f,rr):
 with f.open('w',newline='') as h:w=csv.DictWriter(h,fieldnames=list(rr[0]),lineterminator='\n');w.writeheader();w.writerows(rr)
panel=sorted(read(out/'panel.csv'),key=lambda r:(r['order'],r['organism'],r['accession']));hits={(r['pair_id'],r['accession']):r for r in read(out/'pair_hits.csv')};pairs=read(p/'sequences/primer_pairs.csv');summary=[];detail=[]
colors=['#e0e5e4','#e2b957','#31936c'];plt.rcParams.update({'svg.fonttype':'path','font.size':10})
for region in ['S','M','L','XL']:
 selected=[r for r in pairs if r['region']==region and r['chemistry']!='original'];groups={r['pair_name']:[r['pair_id']] for r in selected};groups[region+'A+'+region+'B']=[r['pair_id'] for r in selected if r['pairs']=='2']
 if region=='S':groups['S-original']=[r['pair_id'] for r in pairs if r['chemistry']=='original']
 states=[];bars=[]
 for name,ids in groups.items():
  row=[]
  for r in panel:
   exact=any(hits.get((n,r['accession']),{}).get('exact')=='1' for n in ids);cov=any(hits.get((n,r['accession']),{}).get('coverage')=='1' for n in ids);assert not exact or cov
   state=2 if exact else 1 if cov else 0;row.append(state);detail.append(dict(region=region,pair_name=name,**r,state=['missed','mismatch_hit','exact'][state]))
  states.append(row);s=np.array(row);w=np.array([float(r['weight']) for r in panel]);non=np.array([r['order']!='Apodida' for r in panel]);nw=w*non/(w*non).sum()
  a=dict(region=region,pair_name=name,coverage_pct=100*sum(w[s>0]),exact_pct=100*sum(w[s==2]),non_Apodida_coverage_pct=100*sum(nw[s>0]),non_Apodida_exact_pct=100*sum(nw[s==2]));summary.append(a);bars.append([a['non_Apodida_exact_pct'],a['non_Apodida_coverage_pct']-a['non_Apodida_exact_pct'],100-a['non_Apodida_coverage_pct']])
 fig,(ax,bx)=plt.subplots(1,2,figsize=(15,4.8),gridspec_kw={'width_ratios':[2.3,1]},layout='constrained');fig.suptitle(f'MiCucumber {region} | Primer matching',fontsize=19,weight='bold')
 ax.imshow(states,aspect='auto',interpolation='nearest',cmap=ListedColormap(colors),vmin=0,vmax=2);ax.set_yticks(range(len(groups)),list(groups));ax.set_title('Common panel: 351 haplotypes / 151 name labels',fontsize=11)
 segments=collections.defaultdict(list)
 for i,r in enumerate(panel):segments[r['order']].append(i)
 ax.set_xticks([sum(v)/len(v) for v in segments.values()],list(segments),rotation=30,ha='right',fontsize=8)
 for v in segments.values():ax.axvline(v[0]-.5,color='white',lw=1)
 ax.set_xlabel('One column per haplotype; ordered by taxonomy')
 b=np.array(bars);left=np.zeros(len(groups))
 for j,col in enumerate([colors[2],colors[1],colors[0]]):bx.barh(range(len(groups)),b[:,j],left=left,color=col,height=.65);left+=b[:,j]
 bx.set_yticks(range(len(groups)),list(groups));bx.invert_yaxis();bx.set_xlim(0,100);bx.set_xlabel('Weighted %');bx.set_title('Non-Apodida weighted matching',fontsize=11)
 for i,x in enumerate(b):bx.text(1,i,f'{x[0]+x[1]:.1f}% covered',va='center',fontsize=8,color='#122e26')
 fig.legend(handles=[Patch(color=colors[2],label='Exact'),Patch(color=colors[1],label='Mismatch-tolerant hit'),Patch(color=colors[0],label='Missed')],loc='outside lower center',ncol=3,frameon=False)
 for ext in ['png','svg','pdf']:
  f=p/f'figures/matching_{region}.{ext}';fig.savefig(f,dpi=170)
  if ext=='svg':f.write_text('\n'.join(l.rstrip() for l in f.read_text().splitlines())+'\n')
 plt.close(fig)
write(out/'summary.csv',summary);write(out/'detection.csv',detail)
# Match portfolio summaries, while A/B remain independently evaluated rows.
lookup={r['pair_name']:r for r in summary}
for r in read(p/'results/comparison.csv'):
 if r['panel']!='common':continue
 name='S-original' if r['scheme']=='MiCucumber-S-original' else r['scheme']
 for k in ['coverage_pct','exact_pct','non_Apodida_coverage_pct','non_Apodida_exact_pct']:assert abs(float(r[k])-lookup[name][k])<1e-8,(name,k)
print('PASS: 21 matching profiles, 7371 per-reference results; portfolio metrics agree.')
