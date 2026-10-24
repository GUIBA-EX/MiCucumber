# File index

[中文](FILES.zh-CN.md) · [Overview](../README.md) · [Naming](NAMING.md) · [Methods](METHODS.md) · [Reproduction](REPRODUCIBILITY.md)

Obtain primers from `sequences/`, compare performance in `results/`, and follow the reproduction guide to rerun calculations.

| Path | Contents |
|---|---|
| [sequences/primer_pairs.csv](../sequences/primer_pairs.csv) | All 17 paired reaction entries, covering 13 portfolios |
| [sequences/primers.fasta](../sequences/primers.fasta) | 34 forward/reverse sequence entries |
| [sequences/](../sequences/) | CSV and FASTA exports by region, plus S-original |
| [results/comparison.csv](../results/comparison.csv) | 13 portfolios × common and own-region panels (26 rows) |
| [results/degenerate/](../results/degenerate/) | Single-pair selection, missed taxa, background hits and thermodynamics |
| [results/nondegenerate/](../results/nondegenerate/) | Concrete candidates, selection audit, matching and validation |
| [results/matching/](../results/matching/) | 21 matching profiles and 7,371 per-reference states |
| [results/reproduction_checks.json](../results/reproduction_checks.json) | Computational reproduction results |
| [figures/](../figures/) | Overview illustration, matching heatmaps, region plots and coordinates |
| [report.html](../report.html) | Bilingual report; download and open locally |
| [scripts/check_release.py](../scripts/check_release.py) | Check exported sequences, metrics, links and hashes |
| [scripts/reproduce.py](../scripts/reproduce.py) | Run the frozen analysis workflows |
| [scripts/plot_matching.py](../scripts/plot_matching.py) | Generate matching summaries and heatmaps |
| [scripts/plot_regions.py](../scripts/plot_regions.py) | Generate reference-region plots |
| [reproducibility/frozen/](../reproducibility/frozen/) | Reference data and analysis input bundles |
| [docs/name_mapping.csv](../docs/name_mapping.csv) | Sequence provenance and identifier mapping |
| [archive/](../archive/) | Archived analysis snapshot |
| [SHA256SUMS.json](../SHA256SUMS.json) | Published file SHA-256 fingerprints |
| [COPYRIGHT.md](../COPYRIGHT.md) | Copyright and reuse terms |
