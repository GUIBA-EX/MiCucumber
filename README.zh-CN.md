![MiCucumber](figures/MiCucumber_overview.png)

置顶图展示现生海参7个目的代表：Apodida、Dendrochirotida、Elasipodida、Holothuriida、Molpadida、Persiculida、Synallactida。分目匹配结果仍沿用当前参考面板标签。[图示说明](figures/overview_design.md)。

![Current binding positions](figures/binding_positions.svg)

共同坐标参考跨度：S 226、M 245、L 302、XL 396 bp。实际产物随类群变化。

# MiCucumber

海参线粒体16S引物的计算设计与匹配评估。[English](README.md)

## 命名与方案

每个长度保留一对简并引物、一对普通引物及普通A/B两对方案；另保留S-original原始对照，共13套方案、17条配对记录、34条FASTA序列。D仅标记简并配对；A/B表示两次独立PCR的组件。

| Region | Degenerate | Ordinary | Ordinary A/B |
|---|---|---|---|
| S | 66.85% | 3.35% | 4 | 3 | 331 |
| M | 33.56% | 5.52% | 1 | 2 | 13 |
| L | 41.03% | 7.87% | 0 | 0 | 46 |
| XL | 15.81% | 0.69% | 1 | 1 | 756 |

**3′末端允许简并。** 按IUPAC相容性判定末端匹配，并逐一检查全部实际变体。每个变体均无末端三连同碱基，末端3位至少含1个G/C、末端5位含1–4个G/C，整条序列连续同碱基不超过4个。最后一位不强制固定，也不强制为G/C。S-original为不参与上述筛选的原始对照。

## 保留理由

按奥卡姆剃刀原则，每个长度仅保留一个正式D方案：SD采用低简并增强（2/8），MD采用严格背景档（64/4），LD采用覆盖增强（32/1），XLD保留原方案（2/1）。SD更激进档、MD 128/4档和XLD小增益档不进入正式序列。本次A/B重选保留普通单对、D及S-original不变，每组四套F/R起止坐标完全相同。这是基于收益与复杂度的人工取舍，不是预设统计阈值或已验证PCR最优条件。

[Before/after / 前后比较](docs/DECISIONS.md)

## 共同面板结果

下表覆盖与完全匹配均为非Apodida指标。共同面板151个分类名称标签、351个单倍型，其中非Apodida为145个标签；标签及标签内单倍型等权。全部目标指标见CSV。背景为5,600条记录。

| 方案 | 覆盖率 | 完全匹配率 | WC≤3 | GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
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

覆盖允许每条引物≤2处错配且末端3位完全相容；完全匹配要求F/R均零错配。背景数为accession数，不是实验扩增比例。GT为单独的G–T容忍敏感性模型。

WC≤4下仍存在明显背景风险，特别是L与XL；小的WC≤3/GT≤2数字不能证明环境样本中的低非目标扩增。所有方案均待实验验证。[修正前后比较与复核](docs/TERMINAL_VALIDATION.md)。

## 序列、坐标与证据

[Primer pairs](sequences/primer_pairs.csv) · [FASTA](sequences/primers.fasta) · [Comparison](results/current/comparison.csv) · [Coordinates](results/current/binding_positions.csv) · [Missed references](results/terminal_optimization/missed_references.csv) · [Terminal audit](results/terminal_optimization/terminal_audit.csv) · [Verification](results/terminal_optimization/verification.json)

[Methods](docs/METHODS.md) · [中文方法](docs/METHODS.zh-CN.md) · [Reproduction](docs/REPRODUCIBILITY.md) · [文件索引 / File index](docs/FILES.md) · [Bilingual report](report.html)

## 碱基匹配图

蓝色为IUPAC相容，橙色为错配，紫色为可能的G–T配对；方框标出末端3位。简并图显示单对，普通图显示A/B。各目展示加权最常见的结合序列；完整网页包含所有方案与参考变体。

![SD base matching](figures/base_matching_SD.svg)

![S base matching](figures/base_matching_S.svg)

![MD base matching](figures/base_matching_MD.svg)

![M base matching](figures/base_matching_M.svg)

![LD base matching](figures/base_matching_LD.svg)

![L base matching](figures/base_matching_L.svg)

![XLD base matching](figures/base_matching_XLD.svg)

![XL base matching](figures/base_matching_XL.svg)

[Full base alignment](results/terminal_optimization/base_matching.html)

## 复核与范围

11,200项目标状态与32项背景集合独立复核全部一致。参考数据同时用于设计与评估；Apodida不参与选择目标，但保留在全部目标报告。两对结果为独立PCR并集，不代表混池实验。

```bash
python scripts/check_release.py
```

## Copyright

Copyright © 2026 Fei Xia (GUIBA-EX). All rights reserved. [Terms / 使用声明](COPYRIGHT.md).


扩大同坐标搜索后，各长度A/B均有双方独有贡献；两项并集指标均不低于此前方案。普通单对和D保持不变。依据样本目标选择单对或互补双对。[互补性与独有命中](docs/AB_COMPLEMENTARITY.md)
