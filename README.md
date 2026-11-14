![MiCucumber](figures/MiCucumber_overview_current.png)

# MiCucumber: in silico design and evaluation of mitochondrial primers for sea cucumber eDNA metabarcoding

**Fei Xia** · The University of Tokyo · xf@g.ecc.u-tokyo.ac.jp · [English](README.md) · [简体中文](README.zh-CN.md)

[Working manuscript PDF](publications/submission/MiCucumber_revision.pdf) · [Manuscript source](publications/submission/MiCucumber_revision.md) · [All primers (FASTA)](sequences/all_testing_primers.fasta) · [All oligonucleotides (CSV)](sequences/all_testing_primers.csv) · [Supplementary table](publications/submission/supplementary_primers.csv)

[Editable manuscript](publications/submission/MiCucumber_revision.docx) · [Supplementary PDF](publications/submission/Supplementary.pdf) · [Primer pairs](publications/submission/ESM_1.xlsx) · [All oligonucleotides](publications/submission/ESM_2.xlsx) · [Fig. 1 A4](publications/submission/figures/Fig1_A4.pdf)

## Complete primer set

The project provides 29 baseline primer pairs across 16S, 12S and COI, plus three 16S lineage-specific supplementary oligonucleotides. The full FASTA and table above are available for testing across lengths and markers. Primer names use XS, S, M, L and XL for window size, with D indicating a degenerate pair. [16S pair table](sequences/primer_pairs.csv) · [12S and COI pair table](markers/12S_COI/candidates.csv) · [Lineage supplement combinations](results/lineage_evaluation/README.md)

## Detailed in silico comparison

| Assay | Reference span | Species matched, 0 / ≤1 / ≤2 mismatches per primer | MIDORI2 non-target species, ≤2 mismatches |
|---|---:|---:|---:|
| 16S SD | 226 bp | 1 / 46 / 155 of 174 | 7 |
| 16S LD | 302 bp | 29 / 66 / 99 of 174 | 45 |
| COI LD | 293 bp | 10 / 58 / 118 of 274 | 0 |

Both 16S assays in this comparison include a supplementary oligonucleotide. The table reports selected assays assessed on the updated MIDORI2 panel. The COI denominator is a WoRMS-reconciled, alignment-evaluable panel; four names without an exact species-level match are listed in the audit. The 16S assays matched none of five Apodida representatives; COI LD matched one of 19. With the same two-mismatch rule, hol.11 matched 163/174 sea cucumber representatives and 49,352 non-target MIDORI2 species. MIDORI2 provides eukaryotic mitochondrial references. These values are computational predictions. [Coverage by order](results/complementarity/) · [MIDORI2 species and counts](results/specificity/) · [Reference-insert resolution](results/resolution/)

![Primer positions](publications/submission/figures/figure1_positions.png)

[Order-level matching](publications/submission/figures/figure2_coverage.png) · [Reference-insert identity](publications/submission/figures/figure3_identity.png) · [Reproduction](scripts/review/README.md)

Ordinary 16S S matched 5, 26 and 110 of the same 174 species at zero, at most one and at most two mismatches per primer. Its additional comparison covers target matching and insert similarity. Fig. 1 shows 31 representatives from seven orders and 21 families with all five binding windows. Fig. 3 shows 16S SD by order; other primer matrices are in supplementary Fig. S5.

## Sequences of the three detailed assays

Sequences are written 5′→3′. Each 16S assay uses the listed primary pair and its supplementary oligonucleotide.

| Assay | Oligonucleotide | Sequence |
|---|---|---|
| 16S SD | F | `TAAGAAAGACGARAAGACCCTRTC` |
| 16S SD | R | `GAGAAGATGACGCTGTTATCCCTR` |
| 16S SD | R-Dendrochirotida | `AAGGAGATTACGCTGTTATCCCTG` |
| 16S LD | F | `AGACTTGTATGAAYGGCRAAACMT` |
| 16S LD | F-Elasipodida | `AAACTAGTATGAATGGCTTTTCAT` |
| 16S LD | R | `CGCTGTTATCCCTGCRGT` |
| COI LD | F | `AAAATGCGAACYCCAGGARTWAC` |
| COI LD | R | `GGTTCTTGCTTWCCTCTRTARTG` |

## Reference-insert resolution

At the species level, 473/483 distinct 16S SD inserts, 338/346 16S LD inserts and 666/683 COI LD inserts carried one species label in the evaluated reference records. The full species, genus and family results and shared inserts are available in the resolution tables.

<details>
<summary>Earlier comparisons and supplementary materials</summary>

[All baseline primer sequences and earlier mismatch gradients](publications/submission/supplementary_primers.csv) · [Supplementary information](publications/submission/Supplementary.pdf)

</details>

[Earlier methods (v1.8)](docs/METHODS.md) · [Copyright](COPYRIGHT.md) · [Citation for v1.8](CITATION.cff) · [Project files](PROJECT_FILES.md)
