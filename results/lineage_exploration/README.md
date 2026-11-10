# MiCucumber 16S 补充候选 / Additional 16S candidates

| 窗口 / Window | 方案 / Design | 预测覆盖 / Covered | 双端完全匹配 / Exact | 新增背景 / New background records |
|---|---|---:|---:|---|
| XS | 补 F 或 R，同坐标或小幅移动 / Additional F or R at the current or nearby sites | — | — | 本轮候选无一通过两档严格背景约束 / None met both strict background constraints |
| S | SD-Dendrochirotida，加同坐标 R / Add R at the original site | 130→155 / 174 | 0→1 / 174 | 严格两档均为 +0，GT2 +1，WC4 +20 / Strict +0 in both, GT2 +1, WC4 +20 |
| M | MD-Holothuriida，补同坐标 F，共用 R 的 5′ 端缩短 1 nt / Add F and shorten the shared R at its 5′ end by 1 nt | 89→106 / 174 | 24→32 / 174 | 五档均为 +0 / +0 in all five |
| XL | 前轮 XLD-Dendrochirotida / Previous XLD-Dendrochirotida candidate | 43→45 / 152 | 3→4 / 152 | 五档均为 +0 / +0 in all five |

本轮 XL 搜索没有找到增益更高且通过两档严格背景约束的补充引物。XS 和 XL 的部分移动候选提高了覆盖，但同时新增大量严格背景命中。S 收录为补充方案，M 列为备选。M 的两档严格背景总数为 0 和 15，S 为 0 和 5。

The new XL search yielded no higher-gain supplement that passed both strict background constraints. Some nearby XS and XL sites improved target coverage and added many strict background hits. S is included as a supplemental pool and M is listed as an alternative candidate. The two strict background totals are 0 and 15 for M, and 0 and 5 for S.

[SD-Dendrochirotida FASTA](sd_pool.fasta)

## 寡核苷酸 / Oligos

坐标相对于 AB525437.1 的 16S 基因，序列按 5′→3′ 书写。/ Coordinates are relative to the AB525437.1 16S gene. Sequences are 5′→3′.

| 方案 / Pool | 组分 / Oligo | 序列 / Sequence | 位点 / Site |
|---|---|---|---:|
| SD-Dendrochirotida | 原 F / Original F | `TAAGAAAGACGARAAGACCCTRTC` | 954–977 |
| SD-Dendrochirotida | 原 R / Original R | `GAGAAGATGACGCTGTTATCCCTR` | 1156–1179 |
| SD-Dendrochirotida | R-Dendrochirotida | `AAGGAGATTACGCTGTTATCCCTG` | 1156–1179 |
| MD-Holothuriida | 原 F / Original F | `AAACTTCTATTHAYGTGAAGAA` | 921–942 |
| MD-Holothuriida | F-Holothuriida | `AAATTTCCTCCTGTGTGAAGAA` | 921–942 |
| MD-Holothuriida | 缩短的共用 R / Shortened shared R | `TTATCCCTGCGGTAACT` | 1148–1164 |

S 的 25 个新增物种包括 Dendrochirotida 14 种和 Holothuriida 11 种。M 的 17 个新增物种均属 Holothuriida，原有覆盖全部保留。

Of the 25 species added by S, 14 are Dendrochirotida and 11 are Holothuriida. All 17 gains in M are Holothuriida. The M pool retains every species covered by the original MD pair.

M 若要求原 R 坐标，仍可用 `GTTATCCCTGCGGTAACT`（1148–1165）作共用 R。保留原 R 时，原 F 与补充 F 在 200 nM 总量下按 90:10 分配，最大 Tm 中点差约 4.995 °C。缩短 R 后，两条 F 等量模型通过两个浓度场景，最大差为 4.30 °C，最高结构 Tm 为 39.42 °C。两版 M 的覆盖与完全匹配物种名单一致。上述浓度比例用于热力学建模。

The original shared R, `GTTATCCCTGCGGTAACT` (1148–1165), is an option when retaining the original coordinates. Its 90:10 original-to-supplemental F model at 200 nM total gives a maximum Tm midpoint difference of about 4.995 °C. Shortening R allows equal allocation of the two F oligos and passes both concentration scenarios. The maximum midpoint difference is 4.30 °C and maximum structure Tm is 39.42 °C. Both M pools have the same covered and exactly matched species. The concentration ratios are modeling inputs.

## 筛查与复核 / Screening and verification

使用各窗口原有的一物种一参考面板及 5,600 条冻结背景参考。双端覆盖采用每端最多两个错配且 3′ 末三位兼容的规则。两档严格背景分别使用仅沃森–克里克配对或另允许鸟嘌呤–胸腺嘧啶配对，并要求末三位兼容。WC3、GT2、WC4 放宽末端限制，允许的每端错配数分别为 3、2、4。表中背景增量为相对原配对新增的 accession。

分别固定 F 或 R。补充端搜索实测模板序列及基于模板两两合并的低简并序列，简并限于 3′ 半段，每条最多 8 个变体。候选的两端坐标分别在原位置 ±5 nt 范围内，寡核苷酸长度最多变化 3 nt。每个方向和位置类别（同坐标或移动）按预期新增覆盖排序，在通过热力学后最多选 30 条作穷举扫描。共扫描 221 条补充候选。M 的共用 R 缩短是后续单独检查。表中的 S 和两个 M 版本都用独立种子扫描复核了逐 accession 的覆盖、完全匹配和五档背景结果。

Each window uses its existing one-reference-per-species panel and the same 5,600 frozen background records. Predicted coverage allows at most two mismatches per end with the terminal three 3′ bases compatible. The strict background models use Watson–Crick pairing or additionally allow guanine–thymine pairing. WC3, GT2 and WC4 relax the terminal constraint and allow three, two and four mismatches per end, respectively. Background changes count accessions newly hit relative to the original pair.

The search fixed F or R and generated additions from observed templates and pairwise IUPAC combinations with ambiguity confined to the 3′ half and at most eight variants. Each endpoint could move by up to five nucleotides, with a length difference of at most three. Up to 30 thermally eligible additions per direction and position class were shortlisted by predicted gain for exhaustive scans. The scan assessed 221 additions. M shared-R shortening was a separate follow-up. Independent seed scans agreed accession by accession for S and both M variants.

[全部候选 / All scanned candidates](scanned_candidates.csv) · [候选摘要 / Shortlist](shortlist.csv) · [候选组分和匹配名单 / Shortlist data](shortlist.json) · [S 与原坐标 M 的复核 / Verification](verification.json) · [M 浓度敏感性 / M ratio sensitivity](md_ratio_sensitivity.csv) · [M 共用 R 缩短评估 / M shared-R shortening](md_balanced_pool.json)

```sh
python -m pip install primer3-py==2.4.0 biopython==1.88
python results/lineage_exploration/search.py --output /tmp/micucumber-exploration
python results/lineage_exploration/verify_shortlist.py --output /tmp/micucumber-exploration
python results/lineage_exploration/md_balance.py --output /tmp/micucumber-exploration
```

从仓库根目录运行。需要 C++17 编译器。/ Run from the repository root with a C++17 compiler.
