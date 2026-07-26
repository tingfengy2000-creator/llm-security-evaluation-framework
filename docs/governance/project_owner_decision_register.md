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
| PODR-015 | 2026-07-25 | S6-T5.4-I1 Controlled Corpus ContentResolver Minimal Implementation | 批准并完成只依赖合成内存正文的最小实现：精确引用、UTF-8 SHA-256 校验、受控 registry/reader 和 legacy exact-match 映射 | IMPLEMENTED_PENDING_HUMAN_ACCEPTANCE | 项目负责人 I1 批准、完成记录、TDD 与离线工程验证 | PODR-014 | 不代表正文 fixture 已读取、正式 RAG 安全实验、ContextBuilder/Citation 或 S6-T5.5 获批 |
| PODR-016 | 2026-07-25 | S6-T5.4 Controlled Corpus ContentResolver Human Acceptance Record | 接受 P1 协议、I1 最小实现、H1 capability/failure-boundary 加固与父任务；确认其只覆盖合成内存工程边界 | HUMAN_ACCEPTED | 项目负责人明确决定、`11a72f7`、完成记录与治理测试 | PODR-013、PODR-014、PODR-015 历史快照 | 不批准 S6-T5.5、EvidenceEnvelope、Citation、ContextBuilder、真实正文 provider 或正式 RAG 实验 |
| PODR-017 | 2026-07-25 | S6-T5.5-P1 EvidenceEnvelope and Citation Boundary Freeze | 批准协议审查，采用无 `citation_id` Envelope 与由未来 ContextBuilder 在最终 Evidence 集后创建 package-local Binding 的方案；冻结 instruction、escaping、错误和敏感导出边界 | DESIGN_FREEZE_COMPLETED_PENDING_HUMAN_ACCEPTANCE | 项目负责人当前指令、S6-T5.5 protocol review record、规格/计划/ADR | — | 不批准 S6-T5.5 业务实现、CitationBinding、rendering、ContextBuilder 或正式 RAG 实验 |
| PODR-018 | 2026-07-26 | S6-T5.5-P1-H1 Evidence Canonical Binding and Citation Rendering Protocol Hardening | 批准修订 Factory canonical Evidence-only 输入、Renderer 的 Envelope + Binding 唯一输入和 `CITATION_BINDING_MISMATCH` fail-closed 语义 | DESIGN_FREEZE_HARDENING_COMPLETED_PENDING_HUMAN_REVIEW | 项目负责人当前指令、S6-T5.5 protocol review record、规格/计划/ADR | PODR-017 ambiguous legacy/renderer boundary | 不批准 S6-T5.5 业务实现、Binding/renderer/ContextBuilder 或正式 RAG 实验 |
| PODR-019 | 2026-07-26 | S6-T5.5 EvidenceEnvelope and Citation Protocol Human Acceptance Record | 人工接受 P1 与 H1 的协议设计；S6-T5.5 仅进入独立实现审批准备 | HUMAN_ACCEPTED | 项目负责人明确决定、P1/H1 protocol review record、规格/计划/ADR、治理测试 | PODR-017、PODR-018 的历史 pending/review 快照 | 不批准 S6-T5.5-I1、EvidenceEnvelope、CitationBinding、renderer、ContextBuilder 或正式 RAG 实验 |
| PODR-020 | 2026-07-26 | S6-T5.5-I1 EvidenceEnvelope, Citation Contracts and Structural Rendering Minimal Implementation | 批准并完成 synthetic-only 的 stable DTO、canonical Factory、instruction 与 single-block renderer 最小实现 | IMPLEMENTED_PENDING_HUMAN_ACCEPTANCE | 项目负责人当前批准、完成记录、TDD 与离线工程验证 | PODR-019 | 不批准 ContextBuilder、package-level allocation、Trust、LLM 或正式 RAG 实验 |
| PODR-021 | 2026-07-26 | S6-T5.5-H1 Evidence and Citation Contract Immutability and Validation Hardening | 修复 I1 人工验收发现：metadata 不可变、timestamp 兼容、固定 Envelope/Binding 错误与 canonical Evidence UID | IMPLEMENTED_PENDING_HUMAN_REVIEW | 项目负责人当前批准、protocol review record、completion record、TDD 与离线工程验证 | PODR-020 | 不批准 S6-T5.6、ContextBuilder、Package、allocator、Trust、LLM 或正式 RAG 实验 |
| PODR-022 | 2026-07-26 | S6-T5.5 Evidence Envelope and Citation Implementation Human Acceptance Record | 人工接受 I1、H1 与父任务；`6da27a6` 为最终接受的 implementation commit | HUMAN_ACCEPTED | 项目负责人明确决定、completion record、protocol review record、治理测试 | PODR-020、PODR-021 的历史 pending/review 快照 | 不批准 S6-T5.6+、ContextBuilder、Trust、LLM 或正式 RAG 实验 |
| PODR-023 | 2026-07-26 | S6-T5.6-P1 Context Package Boundary Freeze | 批准只进行 ContextBuilder、预算、Package、Citation 临时绑定和结构性 abstention 的协议审查 | DESIGN_FREEZE_COMPLETED_PENDING_HUMAN_ACCEPTANCE | 项目负责人明确决定、S6-T5.6 protocol review record、设计/治理测试 | PODR-022 的后续独立协议任务 | 不批准任何 S6-T5.6 实现、ContextBuilder、Package、allocator、Trust、LLM 或正式 RAG 实验 |
| PODR-024 | 2026-07-26 | S6-T5.6-P1-H1 Sequential Resolution, Duplicate Semantics and Context Trace Protocol Hardening | 批准只修订 P1 的顺序解析、精确 UID 重复语义、预算 cutoff 与 Context trace 身份缺口 | DESIGN_FREEZE_HARDENING_COMPLETED_PENDING_HUMAN_REVIEW | 项目负责人明确决定、S6-T5.6 protocol review record、设计/治理测试 | PODR-023 historical selection wording | 不批准任何 S6-T5.6 实现、ContextBuilder、Package、allocator、Trust、LLM 或正式 RAG 实验 |
| PODR-025 | 2026-07-26 | S6-T5.6-P1-H2 Active Specification, Trace Decision and Package Identity Protocol Closure | 批准只关闭活动规格顺序、instruction-budget candidate decision、Trace decision partition 与 Package/Trace identity 的协议矛盾 | DESIGN_FREEZE_HARDENING_COMPLETED_PENDING_HUMAN_REVIEW | 项目负责人明确决定、S6-T5.6 protocol review record、设计/治理测试 | PODR-024 remaining active-spec and identity ambiguity | 不批准任何 S6-T5.6 实现、ContextBuilder、Package、allocator、Trust、LLM 或正式 RAG 实验 |
| PODR-026 | 2026-07-26 | GOV-S6-T5.6-P1-ACCEPTANCE Context Package Protocol Human Acceptance Record | 接受 S6-T5.6-P1、P1-H1、P1-H2 的协议边界；父任务进入 READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL | HUMAN_ACCEPTED | 项目负责人明确决定、`432b07e`、S6-T5.6 protocol review record、治理测试 | PODR-023、PODR-024、PODR-025 的 pending/review 历史快照 | 不批准 S6-T5.6-I1、ContextBuilder、Package、Trace、budgeter、allocator、Trust、LLM 或正式 RAG 实验 |

## 7.1 S6-T5.4 当前审批解释（2026-07-25）

PODR-014 supersedes PODR-013 中“P1 执行结果仍为 pending”的当前状态解释：`S6-T5.4-P1` 当前为
`HUMAN_ACCEPTED`，blocker 当前为 `RESOLVED_BY_APPROVED_PROTOCOL_FREEZE`，父任务当前为
`READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL`。这不构成实现批准；`S6-T5.4-I1` 为 `NOT YET APPROVED`，
`S6-T5.5` 及之后为 `NOT APPROVED`，正式 RAG 安全实验为 `NOT STARTED`。

## 7.2 S6-T5.4-I1 当前实现状态（2026-07-25）

PODR-015 是对 7.1 历史审批快照的后续事实登记：项目负责人已单独批准并完成 `S6-T5.4-I1`，其当前状态为
`Completed, pending human acceptance`。实现仅使用测试内的合成内存正文，不读取 Stage 6 fixture、不生成 fixture
mapping、不调用 Chroma、Embedding、Groq 或 LLM；父任务 `S6-T5.4` 同样为 `Completed, pending human acceptance`。
`S6-T5.5` 及后续任务仍为 `NOT APPROVED`，正式 RAG 安全实验仍为 `NOT STARTED`。

## 7.3 S6-T5.4 最终人工验收状态（2026-07-25）

PODR-016 是对前述 pending 状态历史快照的当前事实登记：`S6-T5.4-P1`、`S6-T5.4-I1`、`S6-T5.4-H1` 与
`S6-T5.4 Controlled Corpus ContentResolver` 当前均为 `HUMAN_ACCEPTED`；最后接受的实现提交为 `11a72f7`。
该验收仅确认 contracts 唯一敏感 DTO、最小 `resolve()` capability、受控 registry/reader、原始 UTF-8 hash、
legacy exact-match、fail-closed identity/integrity、异常脱敏与 cause 保留，以及合成内存验证边界。它不批准
S6-T5.5、EvidenceEnvelope、Citation、ContextBuilder、真实正文 provider、LLM 或正式 RAG 安全实验。

## 7.4 S6-T5.5-P1 协议审查当前状态（2026-07-25）

PODR-017 只批准 `S6-T5.5-P1` 进行设计审查。当前审查完成，状态为 `Completed, pending human acceptance`：
`EvidenceEnvelope` 不含 `citation_id`；future S6-T5.6 ContextBuilder 在最终 Evidence 集合确定后创建
`CitationBinding` 并按 package-local 顺序分配 `E1 ... En`。未来 factory、instruction、XML-like rendering、错误
归属和敏感导出规则均被冻结，但没有实现源码。`S6-T5.5`、S6-T5.6+ 和正式 RAG 安全实验仍为 `NOT APPROVED`/`NOT STARTED`。

## 7.5 S6-T5.5-P1-H1 协议加固当前状态（2026-07-26）

PODR-018 只批准 P1 的人工审查发现项修订。H1 已完成、待人工复核：Factory 只接受 canonical `corpus:`
RetrievalEvidence 且逐项检查 ContentRef、snapshot、chunk、hash；legacy `chroma:` 只在 Resolver 输入转换，不能进入
Factory。renderer 只接受 Envelope + Binding，七项 identity 任一不一致即为 `CITATION_BINDING_MISMATCH`，固定脱敏
外部消息为 `citation binding does not match evidence`，不作为 abstention。P1 仍待人工验收；S6-T5.5、S6-T5.6+ 与
正式 RAG 安全实验仍为 `NOT APPROVED`/`NOT STARTED`。

## 7.6 S6-T5.5-P1 与 P1-H1 人工验收当前状态（2026-07-26）

PODR-019 将 `S6-T5.5-P1` 与 `S6-T5.5-P1-H1` 标记为 `HUMAN_ACCEPTED`，但只接受其设计协议：无
`citation_id` Envelope、future package-local Binding allocation、canonical Factory 输入、七字段 Binding
校验、`CITATION_BINDING_MISMATCH` fail-closed、固定 instruction/rendering 与敏感导出 deny-by-default。该决定不把
`25fb83d` 登记为业务实现提交；最后接受的 stage implementation 仍是 `S6-T5.4 Controlled Corpus ContentResolver`
的 `11a72f7`。本段的 `S6-T5.5` 为 `READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL` 是 I1 获批前的历史快照；当前 `S6-T5.5` 与 `S6-T5.5-I1` 均为 `Completed, pending human acceptance`，但
`NOT YET APPROVED`，`S6-T5.6+` 为 `NOT APPROVED`，正式 RAG 安全实验为 `NOT STARTED`。

## 7.7 S6-T5.5-I1 当前状态（2026-07-26）

PODR-020 单独批准了 I1 的离线工程实现。当前 `EvidenceEnvelope`、`CitationBinding`、`CitationMode`、稳定错误、
canonical Factory、citation instruction 与单 block structural renderer 已完成，状态为 `Completed, pending human
acceptance`。所有正文均为测试中的 synthetic 对象；没有读取 Stage 6 fixture、创建 package/allocator/ContextBuilder，
也没有调用 Embedding、Chroma、Groq、LLM 或正式 RAG 实验。最后接受的业务实现提交仍为 `11a72f7`。

## 7.8 S6-T5.5-H1 当前状态（2026-07-26）

PODR-021 记录 I1 人工验收发现项的最小修复：metadata wrapper 无 `__dict__` 且不可重绑，Envelope timestamp 与
RetrievalEvidence 的 canonical UTC 语义对齐，metric/metadata/ID input 对外固定脱敏，Binding 字段错误使用
`INVALID_CITATION_BINDING`，Evidence UID 严格为 `EV-[0-9a-f]{64}`。当前 H1 为 `Completed, pending human review`；
I1 和父任务仍为 `Completed, pending human acceptance`。这不改变 `11a72f7` 仍是最后接受的业务实现提交，也不批准
S6-T5.6+ 或正式 RAG 安全实验。

## 7.9 GOV-S6-T5.5-ACCEPTANCE：Evidence 与 Citation 实现人工验收（2026-07-26）

PODR-022 记录项目负责人对 `S6-T5.5-I1`、`S6-T5.5-H1` 和父任务 `S6-T5.5` 的人工验收。当前三者均为
`HUMAN_ACCEPTED`；最后接受的 stage task 为 `S6-T5.5 EvidenceEnvelope, Citation Contracts and Structural
Rendering`，最后接受的 implementation commit 为 `6da27a6`。`2cacef7` 保留为 I1 的初始实现历史，不能被
`6da27a6` 覆盖或删除。

本验收确认的边界是：contracts 唯一 DTO owner、canonical Factory、不可变公开 metadata、canonical UTC timestamp、
Evidence UID、CitationBinding 七字段 identity 校验、固定脱敏错误、固定 instruction 与单 block structural rendering。
它只覆盖 synthetic objects 上的离线工程行为，不证明 Citation Accuracy、检索质量、检索安全、ContextBuilder、
RetrievedContextPackage、Trust、LLM 集成、生产可用性或正式 RAG 安全实验结果。

第 7.6--7.8 节中的 pending/review 文字为当时的历史快照，必须保留；本节是 superseding current decision。
`S6-T5.6` 为 `NOT APPROVED`，`S6-T5.7+` 为 `NOT APPROVED`，Formal RAG security experiment 为 `NOT STARTED`。

## 7.10 S6-T5.6-P1 Context Package 协议审查当前状态（2026-07-26）

PODR-023 只批准设计冻结，不批准业务实现。当前 P1 为 `Completed, pending human acceptance`，冻结
`ContextBuildConfig`、唯一 ContextBuilder Protocol、Request/Evidence provenance、稳定 sort/dedup、数量限制、
ContentResolver/EnvelopeFactory 顺序、临时 Citation Binding、Unicode code point budget、safe build trace、
`RetrievedContextPackage`、package ID 和结构性 abstention 边界。临时 Binding 只在单次 build 调用栈内用于精确
renderer 预算计算，未被纳入最终 Package 前不消耗 Citation ID。

父任务 `S6-T5.6`、`S6-T5.7+` 和正式 RAG security experiment 分别仍为 `NOT APPROVED`、`NOT APPROVED` 和
`NOT STARTED`。最后接受的 implementation commit 仍为 `6da27a6`。本冻结不实现 ContextBuilder、
RetrievedContextPackage、budgeter 或 Citation allocator，也不读取 fixture 或调用 Embedding、Chroma、Groq 或 LLM。

## 7.11 S6-T5.6-P1-H1 协议加固当前状态（2026-07-26）

PODR-024 只批准设计缺口修订。H1 当前为 `Completed, pending human review`；P1 仍为
`Completed, pending human acceptance`。它将 active path 固定为先做 provenance、稳定排序、精确 UID
duplicate/conflict 和数量限制，再执行 citation instruction 与 sequential resolution。instruction 单独超预算
不得调用 Resolver；第一个无法完整收录的候选触发停止，后续候选不得访问正文或调用 factory/renderer。

H1 还冻结单向 `ContextBuildTrace -> trace_hash -> Package context_build_trace_hash` 身份关系，并保留
`NO_EVIDENCE_AFTER_DEDUPLICATION` 作为历史快照而非 active code。父任务 `S6-T5.6`、`S6-T5.7+` 与正式实验仍为
`NOT APPROVED`、`NOT APPROVED` 和 `NOT STARTED`；没有业务代码、fixture 读取、模型调用或正式实验。

## 7.12 S6-T5.6-P1-H2 协议闭环当前状态（2026-07-26）

PODR-025 只批准协议矛盾闭环。P1 与 H1 当前为 `Completed, pending human acceptance`；H2 为
`Completed, pending human review`。H2 直接修订 active specification、plan 和 ADR，使其使用同一 sequential
resolution order；instruction-budget exhaustion 有独立 candidate decision；
Trace 的各 UID tuple 是按稳定顺序的完整不相交划分；Package 只持有 `build_trace`，身份 payload 从
`build_trace.trace_hash` 派生 `context_build_trace_hash`。

这不批准任何 ContextBuilder、RetrievedContextPackage、ContextBuildTrace、budgeter 或 Citation allocator
实现。父任务 `S6-T5.6`、`S6-T5.7+` 和正式实验仍为 `NOT APPROVED`、`NOT APPROVED` 与 `NOT STARTED`。

## 7.13 GOV-S6-T5.6-P1-ACCEPTANCE 当前审批解释（2026-07-26）

项目负责人已接受 S6-T5.6-P1、S6-T5.6-P1-H1 和 S6-T5.6-P1-H2。它们的当前状态均为
`HUMAN_ACCEPTED`；S6-T5.6 仅变为 `READY_FOR_SEPARATE_IMPLEMENTATION_APPROVAL`，并不批准
`S6-T5.6-I1`。I1 当前为 `NOT YET APPROVED`，S6-T5.7+ 仍为 `NOT APPROVED`，正式 RAG 安全实验仍为
`NOT STARTED`。

本次接受仅覆盖 future ContextBuilder 接口/依赖边界、稳定排序和精确 UID 去重、数量限制、citation instruction 后的
sequential resolution、temporary `E{n+1}` Binding、真实 renderer 的 Unicode code-point 预算、fit 后提交、
stable-prefix cutoff、instruction 超预算零次 Resolver 调用、cutoff 后无正文访问、完整候选决策分区、Package 仅持有
`build_trace`、从 `build_trace.trace_hash` 派生 package identity、结构性 abstention/integrity failure 分离及无正文
safe audit。它不证明任何实现、Citation Accuracy、检索质量/安全效果、知识污染检测、可信检索、LLM 集成、正式实验或生产可用性。

最后已接受 implementation commit 仍为 `6da27a6`。`432b07e` 是协议闭环提交和本次验收的证据来源，不能登记为
implementation commit。历史 pending/review 文本继续保留为当时事实，不重写为当前状态。

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
