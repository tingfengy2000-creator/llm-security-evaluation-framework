# Signal Feasibility and Separability Study Spec V1

Status = `PREPARED / EXECUTION_NOT_APPROVED`
Population role = `FINAL72 DEVELOPMENT_AND_METHOD_ENGINEERING_SET`

## 目标与问题

第一轮只研究五类可观察 signal 在 `Clean Current`、`Poison`、`Hard Negative` 之间是否呈现可分析差异，重点是
`Poison vs Hard Negative`。它不是最终 Detector 训练，也不是论文效果实验。

正式候选 RQ：

1. RQ1：Semantic / MLM / GMTP baselines 对版本感知隐蔽污染的检测能力如何？
2. RQ2：Five-view fusion 是否优于 Semantic-only？
3. RQ3：Temporal-Version / Provenance 是否降低 Hard Negative FPR？
4. RQ4：各 view 对 HKP1–4 与 S1–S3 的贡献如何变化？
5. RQ5：calibrated risk 是否能降低 poison exposure 并保留 clean utility？

这些均为 `HYPOTHESIS / EXPERIMENTAL QUESTION`，不是结论。

## 第一轮输出合同

- per-sample signal matrix；
- per-view signal availability；
- class-conditional distributions；
- Poison vs Clean descriptive effect；
- Poison vs Hard Negative descriptive effect；
- HKP1–4 breakdown；
- S1–S3 breakdown；
- missing/applicability/confidence/evidence-quality rate。

不得只输出一个准确率；不得在 Final72 上反复调参后把同一数据称为独立测试。

## 标签与泄漏

- 第一主任务：`Poison=1`，`Clean Current / Hard Negative=0`。
- Ground Truth 只在 signal extraction 完成后由 evaluator join，用于分布和诊断。
- extractor、retriever、feature vector 和 inference payload 不得访问 label、attack ID、HKP、stealth 或 expected answer。
- 必须单独报告 Poison vs Hard Negative，不能只与 easy Clean 比较。

## 进入实际执行前的独立审批门

必须另行冻结：输入 snapshot、query/retriever/embedding/model revisions、signal parameterization、missing handling、
normalization、threshold ownership、统计/CI、seed/repeat、资源预算、输出 manifest 与 secret/privacy boundary。本文件不授权
调用模型、运行 GMTP、训练 estimator 或产生正式效果。
