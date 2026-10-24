# Reproduction / 复现

Extract `results/terminal_optimization/reproduction_sources.zip` into an empty directory. The frozen `work/micucumber_terminal/selected.json` is the current Occam-retained release; the earlier joint-locus selector describes the baseline and does not reproduce the final editorial retention decisions.

从冻结的当前选择重新执行以下独立验证、统计与图件步骤：

```bash
python work/micucumber_terminal/verify.py
python work/micucumber_terminal/summarize.py
python work/micucumber_terminal/figures.py
python work/micucumber_terminal/end_audit.py
```

Release check / 发布检查：`python scripts/check_release.py`。探索候选全集位于`results/degenerate_expansion`，保留理由见`docs/DECISIONS.md`。

Expanded A/B search / 扩大A/B搜索：`work/ab_expanded/search.py PROJECT` → `refine.py` → `install.py`, followed by each project’s `verify.py`, `summarize.py` and figure scripts. The bundle contains the preceding selection, expanded candidates and final selection. Run `python scripts/check_ab.py` to check mutual contributions and current README values. The search scripts use the multi-project workspace layout; to reproduce only this release, use its frozen selection and per-project verification pipeline. / 搜索脚本依赖三个项目的共同工作目录；单独复核本发布时使用冻结选配结果及项目独立扫描流程。
