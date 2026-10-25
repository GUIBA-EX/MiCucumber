# Reproduction / 复现

## Current D assays / 当前D方案

Extract [the candidate reproduction bundle](../results/taxon_optimization/reproduction_sources.zip) into an empty directory, then run:

```bash
python verify.py
```

Requires Python 3.10+ and a C++17 compiler; no network or Python packages are needed. The script reproduces ten fixed candidates from original FASTA. Current SD/MD/LD/XLD correspond to SD-T10/MD-T4/LD-T7/XLD-T8 in [the selection policy](../results/current/D_selection_policy.json). / 将冻结包解压至空目录，运行上面命令；使用原始FASTA复核10个候选，正式四个D方案由选择规则映射。

[Standalone reproduction check](../results/taxon_optimization/frozen_reproduction_check.json) · [Current paired hits](../results/current/independent_hits.tsv) · [Current thermal reports](../results/current/thermal.csv).

## Taxonomic coverage / 分类群覆盖

From the repository root / 在项目根目录执行：

```bash
python scripts/taxon_coverage.py
python scripts/check_release.py
python scripts/check_ab.py
python scripts/check_taxon_optimization.py
```

Taxonomic coverage aggregates paired raw-sequence hits, includes Apodida, and balances the five frozen order groups equally. Within-label matching is reported separately. / 以原始配对命中汇总，包含Apodida，对5个冻结目标签等权；种内平均匹配率另列。

## XS

```bash
python scripts/verify_xs.py --output /tmp/MiCucumber-XS-check
```

Uses its standalone frozen inputs and independent C++/Python scans. / 使用XS的独立冻结输入与双算法扫描。

## Ordinary/A-B and baseline evidence / 普通A/B与基线证据

`results/terminal_optimization/reproduction_sources.zip` preserves the preceding selection and its verification/figure scripts. It reproduces the frozen baseline, including the preceding D sequences. Current D sequences use the new bundle above. Ordinary/A/B and S-original retain their frozen sequences and evidence; A/B are separate-PCR unions. / 该旧冻结包用于复核基线及未改变的普通/A/B与原版对照；当前D方案使用本页首个新冻结包。

[Metric definitions](TAXONOMIC_COVERAGE.md) · [Selection decisions](D_OPTIMIZATION.md).
