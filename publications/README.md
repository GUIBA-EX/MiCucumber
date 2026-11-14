# MiCucumber manuscript

Fei Xia · The University of Tokyo · xf@g.ecc.u-tokyo.ac.jp

[Manuscript PDF](submission/MiCucumber_revision.pdf) · [Editable Word](submission/MiCucumber_revision.docx) · [Markdown](submission/MiCucumber_revision.md) · [Supplementary PDF](submission/Supplementary.pdf)

## Supporting files

- [Online Resource 1](submission/ESM_1.xlsx) contains 29 baseline primer pairs and original panel summaries.
- [Online Resource 2](submission/ESM_2.xlsx) contains all 61 oligonucleotides.
- [Online Resource 3](submission/Supplementary.pdf) contains Figs. S1–S5.
- [Fig. 1 A4](submission/figures/Fig1_A4.pdf) displays five 16S windows and [31 representatives](submission/figures/Fig1_representatives.csv).
- [Cover letter](submission/Cover_letter.docx) is the editable submission draft.

## Reproduction

Run python scripts/check_review.py from the repository root. Current analyses are documented in [scripts/review](../scripts/review/README.md). Figure inputs are retained in [results/visualization](../results/visualization/). Run python scripts/render_submission_figures.py with NumPy, Matplotlib and Pillow to reproduce the main figures and Fig. S5. Arial is used when installed.

Run python publications/submission/build_docx.py with Pandoc and python-docx to rebuild editable documents from Markdown. Export the resulting Word files to PDF and inspect pagination before replacing the checked PDFs. Fig. 1 occupies a full page and its caption follows on the next page.

The files directly under this directory retain the earlier v1.8 release and its build scripts. Current files are indexed in [PROJECT_FILES.md](../PROJECT_FILES.md). Checksums are in [SHA256SUMS_revision.txt](submission/SHA256SUMS_revision.txt).
