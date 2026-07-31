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
