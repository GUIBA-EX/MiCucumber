# MiCucumber 16S S/L lineage supplements

S and L supplements share all binding coordinates with their baseline pairs. The 174-species S/L panel and the 151-species five-window intersection each contain one representative per species. A covered species has at least one valid paired product with no more than two mismatches per oligonucleotide and compatible final three 3′ bases. Exact matches require zero mismatches in both oligonucleotides. The S and L union refers to separate assays.

| Scheme | Added oligo | Predicted coverage | Paired exact | Added background records¹ |
| --- | --- | ---: | ---: | ---: |
| SD-Dendrochirotida | R-Dendrochirotida | 130 → 155 / 174 | 0 → 1 / 174 | 0 / 0 / 0 / 1 / 20 |
| LD-Elasipodida | F-Elasipodida | 82 → 97 / 174 | 29 → 29 / 174 | 0 / 0 / 0 / 0 / 0 |
| LD-Synallactida | F-Synallactida | 82 → 104 / 174 | 29 → 36 / 174 | 0 / 0 / 0 / 0 / 0 |
| LD-Synallactida-Elasipodida | Both F oligos | 82 → 119 / 174 | 29 → 36 / 174 | 0 / 0 / 0 / 0 / 0 |

¹ Strict Watson–Crick only, strict also allowing guanine–thymine pairing, relaxed WC3, GT2 and WC4, in that order. The strict models retain the terminal-three constraint. The relaxed models drop it, with respective limits of 3, 2 and 4 mismatches per oligonucleotide. Background counts use 5,600 frozen accession records. The LD baseline and all three L supplements each have 1,015 WC4 hits.

- [Overall metrics](summary.csv) and [metrics by order](by_order.csv) give coverage, paired exact matching and primer-free barcode resolution for both panels. Barcode uniqueness is assessed against all unambiguous reference inserts for that window. `covered_unique` counts species that are both covered and unique. `barcode_nearest_one` counts species whose nearest other-species barcode is at edit distance one.
- [Marginal gains](lineage_gains.csv), [species gained](lineage_gain_species.csv), [separate-assay union](separate_assay_union.csv) and [background accession flags](background_hits.csv) retain the underlying counts and identities.
- [Variant observations](lineage_variants.csv) count exact matches to each concrete oligo variant at its homologous binding site, regardless of the partner match. [Illustrated templates](matching_examples.csv) list the examples shown in the [S base-matching diagram](../../figures/base_matching_SD-Dendrochirotida.svg) and [L base-matching diagram](../../figures/base_matching_LD-Elasipodida.svg). Bases are displayed in primer orientation.

Run from the repository root with the dependencies in `requirements.txt`:

```sh
python3 results/lineage_evaluation/analyze.py
python3 results/lineage_evaluation/plot_matching.py
python3 results/lineage_evaluation/verify_lineages.py
```

The summary checks its baseline counts against the existing common-panel results. The independent verifier scans the original target and background sequences using regex seeds and compares exact, covered and background accession sets for every scheme. [Input hashes](comparison_checks.json) · [Independent checks](independent_checks.json).
