# Primer matching

`by_order.csv` gives 16S results on the 174-species panel and COI results on the original alignment-based 283-record panel. `coi_worms_panel.csv` records the 274 WoRMS-reconciled COI representatives used in the new paper; `coi_worms_coverage.csv` gives the corresponding order-level results. `oligo_tm.csv` reports Primer3 calculations at 50 nM per variant. The 0, 1 and 2 columns allow at most that many mismatches per primer and do not impose a terminal-three rule.

`work/review/` contains the cutadapt output and scripts used to generate the tables. Existing 12S and other candidate results remain in the frozen v1.8 analyses.

`sd_position_mismatch.csv` estimates per-position mismatch frequencies using the best full-length ungapped site within 15 reference bases of each design window.
