# Reference-insert resolution

`resolution.csv` counts unique, unambiguous primer-free insert sequences attributable to one species, genus or family. Each rank uses the distinct inserts for which every contributing record has an assigned label. `collisions.csv` lists distinct inserts shared by multiple species. `target_inserts.csv` records matched original sequences before the COI taxonomic reconciliation. COI resolution uses exact species-level matches from `worms_results.json` and accepted names; 16S uses the frozen curated labels.

All qualifying records participate, including multiple records per species. These are reference-library statistics and do not estimate laboratory identification accuracy.
