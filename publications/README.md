# MiCucumber computational preprint

Author / 作者: **Fei Xia**. Updated / 更新: **30 October 2026**.

- [PDF](MiCucumber_preprint.pdf)
- [Editable Markdown / Markdown稿](MiCucumber_preprint.md)
- [Input provenance / 输入来源与校验](preprint_provenance.json)
- [Validation / 验证](preprint_validation.json)

The manuscript uses the latest frozen computational evaluation. Released primer sequences are unchanged. Genus-blocked fold candidates are diagnostic sequences, not replacement recommendations.
稿件使用最新版冻结计算结果，正式引物不变。属级折内候选为诊断序列，不作为替换推荐。

From the repository root / 在仓库根目录运行：

```sh
python3 -m pip install -r publications/requirements-preprint.txt
python3 publications/build_preprint.py
python3 publications/check_preprint.py
```

Figures are regenerated from committed result tables. The source-data commit and input hashes are recorded in the provenance file. Repository upload is distinct from submission to a preprint server.
图表由已提交结果表重绘，来源提交与输入哈希见provenance。仓库发布不代表已向预印本平台投稿。
