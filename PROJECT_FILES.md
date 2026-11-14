# MiCucumber project files

- `README.md` and `README.zh-CN.md` introduce the current working revision.
- `sequences/all_testing_primers.fasta` and `sequences/all_testing_primers.csv` contain the complete set of 29 baseline pairs and three supplemental oligonucleotides. `sequences/detailed_assays.fasta` contains the eight oligonucleotides in the three detailed comparisons. `sequences/all_markers.fasta` and the marker tables retain the earlier released catalogue.
- `figures/MiCucumber_overview_current.png` is the current README banner.
- `publications/submission/` holds the revised manuscript, supplementary material, figures and editable-document build script. The files directly under `publications/` are the published v1.8 preprint and its build metadata.
- `results/complementarity/`, `results/specificity/` and `results/resolution/` contain the current matching, MIDORI2 and resolution results.
- `scripts/review/` contains the analysis scripts and execution instructions. `scripts/check_review.py` checks the current working revision.
- `report.html`, `results/`, `markers/`, `reproducibility/`, `archive/` and `docs/` also contain the earlier report, frozen v1.8 source data and earlier analyses. `SHA256SUMS.json` is the v1.8 manifest; use `publications/submission/SHA256SUMS_revision.txt` for the current working revision.
- `work/review/` contains local downloaded databases, generated alignments and intermediate files. It is excluded from Git. MIDORI2 release details and checksums are recorded in `results/specificity/manifest.json`.
- `CITATION.cff`, `CITATION.bib` and the published-release link identify v1.8. The current manuscript is a working revision.

The results/visualization directory contains the aligned inserts and ordinary 16S S comparison used in the current figures.
