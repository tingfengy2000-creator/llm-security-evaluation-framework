# Stage 6.1 Hidden Knowledge Poisoning Detection

## 当前状态

- 当前任务：`S6.1-R0-I Control Plane Review`。
- 任务状态：`RETURNED_FOR_WORKER_CORRECTION`；parent R0 为 `REVIEW_PENDING_CORRECTED_WORKER_EVIDENCE`。
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
- Evidence integrity：archive hash verified；internal evidence index `18/18` verified。
- 当前 action：Worker 只返回 [R0-I Review](s6_1_r0_i_control_plane_review.md) 定义的最小 corrected evidence。
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

## 下一审批门

R0-I 未接受当前 Worker summary，状态为 `RETURNED_FOR_WORKER_CORRECTION`。RTX5090 只能生成最小 corrected evidence，
LOCAL 不运行 external baseline。项目负责人随后决定是否接受 R0 以及是否批准建议的 R0-FU1；S6.1-P1 与正式实验
仍未开始。Auto Continue = NO。
