# 项目改名与历史证据台账

## A1R 生效记录

| 字段 | 值 |
| --- | --- |
| 旧名称 | `CodeGuarder` / `codeguarder` |
| 新名称 | `LLMGuard Research Framework` / `llmguard` |
| 生效任务 | `A1R` |
| 生效提交 | `c7d37f2` (`refactor(retrieval): establish llmguard canonical namespace`) |
| 历史产物策略 | 保留旧名称、路径、hash 和原始文本 |
| 保留原因 | 实验发生时事实、可追溯性、hash 完整性、旧 import 兼容 |

## 不改写的历史范围

- Stage 1–4.1 原始 JSON、JSONL、HTML、日志、截图、命令记录和报告；
- `data/stage5/`、Stage 5 及 Stage 5 Paper 的已记录产物；
- `src/codeguarder/stage5_paper/` 及其既有历史测试；
- `provenance/historical_baseline.sha256` 与既有 manifest；
- 记录当时路径或旧项目名称的历史计划、学习笔记和对话导出。

若历史结论本身有错误，只新增 correction log；不通过项目更名修改原始实验文本。精确路径名单
见 `config/naming_legacy_allowlist.yaml`。

## 当前可修改范围

当前 README、总控、架构、研究路线、Stage 6 规格与计划、导航、当前测试 import、当前
`pyproject.toml`、A1R 新源码、未来实验配置可以迁移到 LLMGuard 名称。

## 远端 URL 迁移记录

当前 URL：`https://github.com/tingfengy2000-creator/llm-security-evaluation-framework`。

建议的新仓库名：`llmguard-security-research-framework`。本轮不自动重命名远端；若用户后续
批准，需先备份 remote、在 GitHub 完成重命名、更新 `origin`、验证 `fetch/push`，再将旧 URL、
新 URL 和验证时间补记在本节。
