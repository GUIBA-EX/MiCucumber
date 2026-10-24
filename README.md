![MiCucumber · XS / S / M / L / XL](figures/MiCucumber_overview.png)

The header illustrates seven extant sea-cucumber orders. Badges show primer-inclusive reference spans on AB525437.1: XS 191, S 226, M 245, L 302 and XL 396 bp. Actual products vary among taxa. Analyses retain frozen-panel order labels; the illustration does not establish coverage of all seven orders. [Illustration notes](figures/overview_design.md)

# MiCucumber

Computational design, matching assessment and reproducible evidence for sea-cucumber mitochondrial 16S primers. [中文](README.zh-CN.md)

## Assays and names

XS is one fixed degenerate pair named XS. S, M, L and XL each retain a D degenerate pair, an ordinary pair and complementary ordinary A/B pairs. Ordinary/A/B/D share identical F/R start/end coordinates within each region. A/B represent separate-PCR unions with unique contributions from both components. S-original remains the original control. Total: 14 portfolios, 18 paired rows and 36 FASTA records.

| Region | Degenerate | Ordinary | Ordinary A/B |
|---|---|---|---|
| XS | XS | — | — |
| S | SD | S | SA / SB |
| M | MD | M | MA / MB |
| L | LD | L | LA / LB |
| XL | XLD | XL | XLA / XLB |

## XS short-fragment assay

```text
XS-F  5′-RGYTTTGGTTGGGGCAAC-3′
XS-R  5′-TTDCCCCAATCCAACATCGA-3′
```

F/R degeneracy is 4/3; R=A/G, Y=C/T and D=A/G/T. Reference coordinates are F 1042–1059 and R 1213–1232, spanning 191 bp; predicted products are 186–203 bp. XS prioritizes shorter products and higher coverage; SD remains the comparison with fewer background hits.

On the same panel, XS coverage/exact matching are 88.85%/13.32%, versus 80.92%/9.04% for SD. With the target matching rule (≤2 mismatches per primer and compatible terminal 3 nt), XS hits 20 background records in each WC/GT model; all WC hits are crinoids. SD hits 1/3. XS has zero paired exact background hits. Without the terminal constraint, WC≤3 hits rise to 1,396 for XS versus 26 for SD. XS does not pass the original conservative S–XL background gate; it is retained as an experimental candidate under an explicit relaxation of background limits.

XS still misses Apodida. Among 107 labels amplified by both XS and SD, 93 (86.92%) and 97 (90.65%), respectively, have no observed shared internal barcode. This describes discrimination within the reference library, not experimental identification success. [XS analysis and evidence](docs/XS.md)

## Common-panel results

Main-table metrics exclude Apodida: 351 haplotypes and 151 taxonomic labels, including 145 non-Apodida labels, with equal label weights and equal within-label weights. Coverage permits ≤2 mismatches per primer with IUPAC-compatible terminal 3 nt; exact matching requires zero mismatches in both primers. All-target metrics are in the CSV. Background has 5,600 records. WC uses standard pairing; GT additionally tolerates G–T pairing. Background columns below omit the terminal constraint and count records, not amplification fractions.

| Scheme | Coverage | Exact | WC≤3 | GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
| XS | 88.85% | 13.32% | 1396 | 26 | 2609 |
| SD | 80.92% | 9.04% | 26 | 3 | 455 |
| S | 66.85% | 3.35% | 4 | 3 | 331 |
| SA+SB | 73.49% | 5.53% | 4 | 3 | 378 |
| MD | 67.17% | 25.48% | 2 | 4 | 76 |
| M | 33.56% | 5.52% | 1 | 2 | 13 |
| MA+MB | 36.36% | 10.80% | 1 | 3 | 39 |
| LD | 66.78% | 19.14% | 20 | 16 | 1168 |
| L | 41.03% | 7.87% | 0 | 0 | 46 |
| LA+LB | 43.33% | 15.00% | 0 | 0 | 46 |
| XLD | 19.95% | 0.69% | 1 | 1 | 1309 |
| XL | 15.81% | 0.69% | 1 | 1 | 756 |
| XLA+XLB | 24.29% | 0.69% | 1 | 1 | 756 |
| S-original | 89.84% | 76.75% | 3248 | 3401 | 3923 |

## Coordinates and base matching

![Current binding positions](figures/binding_positions.svg)

Covered XS representatives use independently verified raw-sequence binding templates; uncovered representatives show aligned sites. S–XL plots retain representative binding sequences for their assays. Blue denotes compatibility, orange mismatch, grey gap/unknown, and boxes mark the terminal 3 nt; S–XL plots also use purple for potential G–T pairing. Representative rows do not replace full-panel statistics.

![XS base matching](figures/base_matching_XS.svg)

![SD base matching](figures/base_matching_SD.svg)

![S base matching](figures/base_matching_S.svg)

![MD base matching](figures/base_matching_MD.svg)

![M base matching](figures/base_matching_M.svg)

![LD base matching](figures/base_matching_LD.svg)

![L base matching](figures/base_matching_L.svg)

![XLD base matching](figures/base_matching_XLD.svg)

![XL base matching](figures/base_matching_XL.svg)

[S–XL完整碱基图 / Full S–XL alignment](results/terminal_optimization/base_matching.html)

## Design and verification

3′-terminal degeneracy is allowed. Every concrete variant is checked for no terminal homotriplet, ≥1 G/C in the final 3 nt, 1–4 G/C in the final 5 nt and no homopolymer longer than four. XS passes terminal rules and both thermodynamic concentration scenarios. S-original is the original control.

For XS, C++ exhaustive and Python bit-parallel full-sequence scans agree on 702 target decisions and four strict/exact background sets. S–XL independently agree on 11,200 target decisions and 32 background sets. Verification scopes are recorded separately. Design and evaluation reuse references; all assays await wet-lab validation.

```bash
python scripts/check_release.py
python scripts/check_ab.py
python scripts/verify_xs.py --output /tmp/MiCucumber-XS-check
```

## Data and methods

[引物 / Primer pairs](sequences/primer_pairs.csv) · [FASTA](sequences/primers.fasta) · [结果 / Comparison](results/current/comparison.csv) · [坐标 / Coordinates](results/current/binding_positions.csv) · [XS证据 / Evidence](results/xs/)

[Methods](docs/METHODS.md) · [中文方法](docs/METHODS.zh-CN.md) · [复现 / Reproduction](docs/REPRODUCIBILITY.md) · [文件索引 / File index](docs/FILES.md) · [A/B互补性 / Complementarity](docs/AB_COMPLEMENTARITY.md) · [报告 / Report](report.html)

## Copyright

Copyright © 2026 Fei Xia (GUIBA-EX). All rights reserved. [使用声明 / Terms](COPYRIGHT.md).
