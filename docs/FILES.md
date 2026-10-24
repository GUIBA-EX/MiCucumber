# File index / 文件索引

| Path | Purpose / 用途 |
|---|---|
| `README.md`, `README.zh-CN.md` | Current overview / 当前双语概览 |
| `report.html` | Single bilingual result report / 统一双语结果报告 |
| `sequences/primer_pairs.csv`, `sequences/primers.fasta` | All 13 portfolios, 17 PCR rows, 34 F/R entries / 全部当前方案 |
| `sequences/MiCucumber-{S,M,L,XL}.{csv,fasta}` | Region-specific exports / 分区域序列 |
| `sequences/MiCucumber-S-original.fasta` | Unchanged original control / 原样保留的原始对照 |
| `results/comparison.csv` | 26 rows: 13 portfolios × two panels / 共同与本区域面板 |
| `results/degenerate/` | Degenerate selection, sequences, missed taxa, off-targets, thermal and validation evidence / 简并方案证据 |
| `results/nondegenerate/` | Concrete candidates, selection audit, sequences, comparisons and validation / 无简并方案证据 |
| `results/matching/` | 21 matching profiles and 7,371 per-reference states / 21组匹配概况与7,371条逐参考状态 |
| `figures/` | Current region diagrams and coordinate source / 当前区域图与坐标 |
| `docs/name_mapping.csv` | Row-level old/new names and sequence fingerprints / 逐条命名映射 |
| `scripts/naming.py` | One-pass naming adapter / 单次命名适配器 |
| `scripts/check_release.py` | Export, sequence, link and hash checks / 发布一致性校验 |
| `scripts/reproduce.py` | Current reproduction entry point / 当前复现入口 |
| `reproducibility/frozen/` | Unmodified source bundles, using historical identifiers / 保留历史标识的冻结输入 |
| `archive/pre-renaming-14f156f.zip` | Complete tracked repository before this reorganization / 整理前完整版本 |
| `SHA256SUMS.json` | Current file fingerprints / 当前文件指纹 |

Use `sequences/` for ordering and comparison. Historical multi-pair portfolios remain in the archive and are not current recommendations. CSV reaction entries are paired explicitly; do not arbitrarily combine F/R oligos across rows or treat independent PCRs as a validated mixture.

订购与比较请使用`sequences/`。旧版多对方案在归档中保留，不属于当前推荐。每条CSV记录明确定义一对F/R，请勿任意跨行配对或把独立PCR当作已验证混合体系。
