# Retention decisions / 保留决策

按奥卡姆剃刀原则，每个长度仅保留一个正式D方案：SD采用低简并增强（2/8），MD采用严格背景档（64/4），LD采用覆盖增强（32/1），XLD保留原方案（2/1）。SD更激进档、MD 128/4档和XLD小增益档不进入正式序列。普通、A、B及S-original不变，每组四套F/R起止坐标完全相同。这是基于收益与复杂度的人工取舍，不是预设统计阈值或已验证PCR最优条件。

Following Occam’s razor, retain one D portfolio per length: SD with modest degeneracy (2/8), MD under the strict background gate (64/4), LD for its coverage gain (32/1), and unchanged XLD (2/1). More aggressive SD, MD 128/4 and marginal-gain XLD variants remain comparisons. Ordinary, A, B and S-original are unchanged; all four variants in each length share identical F/R start/end coordinates. This is an explicit benefit–complexity judgment, not a preregistered threshold or experimentally established PCR optimum.

| Scheme | Coverage before → after | Exact before → after | WC≤3 | GT≤2 | WC≤4 |
|---|---|---|---:|---:|---:|
| SD | 73.97 → 80.92% | 5.07 → 9.04% | 26 | 3 | 455 |
| MD | 40.37 → 67.17% | 6.86 → 25.48% | 2 | 4 | 76 |
| LD | 43.33 → 66.78% | 15.00 → 19.14% | 20 | 16 | 1168 |
| XLD | 19.95 → 19.95% | 0.69 → 0.69% | 1 | 1 | 1309 |

Independent full scans: 11,200 target-state checks and 32 background-set checks, zero disagreements. / 独立全窗口复核全部一致。
