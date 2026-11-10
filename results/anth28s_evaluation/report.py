"""Generate the bilingual diagnostic reports.
The formal manuscript is maintained in publications/MiCucumber_preprint.md.
"""
import csv
from pathlib import Path
P=Path(__file__).resolve().parent;R=P/'results'
def read(n):return list(csv.DictReader((R/n).open()))
S=read('mismatch_summary.csv');ID=read('identity_summary.csv')
def count(g,n,k,terminal=0,role='target'):
 return next(x['matched'] for x in S if x['gene']==g and x['name']==n and x['threshold']==str(k) and x['terminal3_required']==str(terminal) and x['role']==role)
def table(head,data):return '| '+' | '.join(head)+' |\n| '+' | '.join(['---']*len(head))+' |\n'+'\n'.join('| '+' | '.join(map(str,row))+' |' for row in data)
def mismatch_table(head,chosen=None):
 data=[]
 if chosen is None:chosen=list(dict.fromkeys((r['gene'],r['name']) for r in S))
 for g,n in chosen:
  size=next(r['n'] for r in S if r['gene']==g and r['name']==n and r['role']=='target')
  data.append([g,n,size,*[count(g,n,k) for k in (0,1,2)],count(g,n,2,1),count(g,n,2,0,'background')])
 return table(head,data)
ENHEAD=['Gene','Assay','Species N','≤0','≤1','≤2','≤2 + terminal 3','Background ≤2']
ZHHEAD=['基因','方案','物种 N','≤0','≤1','≤2','≤2＋末三位','背景 ≤2']
en_methods="""Following the diagnostic approach of McCartin et al. (2024, pp. 6 and 11–13; Fig. 3), all 29 released primer pairs were rescanned on both strands of their frozen target and background sequences. Mismatch thresholds of zero, one and two apply separately to each primer, with IUPAC compatibility treated as a match under Watson–Crick pairing. Each threshold was evaluated with and without requiring compatibility at the final three 3′ bases of both primers. Ambiguous binding sites were excluded. Target product-length limits reproduce the released rules: 70–500 bp with an insert ≥20 bp for 16S XS, 150–500 bp with an insert ≥50 bp for the remaining 16S assays, and 100–500 bp with an insert ≥50 bp for 12S/COI. Background inserts were allowed from 0 to 1,000 bp. Target denominators contain one representative per evaluable species per window; background denominators are 5,600, 438 and 2,216 accession records for 16S, 12S and COI. Counts therefore describe different units and are not amplification proportions in a mixed sample. The released guanine–thymine and more permissive background models remain separately reported.

For sequence-identity matrices, primer-free inserts were extracted between the aligned reference endpoints from each window's evaluable panel. Inserts containing ambiguous nucleotides were excluded; the existing curated gene alignments were retained. Identity equals the number of equal A/C/G/T columns divided by the number of columns containing at least one base. A base opposite a gap is a difference, and double-gap columns are ignored. Matrices were sorted by the source order assignment, genus and species. Ordinary/D alternatives share the same internal region, so one matrix represents each length. Exact ungapped insert identity was also counted independently. Between-species similarities were stratified into same genus, same order/different genus, and different orders. These available-panel summaries do not provide within-species variation, a barcoding-gap test, or matched cross-gene performance estimates. Product distributions count each unique accession/product-span combination once at each threshold; target products are restricted to the evaluable window panel.

The new C++ exhaustive scan was compared with the released exact and strict Watson–Crick summaries in 87 checks. An independent Python regex-seed matcher verified 1,578 threshold/terminal flags on deterministic hit and non-hit subsets spanning every assay and both target/background roles. A further 465 sampled pairwise identities were recalculated independently."""
zh_methods="""参考 McCartin 等（2024，第 6、11–13 页及图 3），对当前 29 对引物和冻结的目标、背景参考序列进行双链配对扫描。0、1、2 个错配均指每条引物各自允许的上限；在沃森–克里克配对下，模板碱基落入 IUPAC 兼容范围即记为匹配。每一档同时比较是否要求两条引物 3′ 末三位兼容。结合区有模糊碱基的命中被排除。产物长度沿用正式规则：16S XS 为 70–500 bp、内部区段至少 20 bp；其余 16S 为 150–500 bp、内部至少 50 bp；12S/COI 为 100–500 bp、内部至少 50 bp。背景扫描允许内部区段 0–1,000 bp。目标按每个可评价物种一条代表计数，三个基因的背景分别为 5,600、438、2,216 条 accession；两类计数单位不同，不能解释为混合样品中的扩增比例。正式报告中允许鸟嘌呤–胸腺嘧啶配对及更宽松错配的背景结果仍单独保留。

序列相似度分析从各长度可评价面板中提取引物之间的内部区段，排除含模糊碱基的区段，沿用现有整理后的基因比对。相似度＝相同 A/C/G/T 列数／至少一端有碱基的列数；碱基对缺口计为差异，双缺口列不计。矩阵按来源目分类、属和物种排序。普通与 D 同坐标，因而每个长度只绘制一个内部序列矩阵；另行统计去缺口后完全相同的跨物种序列。种间相似度分为同属、同目异属、异目三类。各窗口面板不同，这些结果不代表跨基因同面板比较；每物种一条参考也无法估计种内变异或条形码间隙。产物长度图在每个阈值下将唯一 accession／产物长度组合各计一次，目标限于该长度的可评价物种。

新增 C++ 穷举扫描通过 87 项正式完全匹配及严格沃森–克里克结果核对；独立 Python 种子匹配对每个方案的目标与背景命中、未命中子集完成 1,578 项阈值／末端标志检查，并独立重算 465 项序列相似度。"""
en_findings="""The mismatch series separates exact compatibility from tolerance-dependent coverage. On their own available panels, 16S SD matched 0, 24 and 130 of 174 species at zero, one and two mismatches per primer; requiring terminal-three compatibility at the two-mismatch threshold retained all 130. In contrast, LD matched 29, 60 and 84 species, decreasing to 82 after the terminal constraint. For 12S XLD, the series was 7, 16 and 33 of 53 species, with 33 retained by the terminal rule. COI XSD matched 3, 18 and 44 of 57 species, decreasing to 43; COI LD decreased from 122 to 103 of 283 species when terminal compatibility was required at the two-mismatch threshold. These differences show why relaxed mismatch totals cannot replace the released strict coverage measure.

At up to two Watson–Crick mismatches without the terminal constraint, the frozen background scan predicted one record for each of 16S XS and S and none for the other 27 pairs. This restricted model does not replace the reported guanine–thymine or higher-mismatch screens. The product-length plot presents these finite-panel predictions without assuming size selection will separate target and background products.

The 15 identity matrices contain 130,599 distinct within-window species comparisons. Exact insert uniqueness was 154/166 species for 16S XS and 168/174 for S, M and L; the XL panel contained 146/152 unique representatives. For 12S XL, 53/53 available inserts were unique; COI XL contained 62/62 unique inserts. The COI L identity analysis retained 278 of 283 evaluable species after excluding five ambiguous internal inserts, of which 272 had unique inserts. Complete sequences can therefore differ in primer evaluability and usable internal-barcode status. Neither smaller-panel uniqueness nor higher average divergence alone establishes a better assay."""
zh_findings="""错配梯度将完全匹配与依赖容错的覆盖分开呈现。在各自可评价面板上，16S SD 在每端允许 0、1、2 个错配时分别匹配 0、24、130/174 个物种；加入末三位约束仍保留 130。LD 对应为 29、60、84/174，末端约束后为 82。12S XLD 为 7、16、33/53，末端约束后仍为 33。COI XSD 为 3、18、44/57，末端约束后为 43；COI LD 在两处错配下从 122/283 降至末端受约束后的 103/283。这说明宽松匹配总数不能直接代替正式覆盖率。

在每端最多两处沃森–克里克错配、不要求末三位兼容的模型中，16S XS 和 S 各预测命中一条背景记录，其余 27 对为零；这不替代已报告的鸟嘌呤–胸腺嘧啶及更宽松背景模型。长度图展示实际预测范围，不据此假定产物筛选能分离目标与背景。

15 个序列相似度矩阵共包含 130,599 个窗口内跨物种比较。16S XS 为 154/166 个内部序列唯一的物种，S、M、L 各为 168/174，XL 为 146/152。12S XL 为 53/53，COI XL 为 62/62；COI L 的 283 个位点可评价物种中，5 个内部区段含模糊碱基被排除，余下 278 个中有 272 个内部序列唯一。引物位点可评价与内部区段可用于比较应分别计数；小面板上的唯一率或平均差异程度不能单独作为最佳方案依据。"""
figs=[('mismatch_sensitivity','Mismatch sensitivity / 错配梯度'),('identity_16S','16S primer-free sequence identity / 16S 内部序列相似度'),('identity_12S','12S primer-free sequence identity / 12S 内部序列相似度'),('identity_COI','COI primer-free sequence identity / COI 内部序列相似度'),('identity_distributions','Between-species similarities / 分类层级内的种间相似度'),('product_lengths','Product-length distributions / 产物长度分布')]
for lang in ('en','zh'):
 methods,findings=(en_methods,en_findings) if lang=='en' else (zh_methods,zh_findings)
 title='Anth-28S-inspired computational diagnostics' if lang=='en' else '参考 Anth-28S 的计算诊断'
 text=f'# {title}\n\n'+('Computational diagnostics integrated into the MiCucumber preprint; released primer sequences are unchanged.' if lang=='en' else '已整合进 MiCucumber 预印本的计算诊断；保留当前引物序列。')+'\n\n'
 text+=('## Methods\n\n' if lang=='en' else '## 方法\n\n')+methods+'\n\n'
 text+=('## Results\n\n' if lang=='en' else '## 结果\n\n')+findings+'\n\n'
 text+=('Counts below are species for targets and accession records for backgrounds; ≤0/1/2 are per-primer mismatch ceilings. The final background column has no terminal constraint.\n\n' if lang=='en' else '目标计物种、背景计 accession；≤0/1/2 为每端错配上限，最后一列背景不加末三位约束。\n\n')
 text+=mismatch_table(ENHEAD if lang=='en' else ZHHEAD)+'\n\n'
 text+=table(['Gene','Window','Unambiguous species','Unique inserts','Identical species pairs'] if lang=='en' else ['基因','长度','无模糊物种','序列唯一物种','相同序列物种对'],[[r[k] for k in ('gene','window','n','unique_species','identical_species_pairs')] for r in ID])+'\n\n'
 for stem,label in figs:text+=f'![{label}](figures/{stem}.png)\n\n'
 text+=('## Reproduction' if lang=='en' else '## 复现')+'\n\n```sh\npython3 results/anth28s_evaluation/run.py\npython3 results/anth28s_evaluation/verify.py\npython3 results/anth28s_evaluation/plot.py\npython3 results/anth28s_evaluation/report.py\n```\n\n'
 text+=('C++17 compiler; Python 3.10+; matplotlib and numpy for figures. Run from the repository root. Raw hits, product spans, per-order summaries, full identity matrices, source hashes and independent validation are in [results](results). Exact insert uniqueness uses every retained reference insert, independently of whether a released primer matches it.\n\n' if lang=='en' else '需要 C++17 编译器及 Python 3.10+；绘图另需 matplotlib、numpy。从仓库根目录依次运行。原始命中、产物长度、分目汇总、完整相似度矩阵、输入哈希及独立验证见[结果目录](results)。内部序列唯一性纳入全部保留的参考区段，不以正式引物是否匹配作为前提。\n\n')
 text+='McCartin, L., et al. (2024). Nuclear eDNA metabarcoding primers for anthozoan coral biodiversity assessment. *PeerJ*, 12, e18607. https://doi.org/10.7717/peerj.18607\n'
 (P/('README.md' if lang=='en' else 'README.zh-CN.md')).write_text(text)
