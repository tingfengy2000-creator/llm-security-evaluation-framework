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

题目范围登记：

- `TITLE_INTENT = CONFIRMED`
- `DETOXIFICATION_TECHNICAL_SCOPE = SCOPE_CONFIRMATION_REQUIRED`

## 尚未由用户确认的建议

以下内容不得当作已批准方案：

| 建议 ID | 内容 | 当前状态 | 进入已确认区的条件 |
| --- | --- | --- | --- |
| OS-001 | 自动过滤进入 Paper 1 | `SCOPE_CONFIRMATION_REQUIRED` | 项目需求提出人明确确认 |
| OS-002 | 自动重排进入 Paper 1 | `SCOPE_CONFIRMATION_REQUIRED` | 项目需求提出人明确确认 |
| OS-003 | trusted context package 进入 Paper 1 | `SCOPE_CONFIRMATION_REQUIRED` | 项目需求提出人明确确认 |
| OS-004 | 运行时可信检索进入 Paper 1 | `SCOPE_CONFIRMATION_REQUIRED` | 项目需求提出人明确确认 |
| OS-005 | 完整解毒系统进入 Paper 1 | `SCOPE_CONFIRMATION_REQUIRED` | 项目需求提出人明确确认 |
| OS-006 | H2 设计 | 历史状态 `PROPOSED / NOT CANONICAL / NOT APPROVED`；现已由 OR-017 supersede | 已由项目需求提出人明确批准，历史记录保留 |
