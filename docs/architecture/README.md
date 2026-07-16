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
8. [目标目录结构](target_repository_structure.md)：未来新增文件的位置。

当前状态：`A0` 与 `A1R` 已完成；下一步在明确批准后才可进入 `S6-T4`，不能跳过测试直接
实现 Embedding、ChromaDB 或 Groq。
