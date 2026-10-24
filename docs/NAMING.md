# Naming / 命名规范

| Previous name / 旧名 | Current name / 新名 |
|---|---|
| v4opt (optimized v4 region) | S |
| S | M |
| M | L |
| L | XL |
| Original v4 / v4原版 | S-original |

## Current identifiers / 当前标识

`MiCucumber-{S|M|L|XL}-{D1|D2|ND1|ND2}` identifies a portfolio, not a single oligo. `D` means degenerate, `ND` means A/C/G/T-only, and `1/2` is the number of independent PCR pairs. Use the `reaction` column to identify each F/R pair. All sequences are written 5′→3′.

以上名称标识方案，不是单条寡核苷酸。D为简并，ND为无简并，1/2为独立PCR配对数；`reaction`列确定每一对F/R，序列均按5′→3′书写。`MiCucumber-S-original`专指原始v4，不得与优化S-D1混淆。

`R2P...` candidate IDs remain stable. Nondegenerate IDs are region-normalized (`ND_S_...`, `ND_M_...`, `ND_L_...`, `ND_XL_...`). A shared candidate ID may occur in more than one portfolio; this is intentional reuse, not a different sequence.

R2P候选编号保持不变。无简并候选编号同步使用新区域名。不同方案可复用同一配对编号，这不代表不同序列。

## Traceability / 可追溯性

[Row-level old/new names and sequence hashes](name_mapping.csv) covers all 25 reaction rows across 17 portfolios. [Rename validation](../results/rename_validation.json) confirms 50 F/R sequence strings were preserved. S/M/L/XL are relative region labels, not guaranteed product-length classes for every organism.

逐条映射覆盖17套方案的25条反应记录，50条正反引物字符串均保持不变。区域标签只表示本项目的相对长度次序，不保证所有生物的实际产物长度。

Old names are allowed only in this mapping, historical explanations, naming adapters and frozen archives. Do not apply sequential global replacements: old S→M, M→L and L→XL must be mapped simultaneously. Frozen reference bundles and published Git tags retain their original contents; the reproduction adapter converts exported labels in one pass.

旧名仅用于映射、历史说明、命名适配器及冻结归档。不得按S→M→L→XL连续替换，以免串改；复现适配器使用单次映射。冻结证据及已发布Git标签保留原始内容。
