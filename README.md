![MiCucumber](figures/MiCucumber_overview.png)

The header illustrates seven extant sea-cucumber orders: Apodida, Dendrochirotida, Elasipodida, Holothuriida, Molpadida, Persiculida and Synallactida. Order-level matching results retain the current reference-panel labels. [Illustration notes](figures/overview_design.md).

![Current binding positions](figures/binding_positions.svg)

Shared reference spans: S 226, M 245, L 302, XL 396 bp. Product lengths vary among taxa.

# MiCucumber

Computational design and matching assessment of mitochondrial 16S primers for sea cucumbers. [中文](README.zh-CN.md)

## Names and portfolios

Each region retains a degenerate single pair, an ordinary single pair and an ordinary A/B option. With the unchanged S-original control, there are 13 portfolios, 17 paired rows and 34 FASTA records. D denotes degeneracy; A/B are components of separate PCRs.

| Region | Degenerate | Ordinary | Ordinary A/B |
|---|---|---|---|
| S | 66.85% | 3.35% | 4 | 3 | 331 |
| M | 33.56% | 5.52% | 1 | 2 | 13 |
| L | 41.03% | 7.87% | 0 | 0 | 46 |
| XL | 15.81% | 0.69% | 1 | 1 | 756 |

**3′-terminal degeneracy is allowed.** Terminal matching uses IUPAC compatibility, and every concrete variant is checked: no terminal homotriplet, at least one G/C in the last three bases, 1–4 G/C in the last five, and no homopolymer longer than four. The final base need not be fixed or G/C. S-original is an unchanged control exempt from these selection rules.

## Retention decisions

Following Occam’s razor, retain one D portfolio per length: SD with modest degeneracy (2/8), MD under the strict background gate (64/4), LD for its coverage gain (32/1), and unchanged XLD (2/1). More aggressive SD, MD 128/4 and marginal-gain XLD variants remain comparisons. Ordinary single pairs, D and S-original are unchanged in the A/B re-selection; all four variants in each length share identical F/R start/end coordinates. This is an explicit benefit–complexity judgment, not a preregistered threshold or experimentally established PCR optimum.

[Before/after / 前后比较](docs/DECISIONS.md)

## Common-panel results

Coverage and exact matching below are non-Apodida metrics. The common panel has 151 taxonomic name labels and 351 haplotypes, including 145 non-Apodida labels, weighted equally by label and within label. All-target metrics are in the CSV. Background contains 5,600 records.

| Portfolio | Coverage | Exact | WC≤3 | GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
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

Coverage permits ≤2 mismatches per primer with exact terminal-three-base compatibility; exact matching requires zero mismatches in both primers. Background counts are accessions, not experimental amplification fractions. GT is a separate G–T tolerance sensitivity model.

WC≤4 exposes substantial residual background risk, especially in L and XL; small WC≤3/GT≤2 counts do not establish low environmental off-target amplification. All schemes await wet-lab validation. [Before/after comparison and verification](docs/TERMINAL_VALIDATION.md).

## Sequences, coordinates and evidence

[Primer pairs](sequences/primer_pairs.csv) · [FASTA](sequences/primers.fasta) · [Comparison](results/current/comparison.csv) · [Coordinates](results/current/binding_positions.csv) · [Missed references](results/terminal_optimization/missed_references.csv) · [Terminal audit](results/terminal_optimization/terminal_audit.csv) · [Verification](results/terminal_optimization/verification.json)

[Methods](docs/METHODS.md) · [中文方法](docs/METHODS.zh-CN.md) · [Reproduction](docs/REPRODUCIBILITY.md) · [文件索引 / File index](docs/FILES.md) · [Bilingual report](report.html)

## Base matching

Blue: IUPAC-compatible; orange: mismatch; purple: possible G–T pairing. Boxes mark the final three bases. Degenerate plots show the single pair; ordinary plots show A/B. Each order is represented by its most frequent weighted binding sequence; the full page includes all schemes and reference variants.

![SD base matching](figures/base_matching_SD.svg)

![S base matching](figures/base_matching_S.svg)

![MD base matching](figures/base_matching_MD.svg)

![M base matching](figures/base_matching_M.svg)

![LD base matching](figures/base_matching_LD.svg)

![L base matching](figures/base_matching_L.svg)

![XLD base matching](figures/base_matching_XLD.svg)

![XL base matching](figures/base_matching_XL.svg)

[Full base alignment](results/terminal_optimization/base_matching.html)

## Verification and scope

All 11,200 target-state and 32 background-set checks agree. References are reused for design and evaluation. Apodida is excluded from selection but retained in all-target reporting. Two-pair results represent separate-PCR unions, not a multiplex experiment.

```bash
python scripts/check_release.py
```

## Copyright

Copyright © 2026 Fei Xia (GUIBA-EX). All rights reserved. [Terms / 使用声明](COPYRIGHT.md).


Expanded fixed-coordinate search yields mutual A/B contributions at every length without reducing either union metric. Ordinary single pairs and D are unchanged. Choose a single pair or complementary A/B according to the sample objective. [Complementarity and unique hits](docs/AB_COMPLEMENTARITY.md)
