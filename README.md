# MiCucumber

**Sea-cucumber mitochondrial 16S computational primer candidates.** [中文](README.zh-CN.md)

## Current recommendation: one or two pairs per region

Eight portfolios are retained: v4opt, S, M and L, each with one-pair and two-pair versions. Prefer **two-pair v4opt for initial validation**. Regions are alternatives; samples do not require all eight assays. Two pairs mean **two independent PCRs**, not a validated single-tube cocktail. No wet-lab validation is claimed.

Apodida is excluded from the optimization objective, not hidden from reporting. The common panel contains **151 taxon-name labels / 351 within-label haplotypes**, including **145 non-Apodida labels**. Both denominators are shown; own-region panels are in the CSV. Names and historical taxonomy are not synonym-reconciled.

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

Coverage permits ≤2 mismatches per primer with the last three 3′ bases exact; exact coverage requires both primers to match. Labels and within-label haplotypes are equally weighted. Background counts are accession unions among 5,600 records, not species counts or predicted read fractions. WC≤4 risk remains substantial. L has limited coverage even with two pairs and is retained as a long-region comparator.

## Selection and evidence

Selections derive from exhaustive one-/two-pair subsets of the independently checked 96-pair candidate pool, with WC≤3 and GT≤2 unions each ≤5 records. At each pair count, optimize non-Apodida coverage first, then exact coverage within a limited loss on both common and own-region panels: 2 percentage points for two-pair v4opt/M, 1 for other sets. This is conditional selection, not global primer optimality. Apodida coverage has no minimum requirement.

Current eight portfolios passed **21,036 target consistency checks**, plus expanded-IUPAC structural checks under two concentration scenarios. Upstream round-two validation passed 346,488 consistency checks on 1,848 target and 5,600 background records. Two added Apodida loci are homology-inferred, direction-corrected references; six UNVERIFIED records were excluded. Discovery and evaluation reuse references; this is not held-out validation.

The former 6–9-pair portfolios and version v0.1.0 remain historical evidence: [previous overview](docs/HISTORICAL_README.md). Existing release tags are unchanged.

## Nondegenerate comparators (2026-10-24)

Added eight **A/C/G/T-only** one-/two-pair portfolios across four regions, while preserving the **original v4 unchanged**. Enumerated 2,644 concrete variants of the eight current parent pairs. Selected portfolios passed 31,428 detection-result agreement checks and a complete reproduction run.

**Removing degeneracy substantially reduces coverage and exact matching; these are comparators, not replacements for the current degenerate portfolios.** Original v4 retains its degeneracies and higher target coverage but has extensive background hits. Below: non-Apodida common-panel metrics (145 name labels). All-target, own-region and change tables are supplied separately. Two pairs mean separate PCRs.

| Portfolio | Non-Apodida coverage | Non-Apodida exact | WC≤3 | GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
| MiCucumber-v4opt-ND-1pair | 56.78% | 0.34% | 0 | 0 | 2 |
| MiCucumber-v4opt-ND-2pair | 71.96% | 0.34% | 0 | 0 | 2 |
| MiCucumber-S-ND-1pair | 14.05% | 0.00% | 0 | 0 | 0 |
| MiCucumber-S-ND-2pair | 23.70% | 3.91% | 0 | 0 | 0 |
| MiCucumber-M-ND-1pair | 35.24% | 3.97% | 0 | 0 | 0 |
| MiCucumber-M-ND-2pair | 46.68% | 8.00% | 0 | 0 | 0 |
| MiCucumber-L-ND-1pair | 22.88% | 2.93% | 0 | 0 | 0 |
| MiCucumber-L-ND-2pair | 28.86% | 5.23% | 0 | 0 | 1 |
| MiCucumber-v4-original | 89.84% | 76.75% | 3248 | 3401 | 3923 |

[Sequences / 序列](results/nondegenerate/primer_pairs.csv) · [Original v4 / 原版](results/nondegenerate/v4_original.fasta) · [Comparison / 比较](results/nondegenerate/comparison.csv) · [Changes / 与简并版差值](results/nondegenerate/change_vs_degenerate.csv) · [Bilingual report / 双语报告](results/nondegenerate/report.html) · [Reproduction / 完整复现包](results/nondegenerate/reproducibility.zip)

Reproduction: extract the ZIP, install `requirements.txt` and a C++17 compiler, then run `python run_reproduction.py`. All input references, scripts and expected results are included. No wet-lab validation or independent holdout evaluation. / 解压复现包，安装依赖与C++17编译器，运行入口；含参考数据、脚本及预期结果，尚无湿实验或独立留出验证。

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
