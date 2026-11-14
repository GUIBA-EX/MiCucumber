# Reproducing the review analyses

The scripts use the repository root and write intermediate files under `work/review/`. On Yasuda2, cutadapt 5.0 is available in `/home/yasuda2/miniforge3/envs/ipyrad/bin/` and MAFFT 7.525 and primer3-py are available in `/home/yasuda2/miniforge3/envs/geneminer2/`. Set `CUTADAPT` or `MAFFT` to executable paths if these differ. Biopython, matplotlib, NumPy and Primer3 are required for the respective scripts.

Copy the scripts to the working directory before running, as the analysis scripts share `work/review/scan.py`:

```sh
mkdir -p work/review
cp scripts/review/*.py work/review/
python3 work/review/fetch_midori.py
python3 work/review/scan.py
python3 work/review/taxonomy.py
python3 work/review/panels.py
python3 work/review/reconcile.py
python3 work/review/resolution.py
python3 work/review/midori_scan.py
/home/yasuda2/miniforge3/envs/geneminer2/bin/python work/review/thermo.py
/home/yasuda2/miniforge3/envs/geneminer2/bin/python work/review/figures.py
python3 work/review/mismatch_positions.py
```

For an offline replay, copy `results/resolution/worms_results.json` to `work/review/worms_results.json`. The MIDORI2 SINTAX unique-sequence files and their published SHA-256 hashes are in `results/specificity/manifest.json`. The screening selects the longest available sequence per species label in each marker. The COI classification excludes ambiguous or non-exact WoRMS matches. Local candidate names in the review data correspond to the three assays analyzed in detail in the READMEs. Results depend on the frozen data and the stated product-length filters.
