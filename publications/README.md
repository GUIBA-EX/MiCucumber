# MiCucumber preprint

Author: Fei Xia. Computational preprint; not peer reviewed.

[PDF](MiCucumber_preprint.pdf) · [Manuscript](MiCucumber_preprint.md) · [Versioned releases](https://github.com/GUIBA-EX/MiCucumber/releases)

## Reproduction

Install Pandoc, Google Chrome or Chromium, Python 3 and Poppler. Set `CHROME` to the browser executable when needed. From the repository root:

```sh
python3 publications/build_preprint.py
python3 publications/check_preprint.py
python3 scripts/preprint_integrity.py
```

Pushes to `main` check for changes in research inputs and publication sources. A changed input triggers PDF rendering, sequence and result-table checks, checksum verification, a version commit and an immutable tagged GitHub Release containing the PDF, primer FASTA and checksums. Failed checks stop publication. Manuscript interpretations must be updated with the underlying results; the workflow does not generate scientific conclusions.
