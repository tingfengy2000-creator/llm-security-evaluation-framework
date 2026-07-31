# LLMGuard Context Authority Map

## 目的与适用范围

本文冻结 LLMGuard Research Framework 的 Git-native Research Context Recovery System。聊天、Thread、模型上下文、
Codex memory 和单台机器的本地记忆都不是唯一事实源。只要取得 Git 仓库，新协作者就应能恢复项目目标、当前
Stage/Task、Owner Decision、Paper 路线、实验/工程证据、Blocker、Claims Boundary、Technical Debt 与下一审批门。

本文件定义权威层级和冲突规则；具体启动步骤仍由 [上下文恢复协议](context_recovery_protocol.md) 执行。

## L0 — Git / Raw Evidence Authority

最高客观事实来源包括 Git branch、commit、tag、diff、raw experiment artifacts、RunManifest、dataset snapshot
hash、model revision、config hash、raw metric/result artifact 和 immutable historical experiment files。

L0 回答“实际上运行了什么、哪个 SHA 执行、tag 指向哪里、数据/模型是什么版本、结果是否真实存在”。
branch、HEAD、tag、working tree、artifact existence 与 upstream sync 必须动态核验。**Git dynamic facts override stale branch/SHA text**；文档不能让不存在的 commit、tag、run 或结果变成事实。

## L1 — AGENTS.md

[AGENTS.md](../../AGENTS.md) 负责 Codex 工作规则、Mandatory Startup Protocol、禁止事项、审批边界、namespace、
protected assets、TDD 和完成协议。目录内若未来出现更深的 `AGENTS.md`/`AGENTS.override.md`，只能细化作用域，
不能放宽历史不可变、标签隔离或审批门。

## L2 — Long-Term Research Requirements

[long_term_research_requirements.md](long_term_research_requirements.md) 负责长期研究目标、Paper 1/Paper 2/Stage 7
定位、项目优先级、不可删除能力、论文证据标准和长期治理要求。它不记录单次实验，也不动态声明当前 HEAD。

## L3 — Project Owner Decision Register

[project_owner_decision_register.md](project_owner_decision_register.md) 是 **OWNER-CONFIRMED DECISION AUTHORITY**，
只登记项目负责人明确确认的需求、优先级、研究方向、范围调整、机器角色、对标论文、延期/放弃和 Human
Acceptance。未经明确确认不得写 `ACCEPTED`，只能写 `PENDING_CONFIRMATION` 或 `UNKNOWN`。

## L4 — PROJECT_MASTER_CONTEXT.md

[PROJECT_MASTER_CONTEXT.md](../../PROJECT_MASTER_CONTEXT.md) 负责项目架构、Stage 关系、总体叙事、研究与工程
映射和当前系统能力。它不是 Experiment Log；其中的历史状态必须带日期，并由更新的 Owner Decision 和 Git
动态事实解释。

## L5 — Current Work State

[current_work_state.md](current_work_state.md) 是唯一动态任务状态入口，只回答“现在正在做什么”。它维护 current
branch、task、task type/status、current approval、formal experiment status、current blocker、next approval gate
和 must-not-start。branch/HEAD/upstream 的具体值仍由 L0 动态命令决定。

## L6 — Experiment Master Record

[experiment_master_record.md](experiment_master_record.md) 是唯一实验控制面与证据索引，区分
`FORMAL_EXPERIMENT`、`ENGINEERING_VALIDATION`、`DESIGN_FREEZE`、`FAILED_RUN`、`INVALID_RUN` 与历史实验
证据。普通开发活动不能全部塞入该文件；原始 artifact/manifest 的 L0 事实优先。

## L7 — Research Execution Log

[research_execution_log.md](research_execution_log.md) 是 **APPEND-ONLY CHRONOLOGICAL RESEARCH LEDGER**，按时间
记录项目如何推进、经过哪些门、做过什么验证、遇到什么 Blocker 和下一步是什么。历史错误只能追加
`CORRECTION` 或 `SUPERSEDING_RECORD`，不得静默修改。

## L8 — Accepted Stage Specs / Protocols / Research Routes

该层包括已接受 Stage specification、formal experiment protocol、canonical research route、baseline
reproduction protocol、dataset/method/metrics protocol。它们说明具体任务应如何执行，但不能证明已经执行。
Paper 1 当前唯一 canonical route 是
[paper1_research_route.md](../research/stage6_1_hidden_knowledge_poisoning/paper1_research_route.md)。

## L9 — Learning / Explanation Material

[docs/learning](../learning/README.md) 和历史 learning notes 是 **NON_AUTHORITATIVE_EDUCATIONAL_MATERIAL**，只用于
教学、面试、术语、架构和项目理解。它们不得覆盖 Git 事实、Owner Decision、Experiment Record 或 Accepted
Protocol，也不得作为实验结果的唯一证据。

## Context Conflict Resolution

1. Git 动态事实决定 branch、SHA、tag、diff、artifact existence 和 remote sync。
2. 较新的、合法的 Owner-confirmed decision 可以 supersede 较旧研究方案；必须记录 Decision ID、日期、证据和
   被替代对象。
3. Superseded 历史记录不得删除；用 `SUPERSEDING_RECORD` 或明确的历史快照说明保留。
4. 具体实验事实先看 raw artifact/RunManifest，再看对应 commit 和 Stage-specific acceptance，最后才看汇总。
5. 低层教学材料永远不能覆盖高层治理或原始证据。
6. 若无法确认哪项决定更新、冲突会改变数据/历史资产/审批门或来源不能验证，登记
   `CONTEXT_CONFLICT_BLOCKER`，停止关键研究工作并请求项目负责人决定。
7. 禁止用“根据之前应该是”“我记得”等聊天记忆推断研究事实；未知即写 `UNKNOWN`。

## Canonical File Responsibility Map

| 问题 | 唯一首要入口 | 不能替代它的材料 |
| --- | --- | --- |
| Git/运行事实是什么 | L0 Git + Raw Evidence | 静态状态文字、聊天 |
| Codex 可以做什么 | L1 `AGENTS.md` | learning notes |
| 长期目标是什么 | L2 长期需求 | 当前任务页 |
| 用户确认了什么 | L3 Owner Decision Register | 模型记忆 |
| 项目总体如何组织 | L4 Project Master Context | Experiment Log |
| 现在做什么 | L5 Current Work State | 历史 route |
| 哪些实验/结果存在 | L6 Experiment Master Record + L0 artifact | Execution Log |
| 项目如何推进 | L7 Research Execution Log | Experiment Master Record |
| 某任务应该如何做 | L8 accepted protocol/route | 教学文档 |
| 如何理解和面试表达 | L9 Learning Guides | 权威治理文件 |

## Mandatory Git Preflight

每台机器开始正式项目任务前执行：

```powershell
git fetch --prune --tags origin
git status --short --branch
git branch --show-current
git rev-parse HEAD
git log -15 --oneline
```

存在 upstream 且 working tree clean 时再执行 `git pull --ff-only`；upstream 不存在时报告 `NO_UPSTREAM`，不得猜测
远端状态或自动关联错误分支。fetch/pull 冲突、未知修改、HEAD 超预期或分叉都应 fail closed。

## New Codex Context Recovery Checklist

新 Thread、模型、机器、clone 或 context compression 后必须依次：

1. 执行 Mandatory Git Preflight，并检查 worktree、tag、upstream、ahead/behind 和 working tree。
2. 读取 `AGENTS.md`。
3. 读取本 Authority Map。
4. 读取长期需求、Owner Decision Register、Project Master Context、Current Work State。
5. 读取当前 Stage 的 canonical research route 与 task protocol/spec。
6. 读取相关 Experiment Master Record、Research Execution Log 和原始证据入口。
7. 检查更深层 `AGENTS.md`/override、protected paths、runtime ignore 和秘密边界。
8. 输出中文 `Context Recovery Report`；任何不能确认的字段写 `UNKNOWN`。
9. 未获得当前任务批准时停止，不自动进入下一 Task/Stage。

## Context Recovery Report 必填字段

- repository
- worktree
- branch
- HEAD
- tag
- upstream
- working tree
- project identity
- current stage
- current task
- task status
- current Paper 1 route
- owner-confirmed decisions
- current external baselines
- formal experiment status
- current blocker
- claims boundary
- next gate

报告必须同时说明允许修改、禁止修改、未提交/未推送状态，以及文档与 Git 是否冲突。动态字段不得从静态
文档复制后冒充已核验事实。

## 当前基线锚点

- S6-T5 baseline governance acceptance commit：`18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`。
- Recovered baseline tag：annotated `s6-t5-rag-baseline-v1`，`2026-07-31` 本地/远端核验指向上述 commit；
  实际存在性和 target 每次仍需动态核验。
- Accepted baseline content commit：`4ecf73a`。
- Last accepted implementation commit：`b136ee2`。
- Last accepted integration evidence：`b6cedf3`。
- Stage 1–5：immutable historical experiment assets。
- `FORMAL_EXPERIMENT = NOT STARTED` for current Stage 6.1 work。
- Historical pre-approval snapshot：`S6.1-LR1` 与 Context Recovery Governance 已 `HUMAN_ACCEPTED`；当时
  `S6.1-R0` 仅定义、尚未批准执行。
- Historical superseded fact：RTX5090 Bootstrap 已 `HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY`，`S6.1-R0` 曾
  `APPROVED_TO_START` on Compute Worker；首次 R0-I return 保留为历史快照。
- Superseding current fact：R0 is `HUMAN_ACCEPTED_WITH_BLOCKERS`；FU1 is `APPROVED / LOCAL-FIRST / WORKER-GATED`；
  P0 is `COMPLETED_PENDING_OWNER_REVIEW`；W1/W2 and P1 are not approved；Formal Experiment 仍未开始。
- Owner principle：Control-Plane-First Token Economy is accepted as execution-resource governance and cannot override
  Paper-First、safety、evidence quality、label isolation、immutable history or reproducibility。

这些静态锚点只表达已登记的治理身份；是否存在、当前 branch/HEAD/tag 和远端同步仍须由 L0 动态核验。
