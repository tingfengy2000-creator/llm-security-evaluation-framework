# LLMGuard Repository Agent Instructions

本文件是所有 Codex Thread、Agent、Workspace 和 Worktree 进入本仓库时的第一上下文入口，作用域为
整个仓库。当前没有嵌套 `AGENTS.md` 或 `AGENTS.override.md`；未来如新增，深层文件只细化其目录范围，
不得放宽本文件的历史不可变、标签隔离、审批门和安全约束。

## Project Identity

- Project: **LLMGuard Research Framework**
- Chinese name: **LLMGuard 大模型安全评测与可信检索研究框架**
- Canonical Python namespace: `llmguard`
- Legacy namespace: `codeguarder`
- 新业务代码只进入 `src/llmguard/`。
- `src/codeguarder/` 是历史实现和兼容入口，不新增 Stage 6 业务代码。
- Stage 1–5 是不可变历史实验资产。

## Project Priority

1. RAG Security Research
2. LLM Security Evaluation Platform
3. AI Guard Engineering
4. Agent Security Extension

## Canonical Context Sources

任何任务开始前按以下顺序读取和核对：

1. `AGENTS.md`
2. `docs/governance/context_authority_map.md`
3. `docs/governance/project_owner_sovereignty_and_mandatory_escalation_principle.md`
4. `docs/governance/current_work_state.md`
5. `PROJECT_MASTER_CONTEXT.md`
6. `docs/governance/project_owner_decision_register.md` 的最新相关决定
7. `docs/governance/long_term_research_requirements.md`
8. `docs/governance/experiment_master_record.md` 中的相关实验、证据和 blocker
9. 当前 Stage 的 canonical research route / `README.md`
10. 当前任务的 protocol/design specification 与 implementation plan
11. `docs/governance/research_execution_log.md` 的相关时间线记录
12. 最近 15 条 Git commit 与当前 branch、HEAD、worktree、status、tag、upstream sync

文件职责：长期需求记录用户目标、论文/立项方向和后续强制能力；项目负责人决策登记册记录已确认的解释
与决策；项目总控记录总体架构、阶段进度、
已验收成果和结论边界；动态状态记录当前任务与审批门；design spec 定义“设计成什么”；implementation
plan 定义“按什么顺序实现”；Git 是 branch、HEAD、工作树、提交和文件存在性的事实来源。上下文恢复
流程见 `docs/governance/context_recovery_protocol.md`；权威层级与冲突规则见
`docs/governance/context_authority_map.md`。Experiment Master Record 用于恢复实验路线、运行、指标与证据索引；
Research Execution Log 按时间记录项目推进。二者都不替代动态任务状态、项目架构或原始阶段产物。

## Mandatory Startup Protocol

修改文件前必须读取上述来源、检查实际 Git 状态，并用中文输出 Context Recovery Report。报告包含：

1. 项目长期目标；
2. 用户能力优先级；
3. 已完成到哪个 Stage/Task；
4. 当前 branch；
5. 当前 HEAD；
6. 当前任务；
7. 本轮允许修改什么；
8. 本轮禁止修改什么；
9. 下一审批门；
10. 文档与 Git 是否冲突；
11. 是否存在未提交或未推送修改；
12. 当前可以和不能宣称什么。

Git preflight 至少执行 `git fetch --prune --tags origin`、`git status --short --branch`、
`git branch --show-current`、`git rev-parse HEAD` 和 `git log -15 --oneline`。只有存在 upstream 且工作树 clean 时
才执行 `git pull --ff-only`；upstream 缺失、分叉或未知修改必须 fail closed 并报告，不得猜测。

若用户已明确批准当前任务，可在恢复报告后执行；若仍处于设计评审或未批准状态，必须暂停并等待批准。

## Instruction Priority

项目内部执行权威层级：

1. `L0`：动态 Git 事实与不可变 raw evidence，决定客观上存在或执行了什么；
2. `L0.5`：[PO-MHEP](docs/governance/project_owner_sovereignty_and_mandatory_escalation_principle.md)，决定发现事实后是否
   允许继续，是 `HIGHEST_INTERNAL_PROJECT_EXECUTION_AUTHORITY`；
3. `L1` 及以下：本文件、长期需求、Owner Decision、项目总控、动态状态、账本、accepted spec/plan 和学习材料。

L0.5 不能篡改 L0，也不能绕过更高层安全、法律、隐私、许可或平台约束。以下项目文档/任务解释顺序只在 L1 及
以下适用，不能覆盖 L0/L0.5。最新 prompt 只有在它本身是项目负责人的明确决定时才能 supersede 较旧项目决定，且
不得静默豁免 PO-MHEP 的升级和停止义务：

1. 用户在当前会话中的最新明确要求；
2. `docs/governance/long_term_research_requirements.md`；
3. `docs/governance/project_owner_decision_register.md`；
4. `PROJECT_MASTER_CONTEXT.md`；
5. `docs/governance/current_work_state.md`；
6. 当前任务 design specification；
7. 当前任务 implementation plan；
8. 较早的历史计划和学习笔记。

branch、HEAD、working tree、文件和 commit 是否存在、本地与远端是否同步，始终以 Git 为准。发现无法
由上述优先级安全解释的冲突时必须停止并报告，不得自行选择版本继续。长期需求与项目负责人决策登记册
冲突时同样必须停止并报告，不得自行覆盖长期基线。

## Mandatory Human Escalation

完整规则见 [PO-MHEP](docs/governance/project_owner_sovereignty_and_mandatory_escalation_principle.md)。发现以下任一类
情况时，受影响工作立即进入 `HUMAN_DECISION_REQUIRED` 且 `Auto Continue = NO`：

- accepted boundary、Worker contract、claims boundary 或 canonical current-state 冲突；
- 真实 API/token/login/付费服务、未批准外部源或身份不确定的网络替代；
- 系统级安装、管理员权限、大型下载、资源超限、不可逆/污染/数据丢失风险；
- 算法语义 patch、label/Ground Truth 泄漏、架构强耦合、重大技术债或不可恢复运行；
- novelty、baseline fairness、protocol alignment、统计、confounder、许可或论文结论风险；
- 缺 command/flags/stdout/stderr/exit code、只有摘要/估算、身份未绑定、index/archive/manifest 不完整；
- 两个以上会显著影响论文、架构、资源、复现或后续 Stage 的方案，或本机不能高置信判断。

触发后不得默认继续、静默 workaround、下载/安装、调用外部服务、让 Worker 继续、关闭 blocker 或进入下一任务。
只允许只读核验、决策风险分析、证据/上下文保存和 Git/治理记录更新。反馈必须使用 PO-MHEP 的十二字段
decision-ready 格式，不能只说“请人工处理”。

所有 Stage/spec/Worker contract/experiment 前必须执行 `FORWARD_RISK_REVIEW`；论文路线、baseline、dataset、attack、
detector、metric、formal protocol、首次正式运行、ablation、generalization、结论、SOTA 和投稿前必须执行
`PAPER_RISK_REVIEW`。

## Permanent Project Constraints

### Historical Immutability

- 不删除、移动、覆盖 Stage 1–5 历史代码、数据、JSON/JSONL、HTML、日志和报告。
- 历史错误使用 correction log 或新实验修正，不重写原证据。
- 不为测试变绿而重算历史 hash。
- CRLF/LF 历史假阳性只能登记为技术债，不得修改历史文件迎合旧字节清单。

### Namespace and Architecture

- 新实现只进入 `src/llmguard/`；不在 `src/codeguarder/` 新增 Stage 6 业务实现。
- Retrieval、Runtime、Agent Domain 保持边界。
- Ground Truth 只能由 Evaluator/GroundTruthVault 访问。

### Label Isolation

Retriever、VectorStore、ContextBuilder、Guard、LLM 和 Agent 不得访问或暴露：

```text
poisoned, poison_label, label, attack_id, attack_goal, attack_category,
expected_answer, expected_behavior, failure_type, ground_truth, oracle,
risk_goal, stealth_level
```

无防护实验可让污染正文进入受控 Context，但“该正文属于污染样本”的评估标签不得进入运行时链路。

### Evidence and Citation

以下后续能力是 mandatory，不得删除或降级为 optional：Evidence UID、Citation ID、Citation Binding、
XML-like Evidence Envelope、citation mode `off/available/required`、Citation Accuracy、引用支持度、
幻觉溯源和污染证据归因。

### Chunking and Retrieval Baselines

后续必须真实实现 Fixed Token Chunking、Token Overlap、Sentence Chunking、Semantic Chunking，并在论文
阶段实现或比较 BM25、Dense Retrieval、Hybrid Retrieval、普通 Reranker 和 Trust-aware Reranker。

### Trust and Abstention

后续必须实现 EvidenceSignal、TrustAggregator、RetrievalPolicy、Evidence Consistency、Evidence
Trustworthiness、多来源冲突检测、可信证据子集选择、鲁棒聚合和 abstention/refusal。

### Agent Security

Stage 7 必须研究 Tool Injection、Memory Poisoning、Planning Manipulation、Unsafe Tool Intent，以及 RAG
污染向 Agent 决策和工具调用的传播。Agent 只能消费 `TrustedContextPackage` +
`RAGSecurityEnvelope`，不得直接访问 ChromaDB、Ground Truth 或完整知识库。

## Current Approval Gate

当前任务、允许范围和未批准项以 `docs/governance/current_work_state.md` 为准。未获批准的任务不得启动；
不得从设计自动跳到实现，不得从一个 Stage 自动进入下一 Stage。每个 Task 和子任务都需要明确审批门。

RTX5090 永远仅为 `COMPUTE_WORKER / NO_SELF_APPROVAL_AUTHORITY`。任何新依赖、patch、输入/模型/网络变化、资源超限、
算法异常、环境偏差、证据缺口、未冻结参数或人工安装需求都必须 `STOP / RETURN_TO_CONTROL_PLANE`。

## Completion Protocol

每个任务结束前必须执行 `DOCUMENTATION CLOSEOUT GATE`。Paper 1 任务的完整完成条件永久冻结为
`EXECUTION_DONE AND TESTS_PASS AND EVIDENCE_RECORDED AND DOCUMENTATION_CLOSEOUT_PASS AND GIT_STATUS_VALID`；缺少文档收口时只能
报告 `ENGINEERING_COMPLETED / DOCUMENTATION_CLOSEOUT_PENDING`，并登记 `TASK_DOCUMENTATION_CLOSEOUT_BLOCKER`。

每个 Paper 1 任务无论 prompt 是否重复要求，都必须检查并按条件同步
[Paper 1 Documentation Separation Contract](docs/research/stage6_1_hidden_knowledge_poisoning/documentation_separation_contract.md)
规定的 Human Ledger、Agent Ledger、Current Work State、Research Execution Log 及条件式文档矩阵。即使任务明确写
`NO_DOCUMENTATION_CHANGE`，仍须执行条件判断并记录为什么 conditional documents 无需改动；禁止为了制造 diff 机械修改所有文件。

每个任务结束前还必须：

1. 更新 `docs/governance/current_work_state.md`；
2. 更新 `PROJECT_MASTER_CONTEXT.md` 的状态、结论边界和下一步；
3. 根据 closeout matrix 判断当前 Stage README、learning/canonical lessons、Experiment Master、Owner Decision Register、
   Stage Process 与 Research Plan Authority 是否需要更新；
4. 运行任务测试、Ruff、MyPy、标签泄漏检查、secret scan 和 runtime Git-ignore 检查；
5. 创建清晰 commit 并 push；
6. 确认本地与远端同步、工作树干净；
7. 执行 `CONTEXT_PERSISTENCE_CHECK` 和 `PAPER1_DOCUMENT_STALENESS_GATE`，确认 task/status、批准/禁止项、blocker、
   next gate、claims、Formal Experiment、Git sync、private evidence hash/index 均可从物理文件恢复；
8. 完成 `DOCUMENTATION_CLOSEOUT_CHECKLIST`；任何 required field 为 false 时 fail closed；
9. 完成后暂停，不自动开始下一任务。

研究路线、Owner Decision、Blocker、实验/工程验证或审批门发生变化时，还必须追加
`docs/governance/research_execution_log.md`；历史记录错误用 `CORRECTION`/`SUPERSEDING_RECORD`，不得静默覆盖。
`docs/learning/` 始终是 `NON_AUTHORITATIVE_EDUCATIONAL_MATERIAL`，不能覆盖 Git、Owner Decision、Experiment
Record 或 accepted protocol。

`docs/governance/long_term_research_requirements.md` 只有在用户长期目标变化时才能修改；普通实现任务不得
随意重写它。
