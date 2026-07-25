# Stage 6：RAG 安全与可信检索基线

## Metadata

- stage_id: `S6`
- canonical_name: `RAG Security Evaluation`
- canonical_slug: `stage6_rag_security`
- legacy_paths: `stages/stage6_rag/`、`data/stage6_rag/`、`tests/stage6_rag/`
- status: `s6_t5_3_dense_retriever_human_accepted`
- acceptance_hardening: `s6_t5_3_h1_human_accepted`；仅修复 trace 语义、store provenance 与脱敏失败边界。
- s6_t5_4_status: `completed_pending_human_acceptance`；最小 ContentResolver 离线实现完成，等待人工验收。
- s6_t5_4_p1_status: `human_accepted`；Content Resolution Contract and Permission Boundary 已通过人工验收，未创建业务代码。
- s6_t5_4_i1_status: `completed_pending_human_acceptance`；仅使用合成内存正文，未读取 fixture 或生成真实 legacy mapping。
- s6_t5_4_h1_status: `completed_pending_human_review`；关闭 Resolver registry capability escape，并加固注入依赖异常的脱敏/类型-code 所有权。
- objective: 在 S6-T4 与已验收 S6-T5.2 契约基础上，实现受控、离线、Provider-Neutral DenseRetriever；本轮只产出 RetrievalEvidence 与 RetrievalTrace。
- source_locations: `src/llmguard/domains/retrieval/{contracts,attacks,embedding,vectorstore,retrieval,context}/`
- data_locations: `data/stage6_rag/`（已入 manifest 的历史数据路径）
- test_locations: `tests/stage6_rag/`、`tests/architecture/`、`tests/domains/retrieval/`、`tests/integration/retrieval/`
- script_locations: 真实模型测试由 `LLMGUARD_RUN_REAL_EMBEDDING_TESTS=1` 显式开启，无 S6-T4 运行脚本；2026-07-19 已完成一次固定 revision 的真实验收。
- deliverable_locations: 尚未生成独立 Stage 6 证据包。
- evidence_locations: `data/stage6_rag/documents/corpus_manifest.json`
- conclusion_boundary: 已完成人工验收的 S6-T5.3 离线工程边界包括 embedding/vectorstore 基础设施、S6-T5.2 运行时契约、schema `1.1` parent identity carrier、DenseRetriever 与 H1 trace/failure-boundary 加固；S6-T5.4-I1 已实现 contracts、in-memory reader/registry、exact-match legacy adapter 与 hash-verified resolver，H1 又关闭公开 registry capability 并重建注入错误的固定脱敏外部表述。I1 仍待人工验收，H1 待人工复核。未实现 ContextBuilder、Trust、LLM 或 RAG 指标，也未执行正式 RAG 安全实验。
- next_stage: S6-T5.4-H1 等待人工复核；`S6-T5.5` 及之后任务尚未批准。

目标：在 Retrieval 层评测 R1–R6，并为隐蔽知识污染检测与可信检索研究建立稳定证据接口。

- 学习顺序：[架构 ADR](../../docs/architecture/README.md) → [Stage 6 规格](../../docs/superpowers/specs/2026-07-01-stage6-rag-security-trustworthy-retrieval-design.md) → [实施计划](../../docs/superpowers/plans/2026-07-01-stage6-rag-security-trustworthy-retrieval.md)；
- S6-T5 权威设计：[受控检索与可追溯上下文规格](../../docs/superpowers/specs/2026-07-19-s6-t5-controlled-retrieval-traceable-context-design.md) → [八段式实施计划](../../docs/superpowers/plans/2026-07-19-s6-t5-controlled-retrieval-traceable-context.md) → [ADR 0008](../../docs/architecture/0008_retrieval_context_boundary.md)；
- 长期约束：[研究需求基线](../../docs/governance/long_term_research_requirements.md)；它规定 S6-T5 的 Dense-only 边界、Evidence/Citation 契约、上下文分级及 S6.1/6.2/7 路线；
- 实验总记录：[Experiment Master Record](../../docs/governance/experiment_master_record.md)；它索引 Stage 1–5 历史运行与 Stage 6 工程验证，不替代原始交付物；
- Codex 恢复入口：从仓库根 `AGENTS.md` 开始，并读取 `docs/governance/current_work_state.md`；GOV-PODR1、S6-T5.2、S6-T5.3-P1、S6-T5.3-H1 与 S6-T5.3 DenseRetriever 均已获人工验收；S6-T5.4 已批准启动但当前为 protocol blocker；
- 当前代码：[A1R 后的规范实现](../../src/llmguard/domains/retrieval/)；旧 `codeguarder.stage6_rag` 保持 import compatibility；
- P1 协议冻结：唯一 Resolver 只接收 `ContentRef + expected_content_hash`；正文能力 DTO 属于 `contracts/`，snapshot reader 与 legacy mapping 均为最小权限、无 fallback 设计；这不是 ContentResolver 实现，也不表示正文解析已验收；
- 数据：[Stage 6 R1–R6 数据](../../data/stage6_rag/)；Ground Truth 与运行时视图保持隔离；
- 复跑入口：可运行 Static、InMemory 与临时目录 Chroma 测试；真实 Embedding 测试默认 skip，需显式设置环境变量；
- 真实验收：固定 `paraphrase-multilingual-MiniLM-L12-v2` revision、CPU、五篇中文政策文档和临时 Chroma 重开均已验证；中英文休假查询 Top-1 均为 `doc-leave`，不保存正文、标签或 runtime 产物；
- 原始证据：尚未生成独立 `deliverables/stage6_rag/` 证据包；当前可核查的是早期数据、测试与
  架构决策，不能把它误称为完整 RAG 实验报告；
- 工程状态：当前是检索基础设施、分块与运行时契约状态，不是正式 RAG 安全攻击实验；S6-T5.3-H1 与 DenseRetriever 已获人工验收，S6-T5.4 为批准后暂停的 protocol blocker；
- 结论边界：已完成的是数据、契约、Embedding 与向量存储基础，不可宣称已有 Retriever、可信策略或 RAG 指标结果；
- 面试重点：为什么 RetrievalEvidence、EvidenceSignal、TrustedContextPackage 与 RAGSecurityEnvelope 必须分层。

## S6-T5 设计冻结摘要

- 当前 Chunking 基线是 `IdentityChunker`；复杂 Token/Overlap/Sentence/Semantic Chunking 只冻结协议，
  不创建空壳实现；
- Retriever 未来只输出无正文 `RetrievalEvidence` 与 `RetrievalTrace`，正文通过 canonical ContentRef 和
  hash 校验的 ContentResolver 受控解析；
- Evidence UID 用于跨运行追溯，Citation ID 用于单个 Context 内引用，两者通过 CitationBinding 关联；
- ContextBuilder 未来输出 `RetrievedContextPackage`，不能在 Trust Pipeline 前称为 Trusted；
- 设计完成不等于功能完成；下一步是人工审查，不是自动开始 S6-T5.1。

## S6-T5 设计加固留痕

- 唯一 stable DTO 归属已冻结为 `contracts/`；`chunking/`、`retrieval/`、`context/` 不得复制
  ChunkRecord、RetrievalEvidence、Package 等对象；
- Dataset QueryRecord 中的 `attack_id`、`expected_clean_doc_ids`、generation 字段必须在 explicit safe
  projection 时物理剥离，Retriever 只能收到最小 RuntimeQueryView；
- ContentRef 将在唯一 contracts validation contract 中同时识别 `corpus:` 与 legacy `chroma:`，新 producer
  只生成前者，legacy scheme 只映射 fixture corpus；
- EvidenceEnvelope/Package 的正文属于 runtime sensitive data：普通日志只用 `to_audit_dict()`，不能把
  `asdict()` 误称为安全接口；
- EMPTY/BUDGET 等结构性无 Context 可要求 abstention；hash、scheme、fingerprint、metric 不一致必须异常，
  不得伪装成普通拒答。

## S6-T5.1 已实现：确定性分块契约（待人工验收）

- 实现范围：`src/llmguard/domains/retrieval/contracts/{hashing,chunking}.py` 与
  `src/llmguard/domains/retrieval/chunking/`；稳定 DTO 只在 `contracts/` 定义，行为只在
  `chunking/` 实现。
- 当前能力：`IdentityChunker` 对一个经 `DocumentRecord.content_hash` 校验的文档输出一个未改写的
  `ChunkRecord`。chunk ID 由 canonical JSON + SHA-256 生成，content reference 固定为
  `corpus:<corpus_snapshot_id>:CH-<digest>`。
- 隔离边界：公开 metadata 深度冻结，拒绝 evaluator label、Ground Truth、攻击语义和绝对路径；审计
  导出不含正文，ChunkRecord 的 repr 不含正文。
- 验证证据：`tests/domains/retrieval/chunking/` 与 `tests/architecture/test_contract_ownership.py`；
  完整 TDD/验证留痕见 `deliverables/learning_notes.md`。
- 未实现：Retriever、ContentResolver、ContextBuilder、Trust、LLM/Groq、RAG 指标与 R1–R6
  正式实验。S6-T5.2 仍需另行人工批准。

## S6-T5.1 Implementation Hardening（待最终人工验收）

- `window_size` 已从稳定配置删除：fixed token 只用 `max_tokens`，token overlap 只用
  `max_tokens + overlap_tokens`，配置 hash 不包含无效字段。
- Chunking 错误的唯一稳定归属是 `contracts/errors.py`；`chunking.errors` 只作兼容 re-export，
  所有错误仍是 `ValueError` 子类且不回显正文、原始 doc ID、绝对路径或原始 metadata。
- `ChunkRecord` 新增 `chunk_schema_version`，并在构造时用唯一 `derive_chunk_id()` 验证自身 ID；
  content reference 仅能匹配经验证的 canonical identity。
- 当前状态：`Completed, pending final human acceptance`；S6-T5.2 仍未批准。

## S6-T5.2：检索运行时契约与 ID（已完成，待人工验收）

- 运行时查询不再复用数据集 `QueryRecord`：通过显式 safe projection 生成仅含 `query_id`、隐藏 repr 的 `retrieval_query` 与白名单 `public_metadata` 的 `RetrieverQueryRecord`。
- `RetrievalRequest` 固定 query hash、collection fingerprint、query embedding spec hash、retrieval config hash 与 `top_k`，以确定性 `RQ-<sha256>` 表示同一检索意图。
- `RetrievalEvidence` 演进为 chunk 级规范记录；`doc_id == chunk_id`，父文档单独保存。它不包含正文或查询，并且 Evidence UID 可复算。
- `RetrievalTrace` 仅保存 evidence summary、计数、hash、有限排序指标和 latency；latency 变化不会改变语义 trace hash。
- `chroma:` 仅为 S6-T4 fixture 兼容格式；新 producer 只使用 `corpus:<snapshot>:<chunk>`。

上述 S6-T5.2 段落是当时的历史契约快照。当前 S6-T5.3 DenseRetriever 与 H1 已获人工验收；S6-T5.4 ContentResolver 已获启动批准但因协议缺口暂停，ContextBuilder、citation、trust、LLM 和正式安全实验仍等待后续独立人工审批。
