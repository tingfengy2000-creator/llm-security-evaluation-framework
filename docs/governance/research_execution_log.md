# LLMGuard Research Execution Log

## Ledger Contract

> 本文件是项目级追加式审计日志，用于保存治理和执行时间线。<br>
> 它不是 Paper 1 人类实验总账。<br>
> Paper 1 人类入口见：`docs/research/stage6_1_hidden_knowledge_poisoning/human/experiment_ledger_tingfeng.md`<br>
> Paper 1 智能体入口见：`docs/research/stage6_1_hidden_knowledge_poisoning/agent/experiment_ledger_agentUse.md`

本文是 **APPEND-ONLY CHRONOLOGICAL RESEARCH LEDGER**。它回答“项目实际上如何一步一步推进”，不替代 Git、
原始实验 artifact、Experiment Master Record、Current Work State 或 Owner Decision Register。

- 已提交记录不得静默改写或删除。
- 错误使用新的 `CORRECTION` 记录；方案变化使用新的 `SUPERSEDING_RECORD`。
- 每条记录的 `Auto Continue` 默认为 `NO`。
- 未知历史字段写 `NOT_RECORDED`，不得凭聊天记忆补齐。
- Git SHA、branch、tag 和 artifact existence 冲突时，以动态 Git/L0 事实为准。

## Record Schema

每条记录至少包含：Record ID、Date、Timestamp、Machine、Machine Role、Stage、Task ID、Task Name、Task Type、
Initial Status、Final Status、Objective、Why、Previous Gate、Actions、Files Changed、Commands、Validation、Git
Branch、Git SHA、Run ID、Dataset Snapshot、Model / Revision、Environment Identity、Result Summary、Claims
Allowed、Claims Prohibited、Blockers、Blocker ID、Resolution、Owner Decisions、Design Changes、Next Step、Next
Approval Gate、Auto Continue。

## REL-2026-0001 — Stage 1–5 Major Milestones Index

- Record ID: `REL-2026-0001`
- Date: `2026-07-01`
- Timestamp: `NOT_RECORDED`
- Machine: `LOCAL`
- Machine Role: `CONTROL_PLANE`
- Stage: `Stage 1–5`
- Task ID: `HISTORICAL-MILESTONE-INDEX`
- Task Name: `Model Security, Guard A/B and Runtime Evaluation Milestones`
- Task Type: `DOCUMENTATION`
- Initial Status: `HISTORICAL_EVIDENCE_EXISTS`
- Final Status: `INDEXED_WITHOUT_REWRITE`
- Objective: 为 Stage 1–5 已存在不可变历史实验建立高层索引。
- Why: 允许新协作者定位证据，同时避免复制或改写完整历史。
- Previous Gate: `N/A`
- Actions: 指向 Experiment Master Record 和原始 deliverables；不回填每条日常开发活动。
- Files Changed: `NOT_RECORDED`
- Commands: `NOT_RECORDED`
- Validation: 以历史 manifest、JSON/JSONL、日志、报告及完整性测试为准。
- Git Branch: `NOT_RECORDED`
- Git SHA: `MULTIPLE; resolve from Git and Experiment Master Record`
- Run ID: `MULTIPLE; see Experiment Master Record`
- Dataset Snapshot: `MULTIPLE; see original artifacts`
- Model / Revision: `MULTIPLE; missing fields remain NOT_RECORDED`
- Environment Identity: `PARTIALLY_RECORDED`
- Result Summary: Stage 1–5 已有模型层扫描、Mock/Real、Guard A/B、消融和确定性 runtime evidence。
- Claims Allowed: 仅限各历史 artifact 明确支持的配置和样本范围。
- Claims Prohibited: 不得将历史小样本或 Mock 扩张为生产安全结论。
- Blockers: 历史 manifest/revision 缺口与 CRLF/LF 技术债。
- Blocker ID: `BLK-HIST-001; BLK-HIST-002; BLK-HIST-003`
- Resolution: 保留原始证据，未来 correction/new run 只增量添加。
- Owner Decisions: `PODR-005; PODR-006`
- Design Changes: `N/A`
- Next Step: 只在单独批准后补充历史 Learning Guide 或新实验。
- Next Approval Gate: `SEPARATE_APPROVAL_REQUIRED`
- Auto Continue: `NO`

## REL-2026-0002 — S6-T5 Accepted Retrieval/Context Baseline

- Record ID: `REL-2026-0002`
- Date: `2026-07-27`
- Timestamp: `NOT_RECORDED`
- Machine: `LOCAL`
- Machine Role: `CONTROL_PLANE`
- Stage: `Stage 6 / S6-T5`
- Task ID: `GOV-S6-T5-BASELINE-ACCEPTANCE`
- Task Name: `S6-T5 Controlled Retrieval and Traceable Context Baseline`
- Task Type: `GOVERNANCE`
- Initial Status: `COMPLETED_PENDING_HUMAN_ACCEPTANCE`
- Final Status: `HUMAN_ACCEPTED BASELINE`
- Objective: 接受 deterministic、controlled retrieval-to-context engineering baseline 并冻结证据 taxonomy。
- Why: 为 Stage 6.1 提供不混淆实现、集成证据和治理接受的稳定起点。
- Previous Gate: `S6-T5.8-H1 review`
- Actions: 接受 S6-T5.8/H1；登记 implementation/integration/content/governance commit 身份。
- Files Changed: 见 baseline acceptance commit 的 Git diff。
- Commands: 见历史治理记录。
- Validation: 见 baseline acceptance report；不覆盖其历史测试快照。
- Git Branch: `feature/stage6-rag`
- Git SHA: `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`
- Run ID: `N/A`
- Dataset Snapshot: `N/A`
- Model / Revision: `N/A`
- Environment Identity: `N/A`
- Result Summary: `4ecf73a` accepted content；`b136ee2` accepted implementation；`b6cedf3` integration evidence。
- Claims Allowed: 受控、离线、label-isolated retrieval/context engineering baseline 已接受。
- Claims Prohibited: 不证明 RAG security、poisoning detection、retrieval metrics、LLM chain 或生产可用性。
- Blockers: 预期 tag `s6-t5-rag-baseline-v1` 后续动态核验仍缺失。
- Blocker ID: `TO_VERIFY_TAG; not a formal experiment blocker`
- Resolution: 不擅自创建或移动 tag；等待明确治理决定。
- Owner Decisions: `PODR-034`
- Design Changes: `N/A`
- Next Step: 任何 Stage 6.1 工作单独审批。
- Next Approval Gate: `STAGE_6_1_SEPARATE_APPROVAL`
- Auto Continue: `NO`

## REL-2026-0003 — Stage 6.1 Research Branch Creation

- Record ID: `REL-2026-0003`
- Date: `2026-07-31`
- Timestamp: `NOT_RECORDED`
- Machine: `LOCAL`
- Machine Role: `CONTROL_PLANE`
- Stage: `Stage 6.1`
- Task ID: `S6.1-BRANCH-CREATION`
- Task Name: `Create research/stage6-1-hidden-poisoning from accepted baseline`
- Task Type: `GOVERNANCE`
- Initial Status: `APPROVED_TO_CREATE`
- Final Status: `COMPLETED`
- Objective: 从 accepted S6-T5 baseline 建立 Paper 1 研究分支。
- Why: 隔离长期论文研究与已接受 baseline。
- Previous Gate: `PODR-034`
- Actions: 从 `18cf2741...` 创建 `research/stage6-1-hidden-poisoning`；未创建/move tag。
- Files Changed: `N/A`
- Commands: `git switch -c research/stage6-1-hidden-poisoning 18cf2741...`
- Validation: branch/HEAD/worktree 由 Git 动态核验。
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`
- Run ID: `N/A`
- Dataset Snapshot: `N/A`
- Model / Revision: `N/A`
- Environment Identity: `N/A`
- Result Summary: 分支建立；baseline 内容未修改。
- Claims Allowed: 仅可声称研究分支从 accepted baseline 创建。
- Claims Prohibited: 不得声称 Stage 6.1 experiment 已开始。
- Blockers: baseline tag absent。
- Blocker ID: `TO_VERIFY_TAG`
- Resolution: 保持 tag 不变并记录缺失。
- Owner Decisions: `PODR-035`
- Design Changes: `N/A`
- Next Step: 执行批准的 LR1 对齐。
- Next Approval Gate: `S6.1-LR1`
- Auto Continue: `NO`

## REL-2026-0004 — Paper-First Route Supersedes Immediate P1 Drafting

- Record ID: `REL-2026-0004`
- Date: `2026-07-31`
- Timestamp: `NOT_RECORDED`
- Machine: `LOCAL`
- Machine Role: `CONTROL_PLANE`
- Stage: `Stage 6.1`
- Task ID: `S6.1-LR1-ROUTE-SHIFT`
- Task Name: `Paper 1 Literature / Benchmark / Reproduction Alignment Priority`
- Task Type: `DESIGN_FREEZE`
- Initial Status: `S6.1-P1_PLANNED_NEXT`
- Final Status: `S6.1-P1_DEFERRED_UNTIL_LR1_REVIEW`
- Objective: 正式协议前先完成权威论文、源码、公开数据、指标、Published Result 和复现性对齐。
- Why: 防止方法和指标只围绕自建数据，且避免错误 SOTA 比较。
- Previous Gate: `Stage 6.1 branch created`
- Actions: 接受 Paper-First Comparative Evidence Principle；建立 LR1。
- Files Changed: 见 `1294632`。
- Commands: first-party paper/repository verification；无 experiment command。
- Validation: source alignment and architecture governance tests。
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `1294632ca0501e7b999a29383780bec49eaa6b04`
- Run ID: `N/A`
- Dataset Snapshot: `N/A`
- Model / Revision: `N/A`
- Environment Identity: `N/A`
- Result Summary: S6.1-P1 暂缓，LR1 成为当前任务。
- Claims Allowed: 可声称 Paper-first 路线已确认。
- Claims Prohibited: 不得声称 formal protocol/experiment 已开始。
- Blockers: strict comparison artifact/license/environment gaps。
- Blocker ID: `BLK-S6.1-LR1-001`
- Resolution: 先完成 LR1 并等待人工验收。
- Owner Decisions: `PODR-035; PODR-036`
- Design Changes: 原计划先做 P1；当前先做 LR1。Who: project owner；When: 2026-07-31；Evidence: owner instruction。
- Next Step: LR1 evidence alignment。
- Next Approval Gate: `S6.1-LR1_HUMAN_REVIEW`
- Auto Continue: `NO`

## REL-2026-0005 — S6.1-LR1 External Alignment Candidate

- Record ID: `REL-2026-0005`
- Date: `2026-07-31`
- Timestamp: `NOT_RECORDED`
- Machine: `LOCAL`
- Machine Role: `CONTROL_PLANE`
- Stage: `Stage 6.1`
- Task ID: `S6.1-LR1`
- Task Name: `Paper 1 Literature, Benchmark, Source Code, Hardware and Reproduction Alignment`
- Task Type: `REPRODUCTION_AUDIT / DOCUMENTATION`
- Initial Status: `APPROVED_TO_START`
- Final Status: `COMPLETED_PENDING_HUMAN_ACCEPTANCE`
- Objective: 对齐 PoisonedRAG、GMTP、SafeRAG、硬件和复现边界，形成 Paper 1 三轨路线。
- Why: 为后续严格比较、可复现性和 5090 worker 规划建立控制面。
- Previous Gate: `PODR-035`
- Actions: 核验一手论文/仓库；登记 commit/license；建立 matrix、route、protocol、hardware policy。
- Files Changed: 见 commit `1294632`。
- Commands: 仅 source/Git/document/test 检查；未运行外部 baseline。
- Validation: architecture `81 passed`；namespace/label checks、Ruff、MyPy、links、secret/path/integrity checks。
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `1294632ca0501e7b999a29383780bec49eaa6b04`
- Run ID: `N/A`
- Dataset Snapshot: `N/A`
- Model / Revision: `N/A`
- Environment Identity: `LOCAL / CONTROL_PLANE`; no experiment environment。
- Result Summary: 外部对齐候选完成；EcoSafeRAG deferred；formal run 未开始。
- Claims Allowed: literature/artifact/governance alignment only。
- Claims Prohibited: reproduction、5090 measurement、detector effectiveness、SOTA、production readiness。
- Blockers: source/license/revision/hardware unknowns block strict reproduction。
- Blocker ID: `BLK-S6.1-LR1-001`
- Resolution: 保持 OPEN，后续单独批准 artifact resolution/reproduction preparation。
- Owner Decisions: `PODR-035`
- Design Changes: Paper 1 收缩为四类 attack、五视角与三条 track；没有增加未批准 taxonomy。
- Next Step: 人工审查 LR1。
- Next Approval Gate: `ACCEPT_OR_REJECT_S6.1_LR1`
- Auto Continue: `NO`

## REL-2026-0006 — Git-Native Research Context Recovery Governance

- Record ID: `REL-2026-0006`
- Date: `2026-07-31`
- Timestamp: `2026-07-31T17:40:10+08:00`
- Machine: `LOCAL`
- Machine Role: `CONTROL_PLANE`
- Stage: `Stage 6.1`
- Task ID: `S6.1-LR1-CONTEXT-RECOVERY-GOVERNANCE`
- Task Name: `Establish Git-native Research Context Recovery System`
- Task Type: `GOVERNANCE / DOCUMENTATION`
- Initial Status: `APPROVED_TO_START`
- Final Status: `COMPLETED_PENDING_HUMAN_ACCEPTANCE`
- Objective: 让新 Thread、模型或机器仅凭 Git 仓库准确恢复研究事实、决策、证据、blocker 和下一门。
- Why: 聊天上下文、Codex memory 和人工记忆不能成为唯一事实源。
- Previous Gate: `S6.1-LR1 external alignment candidate 1294632`
- Actions: 冻结 L0–L9 authority；建立 append-only ledger、dual-machine sync、learning system；增强 route/blocker/tests。
- Files Changed: governance、Paper 1 route、learning 和 architecture governance tests；不含业务源码/历史资产。
- Commands: Git preflight、pytest、Ruff、MyPy、link/secret/path/protected/runtime-ignore checks。
- Validation: context recovery 红灯 `9 failed` 后绿灯 `9 passed`；architecture `90 passed`；no-label-leakage `8 passed`；Ruff、MyPy、staged diff、Markdown links、secret/absolute-path、UTF-8/LF、runtime-ignore 与 protected historical diff 检查通过。Chroma metadata isolation 在当前 Python 环境因可选 `chromadb` 未安装而未形成绿色证据；历史 manifest 仍保留 `BLK-HIST-001` 所记录的 110 个 CRLF/LF 差异，且受保护历史路径差异为零。
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Run ID: `N/A`
- Dataset Snapshot: `N/A`
- Model / Revision: `N/A`
- Environment Identity: `LOCAL / CONTROL_PLANE`; no experiment environment。
- Result Summary: Git-native context recovery governance candidate completed；formal experiment unchanged。
- Claims Allowed: repository-native context recovery architecture and documentation governance exist。
- Claims Prohibited: 不得写成 formal experiment、security effectiveness、reproduction 或 production readiness。
- Blockers: 无 approved-governance-scope blocker；strict reproduction blockers 保持 OPEN。
- Blocker ID: `N/A for this governance scope; BLK-S6.1-LR1-001 remains external`
- Resolution: `N/A`
- Owner Decisions: `PODR-036` and related confirmed decisions。
- Design Changes: 不推翻 `1294632`；只增加 canonical authority、ledger、learning 和 route persistence。
- Next Step: 提交、推送并等待人工审核。
- Next Approval Gate: `ACCEPT_OR_REJECT_S6.1_LR1_PLUS_CONTEXT_RECOVERY_GOVERNANCE`
- Auto Continue: `NO`

## REL-2026-0007 — LR1 / Context Governance Acceptance and R0 Gate Definition

- Record ID: `REL-2026-0007`
- Date: `2026-07-31`
- Timestamp: `2026-07-31T18:30:00+08:00`
- Machine: `LOCAL`
- Machine Role: `CONTROL_PLANE`
- Stage: `Stage 6.1`
- Task ID: `GOV-S6.1-LR1-FINAL-ACCEPTANCE`
- Task Name: `Accept research alignment, recover baseline tag and define reproduction preflight`
- Task Type: `GOVERNANCE / BASELINE_TAG_RECOVERY / NEXT_GATE_DEFINITION`
- Initial Status: `LR1_AND_CONTEXT_GOVERNANCE_PENDING_HUMAN_ACCEPTANCE`
- Final Status: `HUMAN_ACCEPTED / BASELINE_TAG_RECOVERED / S6.1-R0_DEFINED_NOT_STARTED`
- Objective: 固化人工验收、恢复缺失 baseline tag、拆分外部 artifact 许可语义并定义 R0 下一门。
- Why: 消除 pending 状态、补齐 baseline Git 身份、避免把再分发许可与内部研究/严格比较资格混为一谈，并在 P1
  冻结前先验证外部 baseline 可行性。
- Previous Gate: `ACCEPT_OR_REJECT_S6.1_LR1_PLUS_CONTEXT_RECOVERY_GOVERNANCE`
- Actions: 接受 LR1/Context/Paper-First/current route；批准 annotated tag 恢复；冻结六字段 artifact governance；
  supersede `LR1 -> P1 -> environment` 为 `LR1 -> R0 -> P1`；只定义 R0，不执行。
- Files Changed: governance、Paper 1 route/matrix/protocol/registry、R0 definition、learning 与 architecture governance test。
- Commands: Git/tag preflight、documentation tests and static checks only；无 external baseline/model/data/5090 command。
- Validation: governance TDD 红灯 `6 failed / 5 passed` 后专项 `11 passed`；architecture `92 passed`；namespace +
  label isolation `10 passed`；Ruff、scoped MyPy、Markdown links、secret/absolute-path、UTF-8/LF、runtime-ignore、
  protected historical/S6-T5 diff 与 `git diff --check` 通过；annotated tag 本地/远端 target 均为 `18cf2741...`。
  `BLK-HIST-001` 的历史 manifest 测试仍报告既有 110 个 CRLF/LF 差异且本轮 protected diff 为零；两项历史 report
  integrity 测试因当前 Control Plane 缺少可选 `openai` 包而在 collection 阶段未运行，本任务按禁令未安装环境。
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Run ID: `N/A`
- Dataset Snapshot: `N/A`
- Model / Revision: `N/A`
- Environment Identity: `LOCAL / CONTROL_PLANE`; RTX5090 not contacted。
- Result Summary: LR1、Context Recovery Governance、Paper-First Principle 与 current route 已人工接受；R0 仅定义。
- Claims Allowed: 接受状态、external baseline roles、tag recovery（仅在 Git 验证成功后）和 R0 definition。
- Claims Prohibited: external reproduction、5090 readiness/performance、dataset、Detector、training、Paper Result、SOTA、
  statistics、security effectiveness 或 Formal Experiment started。
- Blockers: `BLK-S6.1-LR1-001` 只继续阻断 future strict comparison；redistribution eligibility 独立待核验。
- Blocker ID: `BLK-S6.1-LR1-001`
- Resolution: governance acceptance complete；annotated tag created and pushed, with local/remote peeled target verified as
  `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`；R0 execution not approved。
- Owner Decisions: `PODR-041; PODR-042; PODR-043; PODR-044; PODR-045`
- Design Changes: owner superseded the temporary sequence with R0-before-P1；historical records retained。
- Next Step: commit/push governance; verify branch/upstream/tag/worktree; then stop。
- Next Approval Gate: `S6.1-R0_EXECUTION_APPROVAL`
- Auto Continue: `NO`

## REL-2026-0008 — RTX5090 Compute Worker Bootstrap Validation

- Record ID: `REL-2026-0008`
- Date: `2026-07-31`
- Timestamp: `NOT_RECORDED`
- Machine: `RTX5090`
- Machine Role: `COMPUTE_WORKER`
- Stage: `Stage 6.1 / R0`
- Task ID: `S6.1-R0-B0`
- Task Name: `RTX5090 Compute Worker Bootstrap Validation`
- Task Type: `ENGINEERING_ENVIRONMENT_VALIDATION`
- Initial Status: `WORKER_BOOTSTRAP_VALIDATION_REPORTED`
- Final Status: `HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY`
- Objective: 验证 Worker 基础硬件、WSL GPU、PyTorch 基础计算、Git context sync 与 baseline tag recovery。
- Why: R0 external baseline preflight 需要受控、可恢复且能够执行 GPU 基础计算的独立 Compute Worker。
- Previous Gate: `S6.1-R0_DEFINED_NOT_STARTED`
- Actions: Worker 完成 WSL/nvidia-smi、PyTorch FP16/BF16 tensor smoke、repo/branch/tag/clean-tree verification；Control
  Plane 仅登记项目负责人验收，不复跑 Worker 命令。
- Files Changed: Control Plane governance only；Worker bootstrap artifacts are not copied into LLMGuard Git。
- Commands: worker-reported environment/Git/GPU probes；exact raw command transcript `NOT_RECORDED` in this Control Plane record。
- Validation: FP16 `RTX5090_GPU_TEST_OK`；BF16 `BF16_TEST_OK`；Git HEAD/remote
  `347dc2bfff2256a7ad6c0c6ab8c468e9f3f833d9`；tag target `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`。
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `347dc2bfff2256a7ad6c0c6ab8c468e9f3f833d9`
- Run ID: `S6.1-R0-B0 / worker-reported; raw run ID NOT_RECORDED`
- Dataset Snapshot: `N/A`
- Model / Revision: `N/A`; PyTorch environment only。
- Environment Identity: Windows 11 Pro 25H2 Build 26200；Ubuntu 24.04 LTS；RTX 5090 31.84 GB；PyTorch
  2.13.0+cu130 / CUDA runtime 13.0；full package fingerprint deferred to R0-A。
- Result Summary: WSL GPU passthrough、basic FP16/BF16 tensor computation and Git collaboration path accepted。
- Claims Allowed: RTX5090 WSL GPU works；PyTorch cu130 works；FP16/BF16 basic tensor computation works；Git context sync works。
- Claims Prohibited: baseline/Paper/training/retrieval/detector result、SOTA、formal experiment or paper-level performance。
- Blockers: none for Bootstrap acceptance；NumPy missing is non-blocking environment completeness observation。
- Blocker ID: `N/A`
- Resolution: R0-A may install/fingerprint NumPy resolved version without bulk dependency installation。
- Owner Decisions: `PODR-046`
- Design Changes: none；bootstrap validates the planned machine role without changing Paper 1 baseline roles。
- Next Step: project-owner decision on R0 execution。
- Next Approval Gate: `S6.1-R0_EXECUTION_APPROVAL`
- Auto Continue: `NO`

## REL-2026-0009 — S6.1-R0 Approved to Start on Compute Worker

- Record ID: `REL-2026-0009`
- Date: `2026-07-31`
- Timestamp: `NOT_RECORDED`
- Machine: `LOCAL`
- Machine Role: `CONTROL_PLANE`
- Stage: `Stage 6.1 / R0`
- Task ID: `S6.1-R0-APPROVAL`
- Task Name: `Approve Paper 1 Reproduction Environment and Baseline Feasibility Validation`
- Task Type: `GOVERNANCE / ENGINEERING_VALIDATION_APPROVAL`
- Initial Status: `DEFINED / NOT STARTED / PENDING OWNER EXECUTION APPROVAL`
- Final Status: `APPROVED_TO_START`
- Objective: 允许 RTX5090 按冻结顺序验证三个 external baseline 的环境与 minimal-smoke 可行性。
- Why: 在 S6.1-P1 protocol freeze 前取得真实 compatibility、resource、revision、sample/model 与 smoke evidence。
- Previous Gate: `HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY`
- Actions: 批准 R0-A 至 R0-I；冻结 repo/environment isolation、minimal data/model、API stop、resource measurement、
  result classification 和 route-review 边界；LOCAL 不执行 R0。
- Files Changed: Control Plane governance、R0 preflight、route、state、learning and architecture tests。
- Commands: governance/test/Git commands on LOCAL only；no external repo, dataset, model or GPU command。
- Validation: red phase `6 failed / 11 passed` before governance synchronization；targeted green `17 passed`；full
  architecture `93 passed`；namespace + label-isolation `10 passed`；Ruff and scoped MyPy passed；16 changed files
  include 14 Markdown governance/research files and 2 architecture tests；UTF-8 no-BOM/LF、relative links、secret/path scan、
  runtime-ignore、protected historical path diff and `git diff --check` all passed。
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Run ID: `N/A`
- Dataset Snapshot: `N/A`
- Model / Revision: `N/A`
- Environment Identity: `LOCAL / CONTROL_PLANE`; R0 execution delegated to accepted RTX5090 worker。
- Result Summary: R0 approved to start；no R0 subtask executed by LOCAL；Formal Experiment unchanged。
- Claims Allowed: R0 execution is approved on the Worker under frozen scope/order。
- Claims Prohibited: baseline reproduced、Paper Result、S6.1-P1 started、Detector/training/SOTA/formal experiment。
- Blockers: `BLK-S6.1-LR1-001` remains open for strict comparison；R0 is intended to resolve/characterize its technical fields。
- Blocker ID: `BLK-S6.1-LR1-001`
- Resolution: Bootstrap accepted；R0 execution approval granted；strict-comparison blocker not resolved yet。
- Owner Decisions: `PODR-046; PODR-047`
- Design Changes: supersedes R0 pending-approval current snapshot；does not supersede route, roles or formal-experiment gate。
- Next Step: push Control Plane commit；RTX5090 pulls it and begins R0-A Environment Fingerprint。
- Next Approval Gate: `R0-I_CONTROL_PLANE_REVIEW`; S6.1-P1 remains not started。
- Auto Continue: `NO`

## REL-2026-0010 — S6.1-R0-I Control Plane Evidence Review

- Record ID: `REL-2026-0010`
- Date: `2026-07-31`
- Timestamp: `NOT_RECORDED`
- Machine: `LOCAL`
- Machine Role: `CONTROL_PLANE`
- Stage: `Stage 6.1 / R0`
- Task ID: `S6.1-R0-I`
- Task Name: `Control Plane Review of Paper 1 Reproduction Preflight Evidence`
- Task Type: `CONTROL_PLANE_EVIDENCE_REVIEW`
- Initial Status: `R0_PARTIAL_WITH_BLOCKERS_PENDING_CONTROL_PLANE_REVIEW`
- Final Status: `RETURNED_FOR_WORKER_CORRECTION`
- Objective: 验证 Worker archive/inner hashes、审查三项 baseline feasibility facts、规范化 blocker，并决定是否接受 R0。
- Why: R0 目标是识别可运行路径与真实 blocker，而不是强制三个 baseline 全部跑通；acceptance 仍要求 summary 与
  raw/official evidence 一致。
- Previous Gate: `S6.1-R0 APPROVED_TO_START`
- Actions: 验证 private archive SHA、safe layout、18-object index 和 component sidecars；审阅 fingerprint/audits/smoke/
  resource/scripts；只读核验三个 official exact commits；未运行 external workload。
- Files Changed: redacted R0-I review、governance/context/route/matrix/registry/learning and architecture tests；raw archive not in Git。
- Commands: Git preflight；PowerShell SHA-256/tar/index verification；official GitHub commit/tree/file read-only inspection；
  governance/test/static checks。No clone/install/data/model/API/baseline execution。
- Validation: red phase `10 failed / 10 passed` before R0-I governance synchronization；targeted green `20 passed`；full
  architecture `96 passed`；namespace + label-isolation `10 passed`；Ruff and scoped MyPy passed；20 changed files contain
  18 Markdown governance/research files and 2 architecture tests；UTF-8 no-BOM/LF、relative links、secret/path scan、raw archive
  exclusion、runtime-ignore、protected historical path diff and `git diff --check` all passed。
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Run ID: `N/A / CONTROL_PLANE_REVIEW`
- Dataset Snapshot: SafeRAG repository artifact at `e8f579743b23e0a3937076dcc0792fe29027cba3`；dataset-only counts SN 100 / ICC 93；
  full dataset identity/license not frozen。
- Model / Revision: `N/A`; no model executed or downloaded by LOCAL。
- Environment Identity: Worker R0-A Ubuntu 24.04.4、Python 3.11.15、NumPy 2.4.6、PyTorch 2.13.0+cu130/CUDA 13.0；
  LOCAL review environment is not baseline execution environment。
- Result Summary: archive SHA `0ce85a2bfe24e0456f9d29edc40659786d4273fcfc634df8749aee6d0e3aa9cc` and index
  `18/18` verified；GMTP sample-absence/Docker claims contradicted by exact upstream；SafeRAG script provenance/all-row coverage
  incomplete；R0 not accepted and returned for minimal correction。
- Claims Allowed: evidence integrity、R0-A fingerprint、three official commit identities、SafeRAG dataset-only artifact smoke、
  review mismatch/gaps、unchanged baseline roles。
- Claims Prohibited: R0 accepted、baseline reproduced、strict comparison ready、SafeRAG pipeline ready、Paper Result、Dataset
  frozen、Detector/training/SOTA/security effectiveness/formal experiment。
- Blockers: `R0-I-EVIDENCE-CORRECTION-001`；`BLK-S6.1-LR1-001` remains open；licenses remain redistribution-only issues。
- Blocker ID: `R0-I-EVIDENCE-CORRECTION-001; BLK-S6.1-LR1-001`
- Resolution: only corrected GMTP source facts and SafeRAG bound/all-row smoke evidence can close the R0-I correction blocker。
- Owner Decisions: `PODR-048; PODR-049`
- Design Changes: registered Control-Plane-First Token Economy Principle；did not change Paper-First or baseline roles。
- Next Step: RTX5090 returns the minimal corrected archive；LOCAL repeats R0-I。
- Next Approval Gate: owner decides R0 acceptance and `R0-FU1: RECOMMEND / NOT APPROVED`；S6.1-P1 remains not started。
- Auto Continue: `NO`

## REL-2026-0011 — S6.1-R0 Corrected-Evidence Final Acceptance

- Record ID: `REL-2026-0011`
- Date: `2026-07-31`
- Timestamp: `NOT_RECORDED`
- Machine: `LOCAL`
- Machine Role: `CONTROL_PLANE`
- Stage: `Stage 6.1 / R0`
- Task ID: `S6.1-R0-I-CORRECTED-REVIEW`
- Task Name: `Corrected Worker Evidence Final Control Plane Review`
- Task Type: `CONTROL_PLANE_EVIDENCE_REVIEW / ENGINEERING_VALIDATION_ACCEPTANCE`
- Initial Status: `RETURNED_FOR_WORKER_CORRECTION / REVIEW_PENDING_CORRECTED_WORKER_EVIDENCE`
- Final Status: `HUMAN_ACCEPTED_WITH_BLOCKERS`
- Objective: 验证 corrected archive/index/matrix 与三项 baseline 修正事实，并对 R0 作最终工程预检验收。
- Why: R0 的完成条件是可靠识别可行路径与真实 blocker，而不是声称 baseline 或论文结果已复现。
- Previous Gate: `S6.1-R0-I RETURNED_FOR_WORKER_CORRECTION`
- Actions: 验证外层 SHA 与 sidecar；安全检查 39 个 archive members；在 Git 外临时目录解包；逐项验证 corrected index
  `12/12` 与 matrix hash；审阅 command-derived evidence、executed script 和 correction scripts；未运行 external workload。
- Files Changed: additive R0 acceptance、owner decision、execution/master records、current/master context、route/matrix/
  registry/preflight/review and semantic governance tests；raw archive and full Worker logs not in Git。
- Commands: Git preflight；PowerShell/tar SHA、safe-member、inner-index checks；read-only evidence review；LOCAL governance/
  architecture/namespace/label/Markdown/secret/path/protected-history/static checks。No baseline、data/model、API or GPU workload。
- Validation: targeted governance/context recovery `21 passed`；full architecture `97 passed`；namespace + label isolation
  `10 passed`；Ruff passed；Markdown relative links `183` checked；secret/private-path、raw archive exclusion、UTF-8 no-BOM/LF、
  protected history/business paths and `git diff --check` passed。
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Run ID: `N/A / CONTROL_PLANE_REVIEW`
- Dataset Snapshot: no dataset frozen；SafeRAG repository artifact at
  `e8f579743b23e0a3937076dcc0792fe29027cba3` has SN 100/100 and ICC 93/93 required-key validation only。
- Model / Revision: `N/A`; no model executed or downloaded by LOCAL。
- Environment Identity: Worker R0-A identity remains historical engineering evidence；LOCAL performed only evidence review。
- Result Summary: corrected archive
  `904d79c59e35c6aeb157540049b0f44262b86e5c1c5b3e8d4e96ee2fad3f1c6b`、index `12/12` and matrix
  `fd7617eca689fa46fc6908f94aa4fa158aaae4d277bb17943bbcc1baf74db9bc` verified；GMTP、SafeRAG and PoisonedRAG
  corrections passed；R0 accepted with normalized downstream blockers。
- Claims Allowed: `S6.1-R0 = HUMAN_ACCEPTED_WITH_BLOCKERS` as reproduction preflight；three final engineering-feasibility
  qualifications；SafeRAG benchmark artifacts available for SN/ICC under later protocol。
- Claims Prohibited: baseline/pipeline/benchmark result reproduced；strict comparison ready；Paper Result；Dataset frozen；
  Detector/training/Our Method/SOTA/security effectiveness/formal experiment。
- Blockers: P1 protocol and formal-experiment environment items remain；license uncertainty is redistribution-only；SafeRAG full
  pipeline is non-blocking if only benchmark artifacts are selected。
- Blocker ID: `R0-I-EVIDENCE-CORRECTION-001 RESOLVED; BLK-S6.1-LR1-001 RECLASSIFIED_DOWNSTREAM`
- Resolution: corrected command-derived evidence closed the R0-I correction blocker without running new LOCAL workload。
- Owner Decisions: `PODR-048; PODR-049; PODR-050`
- Design Changes: none；baseline roles and Paper-First route remain unchanged。
- Next Step: project owner decides whether to approve narrow `S6.1-R0-FU1`。
- Next Approval Gate: `S6.1-R0-FU1 APPROVAL_RECOMMENDED / NOT APPROVED`
- Auto Continue: `NO`

## REL-2026-0012 — S6.1-R0-FU1-P0 Targeted Resolution Contract Freeze

- Record ID: `REL-2026-0012`
- Date: `2026-07-31`
- Timestamp: `NOT_RECORDED`
- Machine: `LOCAL`
- Machine Role: `CONTROL_PLANE`
- Stage: `Stage 6.1 / R0-FU1`
- Task ID: `S6.1-R0-FU1-P0`
- Task Name: `LOCAL Control-Plane Planning and Execution Contract Freeze`
- Task Type: `CONTROL_PLANE_SOURCE_ANALYSIS / CONTRACT_CANDIDATE`
- Initial Status: `APPROVED_TO_START`
- Final Status: `COMPLETED_PENDING_OWNER_REVIEW`
- Objective: resolve dataset/attack/source/call-path planning blockers and freeze exact future W1/W2 candidates without Worker
  execution or external workload。
- Why: minimize Worker research/token use while preserving source identity, reproducibility and approval boundaries。
- Previous Gate: `S6.1-R0 = HUMAN_ACCEPTED_WITH_BLOCKERS; R0-FU1 APPROVAL_RECOMMENDED`
- Actions: compared NQ/HotpotQA/MS MARCO from primary sources；audited PoisonedRAG attack/result identities and API boundary；
  recovered GMTP's official BEIR commit；traced detector-only code/dependencies；froze model revisions, sample identities,
  resource ceilings, SafeRAG SN/ICC artifacts and cross-baseline comparability classes。
- Files Changed: new FU1 resolution；current/owner/execution/master context；experiment master record；Paper 1 route/matrix/
  registry/README；semantic governance tests。No business source or historical evidence changed。
- Commands: Git mandatory startup；read-only official GitHub/Hugging Face metadata/source queries；local document/test checks。
- Validation: targeted context recovery `16 passed`；full architecture `98 passed`；namespace + label isolation `10 passed`；
  Ruff passed；Markdown relative links `222` checked；14 changed files passed secret/private-path and UTF-8 no-BOM/LF checks；
  protected history/business paths `0`；`git diff --check` passed。Pytest cache write warning is non-blocking。
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Run ID: `N/A / CONTROL_PLANE_SOURCE_ANALYSIS`
- Dataset Snapshot: `Dataset = NOT FROZEN`；NQ primary candidate and HotpotQA fallback only；no data downloaded。
- Model / Revision: W2 candidates Contriever `abe8c149...` and BERT `86b5e093...`；not downloaded or executed。
- Environment Identity: `LOCAL / CONTROL_PLANE` source analysis only；Worker environment remains historical R0 evidence。
- Result Summary: PoisonedRAG author-released attack artifact `PARTIAL`；GMTP BEIR source `VERIFIED` and detector-only path
  frozen；SafeRAG artifact contract frozen；W1/W2 exact candidates prepared。
- Claims Allowed: P0 contract candidate completed pending owner review；source identities/dependency separation and artifact
  planning decisions recorded。
- Claims Prohibited: W1/W2 ran；baseline reproduced；strict comparison ready；P1/Dataset/Detector/training/formal result started。
- Blockers: `BLK-S6.1-FU1-W1-001`; `BLK-S6.1-FU1-W2-001`; formal corpus/index and redistribution items remain downstream。
- Blocker ID: `BLK-S6.1-P1-001 RESOLVED; BLK-S6.1-P1-002 RESOLVED; BLK-S6.1-FU1-W1-001 OPEN; BLK-S6.1-FU1-W2-001 OPEN`
- Resolution: source/planning scope frozen locally；runtime compatibility/evidence requires separate owner-approved W1/W2。
- Owner Decisions: `PODR-048; PODR-050; PODR-051`
- Design Changes: none to Paper 1 method/roles；only external baseline candidate identities and execution contracts frozen。
- Next Step: project owner reviews P0 and separately decides W1/W2 approvals。
- Next Approval Gate: `FU1-W1 / FU1-W2 OWNER DECISION`; S6.1-P1 remains not started。
- Auto Continue: `NO`

## REL-2026-0013 — FU1-P0/L1 Human Acceptance and W2 Contract Freeze

- Record ID: `REL-2026-0013`
- Date: `2026-07-31`
- Timestamp: `NOT_RECORDED`
- Machine: `LOCAL`
- Machine Role: `CONTROL_PLANE`
- Stage: `Stage 6.1 / R0-FU1`
- Task ID: `S6.1-R0-FU1-L1`
- Task Name: `PoisonedRAG Released Artifact Identity and Deterministic Assembly Validation`
- Task Type: `SOURCE_ARTIFACT_VALIDATION / DETERMINISTIC_TRANSFORMATION_VALIDATION`
- Initial Status: `P0 COMPLETED_PENDING_OWNER_REVIEW / W1 NOT APPROVED`
- Final Status: `P0 HUMAN_ACCEPTED / L1 HUMAN_ACCEPTED / W1 SUPERSEDED_BY_LOCAL_L1 / W2 READY_FOR_OWNER_EXECUTION_APPROVAL`
- Objective: accept the P0 planning contract, validate the exact released PoisonedRAG NQ artifact and official deterministic
  LM-targeted assembly locally, and harden—but not execute—the GMTP W2 contract.
- Why: source/artifact identity can be closed on the Control Plane without consuming Worker compute, while GMTP runtime
  compatibility still requires a separately approved Worker smoke.
- Previous Gate: `S6.1-R0-FU1-P0 COMPLETED_PENDING_OWNER_REVIEW; FU1-W1/FU1-W2 NOT APPROVED`
- Actions: read exact official GitHub blobs in memory；validated all 100 NQ records and 500 attack-text entries；derived five
  ordered assembled-document hashes and aggregate hash for fixed target `test1`；bound W2 source/input/model/config identities,
  isolated environment, output schema and resource ceiling. No external artifact was saved in Git.
- Files Changed: FU1 resolution；owner/current/execution/experiment/master context；Paper 1 README/matrix/registry and semantic
  governance tests. No business source, fixture/data, historical evidence or Worker archive changed.
- Commands: mandatory Git startup；read-only official GitHub/Hugging Face metadata/content queries；in-memory JSON/hash/schema
  validation；LOCAL documentation and test checks. No model, retrieval, API, NQ corpus, GMTP, SafeRAG or RTX5090 execution.
- Validation: targeted context recovery `16 passed`；full architecture `98 passed`；namespace + label isolation `10 passed`；
  Ruff passed；Markdown relative links `208` checked；10 changed files passed secret/private-path and UTF-8 no-BOM/LF checks；
  protected history/business paths `0`；runtime ignore and `git diff --check` passed。Pytest cache write warning is non-blocking.
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Run ID: `N/A / LOCAL_ARTIFACT_VALIDATION`
- Dataset Snapshot: PoisonedRAG released `results/adv_targeted_results/nq.json` at commit
  `f660d72174f06b13fae5163ce656e7b235db858f`；blob `d1da818b28da7013864ea465ff88ad4c3ca29562`；file SHA-256
  `44df711454a9bada08e72e9e4a003a2cc845c43707ac93a3493e5168ec415cf2`；100 targets x 5 texts. Dataset remains not frozen.
- Model / Revision: no model downloaded or executed. W2 contract only: `facebook/contriever-msmarco@abe8c149...` and canonical
  `google-bert/bert-base-uncased@86b5e093...`.
- Environment Identity: L1 used `LOCAL / CONTROL_PLANE` and in-memory transformation only. Future W2 is isolated as
  `gmtp-compat` with Python 3.11, Torch 2.13.0+cu130, CUDA runtime 13.0, Transformers 4.47.1 and NumPy 1.26.4.
- Result Summary: released artifact identity/schema and exact `question + "." + adv_text` assembly passed；fixed target aggregate
  SHA-256 `f22b7576c27926a07a7138e952cf3ee6b86c982b584a3078f3364577d32c60a7`；API-free released-text reuse is feasible.
- Claims Allowed: P0/L1 accepted；released attack artifact identity and deterministic assembly verified；W2 contract ready for
  owner approval.
- Claims Prohibited: attack generation reproduced；exact paper generation identity established；W2/baseline executed；strict
  comparison ready；P1/Dataset/Detector/training/formal experiment started.
- Blockers: only `BLK-S6.1-FU1-W2-001` remains in FU1 runtime scope；formal corpus/index, historical API/paper-run identity and
  redistribution items remain downstream.
- Blocker ID: `BLK-S6.1-FU1-W1-001 RESOLVED_BY_LOCAL_L1 / SUPERSEDED; BLK-S6.1-FU1-W2-001 OPEN`
- Resolution: source artifact/schema/assembly identity was resolved locally without Worker or API execution；W2 was hardened but
  deliberately not run.
- Owner Decisions: `PODR-048; PODR-050; PODR-051; PODR-052`
- Design Changes: no Paper 1 method/baseline role change；only identity evidence and execution governance advanced.
- Next Step: project owner decides whether to approve the frozen W2 Worker contract.
- Next Approval Gate: `FU1-W2 OWNER EXECUTION DECISION`; S6.1-P1 remains not started.
- Auto Continue: `NO`

## REL-2026-0014 — FU1-W2 GMTP Detection-Core Smoke Execution Approval

- Record ID: `REL-2026-0014`
- Date: `2026-08-01`
- Timestamp: `NOT_RECORDED`
- Machine: `LOCAL`
- Machine Role: `CONTROL_PLANE`
- Stage: `Stage 6.1 / R0-FU1`
- Task ID: `S6.1-R0-FU1-W2-APPROVAL`
- Task Name: `GMTP Detection-Only Minimal Smoke Execution Approval Registration`
- Task Type: `GOVERNANCE_EXECUTION_APPROVAL_RECORD`
- Initial Status: `READY_FOR_OWNER_EXECUTION_APPROVAL / NOT_YET_EXECUTED`
- Final Status: `APPROVED_TO_START / NOT_YET_EXECUTED`
- Objective: register owner approval for RTX5090 to execute only the exact frozen W2 detector-core compatibility smoke.
- Why: P0/L1 resolved planning and attack-artifact identity；W2 runtime compatibility remains the only FU1 execution evidence gap.
- Previous Gate: `P0 HUMAN_ACCEPTED / L1 HUMAN_ACCEPTED / W1 SUPERSEDED / W2 READY_FOR_OWNER_EXECUTION_APPROVAL`
- Actions: added PODR-053；promoted only W2's approval status；reaffirmed source/input/model/parameter/environment/output/resource
  identities, evidence directory and stop codes. LOCAL did not contact or execute the Worker.
- Files Changed: owner/current/execution/experiment/master context and canonical FU1 contract plus semantic governance tests.
  No business source, fixture/data, historical evidence, Worker evidence or external repository changed.
- Commands: mandatory Git fetch/status/branch/HEAD/log/pull preflight；LOCAL documentation and governance validation only.
- Validation: targeted context recovery `16 passed`；full architecture `98 passed`；namespace + label isolation `10 passed`；
  Ruff passed；Markdown relative links `208` checked；9 changed files passed secret/private-path and UTF-8 no-BOM/LF checks；
  protected history/business paths `0`；runtime ignore and `git diff --check` passed。Pytest cache write warning is non-blocking.
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Run ID: `N/A / GOVERNANCE_APPROVAL_ONLY`
- Dataset Snapshot: no dataset frozen or downloaded；W2 remains bound to the accepted GMTP-packaged NQ record/hashes.
- Model / Revision: frozen Contriever `abe8c149...` and canonical BERT `86b5e093...`；not downloaded or loaded by LOCAL.
- Environment Identity: future Worker-only `gmtp-compat`; no LOCAL environment creation or mutation.
- Result Summary: `S6.1-R0-FU1-W2 = APPROVED_TO_START` on `RTX5090 / COMPUTE_WORKER`; execution evidence does not yet exist.
- Claims Allowed: exact W2 engineering smoke is approved to start under its frozen contract.
- Claims Prohibited: W2 executed/passed/accepted；GMTP reproduced；formal comparison/metrics/Paper Result/security effectiveness；
  S6.1-P1 or Formal Experiment started.
- Blockers: `BLK-S6.1-FU1-W2-001` remains open until later accepted Worker evidence；formal environment and redistribution items
  remain downstream.
- Blocker ID: `BLK-S6.1-FU1-W2-001 OPEN / EXECUTION_APPROVED`
- Resolution: approval gate opened without converting an approval record into execution evidence.
- Owner Decisions: `PODR-052; PODR-053`
- Design Changes: none；the already frozen W2 contract and baseline/artifact distinctions remain authoritative.
- Next Step: RTX5090 executes the exact W2 contract and stores evidence under `~/experiments/s6_1_r0_fu1/w2/`.
- Next Approval Gate: later Control Plane evidence review；`S6.1-P1 = NOT STARTED`.
- Auto Continue: `NO`

## REL-2026-0015 — W2 Attempt 1 Evidence Review Blocker and H1 Recovery Gate

- Record ID: `REL-2026-0015`
- Date: `2026-08-01`
- Timestamp: `NOT_RECORDED`
- Machine: `LOCAL`
- Machine Role: `CONTROL_PLANE`
- Stage: `Stage 6.1 / R0-FU1`
- Task ID: `S6.1-R0-FU1-W2-ATTEMPT1-REVIEW`
- Task Name: `GMTP Detection-Only Minimal Smoke Attempt 1 Control Plane Evidence Review`
- Task Type: `CONTROL_PLANE_EVIDENCE_REVIEW / FAIL_CLOSED_RECOVERY_GATE`
- Initial Status: `W2 APPROVED_TO_START / Worker summary MODEL_DOWNLOAD_BLOCKER`
- Final Status: `W2_ATTEMPT1_EVIDENCE_BLOCKER / H1 BLOCKED_NOT_STARTED`
- Objective: validate the submitted Worker archive before accepting Attempt 1 or preparing an offline model bundle.
- Why: Worker summary facts must be carried by indexed archive evidence；chat summary and unexecuted script lines are not proof.
- Previous Gate: `S6.1-R0-FU1-W2 APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED`
- Actions: recomputed outer SHA；validated archive member paths/types；extracted to a controlled temporary review directory；
  verified all indexed payload hashes and harness hash；reviewed redacted source/input/environment/model/result/resource evidence；
  scanned for secret shapes and raw input artifacts. No model/GMTP/GPU workload or Worker contact occurred.
- Files Changed: additive redacted Attempt 1 review；owner/current/execution/experiment/master/FU1 governance and semantic tests.
  Raw archive, model files, local caches and complete Worker logs remain outside Git.
- Commands: mandatory Git preflight；PowerShell SHA/tar/index/safe-path checks；read-only evidence review；LOCAL governance/static
  checks only.
- Validation: outer archive SHA matched sidecar；safe members `18/18`；evidence index `16/16`；harness hash passed；targeted
  context recovery `17 passed`；full architecture `99 passed`；namespace + label isolation `10 passed`；Ruff passed；Markdown
  relative links `230` checked；11 changed files passed secret/private-path and UTF-8 no-BOM/LF checks；raw-artifact/protected-
  history changes `0`；runtime ignore and `git diff --check` passed。Pytest cache write warning is non-blocking.
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Run ID: `N/A / CONTROL_PLANE_EVIDENCE_REVIEW`
- Dataset Snapshot: no dataset frozen/downloaded；only accepted hashes/lengths for fixed GMTP-packaged NQ record were reviewed.
- Model / Revision: Contriever exact revision reported download-blocked；BERT exact revision not attempted；no LOCAL download/load.
- Environment Identity: Worker Python/Torch/CUDA/Transformers/NumPy/GPU evidence matches frozen values；archive does not evidence
  main-repository integrity or environment disk size.
- Result Summary: archive SHA `6acdbb8038e57b1d3e88028350fc08046d73a826ba9dd167452bfc0dd834170f`；safe members
  `18/18`；index `16/16`；harness SHA `8411af2042774f1a18eec95e97a14ade088acbc35f09942ae9ffea4e8ea5fc06`；
  main HEAD/clean and disk measurement absent；Attempt 1 cannot be accepted as a valid blocked run.
- Claims Allowed: named archive/partial evidence fields passed；owner approved future 10 GiB resource correction and exact H1
  recovery contract.
- Claims Prohibited: `VALID_BLOCKED_ENGINEERING_RUN`；`REUSABLE_W2_PREFLIGHT_EVIDENCE`；W2 completed/accepted；algorithm failed；
  GMTP incompatible；offline bundle created；P1/formal experiment started.
- Blockers: corrected indexed evidence must capture main HEAD, delimited clean status and explicit `gmtp-compat` byte count.
- Blocker ID: `W2_ATTEMPT1_EVIDENCE_BLOCKER`
- Resolution: STOP before H1 download/bundle；request evidence-only correction without GMTP rerun or environment rebuild.
- Owner Decisions: `PODR-053; PODR-054`
- Design Changes: future W2 disk ceiling corrected to 10 GiB only；algorithm/data/parameters/models unchanged.
- Next Step: review corrected Attempt 1 archive；H1 remains approved but blocked/not started.
- Next Approval Gate: close `W2_ATTEMPT1_EVIDENCE_BLOCKER`; `S6.1-P1 = NOT STARTED`.
- Auto Continue: `NO`

## REL-2026-0016 — W2 Attempt 1 Correction 01 Review Remains Evidence-Blocked

- Record ID: `REL-2026-0016`
- Date: `2026-08-01`
- Timestamp: `NOT_RECORDED`
- Machine: `LOCAL`
- Machine Role: `CONTROL_PLANE`
- Stage: `Stage 6.1 / R0-FU1`
- Task ID: `S6.1-R0-FU1-W2-ATTEMPT1-CORRECTION-01-REVIEW`
- Task Name: `Minimal Corrected Indexed Evidence Review with Conditional H1 Gate`
- Task Type: `CONTROL_PLANE_EVIDENCE_REVIEW / FAIL_CLOSED_RECOVERY_GATE`
- Initial Status: `W2_ATTEMPT1_EVIDENCE_BLOCKER / H1 BLOCKED_NOT_STARTED`
- Final Status: `W2_ATTEMPT1_EVIDENCE_BLOCKER / CORRECTION_DU_COMMAND_EVIDENCE_MISSING / H1 BLOCKED_NOT_STARTED`
- Objective: determine whether Correction 01 closes the Attempt 1 evidence gate and, only if it does, start approved H1.
- Why: the resource gate requires command-derived distinction between apparent and allocated environment bytes.
- Previous Gate: `PODR-054 / W2_ATTEMPT1_EVIDENCE_BLOCKER`
- Actions: completed Git preflight；verified outer sidecar/recomputed/reported SHA；validated safe archive metadata；extracted to a
  Git-external temporary directory；verified correction index and all four payloads；cross-checked original binding, main repository,
  disk text and manifest；deleted the temporary extraction. H1 was not started.
- Files Changed: additive governance and context records only. Raw correction/original archives, model artifacts, caches and logs
  remain outside Git.
- Commands: Git preflight；PowerShell SHA/index/content checks；Python read-only tar metadata inspection；LOCAL governance/static
  tests only.
- Validation: correction SHA `d911063e3a00daba3f8dcfea6f3e6e3b484e79f4f0fe8853a53ff9d8c415279e` matched three ways；
  safe members `6/6`；index `4/4`；original binding and main-repository integrity passed；manifest/disk values matched；apparent
  `5399301224` and allocated `5492817920` are below `6442450944`；no concrete `du` command/flags/raw output was present；targeted
  context recovery `17 passed`；full architecture `99 passed`；namespace + label isolation `10 passed`；Ruff and `git diff --check`
  passed；Markdown relative links `225` checked；10 changed files passed added-secret/private-path and UTF-8 no-BOM/LF checks；
  raw-artifact/protected-history changes `0`；runtime artifact ignore rule verified. Pytest cache write warning is non-blocking.
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Run ID: `N/A / CONTROL_PLANE_EVIDENCE_REVIEW`
- Dataset Snapshot: unchanged；no dataset downloaded or frozen.
- Model / Revision: frozen Contriever/BERT identities unchanged；no download or load occurred.
- Environment Identity: Correction 01 supports Attempt 1 main-repository integrity and reports internally consistent
  `gmtp-compat` counts, but command-derived measurement semantics remain unverified.
- Result Summary: Correction 01 is integrity-valid but evidence-incomplete；the original blocker remains open and H1 remains
  blocked/not started.
- Claims Allowed: correction archive/index integrity, original binding, main-repository integrity, reported byte values and their
  arithmetic against the 6 GiB ceiling.
- Claims Prohibited: `ENV_DISK_CONTRACT = ACCEPTED`；`VALID_BLOCKED_ENGINEERING_RUN`；reusable preflight；model download/bundle；
  W2 completed/accepted；GMTP compatibility；P1/formal experiment.
- Blockers: exact apparent-size and allocated-size `du` commands, flags and captured raw outputs are absent.
- Blocker ID: `W2_ATTEMPT1_EVIDENCE_BLOCKER`
- Resolution: retain blocker；request minimal additive command-derived indexed evidence；do not start H1.
- Owner Decisions: `PODR-053; PODR-054; PODR-055`
- Design Changes: none；10 GiB task ceiling and 6 GiB environment sub-budget remain unchanged.
- Next Step: review command-derived measurement correction only.
- Next Approval Gate: close `W2_ATTEMPT1_EVIDENCE_BLOCKER`; H1 remains pre-approved but gated；`S6.1-P1 = NOT STARTED`.
- Auto Continue: `NO`

## REL-2026-0017 — PO-MHEP Highest Internal Execution Authority and Correction 02 Candidate

- Record ID: `REL-2026-0017`
- Date: `2026-08-01`
- Timestamp: `NOT_RECORDED`
- Machine: `LOCAL`
- Machine Role: `PRIMARY_CONTROL_PLANE / PROJECT_EXECUTION_LEAD / RESEARCH_GOVERNANCE_LEAD`
- Stage: `Project-wide / Stage 1–7 and future stages`
- Task ID: `GOV-PO-MHEP`
- Task Name: `Project Owner Sovereignty, Mandatory Human Escalation, and Physical Context Preservation Principle`
- Task Type: `PROJECT_WIDE_GOVERNANCE_AUTHORITY_FREEZE / CONTEXT_PERSISTENCE`
- Initial Status: `OWNER_DECISION_RECEIVED / GOVERNANCE_NOT_YET_PERSISTED`
- Final Status: `HUMAN_ACCEPTED / HIGHEST_INTERNAL_PROJECT_EXECUTION_AUTHORITY / PERMANENT`
- Objective: establish a permanent project-wide execution authority, mandatory escalation contract, proactive risk review and
  physical context recovery/persistence system.
- Why: project correctness cannot depend on agent defaults, Worker autonomy, progress pressure, chat memory or post-hoc governance.
- Previous Gate: `PODR-055 / W2_ATTEMPT1_EVIDENCE_BLOCKER / H1 BLOCKED_NOT_STARTED`
- Actions: created one canonical PO-MHEP document；inserted L0.5 authority；updated AGENTS startup/escalation/completion rules；
  synchronized long-term requirements, owner/current/master/experiment governance and Stage 6.1 canonical entries；prepared the
  documentation-only Correction 02 Worker Contract Candidate. No Worker contact or execution occurred.
- Files Changed: governance/context/research documentation and context-recovery tests only；no business code, dataset, model,
  environment, raw evidence or protected history changed.
- Commands: mandatory Git/context preflight；read-only canonical context review；local documentation/static/test validation only.
- Validation: PO-MHEP/context targeted `19 passed`；full architecture `101 passed`；namespace + label isolation `10 passed`；
  Ruff passed；Markdown relative links `255` checked with `0` broken；13 changed files including the new canonical principle passed
  added-secret/private-path and UTF-8 no-BOM/LF checks；protected/raw-history changes `0`；runtime artifact ignore and
  `git diff --check` passed. Pytest cache write warning is non-blocking.
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Run ID: `N/A / GOVERNANCE_AUTHORITY_FREEZE`
- Dataset Snapshot: unchanged；no dataset access/download/freeze.
- Model / Revision: unchanged frozen W2 identities；no download/load.
- Environment Identity: no environment creation, installation, activation, mutation or measurement.
- Result Summary: PO-MHEP is permanent highest internal execution authority；Correction 02 is candidate-only；all W2/H1/P1/
  Formal Experiment execution facts remain unchanged.
- Claims Allowed: PO-MHEP governance status, authority/role/escalation/context contracts and existence of an unapproved Worker
  contract candidate.
- Claims Prohibited: Correction 02 approved/sent/executed；Worker contacted；W2 blocker closed；H1 started；model/GMTP/P1/formal
  execution；any new engineering/security/paper result.
- Blockers: `W2_ATTEMPT1_EVIDENCE_BLOCKER` remains open；Correction 02 still requires explicit owner approval.
- Blocker ID: `W2_ATTEMPT1_EVIDENCE_BLOCKER / CORRECTION02_OWNER_APPROVAL_REQUIRED`
- Resolution: governance task completed without altering the execution blocker；candidate returned to owner for decision.
- Owner Decisions: `PODR-056`
- Design Changes: project-wide governance authority and mandatory review/persistence contracts only；no algorithm/data/model/
  parameter/metric change.
- Paper Impact: requires proactive novelty/fairness/confounder/statistical/license/claims review at specified paper gates；does not
  create paper evidence.
- Architecture Impact: requires forward extensibility/technical-debt/label-isolation/reproducibility review before stage/spec/
  Worker execution；does not change runtime architecture.
- Next Step: project owner approves, rejects or modifies the Correction 02 Worker Contract Candidate.
- Next Approval Gate: explicit Correction 02 owner decision；H1/P1/Formal Experiment remain closed by existing gates.
- Auto Continue: `NO`

## REL-2026-0018 — Correction 02 GNU du Provenance Final Evidence Correction Approval

- Record ID: `REL-2026-0018`
- Date: `2026-08-01`
- Timestamp: `NOT_RECORDED`
- Machine: `LOCAL`
- Machine Role: `PRIMARY_CONTROL_PLANE / 5090_APPROVAL_AUTHORITY / CONTEXT_PRESERVATION_OWNER`
- Stage: `Stage 6.1 / R0-FU1`
- Task ID: `S6.1-R0-FU1-W2-ATTEMPT1-CORRECTION-02`
- Task Name: `W2 Attempt 1 GNU du Provenance Final Evidence Correction`
- Task Type: `EVIDENCE_PACKAGING_CORRECTION_ONLY / GOVERNANCE_EXECUTION_APPROVAL_RECORD`
- Initial Status: `CONTRACT_CANDIDATE / NOT APPROVED / NOT SENT / NOT EXECUTED`
- Final Status: `APPROVED_TO_START / NOT SENT / NOT EXECUTED`
- Objective: approve a final evidence-only correction that captures exact GNU apparent/allocated disk-measurement provenance for
  the existing `gmtp-compat` environment without rerunning GMTP or changing the environment.
- Why: Correction 01 is integrity-valid but cannot prove that its apparent and allocated byte fields came from distinct correct
  GNU `du` semantics；a final materiality rule is needed to close substantive evidence gaps without infinite formatting churn.
- Previous Gate: `PODR-056 / CORRECTION02_OWNER_APPROVAL_REQUIRED / W2_ATTEMPT1_EVIDENCE_BLOCKER OPEN`
- Actions: registered `PODR-057`；promoted the existing candidate to an approved RTX5090 contract；froze `du -sb` versus
  `du -sB1`, tool/platform/Conda/time provenance, raw-stream/exit capture, counts, manifest/index/archive requirements,
  `DISK_MEASUREMENT_MATERIAL_MISMATCH`, Worker success wording and `MATERIALITY_AND_FINAL_CLOSURE_RULE`；completed
  `FORWARD_RISK_REVIEW = PASS_WITH_GUARDRAILS` and `PAPER_RISK_REVIEW = PASS_WITH_CLAIMS_BOUNDARY`. LOCAL did not contact or
  execute the Worker.
- Files Changed: owner/current/execution/experiment/master/PO-MHEP snapshot, Stage README/learning notes, canonical FU1 contract
  and semantic governance tests only. No business source, dataset, model, environment, Worker archive or protected history changed.
- Commands: mandatory Git fetch/status/branch/HEAD/log/pull preflight；LOCAL documentation and governance validation only.
- Validation: targeted context/governance `19 passed`；full architecture `101 passed`；namespace + label isolation `10 passed`；
  Ruff passed；Markdown relative links `234` checked with `0` broken；10 changed files passed added-secret/private-path and UTF-8
  no-BOM/LF checks；protected history/business paths and H1/model/Worker-archive changes `0`；runtime artifact ignore and
  `git diff --check` passed. Pytest cache write warning is non-blocking. The first full-test invocation omitted `src` from
  `PYTHONPATH` and referenced one stale test filename；the corrected repository invocation passed and no environment was modified.
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Run ID: `N/A / GOVERNANCE_APPROVAL_ONLY`
- Dataset Snapshot: unchanged；no dataset access/download/freeze.
- Model / Revision: unchanged frozen W2 identities；no download/load.
- Environment Identity: future Worker uses the existing registered `gmtp-compat`; LOCAL did not activate, inspect, install, mutate
  or measure that environment.
- Result Summary: Correction 02 is approved to start on RTX5090 but is not sent/executed；the evidence blocker is not closed.
- Claims Allowed: exact Correction 02 approval, contract, materiality rule and preserved Worker/Control Plane boundary.
- Claims Prohibited: Correction 02 sent/executed/accepted；Attempt 1 valid blocked/reusable evidence；W2 completed/accepted；H1
  started；GMTP compatible；model/CUDA workload；P1/formal experiment/security/paper result.
- Blockers: `W2_ATTEMPT1_EVIDENCE_BLOCKER` remains open until returned Correction 02 evidence passes separate LOCAL review.
- Blocker ID: `W2_ATTEMPT1_EVIDENCE_BLOCKER OPEN`
- Resolution: owner approval resolves `CORRECTION02_OWNER_APPROVAL_REQUIRED` only；it does not resolve the evidence blocker.
- Owner Decisions: `PODR-056; PODR-057`
- Design Changes: evidence provenance and final closure governance only；no algorithm/data/model/parameter/metric change.
- Paper Impact: none as result evidence；prevents resource-provenance ambiguity from contaminating later reproducibility claims.
- Architecture Impact: none to runtime；strengthens Worker/Control Plane and physical evidence boundaries.
- Next Step: RTX5090 pulls the exact approval commit and executes only the approved Correction 02 contract, then returns the
  indexed private archive for Control Plane review.
- Next Approval Gate: LOCAL raw-evidence review under `MATERIALITY_AND_FINAL_CLOSURE_RULE`; H1/P1/Formal Experiment remain closed.
- Auto Continue: `NO`

## REL-2026-0019 — Correction 02 Final Closure and H1 Offline Model Artifact Preparation

- Record ID: `REL-2026-0019`
- Date: `2026-08-01`
- Timestamp: `2026-08-01T08:58:14.214020Z`
- Machine: `LOCAL`
- Machine Role: `PRIMARY_CONTROL_PLANE / PROJECT_EXECUTION_LEAD / CONTEXT_PRESERVATION_OWNER`
- Stage: `Stage 6.1 / R0-FU1`
- Task ID: `S6.1-R0-FU1-W2-ATTEMPT1-CORRECTION-02; S6.1-R0-FU1-W2-H1`
- Task Name: `Correction 02 Control Plane Evidence Review and Offline Model Artifact Provisioning`
- Task Type: `RAW_EVIDENCE_REVIEW / FINAL_CLOSURE / OFFLINE_MODEL_ARTIFACT_PROVISIONING_ONLY`
- Initial Status: `CORRECTION02_EVIDENCE_READY_FOR_CONTROL_PLANE_REVIEW / H1 APPROVED_BLOCKED_NOT_STARTED`
- Final Status: `CORRECTION02_CONTROL_PLANE_REVIEW_PASS / W2_ATTEMPT1_EVIDENCE_BLOCKER_RESOLVED /
  OFFLINE_MODEL_ARTIFACTS_PREPARED_PENDING_5090_VERIFICATION`
- Objective: independently review the indexed Correction 02 archive, apply the frozen materiality rule, close the Attempt 1
  evidence gate if warranted, then prepare only the two exact public model snapshots for later Worker transfer.
- Why: the original W2 run stopped before smoke because the frozen encoder was unavailable；valid command-derived disk evidence
  was the remaining classification gate, and owner-approved H1 supplies transfer artifacts without changing algorithm semantics.
- Previous Gate: `PODR-057 / W2_ATTEMPT1_EVIDENCE_BLOCKER OPEN / H1 BLOCKED_NOT_STARTED`
- Actions: verified archive/sidecar/reported SHA, safe members, sorted `17/17` index, original/Correction01/approval/task binding,
  exact GNU `du` commands/tool/raw streams/exits/semantics, byte/count/spec/repository identities and no-mutation flags；applied
  `MATERIALITY_AND_FINAL_CLOSURE_RULE`；created isolated `w2-h1-download` environment by offline clone；used anonymous pinned
  `snapshot_download` with one worker；removed download cache and Core ML cross-framework artifacts；generated manifest, sorted
  index, README, deterministic archive and sidecar；independently reverified bundle members and indexed hashes.
- Files Changed: canonical governance/research/learning documents and semantic governance tests only. Private Correction archives,
  model files, download scripts/logs/environment records, manifest/index, bundle and sidecar remain outside Git.
- Commands: read-only Correction archive inspection and hash/index parsing；isolated Conda clone；approved Hugging Face public
  snapshot downloads；file hash/index/archive verification；repository documentation/static/test checks. No model-loading API,
  GMTP/harness command or GPU workload was invoked.
- Validation: Correction 02 archive `4367` bytes, SHA
  `fcfa3f14c98e0103cb5a1de2f0449fa000d179e2e01d74baa6fec4b013503622`, safe members and `17/17` index pass；GNU apparent
  `5399301224`, allocated `5492817920`, files `33556`, directories `3194`, ceiling `6442450944` and materiality `11/11` pass；
  model index `19/19`, bundle 20 files/3 directories, resource gate, sidecar and archive safety pass；targeted governance
  `19 passed`, full architecture `101 passed`, namespace/label isolation `10 passed`, Ruff passed, Markdown relative links `239`
  checked with zero broken, added secret/private path/raw artifact/protected path/runtime-untracked checks all zero, UTF-8
  no-BOM/LF and `git diff --check` passed. Pytest cache write warnings are non-blocking.
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Run ID: `N/A / EVIDENCE_REVIEW_AND_ARTIFACT_PREPARATION_ONLY`
- Dataset Snapshot: unchanged；no dataset read/download/freeze and no raw NQ content entered the bundle.
- Model / Revision: `facebook/contriever-msmarco@abe8c1493371369031bcb1e02acb754cf4e162fa` and
  `google-bert/bert-base-uncased@86b5e0934494bd15c9632b12f734a8a67f723594`; resolved revisions equal requested revisions.
- Environment Identity: isolated `w2-h1-download`, Python `3.9.25`, huggingface-hub `0.34.4`; download/manifest only；no change to
  `llmguard-paper1`, `gmtp-compat` or the project's formal execution environments.
- Result Summary: Attempt 1 is `VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER`; H1 is
  `OFFLINE_MODEL_ARTIFACTS_PREPARED_PENDING_5090_VERIFICATION`; parent W2 is still not completed/accepted.
- Claims Allowed: exact Correction 02 integrity/provenance/closure；narrow reusable preflight facts；exact model identities,
  file counts/bytes, bundle SHA and H1 pending-verification state.
- Claims Prohibited: models loaded；Worker bundle verification；GMTP run/compatibility；detector scores；runtime/RSS/VRAM；W2
  completion/acceptance；P1/formal experiment/security effectiveness or paper result.
- Blockers: `W2_ATTEMPT1_EVIDENCE_BLOCKER` resolved；parent `BLK-S6.1-FU1-W2-001` remains open until separately approved resumed
  Worker validation succeeds；formal-environment and strict-comparison blockers remain separate.
- Blocker ID: `W2_ATTEMPT1_EVIDENCE_BLOCKER = RESOLVED_BY_CORRECTION_02_CONTROL_PLANE_REVIEW`
- Resolution: command-derived Correction 02 evidence satisfied every material final-closure criterion；H1 artifact creation
  succeeded under the existing owner approval and 2 GiB cap.
- Owner Decisions: `PODR-054; PODR-057; PODR-058`
- Design Changes: none to algorithm, data, model selection, parameter, metric or runtime architecture；evidence classification and
  transfer packaging only.
- Paper Impact: improves reproducibility and provenance only；does not add baseline scores, comparison evidence or conclusions.
- Architecture Impact: no runtime change；preserves Control Plane/Worker and Git/private-artifact boundaries.
- Next Step: project owner transfers the exact Git-external bundle to RTX5090；Worker verifies outer SHA, safe extraction and all
  indexed hashes before any separately controlled W2 resume.
- Next Approval Gate: owner-controlled 5090 bundle verification/resume decision；S6.1-P1 and Formal Experiment remain closed.
- Auto Continue: `NO`

## REL-2026-0020 — Paper 1 Documentation Architecture Reconstructed

- Record ID: `REL-2026-0020`
- Date: `2026-08-01`
- Timestamp: `2026-08-01T18:41:48+08:00`
- Machine: `本机`
- Machine Role: `DOCUMENTATION_CONTROL_PLANE`
- Stage: `Stage 6.1 / Paper 1 Documentation Governance`
- Task ID: `S6.1-DOC-RESTRUCTURE-02`
- Task Name: `Paper 1 Human/LLM Documentation Separation and Ledger Reconstruction`
- Task Type: `DOCUMENTATION_ARCHITECTURE / CONTEXT_PRESERVATION / NO_EXPERIMENT`
- Initial Status: `APPROVED_TO_START / PREVIOUS_SYNC_DOCUMENT_NOT_FOUND_NON_BLOCKING`
- Final Status: `COMPLETED_PENDING_COMMIT`
- Objective: 建立 Human、Agent 与 Stage Process 单一职责文档体系，同时保持既有实验状态、失败和证据不可变。
- Why: 原 README、研究路线与项目审计日志承载过多不同受众信息，需要人类权威、派生镜像、上下文存档与阶段事实明确分离。
- Previous Gate: `OWNER_APPROVED S6.1-DOC-RESTRUCTURE-02`
- Actions: 创建 tingfeng 与 agentUse 总账、需求登记册、研究方案权威文件、LLM 上下文存档和三个唯一阶段过程；README 改为 Start Here；历史路线降级为支撑材料；本日志只增加定位提示和本条索引。
- Files Changed: Paper 1 Markdown documentation, current-state authority navigation, this audit index, and architecture tests only.
- Commands: Git preflight; targeted/full architecture tests; namespace/label isolation; Markdown link, secret/private-path, raw artifact, protected-history, runtime-ignore, UTF-8/LF and diff checks.
- Validation: targeted context recovery `26 passed`; full architecture `108 passed`; namespace + label isolation `10 passed`; Ruff passed; changed-file Markdown relative links `52/52`; 13 changed files passed secret/private-path and UTF-8 no-BOM/LF checks; raw-artifact/protected-path changes `0`; runtime ignore and `git diff --check` passed. The pytest cache write-permission warning is non-blocking. An initial full-test invocation omitted `PYTHONPATH=src` and exposed import-environment failures plus one exact README-state assertion; both invocation/state text were corrected before the green reruns.
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Run ID: `N/A / DOCUMENTATION_ONLY`
- Dataset Snapshot: `UNCHANGED / NOT FROZEN`
- Model / Revision: `UNCHANGED / NO MODEL LOAD OR VERIFICATION`
- Environment Identity: `本机 documentation control plane`
- Result Summary: Paper 1 文档责任架构已重构；所有实验状态与结论边界保持不变。
- Claims Allowed: 文档体系、导航、责任边界、状态镜像、历史与证据索引已重构。
- Claims Prohibited: 任何 5090 验证、W2 完成、H2 批准、P1、Dataset、Detector、Training、Formal Experiment 或论文结果。
- Blockers: `NONE for documentation`; existing experimental blockers unchanged.
- Blocker ID: `N/A`
- Resolution: `PREVIOUS_SYNC_DOCUMENT_NOT_FOUND` 按项目需求提出人决定不再构成 blocker；直接从 Git 权威记录建立新总账。
- Owner Decisions: `S6.1-DOC-RESTRUCTURE-02 approval and documentation rules`.
- Design Changes: Documentation architecture only; no algorithm, dataset, model, parameter, metric or experiment change.
- Next Step: STOP after validation, commit and remote synchronization; experimental work remains at the existing owner gate.
- Next Approval Gate: owner-controlled 5090 H1 verification/W2 resume decision; S6.1-P1 remains closed.
- Auto Continue: `NO`

## REL-2026-0021 — H2 Conditional Offline Bundle Verification and Detection-Core Resume Approved

- Record ID: `REL-2026-0021`
- Date: `2026-08-01`
- Timestamp: `2026-08-01T20:43:35+08:00`
- Machine: `本机`
- Machine Role: `GOVERNANCE_CONTROL_PLANE`
- Stage: `Stage 6.1 / Paper 1 / FU1-W2-H2`
- Task ID: `S6.1-R0-FU1-W2-H2`
- Task Name: `Offline Model Bundle Verification and Conditional GMTP Detection-Core Resume`
- Task Type: `APPROVAL_REGISTRATION / CONTRACT_FREEZE / NO_LOCAL_MODEL_EXECUTION`
- Initial Status: `PROPOSED / NOT CANONICAL / NOT APPROVED` (historical pre-approval snapshot)
- Final Status: `APPROVED_TO_START / NOT SENT / NOT EXECUTED`
- Objective: 批准 5090 先独立验证 H1 offline bundle，并仅在 H2-A 全部通过后条件执行一次冻结双文档 GMTP detection-core smoke。
- Why: 当前最小必要步骤是关闭 W2 工程运行门；同一 H2 内的条件式执行既保护模型来源链，也避免 bundle 通过后再制造一次无研究价值审批循环。
- Previous Gate: `S6.1-R0-FU1-W2-H1 = OFFLINE_MODEL_ARTIFACTS_PREPARED_PENDING_5090_VERIFICATION`.
- Actions: 动态 Git preflight；恢复 Paper 1 权威上下文；登记 PODR-059；冻结 H2-A 18 项 bundle gate、环境/离线/资源边界、一次 H2-B 调用、证据与 stop conditions；同步 Human/Agent/FU1/context/governance 文档；运行治理测试；commit/push。
- Files Changed: Paper 1 Human/Agent/Stage Process records, current governance state/decision/master/audit records, project context and governance tests only.
- Commands: Git/context read-only checks, governance/architecture/namespace/link/secret/private-path/raw-artifact/protected-history/encoding/runtime-ignore/diff validation；no model or GMTP commands.
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Approval Base Commit: `212911a21dc35bef05b15fb840542403c415dd13`
- Run ID: `N/A / APPROVAL_ONLY`
- Dataset Snapshot: `UNCHANGED / NOT FROZEN`
- Model / Revision: Contriever `abe8c1493371369031bcb1e02acb754cf4e162fa`; BERT `86b5e0934494bd15c9632b12f734a8a67f723594`; no model extraction/load on 本机.
- Environment Identity: `本机 governance only`; future H2 uses frozen 5090 `gmtp-compat`.
- Result Summary: H2 approval and conditional contract are canonical；H2 has not been sent or executed.
- Claims Allowed: H2 approval status and frozen bundle/source/input/model/environment/parameter/evidence contract.
- Claims Prohibited: H2 execution, 5090 bundle verification, model load, GMTP result/effectiveness/reproduction, W2 completion/acceptance, metrics, P1, Dataset, Detector, Training, Our Method Result or Formal Experiment.
- Blockers: H2 execution evidence absent by design；parent W2 runtime gate remains open.
- Blocker ID: `BLK-S6.1-FU1-W2-001` remains open.
- Resolution: old H2 proposed status superseded by owner approval；no engineering result was created.
- Owner Decisions: `PODR-059`.
- Design Changes: none to research plan, algorithm, dataset, model selection, parameter, metric or paper scope.
- Paper Impact: `PASS_WITH_ENGINEERING_ONLY_CLAIMS`; improves provenance and engineering feasibility evidence only.
- Architecture Impact: no runtime code change；preserves 本机/5090, Git/private-artifact and fail-closed boundaries.
- Next Step: project owner transfers the approval commit and exact Git-external bundle to 5090；5090 runs H2-A, conditionally one H2-B, then stops and returns evidence to 本机.
- Next Approval Gate: 本机 independent H2 evidence review and project-owner decision；S6.1-P1 remains closed.
- Auto Continue: `CONDITIONAL_WITHIN_H2_ONLY`

## REL-2026-0022 — H2 Resume 01 Blocker Reviewed and Resume 02 Namespace Approved

- Record ID: `REL-2026-0022`
- Date: `2026-08-01`
- Timestamp: `2026-08-01T22:41:56+08:00`
- Machine: `本机`
- Machine Role: `GOVERNANCE_CONTROL_PLANE / EVIDENCE_REVIEW`
- Stage: `Stage 6.1 / Paper 1 / FU1-W2-H2`
- Task ID: `S6.1-R0-FU1-W2-H2-RESUME-02`
- Task Name: `Additive Evidence Namespace Rollover and Conditional H2 Resume`
- Task Type: `EVIDENCE_REVIEW / OWNER_APPROVAL / NO_LOCAL_MODEL_EXECUTION`
- Initial Status: resume_01 `OFFLINE_BUNDLE_SHA_BLOCKER`; bundle later synced；nonempty resume_01 causes `EVIDENCE_CAPTURE_BLOCKER` for reuse.
- Final Status: `RESUME_02 APPROVED_TO_START / NOT EXECUTED`
- Objective: 保留 resume_01 不可变证据，在全新 resume_02 从完整 H2-A 重新开始，不改变任何科学或运行合同。
- Why: 覆盖或删除 resume_01 会改写历史；新 evidence namespace 是最小 additive correction，且 H2-B 从未执行、call_count 为零。
- Previous Gate: `PODR-059 / H2 conditional approval`.
- Actions: 核验 returned archive/sidecar SHA；流式检查 archive safety；独立复算 19/19 index；核对 Git/environment/blocker/call_count；定位本机冻结 bundle；确认 owner 已同步 bundle/sidecar；批准 resume_02 path/archive；同步治理文档与测试。
- Validation: resume_01 archive `4570` bytes、SHA256 `941557aa00be58210015165078bbb3c1cbdd2250cab0755c37198e7b7e26e89d`；20 regular files/1 directory；no unsafe members；top-level only resume_01；evidence index `19/19 PASS`；environment pre/post SHA equal；H2-B false；call_count 0；parent W2 unchanged.
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Approval Base Commit: `2f492dc763e865105510cc8cb141ebde5e109b3e`
- Run ID: `RUN-H2-R01 review / RUN-H2-R02 approval`
- Dataset Snapshot: `UNCHANGED / NOT FROZEN`
- Model / Revision: unchanged frozen Contriever/BERT revisions；bundle/sidecar owner-confirmed synchronized；no model extraction/load on 本机.
- Environment Identity: resume_01 explicit spec SHA `62981f4747156189f7870958da8ea7bc2fc0ead49c78bb6463e9fd284bb65961` unchanged pre/post.
- Result Summary: resume_01 is accepted valid blocker evidence；resume_02 is approved only as a new evidence namespace.
- Claims Allowed: fail-closed blocker/evidence integrity；bundle presence and outer size/SHA owner confirmation；resume_02 governance approval.
- Claims Prohibited: full H2-A pass, model index/load, GMTP result/effectiveness/reproduction, W2 completion/acceptance, P1, Dataset, Detector, Training, Our Method Result or Formal Experiment.
- Blockers: complete H2-A and H2-B evidence remain pending.
- Blocker ID: resume_01 `OFFLINE_BUNDLE_SHA_BLOCKER` closed as historical run outcome；reuse conflict `EVIDENCE_CAPTURE_BLOCKER` resolved only by owner-approved additive resume_02 namespace.
- Resolution: preserve resume_01; use `~/experiments/s6_1_r0_fu1/w2/resume_02`; output `s6_1_r0_fu1_w2_resume02_evidence_20260801.tar.gz` and sidecar.
- Owner Decisions: `PODR-060`; owner requirement `OR-018`.
- Design Changes: evidence paths/names only；no source/input/model/parameter/environment/resource/metric change.
- Paper Impact: provenance improvement only；no experimental or paper result.
- Architecture Impact: preserves immutable evidence and fail-closed execution semantics.
- Next Step: 5090 syncs this governance commit, verifies resume_02 absent/empty, runs complete H2-A, conditionally one H2-B, packages resume02 evidence, and stops.
- Next Approval Gate: 本机 independent resume02 evidence review；S6.1-P1 remains closed.
- Auto Continue: `CONDITIONAL_WITHIN_H2_ONLY`

## REL-2026-0023 — H2 Resume 02 Engineering Smoke Evidence Accepted by Control Plane

- Record ID: `REL-2026-0023`
- Date: `2026-08-01`
- Timestamp: `2026-08-01T23:31:00+08:00`
- Machine: `本机`
- Machine Role: `PRIMARY_CONTROL_PLANE / RAW_EVIDENCE_REVIEW`
- Stage: `Stage 6.1 / Paper 1 / FU1-W2-H2`
- Task ID: `S6.1-R0-FU1-W2-H2-RESUME-02-CONTROL-PLANE-REVIEW`
- Task Name: `H2 Resume 02 Engineering Smoke Evidence Review`
- Task Type: `RAW_EVIDENCE_REVIEW / ENGINEERING_SMOKE_CLASSIFICATION / NO_LOCAL_MODEL_EXECUTION`
- Initial Status: Worker `W2_RESUME02_ENGINEERING_SMOKE_COMPLETED_PENDING_REVIEW`；parent W2 not completed/not accepted.
- Final Status: `CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED`；parent W2 unchanged pending owner decision.
- Objective: independently verify the returned resume02 archive and classify only the evidence-supported minimal detector-core feasibility result.
- Previous Gate: `PODR-060 / REL-2026-0022 / RESUME_02 APPROVED_TO_START`.
- Actions: located the one-time mis-synchronized archive under the local D-drive handoff folder；verified sidecar/recomputed SHA；audited tar paths/types/top-level namespace；independently recomputed all indexed hashes；reviewed contract, Git, bundle/model/source/input/environment/offline, harness single-call, redacted result, resource, log and resume_01 integrity evidence；updated governance mirrors and tests.
- Validation: archive `15625` bytes；SHA256 `58da856a81ad89b858af2c041ff617e16156ec254410b07e6511c2888203f563`；27 regular files/1 directory；only top-level `resume_02`；no unsafe member；evidence index independently `25/25 PASS`；H2-A `18/18 PASS`；environment pre/post SHA equal；RTX5090 local CUDA model load；H2-B true；`call_count=1`；exit 0；all redacted outputs finite；resource gates pass；resume_01 unchanged.
- Repository Validation: targeted context/governance `29 passed`；full architecture `111 passed`；namespace/label isolation `10 passed`；Ruff passed；12 changed Markdown files / 246 relative links passed；13 changed files UTF-8 no-BOM/LF passed；evidence credential-shape scan and Git diff checks passed. Pytest cache write-permission warning is non-blocking.
- Git Branch: `research/stage6-1-hidden-poisoning`
- Git SHA: `PENDING_THIS_COMMIT; resolve with git log -1 -- docs/governance/research_execution_log.md`
- Worker Approval Commit: `38931d50bc3751eefc1dff100b2e901fc905ea3f`
- Run ID: `RUN-H2-R02`
- Dataset Snapshot: fixed existing GMTP packaged input only；Dataset remains `NOT FROZEN`.
- Model / Revision: Contriever `abe8c1493371369031bcb1e02acb754cf4e162fa`；BERT `86b5e0934494bd15c9632b12f734a8a67f723594`；verified local paths on 5090.
- Environment Identity: explicit-spec pre/post SHA256 `62981f4747156189f7870958da8ea7bc2fc0ead49c78bb6463e9fd284bb65961`; frozen Python/Torch/CUDA/Transformers/NumPy identities.
- Result Summary: exact two-document engineering smoke completed once；benign retained and poisoned filtered under threshold `0.2`; evidence accepted only for exact minimal feasibility.
- Claims Allowed: exact archive/index integrity；H2-A pass；local CUDA model load；one frozen call；redacted two-document outputs and resources；minimal Worker feasibility blocker closure.
- Claims Prohibited: GMTP reproduction/effectiveness/safety/generalization；paper metrics/result；W2 completion/acceptance；P1, Dataset, Detector, Training or Formal Experiment advancement.
- Blocker ID: `BLK-S6.1-FU1-W2-001 = RESOLVED_BY_H2_RESUME02_CONTROL_PLANE_REVIEW` only for the frozen minimal feasibility gate.
- Resolution: no corrective 5090 prompt required；single H2-B authorization is consumed；resume_01 and resume_02 remain immutable.
- Owner Decisions: none added for parent W2；existing OR-017/018 and PODR-059/060 govern the completed H2. OR-019 preserves the E-drive `LLMGuard-Handoff` folder as the future compute-output handoff directory.
- Design Changes: none to algorithm, source, input, model, parameter, environment, metric or paper scope.
- Paper Impact: `PASS_WITH_ENGINEERING_ONLY_CLAIMS`; no formal or comparative result.
- Architecture Impact: validates the frozen external detection-core path only；no repository runtime-code change.
- Next Step: project owner decides parent W2 disposition. S6.1-P1 remains closed and requires separate approval.
- Next Approval Gate: explicit project-owner W2 decision；no automatic Worker rerun or P1.

## REL-2026-0024 — Parent W2 Engineering Feasibility Accepted; FU1 Closed; P1 Candidate Prepared

- Record ID: `REL-2026-0024`.
- Date: `2026-08-02`.
- Stage: `Stage 6.1 / Paper 1 / FU1 closure and P1 candidate`.
- Task ID: `S6.1-R0-FU1-W2-OWNER-ACCEPTANCE; S6.1-P1-CONTRACT-CANDIDATE`.
- Machine: `本机 / CONTROL_PLANE`.
- Initial Status: parent W2 `APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED`；H2 evidence accepted；P1 not started.
- Final Status: W2 `HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED`；FU1 `HUMAN_ACCEPTED / CLOSED`；P1
  `CONTRACT_CANDIDATE / NOT APPROVED / NOT STARTED`.
- Objective: register the owner decision, freeze the single-sample engineering-only claim boundary, close FU1, and prepare a
  non-authoritative formal protocol/Benchmark candidate without starting research execution.
- Previous Gate: `PODR-060 / REL-2026-0023 / explicit parent W2 owner decision required`.
- Actions: registered PODR-061 and OR-020；updated Human/Agent/current/master/context/process mirrors；preserved resume_01 and
  Attempt 1 history；created one P1 protocol candidate covering RQ1-5, Benchmark/schema, five views, Tracks, metrics, statistics,
  run/evidence/resource/license boundaries and mutually exclusive detoxification A/B/C options；updated governance tests；commit/push.
- Evidence: acceptance base `b19fc59cc5ba771fd547430f6096403720ef1a7d`；resume02 SHA256
  `58da856a81ad89b858af2c041ff617e16156ec254410b07e6511c2888203f563`；index `25/25 PASS`；H2-A `18/18 PASS`；
  H2-B `call_count=1`.
- Validation: targeted governance/context `30 passed`；full architecture `112 passed`；namespace/label isolation `10 passed`；
  Ruff and `git diff --check` passed；281 changed-document relative links passed；15 changed files passed UTF-8 no-BOM/LF；
  secret/private-path/raw-artifact/protected-history and runtime-ignore checks passed. Pytest cache permission warning is non-blocking.
- Observation: benign retained；poisoned filtered。**这是单次冻结样本的工程观察，不是检测性能结论。**
- Claims Allowed: exact offline bundle/models/source/input/parameter/environment/CUDA/resource identities and one frozen two-doc
  engineering call；W2/FU1 engineering-feasibility closure.
- Claims Prohibited: GMTP reproduction/effectiveness/generalization；strict baseline comparison；detector metrics；Paper result；
  P1 approval/start；Dataset/Detector/Training/Formal Experiment advancement.
- Blocker ID: `BLK-S6.1-FU1-W2-001 = RESOLVED_BY_H2_RESUME02_AND_OWNER_ACCEPTANCE`.
- Preserved Failure: resume_01 `VALID_BLOCKED_EVIDENCE / OFFLINE_BUNDLE_SHA_BLOCKER / H2-B NOT EXECUTED / call_count=0`；
  resume_02 `CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED / call_count=1`.
- Owner Decisions: `PODR-061`; owner requirement `OR-020`.
- Execution Exclusions: no 5090 contact, H2/GMTP/model execution, source/data/model/parameter change, Dataset construction,
  Detector implementation, training or Formal Experiment.
- Next Approval Gate: owner reviews the P1 candidate and selects Detoxification Option A/B/C；
  `HUMAN_DECISION_REQUIRED_BEFORE_P1_APPROVAL`.
- Auto Continue: `NO / H2 SINGLE CALL CONSUMED`

## REL-2026-0025 — P1 Protocol Hardened and Option B Scope Frozen as Review Candidate

- Record ID: `REL-2026-0025`.
- Date: `2026-08-02`.
- Stage: `Stage 6.1 / Paper 1 / approval-preparation gate`.
- Task ID: `S6.1-P1-R1`.
- Machine: `本机 / CONTROL_PLANE`.
- Initial Status: Option A/B/C selection pending；old P1 candidate `CONTRACT_CANDIDATE / NOT APPROVED / NOT STARTED`.
- Final Status: `S6.1-P1-R1 = REVIEW_CANDIDATE / NOT APPROVED / NOT STARTED`；Option B scope confirmed；P1/Pilot not approved or started.
- Base Commit: `P1_R1_BASE_COMMIT = aabe504d55626fb31008822b7bbabd3b32e2afd4`.
- Objective: convert the owner-selected Option B into an approval-grade, falsifiable and resource-bounded protocol candidate without
  constructing data, implementing a method or executing any workload.
- Previous Gate: `PODR-061 / OR-020 / REL-2026-0024` plus explicit owner selection of Option B.
- Actions: registered OR-021 and PODR-062；created the P1-R1 candidate；synchronized Human/Agent/current/master/context/README/
  learning records；preserved the old candidate and all W2/FU1 history；updated governance regression tests.
- Protocol Coverage: RQ1-6 with null/alternative/direction/falsification/slices/baselines；evaluation units and group independence；
  public traceable Chinese source strategy；Benchmark schema/split/field visibility/label isolation；HKP/S/hard negatives；baseline
  tiers and fairness labels；five-view interface；hard filtering/soft downweighting；safety/utility metrics；statistics；Pilot；run/resource/
  evidence/license contracts；20 P1 entry conditions；forward and paper risk reviews.
- Option B Boundary: `OPTION_B_DETECTION_AND_LIGHTWEIGHT_RETRIEVAL_INTERVENTION`; includes only hard filtering or soft
  downweighting. Trusted context package、complete context construction、multi-evidence trusted context generation、complex
  end-to-end Agent defense、production RAG platform and complete trusted retrieval chain are excluded from Paper 1.
- Validation: targeted governance/context `31 passed`；full architecture `113 passed`；namespace/label isolation `15 passed`；
  Ruff and `git diff --check` passed；13 changed Markdown files passed UTF-8 no-BOM/LF, secret/private-path and 293 relative-link
  checks；state/authority/stage-process/candidate-history/raw-artifact/protected-history/runtime-ignore checks passed. One separately
  attempted optional Chroma metadata-isolation test stopped at unavailable `chromadb` before its assertion (`16 passed, 1 dependency
  failure` in that broader optional set); it is not changed or required by this documentation-only task. Pytest cache warning is non-blocking.
- Claims Allowed: owner-confirmed Option B research scope and existence/completeness of a non-authoritative approval-grade candidate.
- Claims Prohibited: P1/Pilot approval or start；Dataset freeze/construction；Detector/Retrieval Intervention implementation；training；
  baseline/Pilot/formal run；model load；Paper result/effectiveness/SOTA.
- Preserved States: W2 `HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED`；FU1 `HUMAN_ACCEPTED / CLOSED`；Dataset
  `NOT FROZEN`；Detector/Retrieval Intervention `NOT IMPLEMENTED`；Training/Formal Experiment `NOT STARTED`；Our Method Result `NONE`.
- Owner Decisions: `PODR-062`; owner requirement `OR-021`.
- Forward Risk Review: `PASS_FOR_REVIEW_CANDIDATE`; leakage, independence, comparison, statistics, evidence, resource and scope risks
  are explicit, while Pilot-dependent quantities remain unvalidated.
- Paper Risk Review: `PASS_WITH_SCOPE_GUARD`; the title's detoxification claim is testable but cannot imply a complete trusted RAG/Agent system.
- Next Approval Gate: owner accepts, revises or rejects the P1-R1 candidate and resolves its four high-level decisions. Auto Continue = `NO`.

## REL-2026-0026 — P1 PILOT0 Infrastructure Completed with Synthetic Engineering Validation

- Record ID: `REL-2026-0026`.
- Date: `2026-08-02`.
- Stage: `Stage 6.1 / Paper 1 / PILOT0`.
- Task ID: `S6.1-P1-PILOT0`.
- Machine: `本机`.
- Initial Status: P1-R1 review candidate；P1/Pilot not approved or started.
- Final Status: P1-R1 `HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK`；P1 `APPROVED_FOR_PILOT0_INFRASTRUCTURE_ONLY / NOT FORMAL_EXPERIMENT`；PILOT0 `COMPLETED_PENDING_REVIEW`.
- Resource Policy: `CODEX_RESOURCE_PRIORITY = 本机优先`；`NO_LOW_VALUE_CHURN = ENFORCED`；no 5090 contact, external API, model, GMTP or GPU use.
- Objective: implement the minimum version-aware poisoning Benchmark contracts and lightweight Option B intervention infrastructure, then validate them only with deterministic synthetic Chinese fixtures.
- Base Commit: `4b0395584627636f5f13658a990614d8f39561eb`.
- Implementation: canonical schema/visibility/group/split/leakage/MutationSpec/hard-negative/intervention/abstention/RunManifest modules under `llmguard`; no new dependency, legacy namespace, database, vector store or model integration.
- Fixture Evidence: 24 explicitly synthetic records；12 HKP × stealth pairs plus 12 hard-negative types；snapshot SHA256 `4f381451688150016b1a518895ad75149cfdfdac4cd512dd6062becba04b2ed0`.
- Validation: targeted final `41 passed`；full architecture initially `107 passed / 6 stale-governance failures`, then `113 passed` after narrow approval-state assertion updates；namespace/label isolation `10 passed`；scoped Ruff passed；repository `.venv` MyPy passed on 10 new source files；8 changed Markdown files / 63 relative links and changed-file secret/private-path/raw-exclusion/protected-history/runtime-ignore/diff checks passed. Full-repository Ruff also exposed 25 immutable historical/script findings plus one new unused import；the new import was fixed and historical files were not changed.
- Claims Allowed: protocol-framework acceptance；Option B scope；existence and deterministic engineering behavior of PILOT0 schema, label isolation, group/split, leakage, attack contract, lightweight intervention, manifest and synthetic fixture.
- Claims Prohibited: completed Benchmark, real data, annotation agreement, Detector implementation, GMTP reproduction, Option B effectiveness, performance/Paper metrics, 240-group Pilot, Our Method Result, Formal Experiment, Paper Result or SOTA.
- Preserved States: `P1_NUMERIC_PARAMETERS = PENDING_PILOT_EVIDENCE`；formal protocol `NOT YET FROZEN`；Dataset `NOT FROZEN`；Detector `NOT IMPLEMENTED`；Training/Formal Experiment `NOT STARTED`；Our Method Result `NONE`.
- Owner Requirement: `OR-022`.
- Next Approval Gate: project owner reviews PILOT0 engineering evidence, then decides whether to approve real-data and annotation Pilot. Auto Continue = `NO`.

## REL-2026-0027 — P1 PILOT1 Public Source and Annotation Packet Feasibility Completed

- Record ID: `REL-2026-0027`.
- Date: `2026-08-02`.
- Stage: `Stage 6.1 / Paper 1 / PILOT1`.
- Task ID: `S6.1-P1-PILOT1`.
- Machine: `本机`.
- Initial Status: PILOT0 `HUMAN_ACCEPTED / ENGINEERING_INFRASTRUCTURE_ONLY / CLOSED`；PILOT1 `APPROVED_TO_START / REAL_PUBLIC_SOURCE_FEASIBILITY_ONLY`.
- Final Status: PILOT1 `COMPLETED_PENDING_REVIEW / REAL_PUBLIC_SOURCE_FEASIBILITY_ONLY`.
- Resource Policy: `CODEX_RESOURCE_PRIORITY = 本机优先`；`NO_LOW_VALUE_CHURN = ENFORCED`；no 5090, model, GMTP, GPU, Detector, training or formal experiment.
- Base Commit: `c555e7da4e5593f72cbf062823feda6bc7798e58`.
- Source Audit: corrected authoritative Git-external run passed `15/15` gates；12 independent version chains across 3 domains (4 each)；24 official public artifacts；raw/normalized `24/24`；all `HASH_ONLY` because republication permission was not explicitly verified.
- Candidate Evidence: 36 `ANNOTATION_CANDIDATE / NOT_ADJUDICATED / NOT_BENCHMARK` records；12 clean/current, 12 poison mutation, 12 matched hard negative；all 12 HKP × stealth combinations covered exactly once.
- Packet Evidence: two independent 36-row blinded packets with anonymous deterministic IDs；attack type, candidate label, mutation operation and expected conclusion excluded；packet hashes indexed.
- Evidence Integrity: `17/17 PASS`；schema/group/split readiness/exact-normalized-identity leakage/raw-artifact exclusion passed. Semantic near-duplicate status remains `NOT_IMPLEMENTED / FAIL_IF_REQUIRED`.
- Validation: Pilot1 targeted `4 passed`；hidden_poisoning full `45 passed`；architecture `113 passed / 1614 subtests` after replacing only stale current-state assertions with additive historical compatibility text；namespace/label isolation `10 passed / 1199 subtests`；scoped Ruff and MyPy passed；8 changed Markdown files / 63 relative links passed；secret/private-path, raw-artifact exclusion, protected history, runtime-ignore, UTF-8 and `git diff --check` passed. Pytest cache write-permission warning is non-blocking.
- Preserved Attempts: the first zero-length-normalized-source attempt and one transiently incomplete corrected acquisition remain untouched as non-authoritative history；corrected_02 is authoritative for review.
- Claims Allowed: real public-source mapping, version-chain, controlled-candidate and executable blinded-packet engineering feasibility only.
- Claims Prohibited: completed Benchmark, Ground Truth, human annotation, annotation agreement, Detector/effectiveness/Option B performance, statistics, 240-group Pilot, Our Method Result, Formal Experiment, Paper Result or SOTA.
- Preserved States: HUMAN_ANNOTATION `NOT STARTED`；ANNOTATION_AGREEMENT `NOT ESTABLISHED`；240_GROUP_PILOT `NOT APPROVED / NOT STARTED`；Dataset `NOT FROZEN`；Detector `NOT IMPLEMENTED`；Retrieval Intervention Effectiveness `NOT ESTABLISHED`；Training/Formal Experiment `NOT STARTED`；Our Method Result `NONE`.
- Owner Requirement: `OR-023`.
- Next Approval Gate: project owner reviews the real public sources and annotation packets, then decides whether to authorize real double annotation and a small agreement Pilot. Auto Continue = `NO`.

## REL-2026-0028 — P1 PILOT2 Independent Annotation Kit Prepared

- Record ID: `REL-2026-0028`.
- Date: `2026-08-02`.
- Stage / Task: `Stage 6.1 / Paper 1 / S6.1-P1-PILOT2-KIT`.
- Machine: `本机`；no 5090, source reacquisition, model, GMTP, Detector, training or formal experiment.
- Owner Decision: PILOT1 `HUMAN_ACCEPTED / REAL_PUBLIC_SOURCE_AND_PACKET_FEASIBILITY_ONLY / CLOSED`；PILOT2 approved for the exact 36-candidate independent double-annotation agreement Pilot；mode `TWO_INDEPENDENT_ANNOTATORS_WITH_OWNER_ADJUDICATION`.
- Source Identity: Pilot1 summary SHA256 `4952f166a0d307210c178a12296a370d86f14111771999cb0cd730629cddeea6`；evidence `17/17`；36 candidates = 12 clean/current + 12 poison + 12 matched hard negatives；two packets `36/36`；HKP×stealth `12/12`.
- Artifact: coordinator/training/A-B Phase 1+2/owner-only structure；6 non-overlapping synthetic practices；UTF-8 BOM CSV；all response columns blank；no evaluator-only fields, raw HTML/PDF, credential payload or cross-annotator/owner-only leakage.
- Validation: spreadsheet inspect/render QA passed；package contract `15/15 PASS`；kit index `17/17 PASS`；outer members `24`；outer ZIP `34430` bytes, SHA256 `a3c884ba313670aaeb78c3674e6c214434ae59576f99cc313fe4c4085eac6463` and sidecar matched；final handoff copy byte identity passed.
- Repository Validation: architecture `113 passed / 1614 subtests`；namespace/label isolation `10 passed / 1199 subtests`；scoped Ruff and MyPy passed；8/8 approved Markdown files and 63 relative links passed；secret/private-path, raw artifact exclusion, protected history, runtime-ignore and `git diff --check` passed. Pytest cache write-permission warning is non-blocking.
- Inner ZIP Identities: A Phase1 `79c5d297...6f19`；A Phase2 `551cc368...de99`；B Phase1 `81d2ccbb...8061`；B Phase2 `f491a1d4...332e`.
- Status: `ANNOTATION_KIT_PREPARED_PENDING_HUMAN_EXECUTION`；HUMAN_ANNOTATION `AUTHORIZED / NOT STARTED`；ANNOTATION_AGREEMENT `NOT ESTABLISHED`；no disagreement or adjudication result.
- Claims Boundary: kit identity and distribution readiness only；not annotation completion, agreement, Dataset freeze, Detector/effectiveness, 240-group Pilot, Training, Formal Experiment or Paper Result.
- Next Gate: distribute training plus A/B Phase 1 only；lock both returned Phase 1 files and SHA256 before distributing either Phase 2. Auto Continue = `NO`.
