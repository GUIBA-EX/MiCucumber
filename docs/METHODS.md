# Methods

[中文](METHODS.zh-CN.md) · [Naming](NAMING.md) · [Reproduction](REPRODUCIBILITY.md)

## Scope and reference data

This document describes the current S/M/L/XL one-/two-pair portfolios. Earlier 6–9-pair sets are historical and are preserved in the archive. Original v4 is retained as S-original, with both sequences and all IUPAC symbols unchanged. Naming does not imply a new design run.

The round-two frozen dataset contains 1,848 target records and 5,600 background records. Two additional Apodida 16S regions were inferred by homology from unannotated mitogenomes; their orientation was corrected against AB525437.1. Six UNVERIFIED records were excluded. These inferred regions are not equivalent to curated annotations. The source sequences, accession metadata, orientation audit and reference provenance are in the round-two reproduction bundle. No new database acquisition is claimed for this renaming update.

## Panels and metrics

The common panel comprises 151 binomial-format taxonomic name labels and 351 unique within-label haplotypes, with 145 non-Apodida labels. Own-region eligibility is evaluated separately for each design window; its denominators are supplied in `results/comparison.csv`. Names are not reconciled for synonyms or changes in order taxonomy. Equal weights are assigned to labels, then to haplotypes within a label. Non-Apodida metrics are renormalized after excluding Apodida; all-target metrics include it.

Target binding is scanned on both strands of the original sequences, not inferred solely from an alignment column. Target products must be 150–500 bp with at least 50 nt internal sequence. **Coverage** allows at most two mismatches in each primer, with the terminal three 3′ bases exactly compatible. **Exact matching** requires zero mismatches in both primers; for degenerate primers, IUPAC compatibility counts as matching. An ambiguous target binding base does not count as a confirmed hit. No binding-site indel model is fitted.

The reference coordinate plot shows homologous seed windows on the extracted ungapped 16S sequence of AB525437.1. Window spans are not universal product sizes, and modified oligos may differ in length from the seed. The current plot does not reuse historical panel-conservation percentages or multi-pair counts.

## Background screening

The WC models allow up to two, three or four mismatches per primer. GT≤2 uses the inherited G–T tolerance transformation plus up to two mismatches per primer as a sensitivity model; it is not a complete PCR/polymerase model. Background products allow 0–1,000 nt internal sequence. Ambiguous binding hits are recorded separately in source evidence.

The selection allowance is at most five WC≤3 and five GT≤2 background accessions in the union of component pairs. This is an analyst-defined screening rule, not an experimental abundance threshold. WC≤4 is reported to expose relaxed residual risk. S-original is an unchanged control, not a candidate constrained by this gate, and has extensive background hits. All background counts are accession counts rather than species counts or read fractions.

## Degenerate portfolios: degenerate sets

The final portfolios use a previously independently checked pool of 96 candidate pairs. Enumerate one- and two-pair subsets within each region. Apodida has no minimum coverage requirement and is excluded from the optimization objective. First maximize mean non-Apodida coverage across common and own-region panels. Then maximize mean exact matching while allowing a limited coverage loss relative to that coverage-first anchor **on each panel separately**: two percentage points for S-D-2pair and L-D-2pair; one point for the other portfolios. WC≤3 and GT≤2 accession unions must each remain ≤5.

The selected eight portfolios passed 21,036 target-result consistency checks. Upstream round-two validation recorded 346,488 checks. Exhaustive selection is conditional on the supplied candidate pool and objective, not proof of a global primer-design optimum. Two-pair coverage is the union of two independent PCRs; arbitrary cross-pair combinations and mixed-tube interactions are not validated.

## Nondegenerate portfolios: nondegenerate sets

Enumerate all concrete A/C/G/T variants of the eight parent pairs in the current two-pair degenerate portfolios: 2,644 distinct pair candidates within their respective regions. Do not create arbitrary F/R combinations across different parent pairs or search new binding locations. Apply the structural threshold below, then exhaustively compare one- and two-pair subsets using the same coverage/exact objective and tolerances: S-2pair and L-2pair use two points; all others one point.

Python vectorized binding predictions were compared against an independently implemented C++ exhaustive full-window, both-strand scan. Coverage and exact-match accession sets agreed for all selected pairs; original-control panel predictions were also checked, totaling 31,428 Boolean comparisons. Selected nondegenerate portfolios have no WC≤3 or GT≤2 hits in this frozen background set, but this does not establish experimental specificity. Their loss of target coverage and exact matching is substantial, so they remain comparators rather than replacements for the degenerate sets.

## Thermodynamics

Primer3-py 2.3.1: 50 mM monovalent salt, 1.5 mM Mg²⁺ and 0.6 mM dNTP. Degenerate checks expand IUPAC symbols, using 50 nM per concrete variant and a 200 nM total per direction divided among variants. Within-side and opposite-side interactions are evaluated. For unequal strand concentrations, the larger concentration is used as an approximate scalar input to Primer3.

Nondegenerate candidates are evaluated at 50 and 200 nM per oligo; hairpin, homodimer and F/R heterodimer structural Tm must remain below 55°C. F/R melting-temperature differences are reported, not used to assert a validated annealing temperature. Original S-original is preserved as a historical control. These are computational checks, not a PCR recipe or whole-pool validation.

## Limits and historical evidence

References are incompletely sampled and reused for design and evaluation; no independent holdout validation, wet-lab sensitivity/specificity estimate, or finalized PCR recipe is supplied. Small mismatch-model background counts do not prove low environmental amplification. Historical methods, previous larger portfolios, earlier taxonomy and source identifiers are retained only as frozen evidence. See the naming map before comparing old and new documents.
