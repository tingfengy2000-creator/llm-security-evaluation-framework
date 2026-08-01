# Paper 1 Start Here

> 快速状态：S6.1-LR1 已人工验收；R0 带阻塞项验收；FU1 的 P0/L1 已验收，父 W2 未完成、未验收。H1 离线模型包已由本机准备；H2 已批准但尚未发送或执行，5090 只有在 H2-A 完整通过后才可条件执行一次 H2-B 双文档 smoke。`S6.1-P1 = NOT STARTED`，`FORMAL_EXPERIMENT = NOT STARTED`。本页只提供入口导航与文档职责，不保存完整运行历史。

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
- [S6.1-R0-FU1 工作过程](stage_process/S6.1-R0-FU1_work_process.md) — P0/L1 已验收；H2 已批准、未发送、未执行；父 W2 仍未完成或验收。

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
- [W2 Attempt 1 Control Plane Review](s6_1_r0_fu1_w2_attempt1_control_plane_review.md)

Raw evidence、模型 bundle 和私有 archive 保持 Git-external；这里只保存可审计身份、结论边界和复核索引。

## 五、高级治理与审计

- [Current Work State](../../governance/current_work_state.md) — 项目动态状态控制面。
- [Experiment Master Record](../../governance/experiment_master_record.md) — 跨阶段实验/工程事实与 blocker 主记录。
- [Research Execution Log](../../governance/research_execution_log.md) — 项目级追加式审计时间线，不是 Paper 1 人类总账。
- [Project Owner Decision Register](../../governance/project_owner_decision_register.md) — 项目需求提出人确认决定记录。

职责规则：用户需求只进入需求登记册；当前方案只进入研究方案权威文件；阶段事实只追加到该阶段 work process；人类总览和 agentUse 保持同一状态；上下文恢复不产生新授权；审计日志不复制完整实验总账。
