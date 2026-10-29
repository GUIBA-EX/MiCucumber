# Computational evaluation

The common five-window panel contains 151 species. This release adds equal-denominator comparisons, primer-free barcode identity and nearest-neighbor analysis, and genus-blocked conditional sequence-selection tests. Released primer sequences remain unchanged.

Run from this directory with Python 3.10+: numerical analysis uses the standard library; plotting additionally requires matplotlib.

```sh
python3 scripts/analyze.py
python3 scripts/distances.py
python3 scripts/sensitivity.py
python3 scripts/validate.py
python3 scripts/plot.py
```

### Common panel, barcode discrimination and genus-blocked holdout

The accession intersection of all five windows contains 151 species and provides a common denominator for length comparisons. Own-window results are reported separately. Primer-free inserts were extracted strictly between the aligned binding windows, with gaps removed and ambiguous inserts excluded. Identity uniqueness was assessed against every available unambiguous insert for that window, including species outside the common panel. Unit-cost Levenshtein distances identified each species' nearest other-species neighbor. These analyses separate primer compatibility from barcode discrimination (Riaz et al., 2011).

Five-fold genus-blocked selection used seed 20261030. Genera sharing identical complete representative sequences were linked into one block, preventing duplicate-sequence leakage. Each fold selected new F/R sequences using training species only, without released primers or global candidate pools as seeds. A deterministic greedy search used up to 24 admissible frequent concrete seeds per side, 3′-half ambiguity, ≤8 variants per oligonucleotide and fixed oligonucleotide lengths, allowing local offsets within five alignment columns of the previously chosen binding intervals. Held-out species were assessed by raw-sequence paired scans with the existing window-specific size and mismatch rules. Region discovery preceded splitting, and fold candidates were not screened with the formal thermal/background gates; this is conditional sequence-selection testing rather than external validation of the complete design pipeline. Fold sequences are diagnostic candidates, not released replacement primers.

[Analysis methods and reproduction](README.md)

