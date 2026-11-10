# Marker complementarity and limited mismatch sensitivity

## Species missed by both 16S supplements

The 16S S/L union covers 165 of 174 reference species. This targeted comparison uses the nine missed species, with a usable representative in at least one existing 12S window and one COI window for each species. It retains the 16S order labels across markers. The accepted name *Chiridota hydrothermica* is matched to the source name *C. heheva* following [WoRMS AphiaID 242132](https://www.marinespecies.org/aphia.php?p=taxdetails&id=242132). Accession matches are reported separately from species-name matches.

| Species | Order | 12S compatible assays | COI compatible assays |
| --- | --- | --- | --- |
| *Chiridota hydrothermica* | Apodida | — | — |
| *Chiridota laevis* | Apodida | — | — |
| *Euapta godeffroyi* | Apodida | — | — |
| *Protankyra bidentata* | Apodida | XLD | — |
| *Protankyra verrilli* | Apodida | XLD | — |
| *Ocnus glacialis* | Dendrochirotida | XL, XLD | XS, XSD |
| *Peniagone diaphana* | Elasipodida | — | — |
| *Gephyrothuria alcocki* | Persiculida | SD | — |
| *Paroriza prouhoi* | Persiculida | SD, MD | — |

The 12S XLD and SD assays together add five species. COI XS/XSD also covers *O. glacialis*, already added by 12S. None of these newly compatible assay–species matches was an exact paired match. Dashes indicate that no released assay at that locus covered the species under the strict model. The [accession-level results](missed_species.csv) list the evaluable assays for each species.

## Limited relaxation

Both models allow up to two Watson–Crick mismatches per oligo. The strict model requires compatibility at all three terminal bases. The limited model retains compatibility at the last 3′ base and allows one mismatch across the entire pair at positions −2 or −3. All other size and pairing rules are unchanged. The scenario was motivated by planned KOD One use and a target of at least 500,000 reads. It has no polymerase-specific calibration. Sequencing depth affects sampling of amplicons that were generated.

| Marker and assay | Target, strict → limited | Background, strict → limited |
| --- | --- | --- |
| 16S SD-Dendrochirotida | 155 → 155 / 174 | 0 → 0 / 5,600 |
| 16S LD-Elasipodida | 97 → 98 / 174 | 0 → 0 / 5,600 |
| 12S XLD | 33 → 33 / 53 | 0 → 0 / 438 |
| COI XSD | 43 → 44 / 57 | 0 → 0 / 2,216 |

The added 16S L match is *Cucumaria georgiana*, already covered by S. The added COI match is *Actinopyga lecanora*. Neither is among the original nine misses. [Counts](mismatch_sensitivity.csv) · [Added accessions](added_hits.csv)

## Reference barcode collisions

Six distinct pairs of species share an identical 16S insert in at least one window. Only one pair had both alternate-marker inserts available on the same accessions used for 16S. *Scotoplanes clarki* and *Protelpidia murrayi* had different inserts with both species predicted compatible for 12S XL/XLD and COI XSD/MD. The remaining exact-collision pairs and the eight distinct one-edit nearest-neighbor pairs lacked a matched-accession alternate-marker comparison in these frozen panels. [Results by window and accession](paired_barcode_collisions.csv)

## Reproduction

Run `python3 results/marker_complementarity/compare.py` with the repository's `requirements.txt` dependencies. The script reconciles all twenty 12S/COI strict target counts with the existing tables. It independently rescans strict and limited compatibility for the four focal schemes and checks strict accession sets against the frozen results. The matched-accession collision analysis is separate from species-name matching for missing coverage.
