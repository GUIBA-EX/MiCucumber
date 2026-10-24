# Methods

[中文](METHODS.zh-CN.md) · [Reproduction](REPRODUCIBILITY.md)

## Panel and scope

Frozen references contain 1,848 target and 5,600 background records. The common panel has 151 name labels / 351 haplotypes; 145 labels are non-Apodida. Selection weights labels equally, then haplotypes within each label, excluding Apodida and renormalizing. Final whole-sequence results also report all-target metrics. One Apodida accession, LC704718.1, is absent from the alignment: it remains in final full-sequence evaluation but has no alignment-based prediction or plotted bases. Taxonomic names are not synonym-resolved.

## Candidate construction

Reference coordinates use extracted, ungapped AB525437.1 16S. Search forward starts around S 954, M 924, L 843 and XL 774, and reverse starts around 1133: offsets −15 to +25 in steps of two, lengths 18–32 in steps of two. Gap-free observed windows with ≥40% non-Apodida weight contribute their three most frequent sequences and weighted majority consensus. IUPAC alternatives with ≥8% positional support are added greedily at degeneracy caps 4/8/16/32. Previously generated ordinary MiFish-window oligos are also included. All generated candidates passing the oligo structure gate are background-screened; no coverage-only shortlist is used for final selection.

A second bounded search uses up to 12 distinct coordinate combinations among the strongest ordinary pairs per region. Each one-position IUPAC extension adds an observed alternative with ≥1% panel weight. Up to eight neighbor oligos per side are retained by coverage-plus-exact score, together with the ordinary parent, before testing these pair combinations. This includes 3′ positions. It is a finite search, not proof of a global optimum.

## Terminal rules and thermodynamics

3′-terminal degeneracy is allowed. For every concrete IUPAC variant: no terminal homotriplet; at least one G/C among the last three bases; 1–4 G/C among the last five; and no homopolymer longer than four anywhere. The final base need not be fixed or G/C. These project rules follow the same MiUrchin round, informed by [Thermo Fisher guidance](https://www.thermofisher.com/blog/behindthebench/pcr-primer-design-tips/) and [Primer3 parameters](https://primer3.org/manual.html). They are conservative design choices, not experimentally calibrated success thresholds.

Primer3-py 2.4.0: 50 mM monovalent salt, 1.5 mM Mg²⁺ and 0.6 mM dNTP. Expand all variants under 50 nM per variant and 200 nM total per direction divided among variants. Hairpin, homodimer, within-side heterodimer and F/R heterodimer Tm must all be <55°C. F/R Tm-range midpoint differences must be ≤5°C in both scenarios; this is not a bound on every cross-variant Tm difference. Unequal-concentration heterodimers use the larger concentration as an approximation.

Terminal audit additionally reports 5-mer end-stability ΔG at 37°C against the perfect reverse complement, using the stated salts and 200 nM, in kcal/mol across concrete variants. This descriptive calculation has no fitted yield/pass threshold. S-original remains unchanged and is exempt from selection filters.

## Selection and verification

Coverage permits ≤2 mismatches per primer with exact IUPAC compatibility in the last three bases. Exact matching requires zero mismatches in F and R. Both-strand target products are 150–500 bp with ≥50 internal bases; ambiguous binding bases do not establish a hit. Background products require correct orientation and 0–1,000 internal bases. Each selected portfolio permits ≤5 WC≤3 and ≤5 GT≤2 background accessions. WC≤4 is also reported; substantial residual counts remain in several schemes.

Group candidates by the exact four coordinates (F start/end, R start/end). A locus must support one degenerate pair and at least two distinct ordinary sequence pairs. At each locus, select the best degenerate single, ordinary single and ordinary A/B union by non-Apodida coverage + exact matching, then coverage, exact matching, lower total degeneracy and fewer background hits. Choose the locus with the highest equally weighted mean of the three coverage-plus-exact scores; use mean coverage, mean exact, total degeneracy and background as tie-breakers. All four named variants in each length group therefore share both binding intervals. Failed thermal candidates are removed and the joint choice repeated. S-original remains an unchanged separate control. The A/B metric is a separate-PCR union, not a validated multiplex. XL A/B adds no common-panel coverage or exact matching over XL single.

An independent C++ all-window scanner re-evaluates the selected full products without the background prefilter. All 11,200 alignment-based target-state checks and 32 background-accession-set checks agree. The absent Apodida alignment record is excluded from prediction comparisons but not from final evaluation. Wet-lab and independent-holdout validation remain pending.

## Figures and interpretation

Reference intervals are drawn on one linear axis; interval lengths and oriented reference bases are checked against selected oligos. Shared S/M/L/XL spans are 226/245/302/396 bp. These are reference intervals, not universal product sizes or guaranteed amplification of every reference variant. Base-matching figures show actual 5′→3′ bases, not heatmaps.

Enforcing common coordinates reduces some coverage compared with independently selected loci. The before/after table retains these trade-offs. Background counts are accessions, not experimental read fractions. Design context: [Miya et al. 2015](https://doi.org/10.1098/rsos.150088).
