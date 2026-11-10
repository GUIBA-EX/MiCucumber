# MiCucumber 12S and COI candidate assays

The NCBI snapshot comprises 6,168 distinct accessions. Each locus has its own design panel. The 12S panel contains 90 species from 344 eligible records and the COI panel contains 357 species from 5,681 records. Backgrounds contain 438 reference records for 12S and 2,216 for COI. The COI background includes an expanded set of marine animal references. See the downloads, per-locus FASTA files and sequence audit for accession-level provenance. Order names follow the GenBank source taxonomy.

Window names indicate relative lengths within each gene; current spans and reference endpoints are listed in each locus’s pairs.csv. Within each retained window, ordinary primers are selected from concrete realizations of the D pair at identical reference endpoints. Each oligonucleotide has ≤8 variants, with ambiguity in the 3′ half. The target scan requires a 100–500 bp product, at least 50 internal bases, at most two mismatches per end and compatible terminal three bases. Background scans allow 0–1,000 internal bases. Strict models each admit at most ten background species and relaxed models at most fifty. Frozen scans are rechecked with an independent seed-and-extend implementation. Ordinary and degenerate alternatives are evaluated as separate assays.

Recheck retained assays with `python3 scripts/final_check.py` from this directory (Biopython and primer3-py). For the full search, run scripts/design.py separately for each gene, compile scripts/raw_scan.cpp with a C++17 compiler and invoke it on the gene directory. Repeat under extended/ using the same frozen alignments and FASTA files. Then run scripts/pairs.py for each gene. Final verification needs only the frozen inputs provided here.

### Search and selection record

The two searches evaluated 834 primer pairs for 12S and 1,050 for COI after the thermal gate. Within each length class, the 12S choice maximizes exact matches among pairs reaching at least 80% of the best passing coverage count. COI first retains windows within 95% of the largest evaluable denominator and then maximizes covered species. See the [12S search audit](12S/screening_audit.csv) and [COI search audit](COI/screening_audit.csv). Raw accession and alignment integrity checks run with `python3 scripts/check_data.py`. Reference order names include historical GenBank classifications.

COI XS and XSD use a 145 bp reference span (779–923 on AB525437.1), including a 108 bp internal sequence. Each shares the same F 779–798 and R 907–923 coordinates. Their respective coverage is 20/57 and 43/57, with two and three exact paired matches. Both strict background models return zero hits. The per-window metrics in candidates.csv use the frozen background FASTA supplied with each locus.

Compared with the preceding pairs on the common panel, coverage increased overall. Five formerly covered species per assay were missed:

- **XS:** *Holothuria hilla*, *Isostichopus badionotus*, *I. fuscus*, *Phyllophorella liuwutiensis* and *Neocucumis proteus*.
- **XSD:** *Actinopyga lecanora*, *Benthodytes marianensis*, *B. gosarsi*, *Holothuria pervicax* and *Laetmogone violacea*.
