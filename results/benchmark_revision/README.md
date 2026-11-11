# Candidate comparison and barcode resolution

The tables use the frozen MiCucumber v1.7 reference panels. Run the following from the repository root with the existing Python and primer3-py dependencies.

```sh
python3 results/benchmark_revision/analyze.py
```

- [Marker comparisons](marker_comparison.csv) give each released 12S and COI assay on its available panel, the XS–M intersection, and the five-window intersection for each gene. Known synonyms are merged. Each species is represented by the accession evaluable in the most windows, with longer sequences and then accession order breaking ties. Target denominators retain all binding-evaluable species in the selected panel. Covered-and-unique additionally requires an unambiguous insert assigned to one species in the full usable barcode library for that window.
- [16S resolution](resolution_by_rank.csv) and [shared inserts](barcode_collisions_by_rank.csv) use the complete usable reference set for each window. Each distinct insert contributes one observation. Genera follow the curated species names. Families use the frozen GBIF species records and, where necessary, the unique family observed for that genus in the same records.
- [Changes under limited terminal mismatch](limited_mismatch_changes.csv) reproduce the focal design-panel gains and all external gains. Listed F/R positions are compatible with at least one valid paired product. Position −1 is the terminal 3′ base. Background counts compare the two Watson–Crick rules within the corresponding panel.
- [Other echinoderm classes](near_relative_background.csv) stratifies the original 12S and COI background by accession lineage. These records participated in the original screen. The held-out background comparison is reported separately in the manuscript.
