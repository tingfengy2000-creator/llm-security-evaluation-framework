# LLMGuard 架构决策索引

这里记录长期、可追溯且影响后续实现位置的架构决定。它不是实验结果目录，也不替代各 Stage
的原始 JSON、JSONL、HTML、日志和报告。

阅读顺序：

1. [Architecture Task 0 架构评审](architecture_task0_review.md)：事实、差距、风险、验收；
2. [ADR 0001](0001-research-platform-boundary.md)：研究平台边界；
3. [ADR 0002](0002-stage1-5-compatibility.md)：历史 Stage 1–5 兼容性；
4. [ADR 0003](0003-retrieval-domain-contracts.md)：Retrieval 契约和标签隔离；
5. [ADR 0004](0004-trusted-context-vs-audit-envelope.md)：运行时与审计对象分离；
6. [ADR 0005](0005-stage6-6_1-7-boundary.md)：Stage 6、6.1、7 的边界；
7. [ADR 0006](0006_namespace_migration.md)：LLMGuard 命名冻结与 namespace 迁移；
8. [ADR 0007](0007_embedding_vectorstore_boundary.md)：Embedding 与 VectorStore 基础设施边界；
9. [ADR 0008](0008_retrieval_context_boundary.md)：Retriever、正文解析、Citation 与 Context 的边界；
10. [目标目录结构](target_repository_structure.md)：未来新增文件的位置。

长期研究需求入口：[治理基线](../governance/long_term_research_requirements.md)。其中规定 RAG 安全
优先级、语料/标签治理、Evidence/Citation 契约和 S6-T5 以后阶段的最低能力；它不替代原始实验产物。

当前状态：`A0`、`A1R` 与 `S6-T4` 已完成；`S6-T5 Design Freeze` 已完成并等待人工审查，Python
实现尚未开始。只有设计规格和实施计划获明确批准后才可进入 `S6-T5.1`，不能跨越到 Trust、Groq 或
正式 RAG 实验。

S6-T5 权威入口：

- [设计规格](../superpowers/specs/2026-07-19-s6-t5-controlled-retrieval-traceable-context-design.md)；
- [实施计划](../superpowers/plans/2026-07-19-s6-t5-controlled-retrieval-traceable-context.md)。
