![MiCucumber](figures/MiCucumber_overview.png)

![Current binding positions](figures/binding_positions.svg)

Ordinary, A, B and D variants within each region share identical F/R start and end coordinates. S/M/L/XL reference spans are 226/245/302/396 bp. The map uses current oligo coordinates on one linear scale; product lengths vary among taxa.

# MiCucumber

Computational design and matching assessment of mitochondrial 16S primers for sea cucumbers. [中文](README.zh-CN.md)

## Names and portfolios

Each region retains a degenerate single pair, an ordinary single pair and an ordinary A/B option. With the unchanged S-original control, there are 13 portfolios, 17 paired rows and 34 FASTA records. D denotes degeneracy; A/B are components of separate PCRs.

| Region | Degenerate | Ordinary | Ordinary A/B |
|---|---|---|---|
| S | SD | S | SA / SB |
| M | MD | M | MA / MB |
| L | LD | L | LA / LB |
| XL | XLD | XL | XLA / XLB |

**3′-terminal degeneracy is allowed.** Terminal matching uses IUPAC compatibility, and every concrete variant is checked: no terminal homotriplet, at least one G/C in the last three bases, 1–4 G/C in the last five, and no homopolymer longer than four. The final base need not be fixed or G/C. S-original is an unchanged control exempt from these selection rules.

## Common-panel results

Coverage and exact matching below are non-Apodida metrics. The common panel has 151 taxonomic name labels and 351 haplotypes, including 145 non-Apodida labels, weighted equally by label and within label. All-target metrics are in the CSV. Background contains 5,600 records.

| Portfolio | Coverage | Exact | WC≤3 | GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
| SD | 73.97% | 5.07% | 4 | 3 | 332 |
| S | 66.85% | 3.35% | 4 | 3 | 331 |
| SA+SB | 71.38% | 4.56% | 4 | 3 | 378 |
| MD | 40.37% | 6.86% | 1 | 2 | 17 |
| M | 33.56% | 5.52% | 1 | 2 | 13 |
| MA+MB | 36.36% | 10.80% | 1 | 3 | 39 |
| LD | 43.33% | 15.00% | 0 | 0 | 46 |
| L | 41.03% | 7.87% | 0 | 0 | 46 |
| LA+LB | 43.33% | 15.00% | 0 | 0 | 46 |
| XLD | 19.95% | 0.69% | 1 | 1 | 1309 |
| XL | 15.81% | 0.69% | 1 | 1 | 756 |
| XLA+XLB | 15.81% | 0.69% | 4 | 4 | 757 |
| S-original | 89.84% | 76.75% | 3248 | 3401 | 3923 |

Coverage permits ≤2 mismatches per primer with exact terminal-three-base compatibility; exact matching requires zero mismatches in both primers. Background counts are accessions, not experimental amplification fractions. GT is a separate G–T tolerance sensitivity model.

**Joint locus selection replaces independent optimization of each portfolio location.** At each candidate locus, select the best ordinary single, A/B union and degenerate single, then average their coverage-plus-exact scores equally to choose the shared locus. Some coverage is lost; XL A/B adds no benefit over its single pair and remains a comparator. SD reaches 73.97% coverage / 5.07% exact; LD and LA/LB both reach 43.33% / 15.00%.

WC≤4 exposes substantial residual background risk, especially in S and XL; small WC≤3/GT≤2 counts do not establish low environmental off-target amplification. All schemes await wet-lab validation. [Before/after comparison and verification](docs/TERMINAL_VALIDATION.md).

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

[共同坐标 / Shared coordinates](results/current/joint_locus.csv) · [联合筛选复核 / Joint-locus validation](docs/TERMINAL_VALIDATION.md)
