# Methods

## 1. Historical baselines and frozen inputs

Recover v4 and the older decided pair from the workbook coordinates documented in the README. Do not infer a primer version from a downstream filename. Reuse the frozen MiStar dataset, deduplicate accessions across inputs, and split Holothuroidea from background. The target set has 1,686 annotated records and 160 title-only records. Background: Asteroidea 1,955; Ophiuroidea 1,736; Echinoidea 1,401; Crinoidea 269; other Metazoa 239.

## 2. Alignment and comparable panel

MAFFT 7.526 aligns 116 full-length unambiguous sequences, then adds target fragments with `--addfragments --keeplength`. Reference coordinates use AB525437.1. The shared eligible interval provides 149 binomial-format name labels and 347 label-internal unique haplotypes. Eligibility is alignment-based; binding hits are evaluated on original sequences on both strands, without a binding-site indel model. Historical order names such as Aspidochirotida are retained, not modern reconciled taxonomy.

## 3. Discovery and specificity-first selection

Initial discovery produced 1,366 oligos and 81,352 pairs, followed by local v4 refinement. Same-locus supplementation considered 684 oligos and all 28,682 F/R combinations at four positions. IUPAC variants, approximate Tm compatibility and structural filters are considered. Limited multi-start greedy search chooses up to four component pairs; it does not establish a global optimum. Separate-PCR coverage is a union of explicit component pairs; pool coverage and risk include all F/R combinations.

WC models allow ≤2, ≤3 or ≤4 mismatches per primer. GT≤2 uses the inherited MiStar G:T-tolerance transformation plus up to two other mismatches per primer; it is a sensitivity model, not a complete polymerase model. Background product inner distance is 0–1,000 nt. Target products are 150–500 bp with ≥50 nt internal sequence. Ambiguous binding bases are recorded separately from confirmed hits. An analyst-selected allowance of ≤5 WC≤3 and ≤5 GT≤2 background accessions operationalizes small residual risk, not an experimental abundance threshold.

## 4. Apodida supplementation

Extract observed forward/reverse windows at the same homologous positions from all 17 source Apodida records; retain 37 unique candidate pairs. Unlike the first round, allow and flag AAAA motifs because some true binding windows contain them. Require hairpin Tm <55°C and F/R Tm difference ≤5°C; select additional pairs with Apodida gain prioritized, then overall gain, subject to background union limits. Thirteen scheme-local pairs are retained. Complete supplemented sets contain 7/7/6/9 independent PCR pairs for v4opt/S/M/L respectively. All added pair dimers are <55°C under the recorded 50 nM scenario. New whole-pool mixing is not supported.

## 5. Thermodynamics and validation

Primer3-py 2.3.1, monovalent salt 50 mM, Mg²⁺ 1.5 mM, dNTP 0.6 mM. Round-one pair/pool analyses consider concrete variants at 50 nM and a total 200 nM per direction divided across oligos/variants. Duplicate variants are summed in pools. For unequal concentrations, using the larger concentration as the scalar Primer3 input is an approximate sensitivity analysis, not a PCR recipe. Every concrete same-side and opposite-side interaction is included for round-one pools. Apodida additions have pairwise checks at 50 nM, not a whole-pool or concentration-grid validation.

The independent C++ scanner exhaustively visits all possible binding windows. Round-one target flags/product sizes and background counts are compared against Python results; 386,492 checks passed. Added pairs use that exhaustive scanner but have no separate implementation cross-check. These validations check computation, not experimental accuracy.

## 6. Remaining gaps

The database is frozen, incompletely sampled, and reused for discovery. No fresh download, synonym reconciliation, external held-out validation, wet-lab sensitivity/specificity estimate, or finalized PCR recipe is supplied. v4opt and M still miss two of four common-panel Apodida records; S misses one. L covers all four, not all Apodida species. Exact-match coverage and wider-mismatch background results must accompany mismatch-tolerant coverage claims.
