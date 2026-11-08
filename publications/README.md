# MiCucumber preprint

**Fei Xia** · Computational preprint; not peer reviewed.

[PDF](MiCucumber_preprint.pdf) · [Manuscript](MiCucumber_preprint.md) · [Versioned releases](https://github.com/GUIBA-EX/MiCucumber/releases) · [Citation](../CITATION.cff)

## Build and validate

The preprint integrates the [mismatch, product-length and sequence-identity analyses](../results/anth28s_evaluation/README.md), with six diagnostic figures and source-generated Tables 8–9. All 29 primer pairs and 58 oligonucleotides are retained.

Install Python 3, Pandoc, Poppler and Google Chrome or Chromium. Set `CHROME` to the browser executable when needed. Run from the repository root:

```sh
python3 -m pip install -r publications/requirements-preprint.txt biopython
python3 publications/build_preprint.py
python3 publications/check_preprint.py
python3 scripts/check_release.py
python3 scripts/check_publication.py
python3 scripts/preprint_integrity.py
```

## Automatic updates

Pushes to `main` and manual workflow runs check the committed research results and publication files. Changes to README editions, citations, data, figures, publication sources or release scripts trigger a new minor preprint version. The workflow stamps all editions using Asia/Shanghai time, rebuilds the PDF, checks scientific tables and primer sequences, validates publication metadata and links, and verifies checksums before creating a tagged GitHub Release. A run with no relevant changes validates the existing version without creating a new one.

The release contains the PDF, matching primer FASTA and SHA-256 checksums. Existing public releases remain unchanged. Relative links in the PDF point to the matching source tag. Scientific analyses and their interpretations are maintained in the source files; the workflow rebuilds the paper from those committed results.

## Consistency checks

`release.json` holds the title, version, date, README editions and primer FASTA path. `scripts/stamp_preprint.py` synchronizes the manuscript and citation formats. `scripts/check_publication.py` verifies metadata, local links, visible figure captions and every oligo in the PDF and manuscript. The builder regenerates Tables 1–7 from the current scientific CSV files and copies the current 12S and COI position figures. Checks verify every generated table and both figure copies against their sources. `publication_check.json` records the checked version, page and oligo counts, and output hashes.
