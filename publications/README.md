# MiCucumber preprint

**Fei Xia** · Computational preprint

[PDF](MiCucumber_preprint.pdf) · [Manuscript](MiCucumber_preprint.md) · [Versioned releases](https://github.com/GUIBA-EX/MiCucumber/releases) · [Citation](../CITATION.cff)

## Build and validate

The [mismatch, product-length and sequence-identity analyses](../results/anth28s_evaluation/README.md) supply six diagnostic figures and Tables 8–9. The [16S lineage evaluation](../results/lineage_evaluation/README.md) supplies the S/L gains and order-level tables, two base-matching figures and the independent checks. The [external reference evaluation](../results/external_panel/README.md) supplies Table 12 and the full accession-level results. The [candidate comparison and resolution analysis](../results/benchmark_revision/README.md) supplies Tables 13–15 and the class-specific background counts.

Install Python 3, Pandoc, Poppler and Google Chrome or Chromium. Set `CHROME` to the browser executable when needed. Run from the repository root:

```sh
python3 -m pip install -r publications/requirements-preprint.txt biopython primer3-py==2.4.0
python3 results/benchmark_revision/analyze.py
python3 publications/build_preprint.py
python3 publications/check_preprint.py
python3 scripts/check_release.py
python3 scripts/check_publication.py
python3 scripts/preprint_integrity.py
```

## Automatic updates

Pushes to `main` and manual workflow runs check the committed research results and publication files. Changes to README editions, citations, data, figures, publication sources or release scripts trigger a new minor preprint version. The workflow stamps all editions using Asia/Shanghai time, rebuilds the PDF, checks scientific tables and primer sequences, validates publication metadata and links, and verifies checksums before creating a tagged GitHub Release. A run with no relevant changes validates the existing version without creating a new one.

The release contains the PDF, the baseline primer FASTA, the two selected 16S lineage supplement FASTAs and SHA-256 checksums. Relative links in the PDF point to the matching source tag. The workflow rebuilds the paper from the committed results.

## Consistency checks

`release.json` holds the title, version, date, README editions and baseline and supplementary FASTA paths. `scripts/stamp_preprint.py` synchronizes the manuscript and citation formats. `scripts/check_publication.py` verifies metadata, local links, visible figure captions and the baseline oligos in the PDF and manuscript. The builder regenerates Tables 1–15 from the current scientific CSV files and copies the current 12S and COI position figures. Checks verify every generated table and both figure copies against their sources. `publication_check.json` records the checked version, page and oligo counts, and output hashes.
