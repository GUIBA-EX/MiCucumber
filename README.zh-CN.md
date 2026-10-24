![MiCucumber · XS / S / M / L / XL](figures/MiCucumber_overview.png)

置顶图展示现生海参七个目的代表，徽章为AB525437.1上的含引物参考跨度：XS 191、S 226、M 245、L 302、XL 396 bp。物种间实际产物长度不同。分目分析沿用冻结面板标签，不能由插画推断七个目均已覆盖。 [插画说明](figures/overview_design.md)

# MiCucumber

海参线粒体16S引物的计算设计、匹配评估与复现资料。 [English](README.md)

## 方案与命名

XS为一对固定简并引物，直接命名XS。S、M、L、XL各保留D简并单对、普通单对及互补普通A/B；每个长度内普通、A、B、D的F/R起止坐标完全相同。A/B为独立PCR的并集，各有独有命中。另保留S-original原版对照。合计14套方案、18条配对记录、36条FASTA记录。

| 长度 | 简并 | 普通 | 普通A/B |
|---|---|---|---|
| XS | XS | — | — |
| S | SD | S | SA / SB |
| M | MD | M | MA / MB |
| L | LD | L | LA / LB |
| XL | XLD | XL | XLA / XLB |

## XS短片段方案

```text
XS-F  5′-RGYTTTGGTTGGGGCAAC-3′
XS-R  5′-TTDCCCCAATCCAACATCGA-3′
```

F/R简并度4/3；R=A/G，Y=C/T，D=A/G/T。参考坐标F 1042–1059、R 1213–1232，参考跨度191 bp，实际预测产物186–203 bp。XS以更短片段与较高覆盖为取舍；SD保留为背景命中更少的比较方案。

同面板XS覆盖88.85%、完全匹配13.32%，SD分别为80.92%、9.04%。按目标相同规则筛查背景（每条≤2错配且末端3 nt兼容），XS在WC/GT模型下各命中20条，WC命中均为海百合；SD分别为1/3条。整对完全匹配的背景命中XS为0。放宽为不约束末端的WC≤3时，XS命中1,396条，SD为26条。XS未通过S–XL原有保守背景门槛，作为明确放宽背景限制的实验候选保留。

XS仍漏检Apodida。XS与SD共同扩增的107个标签中，未观察到内部条码共享的标签分别为93（86.92%）与97（90.65%）；该指标是当前参考库内的序列区分能力，不是实验鉴定成功率。 [XS分析与证据](docs/XS.md)

## 同面板结果

主表排除Apodida：351个单倍型、151个分类名称标签，其中非Apodida为145个标签；标签等权，标签内单倍型等权。覆盖允许每条≤2错配且末端3 nt IUPAC兼容；完全匹配要求两条引物均无错配。全目标指标见CSV。背景库5,600条；WC为标准配对，GT为额外允许G–T的敏感性模型。下表背景计数不强制末端兼容，均为记录数，不是扩增比例。

| 方案 | 覆盖率 | 完全匹配率 | WC≤3 | GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
| XS | 88.85% | 13.32% | 1396 | 26 | 2609 |
| SD | 80.92% | 9.04% | 26 | 3 | 455 |
| S | 66.85% | 3.35% | 4 | 3 | 331 |
| SA+SB | 73.49% | 5.53% | 4 | 3 | 378 |
| MD | 67.17% | 25.48% | 2 | 4 | 76 |
| M | 33.56% | 5.52% | 1 | 2 | 13 |
| MA+MB | 36.36% | 10.80% | 1 | 3 | 39 |
| LD | 66.78% | 19.14% | 20 | 16 | 1168 |
| L | 41.03% | 7.87% | 0 | 0 | 46 |
| LA+LB | 43.33% | 15.00% | 0 | 0 | 46 |
| XLD | 19.95% | 0.69% | 1 | 1 | 1309 |
| XL | 15.81% | 0.69% | 1 | 1 | 756 |
| XLA+XLB | 24.29% | 0.69% | 1 | 1 | 756 |
| S-original | 89.84% | 76.75% | 3248 | 3401 | 3923 |

## 坐标与碱基匹配

![Current binding positions](figures/binding_positions.svg)

XS图中的已覆盖代表使用原始序列独立复核的结合模板，未覆盖代表展示比对位点。S–XL图沿用各方案的代表结合序列。蓝色为兼容，橙色为错配，灰色为缺口或未知，方框标示3′末端3 nt；S–XL图另以紫色标示潜在G–T配对。代表行不替代完整面板统计。

![XS base matching](figures/base_matching_XS.svg)

![SD base matching](figures/base_matching_SD.svg)

![S base matching](figures/base_matching_S.svg)

![MD base matching](figures/base_matching_MD.svg)

![M base matching](figures/base_matching_M.svg)

![LD base matching](figures/base_matching_LD.svg)

![L base matching](figures/base_matching_L.svg)

![XLD base matching](figures/base_matching_XLD.svg)

![XL base matching](figures/base_matching_XL.svg)

[S–XL完整碱基图 / Full S–XL alignment](results/terminal_optimization/base_matching.html)

## 设计与复核

允许3′末端简并，逐个实际变体检查：末端无同碱基三连、末端3 nt至少1个G/C、末端5 nt有1–4个G/C、全长无超过4个的同聚物。XS通过末端规则和两种浓度热力学检查。S-original为原版对照。

XS的C++穷举与Python位并行全序列扫描：702项目标判断、4组严格/完全背景命中集合均一致。S–XL独立复核11,200项目标判断、32组背景集合均一致。两部分复核范围独立记录；设计和评估共用参考库，全部方案仍需湿实验验证。

```bash
python scripts/check_release.py
python scripts/check_ab.py
python scripts/verify_xs.py --output /tmp/MiCucumber-XS-check
```

## 数据与方法

[引物 / Primer pairs](sequences/primer_pairs.csv) · [FASTA](sequences/primers.fasta) · [结果 / Comparison](results/current/comparison.csv) · [坐标 / Coordinates](results/current/binding_positions.csv) · [XS证据 / Evidence](results/xs/)

[Methods](docs/METHODS.md) · [中文方法](docs/METHODS.zh-CN.md) · [复现 / Reproduction](docs/REPRODUCIBILITY.md) · [文件索引 / File index](docs/FILES.md) · [A/B互补性 / Complementarity](docs/AB_COMPLEMENTARITY.md) · [报告 / Report](report.html)

## 著作权

Copyright © 2026 Fei Xia (GUIBA-EX). All rights reserved. [使用声明 / Terms](COPYRIGHT.md).
