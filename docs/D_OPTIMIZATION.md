# 当前D引物选择 / Current D selection

S、M、L、XL分别选自SD-T10、MD-T4、LD-T7、XLD-T8。S采用当前方案与覆盖候选的IUPAC并集；M不为额外2.15个百分点覆盖接受WC≤3背景从58增至252条；XL覆盖相同时选择更低简并度。筛选要求末端与热力学通过、每方向简并度≤128、宽松WC≤3/GT≤2各≤100条、严格WC/GT各≤20条；XS单独保留其已说明的背景放宽。这里的“首选”限于本次已复核候选，不宣称全局最优。

| 方案 | 目间覆盖率 | 目间完全匹配率 | 检出标签 | F/R简并度 | 严格WC/GT背景 |
|---|---:|---:|---:|---:|---:|
| XS | 75.52% | 15.42% | 131/151 | 4/3 | 20 / 20 |
| SD | 66.03% | 4.95% | 133/151 | 4/12 | 3 / 6 |
| MD | 73.18% | 29.72% | 124/151 | 128/2 | 2 / 9 |
| LD | 61.63% | 15.99% | 111/151 | 128/8 | 0 / 0 |
| XLD | 35.95% | 4.00% | 37/151 | 2/24 | 0 / 7 |

## 引物序列（5′→3′）

| Assay | F | R |
|---|---|---|
| XS | `RGYTTTGGTTGGGGCAAC` | `TTDCCCCAATCCAACATCGA` |
| SD | `CMAGAAAGACGAGAAGACCCYGTC` | `RAGRAGATDACGCTGTTATCCCTG` |
| MD | `AAAYTYCTAYYNRCGTGAAGAA` | `GTTATCCCTGCGGTARCT` |
| LD | `RRACYWGTATGAAYGGCATWACMT` | `CGCTGTTATCCCTRCRGW` |
| XLD | `RGTCACGCCTGCCCAGTGGA` | `RAGATDACGCTGTTATCCCTGCGGTAACTN` |


当前SD/MD/LD/XLD对应SD-T10/MD-T4/LD-T7/XLD-T8。XS沿用已有固定单对。M的T3为完全匹配优先的比较候选，T5为放宽背景的比较候选；XL的T9未带来覆盖收益，因较高简并度和GT背景不选。/ Current SD/MD/LD/XLD map to SD-T10/MD-T4/LD-T7/XLD-T8. XS is retained. M T3 favors exact matching; T5 relaxes background. XL T9 adds no coverage and is not selected because of greater degeneracy and GT background.

[Selection policy](../results/current/D_selection_policy.json) · [Selected source candidates](../results/current/selected_D.csv) · [Full candidate evidence and plots](../results/taxon_optimization/README.md) · [Frozen reproduction checks](../results/taxon_optimization/frozen_reproduction_check.json)
