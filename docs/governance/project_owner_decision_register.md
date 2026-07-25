# LLMGuard 项目负责人确认需求与决策登记册

*Project Owner Confirmed Requirements and Decision Register*

## 0. 文档职责与使用规则

本文仅记录项目负责人已经明确确认的需求、解释和决策，供新的 Codex Thread、ChatGPT 对话、Workspace 或
Worktree 在旧对话不可用时恢复项目治理上下文。

本文不替代以下权威来源：

- `docs/governance/long_term_research_requirements.md`：长期能力需求与研究方向；
- `PROJECT_MASTER_CONTEXT.md`：总体架构、阶段叙事与结论边界；
- `docs/governance/current_work_state.md`：当前任务和审批门；
- `docs/governance/experiment_master_record.md`：实验控制面、证据索引和原始工件入口；
- ADR、设计规格、实施计划和 Git：分别负责设计、实施顺序和动态工程事实。

未经项目负责人明确确认的内容不得登记为 `ACCEPTED`；不确定内容必须标记为
`PENDING_CONFIRMATION` 或 `UNKNOWN`。后续决策改变时使用 superseding entry 保留历史，不静默删除。
Git 仍决定 branch、HEAD、commit、文件存在性和同步状态。

## 1. 项目身份与用途

- 英文正式名称：**LLMGuard Research Framework**。
- 中文正式名称：**LLMGuard 大模型安全评测与可信检索研究框架**。
- 规范 Python namespace：`llmguard`；`codeguarder` 仅为 legacy namespace。
- 新业务代码只进入 `src/llmguard/`；Stage 1–5 是不可变历史实验资产。

项目同时服务于大模型安全岗位面试、英文论文、科技项目立项和后续 Agent 安全研究。它们共享研究内核，
但不共享证据粒度：面试叙事不能替代论文方法和统计证据，工程测试不能替代正式实验结论。

固定优先级如下：

1. RAG Security Research
2. LLM Security Evaluation Platform
3. AI Guard Engineering
4. Agent Security Extension

## 2. 论文、立项与阶段路线

固定两篇论文路线：

- Paper 1：Stage 6.1 Hidden Knowledge Poisoning Detection（隐蔽知识污染检测）。
- Paper 2：Stage 6.2 Multi-Evidence Trustworthy Retrieval（多证据可信检索）。
- Stage 7：Agent Security Evaluation 是后续扩展，**不属于论文二**，不得重新解释为第二篇论文。

立项正式名称为《面向检索增强生成系统的隐蔽知识污染检测与多证据可信检索关键技术研究》。

阶段路线为：Stage 1 Garak Security Scan Baseline；Stage 2 OpenAI-Compatible Mock API；Stage 3 Real
Model Security Scan；Stage 4 Guard Proxy A/B Evaluation；Stage 4.1 Guard Ablation Evaluation；Stage 5
Runtime Attack Matrix and Failure Taxonomy；Stage 5 Paper Deterministic Runtime Evaluation Baseline；Stage 6
RAG Security Evaluation Baseline；Stage 6.1 Hidden Knowledge Poisoning Detection；Stage 6.2 Multi-Evidence
Trustworthy Retrieval；Stage 7 Agent Security Evaluation。

## 3. 研究、数据与标签隔离

Stage 6 基线优先使用合成、可控、无隐私的企业制度语料；schema 同时支持 enterprise、education 和
research，不把企业领域写死。真实企业内部文件不得直接成为公开论文数据；公开 Artifact 与私有研究仓库
必须分离。

Ground Truth 只能由 Evaluator 或 GroundTruthVault 访问。Retriever、VectorStore、ContextBuilder、Guard、LLM
和 Agent 不得访问或暴露以下 evaluator 标签：

```text
poisoned, poison_label, label, attack_id, attack_goal, attack_category,
expected_answer, expected_behavior, failure_type, ground_truth, oracle,
risk_goal, stealth_level
```

受控无防护实验可以让污染正文进入 Context，但“正文属于污染样本”的标签不得进入运行时链路。

## 4. 稳定 RAG 架构与证据边界

固定目标链路如下；后续能力以增量方式加入，不另建相互竞争的运行时内核：

```text
Query
-> safe projection
-> RetrievalRequest
-> DenseRetriever
-> RetrievalEvidence + RetrievalTrace
-> ContentResolver
-> EvidenceEnvelope + CitationBinding
-> ContextBuilder
-> RetrievedContextPackage
-> EvidenceSignal
-> TrustAggregator
-> RetrievalPolicy
-> TrustedContextPackage
```

Evidence UID、Citation ID、Citation Binding、XML-like Evidence Envelope、citation mode
`off/available/required`、Citation Accuracy、引用支持度、幻觉溯源、Evidence Consistency、Evidence
Trustworthiness 以及 abstention/refusal 是后续不可删除的能力。`RetrievedContextPackage` 表示仅已检索；
只有经过可信分析和策略后才可形成 `TrustedContextPackage`。

## 5. 证据、结论与审批规则

必须区分 `FORMAL_EXPERIMENT`、`ENGINEERING_VALIDATION`、`DESIGN_FREEZE` 与 `FAILED / INVALID RUN`。
Static/Mock 不证明真实语义或生产安全效果；工程验证不等于安全实验；单次真实模型输出不等于统计结论。正式
运行必须记录配置、模型 revision、数据 hash、Git commit 和 RunManifest，且所有结论均限定于当前数据、模型、
配置和策略。

每个 Task 和子任务需要单独批准；设计批准不等于实现批准，前序完成不自动批准后序。严格执行 TDD、独立
提交、blocker 停止留痕和完成后暂停；不得以“先跑起来再补安全”为由越过审批门。

已接受治理事实：`GOV-ER1`、`GOV-ER1-H1`、`GOV-PODR1`、`S6-T5.2`、`S6-T5.3-P1`、`S6-T5.3-H1` 与 `S6-T5.3` 为 `HUMAN_ACCEPTED`。Experiment Master Record
是实验控制面和索引，不替代原始 JSON/JSONL、日志、RunManifest 或阶段报告。

## 6. S6-T5.3 parent identity：历史 blocker 与当前闭环

以下内容是历史快照，不得误写为当前状态：原状态为 `DESIGN_OR_PROTOCOL_BLOCKER`，原因是
`VectorSearchHit` 缺少 `RetrievalEvidence` 必需的 `parent_doc_id`。当时正确处置是停止实现，不猜测
parent identity，不读取语料。

项目负责人批准的解决决策是：`parent_doc_id` 作为公开、非标签、无正文的 provenance metadata。传递链为：

```text
ChunkRecord.parent_doc_id
-> VectorDocument.metadata["parent_doc_id"]
-> VectorSearchHit.metadata["parent_doc_id"]
-> RetrievalEvidence.parent_doc_id
```

版本隔离方案为 public metadata schema `1.0` 保留历史兼容，schema `1.1` 用于 retrieval-ready 公开
metadata；两者使用不同 collection fingerprint，不原地迁移。解决提交为 `2ad3d9c`；DenseRetriever
实现提交为 `bfc329b`；边界澄清提交为 `3c22615`。原 blocker record 保留，其当前历史条目状态为
`RESOLVED_BY_VERSIONED_PUBLIC_METADATA_CONTRACT`。

历史快照中的“已完成、等待人工验收”是当时事实，不得删除。当前事实是：S6-T5.3-P1、DenseRetriever 与
S6-T5.3-H1 均已通过项目负责人 `HUMAN_ACCEPTED`；S6-T5.4 为
`APPROVED_TO_START / DESIGN_OR_PROTOCOL_BLOCKER`，其 P1 协议冻结执行结果为
`Completed, pending human acceptance`；正式 RAG 安全实验为 `Not started`。此前 “S6-T5.4 为 `Not approved`”
属于已保留的历史状态，不能被误读为当前审批门。
不得把“S6-T5.3 已批准但阻塞、未实现 DenseRetriever”写成当前状态。

## 7. 决策台账

| Decision ID | Date | Topic | Decision | Status | Evidence / Source | Supersedes | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PODR-001 | 2026-07-22 | 项目身份与 namespace | 采用 LLMGuard Research Framework、`llmguard` 规范 namespace 与 `codeguarder` legacy facade | ACCEPTED | 长期需求基线、项目负责人确认 | — | 新业务代码只进入 `src/llmguard/` |
| PODR-002 | 2026-07-22 | 研究优先级 | 固定 RAG 安全、评测平台、护栏工程、Agent 扩展四级顺序 | ACCEPTED | 长期需求基线、项目负责人确认 | — | 不因短期演示改变顺序 |
| PODR-003 | 2026-07-22 | 两篇论文路线 | Paper 1 对应 Stage 6.1，Paper 2 对应 Stage 6.2 | ACCEPTED | 长期需求基线、项目负责人确认 | — | 与立项主题一致 |
| PODR-004 | 2026-07-22 | Stage 7 定位 | Stage 7 是 Agent 安全扩展，不属于论文二 | ACCEPTED | 项目负责人确认 | — | 防止论文路线漂移 |
| PODR-005 | 2026-07-22 | 历史资产 | Stage 1–5 为不可变历史实验资产 | ACCEPTED | AGENTS.md、长期需求基线 | — | 仅允许增量 correction log 或新实验 |
| PODR-006 | 2026-07-22 | 审批与 TDD | Task/子任务逐项审批，严格 TDD、独立提交和 blocker 留痕 | ACCEPTED | AGENTS.md、项目负责人确认 | — | 不自动进入下一任务 |
| PODR-007 | 2026-07-22 | 标签隔离 | evaluator 标签与 Ground Truth 不进入运行时检索、生成或 Agent 链路 | ACCEPTED | 长期需求基线、AGENTS.md | — | 字段见第 3 节 |
| PODR-008 | 2026-07-22 | 上下文分级 | 已检索包与可信包分别命名为 RetrievedContextPackage 与 TrustedContextPackage | ACCEPTED | 长期需求基线 | — | Stage 7 仅消费可信包与脱敏安全封装 |
| PODR-009 | 2026-07-22 | GOV-ER1 职责 | Experiment Master Record 是控制面和索引，不替代原始工件或审批门 | ACCEPTED | experiment_master_record.md、项目负责人确认 | — | GOV-ER1 与 GOV-ER1-H1 已 HUMAN_ACCEPTED |
| PODR-010 | 2026-07-22 | parent_doc_id blocker | 保存原 `DESIGN_OR_PROTOCOL_BLOCKER`，并以公开 provenance metadata 解决 | RESOLVED | s6_t5_3_protocol_blocker_record.md、`2ad3d9c` | — | 不删除原 blocker record，不读取语料或猜测身份 |
| PODR-011 | 2026-07-22 | Versioned public metadata carrier | schema 1.0/1.1 隔离；1.1 传递 parent_doc_id，DenseRetriever 只接受 1.1 hit | ACCEPTED | `2ad3d9c`、`bfc329b`、`3c22615` | PODR-010 historical blocker state | 当前 S6-T5.3 Completed, pending human acceptance |
| PODR-012 | 2026-07-25 | S6-T5.3 DenseRetriever 人工验收 | 接受 P1 schema carrier、H1 trace/failure-boundary 加固及 Provider-Neutral DenseRetriever 的离线工程边界 | HUMAN_ACCEPTED | 项目负责人明确决定、`72a2445`、完成记录与治理测试 | — | 不批准 S6-T5.4；不将工程验证改写为正式实验 |
| PODR-013 | 2026-07-25 | S6-T5.4-P1 Content Resolution Contract and Permission Boundary Freeze | 冻结 Resolver 的最小输入、contracts 唯一 ResolvedContent、受控 snapshot reader/registry、legacy exact-match mapping 与稳定错误归属；不批准业务实现或正文读取 | ACCEPTED | 项目负责人正式批准、S6-T5.4 blocker record、S6-T5 design/ADR | — | 决策已接受；P1 执行结果仍为 Completed, pending human acceptance，父任务 blocker 不因此自动解除 |
| PODR-014 | 2026-07-25 | S6-T5.4 Content Resolution Protocol Human Acceptance Record | 接受 P1 的五项协议设计；将 blocker 标记为 RESOLVED_BY_APPROVED_PROTOCOL_FREEZE，父任务进入 READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL | HUMAN_ACCEPTED | 项目负责人明确决定、P1 规格/计划/ADR、blocker record | PODR-013 execution pending state | 不批准 S6-T5.4-I1，不授权正文访问或 ContentResolver 实现，不批准 S6-T5.5 与正式 RAG 实验 |

## 7.1 S6-T5.4 当前审批解释（2026-07-25）

PODR-014 supersedes PODR-013 中“P1 执行结果仍为 pending”的当前状态解释：`S6-T5.4-P1` 当前为
`HUMAN_ACCEPTED`，blocker 当前为 `RESOLVED_BY_APPROVED_PROTOCOL_FREEZE`，父任务当前为
`READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL`。这不构成实现批准；`S6-T5.4-I1` 为 `NOT YET APPROVED`，
`S6-T5.5` 及之后为 `NOT APPROVED`，正式 RAG 安全实验为 `NOT STARTED`。

## 8. 新 Thread 最小读取顺序

1. `AGENTS.md`
2. `docs/governance/long_term_research_requirements.md`
3. `docs/governance/project_owner_decision_register.md`
4. `PROJECT_MASTER_CONTEXT.md`
5. `docs/governance/current_work_state.md`
6. `docs/governance/experiment_master_record.md`
7. 当前 Stage README
8. 当前 design specification
9. 当前 implementation plan
10. Git 最近 commit、branch、HEAD、worktree、status 与 upstream sync

若长期需求与本登记册冲突，必须停止并报告，不得自行覆盖长期基线。
