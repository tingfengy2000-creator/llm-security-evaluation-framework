# Paper 1 Human / Agent / Evidence Documentation Separation Contract

Document Role = `PAPER1_DOCUMENTATION_SEPARATION_CONTRACT`
Status = `OWNER_CONFIRMED`
Task = `GOV-P1-MANDATORY-DOCUMENTATION-CLOSEOUT-01`

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

## PAPER 1 MANDATORY DOCUMENTATION CLOSEOUT

Owner 冻结：

- `PAPER1_MANDATORY_DOCUMENTATION_CLOSEOUT = OWNER_CONFIRMED`
- `PAPER1_HUMAN_LEDGER_SYNC_ON_TASK_CLOSE = MANDATORY`
- `AUTO_DOCUMENTATION_SYNC_POLICY = ACTIVE`
- `PAPER1_TASK_DOCUMENTATION_CLOSEOUT = MANDATORY`
- `PAPER1_HUMAN_LEDGER_CONTINUOUS_SYNC = MANDATORY`

每个 Paper 1 research、data、annotation、evaluation、governance、engineering、experiment、protocol、baseline、detector、
retrieval intervention 或 formal experiment 任务都包含 `TASK EXECUTION` 与 `TASK DOCUMENTATION CLOSEOUT` 两个阶段。
只有二者均通过才能报告任务完成。文档收口未通过时登记 `TASK_DOCUMENTATION_CLOSEOUT_BLOCKER`，状态上限为
`ENGINEERING_COMPLETED / DOCUMENTATION_CLOSEOUT_PENDING`。

永久完成定义：

`TASK_DONE = EXECUTION_DONE AND TESTS_PASS AND EVIDENCE_RECORDED AND DOCUMENTATION_CLOSEOUT_PASS AND GIT_STATUS_VALID`

即使未来 prompt 未重复本规则，仍须执行 closeout；即使 prompt 指定 `NO_DOCUMENTATION_CHANGE`，仍须完成条件评估并记录
无需修改 conditional documents 的理由。

## Mandatory Closeout Matrix

| canonical document | closeout rule |
| --- | --- |
| Human Ledger | `MANDATORY` for Paper 1 state-changing tasks |
| Agent Ledger | `MANDATORY` |
| Current Work State | `MANDATORY` |
| Research Execution Log | `MANDATORY` |
| Experiment Master | `CONDITIONAL`: experiment、dataset、candidate corpus、Ground Truth、annotation protocol、Evidence、metrics、run matrix、evaluation、formal result 或 approval gate 变化 |
| Owner Decision Register | `CONDITIONAL`: Owner approval/rejection/freeze/scope/method/gate decision |
| Stage Process | `CONDITIONAL`: 新 Pilot/annotation phase/Gate/experiment stage 或阶段结束、失败、回退 |
| Canonical Lessons | `CONDITIONAL`: 有跨未来数据集、Paper 2 或其它实验可复用的方法学经验 |
| Research Plan Authority | `ONLY IF` frozen research contract changes |
| README | `ONLY IF` navigation or entry changes |

禁止机械修改每个文件；conditional condition 为 false 时保留文件不变并在 closeout 记录评估结果。

## DOCUMENTATION_CLOSEOUT_CHECKLIST

每次 Final QA 至少逐项给出 true/false：

```text
human_ledger_checked
human_ledger_updated_if_required
agent_ledger_checked
agent_ledger_updated
current_work_state_updated
execution_log_appended
experiment_master_condition_evaluated
owner_decision_condition_evaluated
stage_process_condition_evaluated
lessons_condition_evaluated
research_authority_condition_evaluated
README_condition_evaluated
cross_document_current_task_consistent
cross_document_status_consistent
cross_document_next_action_consistent
cross_document_blocker_consistent
markdown_links_valid
```

任何 required field 为 false，必须 fail closed 为 `TASK_DOCUMENTATION_CLOSEOUT_BLOCKER`。

## PAPER1_DOCUMENT_STALENESS_GATE

至少交叉检查 Human Ledger、Agent Ledger、Current Work State 与 Experiment Master，禁止以下 stale state：旧任务仍标为
current、已解决 blocker 仍为 OPEN、next action 已完成、旧 commit 被写成 latest、旧 Pilot 阶段仍为 current、未经批准已启动
A/B、实际冻结前写 Dataset frozen，或 Formal Experiment 前写 formal result。动态 Git commit 必须从 Git 读取，不以静态文档
值替代当前事实。

## Lesson Promotion Policy

新增经验分为 `PROVISIONAL_LESSON` 与 `ACCEPTED_LESSON`。工程证据存在但相关 Pilot/Gate 尚未获得 Owner 最终验收时只能
登记为 provisional；只有相关 protocol/dataset/experiment 经 Owner 最终验收后才可提升为 accepted。

当前冻结：`PILOT4_PROTOCOL_LESSONS = PROVISIONAL_PENDING_FINAL_ACCEPTANCE`，以及
`PILOT4_LESSON_PROMOTION = AFTER_FINAL_ACCEPTANCE`。未来出现 `PILOT4_ANNOTATION_PROTOCOL_ACCEPTED` 时，对应 acceptance
任务必须执行 `PILOT4_PROTOCOL_LESSON_PROMOTION`，审查 canonical lessons 中列出的 18 项经验；Human Ledger 随后以
“问题 -> 原因 -> 最终规则”的通俗摘要解释经验并链接 canonical lessons。最终成功不得删除 Pilot4 的失败与修复时间线。
