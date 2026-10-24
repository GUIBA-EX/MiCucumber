# Naming

[中文](NAMING.zh-CN.md) · [Overview](../README.md)

| Region | Degenerate pair | Nondegenerate single pair | Nondegenerate A/B pairs |
|---|---|---|---|
| S | SD | S | SA / SB |
| M | MD | M | MA / MB |
| L | LD | L | LA / LB |
| XL | XLD | XL | XLA / XLB |

D denotes degeneracy; A and B identify the component pairs of the two-pair option. SA+SB denotes the union of two separate PCRs. Single-pair names have no suffix. S-original is the separate original control.

In CSV files, `scheme` identifies the evaluated portfolio, `pair_name` identifies its component pair, and `pair_id` is the candidate sequence identifier. Different names may reuse identical sequences, such as S and SA; use the F/R sequences to identify the pair. All sequences are written 5′→3′.

There are 13 portfolios, 17 paired-reaction entries and 34 FASTA entries. These counts include reuse across portfolios, not 34 unique oligos.
