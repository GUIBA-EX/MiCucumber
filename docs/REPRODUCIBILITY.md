# Reproduction

[中文](REPRODUCIBILITY.zh-CN.md) · [Methods](METHODS.md) · [Naming](NAMING.md)

## Check the published files

From the repository root:

```bash
python scripts/check_release.py
```

This requires only the Python standard library. It checks 13 portfolios, region/type/count consistency, 17 reaction rows, 34 FASTA records, A/C/G/T-only nondegenerate sequences, the unchanged original control, source-to-current name/sequence/metric invariance, expected screening limits, Markdown/HTML links, ZIP integrity and file hashes. It does not rerun binding scans.

## Computational reproduction

Use Python 3.12 and install the frozen analysis dependencies. The nondegenerate and round-two routes also need a C++17 compiler (`c++`, or `CXX` where the underlying runner supports it).

```bash
python -m pip install -r requirements.txt
python scripts/reproduce.py degenerate --work-dir reproduction-work
python scripts/reproduce.py nondegenerate --work-dir reproduction-work
```

The two modes use separate subdirectories. For a repeat run, provide a fresh `--work-dir`; existing reproduction folders are not overwritten. No network is required after installing dependencies. Original input bundles remain unchanged.

- **Degenerate:** rerun exhaustive 1–4-pair subset calculations from frozen per-pair target/background evidence, export the four current single-pair degenerate portfolios, normalize names, and compare sequences and common/own-region metrics against published tables. This route does not rescan raw reference sequences or rediscover candidate sites. Current-name outputs are under `degenerate/current-results/`.
- **Nondegenerate:** re-enumerate 2,644 concrete candidates; optimize one-/two-pair subsets; compile and run the independent whole-sequence target/background scanner; compare predictions; retain the original control; normalize final exports and check sequences and metrics. Current-name outputs are under `nondegenerate/current-results/`.
- **Round-two upstream scan:** `python scripts/reproduce.py round2 --work-dir reproduction-work` runs the frozen independent reference revalidation. It retains source identifiers in intermediate evidence and does not itself emit the 13 current portfolios.

## Inputs and outputs

Frozen bundles supply reference data and analysis inputs. `scripts/naming.py` maps output identifiers to current names. Analysis results are written to the degenerate and nondegenerate modes’ `current-results/` directories; sequence and metric verification is recorded in [reproduction checks](../results/reproduction_checks.json).

## Region figures

```bash
python -m pip install -r requirements-plot.txt
python scripts/plot_regions.py
python scripts/plot_regions.py --cjk-font /path/to/CJK-font.ttf
```

Running `plot_regions.py` without a font option generates English PNG/SVG/PDF. Supplying a suitable installed Chinese font generates both languages. Coordinate inputs are in `figures/region_coordinates.csv`; the figure shows seed windows, not empirical product-length distributions. Refresh the file-hash manifest when publishing regenerated figures.

## Matching plots

Run `python scripts/plot_matching.py` after installing `requirements-plot.txt`. It uses frozen `results/matching/panel.csv` and `pair_hits.csv`, generates per-reference states and weighted summaries, and verifies all common-panel portfolio metrics.
