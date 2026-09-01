# LLMGuard 项目负责人确认需求与决策登记册

*Project Owner Confirmed Requirements and Decision Register*

## 0. 文档职责与使用规则

本文仅记录项目负责人已经明确确认的需求、解释和决策，供新的 Codex Thread、ChatGPT 对话、Workspace 或
Worktree 在旧对话不可用时恢复项目治理上下文。

本文是唯一的 **OWNER-CONFIRMED DECISION AUTHORITY**。聊天摘要、learning material 和模型记忆都不能把未经
确认的内容升级为 Owner Decision。

本文不替代以下权威来源：

- `docs/governance/context_authority_map.md`：权威层级、冲突解决与恢复顺序；
- `docs/governance/long_term_research_requirements.md`：长期能力需求与研究方向；
- `PROJECT_MASTER_CONTEXT.md`：总体架构、阶段叙事与结论边界；
- `docs/governance/current_work_state.md`：当前任务和审批门；
- `docs/governance/experiment_master_record.md`：实验控制面、证据索引和原始工件入口；
- `docs/governance/research_execution_log.md`：append-only 项目推进时间线；
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
| PODR-027 | 2026-07-26 | S6-T5.6-I1 Deterministic Retrieved Context Package Minimal Offline Implementation | 批准只使用 synthetic/offline TDD 实现已验收的 Config、Trace、Package、ContextBuilder、顺序解析、预算选择、package-local Binding 与结构性 abstention | APPROVED_TO_START / IMPLEMENTATION_IN_PROGRESS | 项目负责人本轮明确指令、PODR-026、已接受规格/计划/ADR | PODR-026 protocol acceptance | 不批准 fixture/data 访问、Embedding、Chroma、LLM、Trust、Policy、检索策略、Citation Accuracy、S6-T5.7 或正式 RAG 实验 |

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

## PODR-028: S6-T5.6-I1-H1 Candidate Hardening Record

- Date: `2026-07-26`.
- Decision: permit the narrowly scoped candidate hardening record; it is **not** a human-acceptance decision.
- Status: `S6-T5.6-I1-H1: Completed, pending human acceptance`.
- Scope: only Trace scenario invariants, public configuration-hash identity, injected dependency error redaction, and structural abstention reason/Trace correspondence.
- Historical relation: `71067d1` remains the initial I1 candidate implementation; it is not the last accepted implementation commit.
- Last accepted implementation commit: `6da27a6`.
- Boundaries: no new DTO fields, no protocol expansion, no Stage 1-5 or Stage 6 fixture/data change, no Embedding/Chroma/Groq/LLM invocation, and no formal RAG security experiment.
- Next gate: human acceptance, rejection, or a separately approved scoped review. `S6-T5.7+` remains `NOT APPROVED`.

## PODR-030: S6-T5.7 Controlled Retrieval Context Pipeline Integration Validation

- Date: `2026-07-26`.
- Decision: project owner approved S6-T5.7 to start; candidate static and opt-in real-infrastructure validation is now complete and pending human acceptance.
- Evidence: [S6-T5.7 completion record](s6_t5_7_integration_completion_record.md), integration tests and scoped regressions.
- Scope: existing accepted components only. No frozen DTO/protocol semantics or Stage 1-5 / Stage 6 fixture data changed.
- Real-infrastructure evidence: fixed MiniLM revision and temporary ChromaDB completed vectorization, retrieval, close/reopen, controlled resolution and deterministic context-package identity checks.
- Status boundary: this is not an acceptance decision and does not advance the last accepted implementation commit from `b136ee2`.
- Next gate: S6-T5.7 human acceptance or rejection. `S6-T5.8` is `NOT APPROVED`; Formal RAG security experiment is `NOT STARTED`.

## PODR-031: GOV-S6-T5.7-ACCEPTANCE Integration Human Acceptance

- Date: `2026-07-26`.
- Decision: `S6-T5.7 Controlled Retrieval Context Pipeline Integration` is `HUMAN_ACCEPTED`.
- Accepted evidence: `b6cedf3` is the accepted integration evidence commit. It contains integration tests and governance evidence only, so it must not be recorded as an implementation commit.
- Implementation baseline: last accepted implementation commit remains `b136ee2`.
- Accepted boundary: safe query projection, no-body Evidence/Trace, canonical `corpus:` ContentRef plus hash resolution, Envelope/Citation/Context package composition, stable-prefix no-access cutoff, deterministic identities, fail-closed error boundaries, safe audit, fixed MiniLM plus temporary Chroma close/reopen, and synthetic exact-match legacy `chroma:` mapping.
- Non-claims: no retrieval quality or Recall/MRR/NDCG metric, Citation Accuracy, prompt-injection defense, knowledge-poisoning detection, trustworthy retrieval, generative LLM chain, formal RAG security experiment, or production readiness.
- Environment note: the explicit real integration test uses `local_files_only=False`; only a new environment that explicitly enables the test may download the pinned revision. It is not a default offline CI dependency and is not a blocker.
- Next gate: `S6-T5.8` remains `NOT APPROVED`; Formal RAG security experiment remains `NOT STARTED`.

## PODR-032: S6-T5.8 Documentation Baseline Closure Approval

- Date: `2026-07-26`.
- Decision: project owner approved S6-T5.8 `Documentation Baseline Closure` to start. It may consolidate accepted S6-T5.1--S6-T5.7 evidence, document environment and technical-debt boundaries, and add governance consistency checks only.
- Current status: `Completed, pending human acceptance`.
- Required identity boundary: `b136ee2` remains the last accepted implementation commit; `b6cedf3` remains the accepted integration evidence commit; the T5.8 candidate closure commit is not an accepted baseline SHA before final human acceptance.
- Prohibitions: no `src/`, business-test, Stage 1--5, Stage 6 fixture/data or runtime modification; no Embedding/MiniLM/Chroma/Groq/LLM call; no tag, Stage 6.1 branch, formal RAG security experiment, Trust, reranker, policy, Citation Accuracy or poisoning detector.
- Next gate: project owner acceptance or rejection of the T5.8 candidate baseline closure. Stage 6.1 formal research remains `NOT APPROVED`; Formal RAG security experiment remains `NOT STARTED`.

## PODR-033: S6-T5.8-H1 Baseline Commit Taxonomy and Evidence Mapping Hardening

- Date: `2026-07-26`.
- Decision: project owner approved a documentation-only hardening of the S6-T5.8 candidate report. It may correct commit taxonomy and evidence mapping, and add semantic governance assertions only.
- Start snapshot: `S6-T5.8-H1: APPROVED_TO_START / DOCUMENTATION_HARDENING_IN_PROGRESS`.
- Current status: `Completed, pending human acceptance`.
- Required identity boundary: `b136ee2` remains the last accepted implementation commit; `b6cedf3` remains integration evidence only; `c1e8c16` remains integration acceptance only; `37cccdc` remains the original T5.8 candidate baseline closure commit and is not an accepted baseline SHA.
- Prohibitions: no `src/`, business-test, Stage 1--5, Stage 6 fixture/data or runtime modification; no MiniLM/Chroma/Embedding/Groq/LLM invocation; no tag, research branch, Stage 6.1 approval, or formal RAG security experiment.
- Next gate: a later human-acceptance record may register the completed H1 candidate commit after Git creates it. Parent `S6-T5.8` remains `Completed, pending human acceptance`; Stage 6.1 remains `NOT APPROVED`; Formal RAG security experiment remains `NOT STARTED`.

## PODR-034: GOV-S6-T5-BASELINE-ACCEPTANCE Final Human Acceptance

- Date: `2026-07-27`.
- Decision: project owner marks `S6-T5.8-H1` and `S6-T5.8` as `HUMAN_ACCEPTED`, and marks the `S6-T5 Controlled Retrieval and Traceable Context Baseline` as `HUMAN_ACCEPTED BASELINE`.
- Accepted baseline content commit: `4ecf73a`. It contains the T5.8 documentation closure and H1 taxonomy correction.
- Historical identity preservation: `37cccdc` remains the original candidate baseline closure commit; `b136ee2` remains the last accepted implementation commit; `b6cedf3` remains the last accepted integration evidence commit; `c1e8c16` remains the S6-T5.7 integration governance acceptance commit.
- Current governance identity: `CURRENT_ACCEPTANCE_COMMIT / verify from Git after commit` is a baseline governance acceptance commit only. It must not be recorded as implementation or integration evidence.
- Latest H1 verification snapshot: documentation/governance `22 passed, 381 subtests passed`; architecture `76 passed, 912 subtests passed`; namespace plus label isolation `10 passed, 1199 subtests passed`; Ruff, scoped MyPy, Markdown links, changed-file secret/absolute-path scans, protected-path diff, runtime Git-ignore and `git diff --check` passed. The `.pytest_cache` write-permission warning is non-blocking test-environment noise, not a test failure.
- This acceptance's separate verification snapshot: documentation/governance `22 passed, 388 subtests passed`; architecture `76 passed, 919 subtests passed`; namespace plus label isolation `10 passed, 1199 subtests passed`. These added governance assertions do not overwrite the H1, T5.7 or T5.6 historical validation snapshots.
- Historical integrity boundary: `BLK-HIST-001` remains 110 existing Windows CRLF/LF manifest differences. This acceptance records zero protected-path changes and does not rewrite Stage 1--5 or Stage 6 fixture/data to erase historical debt.
- Non-claims: no RAG security, prompt-injection defense, knowledge/retrieval poisoning detection or mitigation, trustworthy retrieval, Trust score/policy, Citation Accuracy, Recall/Precision/MRR/NDCG research conclusion, generative LLM chain, formal attack matrix, formal RAG experiment, paper conclusion or production-readiness claim.
- Next gate: Stage 6.1 remains `NOT APPROVED`; Formal RAG security experiment remains `NOT STARTED`. This acceptance does not create a tag or research branch.

## PODR-029: GOV-S6-T5.6-ACCEPTANCE Final Human Acceptance

- Date: `2026-07-26`.
- Decision: `S6-T5.6-I1-H1`, `S6-T5.6-I1` and parent `S6-T5.6` are `HUMAN_ACCEPTED`.
- Accepted implementation commit: `b136ee2`.
- Historical preservation: `71067d1` remains the initial candidate implementation history; `6da27a6` remains the previously accepted implementation commit.
- Accepted scope: synthetic/offline deterministic Context Package behavior only, including the 16 approved items in `GOV-S6-T5.6-ACCEPTANCE`.
- Final validation: full Stage 6 offline regression `438 passed, 2837 subtests passed`; Ruff and scoped MyPy passed. `421/2796`, `437/2796` and `438/2833` remain dated pre-final-validation snapshots. The four-subtest increase from `2833` is governance assertion coverage added during acceptance-state synchronization.
- Explicit non-claims: no retrieval-quality, prompt-injection-defense, poisoning-detection, Citation Accuracy, trustworthy-retrieval, Chroma/MiniLM/LLM-chain, formal-experiment or production-readiness claim.
- Gate: `S6-T5.7+` is `NOT APPROVED`; Formal RAG security experiment is `NOT STARTED`.

## PODR-035: S6.1-LR1 Paper-First Comparative Evidence Alignment

- Date: `2026-07-31`.
- Decision: project owner accepts the `Paper-First Comparative Evidence Principle` and approves `S6.1-LR1` research-control-plane work.
- Approved scope: first-party verification of PoisonedRAG, GMTP and SafeRAG papers/repositories; commit and license registry; dataset/model/retriever/Top-K/attack-budget/metric alignment; published-result extraction; hardware and RTX 5090 compatibility planning; reproduction checklist; dual-machine policy; governance synchronization.
- Completion status: `S6.1-LR1: COMPLETED_PENDING_HUMAN_ACCEPTANCE`.
- Research branch: `research/stage6-1-hidden-poisoning`, created from accepted baseline `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`.
- Baseline tag fact: after `git fetch --prune --tags origin`, `s6-t5-rag-baseline-v1` was not present; this task did not create, move or rewrite a tag.
- Source facts: PoisonedRAG current HEAD `f660d72174f06b13fae5163ce656e7b235db858f` with MIT license; GMTP current HEAD `15b48d150f93711371eb8da22c211cd84a0cf4df` and SafeRAG current HEAD `e8f579743b23e0a3937076dcc0792fe29027cba3`, both with no root LICENSE found.
- Prohibitions: no formal PoisonedRAG/GMTP/SafeRAG run, dataset/model download, paid API, detector code, training, formal result table, SOTA claim, S6-T5 baseline mutation or automatic S6.1-P1 start.
- Claims boundary: this is literature/artifact/governance alignment only. `FORMAL_EXPERIMENT = NOT STARTED`.
- Next gate: human acceptance/rejection of S6.1-LR1, followed by separate approval of any S6.1-P1 protocol, environment preparation, smoke test or formal reproduction.

## PODR-036: Git-Native Research Context Recovery and Authority Hierarchy

- Date: `2026-07-31`.
- Decision: 项目负责人要求建立 Git-native Research Context Recovery System，并接受 L0–L9 Authority Hierarchy、
  新 Thread Context Recovery Report、Git dynamic fact priority、冲突 fail-closed 和 append-only execution ledger。
- Status: `ACCEPTED`.
- Authority: Git/raw evidence 决定 branch/SHA/tag/artifact existence；本文是 Owner Decision Authority；
  `current_work_state.md` 是动态任务入口；Experiment Master Record 是实验控制面；Learning 是非权威材料。
- Conflict rule: 新的 owner-confirmed decision 可以 supersede 较旧 route，但历史记录不得删除；无法确认时登记
  `CONTEXT_CONFLICT_BLOCKER` 并停止关键研究工作。
- Scope: governance、documentation、context persistence tests；不授权业务实现、数据/模型下载或实验。
- Evidence: 项目负责人本轮追加治理要求、`context_authority_map.md`、`research_execution_log.md`。
- Next gate: 与 S6.1-LR1 一并人工审核；不自动批准 S6.1-P1。

## PODR-037: Paper-First Priority and Paper 1 External Baseline Roles

- Date: `2026-07-31`.
- Decision: `Paper-First Comparative Evidence Principle` 的优先级为
  `HIGHEST_RESEARCH_METHOD_PRIORITY_FOR_PAPER_WORK`。Paper 1 第一轮角色固定为 PoisonedRAG = Primary Attack
  Baseline、GMTP = Primary Detection Baseline、SafeRAG = Primary Benchmark Reference；EcoSafeRAG = `DEFERRED`。
- Status: `ACCEPTED`.
- Safety precedence: 该方法优先级不覆盖 ethics、privacy、label isolation、immutable historical assets 或 approval gates。
- Comparison integrity: Published Result、Reproduced Result、Our Method Result 必须分栏；不一致条件标记
  `NON_STRICT_COMPARISON`，不得宣称 SOTA improvement。
- Supersedes: 对 EcoSafeRAG 的任何未确认 core-baseline 假设；未经新 Owner Decision 不恢复。
- Evidence: 项目负责人本轮追加治理要求、Paper 1 benchmark matrix 和 comparative evidence principle。

## PODR-038: Paper 1 Direction, First-Version Scope and Version-Aware Definition

- Date: `2026-07-31`.
- Decision: Paper 1 当前方向为 *Stealthy Factual Poisoning in Versioned RAG Knowledge Bases*，核心贡献方向是
  Benchmark + Multi-View Detection。第一版 attack families 固定为 HKP-1 Numeric/Entity、HKP-2
  Condition/Exception、HKP-3 Temporal/Version、HKP-4 Provenance/Source Camouflage。
- Status: `ACCEPTED`.
- First-version views: `Semantic`、`Entity-Claim`、`Provenance`、`Temporal-Version`、`Retrieval-Behavior`；
  Cross-document conflict 暂并入 Entity-Claim / Temporal-Version，避免第一版无限膨胀。
- Version-aware: 指 knowledge-document version、predecessor/successor、effective/expiration/repeal、supersedes、
  amendment、publisher 和 factual changes 的联合关系；不是 Git/model version，也不能退化为版本号大小规则。
- Hard negatives: 必须覆盖合法更新、新版本、例外、历史有效版本、部门差异、自然冲突、OCR/formatting noise
  和 paraphrase。
- Change governance: 新 attack family/view 或重大 route 变化必须经过 Research Route Review，并引用 PODR ID、
  Research Execution Log ID 和 related Git commit。
- Evidence: 项目负责人本轮追加治理要求与 canonical Paper 1 route。

## PODR-039: Dual-Machine Roles and Git Context Sync

- Date: `2026-07-31`.
- Decision: `LOCAL / CONTROL_PLANE` 负责研究决策、Git、代码、protocol、governance 与 result integration；
  `RTX5090 / COMPUTE_WORKER` 负责未来获批的 GPU、reproduction、embedding、model/benchmark execution。
- Status: `ACCEPTED`.
- Context sync: 使用 Git，不使用 Codex memory。Compute Worker 不得自行改变研究路线；发现设计问题必须返回
  `RESEARCH_ROUTE_REVIEW_REQUIRED`。
- Worker gate: branch、RunManifest HEAD、clean tree、dataset snapshot、config hash、model revision 和 environment
  fingerprint 任一不匹配都 fail closed。
- Compatibility boundary: compatibility environment 只能把 blocker 标记为 `MITIGATED`，除非证明算法等价并正式关闭，
  不得写 `RESOLVED_NO_IMPACT`。
- Evidence: 项目负责人本轮追加治理要求、`dual_machine_execution_policy.md`。

## PODR-040: Stage Learning Documentation and Current Stop Boundary

- Date: `2026-07-31`.
- Decision: 建立 `docs/learning/` index、统一 Stage Learning Guide template 和 Stage 6.1 guide；历史
  `deliverables/learning_notes.md` 保留，不一次性重写所有 Stage 1–6 材料。
- Status: `ACCEPTED`.
- Authority: 所有 Learning Guide 都是 `NON_AUTHORITATIVE_EDUCATIONAL_MATERIAL`；每个稳定 Stage 最终应有 guide，
  但它不是 Formal Experiment Acceptance 的前置科学证据。
- Current stop boundary: `S6.1-LR1` 与 Context Recovery Governance 完成后停止，等待人工审核；S6.1-P1、dataset
  generation、Detector implementation、model training、RTX5090 formal run 均保持未批准/未开始。
- Evidence: 项目负责人本轮追加治理要求、`docs/learning/README.md`。

## 8. 新 Thread 最小读取顺序

1. `AGENTS.md`
2. `docs/governance/context_authority_map.md`
3. `docs/governance/long_term_research_requirements.md`
4. `docs/governance/project_owner_decision_register.md`
5. `PROJECT_MASTER_CONTEXT.md`
6. `docs/governance/current_work_state.md`
7. 当前 Stage canonical research route / README
8. 当前 task protocol/spec/plan
9. `docs/governance/experiment_master_record.md` relevant entries
10. `docs/governance/research_execution_log.md` relevant entries
11. Git 最近 commit、branch、HEAD、tag、worktree、status 与 upstream sync

若长期需求与本登记册冲突，必须停止并报告，不得自行覆盖长期基线。

## 7.14 S6-T5.6-I1 最小离线实现完成记录（2026-07-26）

PODR-027 的实施状态更新为 `COMPLETED_PENDING_HUMAN_ACCEPTANCE`。本轮只在
`src/llmguard/domains/retrieval/contracts/` 与 `context/` 实现已冻结的
`ContextBuildConfig`、`ContextBuildTrace`、`RetrievedContextPackage`、唯一 `ContextBuilder`、
顺序正文解析、stable-prefix 预算选择、包内 Citation 分配、结构性 abstention 和脱敏错误边界。

这是 synthetic-only、离线工程实现候选，不是人工验收。最后已接受 implementation commit 仍为 `6da27a6`；
本轮提交只能登记为 candidate implementation commit pending human acceptance。未读取或修改 Stage 6 fixture/data，
未调用 Embedding、Chroma、Groq 或 LLM，未实现 Trust、RetrievalPolicy、reranker、Citation Accuracy 或正式 RAG 实验。
`S6-T5.7+` 仍为 `NOT APPROVED`，Formal RAG security experiment 仍为 `NOT STARTED`。

## PODR-041: S6.1-LR1 Final Human Acceptance

- Date: `2026-07-31`.
- Decision: `S6.1-LR1: HUMAN_ACCEPTED`。
- Accepted commit: `1294632ca0501e7b999a29383780bec49eaa6b04`。
- Accepted scope: Paper 1 literature/benchmark/source-code/hardware/reproduction alignment、research route、external
  baseline roles 与 reproduction planning。
- Non-claims: 不接受或证明 dataset、Detector、training、reproduction result、RTX5090 performance、Paper Result、
  SOTA 或 Formal Experiment。
- Formal status: `FORMAL_EXPERIMENT = NOT STARTED`。

## PODR-042: Context Recovery, Paper-First Principle and Canonical Route Final Acceptance

- Date: `2026-07-31`.
- Decision: `Git-Native Research Context Recovery Governance: HUMAN_ACCEPTED`；`Paper-First Comparative Evidence
  Principle: HUMAN_ACCEPTED`；Paper 1 canonical route 为 `ACCEPTED AS CURRENT RESEARCH ROUTE`。
- Accepted governance commit: `85a565535a38196a7d6003e728b5cb6a2b17fa8a`。
- Boundary: 接受 governance system、context persistence 与当前研究方法/路线，不把 planning 升级为实验事实。
- Historical preservation: PODR-035–040 的 candidate/pending stop snapshots 继续作为当时事实保留。

## PODR-043: Missing S6-T5 Baseline Tag Recovery Approval

- Date: `2026-07-31`.
- Decision: 将 tag 缺失分类为 `EXPECTED_BASELINE_TAG_NOT_PUBLISHED`，不是 S6-T5 baseline 内容错误。
- Authorized tag: annotated `s6-t5-rag-baseline-v1`，必须严格指向
  `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`。
- Authorized message: `Accepted S6-T5 controlled retrieval and traceable context baseline`。
- Safety: 创建前必须验证 target 是 commit 且本地/远端同名 tag 都不存在；若同名 tag 指向其他 SHA，登记
  `BASELINE_TAG_CONFLICT_BLOCKER` 并停止，禁止 force move。
- Dynamic fact: tag 是否已创建、推送及目标 SHA 必须用 Git 核验，不能由本文静态文字替代。

## PODR-044: External Artifact Access, Internal Reproduction and Redistribution Separation

- Date: `2026-07-31`.
- Decision: external artifact 必须分别登记 `SOURCE_ACCESS`、`INTERNAL_REPRODUCTION`、
  `STRICT_COMPARISON_ELIGIBILITY`、`REDISTRIBUTION_ELIGIBILITY`、`CODE_LICENSE` 与 `DATASET_LICENSE`。
- PoisonedRAG: source available；code MIT；future approved internal reproduction available；code redistribution
  permitted subject to MIT conditions；NQ/HotpotQA/MS MARCO dataset terms 独立治理。
- GMTP/SafeRAG: source available；code license unconfirmed；future approved internal research workflow 不因缺少根
  LICENSE 自动阻断；strict comparison pending reproduction validation；redistribution to verify。
- Boundary: 这不是法律结论；明确 upstream 条款必须遵守。不得 vendor 大段未知许可源码或宣称未知许可证类型。
- Public artifact preference: 发布自有 source/config/download/preprocessing scripts/hashes/official links，不默认重托管
  第三方原始数据。

## PODR-045: S6.1-R0 Precedes S6.1-P1

- Date: `2026-07-31`.
- Decision: 当前研究顺序为 `S6.1-LR1 HUMAN_ACCEPTED -> S6.1-R0 -> S6.1-P1 -> Dataset/Detector/Formal Experiment`，
  supersede 先前 `LR1 -> P1 -> environment` 的临时规划。
- Task: `S6.1-R0 Paper 1 Reproduction Environment and Baseline Feasibility Validation`。
- Type: `ENGINEERING_VALIDATION / REPRODUCTION_PREFLIGHT`。
- Status: `DEFINED / NOT STARTED / PENDING OWNER EXECUTION APPROVAL`。
- Future worker: `RTX5090 / COMPUTE_WORKER`；external repositories 位于 LLMGuard 主仓库之外。
- Boundary: 本决策只定义 R0，不批准 clone、install、download、smoke、reproduction 或任何 5090 计算；R0 不产生
  Paper Result，S6.1-P1 仍未开始。
- Next gate: project owner separately approves or rejects `S6.1-R0 EXECUTION`。Auto Continue = NO。

## PODR-046: RTX5090 Compute Worker Bootstrap Human Acceptance

- Date: `2026-07-31`.
- Decision: `S6.1-R0-B0 RTX5090 Compute Worker Bootstrap Validation` is
  `HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY`。
- Machine: `RTX5090 / COMPUTE_WORKER`；Windows 11 Pro 25H2 Build 26200；Intel Core i9-14900；approximately
  64 GiB RAM；ADATA SX8200PNP NVMe approximately 2 TB；NVIDIA GeForce RTX 5090 with PyTorch-reported 31.84 GB VRAM。
- Linux/toolchain: WSL2 + Ubuntu 24.04 LTS；GPU passthrough and WSL `nvidia-smi` PASS；Git 2.43.0；GCC 13.3.0；
  CMake 3.28.3；ripgrep 14.1.0；Miniforge；Conda 26.3.2；`llmguard-paper1` Python 3.11 environment。
- GPU evidence: PyTorch 2.13.0+cu130；PyTorch CUDA Runtime 13.0；CUDA available；Compute Capability `(12, 0)`；
  `sm_120`；FP16 `RTX5090_GPU_TEST_OK`；BF16 `BF16_TEST_OK`。
- Driver distinction: CUDA UMD capability 13.3 is not evidence that standalone CUDA Toolkit 13.3 is installed。
- Git evidence: Worker cloned branch `research/stage6-1-hidden-poisoning` at
  `347dc2bfff2256a7ad6c0c6ab8c468e9f3f833d9` with clean tree and matching remote；baseline tag peeled to
  `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`。
- Observation: missing NumPy is `NON_BLOCKING_ENVIRONMENT_COMPLETENESS_OBSERVATION` and did not invalidate CUDA/FP16/BF16。
- Claims boundary: accepts machine bootstrap, basic tensor computation and Git collaboration only；no baseline reproduction、
  Paper Result、training/retrieval/detector result、SOTA or formal experiment。

## PODR-047: S6.1-R0 Execution Approval

- Date: `2026-07-31`.
- Decision: `S6.1-R0: APPROVED_TO_START` as `ENGINEERING_VALIDATION / REPRODUCTION_PREFLIGHT` on
  `RTX5090 / COMPUTE_WORKER`。
- Supersedes: PODR-045's `DEFINED / NOT STARTED / PENDING OWNER EXECUTION APPROVAL` current-state snapshot；the historical
  definition remains preserved。
- Ordered scope: R0-A Environment Fingerprint；R0-B/C PoisonedRAG static audit/minimal smoke；R0-D/E GMTP static
  audit/minimal smoke；R0-F/G SafeRAG static audit/selected-task minimal smoke；R0-H feasibility matrix；R0-I Control Plane review。
- Isolation: external repos stay under `~/paper1_external/` outside LLMGuard；use separate compatibility environments after
  static audit；do not vendor upstream code。
- Data/model boundary: minimal public samples and small necessary public models are permitted；full corpora/indexes require
  `MINIMUM_DATA_REQUIREMENT` review；paid API/API key and unapproved large LLM download remain prohibited。
- Formal boundary: `FORMAL_EXPERIMENT = NOT STARTED`；S6.1-P1 remains `NOT STARTED` until R0 evidence and R0-I review。
- Local boundary: this acceptance authorizes the Compute Worker, not LOCAL execution. LOCAL only updates/pushes Control Plane
  governance and then stops。

## PODR-048: Control-Plane-First Token Economy Principle

- Date: `2026-07-31`.
- Priority: `LONG_TERM_DUAL_MACHINE_EXECUTION_PRINCIPLE`.
- Decision: 在不降低 research quality、reproducibility、security、evidence quality 或 governance quality 的前提下，
  高推理/分析/设计/文档工作优先由 `LOCAL / CONTROL_PLANE` 完成；RTX5090 token 优先用于机器环境、外部执行、GPU、
  reproduction、compatibility、training/inference、resource measurement、raw evidence 和 hardware debugging。
- Worker escalation: 路线级问题返回 `DELEGATE_TO_LOCAL_CONTROL_PLANE` 或 `RESEARCH_ROUTE_REVIEW_REQUIRED`。
- Non-override boundary: 该原则是执行资源治理，不是科学证据优先级；不得覆盖 safety、ethics、evidence quality、
  Paper-First Comparative Evidence、label isolation、immutable history、approval gates 或 experimental reproducibility。

## PODR-049: S6.1-R0-I Returned for Minimal Worker Evidence Correction

- Date: `2026-07-31`.
- Decision: `S6.1-R0-I = RETURNED_FOR_WORKER_CORRECTION`；parent R0 is
  `REVIEW_PENDING_CORRECTED_WORKER_EVIDENCE`，not failed and not accepted。
- Integrity: archive SHA-256 `0ce85a2bfe24e0456f9d29edc40659786d4273fcfc634df8749aee6d0e3aa9cc` and
  internal evidence index `18/18` verified。
- Reason: GMTP exact commit contains advertised 200-sample artifacts although Worker evidence says absent；Docker is a
  convenience path, not algorithm requirement；SafeRAG executed-script hash is not bound and schema coverage checks only the
  first record per task。
- Roles: PoisonedRAG `PRIMARY_ATTACK_BASELINE`、GMTP `PRIMARY_DETECTION_BASELINE`、SafeRAG
  `PRIMARY_BENCHMARK_REFERENCE` remain unchanged。
- Follow-up: only the minimal corrections in the redacted R0-I review are authorized；no new environment exploration、data/model
  download、API、R0-FU1、S6.1-P1 or formal experiment。
- Recommendation: `R0-FU1 = RECOMMEND / NOT APPROVED`；final approval remains with the project owner。

## PODR-050: S6.1-R0 Corrected-Evidence Final Acceptance With Blockers

- Date: `2026-07-31`.
- Decision: `S6.1-R0 = HUMAN_ACCEPTED_WITH_BLOCKERS`；Task Type remains
  `ENGINEERING_VALIDATION / REPRODUCTION_PREFLIGHT`。
- Supersedes current-state effect only: PODR-049 and the historical `RETURNED_FOR_WORKER_CORRECTION` snapshot remain preserved
  as the first-review fact；they are not rewritten or deleted。
- Integrity: corrected archive SHA-256
  `904d79c59e35c6aeb157540049b0f44262b86e5c1c5b3e8d4e96ee2fad3f1c6b`；inner index `12/12`；corrected matrix
  SHA-256 `fd7617eca689fa46fc6908f94aa4fa158aaae4d277bb17943bbcc1baf74db9bc`。
- Baselines: PoisonedRAG `ENGINEERING_FEASIBILITY_IDENTIFIED / P1_PROTOCOL_BLOCKED`；GMTP
  `ENGINEERING_FEASIBILITY_IDENTIFIED / TARGETED_EXECUTION_BLOCKERS_REMAIN` with 18 available 200-sample artifacts and
  Docker not mandatory；SafeRAG `PARTIAL_REPRODUCTION_READY / DATASET_ARTIFACT_ONLY` with SN/ICC
  `BENCHMARK_ARTIFACT_AVAILABLE`。All remain `NOT_STRICT_COMPARISON_READY`。
- Claims boundary: no baseline, SafeRAG pipeline or benchmark result was reproduced；no Paper Result、Our Method Result、
  security-effectiveness or SOTA claim is accepted。
- Remaining classes: `P1_PROTOCOL_BLOCKER` for PoisonedRAG dataset/attack identity and GMTP modified-BEIR/detection-only path；
  `FORMAL_EXPERIMENT_ENVIRONMENT_BLOCKER` for GMTP Java/Pyserini/FAISS and selected generator/model/service paths；
  `REDISTRIBUTION_ONLY_ISSUE` for GMTP/SafeRAG license uncertainty；SafeRAG full pipeline is `NON_BLOCKING` when only its
  benchmark artifacts are used under a frozen contract。
- Recommendation: `S6.1-R0-FU1 = APPROVAL_RECOMMENDED / NOT APPROVED`。No R0-FU1 execution is authorized。
- Stop boundary: `S6.1-P1 = NOT STARTED`；Dataset `NOT FROZEN`；Detector `NOT IMPLEMENTED`；Training `NOT STARTED`；
  Our Method Result `NONE`；`FORMAL_EXPERIMENT = NOT STARTED`。Auto Continue = NO。

## PODR-051: S6.1-R0-FU1 Approval With LOCAL-First Worker Gate

- Date: `2026-07-31`.
- Decision: `S6.1-R0-FU1 = APPROVED` under `LOCAL-FIRST / WORKER-GATED` execution；current authorization is limited to
  `S6.1-R0-FU1-P0 / LOCAL Control-Plane Planning and Execution Contract Freeze`。
- P0 scope: paper/source reasoning、external artifact analysis、dataset comparison、PoisonedRAG attack identity、GMTP source/
  call-path/dependency analysis、SafeRAG artifact contract and exact future Worker contract design。
- P0 completion: `COMPLETED_PENDING_OWNER_REVIEW`；NQ is the primary external dataset candidate, HotpotQA the fallback；
  PoisonedRAG released attack-text reuse is `PARTIAL`；GMTP BEIR identity resolves to official `beir-cellar/beir@f062f0...` and
  detection-only scoring excludes Java/Pyserini/FAISS；SafeRAG SN/ICC artifact contract is frozen。
- Worker gate: `FU1-W1 = NOT APPROVED` and `FU1-W2 = NOT APPROVED`；P0 cannot contact RTX5090, download data/models or run
  PoisonedRAG、GMTP or SafeRAG。Future W1/W2 require separate owner decisions against the exact candidate contracts。
- Large artifact gate: any planned artifact or derived corpus/index footprint above 5 GB requires
  `OWNER_LARGE_ARTIFACT_APPROVAL_REQUIRED`；W1/W2 candidate ceilings are below that threshold。
- Stop boundary: `S6.1-P1 = NOT STARTED`；Dataset `NOT FROZEN`；Detector `NOT IMPLEMENTED`；Training `NOT STARTED`；
  Our Method Result `NONE`；`FORMAL_EXPERIMENT = NOT STARTED`。Auto Continue = NO。
- Evidence: [FU1 Targeted Resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md)、
  upstream exact commits/blob metadata and accepted corrected R0 evidence hashes。

## PODR-052: FU1 Planning and LOCAL Artifact Validation Acceptance; W2 Contract Freeze

- Date: `2026-07-31`.
- Decision: `S6.1-R0-FU1-P0 = HUMAN_ACCEPTED` and
  `S6.1-R0-FU1-L1 = HUMAN_ACCEPTED` on `LOCAL / CONTROL_PLANE`.
- L1 evidence: PoisonedRAG commit `f660d72174f06b13fae5163ce656e7b235db858f`；released NQ artifact blob
  `d1da818b28da7013864ea465ff88ad4c3ca29562` / SHA-256
  `44df711454a9bada08e72e9e4a003a2cc845c43707ac93a3493e5168ec415cf2`；all `100` records satisfy the frozen schema and
  contain exactly five non-empty attack texts；official assembly is exactly `question + "." + adv_text`.
- Determinism: fixed target `test1` has five ordered assembled-document SHA-256 values and aggregate
  `f22b7576c27926a07a7138e952cf3ee6b86c982b584a3078f3364577d32c60a7`, as recorded in the canonical FU1 resolution.
- Boundary: released attack texts are reusable without API calls；this is not attack generation reproduction. Exact historical
  generator/API/paper-run identity remains `PARTIAL / UNRESOLVED`.
- Supersession: historical `FU1-W1` is `SUPERSEDED_BY_LOCAL_L1 / NOT FAILED`; no Worker W1 remains.
- W2: the hardened `GMTP Detection-Only Minimal Smoke` contract is
  `READY_FOR_OWNER_EXECUTION_APPROVAL / NOT_YET_EXECUTED`. Its GMTP-packaged HotFlip/Contriever input is not the L1
  LM-targeted artifact and cannot establish a unified or strict comparison.
- Stop boundary: no RTX5090 contact, W2 execution, model/retrieval/API/NQ-corpus work, S6.1-P1, Dataset freeze, Detector,
  training, Our Method Result or Formal Experiment is authorized by this decision. Auto Continue = NO.
- Evidence: [FU1 Targeted Resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md)、
  [Current Work State](current_work_state.md)、REL-2026-0013 and governance tests.

## PODR-053: GMTP Detection-Only Minimal Smoke Execution Approval

- Date: `2026-08-01`.
- Decision: `S6.1-R0-FU1-W2 = APPROVED_TO_START` as
  `ENGINEERING_VALIDATION / DETECTION_CORE_COMPATIBILITY_SMOKE` on `RTX5090 / COMPUTE_WORKER`.
- Preconditions retained: `S6.1-R0-FU1-P0 = HUMAN_ACCEPTED`；`S6.1-R0-FU1-L1 = HUMAN_ACCEPTED`；historical W1 is
  `SUPERSEDED_BY_LOCAL_L1 / NOT FAILED`；`S6.1-P1 = NOT STARTED`；`FORMAL_EXPERIMENT = NOT STARTED`.
- Frozen identity: `mountinyy/GMTP@15b48d150f93711371eb8da22c211cd84a0cf4df`；detector
  `src/defenses/method.py` blob `84e69b3eadeb8adc0ce521501f8b560d6377b489`；the exact input record and hashes remain
  those accepted in the canonical FU1 resolution. Worker sample selection is prohibited.
- Frozen models: `facebook/contriever-msmarco@abe8c1493371369031bcb1e02acb754cf4e162fa` and canonical
  `google-bert/bert-base-uncased@86b5e0934494bd15c9632b12f734a8a67f723594`; revisions cannot change.
- Environment and parameters: independent `gmtp-compat` only；Python 3.11；Torch 2.13.0+cu130；CUDA runtime 13.0；
  Transformers 4.47.1；NumPy 1.26.4；the accepted `W2_PARAMETER_CONTRACT` is authoritative. `llmguard-paper1` stays unchanged.
- Import/patch stop: an unexpected ordinary Python core import dependency must be recorded as
  `UNEXPECTED_CORE_IMPORT_DEPENDENCY` and may be installed only when small and algorithm-neutral. Any Java/Pyserini/FAISS/BEIR/
  Docker requirement stops and returns to Control Plane. Any required source patch returns
  `COMPATIBILITY_PATCH_REVIEW_REQUIRED` and stops；no silent patch is allowed.
- Evidence/resource boundary: engineering evidence only under `~/experiments/s6_1_r0_fu1/w2/`；main LLMGuard repository is
  read-only；download `<2 GB` expected, disk 5 GB, RAM <=16 GB, VRAM <=8 GiB, runtime <=10 minutes after model availability.
  Any exceedance returns `WORKER_RESOURCE_APPROVAL_REQUIRED` and stops.
- Claims boundary: this approves execution only. It does not assert W2 executed/passed/accepted, GMTP paper reproduction,
  PoisonedRAG-to-GMTP formal comparison, accuracy/F1/AUPRC/AUROC/Filtering Rate/ASR, Paper Result or security effectiveness.
- Artifact distinction: W2 uses GMTP-packaged HotFlip/Contriever/NQ input, not the L1 PoisonedRAG LM-targeted artifact.
- Local boundary: LOCAL only registers and pushes this approval；it does not install, download, run GMTP/GPU work, contact the
  Worker or enter P1. Auto Continue = NO.
- Evidence: [FU1 Targeted Resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md)、
  [Current Work State](current_work_state.md) and REL-2026-0014.

## PODR-054: W2 Attempt 1 Evidence Gate, Resource Correction and Offline Recovery Approval

- Date: `2026-08-01`.
- Decision: W2 Attempt 1 may be classified `VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER` only if the submitted
  archive supports every mandatory Worker-summary fact. Any material gap requires `W2_ATTEMPT1_EVIDENCE_BLOCKER` and STOP.
- Review outcome: archive SHA-256 `6acdbb8038e57b1d3e88028350fc08046d73a826ba9dd167452bfc0dd834170f`, safe members
  `18/18`, evidence index `16/16`, GMTP/source/input/environment identities and `smoke_executed=false` passed；main LLMGuard
  repository HEAD/clean evidence and the claimed environment disk measurement are absent. Therefore Attempt 1 is
  `EVIDENCE_REVIEW_BLOCKED`, not a valid blocked engineering run.
- Resource decision: future resumed W2 uses `W2_TASK_OWNED_DISK_HARD_CEILING = 10 GiB`, subdivided into `gmtp-compat <=6 GiB`,
  two exact model snapshots `<=2 GiB`, harness/evidence/archive `<=256 MiB`, with the remainder reserved for filesystem accounting
  and temporary headroom. RAM `<=16 GB`, VRAM `<=8 GiB`, and post-model runtime `<=10 minutes` remain unchanged. This is a
  `RESOURCE_CONTRACT_CORRECTION`, not an algorithm/data/parameter/model change.
- Recovery decision: `S6.1-R0-FU1-W2-H1 / Offline Model Artifact Provisioning and W2 Resume` is owner-approved as
  `APPROVED_TO_PREPARE_OFFLINE_ARTIFACTS`, with exact Contriever/BERT revisions and no LOCAL model loading/inference.
- Fail-closed effect: H1 preparation is currently `NOT STARTED / BLOCKED_BY_W2_ATTEMPT1_EVIDENCE_BLOCKER`; no local download,
  manifest or bundle may begin until corrected Attempt 1 evidence closes the gate.
- W2 remains `APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED`. This review does not establish `FAILED_ALGORITHM`,
  `GMTP_INCOMPATIBLE`, model compatibility, a detector score, Paper Result or security effectiveness.
- Correction request: capture main-repository HEAD and delimited clean status plus explicit `gmtp-compat` byte measurement in a
  corrected indexed archive. Do not rerun GMTP, rebuild the environment or download models merely to correct evidence packaging.
- Stop boundary: `S6.1-P1 = NOT STARTED`; `FORMAL_EXPERIMENT = NOT STARTED`; LOCAL does not contact RTX5090. Auto Continue = NO.
- Evidence: [Attempt 1 Control Plane Review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_w2_attempt1_control_plane_review.md)、
  [FU1 Targeted Resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md) and REL-2026-0015.

## PODR-055: Correction 01 Conditional Review and H1 Fail-Closed Continuation

- Date: `2026-08-01`.
- Owner authorization: review the minimal corrected indexed evidence first；start the already approved H1 only if every correction
  requirement passes. No new owner approval would be needed after a passing correction.
- Integrity result: correction archive SHA-256
  `d911063e3a00daba3f8dcfea6f3e6e3b484e79f4f0fe8853a53ff9d8c415279e` matches sidecar, recomputation and Worker report；safe
  members `6/6` and correction index `4/4` pass.
- Evidence result: original Attempt 1 binding and main-repository branch/HEAD/upstream/clean/diff/tag evidence pass. Apparent bytes
  `5399301224` and allocated bytes `5492817920` match the manifest and are below ceiling `6442450944`.
- Material gap: the correction records `MEASUREMENT_TOOL=du` but no concrete `du` commands, flags or raw outputs. It therefore
  cannot independently establish that apparent and allocated byte semantics were not confused.
- Decision: keep `W2_ATTEMPT1_EVIDENCE_BLOCKER = OPEN` and Attempt 1 `EVIDENCE_REVIEW_BLOCKED`. Do not reclassify it as
  `VALID_BLOCKED_ENGINEERING_RUN` or accept reusable preflight evidence.
- H1 effect: `APPROVED_TO_PREPARE_OFFLINE_ARTIFACTS / NOT STARTED / BLOCKED_BY_W2_ATTEMPT1_EVIDENCE_BLOCKER`. No model download,
  model load, manifest, index or bundle creation occurred.
- Next correction: additive command-derived evidence only—exact apparent-size and allocated-size `du` command lines, flags and
  captured outputs, bound by an updated index/manifest. No GMTP rerun, environment rebuild or model download is required.
- Stop boundary: no Worker contact, GPU, S6.1-P1 or Formal Experiment. Auto Continue = NO.
- Evidence: [Attempt 1 Control Plane Review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_w2_attempt1_control_plane_review.md)、
  [FU1 Targeted Resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md) and REL-2026-0016.

## PODR-056: PO-MHEP Highest Internal Project Execution Authority

- Date: `2026-08-01`.
- Decision: establish `PROJECT_OWNER_SOVEREIGNTY_AND_MANDATORY_ESCALATION_PRINCIPLE` (`PO-MHEP`) as
  `HUMAN_ACCEPTED / HIGHEST_INTERNAL_PROJECT_EXECUTION_AUTHORITY / PERMANENT / NO_AUTO_EXPIRY` for the entire LLMGuard Research
  Framework, all stages/branches, LOCAL, RTX5090, agents and automation.
- Formal name: `Project Owner Sovereignty, Mandatory Human Escalation, and Physical Context Preservation Principle`；中文为
  “项目负责人主权、强制人工升级与物理上下文保全原则”。
- Authority decision: L0 dynamic Git/raw evidence remains objective fact authority；L0.5 PO-MHEP decides whether execution may
  continue after facts are known；AGENTS and all other project documents are L1 or below.
- Non-override: PO-MHEP cannot alter L0 facts, immutable evidence/history, safety/law/privacy/license, label isolation or the
  project owner's latest explicit decision. It cannot fabricate or lower evidence quality.
- Escalation decision: accepted-boundary conflicts；API/credential/service needs；major resources/system/irreversible operations；
  architecture/algorithm/label-leakage risks；paper novelty/fairness/statistics/confounder/license risks；evidence/provenance gaps；
  context conflicts；and material uncertainty require `HUMAN_DECISION_REQUIRED / Auto Continue = NO`.
- Stop effect: no default choice, silent workaround, Worker continuation, download/install/external call, blocker auto-resolution
  or next-task entry. Only read-only fact collection, risk analysis, context/evidence preservation and governance persistence remain
  allowed before owner decision.
- Machine sovereignty: LOCAL is `PRIMARY_CONTROL_PLANE / PROJECT_EXECUTION_LEAD / RESEARCH_GOVERNANCE_LEAD /
  5090_APPROVAL_AUTHORITY / PAPER_RISK_REVIEWER / CONTEXT_PRESERVATION_OWNER`. RTX5090 is
  `COMPUTE_WORKER / NO_SELF_APPROVAL_AUTHORITY` and must `STOP / RETURN_TO_CONTROL_PLANE` on any contract deviation.
- Proactive obligations: `FORWARD_RISK_REVIEW`, `PAPER_RISK_REVIEW`, mandatory twelve-field human feedback,
  `CONTEXT_PERSISTENCE_CHECK`, canonical documentation, private-evidence abstraction and Git/remote synchronization.
- Current-state preservation: this governance acceptance does not close `W2_ATTEMPT1_EVIDENCE_BLOCKER`, start H1, send/execute
  Correction 02, contact RTX5090, enter P1 or start Formal Experiment.
- Next decision: owner reviews the Correction 02 Worker Contract Candidate recorded in the canonical FU1 resolution. Candidate is
  `NOT APPROVED / NOT SENT / NOT EXECUTED`.
- Canonical evidence: [PO-MHEP](project_owner_sovereignty_and_mandatory_escalation_principle.md)、
  [Context Authority Map](context_authority_map.md)、[Current Work State](current_work_state.md) and REL-2026-0017.
- Auto Continue: `NO`.

## PODR-057: W2 Attempt 1 GNU du Provenance Final Evidence Correction Approval

- Date: `2026-08-01`.
- Decision: `S6.1-R0-FU1-W2-ATTEMPT1-CORRECTION-02 = APPROVED_TO_START / NOT EXECUTED` as
  `EVIDENCE_PACKAGING_CORRECTION_ONLY` on `RTX5090 / COMPUTE_WORKER`. Auto Continue = NO.
- LOCAL boundary: LOCAL only registers this approval, freezes the final acceptance rule and creates/pushes the governance commit.
  It does not contact or substitute for RTX5090, collect Worker evidence, run Correction 02, download/load models, run GMTP/H1,
  enter S6.1-P1 or start Formal Experiment.
- Measurement contract: capture literal GNU `du -sb -- <gmtp-compat-path>` apparent-size and
  `du -sB1 -- <gmtp-compat-path>` allocated-size commands, arguments, raw stdout/stderr, exit codes and UTC timestamps. Equivalent
  long forms are allowed only when the command actually used is preserved verbatim.
- Provenance contract: capture `command -V du`, `type -a du`, `du --version`, `uname -a`, `date -u`, Conda registration and the
  active existing `gmtp-compat` path. Absolute paths remain private；public governance retains only safe abstractions/basename.
- Historical comparison: Correction 01 reported apparent `5399301224`, allocated `5492817920`, files `33556`, directories `3194`
  and ceiling `6442450944` bytes. Correction 02 records new raw results without forced matching；a material difference returns
  `DISK_MEASUREMENT_MATERIAL_MISMATCH` for Control Plane review.
- Final closure: `MATERIALITY_AND_FINAL_CLOSURE_RULE` requires matching archive/sidecar/recomputed SHA, safe archive, complete
  index, correct existing environment identity, both exact GNU commands, explicit semantics, complete raw streams/exit codes,
  zero measurement exits, both sizes below 6 GiB, raw/manifest/summary consistency and no mutation/download/smoke rerun.
- Mandatory effect after a passing LOCAL raw-evidence review: close `W2_ATTEMPT1_EVIDENCE_BLOCKER`, reclassify Attempt 1 as
  `VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER` and accept `REUSABLE_W2_PREFLIGHT_EVIDENCE`. Non-material formatting
  preferences may not create another packaging blocker.
- Current-state preservation: W2 remains `APPROVED / NOT COMPLETED / NOT ACCEPTED`; Attempt 1 remains
  `EVIDENCE_REVIEW_BLOCKED` and the blocker remains open until evidence is returned and accepted. H1 remains approved but
  blocked/not started；after a passing review it may use the existing `PODR-054` approval without a new H1 owner decision unless
  a new API/model-identity/license/resource/architecture risk appears. S6.1-P1 and Formal Experiment remain not started.
- Worker success wording is only `W2_ATTEMPT1_CORRECTION02_EVIDENCE_READY_FOR_CONTROL_PLANE_REVIEW`; it may not claim W2
  completion/acceptance, H1 start, GMTP compatibility or formal execution.
- Canonical evidence: [FU1 Targeted Resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md)、
  [Current Work State](current_work_state.md) and REL-2026-0018.

## PODR-058: Correction 02 Final Closure and H1 Offline Artifact Result

- Date: `2026-08-01`.
- Authority: the project owner's ordered task requires LOCAL to apply the previously frozen
  `MATERIALITY_AND_FINAL_CLOSURE_RULE` after a passing raw-evidence review and then execute the already approved H1 artifact-only
  contract without requesting a second approval.
- Correction 02 integrity: archive size `4367` bytes；sidecar/recomputed/reported SHA-256 all
  `fcfa3f14c98e0103cb5a1de2f0449fa000d179e2e01d74baa6fec4b013503622`；safe archive and sorted index `17/17` pass.
- Correction 02 provenance: GNU coreutils `du 9.4` exact commands and raw streams establish apparent `5399301224` and allocated
  `5492817920`, both zero-exit and below `6442450944`；files `33556`, directories `3194`, Correction 01 deltas zero, pre/post
  explicit-spec SHA identical and no environment/repository/model/smoke/GPU mutation.
- Materiality decision: `11/11 PASS`. Derivable repeated fields, naming/formatting and non-conflicting Conda activation display are
  non-material；no identity, truth, reproducibility, safety or resource gap remains.
- Mandatory closure: `W2_ATTEMPT1_EVIDENCE_BLOCKER = RESOLVED_BY_CORRECTION_02_CONTROL_PLANE_REVIEW`; Attempt 1 becomes
  `VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER` with `smoke_executed=false`, `algorithm_failure=false` and
  `GMTP_incompatibility=not established`.
- Reusable boundary: accept only main/GMTP/input/environment/CUDA/disk identities, encoder download blocker and smoke-not-executed.
  Do not reuse or infer model load, detector scores, runtime/RSS/VRAM, compatibility or security effectiveness.
- H1 result: exact public snapshots
  `facebook/contriever-msmarco@abe8c1493371369031bcb1e02acb754cf4e162fa` (8 files, 438708922 bytes) and
  `google-bert/bert-base-uncased@86b5e0934494bd15c9632b12f734a8a67f723594` (9 files, 881643453 bytes) were prepared with
  anonymous `snapshot_download`, `max_workers=1`, no model load and no GPU/GMTP execution.
- Resource/index result: 17 model files total `1320352375` bytes；sorted final index `19/19` covers model files plus manifest and
  README；bundle source `1320359518` bytes remains below 2 GiB.
- Bundle identity: Git-external archive size `1222137698` bytes and SHA-256
  `aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45`; sidecar, archive safety and archived-file hashes pass.
- H1 status: `OFFLINE_MODEL_ARTIFACTS_PREPARED_PENDING_5090_VERIFICATION`. This is not human acceptance, Worker verification,
  models-loaded evidence, W2 completion, GMTP compatibility or a paper/security result.
- Preserved gates: parent W2 remains `APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED`; S6.1-P1 and Formal Experiment remain not
  started. Next action is owner-controlled bundle transfer and independent 5090 integrity verification；Auto Continue = NO.
- Canonical evidence: [Attempt 1 Control Plane Review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_w2_attempt1_control_plane_review.md)、
  [FU1 Targeted Resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md)、
  [Current Work State](current_work_state.md) and REL-2026-0019.

## PODR-059: H2 Offline Bundle Verification and Conditional Detection-Core Resume Approval

- Date: `2026-08-01`.
- Decision: 项目需求提出人以“继续实验”为明确授权，批准
  `S6.1-R0-FU1-W2-H2 / Offline Model Bundle Verification and Conditional GMTP Detection-Core Resume`。
- Approval base commit: `212911a21dc35bef05b15fb840542403c415dd13`.
- Execution machine: `5090`.
- Status: `APPROVED_TO_START / NOT SENT / NOT EXECUTED`.
- Auto Continue: `CONDITIONAL_WITHIN_H2_ONLY`.
- Supersedes: 批准前 `H2 = PROPOSED / NOT CANONICAL / NOT APPROVED` 历史快照；历史记录保留。
- Conditional gate: 5090 必须先完成 H2-A 的 18 项 bundle 安全、SHA/index/manifest/model identity 核验、冻结环境与
  强制离线核验；任何实质不一致立即停止且不得进入 H2-B。只有全部通过，才允许在同一 H2 合同内执行一次冻结的
  双文档 GMTP detection-core 调用。
- Frozen bundle: `s6_1_r0_fu1_w2_models_20260801.tar.gz`；size `1222137698`；SHA256
  `aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45`；bundle source bytes `1320359518`；
  model index `19/19`.
- Frozen models: `facebook/contriever-msmarco@abe8c1493371369031bcb1e02acb754cf4e162fa` and
  `google-bert/bert-base-uncased@86b5e0934494bd15c9632b12f734a8a67f723594`.
- Frozen GMTP/input: commit `15b48d150f93711371eb8da22c211cd84a0cf4df`；method blob
  `84e69b3eadeb8adc0ce521501f8b560d6377b489`；method SHA256
  `83531fe0e4933074c0a710f3dc07bb260b5d638d3cd4c8c317a353de135e00f6`；input SHA256
  `0233a26ecc56d7baf1448b86a114e328beece60624aa88304fa3553e90421e44`；serialized index `0` / `test0` and
  frozen question/benign/poisoned hashes in the FU1 work process.
- Frozen parameters: `ret_type=contriever`、`N=5`、`M=5`、`remove_threshold=0.2`、`remove_lambda=1.0`、
  `topk=10`、`do_sort=false`；only one `[benign, poisoned]` call.
- Stop: completion or any blocker stops and returns indexed, redacted evidence to 本机. No autonomous repair, retry, source/input/
  parameter/model change, environment mutation, network fallback or CPU fallback.
- Forward risk review: `PASS_FOR_CONDITIONAL_H2` because conditional execution preserves the independent model provenance gate
  without creating a second approval cycle for the same engineering smoke.
- Paper risk review: `PASS_WITH_ENGINEERING_ONLY_CLAIMS`; a single two-document smoke cannot establish metrics, effectiveness,
  reproduction, safety, baseline superiority, SOTA or a paper result.
- Preserved states: H1 remains `OFFLINE_MODEL_ARTIFACTS_PREPARED_PENDING_5090_VERIFICATION`；parent W2 remains
  `APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED`；`S6.1-P1 = NOT STARTED`；Dataset `NOT FROZEN`；Detector
  `NOT IMPLEMENTED`；Training `NOT STARTED`；Our Method Result `NONE`；Formal Experiment `NOT STARTED`.
- Explicit non-approval: no P1, dataset construction/freeze, Detector implementation, training, Formal Experiment or change to the
  detox-method scope (`SCOPE_CONFIRMATION_REQUIRED`).
- Canonical contract: [FU1 work process](../research/stage6_1_hidden_knowledge_poisoning/stage_process/S6.1-R0-FU1_work_process.md),
  [Current Work State](current_work_state.md), and `REL-2026-0021`.

## PODR-060: H2 Resume 02 Additive Evidence Namespace Rollover Approval

- Date: `2026-08-01`.
- Decision: 项目需求提出人确认 bundle 与 sidecar 已同步到 5090，size `1222137698` 与 SHA256
  `aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45` 匹配；批准保留非空 resume_01，并在全新
  `~/experiments/s6_1_r0_fu1/w2/resume_02` 从 H2-A 重新开始。
- Approval base commit: `2f492dc763e865105510cc8cb141ebde5e109b3e`.
- Resume 01 evidence: archive size `4570` bytes；SHA256
  `941557aa00be58210015165078bbb3c1cbdd2250cab0755c37198e7b7e26e89d`；本机流式复核确认 20 regular files、1 directory、
  no unsafe members、top-level only resume_01 and evidence index `19/19 PASS`.
- Resume 01 result: `OFFLINE_BUNDLE_SHA_BLOCKER`；H2-B not executed；`call_count=0`；environment explicit pre/post SHA
  `62981f4747156189f7870958da8ea7bc2fc0ead49c78bb6463e9fd284bb65961` unchanged.
- Rollover reason: bundle 后续到位时，原合同禁止覆盖或删除非空 resume_01；继续写入会触发
  `EVIDENCE_CAPTURE_BLOCKER`。新目录是不可变证据保全所需的 additive namespace，不是算法、输入或实验重试。
- Resume 02 status: `APPROVED_TO_START / NOT EXECUTED`.
- New archive: `/mnt/e/LLMGuard-Handoff/s6_1_r0_fu1_w2_resume02_evidence_20260801.tar.gz` plus `.sha256`；archive 只能包含
  `resume_02`.
- Unchanged contract: bundle/model/source/input/environment/parameters/resources/offline variables/18 H2-A gates/claims boundary
  全部保持 PODR-059；H2-B 的唯一一次调用授权尚未使用。
- Stop: resume_02 开始前必须不存在或为空；若非空，登记 `EVIDENCE_CAPTURE_BLOCKER` 并停止。不得自动创建 resume_03，
  不得覆盖、删除、改名或合并 resume_01。
- Forward risk review: `PASS_FOR_ADDITIVE_RESUME_02`; preserving immutable evidence prevents history rewriting while avoiding any
  scientific or runtime contract drift.
- Paper risk review: `PASS_WITH_ENGINEERING_ONLY_CLAIMS`; no metric, effectiveness, reproduction, safety or paper result exists.
- Preserved gates: parent W2 remains `APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED`; S6.1-P1, Dataset, Detector, Training,
  Our Method Result and Formal Experiment remain unchanged/not started.
- Canonical contract: [FU1 work process](../research/stage6_1_hidden_knowledge_poisoning/stage_process/S6.1-R0-FU1_work_process.md),
  [Current Work State](current_work_state.md), and `REL-2026-0022`.

## PODR-061: Parent W2 Engineering Feasibility Final Acceptance and FU1 Closure

- Date: `2026-08-02`.
- Decision: 项目需求提出人将 `S6.1-R0-FU1-W2` 正式验收为
  `HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED`，并将 `S6.1-R0-FU1` 关闭为 `HUMAN_ACCEPTED / CLOSED`。
- Acceptance base commit: `b19fc59cc5ba771fd547430f6096403720ef1a7d`.
- Evidence basis: H2 resume_02 archive SHA256
  `58da856a81ad89b858af2c041ff617e16156ec254410b07e6511c2888203f563`；evidence index `25/25 PASS`；H2-A
  `18/18 PASS`；唯一 H2-B `call_count=1`；冻结模型 revision、GMTP source/input/parameters/environment/offline/CUDA/resource
  identities passed independent Control Plane review.
- Accepted objective: 在全部固定条件下，两个本地模型成功离线 CUDA 加载；未修改 detection core 完成一次双文档调用；
  产生 finite 工程输出与 retained/filtered 决策；资源和证据合同通过。本次固定样本中 benign retained、poisoned filtered。
  这是单次冻结样本的工程观察，不是检测性能结论。
- Frozen state: `W2_ENGINEERING_OBJECTIVE = SATISFIED`；`W2_RUNTIME_GATE = CLOSED`；
  `BLK-S6.1-FU1-W2-001 = RESOLVED_BY_H2_RESUME02_AND_OWNER_ACCEPTANCE`；
  `W2_ACCEPTANCE_SCOPE = FROZEN_SINGLE_SAMPLE_DETECTION_CORE_ENGINEERING_FEASIBILITY_ONLY`.
- H1/H2: H1 `OFFLINE_MODEL_ARTIFACTS_VERIFIED_ON_5090 / COMPLETED`；H2
  `ENGINEERING_SMOKE_COMPLETED / CONTROL_PLANE_REVIEW_PASS / HUMAN_ACCEPTED_AS_W2_EVIDENCE`.
- Historical preservation: resume_01 remains
  `VALID_BLOCKED_EVIDENCE / OFFLINE_BUNDLE_SHA_BLOCKER / H2-B NOT EXECUTED / call_count=0`；resume_02 remains
  `CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED / call_count=1`；Attempt 1 is not rewritten as a successful run.
- Claims prohibited: `GMTP_REPRODUCTION = NOT ESTABLISHED`；`DETECTION_EFFECTIVENESS = NOT ESTABLISHED`；
  `STRICT_BASELINE_COMPARISON = NOT ESTABLISHED`；no Accuracy/Precision/Recall/F1/AUPRC/AUROC/Filtering Rate/ASR、
  significance、generalization、baseline superiority、SOTA、Our Method Result or Paper Result；`FORMAL_PAPER_RESULT = NONE`.
- P1 gate: only a non-authoritative `CONTRACT_CANDIDATE / NOT APPROVED / NOT STARTED` may be prepared. Dataset remains
  `NOT FROZEN`；Detector `NOT IMPLEMENTED`；Training `NOT STARTED`；Our Method Result `NONE`；Formal Experiment `NOT STARTED`.
- Detoxification gate: mutually exclusive Option A/B/C must be presented；
  `DETOXIFICATION_TECHNICAL_SCOPE = SCOPE_CONFIRMATION_REQUIRED` and
  `HUMAN_DECISION_REQUIRED_BEFORE_P1_APPROVAL`.
- Canonical records: [Current Work State](current_work_state.md), [FU1 work process](../research/stage6_1_hidden_knowledge_poisoning/stage_process/S6.1-R0-FU1_work_process.md), [P1 candidate](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_protocol_candidate.md), `OR-020`, and `REL-2026-0024`.

## PODR-062: P1 Option B Scope Freeze and Protocol Hardening Candidate

- Date: `2026-08-02`.
- Decision: 项目需求提出人明确选择 `DETOXIFICATION_OPTION = OPTION_B`，确认
  `DETOXIFICATION_TECHNICAL_SCOPE = OPTION_B_CONFIRMED`，完整表达为
  `OPTION_B_DETECTION_AND_LIGHTWEIGHT_RETRIEVAL_INTERVENTION`。
- P1 included scope: 中文版本感知隐蔽知识污染 Benchmark、五视角 Detection、Risk Score、Signals、Explanation，以及
  基于校准风险的 hard filtering 或 soft downweighting；安全结果与检索效用分别作为共同主结果，不合并为单一分数。
- P1 excluded scope: trusted context package、完整上下文构造、多证据可信上下文生成、复杂端到端 Agent 防御、
  生产级 RAG 平台和完整可信检索链；这些能力保留给 Paper 2 或后续独立批准的研究。
- Protocol action: 允许本机以 `P1_R1_BASE_COMMIT = aabe504d55626fb31008822b7bbabd3b32e2afd4` 起草、同步并测试
  [P1-R1 approval-grade review candidate](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_r1_protocol_review_candidate.md)。
  新候选只在候选层替代旧 [P1 protocol candidate](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_protocol_candidate.md)；旧文件保留为历史。
- Candidate status: `S6.1-P1-R1 = REVIEW_CANDIDATE / NOT APPROVED / NOT STARTED`；
  `S6.1-P1 = NOT APPROVED / NOT STARTED`；`Pilot = NOT APPROVED / NOT STARTED`。
- Preserved execution states: Dataset `NOT FROZEN`；Detector `NOT IMPLEMENTED`；Retrieval Intervention `NOT IMPLEMENTED`；
  Training `NOT STARTED`；Our Method Result `NONE`；Formal Experiment `NOT STARTED`。
- W2/FU1 preservation: W2 remains `HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED`；FU1 remains
  `HUMAN_ACCEPTED / CLOSED`；no existing engineering evidence or historical blocker record is rewritten.
- Allowed actions: 本机 research design、文档同步、架构测试、Git commit/push only.
- Prohibited actions: contact 5090；build/download a dataset；external API；poison generation；Detector/retrieval intervention
  implementation；model load/training；baseline/Pilot/formal run；Paper result claim.
- Forward risk review: `PASS_FOR_REVIEW_CANDIDATE` because group-aware splitting, label isolation, baseline fairness, statistical
  correction, evidence and resource gates are explicit, while unresolved values remain owner-visible decisions or Pilot-dependent.
- Paper risk review: `PASS_WITH_SCOPE_GUARD` because “解毒” is now testable as narrow retrieval intervention and cannot be silently
  expanded into a complete trusted retrieval or Agent system.
- Next gate: project owner accepts, revises or rejects the P1-R1 candidate and resolves its four high-level decisions. No automatic
  P1/Pilot entry. Auto Continue = `NO`.
- Canonical records: `OR-021`、[Research Plan Authority](../research/stage6_1_hidden_knowledge_poisoning/human/research_plan_authority.md)、
  [Current Work State](current_work_state.md) and `REL-2026-0025`.

## PODR-063: PILOT2 Return Metadata Owner Correction and Annotation Schema Blocker Reinterpretation

- Date: `2026-08-27`.
- Decision: 项目需求提出人确认 Annotator A 的实际顺序为 Phase 1 完成提交、coordinator 回收并锁定、之后才发放
  Phase 2；A 在 Phase 1 期间没有提前看到 Phase 2。因此
  `A_PHASE1_DISTRIBUTION_ORDER = OWNER_CONFIRMED_CORRECT`，
  `A_PHASE1_STRICT_BLINDNESS = PRESERVED_BY_OWNER_CONFIRMED_OPERATIONAL_FACT`。
- Metadata correction: registration CSV 中原时间和 `NOT_DISTRIBUTED` 状态是
  `INCORRECT_RECORDING / DOCUMENTATION_DEFECT_ONLY`。原登记表、原错误时间、原 preflight 推断和原 preflight workbook
  必须保留；不得修改历史制造从未出错的假象。
- Superseding interpretation: the original blind-contamination inference was based on incorrect registration metadata and is
  superseded by owner-confirmed actual distribution order. It must no longer be described as irreversible blind contamination.
- Blocker status: `PILOT2-RETURN-PROTOCOL-BLOCKER-01 = PROTOCOL_AND_ANNOTATION_SCHEMA_BLOCKER`；
  `BLINDNESS_SUBISSUE = RESOLVED_BY_OWNER_CONFIRMED_ACTUAL_DISTRIBUTION_ORDER`；
  `REGISTRATION_METADATA_SUBISSUE = OPEN_FOR_CORRECTION_AND_EVIDENCE_BINDING`；
  `ANNOTATION_SCHEMA_SUBISSUE = OPEN`；`RETURN_FILE_CONTRACT_SUBISSUE = OPEN`。
- Agreement state: Round 1 remains a formal-agreement candidate, but
  `FORMAL_AGREEMENT = PENDING_SCHEMA_V2_REREVIEW_AND_RETURN_VALIDATION`；no agreement or adjudication is established.
- Remaining issues: YES/NO/UNCERTAIN applicability and missing NOT_APPLICABLE；authority/version/legitimate-history applicability；
  incomplete declarations；incorrect registration metadata；GB18030 versus UTF-8 BOM；B header changes and missing timing/lookup
  fields；lookup source-type classification error.
- Preferred next route: `ANNOTATION_SCHEMA_V2 + A/B INDEPENDENT RE-REVIEW`, not strict rerun with new annotators. This priority does
  not approve execution；a separate task must freeze Schema V2 and return-correction/evidence-binding contracts.
- Prohibited actions: automatic agreement, disagreement packet, adjudication, raw-return mutation, 5090 contact, Dataset freeze,
  Detector, Training or Formal Experiment. Auto Continue = `NO`.
- Canonical record: [PILOT2 Return Preflight Owner Correction](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_pilot2_return_owner_correction.md)、`OR-025`、`REL-2026-0029`。

## PODR-064: PILOT2 Annotation Schema V2 and A/B Round1 Independent Re-review Approval

- Date: `2026-08-27`.
- Decision: 项目需求提出人保留 A/B Round1 和四份 raw return，批准
  `ANNOTATION_SCHEMA_V2 = APPROVED_TO_IMPLEMENT` 与 `A_B_INDEPENDENT_ROUND1_REREVIEW = APPROVED`；不使用 C/D，不执行
  新 240-group Pilot，不通过人工统一答案提高一致率。
- Raw evidence: `PILOT2_ROUND1_RAW = PRESERVED_IMMUTABLE`；四份 raw ZIP、GB18030 字节、原列名、缺失值、声明、lookup
  log、registration metadata、preflight workbook、错误盲法推断和 PODR-063 correction 均保持不可变并由
  `ROUND1_RAW_MANIFEST` 绑定。
- Round1 disposition: `PILOT2_ROUND1 = PRESERVED_FOR_SCHEMA_V2_INDEPENDENT_REREVIEW`.
- Owner fact: `A_PHASE1_STRICT_BLINDNESS = OWNER_CONFIRMED_PRESERVED`；原 metadata 只作为
  `INCORRECT_RECORDING / DOCUMENTATION_DEFECT_ONLY` 历史保留。
- Schema: 条件字段采用 `YES / NO / UNCERTAIN / NOT_APPLICABLE`；version/history/authority 均使用先 present、后
  correctness 的适用性合同；`claim_matches_source` 与 `fact_changed` 始终适用；authority 判断候选提出的机构命题，
  不判断页面发布者。
- Schema quality gate: every field passed `ANNOTATION_FIELD_APPLICABILITY_REVIEW`; any future field that cannot answer the ten
  applicability/semantics/example/subset/value questions must stop at `FIELD_SCHEMA_REVIEW_BLOCKER`.
- Independent re-review: A 只能看到 A 本人的 V1 只读参考，B 同理；每字段 `KEEP/REVISE`，修改必须使用冻结 reason
  code；新增 retrospective declaration 和 lookup source-type review；所有 V2 CSV 为 UTF-8 BOM。
- Completion: `ANNOTATION_SCHEMA_V2 = IMPLEMENTED`；`A_B_REREVIEW = READY_FOR_HUMAN_EXECUTION`；
  `ANNOTATION_SCHEMA_SUBISSUE = REMEDIATION_IN_PROGRESS` until four human V2 returns pass validation.
- Agreement: only future calculation/subset logic is prepared. `FORMAL_AGREEMENT_V2 = NOT_YET_ESTABLISHED`；no agreement,
  disagreement packet or adjudication is executed.
- Prohibited: raw mutation, peer-result sharing, candidate/private mapping leakage, 5090 contact, Dataset freeze, Detector,
  Training, Formal Experiment or Paper Result. Auto Continue = `NO`.
- Next gate: coordinator distributes only the matching A/B packages；after all four independent V2 returns and declarations are
  hash-locked, owner separately approves return validation and any agreement calculation.
- Canonical record: [PILOT2 Annotation Schema V2](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_pilot2_annotation_v2.md)、
  `OR-026`、`REL-2026-0030`.

## PODR-065: PILOT2 Annotator-Friendly Targeted Re-review Approval

- Date: `2026-08-27`.
- Decision: 项目需求提出人否决“把完整 V2 全字段机械重做”的默认路径，批准只针对实际测量问题生成 A/B 隔离、
  标注人友好的 targeted re-review kit；完整 V2 包继续作为只读、不可变的完整 schema 参考。
- Substantive scope: Phase1 仅 `locally_detectable`、`cross_document_evidence_needed`、
  `assigned_stealth_level`；Phase2 仅三组 present/correctness、`overall_fact_status`，合计每人 10 字段 × 36 样本。
- Preserved without rework: Phase1 naturalness/topic/confidence、Phase2 `claim_matches_source`/`fact_changed`/confidence
  与全部证据字段保持本人 V1 只读；不得借本轮改写 raw return。
- Process-only scope: 仅 B 补 21 个 `professional_lookup_used` 缺失项并修正 1 个 Google Search source-type；B
  Phase1 历史 `time_seconds` 维持不可恢复，A/B 各阶段只新增一次 retrospective declaration。
- Workload: 每人实质任务从完整 V2 的 `576` 降至 `360`，减少 `216 / 37.5%`；A 总任务 360，B 含 process fixes
  总任务 382，声明不计入逐样本任务。
- Artifact: Git-external `LLMGuard-Handoff/paper1_pilot2_targeted_rereview_20260827`；四个主 XLSX 具有冻结语义、
  下拉输入、只读原值、KEEP/REVISE 推导、applicability 联动提示和分阶段回溯声明。
- Completion: `TARGETED_FIELD_AUDIT = COMPLETED`；`TARGETED_REREVIEW_KIT = READY_FOR_HUMAN_EXECUTION`；
  `FORMAL_AGREEMENT_V2 = NOT_YET_ESTABLISHED`。
- Next gate: 分别发 A/B targeted Phase1，双方回收并 hash-lock 后才发 targeted Phase2；四份 return 锁定后停止，
  由 owner 另行批准 return validation 与任何 agreement analysis。
- Prohibited: automatic agreement/disagreement/adjudication、raw/full-V2 mutation、Dataset freeze、Detector、Training、
  5090、Formal Experiment 或 Paper Result。Auto Continue = `NO`。
- Canonical record: [PILOT2 Targeted Re-review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_pilot2_targeted_rereview.md)、
  `OR-027`、`REL-2026-0031`。

## PODR-066: PILOT2 V1 Mapping Correction and Final Human Round

- Date: `2026-08-28`.
- Owner fact: A Phase1 targeted re-review is reported completed. Its observed workbook is preserved unchanged and remains pending
  return validation/formal hash lock; this record does not declare agreement or Ground Truth.
- Correction decision: correct B Phase1's false all-`[V1_ABSENT]` display, inspect B Phase2/A Phase2 for the same class of defect,
  and provide only the three still-open corrected workbooks for independent human completion.
- Validity intent: the corrected returns are the owner's high-priority/high-weight validity evidence candidates for closing Pilot2
  annotation after return validation; the owner does not want another blanket annotation cycle. This intent does not bypass return
  validation, agreement review, necessary adjudication or Ground Truth acceptance.
- Frozen interpretation: `version_context` is known-correct reference evidence; only factual conflicts receive S1/S2/S3;
  currently consistent/legitimate history maps to `NOT_APPLICABLE`, insufficient evidence to `UNCERTAIN`; one direct official
  source is S2 and not cross-document; S3 requires a multi-evidence/version/authority/provenance chain.
- Artifact rule: publish to an additive correction namespace; do not overwrite the original targeted package or completed A Phase1.
  `[V1_ABSENT]` is valid only for the three genuinely new Phase2 `*_present` fields; every other missing mapping fails closed.
- Prohibited: automatic agreement, adjudication, Dataset freeze, Detector, Training, 5090 or Formal Experiment. Auto Continue = `NO`.
- Canonical record: [PILOT2 Targeted Re-review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_pilot2_targeted_rereview.md)、
  `OR-028`、`REL-2026-0032`。

## PODR-067: Prospective Candidate Minimum Self-Containment Gate

- Date: `2026-08-28`.
- Authority: one of the highest-priority instructions for all future Paper 1 data annotation involving newly created or newly
  introduced candidate text.
- Rule: legal, policy, institutional and standards subjects must be uniquely identifiable from the candidate text itself. Bare
  references such as “条例”、“规定”、“修订文本” or “2017年版” cannot rely on hidden context or annotator inference.
- Failure disposition: `BROKEN_CANDIDATE / MISSING_CONTEXT`; the candidate is barred from the formal Benchmark and must be rewritten
  as a newly reviewed candidate with an explicit subject or excluded.
- Gate order: self-containment admission precedes fact/stealth annotation, agreement, adjudication and Dataset freeze.
- Prospective-only boundary: existing Pilot1/Pilot2 candidates, raw returns and current targeted re-review artifacts are preserved;
  this decision does not rewrite, overturn, relabel or reinterpret historical content.
- Enforcement: executable candidate-admission record and formal-Benchmark fail-closed guard are added under canonical `llmguard`.
- Prohibited inference: registration of this rule is not Dataset freeze, agreement, Ground Truth acceptance or Formal Experiment.
- Canonical authority: [Paper 1 Research Plan Authority](../research/stage6_1_hidden_knowledge_poisoning/human/research_plan_authority.md)、
  `OR-029`、`REL-2026-0033`.

## PODR-068: PILOT2 Post-Annotation Validation and Formal Agreement Approval

- Date: `2026-08-31`.
- Owner fact: A/B targeted Phase2 annotation is complete; A/B Phase1 declaration field `sample_id_changed` was misunderstood and
  has the owner-confirmed effective value `NO`. Source XLSX values remain unchanged and the correction is derived process metadata.
- Approval: execute `S6.1-P1-PILOT2-POST-ANNOTATION` for immutable return hashing, return validation, A/B V2 formal agreement,
  disagreement classification and a disagreement-only owner packet. Do not request a third blanket annotation round.
- V2 authority: each annotator's V2 re-review value supersedes that annotator's V1 value. A/B agreement compares V2 to V2; V1 is
  history only. `[V1_ABSENT]` is not a disagreement or missing label by itself.
- Conditional agreement: presence is compared on all 36 samples; correctness is compared only when both annotators set presence to
  `YES`. Presence mismatch is `APPLICABILITY_DISAGREEMENT`.
- Result: four returns validated for agreement with preserved non-semantic defects; 47 A/B disagreement records plus 37
  schema-logic conflicts require owner adjudication across 26 candidate texts.
- Gate: generate the minimal packet and stop at `WAIT_FOR_OWNER_ADJUDICATION`. Do not auto-adjudicate or generate Ground Truth.
- Prohibited: raw-return mutation, Dataset freeze, Detector, Training, 5090, Formal Experiment, Paper Result or SOTA claim.
- Canonical record: [PILOT2 Post-Annotation](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_pilot2_post_annotation.md)、
  `OR-030`、`REL-2026-0034`.

## PODR-069: PILOT2 Adjudication Closure and Conditional Pilot3 Entry Approval

- Date: `2026-08-31`.
- Owner decision: approve read-only ingestion and validation of the completed owner adjudication workbook; only after a full pass,
  construct a Pilot-only Ground Truth candidate, audit and close Pilot2, then enter a local small-scale Pilot3 signal diagnostic.
- Input correction boundary: never alter owner cells or silently resolve contradictions; an invalid or conflicting owner decision
  stops Ground Truth and produces only a minimal owner reconfirmation table.
- Observed execution result: all `84/84` issue rows and `26/26` candidate rows are filled, but four candidates contain invalid enum
  text or conflicting owner final values. Status is therefore `OWNER_ADJUDICATION_CONSISTENCY_BLOCKER / HUMAN_DECISION_REQUIRED`.
- Owner evidence SHA256:
  `cf47a6c3ffada717a2a0dee2b67d6b92ebfb6236d599fb8a4daf2957e292dcb1`.
- Current authorization boundary: owner may reconfirm only the four blocker candidates; LOCAL may then revalidate. Ground Truth,
  Pilot2 closure and Pilot3 have not occurred.
- Prohibited: A/B relabeling, automatic adjudication, 5090, 240-group data, Dataset freeze, large training, formal Detector or
  intervention claim, Formal Experiment, Paper Result or SOTA claim.
- Canonical evidence: [PILOT2 Adjudication Closure Attempt](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_pilot2_adjudication_closure.md),
  `OR-031`, `REL-2026-0035`.

## PODR-070: PILOT2 Owner Correction, Ground Truth Closure and Pilot3 Smoke

- Date: `2026-08-31`.
- Owner decision: confirm the four blocker candidates exactly as recorded in `OR-032`; preserve the completed owner workbook and
  bind an independent owner-correction record explicitly attributed to the project requirements owner.
- Validation result: `84/84` issues and `26/26` candidate resolutions complete; PENDING `0`; residual owner inconsistency `0`;
  remaining schema-logic conflict `0`.
- Ground Truth: `PILOT2_GROUND_TRUTH_CANDIDATE_V1` generated deterministically with 36 Pilot-only records: Clean `1`, Poison `12`,
  Hard Negative `23`, excluded/insufficient `0`.
- Closure: `S6.1-P1-PILOT2 = HUMAN_ACCEPTED / ANNOTATION_PROTOCOL_AND_GROUND_TRUTH_FEASIBILITY_ONLY / CLOSED`.
- Conditional continuation executed: local CPU-only Pilot3 emitted 180 independent SignalRecord rows. Its status is
  `ENGINEERING_AND_SIGNAL_FEASIBILITY_ESTABLISHED / PILOT_DIAGNOSTIC_ONLY`, never detector effectiveness.
- Stop boundary: no 240-group, Dataset formal freeze, formal Detector/training, 5090, Formal Experiment, Paper Result or SOTA.
- Canonical record: [Pilot2 Closure and Pilot3 Signal Feasibility](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_pilot2_closure_and_pilot3_signal_feasibility.md),
  `OR-032`, `REL-2026-0036`.

## PODR-071: PILOT4 Balanced Pre-annotation and Owner Preflight Approval

- Date: `2026-09-01`.
- Owner decision: execute the last dedicated small-scale data/annotation calibration before any 240-group design. Freeze one
  canonical lessons file; require coverage-before-generation, field-schema quality, subject uniqueness, G1-G14 candidate admission,
  blind cold-reader and four-round QA before human release.
- Approved construction: 24 independent public Chinese source/version subjects, 24 matched Clean/Poison-intent/Hard-Negative
  triplets, 72 preannotation candidates, 48+ self-contained queries, full HKP×intended-S coverage, four domains and three length
  bands. Generation intent is never Ground Truth.
- Signal scope: structured Temporal-Version and Provenance contracts, hard-negative-aware Semantic/Entity diagnostics and an
  operational independence-group/matched-triplet-aware semantic near-duplicate scanner.
- Execution result: `24/24/24`, 12 HKP×S cells ×2, four domains ×6 triplets, length `8/8/8`, authority/temporal applicability
  `12/24` each, six HN subtypes ×4, subject uniqueness `72/72`, G1-G14 and four QA rounds PASS.
- Artifact: Git-external `LLMGuard-Handoff/paper1_pilot4_preannotation_20260901`; Owner sees a stratified 12-row workbook sample.
- Final status: `BALANCED_DIAGNOSTIC_SET_READY_FOR_OWNER_PREFLIGHT / PREANNOTATION_ONLY / NO_HUMAN_DISTRIBUTION`.
- Prohibited: A/B distribution, agreement, adjudication, 240-group, Dataset freeze, formal Detector/training, 5090, Formal
  Experiment, Paper Result or SOTA. Auto Continue = `NO`.
- Canonical authority: [future dataset rules](../research/stage6_1_hidden_knowledge_poisoning/human/annotation_lessons_learned_and_future_dataset_rules.md),
  `OR-033`, `REL-2026-0037`.

## PODR-072: PILOT4 Owner Preflight Return and Targeted Repair

- Date: `2026-09-01`.
- Owner decision: the first Owner Preflight is `TARGETED_CORRECTION_REQUIRED`; preserve the `a843697` implementation and
  Git-external evidence as failed-but-useful history, then perform only the specified targeted repair.
- Failure basis: metadata attack-type misalignment risk; stealth not evidence-path-derived; LONG candidate answer/evidence echo;
  experimental meta-language; applicability not claim-derived; builder-declared PASS not independently recomputed; and weak
  Hard Negative evidence chains.
- Repair result: mutation-semantic and stealth-path contracts PASS; 72 repaired candidates were reloaded from serialized artifacts;
  independent G1--G14 and Round D PASS; a new 12-row second Owner Preflight is ready.
- Status: `PILOT4_BALANCED_SET_REPAIRED / READY_FOR_SECOND_OWNER_PREFLIGHT / PREANNOTATION_ONLY / NO_HUMAN_DISTRIBUTION`.
- Prohibited: do not register acceptance, distribute A/B, calculate agreement, adjudicate, generate Ground Truth, start 240-group,
  freeze Dataset, train, contact 5090 or start Formal Experiment. Auto Continue = `NO`.
- Canonical authority: [future dataset rules](../research/stage6_1_hidden_knowledge_poisoning/human/annotation_lessons_learned_and_future_dataset_rules.md),
  `OR-034`, `REL-2026-0038`.

## PODR-073: Paper 1 Human Documentation Integration and Formal Domain Set

- Date: `2026-09-01`.
- Task classification: `DOCUMENTATION_STRUCTURE_AND_CONTEXT_INTEGRATION`.
- Owner decision: keep `human/experiment_ledger_tingfeng.md` as the stable `PAPER1_PRIMARY_HUMAN_ENTRY`; establish explicit Human,
  Research/Protocol Authority and Agent/Audit/Evidence layers without removing machine detail or duplicating raw evidence.
- Domain decision: `PAPER1_FORMAL_DOMAIN_SET = OWNER_CONFIRMED` for future Scale Pilot/Formal Benchmark planning: Enterprise HR,
  Finance, Information Security, Procurement and R&D, Education and Research.
- Scale planning: `5 domains × 4 HKP × 3 stealth × 4 independent chains = 240 groups`; approximately 720 Clean/Poison/matched-HN
  records is a derived plan only. Neither value is generated, frozen or approved for execution.
- Historical boundary: Pilot4 remains a four-domain Pilot fact. Documentation must not rewrite it as five-domain coverage.
- Experiment status unchanged: `PILOT4_BALANCED_SET_REPAIRED / READY_FOR_SECOND_OWNER_PREFLIGHT / PREANNOTATION_ONLY /
  NO_HUMAN_DISTRIBUTION`.
- Prohibited: Pilot4 acceptance, A/B distribution, agreement, adjudication, Ground Truth, 240-group execution, Dataset freeze,
  Detector/training change, 5090, Formal Experiment or Paper Result. Auto Continue = `NO`.
- Canonical records: [Human Ledger](../research/stage6_1_hidden_knowledge_poisoning/human/experiment_ledger_tingfeng.md),
  [Research Plan Authority](../research/stage6_1_hidden_knowledge_poisoning/human/research_plan_authority.md), `OR-035`,
  `REL-2026-0039`.

## PODR-074: Pilot4 Second Preflight Return and Final Preannotation Repair

- Date: `2026-09-01`.
- Owner decision: the second Pilot4 Owner preflight is `TARGETED_REPAIR_REQUIRED`; do not accept Pilot4 and do not distribute A/B.
- Preservation: keep the first `a843697` preflight and the second `cad3b2b` preflight plus both Git-external evidence trees immutable.
- Approved Repair-02: replace evidence-count S3 with genuine joint-evidence necessity; remove explicit S1 diagnostic commentary; enforce
  actual 35–70 / 71–140 / 141–240 final visible lengths; remove cross-group boilerplate; align all Hard Negative subtype/text/source
  semantics; preserve non-target claim parity; run a Phase1-only human-text sanity validator.
- Final review artifact: 16 rows = one Poison per HKP×S cell, two Clean and two matched Hard Negative, with S3 contribution and
  single-evidence-insufficiency details visible only to Owner.
- Current status: `PILOT4_FINAL_PREANNOTATION_READY_FOR_OWNER_REVIEW / NO_HUMAN_DISTRIBUTION`; this is not acceptance.
- Prohibited: automatic A/B package/distribution, agreement, adjudication, Ground Truth, 240-group, Dataset freeze, formal Detector,
  Training, 5090, Formal Experiment, Paper Result or SOTA claim.
- Evidence and synchronization: `OR-036`, `REL-2026-0040`; Git-external namespace
  `paper1_pilot4_preannotation_repair02_20260901`. Auto Continue `NO`.
