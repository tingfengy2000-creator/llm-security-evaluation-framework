# Paper 1 LLM Context Archive

## Current Context Capsule

```yaml
project_identity: LLMGuard Research Framework / Stage 6.1 / Paper 1
paper_identity:
  chinese_title: 面向中文检索增强生成系统的版本感知隐蔽知识污染基准与多视角解毒方法
  english_working_title: Stealthy Factual Poisoning in Versioned RAG Knowledge Bases - A Benchmark and Multi-View Detection Framework
current_branch: research/stage6-1-hidden-poisoning
current_commit: DYNAMIC_GIT_FACT_VERIFY_LIVE
pilot0_base_commit: 4b0395584627636f5f13658a990614d8f39561eb
pilot1_base_commit: c555e7da4e5593f72cbf062823feda6bc7798e58
research_objective: Chinese version-aware stealthy knowledge poisoning benchmark, multi-view detection and lightweight retrieval intervention
research_boundary: [Benchmark, Detection, Risk Score, Signals, Explanation, Hard Filtering, Soft Downweighting]
accepted_stages:
  S6.1-LR1: HUMAN_ACCEPTED
  Context_Recovery: HUMAN_ACCEPTED
  S6.1-R0: HUMAN_ACCEPTED_WITH_BLOCKERS
  S6.1-R0-FU1-P0: HUMAN_ACCEPTED
  S6.1-R0-FU1-L1: HUMAN_ACCEPTED
current_stage: S6.1-P1 PILOT1 public-source and annotation-packet review gate
current_task: PILOT1 completed pending owner review
current_blockers:
  - real double annotation, agreement Pilot and 240-group Pilot are not approved or started
  - Dataset is not frozen; Detector is not implemented; formal protocol is not frozen
resolved_blockers:
  - W2_ATTEMPT1_EVIDENCE_BLOCKER resolved by Correction 02 control-plane review
  - resume_01 OFFLINE_BUNDLE_SHA_BLOCKER accurately captured and reviewed; bundle/sidecar later synced
  - BLK-S6.1-FU1-W2-001 resolved by H2 resume02 and owner acceptance
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
  h2_resume01_sha256: 941557aa00be58210015165078bbb3c1cbdd2250cab0755c37198e7b7e26e89d
  h2_resume01_index: 19/19 PASS
  h2_resume01_call_count: 0
  h2_resume02_sha256: 58da856a81ad89b858af2c041ff617e16156ec254410b07e6511c2888203f563
  h2_resume02_index: 25/25 PASS
  h2_resume02_call_count: 1
approval_identity:
  h2_approval_base_commit: 212911a21dc35bef05b15fb840542403c415dd13
  h2_resume02_approval_base_commit: 2f492dc763e865105510cc8cb141ebde5e109b3e
  H2_resume01: VALID_BLOCKED_EVIDENCE / OFFLINE_BUNDLE_SHA_BLOCKER
  H2_resume02: CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED
  parent_W2: HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED
  FU1: HUMAN_ACCEPTED / CLOSED
  acceptance_base_commit: b19fc59cc5ba771fd547430f6096403720ef1a7d
  owner_decision: PODR-061
  option_b_decision: PODR-062 / OR-021
  auto_continue: CONSUMED_AND_STOPPED
current_claims:
  - exact two-document engineering-smoke identities, one call and redacted result/resource evidence only
  - H1 bundle and exact local model load verified on 5090 within frozen H2
prohibited_claims:
  - GMTP reproduction, effectiveness, safety, generalization or paper metrics
  - complete strict baseline reproduction
  - any formal Paper 1 result
detoxification_option: OPTION_B
detoxification_scope: OPTION_B_CONFIRMED / OPTION_B_DETECTION_AND_LIGHTWEIGHT_RETRIEVAL_INTERVENTION
excluded_scope: trusted context package, complete context construction, multi-evidence trusted context generation, complex end-to-end Agent defense, production RAG platform, complete trusted retrieval chain
next_decision_gate: project owner reviews PILOT1 public sources and annotation packets, then decides whether to approve real double annotation and a small agreement Pilot
canonical_files:
  owner_requirements: ../human/owner_requirement_register.md
  research_plan: ../human/research_plan_authority.md
  human_ledger: ../human/experiment_ledger_tingfeng.md
  agent_ledger: experiment_ledger_agentUse.md
  current_stage_process: ../stage_process/S6.1-P1_work_process.md
  p1_r1_protocol_candidate: ../s6_1_p1_r1_protocol_review_candidate.md
  historical_p1_protocol_candidate: ../s6_1_p1_protocol_candidate.md
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

### Context Checkpoint — 2026-08-01 — H2-resume-02-rollover

- 当时阶段：S6.1-R0-FU1 / W2-H2。
- 当时任务：保护 resume_01 历史并批准全新 resume_02 证据命名空间。
- 当时状态：resume_01 为 `VALID_BLOCKED_EVIDENCE / OFFLINE_BUNDLE_SHA_BLOCKER`；H2-B 未执行、`call_count=0`；resume_02 为 `APPROVED_TO_START / NOT EXECUTED`。
- 当时 blocker：bundle 后续到位后，非空 resume_01 按合同触发 `EVIDENCE_CAPTURE_BLOCKER`，不得覆盖或删除。
- 当时证据：resume_01 archive 4,570 bytes、SHA256 `941557aa00be58210015165078bbb3c1cbdd2250cab0755c37198e7b7e26e89d`；本机安全复核 20 files/1 directory、index 19/19；项目需求提出人确认 bundle/sidecar 已同步到 5090 且 size/SHA 匹配。
- 当时下一步：5090 同步新的治理提交，在全新 resume_02 从完整 H2-A 开始；只有全部通过才可使用尚未消费的一次 H2-B 授权。
- 后续替代决定：无；不授权覆盖 resume_01、自动 resume_03、P1 或 Formal Experiment。

### Context Checkpoint — 2026-08-02 — W2-owner-acceptance

- 当时阶段：S6.1-R0-FU1 closure / S6.1-P1 candidate gate。
- 当时任务：登记父 W2 最终人工验收、关闭 FU1，并准备非权威 P1 协议候选。
- 当时状态：W2 `HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED`；FU1 `HUMAN_ACCEPTED / CLOSED`；P1 `CONTRACT_CANDIDATE / NOT APPROVED / NOT STARTED`。
- 当时证据：验收基础 `b19fc59cc5ba771fd547430f6096403720ef1a7d`；resume_02 SHA256 `58da856a81ad89b858af2c041ff617e16156ec254410b07e6511c2888203f563`；index `25/25 PASS`；H2-A `18/18 PASS`；H2-B `call_count=1`。
- 历史保留：resume_01 `VALID_BLOCKED_EVIDENCE / OFFLINE_BUNDLE_SHA_BLOCKER / H2-B NOT EXECUTED / call_count=0`；Attempt 1 不重分类为成功运行。
- 声明边界：单样本 benign retained / poisoned filtered 只是工程观察，不是检测性能结论；GMTP reproduction、effectiveness、strict comparison 和 formal paper result 均未建立。
- 当时下一步：项目需求提出人审查 P1 协议候选并选择 Detoxification Option A/B/C；不联系 5090，不自动进入 P1。

### Context Checkpoint — 2026-08-02 — S6.1-P1-R1-option-b-scope-freeze

- 当时阶段：S6.1-P1 审批前协议门。
- 当时任务：`S6.1-P1-R1 / P1 Protocol Hardening and Option B Scope Freeze`。
- 基础提交：`aabe504d55626fb31008822b7bbabd3b32e2afd4`。
- 项目需求：`TITLE_INTENT = CONFIRMED`；`DETOXIFICATION_OPTION = OPTION_B`；`DETOXIFICATION_TECHNICAL_SCOPE = OPTION_B_CONFIRMED`。
- 技术边界：Paper 1 包括 Benchmark、五视角 Detection、Risk Score、Signals、Explanation，以及 hard filtering / soft downweighting；安全与效用分别作为共同主结果。
- 明确排除：trusted context package、完整上下文构造、多证据可信上下文生成、复杂端到端 Agent 防御、生产级 RAG 平台和完整可信检索链；留给 Paper 2 或后续研究。
- 候选证据：[P1-R1 approval-grade review candidate](../s6_1_p1_r1_protocol_review_candidate.md)，覆盖 RQ1-6、Benchmark/schema/split/label isolation、baseline fairness、指标统计、Pilot、资源、evidence、license 和 entry gate。
- 当前状态：P1-R1 `REVIEW_CANDIDATE / NOT APPROVED / NOT STARTED`；P1/Pilot 未批准未开始；Dataset 未冻结；Detector/Retrieval Intervention 未实现；Training/Formal Experiment 未开始；Our Method Result `NONE`。
- 当时下一步：项目负责人只审查或修订候选及四项高层决定；不得联系 5090 或自动推进任何实验。

### Context Checkpoint — 2026-08-02 — S6.1-P1-PILOT0

- 当时任务：在本机实现 Paper 1 Benchmark 与轻量解毒最小基础设施，并仅用纯合成中文 fixture 做确定性工程验证。
- 资源决定：`CODEX_RESOURCE_PRIORITY = 本机优先`；`NO_LOW_VALUE_CHURN = ENFORCED`；没有联系 5090、调用 API、加载模型或使用真实数据。
- 框架状态：P1-R1 `HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK`；`P1_NUMERIC_PARAMETERS = PENDING_PILOT_EVIDENCE`；formal protocol 未冻结。
- 实现状态：PILOT0 `COMPLETED_PENDING_REVIEW`；schema `paper1-pilot0-v1`；24 条纯合成 fixture SHA256 `4f381451688150016b1a518895ad75149cfdfdac4cd512dd6062becba04b2ed0`；targeted tests `41 passed`。
- 声明边界：只证明 schema、标签隔离、group/split、leakage、attack contract、轻量 intervention 和 manifest 的工程可行性；Dataset 未冻结、Detector 未实现、Training/Formal Experiment 未开始、Our Method Result `NONE`。
- 下一门：项目需求提出人审查 PILOT0 工程证据，再决定是否批准真实数据与标注 Pilot；不得自动推进。

### Context Checkpoint — 2026-08-02 — S6.1-P1-PILOT1

- 项目需求提出人最终验收 PILOT0 为 `HUMAN_ACCEPTED / ENGINEERING_INFRASTRUCTURE_ONLY / CLOSED`，并只批准本机执行 `REAL_PUBLIC_SOURCE_FEASIBILITY_ONLY` 的 PILOT1。
- 权威 corrected run：Pilot1-A `15/15 PASS`；12 条独立版本链，3 个领域各 4 条；24 份公开官方来源全部 `HASH_ONLY`，原始和完整正文保持 Git-external。
- Pilot1-B：36 条 `ANNOTATION_CANDIDATE / NOT_ADJUDICATED / NOT_BENCHMARK`，包括 12 clean/current、12 poison mutation、12 matched hard negative；HKP × stealth 12 组合各一条。
- 两类独立盲化包各 36 行，匿名、确定性排序且标签隔离通过；evidence index `17/17 PASS`。首次零长度内容尝试与一次瞬时采集中断作为非权威历史原样保留。
- 当前状态：`S6.1-P1-PILOT1 = COMPLETED_PENDING_REVIEW`；HUMAN_ANNOTATION `NOT STARTED`；ANNOTATION_AGREEMENT `NOT ESTABLISHED`；Dataset `NOT FROZEN`；Detector `NOT IMPLEMENTED`；Formal Experiment `NOT STARTED`。
- 下一门：项目需求提出人审查真实来源与标注包，然后决定是否启动真实双人标注和小规模一致性 Pilot；不得自动推进。
