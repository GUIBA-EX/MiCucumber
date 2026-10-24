# 复现

[English](REPRODUCIBILITY.md) · [方法](METHODS.zh-CN.md) · [命名规范](NAMING.zh-CN.md)

## 检查发布文件

在仓库根目录运行：

```bash
python scripts/check_release.py
```

仅需Python标准库。检查13套方案、区域/类型/对数、17条配对记录、34条FASTA记录、无简并序列仅含A/C/G/T、原版对照不变、旧名到新名的序列和数值一致性、筛选阈值、Markdown/HTML链接、ZIP完整性及文件指纹。此步骤不重新扫描结合位点。

## 计算复现

使用Python 3.12，并安装冻结分析依赖。无简并及第二轮扫描流程还需C++17编译器（`c++`，底层入口支持时可使用`CXX`）。

```bash
python -m pip install -r requirements.txt
python scripts/reproduce.py degenerate --work-dir reproduction-work
python scripts/reproduce.py nondegenerate --work-dir reproduction-work
```

两种模式使用不同子目录。再次运行时请指定新的`--work-dir`；程序不会覆盖已有复现目录。依赖安装后无需联网，原始输入包保持不变。

- **简并方案：**从冻结逐配对目标/背景证据重算1–4对穷举，导出当前4套简并单对方案，转换命名，并与发布序列及共同/区域面板指标比较。此入口不重新扫描原始参考，也不重新发现结合位点。新名输出在`degenerate/current-results/`。
- **无简并方案：**重新枚举2,644个具体候选、优化1对/2对方案、编译并执行独立全序列目标/背景扫描、核对预测及原版对照，然后转换新名并校验序列与指标。新名输出在`nondegenerate/current-results/`。
- **第二轮上游扫描：**运行`python scripts/reproduce.py round2 --work-dir reproduction-work`，执行冻结参考的独立复核。中间证据保留源标识，此入口本身不导出当前13套方案。

## 输入与输出

冻结包提供参考数据及计算输入；`scripts/naming.py`将输出标识映射为当前命名。分析结果位于简并与普通引物两种模式的`current-results/`子目录，序列与指标校验记录见[复现检查](../results/reproduction_checks.json)。

## 扩增区域图

```bash
python -m pip install -r requirements-plot.txt
python scripts/plot_regions.py
python scripts/plot_regions.py --cjk-font /path/to/CJK-font.ttf
```

默认生成英文PNG/SVG/PDF，指定已安装的中文字体后生成两种语言。坐标来源为`figures/region_coordinates.csv`，表示种子窗口，不是实验产物长度分布。重新生成发布图后，需更新文件指纹清单。

## 匹配图

安装绘图依赖后运行 `python scripts/plot_matching.py`。使用冻结的面板及逐配对命中数据，导出逐条状态和加权汇总，并核对共同面板方案指标。
