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
2. `docs/governance/long_term_research_requirements.md`
3. `docs/governance/project_owner_decision_register.md`
4. `PROJECT_MASTER_CONTEXT.md`
5. `docs/governance/current_work_state.md`
6. `docs/governance/experiment_master_record.md`
7. 当前 Stage 的 `README.md`
8. 当前任务的 design specification
9. 当前任务的 implementation plan
10. 最近 15 条 Git commit
11. 当前 branch、HEAD、worktree、status 和 upstream sync

文件职责：长期需求记录用户目标、论文/立项方向和后续强制能力；项目负责人决策登记册记录已确认的解释
与决策；项目总控记录总体架构、阶段进度、
已验收成果和结论边界；动态状态记录当前任务与审批门；design spec 定义“设计成什么”；implementation
plan 定义“按什么顺序实现”；Git 是 branch、HEAD、工作树、提交和文件存在性的事实来源。上下文恢复
流程见 `docs/governance/context_recovery_protocol.md`。Experiment Master Record 用于恢复实验路线、运行、指标
与证据索引；它不替代动态任务状态、项目架构或原始阶段产物。

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

若用户已明确批准当前任务，可在恢复报告后执行；若仍处于设计评审或未批准状态，必须暂停并等待批准。

## Instruction Priority

冲突优先级：

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

## Completion Protocol

每个任务结束前必须：

1. 更新 `docs/governance/current_work_state.md`；
2. 更新 `PROJECT_MASTER_CONTEXT.md` 的状态、结论边界和下一步；
3. 更新当前 Stage README 和学习笔记；
4. 运行任务测试、Ruff、MyPy、标签泄漏检查、secret scan 和 runtime Git-ignore 检查；
5. 创建清晰 commit 并 push；
6. 确认本地与远端同步、工作树干净；
7. 完成后暂停，不自动开始下一任务。

`docs/governance/long_term_research_requirements.md` 只有在用户长期目标变化时才能修改；普通实现任务不得
随意重写它。
