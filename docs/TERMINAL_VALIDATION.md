# Terminal correction / 末端修正

## Material Passport

Verification status: VERIFIED for frozen computational data; wet-lab validation pending. / 冻结数据计算复核通过，实验验证待完成。

Scope: bounded primer search, independent product scans, terminal rules and coordinate verification. No population-wide sensitivity/specificity or hypothesis-test claim is made from this reused design panel. / 范围为有限候选搜索、独立产物扫描、末端规则及坐标复核，不从重复使用的设计面板推断总体灵敏度、特异性或假设检验结果。

3′-terminal degeneracy is permitted; actual variants must satisfy the same MiUrchin terminal constraints. / 允许3′末端简并，实际变体须符合与MiUrchin一致的末端约束。

| Portfolio | Previous coverage / exact | Current coverage / exact |
|---|---:|---:|
| SD | 87.45% / 27.48% | 79.76% / 3.28% |
| S | 56.78% / 0.34% | 67.98% / 2.93% |
| SA+SB | 71.96% / 0.34% | 74.71% / 7.07% |
| MD | 56.90% / 9.43% | 47.42% / 6.44% |
| M | 14.05% / 0.00% | 33.56% / 5.52% |
| MA+MB | 23.70% / 3.91% | 57.64% / 8.79% |
| LD | 70.26% / 33.63% | 65.40% / 6.55% |
| L | 35.24% / 3.97% | 41.03% / 7.87% |
| LA+LB | 46.68% / 8.00% | 55.14% / 16.01% |
| XLD | 48.34% / 9.71% | 24.09% / 0.69% |
| XL | 22.88% / 2.93% | 21.33% / 0.69% |
| XLA+XLB | 28.86% / 5.23% | 21.33% / 0.69% |
| S-original | 89.84% / 76.75% | 89.84% / 76.75% |

Ordinary S/M/L improve, but the strict-terminal constraints reduce several degenerate metrics. In particular SD exact matching falls from 27.48% to 3.28%; XL two-pair coverage and exact matching are unchanged from its new single pair. This is not a uniform upgrade. / 普通S/M/L改善，但多项简并指标下降；SD完全匹配从27.48%降至3.28%，XL两对不优于本轮单对，因此不称为全面升级。

All 32 selected oligos pass across concrete variants. S-original is unchanged and exempt. Target-state checks: 11,200 with zero differences; background-set checks: 32 with zero differences. LC704718.1 is missing from the alignment only and remains in full-sequence reporting. / 32条入选引物的实际变体全部通过规则，原始对照保持不变且豁免筛选。目标状态11,200项、背景集合32项，均无差异。LC704718.1仅缺位置比对，完整序列结果仍保留。

WC≤4 counts remain substantial (e.g. LD 1,157, XLD 1,357); WC≤3/GT≤2 acceptance does not establish experimental specificity. / WC≤4仍有明显命中（如LD 1,157、XLD 1,357）；通过WC≤3/GT≤2不能证明实验特异性。

[Terminal audit](../results/terminal_optimization/terminal_audit.csv) · [Thermodynamics](../results/terminal_optimization/thermal.csv) · [Verification](../results/terminal_optimization/verification.json) · [Missed references](../results/terminal_optimization/missed_references.csv) · [Coordinates](../results/current/binding_positions.csv)

Fresh-directory bundle check: selected sequences, terminal audit and reference-coordinate table reproduced exactly. / 新目录解包复现：所选序列、末端审计和参考坐标表均完全一致。
