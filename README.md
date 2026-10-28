![MiCucumber](figures/MiCucumber_overview.png)

# MiCucumber

[中文](README.zh-CN.md)

Candidate mitochondrial 16S rRNA primers for environmental DNA across XS, S, M, L and XL. Each S–XL window retains an ordinary pair and a degenerate D pair at shared reference coordinates; XS is a single retained pair.
One reference per species is retained. Primary metrics weight evaluable species equally, with order-level results reported separately.
The sea-cucumber panel contains 174 species; XS, S–L and XL have 166, 174 and 152 evaluable species, respectively.

[参考面板 / Reference panel](results/species_qc/panel.csv) · [参考序列审核 / Reference curation](results/species_qc/README.md)

![Binding positions](figures/amplicon_regions.en.svg)

## Predicted performance

| Name | Coverage | Exact | Strict WC / GT | WC≤3 / GT≤2 |
|---|---:|---:|---:|---:|
| XS | 75/166 (45.18%) | 0/166 (0.00%) | 0 / 0 | 33 / 2 |
| S | 110/174 (63.22%) | 5/174 (2.87%) | 1 / 3 | 4 / 3 |
| SD | 130/174 (74.71%) | 0/174 (0.00%) | 0 / 5 | 58 / 6 |
| M | 55/174 (31.61%) | 9/174 (5.17%) | 0 / 2 | 1 / 2 |
| MD | 89/174 (51.15%) | 24/174 (13.79%) | 0 / 15 | 3 / 15 |
| L | 65/174 (37.36%) | 13/174 (7.47%) | 0 / 0 | 0 / 0 |
| LD | 82/174 (47.13%) | 29/174 (16.67%) | 0 / 0 | 0 / 0 |
| XL | 23/152 (15.13%) | 1/152 (0.66%) | 0 / 0 | 1 / 1 |
| XLD | 43/152 (28.29%) | 3/152 (1.97%) | 0 / 10 | 1 / 13 |

Coverage allows at most two mismatches per primer with compatible terminal 3 nt; exact matching requires zero mismatches in both primers. Strict WC/GT retain the terminal constraint; WC≤3 / GT≤2 are permissive background screens.

Each D primer has at most eight variants, with ambiguity confined to its 3′ half. XS is a single pair with a fixed name. Computational predictions require experimental validation.

SD has no exact paired matches in the current panel. LD primarily covers Holothuriida (71/77), with 8/36 Dendrochirotida and 0/22 Elasipodida.

## XS

| Name | F (5′→3′) | R (5′→3′) |
|---|---|---|
| XS | `AACTTTGGTTGGGGYAAC` | `TTTCCCCAATCCAACATCGA` |

![XS base matching](results/current_primers/XS/base_matching_XS.svg)

[XS · Orders](results/current_primers/XS/XS_by_order.csv) · [Species](results/current_primers/XS/XS_by_taxon.csv)

## S

| Name | F (5′→3′) | R (5′→3′) |
|---|---|---|
| S | `CCAGAAAGACGAGAAGACCCTGTC` | `GAGGAGATAACGCTGTTATCCCTG` |
| SD | `TAAGAAAGACGARAAGACCCTRTC` | `GAGAAGATGACGCTGTTATCCCTR` |

![S base matching](results/current_primers/S/base_matching_S.svg)

![SD base matching](results/current_primers/S/base_matching_SD.svg)

[S · Orders](results/current_primers/S/S_by_order.csv) · [Species](results/current_primers/S/S_by_taxon.csv)

[SD · Orders](results/current_primers/S/SD_by_order.csv) · [Species](results/current_primers/S/SD_by_taxon.csv)

## M

| Name | F (5′→3′) | R (5′→3′) |
|---|---|---|
| M | `AAACTTCTATTAACGTGAAGAA` | `GTTATCCCTGCGGTAACT` |
| MD | `AAACTTCTATTHAYGTGAAGAA` | `GTTATCCCTGCGGTAACT` |

![M base matching](results/current_primers/M/base_matching_M.svg)

![MD base matching](results/current_primers/M/base_matching_MD.svg)

[M · Orders](results/current_primers/M/M_by_order.csv) · [Species](results/current_primers/M/M_by_taxon.csv)

[MD · Orders](results/current_primers/M/MD_by_order.csv) · [Species](results/current_primers/M/MD_by_taxon.csv)

## L

| Name | F (5′→3′) | R (5′→3′) |
|---|---|---|
| L | `AGACTCGTATGAACGGCAAAACCT` | `CGCTGTTATCCCTGCGGT` |
| LD | `AGACTTGTATGAAYGGCRAAACMT` | `CGCTGTTATCCCTGCRGT` |

![L base matching](results/current_primers/L/base_matching_L.svg)

![LD base matching](results/current_primers/L/base_matching_LD.svg)

[L · Orders](results/current_primers/L/L_by_order.csv) · [Species](results/current_primers/L/L_by_taxon.csv)

[LD · Orders](results/current_primers/L/LD_by_order.csv) · [Species](results/current_primers/L/LD_by_taxon.csv)

## XL

| Name | F (5′→3′) | R (5′→3′) |
|---|---|---|
| XL | `GGTCACGCCTGCCCAGTGGA` | `AAGATAACGCTGTTATCCCTGCGGTAACTT` |
| XLD | `GGTAACGCCTGCCCARTGGA` | `GAGATTACGCTGTTATCCCTGCGGTAACTD` |

![XL base matching](results/current_primers/XL/base_matching_XL.svg)

![XLD base matching](results/current_primers/XL/base_matching_XLD.svg)

[XL · Orders](results/current_primers/XL/XL_by_order.csv) · [Species](results/current_primers/XL/XL_by_taxon.csv)

[XLD · Orders](results/current_primers/XL/XLD_by_order.csv) · [Species](results/current_primers/XL/XLD_by_taxon.csv)

[Methods / 方法](docs/METHODS.md)

[Validation / 验证](docs/VALIDATION.md) · [Copyright / 著作权](COPYRIGHT.md)
