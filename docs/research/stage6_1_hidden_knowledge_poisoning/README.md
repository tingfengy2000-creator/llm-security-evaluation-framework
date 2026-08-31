# Paper 1 Start Here

> 快速状态：父 W2/FU1、PILOT0/PILOT1 已按各自范围关闭。Owner 的四候选 correction 已独立绑定，原工作簿与 blocker 历史不变；`PILOT2_GROUND_TRUTH_CANDIDATE_V1` 共 36 条（Clean 1 / Poison 12 / Hard Negative 23），PILOT2 仅按 annotation protocol + Ground Truth feasibility 人工关闭。PILOT3 本机五视角 smoke 已建立工程与信号诊断可行性，但信号弱且类别失衡，绝非 detector effectiveness。240-group、Dataset freeze、正式 Detector/Training、5090、Formal Experiment 与 Paper Result 均未推进。

> 永久前瞻性候选门：`PODR-067 / OR-029` 要求以后新建/新引入候选的法律、政策、制度、标准主体在候选文本内唯一可识别；裸指代 fail closed 为 `BROKEN_CANDIDATE / MISSING_CONTEXT`。只向前生效，不改动现有 Pilot1/Pilot2 证据。

## 一、项目需求提出人入口

1. [实验总账 — tingfeng](human/experiment_ledger_tingfeng.md) — 5–10 分钟恢复论文、阶段、结果、失败、风险和下一步。
2. [用户确认需求登记册](human/owner_requirement_register.md) — 唯一保存项目需求提出人明确确认需求的权威入口。
3. [研究方案权威文件](human/research_plan_authority.md) — 唯一保存当前已接受 Paper 1 研究方案的权威入口。
4. [阶段工作过程](stage_process/) — 每阶段一个 canonical 文件，保存时间顺序过程、失败、证据和审批门。
5. [实验总账 — agentUse](agent/experiment_ledger_agentUse.md) — 面向智能体的派生结构化镜像，不覆盖人类权威或原始证据。
6. [LLM 上下文物理存档](agent/llm_context_archive.md) — 精炼的上下文 capsule 与追加式 checkpoint。

## 二、当前阶段过程

- [S6.1-LR1 工作过程](stage_process/S6.1-LR1_work_process.md) — 路线与基线对齐，`HUMAN_ACCEPTED`。
- [S6.1-R0 工作过程](stage_process/S6.1-R0_work_process.md) — 工程预检，`HUMAN_ACCEPTED_WITH_BLOCKERS`。
- [S6.1-R0-FU1 工作过程](stage_process/S6.1-R0-FU1_work_process.md) — P0/L1/W2 已验收；FU1 仅以最小工程可行性范围关闭。
- [S6.1-P1 工作过程](stage_process/S6.1-P1_work_process.md) — P1-R1、PILOT0、PILOT1 与 PILOT2 的唯一追加式过程；当前等待 owner 仅确认 4 个 blocker 候选。
- [PILOT2 Return Owner Correction](s6_1_p1_pilot2_return_owner_correction.md) — 保留原错误登记与原推断，并以 owner-confirmed actual order supersede 盲法污染解释。
- [PILOT2 Annotation Schema V2](s6_1_p1_pilot2_annotation_v2.md) — V2 字段/验证合同、四包身份、验证结果与精确人工下一门。
- [PILOT2 Targeted Re-review](s6_1_p1_pilot2_targeted_rereview.md) — 问题字段审计、A/B 最小工作量、V1 映射 Correction 01、XLSX 保护与人工后续门。
- [PILOT2 Post-Annotation](s6_1_p1_pilot2_post_annotation.md) — 四份 return 身份、V2 agreement、分歧分类与最小 owner adjudication gate。
- [PILOT2 Adjudication Closure Attempt](s6_1_p1_pilot2_adjudication_closure.md) — 完成版 owner workbook 身份、4-candidate consistency blocker 与 Ground Truth/Pilot3 停止门。
- [PILOT2 Closure and PILOT3 Signal Feasibility](s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md) — 独立 owner correction、36 条 Pilot-only Ground Truth、Pilot2 closure 与本机五视角诊断。
- [S6.1-P1-R1 协议强化候选](s6_1_p1_r1_protocol_review_candidate.md) — 已验收框架的来源候选；其中数值参数仍为 `PENDING_PILOT_EVIDENCE`，不取代研究方案权威。
- [旧 S6.1-P1 协议候选](s6_1_p1_protocol_candidate.md) — 历史候选，已在候选层被 P1-R1 替代但不可删除或改写。

## 三、支撑研究材料

- [历史与支撑研究路线](paper1_research_route.md)
- [Paper 1 Benchmark 对齐矩阵](paper1_benchmark_alignment_matrix.md)
- [Baseline 复现协议](baseline_reproduction_protocol.md)
- [外部工件登记](external_artifact_registry.md)
- [硬件执行策略](hardware_execution_policy.md)
- [学习笔记](learning_notes.md)

这些文件提供研究依据、可比性、许可、环境和教学说明；不能覆盖当前研究方案权威文件。

## 四、证据复核材料

- [R0 复现预检](s6_1_r0_reproduction_preflight.md)
- [R0-I Control Plane Review](s6_1_r0_i_control_plane_review.md)
- [R0-FU1 Targeted Resolution](s6_1_r0_fu1_targeted_resolution.md)
- [W2 H2 Resume 02 Control Plane Review](s6_1_r0_fu1_w2_h2_resume02_control_plane_review.md)
- [W2 Attempt 1 Control Plane Review](s6_1_r0_fu1_w2_attempt1_control_plane_review.md)

Raw evidence、模型 bundle 和私有 archive 保持 Git-external；这里只保存可审计身份、结论边界和复核索引。

## 五、高级治理与审计

- [Current Work State](../../governance/current_work_state.md) — 项目动态状态控制面。
- [Experiment Master Record](../../governance/experiment_master_record.md) — 跨阶段实验/工程事实与 blocker 主记录。
- [Research Execution Log](../../governance/research_execution_log.md) — 项目级追加式审计时间线，不是 Paper 1 人类总账。
- [Project Owner Decision Register](../../governance/project_owner_decision_register.md) — 项目需求提出人确认决定记录。

职责规则：用户需求只进入需求登记册；当前方案只进入研究方案权威文件；阶段事实只追加到该阶段 work process；人类总览和 agentUse 保持同一状态；上下文恢复不产生新授权；审计日志不复制完整实验总账。
