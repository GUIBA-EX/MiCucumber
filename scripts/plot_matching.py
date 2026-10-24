"""Plot pair-level matching on the frozen common panel; reproduce CSV and figures."""
from pathlib import Path
import csv,collections
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch, FancyBboxPatch
p=Path(__file__).resolve().parents[1];out=p/'results/matching'
def read(f):return list(csv.DictReader(f.open()))
def write(f,rr):
 with f.open('w',newline='') as h:w=csv.DictWriter(h,fieldnames=list(rr[0]),lineterminator='\n');w.writeheader();w.writerows(rr)
panel=sorted(read(out/'panel.csv'),key=lambda r:(r['order'],r['organism'],r['accession']));hits={(r['pair_id'],r['accession']):r for r in read(out/'pair_hits.csv')};pairs=read(p/'sequences/primer_pairs.csv');summary=[];detail=[]
colors=['#e4edf1','#efc367','#268d91'];plt.rcParams.update({'svg.fonttype':'path','font.size':10})
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
 accent={'S':'#24a9b8','M':'#e8a62b','L':'#338fd0','XL':'#a45ad0'}[region]
 span={'S':208,'M':231,'L':315,'XL':387}[region]
 fig=plt.figure(figsize=(16,6.2),facecolor='#eaf6fb')
 fig.text(.035,.92,'MiCucumber',fontsize=26,weight='bold',color='#164f72')
 fig.text(.225,.925,f' {region} ',fontsize=20,weight='bold',color='white',bbox=dict(boxstyle='round,pad=.4',fc=accent,ec='none'))
 fig.text(.31,.93,f'{span} bp reference window',fontsize=13,color='#315f77')
 fig.text(.31,.89,'Primer matching · exact / mismatch-tolerant / missed',fontsize=11,color='#608296')
 for x,width in [(.025,.635),(.68,.295)]:
  fig.add_artist(FancyBboxPatch((x,.18),width,.63,boxstyle='round,pad=.012,rounding_size=.025',transform=fig.transFigure,facecolor='white',edgecolor='#d4e8f1',lw=1,zorder=0))
 ax=fig.add_axes([.08,.30,.56,.40]);bx=fig.add_axes([.735,.30,.225,.40])
 fig.text(.045,.765,'REFERENCE MATCHING',weight='bold',fontsize=12,color='#164f72')
 fig.text(.045,.725,'351 haplotypes · 151 taxonomic labels · grouped by order',fontsize=10,color='#608296')
 fig.text(.70,.765,'COVERAGE & EXACT MATCH',weight='bold',fontsize=12,color='#164f72')
 fig.text(.70,.725,'Non-Apodida · label-balanced weights',fontsize=10,color='#608296')
 ax.imshow(states,aspect='auto',interpolation='nearest',cmap=ListedColormap(colors),vmin=0,vmax=2)
 ax.set_yticks(range(len(groups)),list(groups),fontsize=11);ax.tick_params(axis='both',length=0)
 segments=collections.defaultdict(list)
 for i,r in enumerate(panel):segments[r['order']].append(i)
 ax.set_xticks([sum(v)/len(v) for v in segments.values()],list(segments),rotation=28,ha='right',fontsize=8,color='#426c80')
 for n,v in enumerate(segments.values()):
  ax.axvline(v[0]-.5,color='white',lw=2)
  ax.plot([v[0]-.5,v[-1]+.5],[-.63,-.63],color=['#48aeb8','#e4b45a','#ec997a','#a48cce','#67add3'][n%5],lw=5,clip_on=False)
 for y in range(len(groups)-1):ax.axhline(y+.5,color='white',lw=.7)
 for spine in ax.spines.values():spine.set_visible(False)
 b=np.array(bars);left=np.zeros(len(groups))
 for j,col in enumerate([colors[2],colors[1],colors[0]]):bx.barh(range(len(groups)),b[:,j],left=left,color=col,height=.64);left+=b[:,j]
 bx.set_yticks(range(len(groups)),list(groups),fontsize=10);bx.invert_yaxis();bx.set_xlim(0,100);bx.set_xticks([0,50,100]);bx.set_xlabel('Weighted %',color='#426c80');bx.tick_params(length=0)
 for spine in bx.spines.values():spine.set_visible(False)
 for i,x in enumerate(b):bx.text(1,i,f'{x[0]+x[1]:.1f}% / {x[0]:.1f}%',va='center',fontsize=9,color='#173f50')
 fig.text(.735,.205,'Bar labels: coverage / exact matching',fontsize=9,color='#608296')
 fig.legend(handles=[Patch(color=colors[2],label='Exact match'),Patch(color=colors[1],label='Mismatch-tolerant hit'),Patch(color=colors[0],label='Not detected')],loc='lower center',bbox_to_anchor=(.5,.095),ncol=3,frameon=False,fontsize=11)
 fig.text(.035,.045,'Each heatmap column is one reference haplotype. A+B combines separate PCRs; reference span is not a universal product length.',fontsize=9,color='#608296')
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
