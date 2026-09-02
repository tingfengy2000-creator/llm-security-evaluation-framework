# Paper 1 Start Here

> 当前实验状态：`PILOT4_FINAL_BLIND_REVIEW_COMPARISON_COMPLETE / PROTOCOL_ACCEPTANCE_RECOMMENDATION_READY /
> OWNER_PROTOCOL_ACCEPTANCE_PENDING / NO_AB_DISTRIBUTION`。第一份 access-limited Phase2 raw 与最终 superseding raw 已分别
> 按原字节锁定；同一 reviewer retry 后 23 条 `SOURCE_UNREACHABLE` 全部解决。raw lock 先于 mapping/expected load，
> Phase1 exact 为 58/72，Phase2 exact 为 48/72。本机只建议 `RECOMMEND_TARGETED_REPAIR`：16 条 primary-label guide
> boundary、expected/minimum-evidence 定向问题及 `BR-18F1D39495` Evidence Pool 缺陷尚待 Owner 决策。72 条候选仍无
> Ground Truth；240-group、
> Dataset freeze、Formal Detector、Training、5090、Formal Experiment 和 Paper Result 均未开始。
> `FORMAL_EXPERIMENT = NOT STARTED`；`DATASET_FORMAL_FREEZE = NOT STARTED`。

## First screen routing

| 入口 | 打开这里 | 用途 |
| --- | --- | --- |
| **FOR HUMAN** | [Paper 1 人类可读实验总规划与实验总账](human/experiment_ledger_tingfeng.md) | 5/15/30 分钟掌握问题、方法、进度、风险和下一步 |
| **FOR CODEX/GPT** | [Agent Experiment Ledger](agent/experiment_ledger_agentUse.md) | YAML、状态枚举、evidence identity、恢复顺序和审批门 |
| **FOR CURRENT STATE** | [Current Work State](../../governance/current_work_state.md) | 唯一动态任务状态与禁止动作 |
| **FOR RESEARCH AUTHORITY** | [Research Plan Authority](human/research_plan_authority.md) | 当前研究范围、五视角合同、正式五领域与进入条件 |
| **FOR EVIDENCE** | [Experiment Master Record](../../governance/experiment_master_record.md) | 运行、工件、blocker 和 claims boundary 的控制面 |

文档职责按 [Human / Agent / Evidence Separation Contract](documentation_separation_contract.md) 分层；现有文件角色和不移动
理由见 [Document Inventory](document_inventory.md)。

## Human

- [人类可读实验总规划与实验总账](human/experiment_ledger_tingfeng.md) — `PAPER1_PRIMARY_HUMAN_ENTRY`。
- [Owner Requirement Register](human/owner_requirement_register.md) — 项目负责人明确需求的追加式登记。
- [Research Plan Authority](human/research_plan_authority.md) — 当前研究方案唯一权威入口。
- [Annotation Lessons and Future Dataset Rules](human/annotation_lessons_learned_and_future_dataset_rules.md) — 未来数据/标注的 canonical 规则。
- [Learning Notes](learning_notes.md) — 可复用研究与工程教训。

## Protocol

- [P1-R1 Protocol Framework Source](s6_1_p1_r1_protocol_review_candidate.md) — 框架已接受；数值参数和正式 protocol 仍待冻结。
- [Paper 1 Benchmark Alignment Matrix](paper1_benchmark_alignment_matrix.md) — 外部工作与本项目角色对齐。
- [Baseline Reproduction Protocol](baseline_reproduction_protocol.md) — 外部 baseline 复现与 claims 边界。
- [Hardware Execution Policy](hardware_execution_policy.md) — 本机与 RTX5090 的职责边界。

## Stage Process

- [S6.1-LR1](stage_process/S6.1-LR1_work_process.md) — 路线与 baseline alignment，已关闭。
- [S6.1-R0](stage_process/S6.1-R0_work_process.md) — 工程预检，已按边界验收。
- [S6.1-R0-FU1](stage_process/S6.1-R0-FU1_work_process.md) — W2 单样本工程可行性，已关闭。
- [S6.1-P1](stage_process/S6.1-P1_work_process.md) — P1-R1、Pilot0–4 的追加式过程；当前等待 Owner 审查定向修复建议，协议与 A/B 均未接受/批准。

## Pilot Records

- [Pilot2 Return Owner Correction](s6_1_p1_pilot2_return_owner_correction.md)
- [Pilot2 Annotation Schema V2](s6_1_p1_pilot2_annotation_v2.md)
- [Pilot2 Targeted Re-review](s6_1_p1_pilot2_targeted_rereview.md)
- [Pilot2 Post-Annotation](s6_1_p1_pilot2_post_annotation.md)
- [Pilot2 Adjudication Closure Attempt](s6_1_p1_pilot2_adjudication_closure.md)
- [Pilot2 Closure and Pilot3 Signal Feasibility](s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md)

Pilot4 当前事实由 [Current Work State](../../governance/current_work_state.md)、
[S6.1-P1 Work Process](stage_process/S6.1-P1_work_process.md)、
[Research Execution Log](../../governance/research_execution_log.md) 与 Git-external evidence 共同绑定。

## R0 / Baseline Records

- [R0 Reproduction Preflight](s6_1_r0_reproduction_preflight.md)
- [R0-I Control Plane Review](s6_1_r0_i_control_plane_review.md)
- [R0-FU1 Targeted Resolution](s6_1_r0_fu1_targeted_resolution.md)
- [W2 Attempt 1 Control Plane Review](s6_1_r0_fu1_w2_attempt1_control_plane_review.md)
- [W2 H2 Resume02 Control Plane Review](s6_1_r0_fu1_w2_h2_resume02_control_plane_review.md)
- [External Artifact Registry](external_artifact_registry.md)

## Historical / Superseded

- [Historical Paper 1 Research Route](paper1_research_route.md) — supporting only；不能覆盖 Research Plan Authority。
- [Old P1 Protocol Candidate](s6_1_p1_protocol_candidate.md) — 已在候选层被 P1-R1 替代，保留历史。
- P1-R1 文件顶部的 `REVIEW_CANDIDATE / NOT APPROVED` 是其创建时来源快照；当前 owner 状态以 Research Plan Authority、
  Current Work State 和 PODR 为准，已是 `HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK`。

## Machine / Governance

- [Agent Experiment Ledger](agent/experiment_ledger_agentUse.md)
- [LLM Context Archive](agent/llm_context_archive.md)
- [Current Work State](../../governance/current_work_state.md)
- [Experiment Master Record](../../governance/experiment_master_record.md)
- [Project Owner Decision Register](../../governance/project_owner_decision_register.md)
- [Research Execution Log](../../governance/research_execution_log.md)

Raw JSON/JSONL/log/XLSX/hash/manifest 保持原治理位置或 Git-external；本目录只提供可审计入口，不复制原始 evidence。
