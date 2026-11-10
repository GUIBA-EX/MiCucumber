![MiCucumber](figures/MiCucumber_overview.png)

# MiCucumber: in silico design and evaluation of mitochondrial primers for sea cucumber (Holothuroidea) eDNA metabarcoding

**Fei Xia**

[English](README.md) · [简体中文](README.zh-CN.md)

<!-- publication:start -->
**Preprint v1.7 · 11 November 2026**

[PDF](publications/MiCucumber_preprint.pdf) · [Manuscript](publications/MiCucumber_preprint.md) · [Versioned release](https://github.com/GUIBA-EX/MiCucumber/releases/tag/preprint-v1.7) · [CITATION.cff](CITATION.cff) · [BibTeX](CITATION.bib) · [Build and updates](publications/README.md)
<!-- publication:end -->

MiCucumber provides 29 candidate primer pairs for sea cucumber eDNA metabarcoding at three mitochondrial loci (16S, 12S and COI), plus two lineage supplements for 16S.

[Baseline primer set (FASTA)](sequences/all_markers.fasta) · [16S primer table (CSV)](sequences/primer_pairs.csv) · [12S and COI primer table (CSV)](markers/12S_COI/candidates.csv)

## Choosing a primer

| Goal | Assay | Reference span | Covered | Exact |
|---|---|---:|---:|---:|
| Broader 16S coverage | 16S SD-Dendrochirotida | 226 bp | 138/151 | 1/151 |
| Exact matches with one 16S pair | 16S LD | 302 bp | 73/151 | 23/151 |
| Highest 12S species count | 12S XLD | 354 bp | 33/53 | 7/53 |
| Shortest COI window | COI XSD | 145 bp | 43/57 | 3/57 |
| Highest COI species count | COI LD | 293 bp | 103/283 | 11/283 |

The 16S rows use the same 151-species panel. For 12S and COI, denominators are the species evaluable in each window. Predicted coverage allows up to two mismatches per primer and requires compatibility at the three 3′ terminal bases. An exact match requires zero mismatches at both sites.

## 16S lineage supplements

Both supplements retain the original binding coordinates. Counts below use the same 174 sea cucumber species.

| Scheme | Added oligo | Covered | Paired exact | Added strict background hits¹ |
|---|---|---:|---:|---:|
| SD-Dendrochirotida | R-Dendrochirotida | 130 → 155 | 0 → 1 | 0 / 0 |
| LD-Elasipodida | F-Elasipodida | 82 → 97 | 29 → 29 | 0 / 0 |
| LD-Synallactida | F-Synallactida | 82 → 104 | 29 → 36 | 0 / 0 |
| LD-Synallactida-Elasipodida | Both F oligos | 82 → 119 | 29 → 36 | 0 / 0 |

¹ Watson–Crick only / also allowing guanine–thymine pairing. SD-Dendrochirotida added 1 and 20 background records under relaxed GT2 and WC4, respectively. The L supplements left all five background hit sets unchanged. SD-Dendrochirotida and LD-Elasipodida used in separate assays cover 165/174 species in union. Adding F-Synallactida to the L assay raises exact matches from 30 to 37, with the same coverage.

[Counts by order](results/lineage_evaluation/by_order.csv) · [Species gained](results/lineage_evaluation/lineage_gain_species.csv) · [Background hits](results/lineage_evaluation/background_hits.csv) · [Methods and verification](results/lineage_evaluation/README.md)

[S pool FASTA](results/lineage_exploration/sd_pool.fasta) · [L pool FASTA](results/lineage_pool/ld_elasipodida.fasta)

<details>
<summary>Base matching at the supplemented S and L sites</summary>

![Original and supplementary S reverse-primer base matching](figures/base_matching_SD-Dendrochirotida.svg)

![Original and supplementary L forward-primer base matching](figures/base_matching_LD-Elasipodida.svg)

</details>

Licuanan and Matias previously described short echinoderm 12S and 16S candidate markers. [Reference](https://doi.org/10.56899/151.03.14)

## Marker complementarity and limited mismatches

Among the nine species missed by both 16S supplements, existing 12S XLD and SD together cover five in silico. COI XS/XSD also covers one of those five. Under a limited near-terminal mismatch scenario, LD-Elasipodida and COI XSD each gain one other target species. All four focal assays retain their strict background hit counts. [Species, mismatch rules and same-accession barcode comparisons](results/marker_complementarity/README.md)

## External reference evaluation

On 28 evaluable external 16S species per window, SD-Dendrochirotida covered 23 (82.1%) with zero exact matches, and LD-Elasipodida covered 16 (57.1%) with two exact matches. COI LD covered 13/15 species with one exact match. No external 12S target passed curation, and no external COI reference spanned both binding sites outside L/LD. The limited mismatch rule added one target each for 16S M, 16S MD and COI L. Neither Watson–Crick rule yielded a background hit among 142, 143 and 127 references for 16S, 12S and COI, respectively. [External panel, all assays and separate guanine–thymine background results](results/external_panel/README.md)

## Primer sequences and binding sites

Sequences are 5′→3′. Ordinary and D pairs for the same window share coordinates. The single 16S XS pair is listed on its own. The expanded tables use each window’s evaluable species panel. Strict background counts are listed as **Watson–Crick only / also allowing guanine–thymine pairing**.

<details>
<summary>16S · sequences, predicted matches and binding map</summary>

Background panel · 5,600 reference records

| Assay | F (5′–3′) | R (5′–3′) | Span (bp) | Covered | Exact | Strict off-target hits | Base matching |
|---|---|---|---:|---:|---:|---:|---|
| XS | `AACTTTGGTTGGGGYAAC` | `TTTCCCCAATCCAACATCGA` | 191 | 75/166 | 0/166 | 0 / 0 | [View](results/current_primers/XS/base_matching_XS.svg) |
| S | `CCAGAAAGACGAGAAGACCCTGTC` | `GAGGAGATAACGCTGTTATCCCTG` | 226 | 110/174 | 5/174 | 1 / 3 | [View](results/current_primers/S/base_matching_S.svg) |
| SD | `TAAGAAAGACGARAAGACCCTRTC` | `GAGAAGATGACGCTGTTATCCCTR` | 226 | 130/174 | 0/174 | 0 / 5 | [View](results/current_primers/S/base_matching_SD.svg) |
| M | `AAACTTCTATTAACGTGAAGAA` | `GTTATCCCTGCGGTAACT` | 245 | 55/174 | 9/174 | 0 / 2 | [View](results/current_primers/M/base_matching_M.svg) |
| MD | `AAACTTCTATTHAYGTGAAGAA` | `GTTATCCCTGCGGTAACT` | 245 | 89/174 | 24/174 | 0 / 15 | [View](results/current_primers/M/base_matching_MD.svg) |
| L | `AGACTCGTATGAACGGCAAAACCT` | `CGCTGTTATCCCTGCGGT` | 302 | 65/174 | 13/174 | 0 / 0 | [View](results/current_primers/L/base_matching_L.svg) |
| LD | `AGACTTGTATGAAYGGCRAAACMT` | `CGCTGTTATCCCTGCRGT` | 302 | 82/174 | 29/174 | 0 / 0 | [View](results/current_primers/L/base_matching_LD.svg) |
| XL | `GGTCACGCCTGCCCAGTGGA` | `AAGATAACGCTGTTATCCCTGCGGTAACTT` | 396 | 23/152 | 1/152 | 0 / 0 | [View](results/current_primers/XL/base_matching_XL.svg) |
| XLD | `GGTAACGCCTGCCCARTGGA` | `GAGATTACGCTGTTATCCCTGCGGTAACTD` | 396 | 43/152 | 3/152 | 0 / 10 | [View](results/current_primers/XL/base_matching_XLD.svg) |

![16S](figures/amplicon_regions.en.svg)

</details>

<details>
<summary>12S · sequences, predicted matches and binding map</summary>

Background panel · 438 reference records

| Assay | F (5′–3′) | R (5′–3′) | Span (bp) | Covered | Exact | Strict off-target hits | Base matching |
|---|---|---|---:|---:|---:|---:|---|
| XS | `AGATACCCTACTATACCCTTC` | `CGACGATGGTATACAAACTG` | 176 | 15/74 | 0/74 | 0 / 0 | [View](markers/12S_COI/figures/12S_XS.svg) |
| XSD | `AGATACCCTACTATACYYTTC` | `CGACGATGGTATACWRRCTG` | 176 | 21/74 | 9/74 | 0 / 0 | [View](markers/12S_COI/figures/12S_XSD.svg) |
| S | `AACACCAGAGCAGTACAGCT` | `CTGCACCTTGATCTGACGT` | 207 | 13/88 | 2/88 | 0 / 0 | [View](markers/12S_COI/figures/12S_S.svg) |
| SD | `AACACCAGAGYAGTACARCY` | `CTGCACCTTGATCTGRHGT` | 207 | 27/88 | 7/88 | 0 / 0 | [View](markers/12S_COI/figures/12S_SD.svg) |
| M | `AGGAGCTTGTCATTAAATTGAT` | `TTACTATCGAATCCTCTTTCAT` | 228 | 8/90 | 0/90 | 0 / 0 | [View](markers/12S_COI/figures/12S_M.svg) |
| MD | `AGGAGCTTGTCATYRAATYGAT` | `TTACTATCGAATCCTCTTTCWD` | 228 | 28/90 | 4/90 | 0 / 5 | [View](markers/12S_COI/figures/12S_MD.svg) |
| L | `AACACCAGAGCAGTACGGCT` | `GCGATGTGTGCGCATTCTAGAG` | 346 | 14/83 | 1/83 | 0 / 0 | [View](markers/12S_COI/figures/12S_L.svg) |
| LD | `AACACCAGAGYAGTACRGYT` | `GCGATGTGTGCRYATTYTAGAG` | 346 | 19/83 | 12/83 | 0 / 0 | [View](markers/12S_COI/figures/12S_LD.svg) |
| XL | `GGTGGTTAATAACGTGCCAG` | `CGACGATGGTATACAGGCTG` | 354 | 31/53 | 5/53 | 0 / 1 | [View](markers/12S_COI/figures/12S_XL.svg) |
| XLD | `GGTGGTTAATAACGTGCCAG` | `CGACGATGGTATACWRRCTG` | 354 | 33/53 | 7/53 | 0 / 1 | [View](markers/12S_COI/figures/12S_XLD.svg) |

![12S](markers/12S_COI/figures/positions_12S.en.svg)

</details>

<details>
<summary>COI · sequences, predicted matches and binding map</summary>

Background panel · 2,216 reference records

| Assay | F (5′–3′) | R (5′–3′) | Span (bp) | Covered | Exact | Strict off-target hits | Base matching |
|---|---|---|---:|---:|---:|---:|---|
| XS | `ACTATAGAGGAAAGCAAGAA` | `GCTGCTGTGAAGTAGGC` | 145 | 20/57 | 2/57 | 0 / 0 | [View](markers/12S_COI/figures/COI_XS.svg) |
| XSD | `ACTATAGAGGRAAGCMAGAR` | `GCTGCTGTRAAGTADGC` | 145 | 43/57 | 3/57 | 0 / 0 | [View](markers/12S_COI/figures/COI_XSD.svg) |
| S | `GAATGGTATACGCTATGGT` | `GTTTCTCAGACTAGCTTTG` | 193 | 10/55 | 0/55 | 0 / 0 | [View](markers/12S_COI/figures/COI_S.svg) |
| SD | `GAATGGTATAYGCWATGRT` | `GTTTCTCAGAYTARCTTKG` | 193 | 30/55 | 0/55 | 0 / 0 | [View](markers/12S_COI/figures/COI_SD.svg) |
| M | `CACTATAGAGGAAAGCAAGAACC` | `AACTTTGATCCTTGTAGGGT` | 218 | 9/55 | 0/55 | 0 / 0 | [View](markers/12S_COI/figures/COI_M.svg) |
| MD | `CACTATAGAGGWAAGMAAGARCC` | `AACTTTGATCCTTGTARNGT` | 218 | 25/55 | 3/55 | 0 / 0 | [View](markers/12S_COI/figures/COI_MD.svg) |
| L | `AAAATGCGAACCCCAGGAGTAAC` | `GGTTCTTGCTTTCCTCTGTAGTG` | 293 | 30/283 | 0/283 | 0 / 0 | [View](markers/12S_COI/figures/COI_L.svg) |
| LD | `AAAATGCGAACYCCAGGARTWAC` | `GGTTCTTGCTTWCCTCTRTARTG` | 293 | 103/283 | 11/283 | 0 / 2 | [View](markers/12S_COI/figures/COI_LD.svg) |
| XL | `ATGAACCTAAACCGCTGAT` | `CGTGGGCTATATTTCTTGA` | 415 | 11/62 | 0/62 | 0 / 0 | [View](markers/12S_COI/figures/COI_XL.svg) |
| XLD | `ATGAACCTAAAMCGYTGAY` | `CGTGGGCTATRTTTCTNGA` | 415 | 37/62 | 1/62 | 0 / 2 | [View](markers/12S_COI/figures/COI_XLD.svg) |

The XS and XSD internal reference barcode is 108 bp after primer removal.

![COI](markers/12S_COI/figures/positions_COI.en.svg)

</details>

## Evaluation and data

The 0–2 mismatch analysis separates exact matches from coverage gained by allowing mismatches. Full results include 15 internal-barcode identity matrices and predicted product lengths.

[Mismatch sensitivity, identity matrices and product lengths](results/anth28s_evaluation/README.md) · [16S common-panel and genus holdout results](results/computational_evaluation/README.md) · [12S and COI panels](markers/12S_COI/README.md) · [Methods](docs/METHODS.md) · [Reproduction](docs/REPRODUCIBILITY.md)

## Citation and permissions

Xia, F. (2026). *MiCucumber: in silico design and evaluation of mitochondrial primers for sea cucumber (Holothuroidea) eDNA metabarcoding*. Computational preprint v1.7. [GitHub Release](https://github.com/GUIBA-EX/MiCucumber/releases/tag/preprint-v1.7).

[Copyright](COPYRIGHT.md)

<details>
<summary>References</summary>

1. Gold, Z., Wall, A. R., Schweizer, T. M., et al. (2022). A manager’s guide to using eDNA metabarcoding in marine ecosystems. *PeerJ*, 10, e14071. https://doi.org/10.7717/peerj.14071

2. Miya, M., Sato, Y., Fukunaga, T., et al. (2015). MiFish, a set of universal PCR primers for metabarcoding environmental DNA from fishes: detection of more than 230 subtropical marine species. *Royal Society Open Science*, 2, 150088. https://doi.org/10.1098/rsos.150088

3. Hamamoto, K., Soliman, T., Poliseno, A., Fernandez-Silva, I., & Reimer, J. D. (2021). Higher genetic diversity of the common sea cucumber *Holothuria (Halodeima) atra* in marine protected areas of the central and southern Ryukyu Islands. *Frontiers in Conservation Science*, 2, 736633. https://doi.org/10.3389/fcosc.2021.736633

4. Katoh, K., & Standley, D. M. (2013). MAFFT multiple sequence alignment software version 7: improvements in performance and usability. *Molecular Biology and Evolution*, 30, 772–780. https://doi.org/10.1093/molbev/mst010

5. Untergasser, A., Cutcutache, I., Koressaar, T., et al. (2012). Primer3—new capabilities and interfaces. *Nucleic Acids Research*, 40, e115. https://doi.org/10.1093/nar/gks596

6. Riaz, T., Shehzad, W., Viari, A., et al. (2011). ecoPrimers: inference of new DNA barcode markers from whole genome sequence analysis. *Nucleic Acids Research*, 39, e145. https://doi.org/10.1093/nar/gkr732


7. Uthicke, S., Byrne, M., & Conand, C. (2010). Genetic barcoding of commercial Bêche-de-mer species (Echinodermata: Holothuroidea). *Molecular Ecology Resources*, 10(4), 634–646. https://doi.org/10.1111/j.1755-0998.2009.02826.x

8. Hoareau, T. B., & Boissin, E. (2010). Design of phylum-specific hybrid primers for DNA barcoding: addressing the need for efficient COI amplification in the Echinodermata. *Molecular Ecology Resources*, 10(6), 960–967. https://doi.org/10.1111/j.1755-0998.2010.02848.x

9. Byrne, M., Rowe, F., & Uthicke, S. (2010). Molecular taxonomy, phylogeny and evolution in the family Stichopodidae (Aspidochirotida: Holothuroidea) based on COI and 16S mitochondrial DNA. *Molecular Phylogenetics and Evolution*, 56(3), 1068–1081. https://doi.org/10.1016/j.ympev.2010.04.013

10. Wen, J., Hu, C., Zhang, L., Luo, P., Zhao, Z., Fan, S., & Su, T. (2010). The application of PCR–RFLP and FINS for species identification used in sea cucumbers (Aspidochirotida: Stichopodidae) products from the market. *Food Control*, 21(4), 403–407. https://doi.org/10.1016/j.foodcont.2009.06.014

11. Wen, J., Hu, C., Zhang, L., & Fan, S. (2011). Genetic identification of global commercial sea cucumber species on the basis of mitochondrial DNA sequences. *Food Control*, 22(1), 72–77. https://doi.org/10.1016/j.foodcont.2010.06.010

12. Xing, R.-R., Hu, R.-R., Wang, N., Zhang, J.-K., Ge, Y.-Q., & Chen, Y. (2021). Authentication of sea cucumber products using NGS-based DNA mini-barcoding. *Food Control*, 129, 108199. https://doi.org/10.1016/j.foodcont.2021.108199

</details>
