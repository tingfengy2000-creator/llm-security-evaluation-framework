# 给项目负责人的 D1/L0 基线审阅包

先读 [负责人报告](PAPER1_L0_D1_BASELINE_OWNER_REPORT_V1.md) 或 [PDF](output/pdf/PAPER1_L0_D1_BASELINE_OWNER_REPORT_V1.pdf)。

本包整理到 `4dc9161` 的 D1 开发证据。建议结束本轮基线和固定提示探索；不代表方法有效或负责人已经验收。

## 文件用途

- `RESULTS_REVIEWED_V1.json`：带来源和缺失标记的汇总数据，不是逐条原始预测。
- `RESULTS_TABLE_V1.csv`：分子、分母、比例和独立复算的样本级 Wilson 区间。
- `SOURCE_REGISTER_V1.json`：固定 Git 来源、快照 SHA256、私有归档报告哈希及核验级别。
- `evidence/`：截止提交的 20 份本仓库脱敏记录/代码快照，未改原文件。
- `REPORT_VALIDATION_V1.json`：算术、来源身份、链接和历史保护核对。
- `DELIVERY_QA_V1.json`：PDF 页面检查、收口矩阵及本次交付状态。

**私有原始证据不在本包。** FULL01/ALIGN01 的正文、标签、逐条 raw 和私有归档留在 5090。清单中的这些哈希是原持有方报告值，未在控制端独立重算；本报告没有重放家族 bootstrap 或模型。

## 重建与核对

`build_owner_report.py metadata` 从固定 Git 提交复制脱敏快照并写 CSV；`figures` 使用现有 matplotlib；`pdf` 使用现有 ReportLab 和 Windows 微软雅黑字体；`validate` 执行本包一致性核对。不安装依赖，不加载模型，不改历史结果。

PDF 与图表是本报告派生展示，不是新实验或新分数。主要事实来自原协议、结果和审计。PDF 内证据链接指向固定提交；本地 Markdown 可从同包快照离线下钻。
