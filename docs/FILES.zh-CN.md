# 文件索引

[English](FILES.md) · [概览](../README.zh-CN.md) · [命名](NAMING.zh-CN.md) · [方法](METHODS.zh-CN.md) · [复现](REPRODUCIBILITY.zh-CN.md)

从`sequences/`获取引物，使用`results/`比较表现，按复现说明重新计算。

| 路径 | 内容 |
|---|---|
| [sequences/primer_pairs.csv](../sequences/primer_pairs.csv) | 13套方案的17条配对反应记录 |
| [sequences/primers.fasta](../sequences/primers.fasta) | 34条正反向序列记录 |
| [sequences/](../sequences/) | 各长度CSV与FASTA，以及S-original |
| [results/comparison.csv](../results/comparison.csv) | 13套方案×共同及区域面板，共26行 |
| [results/degenerate/](../results/degenerate/) | 简并单对筛选、漏检类群、背景命中与热力学结果 |
| [results/nondegenerate/](../results/nondegenerate/) | 普通引物候选、筛选记录、匹配与验证结果 |
| [results/matching/](../results/matching/) | 21组匹配概况及7,371条逐参考状态 |
| [results/reproduction_checks.json](../results/reproduction_checks.json) | 计算复现检查结果 |
| [figures/](../figures/) | 顶部示意图、匹配热图、区域图及坐标 |
| [report.html](../report.html) | 双语报告，下载后在本地打开 |
| [scripts/check_release.py](../scripts/check_release.py) | 检查导出序列、指标、链接与指纹 |
| [scripts/reproduce.py](../scripts/reproduce.py) | 运行冻结分析流程 |
| [scripts/plot_matching.py](../scripts/plot_matching.py) | 生成匹配汇总与热图 |
| [scripts/plot_regions.py](../scripts/plot_regions.py) | 生成参考区域图 |
| [reproducibility/frozen/](../reproducibility/frozen/) | 参考数据及分析输入包 |
| [docs/name_mapping.csv](../docs/name_mapping.csv) | 序列溯源及标识映射 |
| [archive/](../archive/) | 分析快照归档 |
| [SHA256SUMS.json](../SHA256SUMS.json) | 发布文件的SHA-256指纹 |
| [COPYRIGHT.md](../COPYRIGHT.md) | 著作权及使用条款 |
