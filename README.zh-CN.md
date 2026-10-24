![MiCucumber](figures/MiCucumber_overview.png)

![Current binding positions](figures/binding_positions.svg)

徽标为SD、MD、LD、XLD的参考跨度：223、247、310、394 bp。位置图直接使用当前引物坐标，全部按同一线性比例绘制；实际产物长度随类群变化。

# MiCucumber

海参线粒体16S引物的计算设计与匹配评估。[English](README.md)

## 命名与方案

每个长度保留一对简并引物、一对普通引物及普通A/B两对方案；另保留S-original原始对照，共13套方案、17条配对记录、34条FASTA序列。D仅标记简并配对；A/B表示两次独立PCR的组件。

| Region | Degenerate | Ordinary | Ordinary A/B |
|---|---|---|---|
| S | SD | S | SA / SB |
| M | MD | M | MA / MB |
| L | LD | L | LA / LB |
| XL | XLD | XL | XLA / XLB |

**3′末端允许简并。** 按IUPAC相容性判定末端匹配，并逐一检查全部实际变体。每个变体均无末端三连同碱基，末端3位至少含1个G/C、末端5位含1–4个G/C，整条序列连续同碱基不超过4个。最后一位不强制固定，也不强制为G/C。S-original为不参与上述筛选的原始对照。

## 共同面板结果

下表覆盖与完全匹配均为非Apodida指标。共同面板151个分类名称标签、351个单倍型，其中非Apodida为145个标签；标签及标签内单倍型等权。全部目标指标见CSV。背景为5,600条记录。

| 方案 | 覆盖率 | 完全匹配率 | WC≤3 | GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
| SD | 79.76% | 3.28% | 4 | 5 | 312 |
| S | 67.98% | 2.93% | 4 | 3 | 451 |
| SA+SB | 74.71% | 7.07% | 4 | 3 | 451 |
| MD | 47.42% | 6.44% | 2 | 1 | 137 |
| M | 33.56% | 5.52% | 1 | 2 | 13 |
| MA+MB | 57.64% | 8.79% | 2 | 3 | 40 |
| LD | 65.40% | 6.55% | 5 | 0 | 1157 |
| L | 41.03% | 7.87% | 0 | 0 | 46 |
| LA+LB | 55.14% | 16.01% | 5 | 5 | 436 |
| XLD | 24.09% | 0.69% | 5 | 4 | 1357 |
| XL | 21.33% | 0.69% | 5 | 4 | 1357 |
| XLA+XLB | 21.33% | 0.69% | 5 | 4 | 1359 |
| S-original | 89.84% | 76.75% | 3248 | 3401 | 3923 |

覆盖允许每条引物≤2处错配且末端3位完全相容；完全匹配要求F/R均零错配。背景数为accession数，不是实验扩增比例。GT为单独的G–T容忍敏感性模型。

**这是严格末端约束下的候选比较，不是全面性能提升。** 普通S、M、L较上一版改善；简并方案的完全匹配率下降，XL覆盖较低，A/B两对也未增加其共同面板覆盖或完全匹配，不建议为此增加PCR对数。SD覆盖79.76%，但完全匹配仅3.28%。优先比较普通M单对与MA+MB，并结合样品目的选择SD或普通S。

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
