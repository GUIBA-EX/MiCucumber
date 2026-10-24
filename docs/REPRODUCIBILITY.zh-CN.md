# Reproduction / 复现

Install Python 3.12 dependencies from `requirements.txt`, then extract [the current source bundle](../results/terminal_optimization/reproduction_sources.zip) into a fresh directory. / 安装依赖并将当前源码包解压到新目录。

```sh
python -m pip install -r requirements.txt
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python work/micucumber_terminal/choose.py
mkdir -p work/micucumber_nondegenerate
c++ -O3 -std=c++17 work/micucumber_nondegenerate/independent_scan.cpp -o work/micucumber_nondegenerate/independent_scan
python work/micucumber_terminal/verify.py
python work/micucumber_terminal/summarize.py
python work/micucumber_terminal/end_audit.py
python work/micucumber_terminal/figures.py
```

Outputs: `work/micucumber_terminal/release/`. This route repeats selection from frozen feasible states, full-product verification, terminal audit and figures without new database retrieval. It requires installed dependencies and a C++17 compiler. / 从冻结可行候选状态重算选择、全产物复核、末端审计和图件，不重新下载数据库。

For upstream discovery, the bundle also includes `discover.py`, `scan_sites.cpp`, `optimize.py`, `neighbors.py` and `merge_neighbors.py`. Run discovery, compile the site scanner, scan `work/micucumber_terminal/sites`, run `optimize.py`, build neighbors, scan `neighbor_sites`, merge neighbors, then execute the commands above. The site scanner writes all candidate background sites; these intermediate files can be large. / 源码包也包含完整上游候选搜索及背景扫描代码；按上述顺序重算，中间背景位点文件较大。

```sh
python scripts/check_release.py
```

The release checker uses the standard library to verify exported sequences, all concrete-variant terminal rules, both concentration scenarios, recomputed panel/background metrics, original-control invariance, reference coordinates, local links, bundle integrity and SHA-256 hashes. / 发布检查器使用标准库验证序列、末端规则、双浓度热力学、指标、原始对照不变性、坐标、链接、压缩包与哈希。

Earlier workflows in `scripts/reproduce.py` and `reproducibility/frozen/` describe the retained pre-terminal analysis; they are not the current design entry point. / 早期脚本和冻结包为保留分析，不是本轮设计入口。
