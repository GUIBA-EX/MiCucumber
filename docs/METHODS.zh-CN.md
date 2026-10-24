# MiCucumber

按奥卡姆剃刀原则，每个长度仅保留一个正式D方案：SD采用低简并增强（2/8），MD采用严格背景档（64/4），LD采用覆盖增强（32/1），XLD保留原方案（2/1）。SD更激进档、MD 128/4档和XLD小增益档不进入正式序列。普通、A、B及S-original不变，每组四套F/R起止坐标完全相同。这是基于收益与复杂度的人工取舍，不是预设统计阈值或已验证PCR最优条件。

非Apodida共同面板按名称标签等权、标签内单倍型等权。覆盖允许每条引物≤2处错配且末端3位IUPAC相容；完全匹配要求两端零错配。所有实际变体均无末端三连同碱基、末端3位至少1个GC、末端5位1–4个GC，全序列同碱基连续不超过4。

Primer3: 50 mM monovalent salt, 1.5 mM Mg, 0.6 mM dNTP; 50 nM per variant and 200 nM per direction. Hairpin/dimer Tm <55°C; F/R Tm-range midpoint difference ≤5°C. Background gates: SD ≤50, LD ≤20, others ≤5 accessions under both WC≤3 and GT≤2. S-original is an unchanged control. WC≤4 is a sensitivity analysis, not a selection gate.

原共同位点保持固定；扩展碱基采用参考支持率≥1%，测试不同简并上限，保留上述取舍。M每方向总浓度200 nM时F变体浓度3.125 nM。L的WC≤4命中1168条背景记录，代价明显。设计与评估共享参考集，尚无湿实验验证。
