# ADR 0002：Stage 1–5 历史兼容与证据保护

## 状态

已接受，2026-07-16。

## 不可变范围

以下内容承担历史实验的可追溯证据责任，不删除、不移动、不覆盖、不批量重写：

- `llm-security-stage1/`；
- Stage 1–4.1 历史脚本和已有运行目录；
- `data/stage5/`；
- `src/codeguarder/stage5_paper/`；
- Stage 1–5 的 JSON、JSONL、HTML、日志、摘要和报告；
- 已被历史完整性校验使用的文件。

## 允许的增量变更

- 新增导航 README；
- 新增 compatibility adapter；
- 新增实验注册、artifact index 与脱敏索引；
- 新增历史完整性测试与 correction ledger；
- 修复明确的软件错误，同时保留旧证据并记录修正原因。

## 兼容策略

历史代码通过 `compatibility/stage1_4/`、`compatibility/stage4_guard/`、`compatibility/stage5/`、`compatibility/garak/` 接入新内核。适配器的输入、输出和版本必须写入测试；旧模块不得反向导入新领域实现的内部模块。

## 验收

- 历史路径 Git diff 为零；
- 既有 Stage 5/Stage 5 Paper 历史完整性测试继续通过；
- 新代码只能以新增文件或兼容入口方式引用历史成果；
- 对历史结论的修正使用新增 correction log，不修改原始报告。

## 退出策略

compatibility 层没有按日期删除的目标。只有当公开 API 已稳定、所有下游调用完成迁移、历史复现实验有独立归档且用户明确批准时，才可单独评审弃用范围。
