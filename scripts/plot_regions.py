"""Plot current homologous design windows; no assay count or historical panel claims."""
from pathlib import Path
import argparse,csv
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt,font_manager
p=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('--cjk-font');args=a.parse_args()
if args.cjk_font:font_manager.fontManager.addfont(args.cjk_font)
font=font_manager.FontProperties(fname=args.cjk_font).get_name() if args.cjk_font else 'DejaVu Sans'
plt.rcParams.update({'font.family':font,'svg.fonttype':'path','pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False})
rows=list(csv.DictReader((p/'figures/region_coordinates.csv').open()))
for lang in (['en','zh'] if args.cjk_font else ['en']):
 zh=lang=='zh';fig,ax=plt.subplots(figsize=(12,5.8));fig.subplots_adjust(left=.1,right=.96,top=.77,bottom=.24)
 fig.text(.06,.94,'MiCucumber · S / M / L / XL',fontsize=21,weight='bold',color='#174c3b')
 fig.text(.06,.87,'四个同源设计窗口；简并仅1对；普通1对或2对（A/B）' if zh else 'Four homologous design windows; One degenerate pair; one or two nondegenerate pairs (A/B)',fontsize=11,color='#50655e')
 for y,(r,col) in enumerate(zip(rows,['#087e8b','#c28b29','#386eaf','#8653a1'])):
  fs,fe,rs,re=[int(r[k]) for k in ('F_start','F_end','R_start','R_end')]
  ax.plot([fe,rs],[y,y],color=col,lw=3,alpha=.35)
  for start,end in [(fs,fe),(re,rs)]:ax.annotate('',xy=(end,y),xytext=(start,y),arrowprops=dict(arrowstyle='-|>',lw=4,color=col,shrinkA=0,shrinkB=0))
  ax.text((fe+rs)/2,y-.16,(f"参考窗口 {r['reference_span_bp']} bp" if zh else f"Reference window: {r['reference_span_bp']} bp"),ha='center',fontsize=10)
  ax.text(fs,y+.25,f'F {fs}–{fe}',ha='left',color=col,fontsize=9)
  ax.text(re,y+.25,f'R {rs}–{re}',ha='right',color=col,fontsize=9)
 ax.set_yticks(range(4),[r['locus'] for r in rows],fontsize=14,weight='bold');ax.set_ylim(3.5,-.5);ax.set_xlim(750,1185);ax.grid(axis='x',alpha=.15);ax.tick_params(axis='y',length=0)
 ax.set_xlabel('AB525437.1 提取的无缺口16S参考坐标（1-based）' if zh else 'Extracted ungapped 16S reference coordinates of AB525437.1 (1-based)',labelpad=12)
 foot=('箭头表示历史种子窗口，变体引物长度可能不同；参考窗口跨度不等于所有物种的产物长度。\n简并仅1对；普通1对或2对（A/B）。S-original单独保留为原版对照。' if zh else 'Arrows show seed binding windows; variant primer lengths can differ. Reference spans are not product lengths in every taxon.\nOne degenerate pair; one or two nondegenerate pairs (A/B). S-original is retained separately as the original control.')
 fig.text(.06,.05,foot,fontsize=9,color='#50655e',linespacing=1.8)
 for ext in ('png','svg','pdf'):
  target=p/f'figures/amplicon_regions.{lang}.{ext}'
  fig.savefig(target,dpi=180,facecolor='white')
  if ext=='svg':target.write_text('\n'.join(line.rstrip() for line in target.read_text().splitlines())+'\n')
 plt.close(fig)
print('Generated current S/M/L/XL figures')
