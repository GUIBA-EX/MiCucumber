![MiCucumber · XS / S / M / L / XL](figures/MiCucumber_overview.png)

置顶图展示现生海参七目代表；徽章为AB525437.1提取的无缺口16S参考跨度：XS 191、S 226、M 245、L 302、XL 396 bp。实际产物因类群而异。[插画说明](figures/overview_design.md)

# MiCucumber

海参线粒体16S引物、分类群覆盖评估与复现资料。[English](README.md)

## 最新物种参考面板筛选

最新候选采用每物种一条参考序列，对可评价物种等权。详见[最新筛选及碱基匹配图](results/species_refine/README.md)、[引物序列](results/species_refine/sequences.csv)、[各目结果](results/species_refine/by_order.csv)和[参考序列整理](results/species_qc/README.md)。原引物保留供对照；下文原有统计使用此前的参考面板。

## 当前简并方案

每个长度仅保留一对简并方案。XS沿用固定单对名称；S–XL的D已按目间覆盖重新选定，普通、A、B与D在各长度内的F/R起止坐标完全相同。

主指标为**目间等权覆盖率**：先算目内至少一条参考命中的名称标签比例，再对各目等权平均；完全匹配也采用同一分层方式。主分析包含Apodida。当前面板为351个单倍型、151个名称标签，使用5个冻结目标签（含旧目名Aspidochirotida），不是现生七目的完整覆盖评估。

| 方案 | 目间覆盖率 | 目间完全匹配率 | 检出标签 | F/R简并度 | 严格WC/GT背景 |
|---|---:|---:|---:|---:|---:|
| XS | 75.52% | 15.42% | 131/151 | 4/3 | 20 / 20 |
| SD | 66.03% | 4.95% | 133/151 | 4/12 | 3 / 6 |
| MD | 73.18% | 29.72% | 124/151 | 128/2 | 2 / 9 |
| LD | 61.63% | 15.99% | 111/151 | 128/8 | 0 / 0 |
| XLD | 35.95% | 4.00% | 37/151 | 2/24 | 0 / 7 |

S、M、L、XL分别选自SD-T10、MD-T4、LD-T7、XLD-T8。S采用当前方案与覆盖候选的IUPAC并集；M不为额外2.15个百分点覆盖接受WC≤3背景从58增至252条；XL覆盖相同时选择更低简并度。筛选要求末端与热力学通过、每方向简并度≤128、宽松WC≤3/GT≤2各≤100条、严格WC/GT各≤20条；XS单独保留其已说明的背景放宽。这里的“首选”限于本次已复核候选，不宣称全局最优。

[选择依据与序列](docs/D_OPTIMIZATION.md) · [指标定义与分目明细](docs/TAXONOMIC_COVERAGE.md) · [机器可读选择规则](results/current/D_selection_policy.json)

## 引物序列（5′→3′）

| Assay | F | R |
|---|---|---|
| XS | `RGYTTTGGTTGGGGCAAC` | `TTDCCCCAATCCAACATCGA` |
| SD | `CMAGAAAGACGAGAAGACCCYGTC` | `RAGRAGATDACGCTGTTATCCCTG` |
| MD | `AAAYTYCTAYYNRCGTGAAGAA` | `GTTATCCCTGCGGTARCT` |
| LD | `RRACYWGTATGAAYGGCATWACMT` | `CGCTGTTATCCCTRCRGW` |
| XLD | `RGTCACGCCTGCCCAGTGGA` | `RAGATDACGCTGTTATCCCTGCGGTAACTN` |

## 普通方案与命名

S–XL同时保留普通单对和普通A/B。A/B分别进行PCR，以命中并集统计，不代表多重PCR。D为简并单对；XS无额外D后缀。S-original为原版对照。共14套方案、18条配对记录、36条FASTA记录。

| Region | Degenerate | Ordinary | Ordinary A/B |
|---|---|---|---|
| XS | XS | — | — |
| S | SD | S | SA / SB |
| M | MD | M | MA / MB |
| L | LD | L | LA / LB |
| XL | XLD | XL | XLA / XLB |

<details>
<summary>辅助指标：平均种内匹配与背景命中</summary>

以下匹配率排除Apodida，按名称标签等权计算种内参考匹配比例，并非分类群检出率。WC≤3、GT≤2和WC≤4背景列不强制末端兼容；严格背景采用每条≤2错配且末端3 nt兼容。背景库5,600条，计数不是实验扩增比例。

| 方案 | 平均种内匹配率 | 平均种内完全匹配率 | WC≤3 | GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
| XS | 88.85% | 13.32% | 1396 | 26 | 2609 |
| SD | 90.73% | 11.06% | 71 | 7 | 475 |
| S | 66.85% | 3.35% | 4 | 3 | 331 |
| SA+SB | 73.49% | 5.53% | 4 | 3 | 378 |
| MD | 83.92% | 26.90% | 58 | 9 | 536 |
| M | 33.56% | 5.52% | 1 | 2 | 13 |
| MA+MB | 36.36% | 10.80% | 1 | 3 | 39 |
| LD | 74.80% | 7.59% | 21 | 21 | 485 |
| L | 41.03% | 7.87% | 0 | 0 | 46 |
| LA+LB | 43.33% | 15.00% | 0 | 0 | 46 |
| XLD | 24.78% | 0.69% | 13 | 10 | 1392 |
| XL | 15.81% | 0.69% | 1 | 1 | 756 |
| XLA+XLB | 24.29% | 0.69% | 1 | 1 | 756 |
| S-original | 89.84% | 76.75% | 3248 | 3401 | 3923 |

</details>

## 坐标与碱基匹配

![Current binding positions](figures/binding_positions.svg)

蓝色为IUPAC兼容，橙色为错配，方框为3′末端3 nt。当前D图采用独立复核的原始结合模板；无配对命中的目显示灰色空位，不能解读为模板缺失。普通图另外标示潜在G–T配对。代表行不替代完整面板统计。

![XS base matching](figures/base_matching_XS.svg)

![SD base matching](figures/base_matching_SD.svg)

![S base matching](figures/base_matching_S.svg)

![MD base matching](figures/base_matching_MD.svg)

![M base matching](figures/base_matching_M.svg)

![LD base matching](figures/base_matching_LD.svg)

![L base matching](figures/base_matching_L.svg)

![XLD base matching](figures/base_matching_XLD.svg)

![XL base matching](figures/base_matching_XL.svg)

## 复核与使用范围

末端允许简并，逐实际变体检查：无末端同碱基三连，末端3 nt至少1个G/C，末端5 nt有1–4个G/C，无超过4个的同聚物。两种浓度下要求最高发卡/二聚体Tm<55°C、F/R Tm区间中点温差≤5°C。

本轮10个候选共7,020项目标判断、40组严格/完全背景集合独立扫描与冻结输入复现一致；当前4个D方案来自其中。XS与普通/A/B保留各自的冻结复核证据。Apodida仍为0/6，高简并方案有变体稀释代价；设计与评估共用参考库，全部方案仍需湿实验验证。

```bash
python scripts/check_release.py
python scripts/check_ab.py
python scripts/check_taxon_optimization.py
python scripts/taxon_coverage.py
```

## 数据与方法

[Primer pairs](sequences/primer_pairs.csv) · [FASTA](sequences/primers.fasta) · [Taxonomic comparison](results/current/taxonomic_comparison.csv) · [Coordinates](results/current/binding_positions.csv)

[Methods](docs/METHODS.md) · [中文方法](docs/METHODS.zh-CN.md) · [Reproduction](docs/REPRODUCIBILITY.md) · [File index](docs/FILES.md) · [Report](report.html)

## 著作权

Copyright © 2026 Fei Xia (GUIBA-EX). All rights reserved. [Terms / 使用声明](COPYRIGHT.md).
