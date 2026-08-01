# Stage 6.1 Hidden Knowledge Poisoning Detection

## 当前状态

- 当前项目任务：`GOV-PO-MHEP = HUMAN_ACCEPTED / HIGHEST_INTERNAL_PROJECT_EXECUTION_AUTHORITY / PERMANENT`。
- Stage 6.1 子状态：`W2_ATTEMPT1_EVIDENCE_BLOCKER / CORRECTION_DU_COMMAND_EVIDENCE_MISSING`；W2 仍
  `APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED`；H1
  `APPROVED_TO_PREPARE_OFFLINE_ARTIFACTS / BLOCKED_NOT_STARTED`。
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
- 当前 action：只返回上述最小 command-derived indexed evidence；H1 下载/bundle 与 W2 resume 均暂停。无需为 evidence
  packaging 修正重跑 GMTP 或重建环境。
- Worker 状态：原 `FU1-W1 = SUPERSEDED_BY_LOCAL_L1 / NOT FAILED`；`FU1-W2 = READY_FOR_OWNER_EXECUTION_APPROVAL /
  NOT_YET_EXECUTED` 为历史快照；当前 W2 未完成/未验收，Attempt 1 evidence-blocked。本轮 LOCAL 不联系或执行 Worker。
- Token economy：高推理/设计/审查任务优先 LOCAL；该资源原则不覆盖科学证据与安全治理。
- Correction 02：仅存在 `CONTRACT_CANDIDATE / NOT APPROVED / NOT SENT / NOT EXECUTED`；等待项目负责人决定。

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
15. [S6.1-R0-FU1 Targeted Resolution and Correction 02 Candidate](s6_1_r0_fu1_targeted_resolution.md)
16. [W2 Attempt 1 Control Plane Review](s6_1_r0_fu1_w2_attempt1_control_plane_review.md)

## 下一审批门

`S6.1-R0-FU1-P0 = HUMAN_ACCEPTED` 且 `S6.1-R0-FU1-L1 = HUMAN_ACCEPTED`。W2 Attempt 1 目前为
`W2_ATTEMPT1_EVIDENCE_BLOCKER`；H1 虽已获 owner approval，但不得在 blocker 关闭前准备模型 bundle。S6.1-P1、Dataset
freeze、Detector、training 和正式实验均未获批准。
Correction 02 Worker Contract Candidate 必须由项目负责人明确批准后才能发送。
Auto Continue = NO。
