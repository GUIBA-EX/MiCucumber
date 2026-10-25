# 分类群覆盖 / Taxonomic coverage

## 定义 / Definitions

旧`coverage_pct`是“各名称标签内部单倍型匹配率的等权平均”，已经避免序列多的物种直接主导结果，但没有衡量目间覆盖广度。新结果将三类指标分开，不再互称覆盖率。

The legacy `coverage_pct` is the equally weighted mean of within-label haplotype matching. It reduces dominance by heavily sequenced labels but does not measure breadth across orders. The following metrics remain distinct.

1. **分类群检出率 / Taxon detection coverage**：同一名称标签至少有一条参考序列满足整对引物匹配，就记为检出；分母为范围内全部标签。两端必须命中同一参考，A/B先按参考取并集，再合并标签。每个标签计一次。
2. **目间均衡覆盖率 / Order-balanced coverage**：先在每个目内计算分类群检出率，再对有参考数据的各目等权平均。零命中的目也进入分母。一个参考丰富的目不能抵消另一个目的整组漏检。
3. **种内稳健性 / Within-label robustness**：逐标签保留全覆盖、部分覆盖、未覆盖状态，以及内部参考匹配率。至少一条命中并不意味着种内变异已全部覆盖。

Taxon coverage counts each frozen name label once if any reference has a paired hit. Order-balanced coverage is the arithmetic mean of these percentages across represented orders, including zero-hit orders. Within-label matching remains a separate robustness measure; one detected reference does not establish coverage of all intraspecific variation.

完全匹配采用相同分层定义，但要求同一参考上的F/R均零错配；普通覆盖仍为每条≤2错配且末端3 nt IUPAC兼容。/ Exact taxonomic coverage uses the same hierarchy but requires zero mismatches for both primers on the same reference. Standard coverage permits ≤2 mismatches per primer with compatible terminal 3 nt.

## 范围 / Scope

主表包含Apodida，完整分母为151个名称标签；另提供非Apodida的145标签结果，便于与既往分析对照。标签沿用冻结面板，其中包含未定种或待核实的名称，不能全部当作已验证物种。目标签包括旧分类Aspidochirotida；当前数据不能证明现生七目都已充分采样。属、科的均衡指标需补充核实分类表后计算，不从名称字符串臆测科目关系。

The full panel contains 151 name labels including Apodida; a secondary non-Apodida scope contains 145. Labels include uncertain identifications and are not all validated species. Frozen order names include the legacy Aspidochirotida, and do not establish sampling of all seven extant orders. Genus/family-balanced measures require a verified taxonomy map.

## 当前方案重新统计 / Current assays re-scored

| Scheme | Detected labels | Taxon coverage | Order-balanced coverage | Exact taxon coverage | Fully covered labels | Partially covered labels |
|---|---:|---:|---:|---:|---:|---:|
| XS | 131/151 | 86.75% | 75.52% | 13.25% | 122 | 9 |
| SD | 133/151 | 88.08% | 66.03% | 12.58% | 129 | 4 |
| S | 99/151 | 65.56% | 39.28% | 3.31% | 93 | 6 |
| SA+SB | 109/151 | 72.19% | 41.86% | 5.96% | 101 | 8 |
| MD | 124/151 | 82.12% | 73.18% | 25.83% | 117 | 7 |
| M | 49/151 | 32.45% | 30.07% | 5.30% | 48 | 1 |
| MA+MB | 55/151 | 36.42% | 31.37% | 10.60% | 50 | 5 |
| LD | 111/151 | 73.51% | 61.63% | 7.28% | 106 | 5 |
| L | 60/151 | 39.74% | 13.04% | 8.61% | 58 | 2 |
| LA+LB | 63/151 | 41.72% | 13.70% | 15.89% | 62 | 1 |
| XLD | 37/151 | 24.50% | 35.95% | 0.66% | 35 | 2 |
| XL | 24/151 | 15.89% | 26.58% | 0.66% | 22 | 2 |
| XLA+XLB | 36/151 | 23.84% | 30.82% | 0.66% | 33 | 3 |
| S-original | 131/151 | 86.75% | 69.57% | 74.83% | 127 | 4 |

## 各目检出情况 / Detection by frozen order

| Scheme | Apodida | Aspidochirotida | Dendrochirotida | Elasipodida | Molpadida |
|---|---:|---:|---:|---:|---:|
| XS | 0/6 | 80/92 | 31/32 | 15/16 | 5/5 |
| SD | 0/6 | 91/92 | 32/32 | 5/16 | 5/5 |
| MD | 0/6 | 75/92 | 29/32 | 15/16 | 5/5 |
| LD | 0/6 | 69/92 | 27/32 | 11/16 | 4/5 |
| XLD | 0/6 | 13/92 | 17/32 | 2/16 | 5/5 |

更新前冻结SD的平均种内匹配率为80.92%（排除Apodida），但Elasipodida为0/16。因此提高旧指标不必然补上分类群缺口。采用目间均衡指标时，应优先奖励新增目内标签及补齐整目漏检，而不是只改善参考丰富类群的单倍型匹配。

The preceding frozen SD had a non-Apodida mean within-label match of 80.92%, but detects 0/16 Elasipodida labels. Increasing that older score need not fill a taxonomic gap. An order-balanced objective should prioritize recovered labels in poorly covered orders and whole-order gaps, rather than only improved haplotype matching in well-sampled groups.

至少一条参考命中的定义也有局限：标签参考越少，越难评估种内稳健性；各目等权可能让样本很少的目影响较大。应始终同时展示每目分母和全/部分覆盖状态。这些是当前库内的计算检出指标，不是实验扩增概率。

Any-reference detection has limits: sparsely sampled labels provide little evidence on within-label robustness, while order balancing gives sparsely sampled orders substantial influence. Always show order denominators and full/partial label states. These are reference-library detection metrics, not experimental amplification probabilities.

## 复现与兼容 / Reproduction and compatibility

```bash
python scripts/taxon_coverage.py
```

脚本直接从已独立复核的原始序列配对命中结果重算，且检查平均种内匹配率能复现旧指标。引物序列不变；原比较CSV的旧字段保留供既往复现，新增结果使用明确字段名，避免改变同一字段的意义。

The script aggregates independently verified raw-sequence paired hits and confirms that within-label means reproduce the legacy metrics. Primer sequences are unchanged. Legacy CSV fields remain for reproducibility; new tables use explicit metric names rather than changing the meaning of existing fields.

[Comparison, both scopes](../results/current/taxonomic_comparison.csv) · [Per order](../results/taxonomic_coverage/by_order.csv) · [Per taxon](../results/taxonomic_coverage/by_taxon.csv) · [Uncovered labels](../results/taxonomic_coverage/uncovered_taxa.csv) · [Machine-readable definitions](../results/taxonomic_coverage/definitions.json)
