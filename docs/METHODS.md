# Design and evaluation

## Reference panel and matching

The shared panel contains 351 haplotypes with 151 taxonomic name labels, including 145 non-Apodida labels. Labels receive equal weight, as do haplotypes within each label. Primary taxonomic coverage includes Apodida and balances represented orders equally. Taxon detection counts a name label if any reference is covered; mean within-label matching remains a secondary measure. [Definitions](TAXONOMIC_COVERAGE.md). Frozen order labels are retained without reclassification. Design and evaluation reuse this panel.

Coverage allows ≤2 mismatches per primer and IUPAC-compatible final three bases. Exact matching requires zero mismatches in both primers. Background contains 5,600 non-target records. WC uses standard pairing; GT additionally tolerates G–T pairing. Background WC≤3, GT≤2 and WC≤4 columns omit the terminal constraint. Strict background counts apply the target coverage rule. Counts are accessions, not experimental amplification fractions.

## Assays and complexity

XS is one fixed degenerate assay at F 1042–1059 and R 1213–1232 on extracted ungapped AB525437.1 16S. Reference span is 191 bp, with predicted products 186–203 bp. Its bounded search around the homologous MiLily-XS region is described in [XS](XS.md).


## Terminal and thermal rules

3′ degeneracy is allowed. Every concrete variant must have no terminal homotriplet, ≥1 G/C in the last three bases, 1–4 G/C in the last five and no homopolymer longer than four. S-original is exempt as a control.

Primer3 uses 50 mM monovalent salt, 1.5 mM Mg and 0.6 mM dNTP, under 50 nM per concrete variant and 200 nM per direction. Maximum predicted hairpin/dimer Tm must be <55°C and the F/R Tm-range midpoint difference ≤5°C in both scenarios. XS and current S–XL pass these rules. At 200 nM per direction, each MD forward variant is 1.5625 nM.

## Background trade-off and verification


XS metrics use full original-FASTA scans in both orientations: targets require 70–500 bp products and ≥20 bp internal sequence; background internal spacing is 0–1000 bp. The existing S–XL pipeline retains its frozen product settings. Independent C++/Python full-sequence checks for XS agree on 702 target decisions and four strict/exact background sets; its broader background metrics are recalculated by C++. S–XL verification separately agrees on 11,200 target decisions and 32 background sets. Representative base plots supplement full-panel statistics.

References are reused for selection and evaluation. Apodida remains poorly covered; all assays await wet-lab validation. XS is shorter and has greater coverage than SD, with more background hits and slightly lower observed discrimination on common labels. [XS assessment](XS.md) · [Reproduction](REPRODUCIBILITY.md).


Current four D assays are independently checked source candidates from the ten-candidate round (7,020 target decisions, 40 strict/exact background sets; zero disagreements). / 当前四个D方案来自10候选独立复核（7,020项目标判断、40组严格/完全背景集合，差异为0）。
