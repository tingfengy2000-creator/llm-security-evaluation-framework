# Stage 6.1 Hidden Knowledge Poisoning Detection

## 当前状态

- 当前任务：`S6.1-R0-FU1-W2 GMTP Detection-Only Minimal Smoke`。
- 任务状态：`P0 HUMAN_ACCEPTED / L1 HUMAN_ACCEPTED / W2 APPROVED_TO_START / NOT_YET_EXECUTED`；parent FU1 为
  `APPROVED / LOCAL-FIRST / WORKER-GATED`。
- 历史前置：`S6.1-LR1` 为 `HUMAN_ACCEPTED`。
- 追加治理：Git-native Context Recovery Governance 与 Paper-First Comparative Evidence Principle 均为 `HUMAN_ACCEPTED`。
- Paper 1 canonical route：`ACCEPTED AS CURRENT RESEARCH ROUTE`。
- 正式 RAG 安全实验：`NOT STARTED`。
- 数据集构建、Detector 实现、模型训练和论文结果：`NOT STARTED`。
- 研究分支：`research/stage6-1-hidden-poisoning`。
- 起点：accepted S6-T5 baseline `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`。
- baseline tag `s6-t5-rag-baseline-v1`：已恢复为 annotated tag，并在 `2026-07-31` 核验本地/远端均严格指向
  `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`；后续仍以 Git 动态事实为准。
- RTX5090 Bootstrap：`HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY`。
- Superseded R0 snapshot：`DEFINED / NOT STARTED / PENDING OWNER EXECUTION APPROVAL`。
- Historical R0 execution snapshot：`APPROVED_TO_START`。
- R0：`HUMAN_ACCEPTED_WITH_BLOCKERS`；historical first-review return 与 corrected-evidence acceptance 均保留。
- FU1 outcome：P0 合同已验收；L1 已验证 PoisonedRAG released NQ artifact、100-record schema、官方 LM-targeted
  `question + "." + adv_text` 拼装与固定样本哈希。工件可 API-free 复用，但不等于复现 API generation。
- 当前 action：RTX5090 只按 [FU1 targeted resolution](s6_1_r0_fu1_targeted_resolution.md) 中冻结的 W2 合同执行并返回证据。
- Worker 状态：原 `FU1-W1 = SUPERSEDED_BY_LOCAL_L1 / NOT FAILED`；`FU1-W2 = READY_FOR_OWNER_EXECUTION_APPROVAL /
  NOT_YET_EXECUTED` 为历史快照，当前为 `APPROVED_TO_START / NOT_YET_EXECUTED`。本轮 LOCAL 不联系或执行 Worker。
- Token economy：高推理/设计/审查任务优先 LOCAL；该资源原则不覆盖科学证据与安全治理。

## 权威入口

1. [论文优先比较证据原则](../paper_comparative_evidence_principle.md)
2. [Paper 1 研究路线](paper1_research_route.md)
3. [Benchmark 对齐矩阵](paper1_benchmark_alignment_matrix.md)
4. [外部 Artifact 登记册](external_artifact_registry.md)
5. [Baseline 复现协议](baseline_reproduction_protocol.md)
6. [硬件与双机执行政策](hardware_execution_policy.md)
7. [学习与面试笔记](learning_notes.md)
8. [Context Authority Map](../../governance/context_authority_map.md)
9. [Research Execution Log](../../governance/research_execution_log.md)
10. [Dual-Machine Context Sync Policy](../../governance/dual_machine_execution_policy.md)
11. [Stage 6.1 Learning Guide](../../learning/stage6_1_hidden_poisoning.md)
12. [S6.1-R0 Reproduction Preflight Definition](s6_1_r0_reproduction_preflight.md)
13. [S6.1-R0-I Control Plane Review](s6_1_r0_i_control_plane_review.md)
14. [S6.1-R0-FU1 Targeted Resolution](s6_1_r0_fu1_targeted_resolution.md)

## 下一审批门

`S6.1-R0-FU1-P0 = HUMAN_ACCEPTED` 且 `S6.1-R0-FU1-L1 = HUMAN_ACCEPTED`。`FU1-W2 = APPROVED_TO_START /
NOT_YET_EXECUTED`，下一步是 Worker 按冻结合同执行后返回证据；不得把批准写成通过或验收。S6.1-P1、Dataset
freeze、Detector、training 和正式实验均未获批准。
Auto Continue = NO。
