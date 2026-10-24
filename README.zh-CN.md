![MiCucumber](figures/MiCucumber_overview.png)

# MiCucumber

海参线粒体16S引物的计算设计与匹配评估。[English](README.md)

## 方案与命名

四个长度各保留简并单对、普通单对和普通两对组合，另保留S-original对照，共 **13套方案、17条配对记录**。

| 长度 | 简并单对 | 普通单对 | 普通两对 |
|---|---|---|---|
| S | SD | S | SA / SB |
| M | MD | M | MA / MB |
| L | LD | L | LA / LB |
| XL | XLD | XL | XLA / XLB |

D仅表示简并；A、B分别标识具体配对，SA+SB等表示两个独立PCR结果的并集。S-original为原始对照。序列均按5′→3′书写。

**优先以SD开展实验验证。** 普通引物保留作比较，S-original的非目标命中较多。目前尚无湿实验验证。

## 序列与文档

- [全部配对 CSV](sequences/primer_pairs.csv) · [全部序列 FASTA](sequences/primers.fasta) · [S-original](sequences/MiCucumber-S-original.fasta)
- [S](sequences/MiCucumber-S.csv) · [M](sequences/MiCucumber-M.csv) · [L](sequences/MiCucumber-L.csv) · [XL](sequences/MiCucumber-XL.csv)
- [命名](docs/NAMING.zh-CN.md) · [方法](docs/METHODS.zh-CN.md) · [复现](docs/REPRODUCIBILITY.zh-CN.md) · [文件索引](docs/FILES.zh-CN.md)
- [双语报告](report.html)（下载后打开） · [完整比较表](results/comparison.csv)

## 共同面板结果

下表的覆盖率和完全匹配率均为**非Apodida指标**。共同面板包含151个分类名称标签、351个标签内单倍型，其中非Apodida为145个标签；计算采用标签等权、标签内单倍型等权。包含Apodida的结果及各区域面板分母见完整比较表。

| 方案 | 覆盖率 | 完全匹配率 | WC≤3 | GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
| SD | 87.45% | 27.48% | 2 | 0 | 742 |
| MD | 56.90% | 9.43% | 0 | 0 | 130 |
| LD | 70.26% | 33.63% | 4 | 0 | 109 |
| XLD | 48.34% | 9.71% | 0 | 0 | 486 |
| S | 56.78% | 0.34% | 0 | 0 | 2 |
| SA+SB | 71.96% | 0.34% | 0 | 0 | 2 |
| M | 14.05% | 0.00% | 0 | 0 | 0 |
| MA+MB | 23.70% | 3.91% | 0 | 0 | 0 |
| L | 35.24% | 3.97% | 0 | 0 | 0 |
| LA+LB | 46.68% | 8.00% | 0 | 0 | 0 |
| XL | 22.88% | 2.93% | 0 | 0 | 0 |
| XLA+XLB | 28.86% | 5.23% | 0 | 0 | 1 |
| S-original | 89.84% | 76.75% | 3248 | 3401 | 3923 |

覆盖允许每条引物≤2处错配，且3′末端3 nt完全相容；完全匹配要求正反均0错配。背景列为5,600条参考记录中的命中accession数。WC采用Watson–Crick配对，GT为容许G–T配对的敏感性模型；数字表示每条引物允许的最大错配数，详见[模型定义](docs/METHODS.zh-CN.md#非目标筛选)。

## 各长度匹配图

左图每列为一个共同面板单倍型，按目和物种排序；右图为非Apodida加权比例，标注“覆盖率 / 完全匹配率”。蓝绿色为完全匹配，金黄色为允许错配命中，浅灰色为未命中。A、B单独显示，并给出A+B的合用结果。

![S matching](figures/matching_S.png)

![M matching](figures/matching_M.png)

![L matching](figures/matching_L.png)

![XL matching](figures/matching_XL.png)

[匹配汇总](results/matching/summary.csv) · [逐参考匹配状态](results/matching/detection.csv)。共21组匹配概况、7,371条逐参考记录。

## 参考区域

![S M L XL](figures/amplicon_regions.zh.png)

图示为AB525437.1的同源种子窗口，参考跨度分别为208、231、315、387 bp；各分类群的实际产物长度可以不同。

## 数据与复现

参考库包括1,848条目标和5,600条背景记录。Apodida不参与筛选目标，但保留在全部目标统计中。设计与评估使用同一冻结参考库。

```bash
python scripts/check_release.py
```

完整计算流程、依赖与绘图入口见 [复现说明](docs/REPRODUCIBILITY.zh-CN.md)。

## 著作权

Copyright © 2026 Fei Xia (GUIBA-EX). All rights reserved. 使用与转载规则见[完整声明](COPYRIGHT.md)。
