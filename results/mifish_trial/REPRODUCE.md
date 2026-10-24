# Reproduce this trial

Extract analysis_sources.zip into an empty directory, preserving its paths. Use Python 3.12 with numpy, biopython and primer3-py, plus a C++17 compiler.

```sh
c++ -O3 -std=c++17 work/micucumber_mifish/specific/scan_sites.cpp -o work/micucumber_mifish/specific/scan_sites
c++ -O3 -std=c++17 work/micucumber_nondegenerate/independent_scan.cpp -o work/micucumber_nondegenerate/independent_scan
python3 work/micucumber_mifish/specific/prepare.py
work/micucumber_mifish/specific/scan_sites work/micucumber_mifish/specific
python3 work/micucumber_mifish/specific/optimize_pairs.py
python3 work/micucumber_mifish/specific/verify_selected.py
python3 work/micucumber_mifish/specific/svg_plot.py
python3 work/micucumber_mifish/specific/report.py
```

Candidate generation and selection use aligned windows. Reported final metrics use the independent full-sequence scanner. The search is bounded to the stated windows and candidate variants; it does not prove a global optimum. Two-pair results represent separate PCR unions. The final report recommends retaining current L and XL.
