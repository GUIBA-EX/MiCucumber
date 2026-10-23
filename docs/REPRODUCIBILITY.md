# Reproducibility / 复现

## Supported route / 支持的流程

Run `python revalidate.py` from any directory using its absolute path, or from the repository root as shown in the README. Python 3.12, pinned requirements and a C++17 compiler are required. It reruns target validation, the independent scanner, round-one consistency checks, portfolio unions, Apodida scanner/selection, and pair/pool thermodynamics. It overwrites generated analysis results and creates temporary reference copies for Apodida. No network access is needed after installing dependencies.

按README安装依赖后运行`python revalidate.py`，也可以从任意目录使用脚本绝对路径。该流程重新验证目标、独立扫描、第一轮一致性、组合并集、Apodida筛选及热力学。运行会覆盖生成的分析结果，并为Apodida创建临时参考副本。依赖安装后不需要联网。

## Files / 文件

- `analysis/`: frozen FASTA, alignment, accession metadata, panel, selected candidates, evaluation programs and machine-readable evidence / 冻结输入、选中候选、评估程序及证据。
- `analysis/apodida/`: observed candidate windows, 37 candidate pairs and exhaustive scan / 实际窗口、37对候选及扫描结果。
- `results/`: user-facing primer and comparison tables / 用户序列与结果表。
- `discovery/`: historical discovery implementation for inspection, **not a turnkey pipeline**. Scripts were originally run beside intermediate inputs and caches; large transient caches and complete discovery intermediates are not included. / 历史设计实现供审阅，不是可一键运行的全流程；部分中间文件与大型缓存未打包。
- `analysis/final_selected.json`: historical single-pair seeds used by the Apodida diagnostic script, **not the final recommended portfolio**. / 历史单对种子，不是最终组合推荐表。
- `SHA256SUMS.json`: hashes of the published snapshot / 发布快照指纹。

The supported reproducibility claim is **revalidation of selected candidates from the frozen inputs**, not complete rediscovery or fresh database acquisition. Original source fingerprints are retained with local paths removed. MAFFT 7.526 produced the saved alignments; it is not needed for this revalidation entrypoint.

支持的复现范围是从冻结输入重新验证已选候选，不是完整重新发现候选或重新获取数据库。原始数据指纹保留，但移除了本机路径。保存的比对由MAFFT 7.526生成；当前复核入口不需要重新运行MAFFT。
