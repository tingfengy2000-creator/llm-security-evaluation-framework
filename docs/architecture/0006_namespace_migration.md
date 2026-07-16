# ADR 0006：LLMGuard 命名冻结与 Namespace 迁移

## 状态

已接受，2026-07-16；由 `A1R` 实施。

## 决策

项目正式名称冻结为 **LLMGuard Research Framework**，中文名称为 **LLMGuard 大模型安全评测
与可信检索研究框架**，简称 **LLMGuard**。Python distribution 固定为
`llmguard-research-framework`，唯一规范 import namespace 为 `llmguard`。

`src/llmguard/` 是唯一的规范实现根；A1R 已将 Stage 6 Task 1–3 的规范 contracts、schema、
attack renderer 与 attack matrix 移至 `llmguard.domains.retrieval`。旧
`codeguarder.stage6_rag` 仅为 re-export facade，新旧公开对象必须保持同一 identity。

## 历史例外

`src/codeguarder/` 中的 Stage 5 与 Stage 5 Paper 仍是受保护的历史实现。本 ADR 不移动、
复制或重写它们；它们是“只读 legacy 例外”，不是以后新增业务代码的位置。例外路径和理由由
`config/naming_legacy_allowlist.yaml` 与 `docs/governance/project_rename_ledger.md` 精确记录。

## 后果

- 新业务代码只写入 `src/llmguard/`；
- `llmguard` 不得反向 import `codeguarder`；
- `data/stage6_rag/`、`tests/stage6_rag/` 等已入 manifest 的路径保留，以保护证据；
- 导航层迁移为规范 slug，历史代码、数据、交付物不随导航移动；
- 不使用 `llm-guard` 或 `llm_guard`，并在公开文档中声明与 Protect AI 的项目无关联；
- 本任务不开始 S6-T4，不下载模型、不创建 ChromaDB、不调用 Groq。
