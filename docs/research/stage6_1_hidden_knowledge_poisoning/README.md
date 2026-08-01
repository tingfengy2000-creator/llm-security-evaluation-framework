# Stage 6.1 Hidden Knowledge Poisoning Detection

## 当前状态

- 当前项目任务：`S6.1-R0-FU1-W2-H1 = OFFLINE_MODEL_ARTIFACTS_PREPARED_PENDING_5090_VERIFICATION`，前置 Correction 02
  Control Plane review 已通过并应用 final closure。
- Stage 6.1 子状态：历史 `W2_ATTEMPT1_EVIDENCE_BLOCKER` 已解决；Attempt 1 为
  `VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER`；W2 仍 `APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED`。
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
- Attempt 1 review：archive SHA/safe/index 和部分身份通过，但缺少主仓库 HEAD/clean 捕获与环境 disk byte measurement；
  见 [redacted review](s6_1_r0_fu1_w2_attempt1_control_plane_review.md)。
- Correction 01：外层 SHA、安全成员 `6/6`、index `4/4`、原 Attempt 绑定和主仓库现场证据通过；disk 数值与 manifest
  一致且低于 6 GiB，但没有捕获区分 apparent/allocated 的具体 `du` 命令、flags 与 raw output。
- Correction 02 final review：archive SHA
  `fcfa3f14c98e0103cb5a1de2f0449fa000d179e2e01d74baa6fec4b013503622`、安全检查、index `17/17`、GNU `du 9.4`
  command-derived apparent/allocated 证据和 materiality `11/11` 均通过。
- H1 artifact：Contriever 8 文件 / 438708922 bytes；BERT MLM 9 文件 / 881643453 bytes；总模型 `1320352375` bytes；
  bundle SHA `aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45`，仍待 5090 独立验证。
- Worker 状态：原 `FU1-W1 = SUPERSEDED_BY_LOCAL_L1 / NOT FAILED`；`FU1-W2 = READY_FOR_OWNER_EXECUTION_APPROVAL /
  NOT_YET_EXECUTED` 为历史快照；当前 W2 未完成/未验收，Attempt 1 valid blocked by model download。本轮 LOCAL 不联系或执行 Worker。
- Token economy：高推理/设计/审查任务优先 LOCAL；该资源原则不覆盖科学证据与安全治理。
- 当前 action：项目负责人可通过 owner-controlled handoff 将精确 bundle 传给 RTX5090，先验证外层 SHA、安全解压和
  `model_files.sha256`，再单独决定是否恢复 W2。本轮不自动联系 Worker，不加载模型或运行 GMTP。

## 权威入口

1. [论文优先比较证据原则](../paper_comparative_evidence_principle.md)
2. [Paper 1 研究路线](paper1_research_route.md)
3. [Benchmark 对齐矩阵](paper1_benchmark_alignment_matrix.md)
4. [外部 Artifact 登记册](external_artifact_registry.md)
5. [Baseline 复现协议](baseline_reproduction_protocol.md)
6. [硬件与双机执行政策](hardware_execution_policy.md)
7. [学习与面试笔记](learning_notes.md)
8. [Context Authority Map](../../governance/context_authority_map.md)
9. [PO-MHEP Highest Internal Execution Authority](../../governance/project_owner_sovereignty_and_mandatory_escalation_principle.md)
10. [Research Execution Log](../../governance/research_execution_log.md)
11. [Dual-Machine Context Sync Policy](../../governance/dual_machine_execution_policy.md)
12. [Stage 6.1 Learning Guide](../../learning/stage6_1_hidden_poisoning.md)
13. [S6.1-R0 Reproduction Preflight Definition](s6_1_r0_reproduction_preflight.md)
14. [S6.1-R0-I Control Plane Review](s6_1_r0_i_control_plane_review.md)
15. [S6.1-R0-FU1 Targeted Resolution and Approved Correction 02 Contract](s6_1_r0_fu1_targeted_resolution.md)
16. [W2 Attempt 1 Control Plane Review](s6_1_r0_fu1_w2_attempt1_control_plane_review.md)

## 下一审批门

`S6.1-R0-FU1-P0 = HUMAN_ACCEPTED` 且 `S6.1-R0-FU1-L1 = HUMAN_ACCEPTED`。Correction 02 已通过并关闭 Attempt 1
evidence blocker；H1 bundle 已准备但未获 5090 验证。下一门是 owner-controlled 5090 transfer/integrity verification
及独立 W2 resume 决策。S6.1-P1、Dataset freeze、Detector、training 和正式实验均未获批准。
Auto Continue = NO。
