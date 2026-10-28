"""Draw current reference windows using the shared MiCucumber visual style."""
from pathlib import Path
import argparse,csv
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt,font_manager,ticker
p=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--cjk-font',default='/System/Library/Fonts/STHeiti Medium.ttc');args=parser.parse_args()
font_manager.fontManager.addfont(args.cjk_font);cjk=font_manager.FontProperties(fname=args.cjk_font).get_name()
rows=list(csv.DictReader((p/'figures/current_region_coordinates.csv').open()));ref=rows[0]['reference'];project=p.name
assert all(r['reference']==ref for r in rows)
for lang in ('en','zh'):
 zh=lang=='zh';plt.rcParams.update({'font.family':cjk if zh else 'DejaVu Sans','svg.fonttype':'path','pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False})
 fig,ax=plt.subplots(figsize=(12,5.8));fig.subplots_adjust(left=.1,right=.96,top=.77,bottom=.25)
 fig.text(.06,.94,f'{project} · XS / S / M / L / XL',fontsize=21,weight='bold',color='#174c3b')
 fig.text(.06,.87,'五个参考设计窗口' if zh else 'Five reference design windows',fontsize=11,color='#50655e')
 scale=max(int(r['R_end']) for r in rows)-min(int(r['F_start']) for r in rows)
 for y,(r,col) in enumerate(zip(rows,['#65a544','#087e8b','#c28b29','#386eaf','#8653a1'])):
  fs,fe,rs,re=(int(r[k]) for k in ('F_start','F_end','R_start','R_end'))
  ax.plot([fe,rs],[y,y],color=col,lw=3,alpha=.35)
  for start,end in ((fs,fe),(re,rs)):ax.annotate('',xy=(end,y),xytext=(start,y),arrowprops=dict(arrowstyle='-|>',lw=4,color=col,shrinkA=0,shrinkB=0))
  ax.text((fe+rs)/2,y-.16,(f"参考区间：{r['reference_span_bp']} bp" if zh else f"Reference window: {r['reference_span_bp']} bp"),ha='center',fontsize=10)
  outside=(re-fs)/scale<.22
  ax.text(fs,y+.20 if outside else y+.25,f'F {fs}–{fe}',ha='left',color=col,fontsize=9)
  ax.text(re,y+.42 if outside else y+.25,f'R {rs}–{re}',ha='right',color=col,fontsize=9)
 a=min(int(r['F_start']) for r in rows);b=max(int(r['R_end']) for r in rows);pad=max(35,(b-a)*.06)
 ax.set_yticks(range(len(rows)),[r['locus'] for r in rows],fontsize=14,weight='bold');ax.set_ylim(len(rows)-.5,-.5);ax.set_xlim(a-pad,b+pad);ax.xaxis.set_major_locator(ticker.MaxNLocator(6,integer=True));ax.grid(axis='x',alpha=.15);ax.tick_params(axis='y',length=0)
 ax.set_xlabel(f'{ref} 去空位 16S 参考坐标（从 1 开始）' if zh else f'Extracted ungapped 16S reference coordinates of {ref} (1-based)',labelpad=12)
 foot=('箭头表示参考设计窗口；参考跨度包含引物，不代表所有物种的产物长度。\n相同长度的普通与 D 引物共享参考坐标；各物种的实际结合位置可能不同。' if zh else 'Arrows indicate reference design windows. Reference spans include primers; amplicon lengths can vary among taxa.\nOrdinary and D primers at the same length share coordinates; actual binding positions can differ among taxa.')
 fig.text(.06,.05,foot,fontsize=9,color='#50655e',linespacing=1.8)
 for ext in ('png','svg','pdf'):
  target=p/f'figures/amplicon_regions.{lang}.{ext}';fig.savefig(target,dpi=180,facecolor='white')
  if ext=='svg':target.write_text('\n'.join(line.rstrip() for line in target.read_text().splitlines())+'\n')
 plt.close(fig)
