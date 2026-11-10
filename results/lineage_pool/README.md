# 16S-LD 谱系补充引物 / Lineage supplements

**LD-Elasipodida** 在原 LD 的 F 和 R 上加入 F-Elasipodida，适合作为新版 S 的独立补充扩增。**LD-Synallactida** 加入 F-Synallactida。**LD-Synallactida-Elasipodida** 同时使用两条补充 F。补充引物按各自新增覆盖物种数最多的目命名。序列按 5′→3′ 书写，坐标相对于 AB525437.1 的 16S 基因。

**LD-Elasipodida** adds F-Elasipodida to the original LD F and R for a separate assay alongside the updated S pool. **LD-Synallactida** adds F-Synallactida. **LD-Synallactida-Elasipodida** includes both supplemental F oligos. Each supplemental oligo is named after the order in which it adds the most covered species. Sequences are 5′→3′, with coordinates relative to the 16S gene of AB525437.1.

| 引物 / Oligo | 序列 / Sequence | 位点 / Coordinates | 用途 / Role |
|---|---|---:|---|
| F | `AGACTTGTATGAAYGGCRAAACMT` | 868–891 | 原 LD / Original LD |
| F-Synallactida | `GGACCTGTATGAATGGCTTTTCAT` | 868–891 | 主要补 Synallactida / Mainly adds Synallactida |
| F-Elasipodida | `AAACTAGTATGAATGGCTTTTCAT` | 868–891 | 补 Elasipodida / Adds Elasipodida |
| R | `CGCTGTTATCCCTGCRGT` | 1152–1169 | 共用 R / Shared R |

[LD-Elasipodida FASTA](ld_elasipodida.fasta) · [全部四条 L 寡核苷酸 / All four L oligos](ld_pool.fasta) · [各方案组分 / Pool composition](oligos.csv)

| 方案 / Pool | 覆盖 / Covered | 完全匹配 / Exact | Synallactida | Elasipodida |
|---|---:|---:|---:|---:|
| LD | 82/174 | 29/174 | 3/26 | 0/22 |
| LD-Elasipodida | 97/174 | 29/174 | 3/26 | 15/22 |
| LD-Synallactida | 104/174 | 36/174 | 20/26 | 0/22 |
| LD-Synallactida-Elasipodida | 119/174 | 36/174 | 20/26 | 15/22 |

与 SD-Dendrochirotida 分开扩增时，LD-Elasipodida 的预测覆盖并集为 165/174。此时再加入 F-Synallactida 可将并集中的完全匹配数从 30 提到 37。五窗口共同面板上，两个 S＋L 方案均覆盖 142/151 种。

Separate LD-Elasipodida and SD-Dendrochirotida assays jointly cover 165/174 species. Including F-Synallactida in the L assay raises the exact-match union from 30 to 37 species. Both S + L options cover 142/151 on the five-window common panel.

以至少一条 F 与共用 R 组成有效预测产物计覆盖。三个补充方案在 5,600 条背景参考的五档规则下均无新增命中。两档严格规则、WC3 和 GT2 均为 0，最宽松的 WC4 命中 1,015 条记录。实际混合 PCR 的引物竞争和比例需另行确定。

Coverage is the union of predicted products formed by any F with the shared R. The three supplemental pools added zero background accessions under all five rules across 5,600 records. Both strict models, WC3 and GT2 returned zero hits. WC4, the most permissive screen, returned 1,015 hits. Primer competition and proportions in mixed PCR require separate assessment.

[逐物种结果 / Species results](ld_by_species.csv) · [分目结果 / By order](by_order.csv) · [五个窗口筛查 / Screening across five windows](screening.csv) · [对比结果 / Comparison](comparison.csv) · [温度与二级结构 / Thermodynamics](thermal.csv) · [独立复核 / Independent verification](verification.json)

[其他 16S 长度的候选筛查 / Screening of other 16S windows](../lineage_exploration/README.md)

## 筛选与复现 / Selection and reproduction

固定同源坐标和原有引物，从冻结比对中枚举观测到的普通补充序列。XS、SD 检查补 R，MD、LD、XLD 检查补 F。先要求项目原有的末端约束，并要求原始序列扫描的新增覆盖能在指定结合位点复现、五档背景 accession 集合均不扩大。然后枚举两条或三条引物的组合，优先最大化覆盖数，其次最大化完全匹配数。LD-Elasipodida 使用三条 F 方案中的 Elasipodida 补充引物，并单独复核。XS、SD、MD 在此搜索范围内没有补充序列同时通过全部约束，XLD 的最佳增益为 2 个覆盖物种。

The search enumerated observed nondegenerate additions in the frozen alignment while retaining the original pair and its reference coordinates. It tested added R oligos for XS and SD, and added F oligos for MD, LD and XLD. Candidates had to satisfy the terminal constraints, reproduce each new hit at the intended site and add zero accessions in all five background models. All two- and three-oligo combinations were ranked by coverage and then exact matches. LD-Elasipodida uses the Elasipodida supplement from the three-F pool and was checked separately. XS, SD and MD yielded no passing additions under all the constraints of this search. XLD gained two species.

热力学评估采用现有 Primer3 条件，检查所有具体变体的发卡、同二聚体及 F–R 和同向引物间的异二聚体。分别模拟每个变体 50 nM 和每方向总量 200 nM。后一种情况先在同方向的寡核苷酸间等分，再在每条的具体变体间等分。每条 F 与共用 R 的双链 Tm 区间中点差须 ≤5 °C，结构 Tm 须 <55 °C。LD-Synallactida、LD-Elasipodida 和三条 F 方案的最大中点差分别为 1.56、3.86 和 4.35 °C，最高结构 Tm 均为 45.74 °C。

Thermodynamic screening used the project's Primer3 conditions, including hairpins, homodimers and all heterodimers across and within primer directions. It evaluated 50 nM per variant and 200 nM total per direction. The latter was split equally by oligo formulation and then by variant. Each F-to-R duplex Tm midpoint difference had to be ≤5 °C, with structure Tm <55 °C. The maximum midpoint differences for LD-Synallactida, LD-Elasipodida and the three-F pool were 1.56, 3.86 and 4.35 °C, respectively. All three had a maximum structure Tm of 45.74 °C.

使用穷举扫描和独立种子匹配逐 accession 比较 LD 四个方案，在 174 个目标物种和 5,600 条背景记录上均无分歧。

Exhaustive and independent seed-based scans agreed on every accession for all four LD schemes across 174 target species and 5,600 background records.

从仓库根目录运行 / Run from the repository root:

```sh
python -m pip install primer3-py==2.4.0 biopython==1.88
python results/lineage_pool/design.py --output /tmp/micucumber-lineage
python results/lineage_pool/verify.py --output /tmp/micucumber-lineage
```

扫描程序需要 C++17 编译器。/ The exhaustive scan requires a C++17 compiler.
