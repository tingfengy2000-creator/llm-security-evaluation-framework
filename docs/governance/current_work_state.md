# Current Work State

本文是**唯一动态任务状态入口**，只回答当前正在执行什么、当前批准了什么、哪些工作必须停止。Git 仍动态决定
branch、HEAD、tag、working tree 和 upstream；权威层级见 [Context Authority Map](context_authority_map.md)。

## Repository Facts

- Active branch: `research/stage6-1-hidden-poisoning`.
- Branch base: accepted S6-T5 baseline `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`.
- Baseline tag `s6-t5-rag-baseline-v1`: recovered as an annotated tag and verified locally/remotely on `2026-07-31` to
  peel strictly to `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`. Future existence and target remain dynamic Git facts.
- Worktree, HEAD, working-tree state and upstream synchronization are dynamic Git facts. Verify them with `git rev-parse`, `git status --short` and `git rev-list --left-right --count @{upstream}...HEAD` before every task.
- Historical Stage 1-5 assets and Stage 6 fixture data remain immutable. Corrections are additive records, never rewrites of evidence.
- Experiment route, historical runs, metrics and evidence indexes are recorded in `docs/governance/experiment_master_record.md`; this file remains the sole dynamic task and approval-gate source.
- Chronological project execution is append-only in [Research Execution Log](research_execution_log.md); it does not replace this current-state page.

## Current Task

- Task ID: `S6.1-P1-PILOT2-ANNOTATION-V2`.
- Task name: `Pilot2 Annotation Schema Repair and Round1 Independent Re-review`.
- Task type: **LOCAL_SCHEMA_REPAIR / ARTIFACT_PREPARATION / NO_AGREEMENT / NO_ADJUDICATION / NO_FORMAL_EXPERIMENT**.
- Status: **ANNOTATION_SCHEMA_V2_IMPLEMENTED / A_B_REREVIEW_READY_FOR_HUMAN_EXECUTION / AUTO_CONTINUE_NO**.
- Base commit: `PILOT2_ANNOTATION_V2_BASE_COMMIT = 561750c6fc5706582dc547cc000271b981abed85`.
- Execution machine: **本机**. Four immutable Round1 returns and the original preflight are hash-bound；V2 validators, complete field
  dictionary and four annotator-isolated re-review ZIPs are prepared. No agreement, adjudication, return mutation, 5090 contact,
  model/GMTP/GPU work, Dataset freeze, Detector, Training or formal experiment occurs.
- Current ordered step: stop after Git synchronization. Human A/B independently complete the V2 packages；after all four returns are
  locked, the owner must separately approve return validation and any agreement calculation.
- Historical superseded H2 snapshot: `PROPOSED / NOT CANONICAL / NOT APPROVED`; preserve as history.
- Formal RAG security experiment: **NOT STARTED**.
- Canonical formal status: `FORMAL_EXPERIMENT = NOT STARTED`.
- Git-Native Research Context Recovery Governance: **HUMAN_ACCEPTED**.
- PO-MHEP: **HUMAN_ACCEPTED / HIGHEST_INTERNAL_PROJECT_EXECUTION_AUTHORITY / PERMANENT / NO_AUTO_EXPIRY**.
- LOCAL role: **PRIMARY_CONTROL_PLANE / PROJECT_EXECUTION_LEAD / RESEARCH_GOVERNANCE_LEAD / 5090_APPROVAL_AUTHORITY /
  PAPER_RISK_REVIEWER / CONTEXT_PRESERVATION_OWNER**.
- RTX5090 role: **COMPUTE_WORKER / NO_SELF_APPROVAL_AUTHORITY**.
- Paper-First Comparative Evidence Principle: **HUMAN_ACCEPTED**.
- Paper 1 current research plan authority: [research_plan_authority.md](../research/stage6_1_hidden_knowledge_poisoning/human/research_plan_authority.md), **ACCEPTED_CURRENT_RESEARCH_PLAN**. The formerly canonical `paper1_research_route.md` remains historical/supporting and does not override it.
- RTX5090 Compute Worker Bootstrap: **HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY**.
- Historical superseded execution snapshot — S6.1-R0: **APPROVED_TO_START**.
- Historical first-review snapshot — S6.1-R0-I: **RETURNED_FOR_WORKER_CORRECTION**.
- Historical first-review parent snapshot — S6.1-R0: **REVIEW_PENDING_CORRECTED_WORKER_EVIDENCE**.
- Parent S6.1-R0: **HUMAN_ACCEPTED_WITH_BLOCKERS**.
- S6.1-R0-FU1: **HUMAN_ACCEPTED / CLOSED**.
- Historical P0 snapshot: **COMPLETED_PENDING_OWNER_REVIEW**.
- S6.1-R0-FU1-P0: **HUMAN_ACCEPTED**.
- S6.1-R0-FU1-L1: **HUMAN_ACCEPTED**.
- Historical S6.1-R0-FU1-W1 candidate: **SUPERSEDED_BY_LOCAL_L1 / NOT FAILED**.
- Historical S6.1-R0-FU1-W2 snapshot: **READY_FOR_OWNER_EXECUTION_APPROVAL / NOT_YET_EXECUTED**.
- S6.1-R0-FU1-W2: **HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED**.
- W2_ENGINEERING_OBJECTIVE: **SATISFIED**.
- W2_RUNTIME_GATE: **CLOSED**.
- W2_ACCEPTANCE_SCOPE: **FROZEN_SINGLE_SAMPLE_DETECTION_CORE_ENGINEERING_FEASIBILITY_ONLY**.
- S6.1-R0-FU1-W2-ATTEMPT1: **VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER**；`smoke_executed=false`；
  `algorithm_failure=false`；`GMTP_incompatibility=not established`.
- S6.1-R0-FU1-W2-ATTEMPT1-CORRECTION-01 gap: **RESOLVED_BY_CORRECTION_02**.
- S6.1-R0-FU1-W2-H1: **OFFLINE_MODEL_ARTIFACTS_VERIFIED_ON_5090 / COMPLETED**.
- S6.1-R0-FU1-W2-H2: **ENGINEERING_SMOKE_COMPLETED / CONTROL_PLANE_REVIEW_PASS / HUMAN_ACCEPTED_AS_W2_EVIDENCE**.
- S6.1-R0-FU1-W2-H2-RESUME-01: **VALID_BLOCKED_EVIDENCE / OFFLINE_BUNDLE_SHA_BLOCKER / H2-B NOT EXECUTED / call_count=0**.
- S6.1-R0-FU1-W2-H2-RESUME-02: **CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED / call_count=1**.
- S6.1-R0-FU1-W2-ATTEMPT1-CORRECTION-02: **CONTROL_PLANE_REVIEW_PASS / FINAL_CLOSURE_APPLIED** under
  `PODR-057` and `PODR-058`.
- S6.1-P1-R1: **HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK**.
- P1 numeric parameters: **PENDING_PILOT_EVIDENCE**；formal protocol: **NOT YET FROZEN**.
- S6.1-P1: **PILOT2_SCHEMA_V2_REREVIEW_PREPARATION_ONLY / NOT FORMAL_EXPERIMENT**.
- S6.1-P1-PILOT0: **HUMAN_ACCEPTED / ENGINEERING_INFRASTRUCTURE_ONLY / CLOSED**.
- S6.1-P1-PILOT1: **HUMAN_ACCEPTED / REAL_PUBLIC_SOURCE_AND_PACKET_FEASIBILITY_ONLY / CLOSED**.
- Historical S6.1-P1-PILOT1: **COMPLETED_PENDING_REVIEW / REAL_PUBLIC_SOURCE_FEASIBILITY_ONLY**；superseded by OR-024.
- S6.1-P1-PILOT2: **ROUND1_RAW_PRESERVED / SCHEMA_V2_REREVIEW_READY_FOR_HUMAN_EXECUTION**.
- PILOT2_ROUND1_RAW: **PRESERVED_IMMUTABLE**.
- PILOT2_ROUND1: **PRESERVED_FOR_SCHEMA_V2_INDEPENDENT_REREVIEW**.
- A_PHASE1_STRICT_BLINDNESS: **OWNER_CONFIRMED_PRESERVED**.
- ANNOTATION_SCHEMA_V2: **IMPLEMENTED**.
- A_B_REREVIEW: **READY_FOR_HUMAN_EXECUTION**.
- FORMAL_AGREEMENT_V2: **NOT_YET_ESTABLISHED**.
- ANNOTATION_MODE: **TWO_INDEPENDENT_ANNOTATORS_WITH_OWNER_ADJUDICATION**.
- BLINDNESS_SUBISSUE: **RESOLVED_BY_OWNER_CONFIRMED_ACTUAL_DISTRIBUTION_ORDER**.
- REGISTRATION_METADATA_SUBISSUE: **DOCUMENTED_AND_EVIDENCE_BOUND / ORIGINAL_METADATA_PRESERVED**.
- REGISTRATION_METADATA_ERROR: **DOCUMENTED**.
- ANNOTATION_SCHEMA_SUBISSUE: **REMEDIATION_IN_PROGRESS**.
- RETURN_FILE_CONTRACT_SUBISSUE: **V2_CONTRACT_IMPLEMENTED_PENDING_HUMAN_RETURN**.
- ROUND1_PRESERVATION: **APPROVED / PRESERVED_IMMUTABLE**.
- SCHEMA_V2_REREVIEW: **APPROVED / READY_FOR_HUMAN_EXECUTION**.
- Historical S6.1-P1: **APPROVED_FOR_PILOT0_INFRASTRUCTURE_ONLY / NOT FORMAL_EXPERIMENT**；superseded by OR-023.
- Historical S6.1-P1-PILOT0: **COMPLETED_PENDING_REVIEW**；superseded by final owner acceptance under OR-023.
- HUMAN_ANNOTATION: **ROUND1 A/B PHASE1+2 RETURNS RECEIVED / V2 INDEPENDENT REREVIEW READY / NOT YET EXECUTED**；
  ANNOTATION_AGREEMENT: **PENDING_SCHEMA_V2_REREVIEW_AND_RETURN_VALIDATION / NOT ESTABLISHED**.
- REAL_DOUBLE_ANNOTATION / 240_GROUP_PILOT: **NOT APPROVED / NOT STARTED**.
- Historical REAL_DATA_PILOT / 240_GROUP_PILOT: **NOT APPROVED / NOT STARTED**；PILOT1 did not authorize human annotation or the 240-group Pilot.
- MINIMAL_MATRIX / FULL_MATRIX: **NOT APPROVED**.
- Dataset: **NOT FROZEN**.
- Dataset Generation: **NOT APPROVED**.
- Detector: **NOT IMPLEMENTED**.
- Detector Implementation: **NOT APPROVED**.
- Retrieval Intervention: **NOT IMPLEMENTED**.
- Retrieval Intervention Implementation: **NOT APPROVED**.
- Training: **NOT STARTED**.
- Model Training: **NOT APPROVED**.
- Our Method Result: **NONE**.
- Corrected review blocker: `R0-I-EVIDENCE-CORRECTION-001` is **RESOLVED_BY_CORRECTED_EVIDENCE**；its discovery and first
  return remain historical evidence。
- `BLK-S6.1-LR1-001` remains **OPEN** for future strict comparison；license/redistribution issues remain separate from internal
  research access。
- P0 source/planning blockers remain resolved. L1 additionally resolves `BLK-S6.1-FU1-W1-001` through exact artifact/schema/
  assembly evidence and supersedes the Worker W1 route. Parent W2 acceptance gate is closed under PODR-061. The historical
  `W2_ATTEMPT1_EVIDENCE_BLOCKER` is
  **RESOLVED_BY_CORRECTION_02_CONTROL_PLANE_REVIEW**。`BLK-S6.1-FU1-W2-001` is
  **RESOLVED_BY_H2_RESUME02_AND_OWNER_ACCEPTANCE** only for the exact frozen minimal detector-core feasibility gate.
- `GMTP_REPRODUCTION = NOT ESTABLISHED`；`DETECTION_EFFECTIVENESS = NOT ESTABLISHED`；
  `STRICT_BASELINE_COMPARISON = NOT ESTABLISHED`；`FORMAL_PAPER_RESULT = NONE`.
- In the single frozen sample pair, benign was retained and poisoned was filtered. 这是单次冻结样本的工程观察，不是检测性能结论。
- `DETOXIFICATION_OPTION = OPTION_B`；`DETOXIFICATION_TECHNICAL_SCOPE = OPTION_B_CONFIRMED`；
  `DETOXIFICATION_TECHNICAL_SCOPE_FULL = OPTION_B_DETECTION_AND_LIGHTWEIGHT_RETRIEVAL_INTERVENTION`.
- Paper 1 intervention is limited to hard filtering or soft downweighting. Trusted context packages, complete context construction,
  multi-evidence trusted context generation, complex end-to-end Agent defense, production RAG platforms and a complete trusted
  retrieval chain are excluded and reserved for Paper 2 or later work.
- Attempt 1 archive integrity passed narrowly: outer SHA-256
  `6acdbb8038e57b1d3e88028350fc08046d73a826ba9dd167452bfc0dd834170f`, safe members `18/18`, evidence index `16/16` and
  harness SHA-256 `8411af2042774f1a18eec95e97a14ade088acbc35f09942ae9ffea4e8ea5fc06`.
- Attempt 1 evidence supports GMTP/source/input/environment identity, encoder `MODEL_DOWNLOAD_BLOCKER` and
  `smoke_executed=false`, but does not contain main-repository HEAD/clean evidence or the claimed 5.2 GB environment measurement.
- Correction 01 archive SHA-256
  `d911063e3a00daba3f8dcfea6f3e6e3b484e79f4f0fe8853a53ff9d8c415279e` passed sidecar/recompute/Worker comparison, safe members
  `6/6` and correction index `4/4`. It binds the original Attempt 1 and supplies passing main-repository integrity evidence.
- Correction 01 reports apparent bytes `5399301224` and allocated bytes `5492817920`, both below `6442450944` and internally
  consistent with its manifest. It does not capture the actual `du` commands or flags, so field provenance and non-confusion were
  not independently verifiable at that review；the later Correction 02 facts below supersede that historical gate state.
- Correction 02 archive `s6_1_r0_fu1_w2_attempt1_correction02_20260801.tar.gz` is 4367 bytes with SHA-256
  `fcfa3f14c98e0103cb5a1de2f0449fa000d179e2e01d74baa6fec4b013503622`. Sidecar/recomputation/report, archive safety and
  sorted evidence index `17/17` passed. GNU coreutils `du 9.4` raw evidence supports apparent `5399301224` from `du -sb` and
  allocated `5492817920` from `du -sB1`, zero exits, unchanged counts/spec identity and both values below `6442450944`.
- The frozen `MATERIALITY_AND_FINAL_CLOSURE_RULE` therefore closes `W2_ATTEMPT1_EVIDENCE_BLOCKER`. Accepted reusable evidence is
  limited to main/GMTP/input/environment/CUDA/disk identities, the encoder download blocker and smoke-not-executed fact；model
  loading, detector outputs/scores, runtime/RSS/VRAM, compatibility and security effectiveness are not reusable evidence.
- H1 prepared exact public snapshots `facebook/contriever-msmarco@abe8c1493371369031bcb1e02acb754cf4e162fa` (8 files,
  438708922 bytes) and `google-bert/bert-base-uncased@86b5e0934494bd15c9632b12f734a8a67f723594` (9 files,
  881643453 bytes). Total model bytes are `1320352375`, below 2 GiB. The Git-external transfer archive SHA-256 is
  `aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45`; H2 resume02 evidence verifies its identity/index and
  local CUDA load on 5090 within the frozen smoke.
- Resource contract is corrected for a future resumed W2 to task-owned disk hard ceiling `10 GiB` (`gmtp-compat <=6 GiB`, two
  exact models `<=2 GiB`, harness/evidence/archive `<=256 MiB`); RAM/VRAM/runtime ceilings remain unchanged. The archive itself
  reports disk/resource limits `NOT_EVALUATED`.
- Environment observation resolved narrowly: R0-A records NumPy 2.4.6 in `llmguard-paper1`；this remains environment evidence,
  not a baseline result。
- Evidence archive SHA-256:
  historical first archive `0ce85a2bfe24e0456f9d29edc40659786d4273fcfc634df8749aee6d0e3aa9cc` with index `18/18`；
  corrected archive `904d79c59e35c6aeb157540049b0f44262b86e5c1c5b3e8d4e96ee2fad3f1c6b` with index `12/12` and matrix
  `fd7617eca689fa46fc6908f94aa4fa158aaae4d277bb17943bbcc1baf74db9bc`。
- LOCAL Control Plane read exact small GitHub source/artifact content in memory for L1；it did not acquire the NQ corpus, install
  dependencies, invoke a model/API service, run retrieval/GMTP/SafeRAG or contact RTX5090.
- Canonical entry: [Stage 6.1 research README](../research/stage6_1_hidden_knowledge_poisoning/README.md).
- Canonical Paper 1 route: [Paper 1 Research Route](../research/stage6_1_hidden_knowledge_poisoning/paper1_research_route.md).
- Canonical FU1-P0 resolution: [Targeted Resolution](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_targeted_resolution.md).
- Canonical H2 resume02 review: [Control Plane Evidence Review](../research/stage6_1_hidden_knowledge_poisoning/s6_1_r0_fu1_w2_h2_resume02_control_plane_review.md).
- Current non-authoritative P1-R1 candidate: [Protocol Hardening and Option B Scope Freeze](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_r1_protocol_review_candidate.md).
- Historical non-authoritative P1 candidate: [Formal Protocol and Benchmark Specification](../research/stage6_1_hidden_knowledge_poisoning/s6_1_p1_protocol_candidate.md).
- Context recovery entry: [Context Authority Map](context_authority_map.md).
- Highest internal execution authority: [PO-MHEP](project_owner_sovereignty_and_mandatory_escalation_principle.md).

## Accepted Baseline

- Last accepted architecture task: `A1R` namespace migration and governance freeze.
- Last accepted implementation stage task: `S6-T5.6 Deterministic Context Package Implementation`.
- Last accepted integration-validation task: `S6-T5.7 Controlled Retrieval Context Pipeline Integration`.
- Last accepted governance task: `GOV-S6-T5-BASELINE-ACCEPTANCE`.
- Historical acceptance snapshot: `GOV-S6-T5.6-ACCEPTANCE`; historical stage label: Last accepted stage task: `S6-T5.6 Deterministic Context Package Implementation`.
- Last accepted implementation commit: `b136ee2`.
- Last accepted integration evidence commit: `b6cedf3`. This is a test/governance evidence commit, never an implementation commit.
- Protocol acceptance closure commit: `432b07e`. It is a governance/design commit, never an implementation commit.
- Accepted capability boundary: deterministic, label-isolated provider-neutral DenseRetriever engineering behavior, including the S6-T5.3-H1 trace and failure-boundary hardening; the S6-T5.4 synthetic in-memory ContentResolver boundary; the S6-T5.5 EvidenceEnvelope/Citation boundary; and the S6-T5.6 synthetic/offline deterministic Context Package boundary. S6-T5.7 additionally accepts controlled integration evidence for these existing components. This does not establish retrieval quality, security effectiveness, context safety, trust policy, LLM integration, or a formal RAG experiment.

## Historical S6-T5 Acceptance Task Snapshot

- Task ID: `GOV-S6-T5-BASELINE-ACCEPTANCE`.
- Task name: `S6-T5 Controlled Retrieval and Traceable Context Baseline Final Human Acceptance`.
- Task type: **GOVERNANCE_BASELINE_ACCEPTANCE_RECORD**.
- Status: **HUMAN_ACCEPTED**. The Git commit created by this task is the baseline governance acceptance record and remains subject to post-commit SHA verification.
- S6-T5.6-P1: HUMAN_ACCEPTED.
- S6-T5.6-P1-H1: HUMAN_ACCEPTED.
- S6-T5.6-P1-H2: HUMAN_ACCEPTED.
- S6-T5.6: HUMAN_ACCEPTED.
- S6-T5.6-I1: HUMAN_ACCEPTED.
- S6-T5.6-I1-H1: HUMAN_ACCEPTED. It hardens only trace scenarios, package configuration identity, dependency error redaction and abstention/trace consistency.
- S6-T5.7: **HUMAN_ACCEPTED**. Static and opt-in real-infrastructure integration evidence is recorded in [S6-T5.7 completion record](s6_t5_7_integration_completion_record.md). Its accepted evidence commit is `b6cedf3`, not a new implementation commit.
- S6-T5.8-H1: **HUMAN_ACCEPTED**. It corrects only the commit-evidence taxonomy and semantic mapping in the [S6-T5 baseline acceptance report](s6_t5_baseline_acceptance_report.md).
- S6-T5.8: **HUMAN_ACCEPTED**. Its original candidate baseline closure commit remains `37cccdc`; its accepted baseline content commit is `4ecf73a`.
- S6-T5 Controlled Retrieval and Traceable Context Baseline: **HUMAN_ACCEPTED BASELINE**. The baseline governance acceptance commit is `CURRENT_ACCEPTANCE_COMMIT / verify from Git after commit`; it is neither an implementation commit nor an integration evidence commit.
- Historical approval snapshot: S6-T5.8 was `APPROVED_TO_START / DOCUMENTATION_IN_PROGRESS` under `PODR-032`; this is not its current status.
- Historical approval snapshot: S6-T5.8-H1 was `APPROVED_TO_START / DOCUMENTATION_HARDENING_IN_PROGRESS`; this is not its current status.
- Historical pre-LR1 snapshot: Stage 6.1 formal research: NOT APPROVED.
- Formal RAG security experiment: NOT STARTED.
- Historical approval-gate snapshot, not the current status: `S6-T5.7+: NOT APPROVED`. The accepted S6-T5.6 implementation history remains `71067d1` (initial candidate), `b136ee2` (final accepted implementation) and `6da27a6` (previous accepted implementation).
- S6-T5.5-P1: **HUMAN_ACCEPTED**.
- S6-T5.5-P1-H1: **HUMAN_ACCEPTED**. Factory only accepts canonical `corpus:` RetrievalEvidence; renderer only accepts Envelope + Binding and fails closed on seven-field mismatch.
- S6-T5.5: **HUMAN_ACCEPTED**.
- S6-T5.5-I1: **HUMAN_ACCEPTED**. Initial implementation commit `2cacef7` remains historical evidence.
- S6-T5.5-H1: **HUMAN_ACCEPTED**. Final hardening commit `6da27a6` fixes metadata immutability, timestamp parity, canonical Evidence UID and fixed redacted input-error semantics without adding ContextBuilder behavior.
- S6-T5.4-P1: **HUMAN_ACCEPTED**.
- Governance acceptance record: `GOV-S6-T5.4-P1-ACCEPTANCE`.
- S6-T5.4 protocol blocker: **RESOLVED_BY_APPROVED_PROTOCOL_FREEZE**. The original discovery, risks and fail-closed stop remain preserved in the blocker record.
- S6-T5.4: **HUMAN_ACCEPTED**.
- S6-T5.4-I1: **HUMAN_ACCEPTED**. It remains an offline engineering implementation, not a formal RAG security experiment.
- S6-T5.4-H1: **HUMAN_ACCEPTED**. It is an acceptance hardening fix, not a new retrieval or RAG capability.
- Blocker record: [S6-T5.4 protocol blocker](s6_t5_4_protocol_blocker_record.md).
- S6-T5.5-P1 review record: [EvidenceEnvelope and Citation boundary freeze](s6_t5_5_protocol_review_record.md).

## Stage 6 Implementation State

- Task ID: `S6-T5.3`.
- Task name: `Provider-Neutral DenseRetriever`.
- Status: **HUMAN_ACCEPTED**.
- GOV-ER1: **HUMAN_ACCEPTED**.
- GOV-ER1-H1: **HUMAN_ACCEPTED**.
- GOV-PODR1: **HUMAN_ACCEPTED**.
- S6-T5.2 `Retrieval Runtime Contracts and IDs`: **HUMAN_ACCEPTED**. Its completed scope is explicit safe query projection, canonical `RetrieverQueryRecord`, deterministic `RetrievalRequest`, `ContentRef`, evidence UID, chunk-level `RetrievalEvidence`, safe evidence summaries, deterministic `RetrievalTrace`, and legacy import/adapter compatibility.
- S6-T5.3-P1: **HUMAN_ACCEPTED**. Public metadata schema `1.1` carries a validated, non-label, no-body `parent_doc_id` from VectorDocument to VectorSearchHit; schema `1.0` remains legacy-compatible.
- S6-T5.3: **HUMAN_ACCEPTED**. DenseRetriever accepts only schema `1.1` hits, validates request/store provenance, and produces canonical `RetrievalEvidence` plus `RetrievalTrace` without reading the corpus.
- S6-T5.3-H1: **HUMAN_ACCEPTED**. Trace `candidate_count` means raw query hits before sorting/deduplication; store provenance and provider/store failure boundaries fail closed with redacted Retrieval errors.
- S6-T5.4: **HUMAN_ACCEPTED**. I1 implements only contracts, injected protocols and synthetic in-memory dependencies; it does not read Stage 6 fixture content or create a real fixture mapping.
- S6-T5.4-H1: **HUMAN_ACCEPTED**. The resolver has no public registry/reader escape hatch; injected adapter, registry and reader errors are re-instantiated with fixed redacted messages while preserving causes.
- Audit boundary: ordinary `repr()` and `to_audit_dict()` omit retrieval query text, document plaintext and content-reference expansion. Runtime query objects physically exclude evaluator fields.

## Approval Gate

- `S6.1-LR1` is `HUMAN_ACCEPTED` at commits `1294632ca0501e7b999a29383780bec49eaa6b04` and
  `85a565535a38196a7d6003e728b5cb6a2b17fa8a` for its benchmark alignment and Context Recovery Governance records.
- The accepted scope is research route, benchmark alignment, governance, context persistence and reproduction planning only.
- Historical R0 execution approval and first `RETURNED_FOR_WORKER_CORRECTION` review remain preserved。The superseding corrected-
  evidence decision is `S6.1-R0 = HUMAN_ACCEPTED_WITH_BLOCKERS`。
- Next operational action: distribute only each annotator's matching V2 packages；A/B independently complete their own Phase1/Phase2
  forms, change logs and retrospective declarations；lock all four return SHA256 values and stop. No automatic agreement calculation
  or adjudication.
  No second H2-B call, automatic resume_03, real-data Pilot, matrix, Dataset, Detector, training or formal experiment is authorized.
- Human accepted: GOV-ER1, GOV-ER1-H1, GOV-PODR1, S6-T5.2, S6-T5.3-P1, S6-T5.3-H1, S6-T5.3 DenseRetriever, S6-T5.4-P1, S6-T5.4-I1, S6-T5.4-H1, and S6-T5.4.
- S6-T5.3 human acceptance is limited to its documented offline engineering scope and deterministic test behavior.
- `S6-T5.4` is **HUMAN_ACCEPTED**. Its acceptance does not approve S6-T5.6 ContextBuilder behavior; that remains a separate boundary.
- `S6-T5.5-P1` and `S6-T5.5-P1-H1` are **HUMAN_ACCEPTED** design protocols. Their I1/H1 implementation was separately accepted; S6-T5.6-P1 now freezes the future package-level selection contract without implementing it.
- `S6-T5.5-I1`, `S6-T5.5-H1` and parent `S6-T5.5` are **HUMAN_ACCEPTED**. They implement only Envelope/Citation contracts and one structural block.
- The acceptance did not authorize Citation allocation, a package or ContextBuilder before I1. The separately approved I1 now implements only those frozen offline behaviors; it does not authorize Trust or model calls.
- S6-T5.6 P1/H1/H2 are HUMAN_ACCEPTED protocol records. `S6-T5.6-I1`, `S6-T5.6-I1-H1` and parent S6-T5.6 are HUMAN_ACCEPTED synthetic/offline implementations.
- S6-T5.7 is HUMAN_ACCEPTED only for the documented controlled retrieval-context engineering evidence. It does not change the accepted implementation commit or establish a formal RAG experiment.
- S6-T5 baseline final acceptance does not create a tag, a Stage 6.1 branch, or a formal RAG experiment.
- Historical S6-T5 snapshot: the project owner had to separately approve Stage 6.1; that snapshot is superseded only for the documentation-only S6.1-LR1 scope.

## Must Not Start

- Automatic 5090 contact/transmission by Codex or any replay of Correction 02. Its evidence-only run and 本机 review are complete.
- On 本机: any external baseline workload, archive extraction, model loading, GMTP/harness smoke, dataset acquisition, GPU computation or formal
  experiment. The narrowly approved H1 public-artifact download is complete and grants no continuing download authority.
- On 5090: overwrite/delete/rename resume_01；reuse or rerun resume_02；automatic resume_03；a second H2-B call；anything beyond the exact frozen H2 contract；network fallback、
  environment mutation、algorithm reimplementation、silent source patch、parameter/input/model substitution or formal workload。
- Everywhere: any unapproved FU1 Worker execution、S6.1-P1、Pilot、Detector/Retrieval Intervention implementation、dataset freeze/construction、training、Paper Result、
  formal experiment or SOTA comparison。
- Additional ContentResolver changes, document-content access beyond synthetic test inputs, Trust policy, retrieval guard, or any S6-T5.8 behavior beyond the completed documentation closure.
- Groq, mock/real LLM invocation, evaluator, metrics, T10-T15, formal RAG attack matrix or report generation.
- New Stage 6 business code under `src/codeguarder/`, any mutation of Stage 1-5, or any mutation of Stage 6 data fixtures.

## Current Claims Boundary

Can additionally claim: H2 resume_01 produced valid fail-closed evidence for a missing bundle/sidecar；its 4,570-byte archive SHA
`941557aa00be58210015165078bbb3c1cbdd2250cab0755c37198e7b7e26e89d`, safe 20-file/1-directory layout and 19/19 index passed 本机 review；H2-B did not execute and call_count is zero。Resume_02 archive SHA
`58da856a81ad89b858af2c041ff617e16156ec254410b07e6511c2888203f563`, safe 27-file/1-directory layout and independently
recomputed `25/25` index passed；H2-A is `18/18 PASS`, exact local models loaded on RTX5090 without CPU fallback, the authorized
H2-B call executed exactly once, and the redacted two-document outputs/resource values are accepted as engineering-smoke evidence
only。Correction 02 passed 本机 raw-evidence review and the final materiality rule closed the historical
`W2_ATTEMPT1_EVIDENCE_BLOCKER`。Attempt 1 is `VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER`, with the narrow reusable
preflight boundary recorded above。H1 prepared two exact-revision offline model snapshots and an integrity-checked transfer bundle
  that is now verified on 5090 for the frozen H2 smoke。P0 and L1 are `HUMAN_ACCEPTED`；the exact released NQ attack-text artifact identity, all 100 records and
official deterministic LM-targeted assembly are verified；API-free reuse is verified feasible while API-free generation and exact
paper-generation identity remain unresolved/partial。The GMTP W2 input, models, parameters, isolated environment and resource
ceiling are frozen and W2/FU1 are accepted and closed only for engineering feasibility。The original
baseline roles remain unchanged。PO-MHEP is permanently accepted as the highest internal execution authority。

Can claim: within the offline engineering-test scope, the `S6-T5 Controlled Retrieval and Traceable Context Baseline` is HUMAN_ACCEPTED. It comprises deterministic and label-isolated retrieval runtime contracts, provider-neutral DenseRetriever, the synthetic ContentResolver, EvidenceEnvelope/Citation boundaries, deterministic Context Package behavior, and S6-T5.7 controlled integration evidence including an opt-in fixed MiniLM plus temporary Chroma close/reopen check. `4ecf73a` is the accepted baseline content commit; the current governance acceptance commit is not an implementation or integration-evidence commit. Historical public loader imports remain compatible through the canonical `llmguard` type.

Cannot claim: the two-document smoke reproduces GMTP；its two scores establish detector effectiveness, calibration, safety,
generalization or a paper metric；any
external baseline was reproduced；strict comparison is ready；SafeRAG pipeline is ready；dataset/
Detector/Our Method/training/result exists；or retrieval quality/security, SOTA, production readiness or formal-experiment outcomes
are established.

## Known Technical Debt

- Historical CRLF/LF hash-baseline false positives remain historical facts; do not rewrite their files to silence checks.
- Dynamic Git state must not be represented as a static assertion in this document.
- S6-T5.3 must preserve all frozen contracts; any need to change them is a `DESIGN_OR_PROTOCOL_BLOCKER`.
- Resolved protocol record: the former hit boundary lacked `parent_doc_id`; schema `1.1` now carries it through the public metadata contract without changing legacy schema `1.0`. See [S6-T5.3 blocker record](s6_t5_3_protocol_blocker_record.md).

## Last Update

- Date: `2026-08-27`.
- Updated by: 本机 implementing PODR-064/OR-026. PODR-063 history and all raw/preflight evidence remain immutable；registration
  error is documented and evidence-bound；Schema V2 and four isolated A/B re-review packages are ready for human execution.
  Formal agreement, disagreement, adjudication, Dataset, Detector, Training and Formal Experiment remain unestablished；Auto
  Continue = `NO`.
