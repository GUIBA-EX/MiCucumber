# MiCucumber

**海参线粒体16S引物设计与计算评估。**

[English](README.md) · [方法说明](docs/METHODS.zh-CN.md) · [复现说明](docs/REPRODUCIBILITY.md)

本项目参考 MiStar 工作流，优化历史 MiCucumber 引物，优先降低非目标风险，使用同位置多对引物补充覆盖，并设计多个长度系列。**v0.1.0 是计算候选发布版，尚未经湿实验验证，也不代表历史引物“v5”。**

## 最新结果

| Version / 版本 | Independent PCRs / 独立PCR | Overall coverage / 总覆盖 | Apodida panel / 面板 | WC≤3 / GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
| v4opt + Apodida | 7 | 92.51% | 2/4 | 2 / 0 | 750 |
| S + Apodida | 7 | 70.70% | 3/4 | 0 / 0 | 130 |
| M + Apodida | 6 | 79.48% | 2/4 | 4 / 0 | 109 |
| L + Apodida | 9 | 66.76% | 4/4 | 0 / 4 | 492 |

总覆盖率基于共同面板149个名称标签、347个标签内去重单倍型，标签等权、标签内单倍型等权。面板中Apodida仅有4条记录、4个标签；4/4不能证明覆盖整个目。覆盖模型允许每条引物≤2个错配，同时要求3′末端3个碱基完全匹配。非目标数为5,600条背景参考记录中的accession并集，不是物种数或实验读数比例。

原v4覆盖87.46%，WC≤3 / GT≤2背景命中为3,248 / 3,401。第一轮优化版分别PCR覆盖90.50%；补充后达到92.51%，非目标并集未增加。更宽松的WC≤4下仍存在明显风险。

## 使用序列

- **[最新完整独立PCR配对表](results/final_separate_pairs.csv)**：已合并原4对和追加引物，无需手工拼表。
- [FASTA序列](results/final_separate_primers.fasta)：均为5′→3′基因特异序列，不含接头和索引。
- [Apodida追加配对](results/apodida_additional_pairs.csv)、[最新结果](results/apodida_comparison.csv)。
- [第一轮序列](results/round1_primers.csv)、[配对与交叉组合](results/round1_pairings.csv)、[方案比较及历史基线](results/round1_comparison.csv)。

**最新配对表每行对应一个独立PCR。** 新增方案尚未评估全部混合交叉组合及全池二聚体，不可直接混成单管。第一轮Pool方案已经评估4F×4R，但其序列集合与Separate不同；不同长度系列混合也未评估。

第一轮目标预测产物范围（含引物，不含接头）：v4opt 178–218 bp、S 201–241 bp、M 285–325 bp、L 354–395 bp。补充序列长度可能变化，不能直接沿用这些范围；逐记录预测长度见`analysis/apodida/independent_hits.tsv`。

## 证据和限制

- 冻结参考库包含1,846条目标、5,600条背景，使用116条完整无模糊碱基序列构建比对骨架。
- 第一轮110个候选/基线配对经独立C++逐位置扫描复核，通过386,492项一致性检查。
- Apodida补充从17条源记录提取37对候选，保留13条方案内追加配对；使用同一穷举扫描器，但新增配对尚无第二实现的交叉核对。
- 发现与评估使用同一数据库，并非独立验证；名称与历史分类未统一，短片段及模糊碱基限制阴性判断。
- 第一轮优化方案完全匹配覆盖率仅11.66%–37.44%；允许错配后的覆盖不能证明实际扩增均一性。追加引物同样需要实验验证。

## 复现

需要Python 3.12和C++17编译器，在独立环境中运行：

```bash
python -m pip install -r requirements.txt
python revalidate.py
```

[复现说明](docs/REPRODUCIBILITY.md)列出支持范围。仓库包含冻结输入和验证代码，不重新下载NCBI数据。

## 来源与使用

历史v4来源为`MiStar.xlsx`的`Primer_Cucumber`工作表B30:C31（2024-08-23），旧决定版Fv2/Rv3A来源为B17:C18并移除接头。不公开原始私人工作簿或往来通信。参考记录见`analysis/metadata.tsv`，继承数据的指纹见`analysis/input_manifest.json`。

本次发布尚未选择软件或数据许可证；公开可见不等于已授予开源许可。参考序列保留原始数据库来源，本项目不声称拥有其原创权。
