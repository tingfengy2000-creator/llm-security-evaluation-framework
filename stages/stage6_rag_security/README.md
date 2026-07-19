# Stage 6：RAG 安全与可信检索基线

## Metadata

- stage_id: `S6`
- canonical_name: `RAG Security Evaluation`
- canonical_slug: `stage6_rag_security`
- legacy_paths: `stages/stage6_rag/`、`data/stage6_rag/`、`tests/stage6_rag/`
- status: `s6_t5_design_hardening_completed_pending_second_human_review`
- objective: 在 S6-T4 基础上加固受控 Dense Retrieval 的唯一契约、Query 投影、ContentRef、敏感序列化与失败边界。
- source_locations: `src/llmguard/domains/retrieval/{contracts,attacks,embedding,vectorstore}/`
- data_locations: `data/stage6_rag/`（已入 manifest 的历史数据路径）
- test_locations: `tests/stage6_rag/`、`tests/architecture/`、`tests/domains/retrieval/`、`tests/integration/retrieval/`
- script_locations: 真实模型测试由 `LLMGUARD_RUN_REAL_EMBEDDING_TESTS=1` 显式开启，无 S6-T4 运行脚本；2026-07-19 已完成一次固定 revision 的真实验收。
- deliverable_locations: 尚未生成独立 Stage 6 证据包。
- evidence_locations: `data/stage6_rag/documents/corpus_manifest.json`
- conclusion_boundary: 已完成 embedding/vectorstore 基础设施和 S6-T5 设计加固；未实现 Retriever、ContextBuilder、Trust、LLM 或 RAG 指标。
- next_stage: 第二次人工审查 hardened design、迁移矩阵与计划；`S6-T5.1 implementation: Not approved`。

目标：在 Retrieval 层评测 R1–R6，并为隐蔽知识污染检测与可信检索研究建立稳定证据接口。

- 学习顺序：[架构 ADR](../../docs/architecture/README.md) → [Stage 6 规格](../../docs/superpowers/specs/2026-07-01-stage6-rag-security-trustworthy-retrieval-design.md) → [实施计划](../../docs/superpowers/plans/2026-07-01-stage6-rag-security-trustworthy-retrieval.md)；
- S6-T5 权威设计：[受控检索与可追溯上下文规格](../../docs/superpowers/specs/2026-07-19-s6-t5-controlled-retrieval-traceable-context-design.md) → [八段式实施计划](../../docs/superpowers/plans/2026-07-19-s6-t5-controlled-retrieval-traceable-context.md) → [ADR 0008](../../docs/architecture/0008_retrieval_context_boundary.md)；
- 长期约束：[研究需求基线](../../docs/governance/long_term_research_requirements.md)；它规定 S6-T5 的 Dense-only 边界、Evidence/Citation 契约、上下文分级及 S6.1/6.2/7 路线；
- Codex 恢复入口：从仓库根 `AGENTS.md` 开始，并读取 `docs/governance/current_work_state.md`；S6-T5 设计加固已完成并等待第二次人工审查，Python 实现尚未批准；
- 当前代码：[A1R 后的规范实现](../../src/llmguard/domains/retrieval/)；旧 `codeguarder.stage6_rag` 保持 import compatibility；
- 数据：[Stage 6 R1–R6 数据](../../data/stage6_rag/)；Ground Truth 与运行时视图保持隔离；
- 复跑入口：可运行 Static、InMemory 与临时目录 Chroma 测试；真实 Embedding 测试默认 skip，需显式设置环境变量；
- 真实验收：固定 `paraphrase-multilingual-MiniLM-L12-v2` revision、CPU、五篇中文政策文档和临时 Chroma 重开均已验证；中英文休假查询 Top-1 均为 `doc-leave`，不保存正文、标签或 runtime 产物；
- 原始证据：尚未生成独立 `deliverables/stage6_rag/` 证据包；当前可核查的是早期数据、测试与
  架构决策，不能把它误称为完整 RAG 实验报告；
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
