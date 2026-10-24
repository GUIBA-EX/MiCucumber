# Reproduction

[中文](REPRODUCIBILITY.zh-CN.md) · [Methods](METHODS.md) · [Naming](NAMING.md)

## Check the published files

From the repository root:

```bash
python scripts/check_release.py
```

This requires only the Python standard library. It checks 17 portfolios, region/type/count consistency, 25 reaction rows, 50 FASTA records, A/C/G/T-only ND sequences, the unchanged original control, source-to-current name/sequence/metric invariance, expected screening limits, Markdown/HTML links, ZIP integrity and file hashes. It does not rerun binding scans.

## Computational reproduction

Use Python 3.12 and install the frozen analysis dependencies. The nondegenerate and round-two routes also need a C++17 compiler (`c++`, or `CXX` where the underlying runner supports it).

```bash
python -m pip install -r requirements.txt
python scripts/reproduce.py degenerate --work-dir reproduction-work
python scripts/reproduce.py nondegenerate --work-dir reproduction-work
```

The two modes use separate subdirectories. For a repeat run, provide a fresh `--work-dir`; existing reproduction folders are not overwritten. No network is required after installing dependencies. Original input bundles remain unchanged.

- **Degenerate:** rerun exhaustive 1–4-pair subset calculations from frozen per-pair target/background evidence, select the eight current one-/two-pair portfolios, normalize names, and compare sequences and common/own-region metrics against published tables. This route does not rescan raw reference sequences or rediscover candidate sites. Current-name outputs are under `degenerate/current-results/`.
- **Nondegenerate:** re-enumerate 2,644 concrete candidates; optimize one-/two-pair subsets; compile and run the independent whole-sequence target/background scanner; compare predictions; retain the original control; normalize final exports and check sequences and metrics. Current-name outputs are under `nondegenerate/current-results/`.
- **Round-two upstream scan:** `python scripts/reproduce.py round2 --work-dir reproduction-work` runs the frozen independent reference revalidation. It retains source identifiers in intermediate evidence and does not itself emit the 17 current portfolios.

The current-name degenerate and nondegenerate adapters were rerun during this reorganization. Their selected sequences and metrics agree with the pre-renaming results; see [reproduction checks](../results/reproduction_checks.json). The round-two frozen bundle retains its earlier revalidation evidence; its computation was not changed by this update.

## Historical identifiers and archives

Files in `reproducibility/frozen/` retain the source identifiers required by the original pipelines. `scripts/naming.py` maps exported identifiers exactly once; it does not modify reference sequences, risk models or scores. Legacy intermediate reports produced inside reproduction folders are historical working outputs; use `current-results/` and the repository's current report for renamed results.

`archive/pre-renaming-14f156f.zip` is the complete prior tracked repository. Its `revalidate.py`, historical check scripts and original multi-pair recommendations are scoped to that archived snapshot. They are not current root-level commands. Existing Git tags are unchanged.

## Region figures

```bash
python -m pip install -r requirements-plot.txt
python scripts/plot_regions.py
python scripts/plot_regions.py --cjk-font /path/to/CJK-font.ttf
```

The first command generates English PNG/SVG/PDF. Supplying a suitable installed Chinese font generates both languages. Coordinate inputs are in `figures/region_coordinates.csv`; the figure shows seed windows, not empirical product-length distributions. A figure regeneration may change binary hashes across fonts or plotting environments; do not treat regenerated binaries as the original frozen release without refreshing its manifest.

## Scientific limits

Reproduction verifies computation from frozen inputs, not biological accuracy, independent holdout performance or wet-lab PCR performance. No fresh database retrieval, complete de novo rediscovery, or validated single-tube multiplex recipe is implied.
