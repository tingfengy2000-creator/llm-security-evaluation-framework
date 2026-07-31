# LLMGuard Research Execution Log

## Ledger Contract

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
