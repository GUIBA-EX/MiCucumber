# Joint-locus validation / 共同位点复核

Ordinary, A, B and D share identical F/R start/end coordinates within each region. / 每个长度组内普通、A、B、D的F/R起止坐标分别完全相同。

| Region | F interval | R interval | Reference span |
|---|---|---|---:|
| S | 954–977 | 1156–1179 | 226 bp |
| M | 921–942 | 1148–1165 | 245 bp |
| L | 868–891 | 1152–1169 | 302 bp |
| XL | 781–800 | 1147–1176 | 396 bp |

## Performance / 性能

Non-Apodida label-balanced metrics, using the same panel before and after. / 前后均使用同一非Apodida标签等权面板。

| Portfolio | Previous coverage / exact | Shared-locus coverage / exact |
|---|---:|---:|
| SD | 79.76% / 3.28% | 73.97% / 5.07% |
| S | 67.98% / 2.93% | 66.85% / 3.35% |
| SA+SB | 74.71% / 7.07% | 71.38% / 4.56% |
| MD | 47.42% / 6.44% | 40.37% / 6.86% |
| M | 33.56% / 5.52% | 33.56% / 5.52% |
| MA+MB | 57.64% / 8.79% | 36.36% / 10.80% |
| LD | 65.40% / 6.55% | 43.33% / 15.00% |
| L | 41.03% / 7.87% | 41.03% / 7.87% |
| LA+LB | 55.14% / 16.01% | 43.33% / 15.00% |
| XLD | 24.09% / 0.69% | 19.95% / 0.69% |
| XL | 21.33% / 0.69% | 15.81% / 0.69% |
| XLA+XLB | 21.33% / 0.69% | 15.81% / 0.69% |
| S-original | 89.84% / 76.75% | 89.84% / 76.75% |

All 11,200 target-state and 32 background-set checks agree with the independent whole-sequence scanner. All concrete variants pass terminal rules and both thermal scenarios. / 11,200项目标状态及32项背景集合复核全部一致；实际变体通过末端与双浓度热力学检查。

S-original is unchanged and exempt from joint selection. Apodida is excluded from selection but included in all-target reporting; LC704718.1 remains absent from the alignment. This reused design panel is not an independent holdout or wet-lab validation. / 原始对照保持不变，不参与联合筛选；Apodida保留在全部目标报告，LC704718.1仍缺位置比对。设计面板重复用于评估，不是独立留出测试或湿实验。

Coverage losses are retained rather than hidden by shifting sites. XL remains weak; XL A/B adds no coverage/exact benefit, and relaxed background counts remain high. / 如实保留统一坐标造成的覆盖损失；XL表现仍弱，A/B没有覆盖或完全匹配收益，宽松背景命中仍较多。

[Coordinates](../results/current/binding_positions.csv) · [Terminal audit](../results/terminal_optimization/terminal_audit.csv) · [Thermodynamics](../results/terminal_optimization/thermal.csv) · [Raw verification](../results/terminal_optimization/verification.json)

Fresh extraction of the published reproduction bundle and rerunning `choose.py` reproduces all 16 selected variants exactly. / 从发布复现包重新解压运行选择脚本，16条入选变体与发布结果完全一致。
