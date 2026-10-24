# MiCucumber

Computational mitochondrial 16S primer candidates for sea cucumbers. The four regions are **S, M, L and XL**, each with one-/two-pair degenerate and nondegenerate options. **S-original** preserves the original control: 17 portfolios in total. [中文](README.zh-CN.md)

## Naming and selection

- `D1` / `D2`: one / two degenerate primer pairs; `ND1` / `ND2`: one / two A/C/G/T-only pairs.
- `S-original`: the original v4 pair, including its original degeneracies; distinct from optimized S-D1.
- Two pairs mean two independent PCRs. Regions are alternative comparisons; no requirement to run all portfolios on every sample.
- **Prioritize S-D2 for experimental evaluation.** Nondegenerate sets lose substantial coverage and exact matching and remain comparators. S-original has extensive background hits.
- No portfolio has wet-lab validation or a validated single-tube multiplex recipe.

| Previous name / 旧名 | Current name / 新名 |
|---|---|
| v4opt (optimized v4 region) | S |
| S | M |
| M | L |
| L | XL |
| Original v4 / v4原版 | S-original |

This update changes names, file organization and documentation only. **Primer sequences and numerical results are unchanged.** [Naming rules and row-level mapping](docs/NAMING.md)

## Downloads and documentation

- **[All primer pairs, CSV](sequences/primer_pairs.csv)** · [FASTA](sequences/primers.fasta) · [S-original](sequences/MiCucumber-S-original.fasta)
- By region: [S](sequences/MiCucumber-S.csv) · [M](sequences/MiCucumber-M.csv) · [L](sequences/MiCucumber-L.csv) · [XL](sequences/MiCucumber-XL.csv)
- [Bilingual report](report.html) (download to view) · [Full common/own-region comparison](results/comparison.csv)
- [Methods](docs/METHODS.md) · [Reproduction](docs/REPRODUCIBILITY.md) · [File index](docs/FILES.md)

## Degenerate portfolios

The tables below report **non-Apodida common-panel** metrics. The full common panel has 151 taxonomic name labels and 351 within-label haplotypes, including 145 non-Apodida labels. Equal label and within-label haplotype weights; synonyms are not reconciled. All-target metrics including Apodida and own-region metrics are in the full comparison file.

| Portfolio | Non-Apodida coverage | Exact matching | WC≤3 | GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
| MiCucumber-S-D1 | 87.45% | 27.48% | 2 | 0 | 742 |
| MiCucumber-S-D2 | 88.53% | 40.84% | 2 | 0 | 742 |
| MiCucumber-M-D1 | 56.90% | 9.43% | 0 | 0 | 130 |
| MiCucumber-M-D2 | 62.42% | 14.25% | 0 | 0 | 131 |
| MiCucumber-L-D1 | 70.26% | 33.63% | 4 | 0 | 109 |
| MiCucumber-L-D2 | 74.06% | 35.01% | 4 | 0 | 109 |
| MiCucumber-XL-D1 | 48.34% | 9.71% | 0 | 0 | 486 |
| MiCucumber-XL-D2 | 55.27% | 11.78% | 0 | 4 | 492 |

## Nondegenerate comparators

| Portfolio | Non-Apodida coverage | Exact matching | WC≤3 | GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
| MiCucumber-S-ND1 | 56.78% | 0.34% | 0 | 0 | 2 |
| MiCucumber-S-ND2 | 71.96% | 0.34% | 0 | 0 | 2 |
| MiCucumber-M-ND1 | 14.05% | 0.00% | 0 | 0 | 0 |
| MiCucumber-M-ND2 | 23.70% | 3.91% | 0 | 0 | 0 |
| MiCucumber-L-ND1 | 35.24% | 3.97% | 0 | 0 | 0 |
| MiCucumber-L-ND2 | 46.68% | 8.00% | 0 | 0 | 0 |
| MiCucumber-XL-ND1 | 22.88% | 2.93% | 0 | 0 | 0 |
| MiCucumber-XL-ND2 | 28.86% | 5.23% | 0 | 0 | 1 |

## Original control

| Portfolio | Non-Apodida coverage | Exact matching | WC≤3 | GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
| MiCucumber-S-original | 89.84% | 76.75% | 3248 | 3401 | 3923 |

Coverage permits ≤2 mismatches per primer with the terminal 3 nt exact; exact matching requires zero mismatches in both primers. Background hits are accession unions among 5,600 records, not species counts or read fractions. WC≤3 and GT≤2 are screening models; WC≤4 exposes relaxed residual risk. These counts do not directly predict experimental amplification fractions.

## Amplicon regions

![S M L XL reference design windows](figures/amplicon_regions.en.png)

The figure shows homologous seed windows on AB525437.1. Variant primer lengths can differ, and reference spans are not universal product-length predictions. Historical 7/7/6/9-pair annotations have been removed.

## Evidence and reproduction scope

- Degenerate sets: selected from 96 independently checked candidate pairs; 21,036 target agreement checks for the eight current portfolios.
- Nondegenerate sets: 2,644 concrete candidate pairs enumerated; 31,428 agreement checks for the selected portfolios and original control, with complete reproduction tested.
- Current references: 1,848 target and 5,600 background records. Apodida is excluded from optimization but retained in all-target reporting. Two added loci are direction-corrected homology inferences; six UNVERIFIED records were excluded.
- Design and evaluation reuse frozen references; no independent holdout validation. Exhaustive optimality is conditional on the candidate pool and objective.
- Run `python scripts/check_release.py` to check current exports, mappings and hashes. Computational entry points are documented under [Reproduction](docs/REPRODUCIBILITY.md).

Previous documents, historical sequences and analysis implementations are preserved in the [historical archive](archive/README.md). Frozen evidence retains its source identifiers; current exports are normalized. Existing release tags are unchanged.

## Copyright

Copyright © 2026 Fei Xia (GUIBA-EX). All rights reserved. Public access is not an open-source license. Unauthorized republication and redistribution of protected original materials are prohibited, subject to statutory exceptions, GitHub platform rights and third-party data rights. [Full notice](COPYRIGHT.md)
