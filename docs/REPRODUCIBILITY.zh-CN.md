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


当前XS方案 / Current XS assay: [sequences, matching, background and reproduction / 序列、匹配、背景与复现](XS.md). XS is a fixed single assay; within-region ordinary/A/B/D coordinate rules apply to S–XL. / XS为固定单对；普通、A、B、D同坐标规则适用于S–XL。

## XS

```bash
python scripts/verify_xs.py --output /tmp/MiCucumber-XS-check
```

Frozen standalone inputs, C++ exhaustive scan and independent Python raw-sequence verification. The terminal-optimization bundle above reproduces S–XL; XS uses its separate frozen bundle and script. / 上述terminal_optimization冻结包对应S–XL；XS使用独立冻结输入与脚本，复核702项目标判断及4组背景集合。
