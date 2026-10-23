"""Reference-coordinate region map, inspired by the MiStar discussion figure.
Run: python plot_regions.py [--cjk-font /path/to/CJK.ttf]
Reference coordinates are 1-based extracted 16S positions, not mitogenome positions.
"""
from pathlib import Path
import argparse,csv,json,collections
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
p=Path(__file__).resolve().parent;a=p/'analysis';out=p/'figures';out.mkdir(exist_ok=True)
args=argparse.ArgumentParser();args.add_argument('--cjk-font');args=args.parse_args()
if args.cjk_font:font_manager.fontManager.addfont(args.cjk_font)
font=font_manager.FontProperties(fname=args.cjk_font).get_name() if args.cjk_font else 'DejaVu Sans'
plt.rcParams.update({'font.family':font,'font.size':11,'svg.fonttype':'path','pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#314651','text.color':'#223b47'})
def fasta(path):
 d={};key=None
 for line in path.read_text().splitlines():
  if line.startswith('>'):key=line[1:].split()[0].removeprefix('_R_');d[key]=''
  else:d[key]+=line.strip().upper()
 return d
def read(n):return list(csv.DictReader((p/n).open(encoding='utf-8-sig'),delimiter='\t' if n.endswith('.tsv') else ','))
al=fasta(a/'target_aligned.fasta');ids=json.loads((a/'common_panel.json').read_text())['ids'];meta={r['accession']:r for r in read('analysis/metadata.tsv')};cnt=collections.Counter(meta[k]['organism'] for k in ids);w=np.array([1/len(cnt)/cnt[meta[k]['organism']] for k in ids]);assert len(cnt)==149 and len(ids)==347 and np.isclose(w.sum(),1)
coord=[i for i,c in enumerate(al['AB525437.1']) if c!='-'];lo,hi=730,1200;positions=np.arange(lo,hi+1)
con=[];call=[]
for pos in positions:
 bases=np.array([al[k][coord[pos-1]] for k in ids]);freq=np.array([w[bases==b].sum() for b in 'ACGT']);den=freq.sum();call.append(100*den);con.append(100*freq.max()/den if den else np.nan)
def smooth(v):return np.array([np.nanmean(v[max(0,i-5):min(len(v),i+6)]) for i in range(len(v))])
seeds={s['label']:s for s in json.loads((a/'final_selected.json').read_text())[:4]};comparison={r['scheme']:r for r in read('results/apodida_comparison.csv')};tracks=[]
for short in ['v4opt','S','M','L']:
 s=seeds['MiCucumber-'+short];left,right=int(s['left']),int(s['right']);L,R=len(s['F']),len(s['R']);r=comparison[s['label']+'-Separate-Apodida']
 tracks.append(dict(locus=short,F_start=left+1,F_end=left+L,R_start=right-R+1,R_end=right,reference_span_bp=right-left,reference_internal_bp=right-left-L-R,total_pairs=int(r['total_pairs']),added_pairs=int(r['additional_pairs']),Apodida_hits=int(r['Apodida_hit_records'])))
with (out/'region_coordinates.csv').open('w',newline='') as f:wr=csv.DictWriter(f,fieldnames=list(tracks[0]));wr.writeheader();wr.writerows(tracks)
with (out/'reference_conservation.csv').open('w',newline='') as f:
 wr=csv.writer(f);wr.writerow(['reference_position_1based','major_base_frequency_pct','callable_weight_pct','major_base_11nt_mean_pct','callable_11nt_mean_pct']);wr.writerows(zip(positions,con,call,smooth(con),smooth(call)))
for lang in (['en','zh'] if args.cjk_font else ['en']):
 zh=lang=='zh';fig,(ax,bx)=plt.subplots(2,1,figsize=(14,9),sharex=True,gridspec_kw={'height_ratios':[1,2]});fig.subplots_adjust(left=.12,right=.97,top=.88,bottom=.17,hspace=.38)
 fig.suptitle('MiCucumber 扩增区域与同位置补覆盖' if zh else 'MiCucumber amplicon regions and same-locus supplementation',x=.04,y=.98,ha='left',fontsize=19,fontweight='bold')
 fig.text(.04,.932,'共同面板：149个名称标签 / 347条单倍型；参考：Apostichopus japonicus AB525437.1' if zh else 'Common panel: 149 name labels / 347 haplotypes | Reference: Apostichopus japonicus AB525437.1',fontsize=11,color='#526770')
 ax.plot(positions,smooth(con),color='#287bb5',lw=1.7,label='可判定碱基中的主碱基频率' if zh else 'Major-base frequency among callable bases');ax.plot(positions,smooth(call),color='#8a98a4',ls='--',label='可判定A/C/G/T的权重' if zh else 'Callable A/C/G/T weight');ax.set_ylim(0,105);ax.set_ylabel('加权百分比' if zh else 'Weighted %');ax.set_title('A  观察到的保守性（11个参考碱基滑动均值）' if zh else 'A  Observed conservation (11-reference-base moving mean)',loc='left',fontweight='bold',fontsize=12);ax.legend(loc='lower left',fontsize=9,frameon=False)
 colors=['#087e8b','#c28b29','#386eaf','#8653a1']
 for y,(r,col) in enumerate(zip(tracks,colors)):
  fs,fe,rs,re=[r[k] for k in ['F_start','F_end','R_start','R_end']]
  bx.plot([fe,rs],[y,y],color=col,lw=3,alpha=.45)
  for start,end in [(fs,fe),(re,rs)]:bx.annotate('',xy=(end,y),xytext=(start,y),arrowprops={'arrowstyle':'-|>','lw':4,'color':col,'shrinkA':0,'shrinkB':0})
  bx.text((fe+rs)/2,y-.17,(f"参考内部区间 {r['reference_internal_bp']} bp · 全窗口 {r['reference_span_bp']} bp" if zh else f"{r['reference_internal_bp']} bp internal | {r['reference_span_bp']} bp outer span"),ha='center',fontsize=10)
  bx.text((fs+fe)/2,y+.22,f'F {fs}–{fe}',ha='center',color=col,fontsize=9)
  bx.text((rs+re)/2,y+.22,f'R {rs}–{re}',ha='center',color=col,fontsize=9)
  bx.text(735,y+.42,(f"4 + {r['added_pairs']} = {r['total_pairs']}个独立PCR；Apodida {r['Apodida_hits']}/4" if zh else f"4 + {r['added_pairs']} = {r['total_pairs']} separate PCRs; Apodida {r['Apodida_hits']}/4"),fontsize=9,color='#526770')
 bx.set_yticks(range(4),['v4opt','S','M','L']);bx.set_ylim(3.65,-.55);bx.set_xlim(lo,hi);bx.set_xticks(np.arange(750,1201,50));bx.grid(axis='x',alpha=.13);bx.set_title('B  同源设计窗口与引物方向（箭头为种子窗口，不代表所有变体等长）' if zh else 'B  Homologous design windows and primer direction (seed windows; variant lengths can differ)',loc='left',fontweight='bold',fontsize=12)
 bx.set_xlabel('AB525437.1 提取的无缺口16S坐标（1-based；非线粒体基因组坐标）' if zh else 'Position in extracted, ungapped 16S of AB525437.1 (1-based; not mitogenome coordinates)')
 foot=('图中跨度为参考设计窗口，不是所有分类群的实际产物长度。新增Apodida引物沿用同源窗口，需分别PCR。\n保守性排除缺口与模糊碱基后计算；虚线保留可判定比例。面板仅含4条Apodida记录，4/4不代表全目覆盖。' if zh else 'Spans describe reference design windows, not actual product lengths in every taxon. Added Apodida pairs use homologous windows and separate PCRs.\nConservation excludes gaps/ambiguous bases; the dashed curve shows callable weight. Only four Apodida records are in this panel; 4/4 is not order-wide coverage.')
 fig.text(.04,.045,foot,fontsize=9,color='#526770',linespacing=1.7)
 for ext in ['png','svg','pdf']:fig.savefig(out/f'amplicon_regions.{lang}.{ext}',dpi=170,facecolor='white')
 plt.close(fig)
print('Generated region map and source tables')
