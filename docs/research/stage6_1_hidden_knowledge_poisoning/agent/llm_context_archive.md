# Paper 1 LLM Context Archive

## Current Context Capsule

```yaml
project_identity: LLMGuard Research Framework / Stage 6.1 / Paper 1
paper_identity:
  chinese_title: 面向中文检索增强生成系统的版本感知隐蔽知识污染基准与多视角解毒方法
  english_working_title: Stealthy Factual Poisoning in Versioned RAG Knowledge Bases - A Benchmark and Multi-View Detection Framework
current_branch: research/stage6-1-hidden-poisoning
current_commit: 212911a21dc35bef05b15fb840542403c415dd13
research_objective: Chinese version-aware stealthy knowledge poisoning benchmark and multi-view detection
research_boundary: [Benchmark, Detection, Risk Score, Signals, Explanation]
accepted_stages:
  S6.1-LR1: HUMAN_ACCEPTED
  Context_Recovery: HUMAN_ACCEPTED
  S6.1-R0: HUMAN_ACCEPTED_WITH_BLOCKERS
  S6.1-R0-FU1-P0: HUMAN_ACCEPTED
  S6.1-R0-FU1-L1: HUMAN_ACCEPTED
current_stage: S6.1-R0-FU1
current_task: H2 approved, not sent, not executed; 5090 H2-A then conditional single H2-B
current_blockers:
  - H2 execution evidence absent because task is not sent or executed
  - H1 not verified or loaded on 5090
  - GMTP detection-core incomplete
  - parent W2 not completed or accepted
resolved_blockers:
  - W2_ATTEMPT1_EVIDENCE_BLOCKER resolved by Correction 02 control-plane review
machine_responsibilities:
  本机: planning, static analysis, evidence review, light artifact preparation, governance
  5090: explicitly approved compute execution and independent artifact verification
source_data_model_identities:
  PoisonedRAG_commit: f660d72174f06b13fae5163ce656e7b235db858f
  GMTP_commit: 15b48d150f93711371eb8da22c211cd84a0cf4df
  SafeRAG_commit: e8f579743b23e0a3937076dcc0792fe29027cba3
  GMTP_input_sha256: 0233a26ecc56d7baf1448b86a114e328beece60624aa88304fa3553e90421e44
  encoder_revision: abe8c1493371369031bcb1e02acb754cf4e162fa
  mlm_revision: 86b5e0934494bd15c9632b12f734a8a67f723594
evidence_identities:
  correction02_sha256: fcfa3f14c98e0103cb5a1de2f0449fa000d179e2e01d74baa6fec4b013503622
  correction02_index: 17/17 PASS
  h1_bundle_sha256: aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45
  h1_model_index: 19/19 PASS
  h1_bundle_source_bytes: 1320359518
approval_identity:
  h2_approval_base_commit: 212911a21dc35bef05b15fb840542403c415dd13
  H2: APPROVED_TO_START / NOT SENT / NOT EXECUTED
  auto_continue: CONDITIONAL_WITHIN_H2_ONLY
current_claims:
  - engineering identities and evidence closure only
  - H1 bundle prepared and verified on 本机 only
prohibited_claims:
  - model verified or loaded on 5090
  - GMTP or W2 completed or accepted
  - complete strict baseline reproduction
  - any formal Paper 1 result
next_decision_gate: project owner transfers approval commit and bundle; 5090 executes H2-A, conditionally one H2-B, then stops for 本机 review
canonical_files:
  owner_requirements: ../human/owner_requirement_register.md
  research_plan: ../human/research_plan_authority.md
  human_ledger: ../human/experiment_ledger_tingfeng.md
  agent_ledger: experiment_ledger_agentUse.md
  current_stage_process: ../stage_process/S6.1-R0-FU1_work_process.md
```

This document is a context recovery artifact.

It is not:

- owner requirement authority;
- research plan authority;
- raw evidence;
- formal result.

Live Git and raw evidence override stale snapshot fields. Owner-confirmed requirements and the research plan can only be changed in their respective canonical human files under the required approval rules.

## Historical Context Checkpoints

### Context Checkpoint — 2026-07-27 — 18cf2741c8383d35604715af6ebf8cbaa2a3ddf1

- 当时阶段：S6-T5 closure。
- 当时任务：受控 retrieval-to-context 工程基线验收。
- 当时状态：`HUMAN_ACCEPTED BASELINE`。
- 当时 blocker：Stage 6.1 未批准，正式实验未开始。
- 当时证据：accepted baseline commit/tag 与测试证据。
- 当时下一步：等待独立批准 Stage 6.1。
- 后续替代决定：S6.1-LR1 路线批准和人工验收；不替代其工程限定声明。

### Context Checkpoint — 2026-07-31 — 2762ae90ccb739892a58f1684248cf777d2b24ed

- 当时阶段：S6.1-R0 closure。
- 当时任务：corrected 5090 evidence review。
- 当时状态：`S6.1-R0 = HUMAN_ACCEPTED_WITH_BLOCKERS`。
- 当时 blocker：PoisonedRAG、GMTP、SafeRAG 仍有定向执行阻塞。
- 当时证据：corrected archive SHA256 `904d79c59e35c6aeb157540049b0f44262b86e5c1c5b3e8d4e96ee2fad3f1c6b`，12/12 index。
- 当时下一步：仅可提出 FU1。
- 后续替代决定：FU1 获批；R0 历史状态不变。

### Context Checkpoint — 2026-08-01 — b922fb9091159a01bd5baad8ee1224d36a665e0d

- 当时阶段：S6.1-R0-FU1 / W2。
- 当时任务：Correction 02 证据闭环与 H1 离线资产准备。
- 当时状态：W2 Attempt 1 为 `VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER`；父 W2 未完成、未验收。
- 当时 blocker：H1 等待 5090 独立验证和离线加载；GMTP detection-core 未完成。
- 当时证据：Correction 02 `fcfa3f14…` 17/17；H1 bundle `aa06e4cd…` 19/19。
- 当时下一步：人工批准后才可由 5090 验证；S6.1-P1 不得启动。
- 后续替代决定：尚无；本 checkpoint 为当前实验上下文。

### Context Checkpoint — 2026-08-01 — documentation-restructure

- 当时阶段：Paper 1 documentation governance。
- 当时任务：`S6.1-DOC-RESTRUCTURE-02`。
- 当时状态：实验状态保持不变；Human/Agent/Stage Process 责任体系建立。
- 当时 blocker：无文档迁移 blocker；实验 blocker 仍如 Current Context Capsule。
- 当时证据：本次文档、架构测试、提交与远端同步记录。
- 当时下一步：停止文档任务；实验继续停在既有人工审批门。
- 后续替代决定：尚无。

### Context Checkpoint — 2026-08-01 — H2-approval

- 当时阶段：S6.1-R0-FU1 / W2。
- 当时任务：`S6.1-R0-FU1-W2-H2` 离线模型包验证与条件式 GMTP 检测核心恢复。
- 当时状态：`APPROVED_TO_START / NOT SENT / NOT EXECUTED`；批准基础提交 `212911a21dc35bef05b15fb840542403c415dd13`。
- 当时 blocker：H1 尚未由 5090 验证或加载；H2 尚无执行证据；父 W2 未完成、未验收。
- 当时证据：项目需求提出人本轮明确批准；bundle、模型、源码、输入、参数、离线、资源和证据合同已物理冻结。
- 当时下一步：项目需求提出人将批准提交与 Git-external bundle 交给 5090；H2-A 全通过后才允许一次 H2-B；完成或任一 blocker 后返回本机复核。
- 后续替代决定：supersede 旧 `H2 = PROPOSED / NOT CANONICAL / NOT APPROVED` 历史快照；不批准 P1、数据集、Detector、训练或正式实验。
