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
