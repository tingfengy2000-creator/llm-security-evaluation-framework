# Paper 1 Fusion, Risk and Explanation Design V1

Status = `INTERFACE_AND_DESIGN_ONLY / NOT TRAINED`

## Detection fusion

- Primary：Logistic Regression。
- 输入：normalized five-view signal values + applicability indicators + 必要 confidence/evidence-quality features。
- Nonlinear comparison：XGBoost / LightGBM。
- 当前禁止：大型 Transformer fusion、GNN、复杂端到端 training；除非后续实验证明必要并获单独批准。
- 每个 view 必须先产生 single-view detection score，再与完整 fusion 比较。
- `NOT_APPLICABLE` 必须由 indicator + null value 表示，不能变为 safe zero。

## Risk

Detection 先输出 `raw_risk`。后续 calibration 候选为 Platt Scaling 与 Isotonic Regression；只能在 development protocol
上选择，禁止 test-set tuning。风险阶段至少报告 Brier Score 与 Expected Calibration Error，但本轮不计算。

## Explanation

解释结构固定为 `SIGNAL_GROUNDED + EVIDENCE_GROUNDED`，至少输出：

- overall risk；
- top contributing views；
- top contributing signals；
- evidence references；
- version/provenance conflict reason codes。

Free-form LLM explanation 不能成为唯一解释。当前不声称 explanation faithful，也不执行 retrieval detoxification。
