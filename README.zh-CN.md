# MiCucumber

**海参线粒体16S计算候选引物。** [English](README.md)

## 当前方案：四个区域，各1对和2对

保留v4opt、S、M、L各1对和2对，共8套方案。优先以 **v4opt两对版开展实验验证**；四个区域是替代选择，不要求同一样本全部运行。两对指**两套独立PCR**，不是已验证的单管混池。目前均未完成湿实验验证。

Apodida不参与优化目标，但仍报告含Apodida的全部目标覆盖。共同面板为 **151个分类名称标签／351个标签内单倍型，其中非Apodida为145个标签**。两种分母不能混用；区域面板见CSV。名称与历史分类尚未进行同物异名统一。

| Version | Pairs | All-target coverage | All-target exact | Non-Apodida coverage | Non-Apodida exact | WC≤3 / GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| v4opt | 1 | 83.97% | 26.39% | 87.45% | 27.48% | 2 / 0 | 742 |
| v4opt | 2 | 85.01% | 39.22% | 88.53% | 40.84% | 2 / 0 | 742 |
| S | 1 | 54.64% | 9.05% | 56.90% | 9.43% | 0 / 0 | 130 |
| S | 2 | 59.94% | 13.69% | 62.42% | 14.25% | 0 / 0 | 131 |
| M | 1 | 67.47% | 32.30% | 70.26% | 33.63% | 4 / 0 | 109 |
| M | 2 | 71.11% | 33.62% | 74.06% | 35.01% | 4 / 0 | 109 |
| L | 1 | 46.42% | 9.33% | 48.34% | 9.71% | 0 / 0 | 486 |
| L | 2 | 53.08% | 11.31% | 55.27% | 11.78% | 0 / 4 | 492 |

Coverage为每条引物≤2处错配且3′末端3碱基完全匹配；Exact为正反引物均完全匹配。按标签等权、标签内单倍型等权计算。非目标数是5,600条参考中的accession并集，不是物种数或reads比例。WC≤4残余风险仍较高；L两对版覆盖有限，仅保留为长区域对照。

## 选择与复核

在已独立验证的96个配对中穷举各区域1–2对组合；WC≤3、GT≤2背景记录并集分别≤5。不要求保留Apodida覆盖。同对数先优化非Apodida覆盖，再允许共同、区域面板分别相对覆盖优先锚点小幅下降以提高完全匹配率：v4opt/M两对版容差2个百分点，其余1个百分点。最优性仅限于已验证候选池。

当前8套方案通过 **21,036项检测结果一致性检查**，以及展开简并碱基后的两种浓度场景结构检查。上游第二轮对1,848条目标与5,600条背景完成346,488项一致性检查。新增两条Apodida位点仍为同源推断参考，已校正方向；6条UNVERIFIED记录排除。参考库同时用于设计与评估，不是独立留出验证。

旧6–9对组合和v0.1.0保留为历史证据：[历史概览](docs/HISTORICAL_README.zh-CN.md)。本次不移动既有发布标签。

## Files / 文件

- [Eight portfolios: primer sequences / 八套配对序列](results/compact/primer_pairs.csv) · [FASTA](results/compact/primers.fasta)
- [v4opt](results/compact/v4opt_1_2pairs.csv) · [S](results/compact/S_1_2pairs.csv) · [M](results/compact/M_1_2pairs.csv) · [L](results/compact/L_1_2pairs.csv)
- [Common and own-region comparisons / 两类面板](results/compact/comparison.csv)
- [Missed taxa / 漏检类群](results/compact/missed_taxa.csv) · [Off-target records / 非目标命中](results/compact/offtargets.csv)
- [Thermodynamics / 热力学](results/compact/thermodynamics.tsv) · [Validation / 复核](results/compact/validation.json)
- [Bilingual HTML report / 双语报告（下载后打开）](results/compact/report.html)

## Amplicon regions / 扩增区域

![MiCucumber reference regions](figures/amplicon_regions.en.png)

This historical map locates the four design windows. Its reaction counts refer to the earlier Apodida-supplemented portfolios, **not** the current 1-/2-pair sets. Reference coordinates are not universal product-length predictions.
旧图展示四个设计区域；图中反应数对应历史Apodida补充组合，**不是当前1对/2对方案**。坐标跨度不等于所有物种的扩增产物长度。

## Reproducibility / 复现

- [Round-two frozen references and independent scan reproduction](evidence/MiCucumber_round2_reproducibility.zip): extract, install its requirements, run `python run_revalidation.py`. Includes the original public reference data and orientation audit. / 含冻结参考数据、方向审计及独立扫描复核入口。
- [Exhaustive 1–4-pair subset analysis](evidence/MiCucumber_compact_reproducibility.zip): extract, install NumPy, run `python work/micucumber_compact/optimize.py`. Recomputes selection from frozen per-pair evidence; does not rerun original sequence scanning. / 从冻结逐配对证据重算组合。
- `python check_release.py` checks retained historical evidence; `python check_compact.py` checks the current eight portfolios and file hashes. The legacy `revalidate.py` remains scoped to the earlier release. / 历史复现入口不代表当前八套方案。
- Final export scripts in `evidence/compact_*.py` are provenance records with original workspace-layout dependencies; the two archives above provide the supported reproduction entry points.

## Copyright / 著作权

Copyright © 2026 Fei Xia (GUIBA-EX). All rights reserved. Public access is not an open-source license. Unauthorized republication and redistribution of protected original materials are prohibited, subject to statutory exceptions, GitHub platform rights and third-party data rights. [Permissions / 声明](COPYRIGHT.md).
