# External reference evaluation

This evaluation uses GenBank accessions outside the documented MiCucumber design and screening inputs. It tests 29 released pairs and four 16S lineage schemes with the existing sequences and coordinates.

| Marker | Target species retained | Evaluable target species per assay | Background accessions |
| --- | ---: | ---: | ---: |
| 16S | 31 | 21–30 | 142 |
| 12S | 0 | NA | 143 |
| COI | 17 | 15 for L/LD, NA for other windows | 127 |

## Reference selection

The [GenBank searches](query_manifest.json) and [511 fetched candidate accessions](candidate_sources.json) were frozen on 11 November 2026. We excluded accession stems found in the four archived design bundles, the 12S/COI download manifest and available earlier design and challenge files. We also excluded strand-normalized exact sequence duplicates and identical contained fragments spanning at least 85% of the longer sequence. The inventory covers 230 documented inputs, with 16,597 accession stems and 13,712 distinct canonical sequences.

We required an explicit mitochondrial annotation and a named species. Background references required a fully annotated marker from a mitochondrial record at least 12 kb long. Within a species and marker, we selected one accession by feature completeness, decreasing length, increasing ambiguous-base count and accession order. Selection preceded all primer scans. Some external accessions represent species already present in the design panels. The background contains five major groups and no other echinoderm classes after these filters. It measures compatibility with the sampled background.

Target fragments were added to the frozen reference alignments with MAFFT 7.526. Both binding intervals had to be spanned by concrete bases. For 16S we also required at least 90% of the reference-site bases in each interval. Missing intervals produce an empty rate when no targets are evaluable. COI fragments outside the XS, S, M and XL binding intervals contribute no denominator for those windows.

## Matching rules and results

- **Exact** requires compatible bases at both full sites using Watson–Crick pairing and IUPAC alternatives.
- **Strict** allows up to two mismatches per oligo and requires compatibility in the final three 3′ bases of each oligo.
- **Limited** retains the two-mismatch-per-oligo ceiling and allows one mismatch in total at position 2 or 3 from either 3′ end. The last base of each oligo must still be compatible.
- **Strict with guanine–thymine pairing** is a separate background check. Product and insert bounds follow the released geometry.

16S SD-Dendrochirotida covered 23/28 species (82.1%), with 0/28 exact. LD-Elasipodida covered 16/28 (57.1%), with 2/28 exact. Separate S and L assays together covered 25/27 species with both windows evaluable. The limited rule added one target each for 16S M, 16S MD and COI L. No background accession matched either Watson–Crick coverage rule. The separate guanine–thymine model produced three hits for 16S S and one each for 16S XLD and COI XSD.

- [All 33 assay summaries](summary.csv), [per-accession predictions](predictions.csv), [background by group](background_by_group.csv) and [S/L union on shared targets](separate_assay_union.csv)
- [Selected accessions and extraction intervals](panel.csv), [selection audit](selection_audit.csv), [historical accessions](historical_accessions.txt), [historical input hashes](historical_inputs.json) and [curation provenance](curation_provenance.json)
- Frozen target and background FASTAs are in this directory. `12S_target.fasta` is deliberately empty.

## Reproduce the scores

From the repository root, use Python 3, `primer3-py`, MAFFT 7.526 and a C++17 compiler. The scoring replay uses the frozen FASTAs without network access.

```sh
python3 results/external_panel/evaluate.py
```

The C++ scanner and Python matcher agreed on the strict and exact Watson–Crick calls across all 5,119 assay–accession comparisons. The panel files and query audit permit inspection of the source records. Repeating the original historical exclusion index also requires the earlier local inputs listed in the hash inventory.
