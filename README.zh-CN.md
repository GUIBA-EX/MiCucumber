![MiCucumber](figures/MiCucumber_overview.png)

# MiCucumber

[English](README.md)

MiCucumber 是面向海参类环境 DNA 的线粒体 16S rRNA 候选引物，覆盖 XS、S、M、L、XL 五个长度。每个长度保留最新筛选的单对候选；同一长度的正反向引物使用相同参考坐标。
主要指标按**可评价物种等权**：每个物种选一条参考序列，计算预测覆盖与完全匹配比例。参考面板包含 174 个具名物种；数据库中的物种数量不能代表各目的全球丰富度。
海参 XS、S–L、XL 分别有 166、174、152 个物种可评价；缺少结合区域的物种不计作漏检。

[参考面板 / Reference panel](results/species_qc/panel.csv) · [分类与覆盖 / Coverage by order](results/species_refine/by_order.csv) · [参考序列审核 / Reference curation](results/species_qc/README.md)

![Binding positions](figures/amplicon_regions.en.svg)

## 当前表现

| Candidate | Species coverage | Exact | Strict WC / GT | WC≤3 / GT≤2 |
|---|---:|---:|---:|---:|
| XS-R100-coverage | 75/166 (45.18%) | 0/166 (0.00%) | 0 / 0 | 33 / 2 |
| S-R20-coverage | 124/174 (71.26%) | 0/174 (0.00%) | 0 / 3 | 4 / 4 |
| S-R100-coverage | 130/174 (74.71%) | 0/174 (0.00%) | 0 / 5 | 58 / 6 |
| S-R100-exact | 124/174 (71.26%) | 1/174 (0.57%) | 0 / 5 | 54 / 6 |
| M-R20-coverage | 89/174 (51.15%) | 24/174 (13.79%) | 0 / 15 | 3 / 15 |
| L-R20-coverage | 85/174 (48.85%) | 1/174 (0.57%) | 0 / 0 | 15 / 19 |
| L-R20-exact | 82/174 (47.13%) | 29/174 (16.67%) | 0 / 0 | 0 / 0 |
| XL-R20-coverage | 43/152 (28.29%) | 3/152 (1.97%) | 0 / 10 | 1 / 13 |
| XL-R100-coverage | 45/152 (29.61%) | 3/152 (1.97%) | 0 / 10 | 48 / 13 |

预测覆盖要求每条引物最多 2 个错配且末端 3 个碱基兼容；完全匹配要求两条引物均无错配。严格 WC/GT 为上述规则下的非目标记录数；WC≤3 和 GT≤2 是不施加末端约束的宽松筛查。

## 筛选与取舍

新版候选每条引物简并度不超过 8，简并位点限于 3′ 半段；覆盖优先和完全匹配优先候选分别保留。指标为计算预测，需通过实验验证。

[筛选结果与复核 / Screening and verification](results/species_refine/README.md) · [引物序列 / Primer sequences](sequences/primer_pairs.csv)

## XS

| Name | F (5′→3′) | R (5′→3′) |
|---|---|---|
| XS-R100-coverage | `AACTTTGGTTGGGGYAAC` | `TTTCCCCAATCCAACATCGA` |

![XS-R100-coverage base matching](results/species_refine/XS/base_matching_XS-R100-coverage.svg)

## S

| Name | F (5′→3′) | R (5′→3′) |
|---|---|---|
| S-R20-coverage | `CAAGAAAGACGARAAGACCCTGTC` | `GAGGAGATAACGCTGTTATCCCTG` |
| S-R100-coverage | `TAAGAAAGACGARAAGACCCTRTC` | `GAGAAGATGACGCTGTTATCCCTR` |
| S-R100-exact | `TAAGAAAGACGAGAAGACCCTRTC` | `GAGGAGATAACGCTGTTATCCCTG` |

![S-R20-coverage base matching](results/species_refine/S/base_matching_S-R20-coverage.svg)

![S-R100-coverage base matching](results/species_refine/S/base_matching_S-R100-coverage.svg)

![S-R100-exact base matching](results/species_refine/S/base_matching_S-R100-exact.svg)

## M

| Name | F (5′→3′) | R (5′→3′) |
|---|---|---|
| M-R20-coverage | `AAACTTCTATTHAYGTGAAGAA` | `GTTATCCCTGCGGTAACT` |

![M-R20-coverage base matching](results/species_refine/M/base_matching_M-R20-coverage.svg)

## L

| Name | F (5′→3′) | R (5′→3′) |
|---|---|---|
| L-R20-coverage | `AGACTTGTATGAAYGGCATWACMT` | `CGCTGTTATCCCTGCGGT` |
| L-R20-exact | `AGACTTGTATGAAYGGCRAAACMT` | `CGCTGTTATCCCTGCRGT` |

![L-R20-coverage base matching](results/species_refine/L/base_matching_L-R20-coverage.svg)

![L-R20-exact base matching](results/species_refine/L/base_matching_L-R20-exact.svg)

## XL

| Name | F (5′→3′) | R (5′→3′) |
|---|---|---|
| XL-R20-coverage | `GGTAACGCCTGCCCARTGGA` | `GAGATTACGCTGTTATCCCTGCGGTAACTD` |
| XL-R100-coverage | `GGTAACGCCTGCCCARTGRA` | `GAGATTACGCTGTTATCCCTGCGGTAACTD` |

![XL-R20-coverage base matching](results/species_refine/XL/base_matching_XL-R20-coverage.svg)

![XL-R100-coverage base matching](results/species_refine/XL/base_matching_XL-R100-coverage.svg)

## 方法与数据

[参考数据及物种去重](results/species_qc/README.md) · [筛选比较](results/species_refine/comparison.csv) · [著作权声明](COPYRIGHT.md)
