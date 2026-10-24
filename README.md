# MiCucumber

Computational mitochondrial 16S primer candidates for sea cucumbers. The four regions are **S, M, L and XL**, each with one-/two-pair degenerate and nondegenerate options. **S-original** preserves the original control: 17 portfolios in total. [中文](README.zh-CN.md)

## Portfolio selection

Degenerate sets use **S-D, M-D, L-D and XL-D**; nondegenerate sets use **S, M, L and XL**. The final `1pair` / `2pair` indicates pair count.

- Two pairs mean two independent PCRs. Regions are alternative comparisons; no requirement to run all portfolios on every sample.
- **Prioritize S-D-2pair for experimental evaluation.** Nondegenerate sets lose substantial coverage and exact matching and remain comparators. S-original has extensive background hits.
- No portfolio has wet-lab validation or a validated single-tube multiplex recipe.

## Downloads and documentation

- **[All primer pairs, CSV](sequences/primer_pairs.csv)** · [FASTA](sequences/primers.fasta) · [S-original](sequences/MiCucumber-S-original.fasta)
- By region: [S](sequences/MiCucumber-S.csv) · [M](sequences/MiCucumber-M.csv) · [L](sequences/MiCucumber-L.csv) · [XL](sequences/MiCucumber-XL.csv)
- [Bilingual report](report.html) (download to view) · [Full common/own-region comparison](results/comparison.csv)
- [Methods](docs/METHODS.md) · [Reproduction](docs/REPRODUCIBILITY.md) · [File index](docs/FILES.md)

## Degenerate portfolios

The tables below report **non-Apodida common-panel** metrics. The full common panel has 151 taxonomic name labels and 351 within-label haplotypes, including 145 non-Apodida labels. Equal label and within-label haplotype weights; synonyms are not reconciled. All-target metrics including Apodida and own-region metrics are in the full comparison file.

| Portfolio | Non-Apodida coverage | Exact matching | WC≤3 | GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
| MiCucumber-S-D-1pair | 87.45% | 27.48% | 2 | 0 | 742 |
| MiCucumber-S-D-2pair | 88.53% | 40.84% | 2 | 0 | 742 |
| MiCucumber-M-D-1pair | 56.90% | 9.43% | 0 | 0 | 130 |
| MiCucumber-M-D-2pair | 62.42% | 14.25% | 0 | 0 | 131 |
| MiCucumber-L-D-1pair | 70.26% | 33.63% | 4 | 0 | 109 |
| MiCucumber-L-D-2pair | 74.06% | 35.01% | 4 | 0 | 109 |
| MiCucumber-XL-D-1pair | 48.34% | 9.71% | 0 | 0 | 486 |
| MiCucumber-XL-D-2pair | 55.27% | 11.78% | 0 | 4 | 492 |

## Nondegenerate comparators

| Portfolio | Non-Apodida coverage | Exact matching | WC≤3 | GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
| MiCucumber-S-1pair | 56.78% | 0.34% | 0 | 0 | 2 |
| MiCucumber-S-2pair | 71.96% | 0.34% | 0 | 0 | 2 |
| MiCucumber-M-1pair | 14.05% | 0.00% | 0 | 0 | 0 |
| MiCucumber-M-2pair | 23.70% | 3.91% | 0 | 0 | 0 |
| MiCucumber-L-1pair | 35.24% | 3.97% | 0 | 0 | 0 |
| MiCucumber-L-2pair | 46.68% | 8.00% | 0 | 0 | 0 |
| MiCucumber-XL-1pair | 22.88% | 2.93% | 0 | 0 | 0 |
| MiCucumber-XL-2pair | 28.86% | 5.23% | 0 | 0 | 1 |

## Original control

| Portfolio | Non-Apodida coverage | Exact matching | WC≤3 | GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
| MiCucumber-S-original | 89.84% | 76.75% | 3248 | 3401 | 3923 |

Coverage permits ≤2 mismatches per primer with the terminal 3 nt exact; exact matching requires zero mismatches in both primers. Background hits are accession unions among 5,600 records, not species counts or read fractions. WC≤3 and GT≤2 are screening models; WC≤4 exposes relaxed residual risk. These counts do not directly predict experimental amplification fractions.

## Amplicon regions

![S M L XL reference design windows](figures/amplicon_regions.en.png)

## Data and reproduction

- Degenerate sets: selected from 96 independently checked candidate pairs; 21,036 target agreement checks for the eight current portfolios.
- Nondegenerate sets: 2,644 concrete candidate pairs enumerated; 31,428 agreement checks for the selected portfolios and original control, with complete reproduction tested.
- Current references: 1,848 target and 5,600 background records. Apodida is excluded from optimization but retained in all-target reporting. Two added loci are direction-corrected homology inferences; six UNVERIFIED records were excluded.
- Design and evaluation reuse frozen references; no independent holdout validation. Exhaustive optimality is conditional on the candidate pool and objective.
- Run `python scripts/check_release.py` to check current exports, mappings and hashes. Computational entry points are documented under [Reproduction](docs/REPRODUCIBILITY.md).

## Copyright

Copyright © 2026 Fei Xia (GUIBA-EX). All rights reserved. Public access is not an open-source license. Unauthorized republication and redistribution of protected original materials are prohibited, subject to statutory exceptions, GitHub platform rights and third-party data rights. [Full notice](COPYRIGHT.md)
