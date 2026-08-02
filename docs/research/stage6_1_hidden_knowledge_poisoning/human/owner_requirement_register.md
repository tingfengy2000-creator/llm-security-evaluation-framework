# Paper 1 用户确认需求登记册

> 文档职责：`PAPER1_OWNER_REQUIREMENT_AUTHORITY`。这是 Paper 1 中唯一登记项目需求提出人已明确确认需求的入口。建议、推断和草案不得进入主表。

| 需求 ID | 日期 | 用户明确需求 | 类型 | 影响范围 | 当前状态 | 对应阶段 | 证据来源 | 替代关系 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OR-001 | 2026-07 | Paper-first，优先形成可发表的比较证据 | 研究方向 | Paper 1 全局 | 已确认 | S6.1-LR1+ | PODR-036 | 无 |
| OR-002 | 2026-07 | 聚焦中文版本化隐蔽知识污染 | 研究方向 | 问题、威胁模型、数据 | 已确认 | S6.1-LR1+ | Paper 1 路线与决策登记 | 无 |
| OR-003 | 2026-07 | PoisonedRAG 为攻击基线、GMTP 为检测基线、SafeRAG 为 Benchmark 参考 | Baseline 选择 | Track A | 已确认 | S6.1-LR1/R0 | PODR-036 至 PODR-040 | 无 |
| OR-004 | 2026-07 | 本机负责控制、复核和轻量准备；5090负责获批计算工作 | 机器分工 | 执行治理 | 已确认 | R0/FU1 | 双机策略与 PODR 记录 | 替代旧机器别名表达 |
| OR-005 | 2026-07 | 工程验证不得冒充论文结果 | 结论边界 | 全部阶段 | 已确认 | 全局 | 决策登记与验收记录 | 无 |
| OR-006 | 2026-07 | 研究上下文必须以 Git 文件物理保存 | 上下文保存 | 恢复治理 | 已确认 | 全局 | Context Recovery 验收 | 无 |
| OR-007 | 2026-08-01 | 人类文档与 LLM 文档分离 | 文档体系 | Paper 1 文档 | 已确认 | DOC-RESTRUCTURE-02 | 本任务批准文本 | 无 |
| OR-008 | 2026-08-01 | 建立中文 `tingfeng` 实验总账作为人类总入口 | 文档体系 | 人类阅读 | 已确认 | DOC-RESTRUCTURE-02 | 本任务批准文本 | 无 |
| OR-009 | 2026-08-01 | 建立派生的 `agentUse` 结构化实验总账 | 文档体系 | 智能体恢复 | 已确认 | DOC-RESTRUCTURE-02 | 本任务批准文本 | 无 |
| OR-010 | 2026-08-01 | 建立唯一用户确认需求登记册 | 架构要求 | 需求权威 | 已确认 | DOC-RESTRUCTURE-02 | 本任务批准文本 | 无 |
| OR-011 | 2026-08-01 | 建立唯一当前研究方案权威文件 | 架构要求 | 方案权威 | 已确认 | DOC-RESTRUCTURE-02 | 本任务批准文本 | 无 |
| OR-012 | 2026-08-01 | 每阶段仅有一个 canonical 工作过程文件 | 架构要求 | 阶段历史 | 已确认 | DOC-RESTRUCTURE-02 | 本任务批准文本 | 无 |
| OR-013 | 2026-08-01 | 中文题目采用《面向中文检索增强生成系统的版本感知隐蔽知识污染基准与多视角解毒方法》 | 论文题目 | 论文身份 | 题目意图已确认 | Paper 1 | 本任务批准文本 | 更新中文题目表达 |
| OR-014 | 2026-08-01 | 原始证据、失败、hash 与 revision 必须保存，整改采用追加式记录 | 结论边界 | 证据体系 | 已确认 | 全局 | 本任务批准文本 | 无 |
| OR-015 | 2026-08-01 | README 只作快速状态、职责说明与导航 | 文档体系 | Start Here | 已确认 | DOC-RESTRUCTURE-02 | 本任务批准文本 | 降级原 README 历史堆叠 |
| OR-016 | 2026-08-01 | 项目执行日志只保留追加式审计时间线，不承担 Paper 1 人类总账职责 | 文档体系 | 项目审计 | 已确认 | DOC-RESTRUCTURE-02 | 本任务批准文本 | 明确职责，不改写历史 |
| OR-017 | 2026-08-01 | 继续实验并批准 `S6.1-R0-FU1-W2-H2`：5090 先完成 H2-A 离线模型包验证，全部通过后才可在同一合同内执行一次 H2-B 双文档 GMTP detection-core 工程 smoke；完成或遇到 blocker 后停止，不批准 P1、数据集、Detector、训练或正式实验 | 实验批准 | FU1/W2/H2 | `APPROVED_TO_START / NOT SENT / NOT EXECUTED` | S6.1-R0-FU1-W2-H2 | 当前任务批准文本；H2 审批基础 `212911a21dc35bef05b15fb840542403c415dd13` | supersede OS-006 的批准前历史状态 |
| OR-018 | 2026-08-01 | 确认 bundle 与 sidecar 已同步到 5090；保留非空 `resume_01` blocker evidence，不覆盖、不删除；批准改用全新 `resume_02` 从 H2-A 重新开始，并使用新的 resume02 archive；除证据命名空间外合同不变 | 实验继续批准 | FU1/W2/H2 | `RESUME_02 APPROVED_TO_START / NOT EXECUTED` | S6.1-R0-FU1-W2-H2-RESUME-02 | 当前任务明确确认；resume_01 evidence 与本机复核 | 不授权 resume_03、重复 H2-B、P1 或正式实验 |
| OR-019 | 2026-08-01 | 后续 5090 输出仍同步到 E 盘 `LLMGuard-Handoff` 文件夹；本次误同步到 D 盘 `llmProject/handoff` 仅为单次例外，不改变冻结计算端输出路径 | 工件交接规则 | 本机/5090 证据传递 | 已确认 | FU1 及后续获批计算任务 | 项目需求提出人当前明确说明 | 不移动或改写既有证据；不把 D 盘例外变成新规范 |
| OR-020 | 2026-08-02 | 正式验收父 W2 为 `HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED` 并关闭 FU1；只接受冻结单样本 detection-core 工程可行性；准备 P1 协议候选但不批准、不启动 P1，不扩大论文结论；解毒 A/B/C 范围须后续人工选择 | 最终验收与下一阶段范围门 | FU1/W2/P1 candidate | W2/FU1 accepted and closed；P1 candidate pending | S6.1-R0-FU1-W2；S6.1-P1 | owner 明确指令；验收基础 `b19fc59cc5ba771fd547430f6096403720ef1a7d`；PODR-061 | 禁止 5090/H2/GMTP/model、Dataset、Detector、Training、Formal Experiment 或 Paper Result 自动推进 |
| OR-021 | 2026-08-02 | 明确选择 `DETOXIFICATION_OPTION = OPTION_B`，确认 Paper 1 技术范围为 Benchmark、多视角检测、风险/信号/解释，以及轻量 hard filtering 或 soft downweighting，并以安全—效用双主结果评估；trusted context package、完整上下文构造、多证据可信上下文生成、复杂端到端 Agent 防御、生产级 RAG 平台和完整可信检索链留给 Paper 2 或后续研究 | Paper 1 技术范围冻结 | Paper 1 / P1-R1 | `OPTION_B_CONFIRMED`；协议强化候选待审 | S6.1-P1-R1 | 项目需求提出人本轮明确选择；PODR-062 | 只冻结范围与审批级候选；不批准 P1、Pilot、Dataset、Detector、Retrieval Intervention、Training 或 Formal Experiment |
| OR-022 | 2026-08-02 | 验收 P1-R1 为协议框架，数值参数仍待 Pilot 证据；批准本机优先实施 PILOT0 的 schema、标签隔离、group/split、leakage、attack contract、轻量 intervention、manifest 与纯合成 fixture；强制禁止低价值 churn、真实数据、模型、5090、GMTP、训练和正式实验 | 协议框架验收与基础设施批准 | Paper 1 / P1-PILOT0 | `P1-R1 HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK`；`PILOT0 APPROVED_TO_IMPLEMENT` | S6.1-P1-PILOT0 | 项目需求提出人当前任务批准文本 | 仅授权工程基础设施；真实数据/标注 Pilot、240 groups、矩阵与 formal protocol 仍需独立批准 |

题目范围登记：

- `TITLE_INTENT = CONFIRMED`
- `DETOXIFICATION_OPTION = OPTION_B`
- `DETOXIFICATION_TECHNICAL_SCOPE = OPTION_B_CONFIRMED`
- `DETOXIFICATION_TECHNICAL_SCOPE_FULL = OPTION_B_DETECTION_AND_LIGHTWEIGHT_RETRIEVAL_INTERVENTION`

## 尚未由用户确认的建议

以下内容不得当作已批准方案：

| 建议 ID | 内容 | 当前状态 | 进入已确认区的条件 |
| --- | --- | --- | --- |
| OS-001 | 自动过滤进入 Paper 1 | `ACCEPTED_NARROWLY_BY_OR-021` | 仅指基于冻结风险阈值的轻量 hard filtering |
| OS-002 | 自动重排进入 Paper 1 | `ACCEPTED_NARROWLY_BY_OR-021_AS_SOFT_DOWNWEIGHTING` | 仅指检索分数减去风险惩罚；不含完整 reranker 或可信检索链 |
| OS-003 | trusted context package 进入 Paper 1 | `EXCLUDED_FROM_PAPER1_BY_OR-021 / RESERVED_FOR_PAPER2` | 需后续独立需求与批准 |
| OS-004 | 运行时可信检索进入 Paper 1 | `EXCLUDED_EXCEPT_NARROW_OPTION_B_INTERVENTION / RESERVED_FOR_LATER` | Paper 1 只含 hard filtering / soft downweighting，不含完整可信检索链 |
| OS-005 | 完整解毒系统进入 Paper 1 | `EXCLUDED_FROM_PAPER1_BY_OR-021 / RESERVED_FOR_LATER` | 需后续独立需求与批准 |
| OS-006 | H2 设计 | 历史状态 `PROPOSED / NOT CANONICAL / NOT APPROVED`；现已由 OR-017 supersede | 已由项目需求提出人明确批准，历史记录保留 |
