# MiCucumber-XS

XS是一对固定简并引物，不另设A/B/D分支。F `RGYTTTGGTTGGGGCAAC`，R `TTDCCCCAATCCAACATCGA`（5′→3′），简并度4/3。AB525437.1提取的无缺口16S坐标F 1042–1059、R 1213–1232；含引物参考跨度191 bp，原始目标序列预测产物186–203 bp。

XS is one fixed degenerate assay without A/B/D branches. F `RGYTTTGGTTGGGGCAAC`, R `TTDCCCCAATCCAACATCGA` (5′→3′), degeneracy 4/3. Extracted ungapped 16S coordinates on AB525437.1 are F 1042–1059 and R 1213–1232. The primer-inclusive reference span is 191 bp; predicted raw-sequence products are 186–203 bp.

## 匹配与取舍 / Matching and trade-offs

| Metric | XS | SD |
|---|---:|---:|
| Non-Apodida coverage | 88.85% | 80.92% |
| Non-Apodida exact | 13.32% | 9.04% |
| All-target coverage | 85.32% | 77.71% |
| All-target exact | 12.79% | 8.68% |
| Strict WC background, ≤2/primer + terminal 3 nt | 20 | 1 |
| Strict GT background, ≤2/primer + terminal 3 nt | 20 | 3 |
| WC≤3 background, no terminal constraint | 1396 | 26 |
| GT≤2 background, no terminal constraint | 26 | 3 |
| WC≤4 background, no terminal constraint | 2609 | 455 |
| Product range, bp | 186–203 | 198–239 |
| Unshared labels / 107 common amplified labels | 93 (86.92%) | 97 (90.65%) |

XS以短片段和较高覆盖换取更多背景命中，并不全面优于SD。XS严格WC命中20条均为Crinoidea，WC和GT整对完全匹配背景命中均为0。它未通过S–XL原有保守背景门槛，单独记录为放宽背景限制的实验候选。共有标签的条码共享按内部扩增序列判断；不能外推为未知物种或实验鉴定成功率。XS仍漏检Apodida。

XS trades shorter products and higher coverage for more background hits; it does not dominate SD. All 20 strict WC hits are Crinoidea; paired exact background hits are zero under WC and GT. XS fails the original conservative S–XL background gate and is recorded separately as an experimental candidate under relaxed background limits. Barcode sharing uses internal amplicon sequences among common labels and does not establish identification success for unknown taxa or experiments. XS still misses Apodida.

## 热力学 / Thermodynamics

Primer3：50 mM单价盐、1.5 mM Mg、0.6 mM dNTP。50 nM/实际变体时F Tm 55.97–59.57°C、R 56.52–59.96°C；200 nM/方向时F 55.97–59.57°C、R 56.93–60.38°C。最高结构Tm 42.89°C，低于55°C门槛；F/R区间中点温差≤5°C。逐变体末端规则通过。

Primer3 uses 50 mM monovalent salt, 1.5 mM Mg and 0.6 mM dNTP. At 50 nM/variant: F Tm 55.97–59.57°C, R 56.52–59.96°C. At 200 nM/direction: F 55.97–59.57°C, R 56.93–60.38°C. Maximum structure Tm is 42.89°C, below the 55°C gate; the F/R range-midpoint difference is ≤5°C. Every concrete variant passes terminal rules.

## 搜索与复现 / Search and reproduction

围绕MiLily-XS同源区及内侧反向窗口搜索，F起点1040–1060、R起点1193–1213与1146–1166、长度16–24 nt，比较普通及多档简并候选，并补充有面板碱基支持的同位点组合。这是有边界的启发式搜索，不保证全16S最优。最终指标扫描原始FASTA，不用局部比对预测替代。

Search examined the homologous MiLily-XS region and an inner reverse window: F starts 1040–1060, R starts 1193–1213 and 1146–1166, lengths 16–24 nt, comparing ordinary and degenerate candidates plus panel-supported same-site combinations. This bounded heuristic search does not establish a global 16S optimum. Final metrics scan original FASTA rather than substituting local-alignment predictions.

目标产物70–500 bp、内部长度≥20 bp；背景内部距离0–1000 bp；两种方向均扫描。C++穷举与Python位并行算法独立核对351条面板序列的覆盖/完全匹配共702项判断，以及WC/GT严格与完全匹配4组背景集合，差异为0。宽松背景指标由C++扫描重算。重复使用设计参考库，未做湿实验。

Targets require 70–500 bp products and ≥20 bp internal sequence; background internal spacing is 0–1000 bp, scanning both orientations. Independent C++ exhaustive and Python bit-parallel scans agree on 702 coverage/exact decisions for 351 panel sequences and four strict/exact WC/GT background sets. Broader background metrics are recalculated by C++. Design references are reused for evaluation; no wet-lab validation has been performed.

```bash
python scripts/verify_xs.py --output /tmp/MiCucumber-XS-check
```

从项目根目录执行，使用Python标准库与C++17编译器，无需联网。冻结输入在`reproducibility/frozen/xs_inputs.zip`。/ Run from the project root with Python standard libraries and a C++17 compiler; no network is required. Inputs are frozen in `reproducibility/frozen/xs_inputs.zip`.

![XS base matching](../figures/base_matching_XS.svg)

分目名称沿用冻结面板，包括旧标签Aspidochirotida；插画中的现生七目不能替代分目评估。已覆盖代表行来自独立复核的原始结合模板，未覆盖代表展示比对位点。/ Order names follow the frozen panel, including the legacy label Aspidochirotida; the seven extant orders in the illustration do not replace order-level assessment. Covered rows use independently verified raw binding templates; uncovered rows show aligned sites.

[Assessment](../results/xs/assessment.json) · [Independent checks](../results/xs/verification.json) · [Raw hits](../results/xs/independent_hits.tsv) · [Missed references](../results/xs/missed_references.csv) · [By order](../results/xs/by_order.csv) · [Background hits](../results/xs/strict_background_hits.csv) · [Thermodynamics](../results/xs/thermal.csv) · [Common-label resolution](../results/xs/common_label_resolution.csv) · [Verified templates](../results/xs/verified_base_templates.csv)
