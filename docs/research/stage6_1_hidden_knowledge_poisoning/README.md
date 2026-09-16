# Paper 1 Start Here

> 当前实验状态：`RETRIEVAL_HARNESS_COMPLETE / TWO_STAGE_RISK_BOUNDARY_FROZEN /
> DOCUMENT_DETECTOR_NOT_READY / RETRIEVAL_RISK_READY_WITH_LIMITATIONS / NO_FORMAL_DETECTOR_RESULT_YET`。
> Owner 已按 M2 `2/16`、matched controls `16/16`、M4 `0`、M8 `4/4` 和其余冻结门全部 PASS 正式接受 Protocol；
> 两条 residual reviewer variance 保持不可变且不触发 R4。Accepted Stack 绑定 Final72、Attempt2 Phase1、Guide V3.2、
> Expected V3、Evidence Pool V2 与 frozen snapshot + URL provenance。Owner 已指定两个不同真人并批准 A/B 执行与
> Phase1 分发；V1 因 human usability 被 V2 替代但原样保留。A/B 已独立完成 Phase1，两份 raw 已原样锁定并通过双门。
> Candidate、ID、顺序与研究规则均未变化；A/B Phase2 V3.2 返回均已锁定并通过 QA，映射只在四 raw 锁定后解锁。
> Agreement preflight 发现的 78 个 material field disagreements（40 个 sample）及五个 late-candidate-defect flags 已由
> Owner 完成仲裁；返回工作簿已原样锁定并提取 5+78 项决定。Owner 又逐项确认了 9 个关系/证据来源核验项，控制面以 10 个
> 字段级 overlay 保留 before/after、理由、Evidence basis 和 Owner lineage；6 个值变化、4 个值不变但有效理由得到规范化。
> 全量 72×8 一致性复核为 PASS、未解决 blocker 为 0。Expected V3 直到此后才首次用于研究者侧 QC，且不具有
> Ground Truth 优先级。Final72 GT Candidate 已按 498 个 A/B consensus、78 个 Owner 盲态仲裁及批准的 additive overlay
> 重建为 72 条/576 字段；Expected 显式定义的 504 个字段中 469 个一致，35 个差异均已分类，新的 GT blocker 为 0。
> Owner 已以 `ACCEPTED_WITH_KNOWN_EVIDENCE_LIMITATIONS` 接受 Final72 GT；72/576 与 lineage 完整，11 项已知冻结
> Evidence limitation 继续显式编码。Final72 只能用于 development/method engineering，不是 untouched final test。
> 五视角 signal feasibility 已按 label-blind raw lock → post-lock analysis 的顺序完成。72×42 raw records 不含 class/HKP/S/
> GT/Expected/Owner 字段；S/E/P/T 有可计算项，Retrieval 因无冻结 query/run trace 为 input gap，MLM/PPL 因无冻结模型不可用。
> 这些是 development-set 单信号诊断，不是 Detector 或论文结果；240-group、Dataset freeze、正式 Detector、Training、5090、
> Formal Experiment 和 Paper Result 均未开始。
> Retrieval harness 已冻结 24 个中性 current-state query、统一 72 文档 corpus、deterministic char n-gram BM25 和
> fixed-revision offline Dense trace。R 的 rank/score/stability 已可计算；7 个 current/history signals 因缺 Trusted
> Version Registry 继续 `INPUT_MISSING`。42 signals 中 29 个依赖 matched E1/E2，只能作为 oracle diagnostic。
> 现在明确区分 Stage A `S+E+P+T → document_poison_risk` 与 Stage B
> `document_poison_risk+R+query → retrieval_exposure_risk`；合法 HN 高 rank 不等于 Poison。
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

## Signal / Detection Method Engineering

- [Five-view Signal Contract V1](method_engineering/PAPER1_FIVE_VIEW_SIGNAL_CONTRACT_V1.md)
- [Signal Feasibility Experiment Spec V1](method_engineering/SIGNAL_FEASIBILITY_EXPERIMENT_SPEC_V1.md)
- [Final72 Five-view Signal Feasibility Report V1](method_engineering/PAPER1_FINAL72_FIVE_VIEW_SIGNAL_FEASIBILITY_REPORT_V1.md)
- [Final72 Signal Feasibility Report V2](method_engineering/PAPER1_FINAL72_SIGNAL_FEASIBILITY_REPORT_V2.md)
- [Two-stage Risk Architecture V1](method_engineering/PAPER1_TWO_STAGE_RISK_ARCHITECTURE_V1.md)
- [Signal Deployability Matrix V1](method_engineering/PAPER1_SIGNAL_DEPLOYABILITY_MATRIX_V1.md)
- [Trusted Version Registry Contract V1](method_engineering/PAPER1_TRUSTED_VERSION_REGISTRY_CONTRACT_V1.md)
- [Signal-to-Scale Requirement Feedback V1](benchmark/PAPER1_SIGNAL_TO_SCALE_REQUIREMENT_FEEDBACK_V1.md)
- [Baseline Matrix V1](method_engineering/PAPER1_BASELINE_MATRIX_V1.md)
- [Fusion, Risk and Explanation Design V1](method_engineering/PAPER1_FUSION_RISK_EXPLANATION_DESIGN_V1.md)
- [Metric and Ablation Contract V1](method_engineering/PAPER1_METRIC_AND_ABLATION_CONTRACT_V1.md)
- [240-group Scale Readiness Spec V1](benchmark/PAPER1_240_GROUP_SCALE_READINESS_SPEC_V1.md)
- [Baseline Reproduction Protocol](baseline_reproduction_protocol.md) — 外部 baseline 复现与 claims 边界。
- [Hardware Execution Policy](hardware_execution_policy.md) — 本机与 RTX5090 的职责边界。

## Stage Process

- [S6.1-LR1](stage_process/S6.1-LR1_work_process.md) — 路线与 baseline alignment，已关闭。
- [S6.1-R0](stage_process/S6.1-R0_work_process.md) — 工程预检，已按边界验收。
- [S6.1-R0-FU1](stage_process/S6.1-R0-FU1_work_process.md) — W2 单样本工程可行性，已关闭。
- [S6.1-P1](stage_process/S6.1-P1_work_process.md) — P1-R1、Pilot0–4 的追加式过程；Owner 仲裁一致性已闭合，等待下一步单独批准。

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
