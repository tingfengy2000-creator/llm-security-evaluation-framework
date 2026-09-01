# Paper 1 Human / Agent / Evidence Documentation Separation Contract

Document Role = `PAPER1_DOCUMENTATION_SEPARATION_CONTRACT`
Status = `OWNER_CONFIRMED`
Task = `GOV-P1-HUMAN-DOCS-INTEGRATION-01`

## HUMAN DOC

- 中文优先，第一次出现专业术语时保留英文并给出简短中文解释。
- 回答 `why / what / where / next`，让项目负责人、导师和新成员在 5/15/30 分钟内进入状态。
- 不复制 raw evidence，不堆叠 hash；必要状态码必须附中文解释，并通过链接下钻到权威或证据。
- 人类总览不产生新授权，不把 Pilot 或工程观察升级为正式论文结果。

## AGENT DOC

- 保留 explicit status、stable IDs、hashes、evidence paths、constraints、frozen definitions、field semantics 与 approval gates。
- 机器文档可使用 YAML、枚举和结构化表格，无须为了易读删除可恢复信息。
- Agent ledger 是派生镜像；冲突时按治理 authority order 回到 Owner 决定、动态状态、stage process、Git 与原始证据。

## EVIDENCE

- raw JSON/JSONL/log/XLSX/hash/manifest 是可审计事实载体，不作为人类第一阅读入口。
- 原始证据和人工 return 保持不可变；纠正采用追加记录与新命名空间，不覆盖历史痕迹。
- 文档可以链接、解释和限定证据，但不得替代证据、伪造执行或改变实验状态。
