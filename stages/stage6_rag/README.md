# Stage 6：RAG 安全与可信检索基线

目标：在 Retrieval 层评测 R1–R6，并为隐蔽知识污染检测与可信检索研究建立稳定证据接口。

- 学习顺序：[架构 ADR](../../docs/architecture/README.md) → [Stage 6 规格](../../docs/superpowers/specs/2026-07-01-stage6-rag-security-trustworthy-retrieval-design.md) → [实施计划](../../docs/superpowers/plans/2026-07-01-stage6-rag-security-trustworthy-retrieval.md)；
- 当前代码：[早期 Task 1–3 实现](../../src/codeguarder/stage6_rag/)；新规范路径为 `src/codeguarder/domains/retrieval/`，需在 Architecture Task 1 后创建；
- 数据：[Stage 6 R1–R6 数据](../../data/stage6_rag/)；Ground Truth 与运行时视图保持隔离；
- 复跑入口：当前仅可运行 Task 1–3 的离线测试，真实 Embedding/Chroma/Groq 尚未开始；
- 原始证据：尚未生成独立 `deliverables/stage6_rag/` 证据包；当前可核查的是早期数据、测试与
  架构决策，不能把它误称为完整 RAG 实验报告；
- 结论边界：已完成的是数据和契约基础，不可宣称已有真实检索、可信策略或 RAG 指标结果；
- 面试重点：为什么 RetrievalEvidence、EvidenceSignal、TrustedContextPackage 与 RAGSecurityEnvelope 必须分层。
