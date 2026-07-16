# Stage 6：RAG 安全与可信检索基线

## Metadata

- stage_id: `S6`
- canonical_name: `RAG Security Evaluation`
- canonical_slug: `stage6_rag_security`
- legacy_paths: `stages/stage6_rag/`、`data/stage6_rag/`、`tests/stage6_rag/`
- status: `a1r_migrated`
- objective: 在 Retrieval 层评测 R1–R6，并冻结可信检索研究接口。
- source_locations: `src/llmguard/domains/retrieval/`
- data_locations: `data/stage6_rag/`（已入 manifest 的历史数据路径）
- test_locations: `tests/stage6_rag/`、`tests/architecture/`
- script_locations: 尚未创建 S6-T4 之后的脚本。
- deliverable_locations: 尚未生成独立 Stage 6 证据包。
- evidence_locations: `data/stage6_rag/documents/corpus_manifest.json`
- conclusion_boundary: 仅有 Task 1–3 数据与契约基础，未实现真实检索。
- next_stage: `S6.1 stage6_1_hidden_knowledge_poisoning`

目标：在 Retrieval 层评测 R1–R6，并为隐蔽知识污染检测与可信检索研究建立稳定证据接口。

- 学习顺序：[架构 ADR](../../docs/architecture/README.md) → [Stage 6 规格](../../docs/superpowers/specs/2026-07-01-stage6-rag-security-trustworthy-retrieval-design.md) → [实施计划](../../docs/superpowers/plans/2026-07-01-stage6-rag-security-trustworthy-retrieval.md)；
- 当前代码：[A1R 后的规范实现](../../src/llmguard/domains/retrieval/)；旧 `codeguarder.stage6_rag` 保持 import compatibility；
- 数据：[Stage 6 R1–R6 数据](../../data/stage6_rag/)；Ground Truth 与运行时视图保持隔离；
- 复跑入口：当前仅可运行 Task 1–3 的离线测试，真实 Embedding/Chroma/Groq 尚未开始；
- 原始证据：尚未生成独立 `deliverables/stage6_rag/` 证据包；当前可核查的是早期数据、测试与
  架构决策，不能把它误称为完整 RAG 实验报告；
- 结论边界：已完成的是数据和契约基础，不可宣称已有真实检索、可信策略或 RAG 指标结果；
- 面试重点：为什么 RetrievalEvidence、EvidenceSignal、TrustedContextPackage 与 RAGSecurityEnvelope 必须分层。
