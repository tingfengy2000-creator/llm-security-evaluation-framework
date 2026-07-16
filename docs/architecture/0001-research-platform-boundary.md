# ADR 0001：研究平台边界与稳定分层

> A1R 补充：本文 A0 时的 `src/codeguarder/` 目标根已由
> [ADR 0006](0006_namespace_migration.md) 替换为 `src/llmguard/`；下方旧名称保留为决策历史。

## 状态

已接受，2026-07-16。

## 决策

LLMGuard Research Framework 冻结为三层研究平台：

```text
src/llmguard/
├── core/           # Runtime、Retrieval、Agent 共同复用的稳定能力
├── domains/        # 领域能力：runtime、retrieval、agent
└── compatibility/  # 历史阶段到新内核的适配器
```

`core/` 只承载通用契约、Provider、Guard、Detector、评估、报告、实验配置和审计能力。任何 RAG 专有字段、ChromaDB 细节、污染标签、检索排序逻辑都不得进入 `core/`。

`domains/retrieval/` 是 Stage 6、Stage 6.1 和可信检索研究的唯一规范实现位置。`domains/runtime/` 与 `domains/agent/` 只预留稳定边界；Stage 1–5 历史源码不会迁移或重写。

`compatibility/` 只允许 re-export、import alias、参数转换、弃用说明和历史调用适配。它不得复制业务逻辑，也不得让历史 Stage 直接依赖新目录内部细节。

## 背景与理由

项目已经从 garak 练习扩展为模型层、Runtime、RAG 与 Agent 的长期安全研究平台。继续以 Stage 目录堆叠实现，会导致 Runner、指标、报告和审计逻辑重复，进而阻碍论文复现和科技项目验收。

这次冻结保留“历史证据不可变”与“新能力可插件化”两个原则：历史目录承担证据责任，新平台目录承担未来规范实现责任。

## 后果

- Stage 6 Task 1–3 在 Architecture Task 1 中一次性迁移到 `domains/retrieval/`；
- `stage6_rag` 随后只做兼容门面，不能保留双份业务实现；
- Stage 6.1 的检测算法、可信聚合和重排必须作为 Retrieval 插件新增；
- Stage 7 只能消费稳定的业务上下文与审计信封，不得访问向量库内部对象或 Ground Truth。

## 非目标

- 不在本 ADR 中实现 `core/` 或迁移代码；
- 不重新组织 Stage 1–5 历史文件；
- 不把规则基线描述为论文算法贡献；
- 不公开私有实验仓库。
