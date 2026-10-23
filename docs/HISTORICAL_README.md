# MiCucumber

**Sea-cucumber mitochondrial 16S primer design and in-silico evaluation.**

[中文说明](../README.zh-CN.md) · [Methods](METHODS.md) · [方法说明](METHODS.zh-CN.md) · [Reproducibility / 复现](REPRODUCIBILITY.md)

This repository documents the optimization of historical MiCucumber primers using a frozen MiStar reference dataset: specificity-first screening, multiple length series, and additional same-locus primer pairs to improve Apodida coverage. Release **v0.1.0** is a computational candidate release, not a validated wet-lab assay or a historical “v5”.

## Latest results

| Version / 版本 | Independent PCRs / 独立PCR | Overall coverage / 总覆盖 | Apodida panel / 面板 | WC≤3 / GT≤2 | WC≤4 |
|---|---:|---:|---:|---:|---:|
| v4opt + Apodida | 7 | 92.51% | 2/4 | 2 / 0 | 750 |
| S + Apodida | 7 | 70.70% | 3/4 | 0 / 0 | 130 |
| M + Apodida | 6 | 79.48% | 2/4 | 4 / 0 | 109 |
| L + Apodida | 9 | 66.76% | 4/4 | 0 / 4 | 492 |

Coverage uses a common panel of **149 taxon-name labels / 347 within-label haplotypes**, with equal label weighting and equal haplotype weighting within each label. The panel contains just **four Apodida records / four labels**; 4/4 does not establish order-wide coverage. Each primer may have ≤2 mismatches, with its terminal three 3′ bases perfectly matched. Background counts are accession unions among 5,600 reference records, not species counts or predicted read fractions.

The original v4 has 87.46% coverage and 3,248 / 3,401 WC≤3 / GT≤2 background hits. The first optimized separate-PCR v4 reached 90.50%; Apodida supplementation raises this to 92.51% without increasing its background unions. Substantial WC≤4 risk remains.

## Amplicon region map

![MiCucumber conservation and amplicon regions](../figures/amplicon_regions.en.png)

Following the MiStar visualization layout, the upper panel shows equal-label-weighted conservation and callable-base weight; the lower panel shows forward/reverse primer direction and primer-free intervals on **AB525437.1 extracted 16S coordinates (1-based)**. Arrows depict the four seed design windows; same-locus variants and Apodida additions can have different physical lengths. The reference spans are not universal product-size predictions. Counts refer to the latest **separate-PCR** schemes, not a mixed tube.

[Vector SVG](../figures/amplicon_regions.en.svg) · [PDF](../figures/amplicon_regions.en.pdf) · [Coordinates](../figures/region_coordinates.csv) · [Conservation data](../figures/reference_conservation.csv) · [Plot script](../plot_regions.py)

## Get the primers

- **[Complete latest separate-PCR pairs](../results/final_separate_pairs.csv)** — includes the four original component pairs plus additions; no manual joining needed.
- [FASTA, 5′→3′](../results/final_separate_primers.fasta) — gene-specific sequences only, no adapters or indexes.
- [Apodida additions](../results/apodida_additional_pairs.csv) and [latest comparison](../results/apodida_comparison.csv).
- [Round-one primers](../results/round1_primers.csv), [pairings](../results/round1_pairings.csv), and [comparison](../results/round1_comparison.csv), including original v4 and the older decided pair.

**Each row of the latest pair table is a separate PCR.** Do not mix the supplemented sets in one tube: their new cross-pair combinations and whole-pool dimers have not been evaluated. Round-one Pool sets were evaluated as 4F × 4R; their sequences differ from Separate sets. Cross-length multiplexing is not evaluated.

Round-one predicted product ranges (including primers, excluding adapters) are v4opt 178–218 bp, S 201–241 bp, M 285–325 bp, L 354–395 bp. These ranges must not be automatically assigned to the supplemented sets, whose oligo lengths can differ; per-record sizes are saved in `analysis/apodida/independent_hits.tsv`.

## Evidence and limits

- 1,846 target records and 5,600 background records; 116 full-length unambiguous sequences anchor the alignment.
- All 110 round-one selected/baseline pairs were checked by an independent exhaustive C++ scanner: **386,492 consistency checks passed**.
- Apodida supplementation screened 37 observed pairs from 17 source records and retained 13 scheme-local additions. It uses the same exhaustive scanner but does not yet have a second independent implementation cross-check for the added pairs.
- The reference set is reused for discovery and evaluation; this is not held-out validation. Names and historical taxonomy were not synonym-reconciled. Partial references and ambiguous bases limit negative evidence.
- Round-one exact-match coverage is only 11.66–37.44% for optimized schemes; mismatch-tolerant coverage does not establish amplification uniformity. Added pairs also need wet-lab testing.

## Revalidate

Python 3.12 and a C++17 compiler are required. Install the pinned dependencies in an isolated environment, then run:

```bash
python -m pip install -r requirements.txt
python revalidate.py
```

See [reproducibility](REPRODUCIBILITY.md) for the supported scope. The frozen inputs and validation code are included. No fresh NCBI download is performed.

## Provenance and reuse

Historical v4 sequences were transcribed from `MiStar.xlsx`, sheet `Primer_Cucumber`, B30:C31 (2024-08-23); the older decided Fv2/Rv3A pair comes from B17:C18 after removing adapters. The private workbook and correspondence are not distributed. The public accession manifest is `analysis/metadata.tsv`; inherited source fingerprints are in `analysis/input_manifest.json`.

**Copyright © 2026 Fei Xia (GUIBA-EX). All rights reserved.** Unauthorized republication, mirroring, redistribution, and publication of translations/adaptations of protected original materials are prohibited. Public access is not an open-source license. Statutory exceptions, GitHub platform rights and third-party reference-data rights remain unaffected. See [Copyright and permissions](../COPYRIGHT.md).
