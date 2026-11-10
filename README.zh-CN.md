![MiCucumber](figures/MiCucumber_overview.png)

# MiCucumber: in silico design and evaluation of mitochondrial primers for sea cucumber (Holothuroidea) eDNA metabarcoding

**Fei Xia**

[English](README.md) · [简体中文](README.zh-CN.md)

<!-- publication:start -->
**预印本 v1.7 · 2026 年 11 月 11 日**

[PDF](publications/MiCucumber_preprint.pdf) · [论文 Markdown](publications/MiCucumber_preprint.md) · [固定版本](https://github.com/GUIBA-EX/MiCucumber/releases/tag/preprint-v1.7) · [CITATION.cff](CITATION.cff) · [BibTeX](CITATION.bib) · [构建与更新](publications/README.md)
<!-- publication:end -->

MiCucumber 提供 29 对海参环境 DNA 宏条形码候选引物，靶向线粒体 16S、12S 和 COI 三个标记，并提供两套 16S 谱系补充方案。

[基础引物集（FASTA）](sequences/all_markers.fasta) · [16S 引物表（CSV）](sequences/primer_pairs.csv) · [12S 与 COI 引物表（CSV）](markers/12S_COI/candidates.csv)

## 引物怎么选

| 用途 | 方案 | 参考跨度 | 覆盖 | 完全匹配 |
|---|---|---:|---:|---:|
| 优先扩大 16S 覆盖 | 16S SD-Dendrochirotida | 226 bp | 138/151 | 1/151 |
| 优先考虑单对 16S 引物的完全匹配 | 16S LD | 302 bp | 73/151 | 23/151 |
| 覆盖物种数最多的 12S 方案 | 12S XLD | 354 bp | 33/53 | 7/53 |
| 最短 COI 窗口 | COI XSD | 145 bp | 43/57 | 3/57 |
| 覆盖物种数最多的 COI 方案 | COI LD | 293 bp | 103/283 | 11/283 |

16S 两项使用同一组 151 个物种。12S 和 COI 以各窗口可评价的物种数为分母。预测覆盖允许每条引物最多两个错配，并要求 3′ 末端三个碱基兼容。双端完全匹配要求两条引物均无错配。

## 16S 谱系补充

补充引物沿用原结合坐标。下表使用同一组 174 种海参参考。

| 方案 | 增加的引物 | 预测覆盖 | 双端完全匹配 | 严格背景新增¹ |
|---|---|---:|---:|---:|
| SD-Dendrochirotida | R-Dendrochirotida | 130 → 155 | 0 → 1 | 0 / 0 |
| LD-Elasipodida | F-Elasipodida | 82 → 97 | 29 → 29 | 0 / 0 |
| LD-Synallactida | F-Synallactida | 82 → 104 | 29 → 36 | 0 / 0 |
| LD-Synallactida-Elasipodida | 两条补充 F | 82 → 119 | 29 → 36 | 0 / 0 |

¹ 仅沃森–克里克配对 / 另允许鸟嘌呤–胸腺嘧啶配对。SD-Dendrochirotida 在宽松 GT2 和 WC4 下分别新增 1 条和 20 条背景记录。L 补充方案的五档背景命中名单均与 LD 一致。S 补充方案与 LD-Elasipodida 分开使用时，预测覆盖并集为 165/174 种。再给 L 加入 F-Synallactida，完全匹配由 30 种增至 37 种，覆盖物种名单相同。

[分目覆盖、完全匹配和物种分辨率](results/lineage_evaluation/by_order.csv) · [新增物种](results/lineage_evaluation/lineage_gain_species.csv) · [背景命中](results/lineage_evaluation/background_hits.csv) · [方法与复核](results/lineage_evaluation/README.md)

[S 补充组合 FASTA](results/lineage_exploration/sd_pool.fasta) · [L 补充组合 FASTA](results/lineage_pool/ld_elasipodida.fasta)

<details>
<summary>S 和 L 补充位点的逐碱基匹配图</summary>

![S 原反向引物与补充反向引物的碱基匹配](figures/base_matching_SD-Dendrochirotida.svg)

![L 原正向引物与补充正向引物的碱基匹配](figures/base_matching_LD-Elasipodida.svg)

</details>

Licuanan 和 Matias 曾提出棘皮动物 12S 和 16S 短片段候选标记。 [参考文献](https://doi.org/10.56899/151.03.14)

## 跨标记互补与有限错配

两套 16S 补充方案均漏检的 9 种海参中，现有 12S XLD 与 SD 合计预测补回 5 种。COI XS/XSD 也覆盖其中 1 种。有限放宽 3′ 端附近错配后，LD-Elasipodida 和 COI XSD 各新增 1 个其他目标物种，四个重点方案的背景命中数均无新增。 [逐物种结果、错配规则和同 accession 条形码比较](results/marker_complementarity/README.md)

## 外部参考复核

在各有 28 个可评价物种的外部 16S 参考中，SD-Dendrochirotida 覆盖 23 种（82.1%），完全匹配 0 种。LD-Elasipodida 覆盖 16 种（57.1%），完全匹配 2 种。COI LD 覆盖 13/15 种，完全匹配 1 种。12S 没有通过筛选的外部海参参考，COI 只有 L/LD 的结合区有可评价参考。有限错配规则为 16S M、16S MD 和 COI L 各新增 1 个覆盖物种。两套沃森–克里克规则在 16S、12S、COI 的 142、143、127 条背景参考中均未命中。 [外部面板、全部引物结果及另允许鸟嘌呤–胸腺嘧啶配对的背景结果](results/external_panel/README.md)

## 引物序列与结合位置

序列按 5′→3′ 书写。同一窗口的普通与 D 引物共享坐标，16S XS 单列一对。展开后的表格使用各窗口的可评价物种作为分母。严格背景命中依次为 **仅沃森–克里克配对 / 另允许鸟嘌呤–胸腺嘧啶配对**。

<details>
<summary>16S · 序列、预测匹配和结合位置</summary>

背景面板 · 5,600条参考记录

| 方案 | F（5′–3′） | R（5′–3′） | 跨度（bp） | 覆盖 | 完全匹配 | 严格非目标 | 碱基图 |
|---|---|---|---:|---:|---:|---:|---|
| XS | `AACTTTGGTTGGGGYAAC` | `TTTCCCCAATCCAACATCGA` | 191 | 75/166 | 0/166 | 0 / 0 | [查看](results/current_primers/XS/base_matching_XS.svg) |
| S | `CCAGAAAGACGAGAAGACCCTGTC` | `GAGGAGATAACGCTGTTATCCCTG` | 226 | 110/174 | 5/174 | 1 / 3 | [查看](results/current_primers/S/base_matching_S.svg) |
| SD | `TAAGAAAGACGARAAGACCCTRTC` | `GAGAAGATGACGCTGTTATCCCTR` | 226 | 130/174 | 0/174 | 0 / 5 | [查看](results/current_primers/S/base_matching_SD.svg) |
| M | `AAACTTCTATTAACGTGAAGAA` | `GTTATCCCTGCGGTAACT` | 245 | 55/174 | 9/174 | 0 / 2 | [查看](results/current_primers/M/base_matching_M.svg) |
| MD | `AAACTTCTATTHAYGTGAAGAA` | `GTTATCCCTGCGGTAACT` | 245 | 89/174 | 24/174 | 0 / 15 | [查看](results/current_primers/M/base_matching_MD.svg) |
| L | `AGACTCGTATGAACGGCAAAACCT` | `CGCTGTTATCCCTGCGGT` | 302 | 65/174 | 13/174 | 0 / 0 | [查看](results/current_primers/L/base_matching_L.svg) |
| LD | `AGACTTGTATGAAYGGCRAAACMT` | `CGCTGTTATCCCTGCRGT` | 302 | 82/174 | 29/174 | 0 / 0 | [查看](results/current_primers/L/base_matching_LD.svg) |
| XL | `GGTCACGCCTGCCCAGTGGA` | `AAGATAACGCTGTTATCCCTGCGGTAACTT` | 396 | 23/152 | 1/152 | 0 / 0 | [查看](results/current_primers/XL/base_matching_XL.svg) |
| XLD | `GGTAACGCCTGCCCARTGGA` | `GAGATTACGCTGTTATCCCTGCGGTAACTD` | 396 | 43/152 | 3/152 | 0 / 10 | [查看](results/current_primers/XL/base_matching_XLD.svg) |

![16S](figures/amplicon_regions.zh.svg)

</details>

<details>
<summary>12S · 序列、预测匹配和结合位置</summary>

背景面板 · 438条参考记录

| 方案 | F（5′–3′） | R（5′–3′） | 跨度（bp） | 覆盖 | 完全匹配 | 严格非目标 | 碱基图 |
|---|---|---|---:|---:|---:|---:|---|
| XS | `AGATACCCTACTATACCCTTC` | `CGACGATGGTATACAAACTG` | 176 | 15/74 | 0/74 | 0 / 0 | [查看](markers/12S_COI/figures/12S_XS.svg) |
| XSD | `AGATACCCTACTATACYYTTC` | `CGACGATGGTATACWRRCTG` | 176 | 21/74 | 9/74 | 0 / 0 | [查看](markers/12S_COI/figures/12S_XSD.svg) |
| S | `AACACCAGAGCAGTACAGCT` | `CTGCACCTTGATCTGACGT` | 207 | 13/88 | 2/88 | 0 / 0 | [查看](markers/12S_COI/figures/12S_S.svg) |
| SD | `AACACCAGAGYAGTACARCY` | `CTGCACCTTGATCTGRHGT` | 207 | 27/88 | 7/88 | 0 / 0 | [查看](markers/12S_COI/figures/12S_SD.svg) |
| M | `AGGAGCTTGTCATTAAATTGAT` | `TTACTATCGAATCCTCTTTCAT` | 228 | 8/90 | 0/90 | 0 / 0 | [查看](markers/12S_COI/figures/12S_M.svg) |
| MD | `AGGAGCTTGTCATYRAATYGAT` | `TTACTATCGAATCCTCTTTCWD` | 228 | 28/90 | 4/90 | 0 / 5 | [查看](markers/12S_COI/figures/12S_MD.svg) |
| L | `AACACCAGAGCAGTACGGCT` | `GCGATGTGTGCGCATTCTAGAG` | 346 | 14/83 | 1/83 | 0 / 0 | [查看](markers/12S_COI/figures/12S_L.svg) |
| LD | `AACACCAGAGYAGTACRGYT` | `GCGATGTGTGCRYATTYTAGAG` | 346 | 19/83 | 12/83 | 0 / 0 | [查看](markers/12S_COI/figures/12S_LD.svg) |
| XL | `GGTGGTTAATAACGTGCCAG` | `CGACGATGGTATACAGGCTG` | 354 | 31/53 | 5/53 | 0 / 1 | [查看](markers/12S_COI/figures/12S_XL.svg) |
| XLD | `GGTGGTTAATAACGTGCCAG` | `CGACGATGGTATACWRRCTG` | 354 | 33/53 | 7/53 | 0 / 1 | [查看](markers/12S_COI/figures/12S_XLD.svg) |

![12S](markers/12S_COI/figures/positions_12S.zh.svg)

</details>

<details>
<summary>COI · 序列、预测匹配和结合位置</summary>

背景面板 · 2,216条参考记录

| 方案 | F（5′–3′） | R（5′–3′） | 跨度（bp） | 覆盖 | 完全匹配 | 严格非目标 | 碱基图 |
|---|---|---|---:|---:|---:|---:|---|
| XS | `ACTATAGAGGAAAGCAAGAA` | `GCTGCTGTGAAGTAGGC` | 145 | 20/57 | 2/57 | 0 / 0 | [查看](markers/12S_COI/figures/COI_XS.svg) |
| XSD | `ACTATAGAGGRAAGCMAGAR` | `GCTGCTGTRAAGTADGC` | 145 | 43/57 | 3/57 | 0 / 0 | [查看](markers/12S_COI/figures/COI_XSD.svg) |
| S | `GAATGGTATACGCTATGGT` | `GTTTCTCAGACTAGCTTTG` | 193 | 10/55 | 0/55 | 0 / 0 | [查看](markers/12S_COI/figures/COI_S.svg) |
| SD | `GAATGGTATAYGCWATGRT` | `GTTTCTCAGAYTARCTTKG` | 193 | 30/55 | 0/55 | 0 / 0 | [查看](markers/12S_COI/figures/COI_SD.svg) |
| M | `CACTATAGAGGAAAGCAAGAACC` | `AACTTTGATCCTTGTAGGGT` | 218 | 9/55 | 0/55 | 0 / 0 | [查看](markers/12S_COI/figures/COI_M.svg) |
| MD | `CACTATAGAGGWAAGMAAGARCC` | `AACTTTGATCCTTGTARNGT` | 218 | 25/55 | 3/55 | 0 / 0 | [查看](markers/12S_COI/figures/COI_MD.svg) |
| L | `AAAATGCGAACCCCAGGAGTAAC` | `GGTTCTTGCTTTCCTCTGTAGTG` | 293 | 30/283 | 0/283 | 0 / 0 | [查看](markers/12S_COI/figures/COI_L.svg) |
| LD | `AAAATGCGAACYCCAGGARTWAC` | `GGTTCTTGCTTWCCTCTRTARTG` | 293 | 103/283 | 11/283 | 0 / 2 | [查看](markers/12S_COI/figures/COI_LD.svg) |
| XL | `ATGAACCTAAACCGCTGAT` | `CGTGGGCTATATTTCTTGA` | 415 | 11/62 | 0/62 | 0 / 0 | [查看](markers/12S_COI/figures/COI_XL.svg) |
| XLD | `ATGAACCTAAAMCGYTGAY` | `CGTGGGCTATRTTTCTNGA` | 415 | 37/62 | 1/62 | 0 / 2 | [查看](markers/12S_COI/figures/COI_XLD.svg) |

XS 与 XSD 去除引物后的参考内部条码为 108 bp。

![COI](markers/12S_COI/figures/positions_COI.zh.svg)

</details>

## 评价与数据

每端 0–2 个错配的分析区分了完全匹配与放宽错配后增加的覆盖。完整结果包含 15 个内部条形码相似度矩阵及预测产物长度。

[错配梯度、相似度矩阵与产物长度](results/anth28s_evaluation/README.zh-CN.md) · [16S 共同面板与属级留出结果](results/computational_evaluation/README.zh-CN.md) · [12S 与 COI 面板](markers/12S_COI/README.md) · [方法](docs/METHODS.zh-CN.md) · [复现](docs/REPRODUCIBILITY.zh-CN.md)

## 引用与著作权

Xia, F. (2026). *MiCucumber: in silico design and evaluation of mitochondrial primers for sea cucumber (Holothuroidea) eDNA metabarcoding*. Computational preprint v1.7. [GitHub Release](https://github.com/GUIBA-EX/MiCucumber/releases/tag/preprint-v1.7).

[著作权](COPYRIGHT.md)

<details>
<summary>参考文献</summary>

1. Gold, Z., Wall, A. R., Schweizer, T. M., et al. (2022). A manager’s guide to using eDNA metabarcoding in marine ecosystems. *PeerJ*, 10, e14071. https://doi.org/10.7717/peerj.14071

2. Miya, M., Sato, Y., Fukunaga, T., et al. (2015). MiFish, a set of universal PCR primers for metabarcoding environmental DNA from fishes: detection of more than 230 subtropical marine species. *Royal Society Open Science*, 2, 150088. https://doi.org/10.1098/rsos.150088

3. Hamamoto, K., Soliman, T., Poliseno, A., Fernandez-Silva, I., & Reimer, J. D. (2021). Higher genetic diversity of the common sea cucumber *Holothuria (Halodeima) atra* in marine protected areas of the central and southern Ryukyu Islands. *Frontiers in Conservation Science*, 2, 736633. https://doi.org/10.3389/fcosc.2021.736633

4. Katoh, K., & Standley, D. M. (2013). MAFFT multiple sequence alignment software version 7: improvements in performance and usability. *Molecular Biology and Evolution*, 30, 772–780. https://doi.org/10.1093/molbev/mst010

5. Untergasser, A., Cutcutache, I., Koressaar, T., et al. (2012). Primer3—new capabilities and interfaces. *Nucleic Acids Research*, 40, e115. https://doi.org/10.1093/nar/gks596

6. Riaz, T., Shehzad, W., Viari, A., et al. (2011). ecoPrimers: inference of new DNA barcode markers from whole genome sequence analysis. *Nucleic Acids Research*, 39, e145. https://doi.org/10.1093/nar/gkr732


7. Uthicke, S., Byrne, M., & Conand, C. (2010). Genetic barcoding of commercial Bêche-de-mer species (Echinodermata: Holothuroidea). *Molecular Ecology Resources*, 10(4), 634–646. https://doi.org/10.1111/j.1755-0998.2009.02826.x

8. Hoareau, T. B., & Boissin, E. (2010). Design of phylum-specific hybrid primers for DNA barcoding: addressing the need for efficient COI amplification in the Echinodermata. *Molecular Ecology Resources*, 10(6), 960–967. https://doi.org/10.1111/j.1755-0998.2010.02848.x

9. Byrne, M., Rowe, F., & Uthicke, S. (2010). Molecular taxonomy, phylogeny and evolution in the family Stichopodidae (Aspidochirotida: Holothuroidea) based on COI and 16S mitochondrial DNA. *Molecular Phylogenetics and Evolution*, 56(3), 1068–1081. https://doi.org/10.1016/j.ympev.2010.04.013

10. Wen, J., Hu, C., Zhang, L., Luo, P., Zhao, Z., Fan, S., & Su, T. (2010). The application of PCR–RFLP and FINS for species identification used in sea cucumbers (Aspidochirotida: Stichopodidae) products from the market. *Food Control*, 21(4), 403–407. https://doi.org/10.1016/j.foodcont.2009.06.014

11. Wen, J., Hu, C., Zhang, L., & Fan, S. (2011). Genetic identification of global commercial sea cucumber species on the basis of mitochondrial DNA sequences. *Food Control*, 22(1), 72–77. https://doi.org/10.1016/j.foodcont.2010.06.010

12. Xing, R.-R., Hu, R.-R., Wang, N., Zhang, J.-K., Ge, Y.-Q., & Chen, Y. (2021). Authentication of sea cucumber products using NGS-based DNA mini-barcoding. *Food Control*, 129, 108199. https://doi.org/10.1016/j.foodcont.2021.108199

</details>
