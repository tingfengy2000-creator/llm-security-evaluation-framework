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

- **Current as of 2026-09-26 (supersedes the targeted-review-pending snapshot):** Task `P1-FORMAL240-D1-CANARY-PHASE1-FINAL-CLOSEOUT-AND-PHASE2-RELEASE-PREP-01`, Owner `PODR-113 / OR-069`. R3-gpt and R4-codex targeted Phase1 JSON arrays were byte-sliced from the Owner composite attachment and locked independently; both pass 2/2 exact ID/order/schema/enum and five-field agreement 2/2. Candidate V3's two-item naturalness repair is accepted; the designed internal conflict remains. Candidate V3 SHA `6210a6de8f519fb4a58334ff531954b67e774375d021d099dea050f8fe47032e`; existing Phase2 V4 SHA `2daf08286581cb8d28e70ab95ea844e5cdf41e2a6916980bf41b0a90a548ac38` is promoted without overwrite after 24/24 Evidence parity and bounded mechanical re-QA. [Closeout](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_PHASE1_FINAL_CLOSEOUT_V1.md). `PRIMARY_GATING_PAIR=R3-gpt+R4-codex / PHASE1_PRIMARY_QA_ACCEPTED / PHASE2_RELEASE_AUTHORIZED=TRUE / PHASE2_NOT_EXECUTED`. R5-claude is optional/non-gating; Owner later supplied actual 24-row and 2-row files, both byte-locked and validated in the same new namespace. Its naturalness disagreement is auxiliary and does not override the primary gate. Next: Owner sends V4 packet/schema/Guide V4+V4.1 and separate prompts to the **same** R3/R4 sessions, then submits both Phase2 raw returns. Canary Owner acceptance, Human A/B, remaining40, split and training remain unauthorized. Existing unrelated design-spec edit remains untouched.

- **Current as of 2026-09-23 (superseding the R3/R4-not-started snapshot below):** Task `P1-FORMAL240-D1-CANARY-R3R4-PHASE1-LOCK-AND-TARGETED-NATURALNESS-REPAIR-01`, Owner `PODR-112 / OR-068`. Owner corrected attachment attribution: attachment 1 is `R4-codex`, attachment 2 is `R3-gpt`; both raw JSON files are byte-locked in Git-external `paper1_formal240_d1_canary_r3r4_phase1_raw_lock_20260923`, each 24/24 exact ID/order/keys/enums. Five categorical fields agree 24/24; two replicated `MINOR_ISSUE` rows prompted an exact single-phrase V3 repair with two new opaque IDs. The other 22 candidates and frozen Evidence are unchanged. Owner directly attested fresh isolated sessions and no external search, but no session URL/system access log was supplied: `INDEPENDENCE_EVIDENCE=OWNER_ATTESTED_NOT_MACHINE_VERIFIED`. The two-row targeted Phase1 package is ready; Phase2 V4 is prebuilt/hash-locked but withheld. [Record](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_R3_R4_PHASE1_LOCK_AND_TARGETED_REPAIR_RECORD_V1.md). `R3_GPT_PHASE1_LOCKED / R4_CODEX_PHASE1_LOCKED / PHASE1_STRUCTURED_AGREEMENT_COMPLETE / TARGETED_NATURALNESS_REPAIR_PREPARED / WAITING_FOR_R3_R4_TARGETED_REVIEW / PHASE2_RELEASE_AUTHORIZED=FALSE / CANARY_ACCEPTANCE=PENDING / NO_HUMAN_AB`. Next gate: both original reviewer sessions return and separately lock the two repaired candidates' targeted Phase1 results; only on pass can V3 be accepted and V4 release considered. No remaining40, split, training or formal result.

- **Current as of 2026-09-23 (superseding only fresh-reviewer naming and release procedure):** Owner has renamed the future isolated pair to `R3-gpt` + `R4-codex` (`PODR-111 / OR-067`). The [additive V2 plan](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_R3_GPT_R4_CODEX_REVIEW_PLAN_V2.md) and phase prompts are ready; **neither fresh session has started or been attested**. R4-codex must be a new projectless Codex task in an empty isolated directory, not this control-plane/construction session or a fork, with no repository/handoff/context access; an instruction alone is not proof. Both reviewers receive information-equivalent phase files. `PHASE2_RELEASE_AUTHORIZED=FALSE` until **both** new Phase1 raw returns are byte-locked, 24/24 validated and independently attested. Future run-level attestation is separate from candidate JSON. `R3_GPT_REVIEW_SLOT_READY / R4_CODEX_REVIEW_SLOT_READY / FRESH_SESSION_ISOLATION_REQUIRED / WAITING_FOR_R3_GPT_AND_R4_CODEX_PHASE1`. R1/R2 raw and V4/V4.1 remain immutable; Canary acceptance, Human A/B, remaining40, formal split and training are not authorized.

- **Current as of 2026-09-23 (superseding the prior Phase2-release gate):** Owner supplied one composite attachment containing current Phase2 R1/R2 JSON. The whole attachment and two verbatim JSON byte slices are locked in Git-external `paper1_formal240_d1_canary_phase2_preclarification_20260923`; both slices pass 24/24 exact ID/order/schema/enum checks. R1 raw explicitly reports that its session's Phase1 role was R2, so `CURRENT_R1_PHASE2_INDEPENDENCE_VALID=FALSE`. This is a **review-run** incident, not a candidate `phase2_issue`; R1 raw's `OTHER` and note remain untouched. R1/R2 differences are diagnostic-only, never valid independent agreement. [Incident](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_BLIND_REVIEW_PROCESS_INCIDENT_V1.md).
- **Next gate:** Additive [Formal V4.1 field clarification](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_ANNOTATION_GUIDE_V4_1_CLARIFICATION.md) and [fresh R3/R4 plan](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_R3_R4_REVIEW_PLAN_V1.md) are ready. Owner/coordinator must use two new isolated sessions, lock each Phase1 V2 raw before releasing that session's Phase2 V3 + V4.1, then lock both Phase2 raw and resolve blocking discrepancies. `CANARY_ACCEPTANCE=PENDING / HUMAN_AB=PROHIBITED / D1_REMAINING40=NOT_GENERATED / FORMAL_SPLIT_AND_TRAINING=NOT_STARTED`. The previous Phase1 raw locks remain historical evidence; they do not establish a valid cross-phase R1 chain.

- **Current as of 2026-09-23 (superseding the earlier “R1/R2 pending” snapshot):** Owner supplied two independently produced external GPT Phase1 returns for the D1 Canary and authorized `P1-FORMAL240-D1-CANARY-BLIND-PHASE1-RAW-LOCK-01` (`PODR-109 / OR-065`). Both byte-identical raw copies are locked in Git-external `paper1_formal240_d1_canary_phase1_raw_lock_20260923`; R1/R2 each pass 24/24 exact ID/order/schema/enum validation. All five categorical fields agree 24/24, with zero disagreement IDs. The two nonempty note pairs differ in wording but describe the same internal conflicts. [Lock record](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_CANARY_BLIND_PHASE1_RAW_LOCK_RECORD_V1.md).
- **Gate / next action:** `PHASE1_R1_LOCKED=TRUE / PHASE1_R2_LOCKED=TRUE / PHASE1_DOUBLE_BLIND_LOCK_COMPLETE=TRUE / PHASE2_RELEASE_AUTHORIZED=TRUE / PHASE2_NOT_DISTRIBUTED_BY_THIS_TASK`. Independence is Owner-attested, not proven by JSON equality. The next separately executed step is Phase2 V3 distribution to the same isolated R1/R2, then raw return lock/QA. Canary Owner acceptance, Human A/B, remaining D1 40 groups, Formal240 split, Detector training and paper results remain pending/not started. The unrelated existing Stage6 design-spec edit is untouched.

- **Current as of 2026-09-23 (superseding the former D1-approval gate):** Owner approved `P1-FORMAL240-D1-EVIDENCE-FIRST-CANARY-AND-PREANNOTATION-QA-01` as an 8-group/24-candidate construction Canary, with external independent blind GPT QA before any Human A/B release (`PODR-108 / OR-064`). Eight selected slots are real frozen D1 matrix slots; 14 official raw webpage snapshots pass hash checks. A prior V0 wording draft predates the full per-signal preflight and remains scratch-only; the post-preflight candidate V2 and phase-separated blind packages are private, additive construction artifacts. Mechanical QA passed its bounded checks but cannot certify full factual/naturalness/annotation determinacy.
- **Current status / next gate:** `D1_CANARY_CONSTRUCTION_V2_AND_MECHANICAL_QA_READY / EXTERNAL_BLIND_REVIEW_PENDING / OWNER_CANARY_ACCEPTANCE_PENDING / NO_HUMAN_AB`. Owner/coordinator must independently lock R1 and R2 Phase1 returns before releasing Phase2; review flags require versioned repair and full re-review. Canary is **not accepted**, remaining D1 40 groups and Human A/B packets do not exist, Formal240 split/Detector training/formal result remain `NOT_STARTED`. Private evidence namespace `paper1_formal240_d1_canary_20260922`; [full-wave plan](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_D1_FULL_WAVE_CONSTRUCTION_PLAN_V1.md). The unrelated pre-existing Stage6 design-spec edit remains untouched and outside task staging.

- **Current as of 2026-09-22 (superseding previous next-gate text):** Owner approved `P1-FORMAL240-ANNOTATION-SCHEMA-V4-AND-CONSTRUCTION-PROTOCOL-FREEZE-01`. Additive Formal V4, 240 **unfilled** factorial group slots, construction/evidence/metadata/annotation/split design contracts are frozen under [Formal240 protocol](../research/stage6_1_hidden_knowledge_poisoning/formal240/PAPER1_FORMAL_240_GROUP_BENCHMARK_CONSTRUCTION_PROTOCOL_V1.md). `FINAL72_DEVELOPMENT_PHASE_CLOSED=TRUE` moves construction priority; Final72 remains exposed engineering evidence, not an untouched test or formal result. Pilot4/Final72 history remains immutable.
- **Current status / next gate:** `FORMAL_ANNOTATION_SCHEMA_V4_FROZEN / FORMAL_240_GROUP_PROTOCOL_FROZEN / FORMAL_240_GROUP_MATRIX_FROZEN / WAITING_FOR_OWNER_WAVE_D1_APPROVAL`. Matrix: 240 design slots, 0 formal candidates, 0 annotations, 0 split assignments. Seed `20260922` is algorithm-only. Owner must separately approve D1 enterprise-HR Wave (48 groups/144 candidates). No automatic D1, other waves, formal GT/dataset freeze, split execution, detector training, risk calibration, Stage B or Paper Result; `FORMAL_EXPERIMENT=NOT_STARTED`. The pre-existing unrelated Stage6 design.md edit remains outside this task.

- **Current as of 2026-09-22 (superseding the below blocker snapshot):** Owner approved `A_FIRST_THEN_B_IF_NEEDED` for `P1-FDD-FAILURE-ANALYSIS-EVIDENCE-BLOCKER-01`. Bounded original-artifact search found no attributable eight-model OOF; one-time exact evidence reconstruction then passed canonical Full 72-row OOF and all nine machine-summary identity gates under original input/script/environment/fold configuration. The original run remains immutable. Post-lock 21-feature, matched group, T/P, hard-group, HKP/S/domain and scale-hypothesis analysis is complete as **development-only** evidence. See [reconstruction record](../research/stage6_1_hidden_knowledge_poisoning/method_engineering/PAPER1_DETECTOR_V1_1_EVIDENCE_RECONSTRUCTION_RECORD_V1.md) and [analysis](../research/stage6_1_hidden_knowledge_poisoning/method_engineering/PAPER1_FINAL72_DOCUMENT_DETECTOR_FAILURE_ANALYSIS_REPORT_V1.md).
- **Status / next gate:** `EXACT_EVIDENCE_RECONSTRUCTION_PASS / FAILURE_ANALYSIS_COMPLETE / MULTIVIEW_SIGNAL_MIXED / FORMAL_EXPERIMENT_NOT_STARTED`. Recommended next priority is formal 240-group benchmark **construction planning**, subject to separate Owner approval. No Final72 re-tuning, formal sample generation, Detector training, calibration, Stage B model or paper superiority claim is authorized. The earlier `HUMAN_DECISION_REQUIRED` below is historical and resolved by this Owner decision.

- **Current as of 2026-09-22**: `P1-DOCUMENT-DETECTOR-FAILURE-ANALYSIS-AND-SCALE-HYPOTHESIS-REFINEMENT-01` is `HUMAN_DECISION_REQUIRED / Auto Continue=NO`. The Owner approved frozen-result diagnosis, but preflight found the original hash-locked run persisted sample-level OOF only for Full SEPT; eight view/ablation models have aggregate metrics but no per-sample scores. Therefore the required 24-group Full-vs-Full-T/P score shifts and view-specific failure analysis are not evaluable under the explicit no-retraining rule. [Decision-ready blocker](../research/stage6_1_hidden_knowledge_poisoning/method_engineering/PAPER1_DOCUMENT_DETECTOR_FAILURE_ANALYSIS_EVIDENCE_BLOCKER_01.md): `P1-FDD-FAILURE-ANALYSIS-EVIDENCE-BLOCKER-01`.
- **Next gate**: Owner must choose authentic existing OOF artifact, separately authorized additive exact-run reconstruction, or an explicitly reduced-scope partial analysis. Until then, no model fit, no fabricated group shift, no formal hypotheses acceptance, and no claim that this task is complete. Frozen prototype remains `MULTIVIEW_SIGNAL_MIXED / PROTOTYPE_VALID_WITH_LIMITATIONS`; formal experiment remains not started.

## Completed 2026-09-22 detector prototype snapshot (superseded as current)

- **Current as of 2026-09-22**: `P1-FIRST-DOCUMENT-DETECTOR-V1_1-LOGO-PROTOTYPE-EXECUTION-01` completed the first **development-only** non-Oracle Document Detector fit under Owner approval `PODR-104`. Frozen V1.1 GT/Feature Set/Matrix identities passed; 9 fixed LR models each produced 72/72 OOF predictions under 24 complete-group LOGO folds. Full SEPT AUROC `.6471`, AUPRC `.4964`, Poison>HN `18/24`, HN-FPR@0.5 `8/24`; development finding `MULTIVIEW_SIGNAL_MIXED / PROTOTYPE_VALID_WITH_LIMITATIONS`. See the [human report](../research/stage6_1_hidden_knowledge_poisoning/method_engineering/PAPER1_FINAL72_DOCUMENT_DETECTOR_PROTOTYPE_REPORT_V1_1.md) and Git-external hash-locked run `paper1_final72_document_detector_v1_1_logo_20260922`.
- **Next gate**: Owner review and separate approval for failure analysis/scale-hypothesis refinement. No Final72-tuned feature or threshold repair, risk calibration, Stage B, 240-group formal result, untouched-test claim or superiority claim is authorized. `FORMAL_EXPERIMENT=NOT_STARTED`.
- **Git note**: the unrelated pre-existing edit to the Stage 6 trustworthy-retrieval design file remains outside this task; resolve ownership separately. Branch/HEAD/upstream remain dynamic Git facts.

## Completed 2026-09-22 input-resolution snapshot (superseded as current)

- **Current as of 2026-09-22**: `P1-DOCUMENT-DETECTOR-MISSINGNESS-CONTRACT-OWNER-RESOLUTION-01` has completed the Owner-approved A→conditional-C missingness resolution. Option A did not produce a lawful candidate-level relation; Option B was explicitly rejected; additive Option C freezes Feature Set V1.1 and Matrix V1.1 at 72×21 (S3/E9/P6/T3).
- **Gate**: `PHASE_A_PREFLIGHT_PASS / READY_TO_EXECUTE_FIRST_DETECTOR_PROTOTYPE / TRAINING_STARTED_FALSE`. All 24 LOGO training folds have a legal train-only statistic for every retained feature. This is input readiness, not a model, OOF prediction, formal result or automatic execution authority.
- **Evidence**: `E:\LLMGuard-Handoff\paper1_document_detector_missingness_owner_resolution_20260922`; matrix SHA256 `2d418ae2fd6d22f848fcf812a6126fd68ff9b7b880c389a2ca510a5c94dd5b2d`. The original 23-feature artifacts and the 2026-09-21 blocker remain immutable history.
- **Next gate**: separately execute the first Final72 development-only LOGO Detector prototype using exactly V1.1, after a fresh execution preflight. No model fit, threshold tuning, calibration, Stage B or formal benchmark has occurred in this task.

## Historical 2026-09-16 task snapshot (superseded as current)

- Task ID: `P1-RETRIEVAL-BEHAVIOR-HARNESS-AND-DEPLOYABLE-SIGNAL-BOUNDARY-01`.
- Task name: `Paper 1 Retrieval-Behavior Harness, Two-stage Risk Boundary and Deployable Signal Audit`.
- Task type: **OWNER-APPROVED LABEL-BLIND RETRIEVAL HARNESS / THREAT-MODEL AUDIT / TEMPORAL INPUT-GAP AUDIT**.
- Engineering status: **24 QUERY LOCK / 72-DOCUMENT CORPUS LOCK / SPARSE+DENSE DOUBLE TRACE / 8448-ROW R MATRIX LOCK /
  42-SIGNAL DEPLOYABILITY AUDIT / DOCUMENTATION CLOSEOUT**.
- Experiment status: **RETRIEVAL_HARNESS_COMPLETE / TWO_STAGE_RISK_BOUNDARY_FROZEN / DOCUMENT_DETECTOR_NOT_READY /
  RETRIEVAL_RISK_READY_WITH_LIMITATIONS / NO_DETECTOR_TRAINING / NO_FORMAL_RESULT / AUTO_CONTINUE_NO**.
- Documentation gate: **PAPER1_MANDATORY_DOCUMENTATION_CLOSEOUT = OWNER_CONFIRMED / HUMAN_LEDGER_CONTINUOUS_SYNC =
  MANDATORY / TASK_DOCUMENTATION_CLOSEOUT = MANDATORY**. Paper 1 task completion requires execution, tests, evidence,
  documentation closeout and valid Git status; otherwise status is `ENGINEERING_COMPLETED / DOCUMENTATION_CLOSEOUT_PENDING` with
  `TASK_DOCUMENTATION_CLOSEOUT_BLOCKER`.
- Execution base commit: `e46639518aaf58eb9590790917a235e96447898c`.
- Candidate source identity: `candidates_v3_1_additive.jsonl` SHA256
  `15500aa75bced9fb470edaac98f9527e7bb4bc689b86583e6f69b892c48eb210`; final additive corpus SHA256
  `f530471ecd6551300d68c8ddf104cadce2305d8ff91e64010be222820628252d`.
- Execution machine: **本机**. Frozen MiniLM ran CPU/local-only; no download、GPU workload、5090 contact、Detector training、240-group
  generation、formal Dataset or formal experiment occurred.
- Current ordered step: STOP after harness closeout. The next recommended but separately gated task is
  `P1-TRUSTED-EVIDENCE-RETRIEVER-AND-VERSION-REGISTRY-PROTOTYPE-01`; Detector training is not automatically authorized.
- Current blocker: **DOCUMENT DETECTOR INPUT THREAT MODEL NOT CLOSED**. Twenty-nine S/E/P/T signals still depend on oracle-matched
  E1/E2. Seven R signals require a Trusted Version Registry; they remain input-missing rather than using GT/HN roles.
- Current evidence: Git-external namespace `paper1_retrieval_behavior_harness_20260915`. Query/corpus locks are
  `d101d2d4...6f1f` / `0194e1d3...446b`. Sparse and Dense each have two full 1728-row traces. The 8448-row R matrix SHA256 is
  `eeebe7ea92857b0b04dbfb983497b0e28b72f785f507f1acd046cd3cedc6fdef`; 7104 rows compute rank/score/stability and 1344 rows remain
  input-missing for seven version-aware signal types. Query/corpus leakage is zero; locks precede first label load.
- Owner acceptance: `PILOT4_ANNOTATION_PROTOCOL_ACCEPTED=TRUE / ACCEPTED_WITH_NONBLOCKING_NOTES`；all frozen A–F gates passed；
  the two nonblocking reviewer variances remain immutable and do not trigger R4.
- Accepted stack: `PILOT4_ACCEPTED_ANNOTATION_STACK_V1` points to the existing Final72 corpus、Attempt2 final Phase1 protocol/raw、
  Guide V3.2、Expected V3、Evidence Pool V2 and `FROZEN_OFFICIAL_SNAPSHOT_PLUS_URL_PROVENANCE`; it creates no rewritten accepted content.
- A/B execution: Owner named two different independent humans, `HUMAN-A01` and `HUMAN-B01`, and froze complete isolation plus
  `NO_LLM_ASSISTANCE`. The original V1 packages remain immutable/not distributed and are now superseded for distribution because
  their human-facing explanations were insufficient. Additive V2 keeps all 72 candidates、opaque IDs、independent order and exact
  five-column CSV schema unchanged；Packet V2 is a three-column read-only question sheet, while CSV is the only answer sheet.
  Both Phase1 V2 returns are now complete and locked. The additive Phase2 V3.2 workbooks keep Candidate visible beside E1/E2 titles
  and full official URLs plus seven highlighted inputs, retain 144/144 frozen Evidence snapshots as backup, remove sheet protection,
  and preserve canonical English enum dropdowns. Guide V4 adds explanation only. All four raw locks still precede mapping/Expected comparison.
  Git-external V1 namespace remains `paper1_pilot4_ab_execution_20260903` with manifest SHA256
  `aa8742baccab4072a0fe901bcd430b46011cea9b436738a730164f166f0d7d91`；V2 is additive under
  `paper1_pilot4_ab_usability_repair_20260903`; the current additive release namespace is
  `paper1_pilot4_dual_phase1_phase2_v3_20260908`; V3 is immutable but superseded for distribution by
  `paper1_pilot4_phase2_usability_repair_20260909`.
- R3 raw facts: `12062 bytes`；SHA256 `80a10a1ebf2e2321198c750e92214b8d26f9b2a8f4161c64ebf38cae830b4441`；
  exact 8 columns；37 rows / 37 unique opaque IDs；enum、reason and internal consistency PASS；raw-lock-before-Expected PASS；
  mapping parity `37/37`；affected/control `21/16`.
- Expected V3 facts: reviewer-blind independent justification PASS；Expected V3 SHA256
  `dc549ff6adbacc6a87049c08c7db7e414b9d52dafc19c31f98b5c10490031433`；exact row diff `7 fields / 6 candidates`；
  candidate/reviewer changes `0`；Expected V1/V2、Guide、Evidence、mapping and prior comparison/acceptance artifacts unchanged.
- R3 V3 comparison facts: overall `35/37`；version `37/37`；authority `37/37`；minimum evidence `37/37`；issue `37/37`；
  exact relevant fields `35/37`. M2 residual `2/16`；same-root cluster `2`；controls overall/exact `16/16`；M4/BR18 PASS；
  M8 `4/4` PASS；gates A–F all PASS. Residual taxonomy contains only two non-systemic `R3-M1 REVIEWER_VARIANCE`；
  Expected V3 defect `0`；Evidence defect `0`；Guide systemic blocker `0`.
- Calibration decision: `PILOT4_PREANNOTATION_CALIBRATION=CLOSED / PILOT4_CALIBRATION_STOP_CONDITION_MET=TRUE /
  R4_EXTERNAL_REVIEW_REQUIRED=FALSE`. R1/R2 remain historical calibration evidence；R3 is final targeted validation evidence.
- Pilot4 lesson status: thirteen evidence-supported protocol lessons are individually promoted to
  `ACCEPTED_PILOT4_PROTOCOL_LESSON`; claims requiring actual A/B、Ground Truth、Dataset freeze or scale evidence remain provisional.
- Combined-packet correction: the `5d6b4b5` combined packet is preserved unchanged as
  `COMBINED_PACKET_ENGINEERING_ARTIFACT / NOT_APPROVED_FOR_BLIND_SEMANTIC_REVIEW` and
  `SUPERSEDED_FOR_REVIEW_BY_PHASE_SEPARATED_PROTOCOL`. Evidence being present in one LLM context breaks strict Phase1 blindness;
  a behavioral “do not read yet” instruction is not structural separation.
- Attempt2 final comparison facts: first Phase2 raw SHA256 `d7aed1b2...f6cd` remains immutable process evidence；final Phase2 raw is
  `16321 bytes` / SHA256 `6f6cc042...92f1` and supersedes it for analysis. Raw lock preceded mapping/expected load；mapping and final
  corpus parity are 72/72；Phase1 exact is 58/72 and Phase2 exact is 48/72. This comparison authorization is consumed and does not
  authorize protocol acceptance or A/B.
- Attempt1 history: raw bytes `5001`, SHA256 `59446c4be65b035be29528de81b6b8f8aa4113007df8fcac962fe4058a889261`；
  exact five-column schema、72/72 opaque IDs、enums and conditional reasons passed. Owner accepted all five blind-level issues and
  required local repair. Attempt1 remains `VALID_DEFECT_DISCOVERY_REVIEW / NOT_FINAL_CORPUS_ACCEPTANCE_REVIEW` and all files are
  immutable.
- Repair/Attempt2 facts: controlled Attempt1 mapping output `5/5` with 0 unauthorized rows；semantic and source parity `5/5`；67
  unaffected candidate texts and source lines byte-identical；final additive corpus 72；Attempt2 raw SHA256
  `1e5e81fee3825071a77d520c6da5cbfc4c2b59125aca0499cda6c7e2f363c9c5`；exact schema/72 IDs/enums/7 reasons PASS；
  `phase1_issue=NONE` is 72/72. Attempt2 Phase2 has 72 rows / 144 distinct slots and is released as an unfilled packet only.
- Historical correction: the `c1b1245` Full72 result is
  `SAMPLE_ID_LABEL_LOOKUP_CONTAMINATED_REVIEW / NOT_ACCEPTABLE_AS_EXTERNAL_LABEL_BLIND_EVIDENCE` because reviewer logic used
  `sample_id` to query compiled label sets. Its locked output, mismatch chain, final comparison and workbooks remain immutable.
- Historical completed task identity: `S6.1-P1-PILOT2-ADJUDICATION-CLOSURE-AND-PILOT3-ENTRY` closed Pilot2 feasibility and
  established the Pilot3 diagnostic baseline; the immutable closure history remains governed by `PODR-070 / OR-032`.
- Permanent prospective candidate gate (`PODR-067 / OR-029`): every annotation candidate created or newly introduced after
  `2026-08-28` must identify its legal/policy/institutional/standards subject unambiguously from the candidate text itself. Bare
  references such as “条例”、“规定”、“修订文本”、“2017年版” fail closed as `BROKEN_CANDIDATE / MISSING_CONTEXT` and must be
  rewritten or excluded before formal Benchmark admission. Frozen historical candidates and returns are preserved and are not
  retroactively rewritten, relabeled or reinterpreted by this rule.
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
- S6.1-P1: **PILOT4_FINAL72_GT_ACCEPTED / PILOT4_GT_CONSTRUCTION_CLOSED /
  PAPER1_SIGNAL_DETECTION_ENGINEERING_STARTED / FINAL72_DEVELOPMENT_SET_ACTIVE /
  FORMAL_SCALE_BENCHMARK_PENDING / NO_FORMAL_DETECTOR_RESULT_YET /
  NOT FORMAL_EXPERIMENT**.
- S6.1-P1-PILOT0: **HUMAN_ACCEPTED / ENGINEERING_INFRASTRUCTURE_ONLY / CLOSED**.
- S6.1-P1-PILOT1: **HUMAN_ACCEPTED / REAL_PUBLIC_SOURCE_AND_PACKET_FEASIBILITY_ONLY / CLOSED**.
- Historical S6.1-P1-PILOT1: **COMPLETED_PENDING_REVIEW / REAL_PUBLIC_SOURCE_FEASIBILITY_ONLY**；superseded by OR-024.
- S6.1-P1-PILOT2: **HUMAN_ACCEPTED / ANNOTATION_PROTOCOL_AND_GROUND_TRUTH_FEASIBILITY_ONLY / CLOSED**.
- PILOT2_ROUND1_RAW: **PRESERVED_IMMUTABLE**.
- PILOT2_ROUND1: **PRESERVED_FOR_SCHEMA_V2_INDEPENDENT_REREVIEW**.
- A_PHASE1_STRICT_BLINDNESS: **OWNER_CONFIRMED_PRESERVED**.
- ANNOTATION_SCHEMA_V2: **IMPLEMENTED**.
- A_B_REREVIEW: **FOUR_TARGETED_RETURNS_RECEIVED / HASH_LOCKED / VALIDATED_FOR_AGREEMENT**.
- FORMAL_AGREEMENT_V2: **COMPLETED_ON_A_B_V2_CURRENT_VALUES**.
- OWNER_ADJUDICATION: **COMPLETION_PASS / OWNER_CORRECTION_BOUND_SEPARATELY / CONSISTENCY_PASS / NO_PENDING**.
- GROUND_TRUTH_CANDIDATE: **GENERATED / 36_RECORDS / PILOT_ONLY / NOT_FORMAL_DATASET**.
- PILOT3: **ENGINEERING_AND_SIGNAL_FEASIBILITY_ESTABLISHED / PILOT_DIAGNOSTIC_ONLY / STOPPED**.
- Historical PILOT4 first preflight: **OWNER_PREFLIGHT_RETURNED_FOR_TARGETED_REPAIR / a843697 EVIDENCE PRESERVED**.
- Historical PILOT4 second preflight: **SECOND_OWNER_PREFLIGHT_RETURNED_FOR_TARGETED_REPAIR / cad3b2b EVIDENCE PRESERVED**.
- PILOT4: **PILOT4_ANNOTATION_PROTOCOL_ACCEPTED / PILOT4_CALIBRATION_CLOSED /
  PILOT4_A_B_EXECUTION_COMPLETED / OWNER_ADJUDICATION_CLOSED /
  PILOT4_FINAL72_GT_ACCEPTED / ACCEPTED_WITH_KNOWN_EVIDENCE_LIMITATIONS /
  PILOT4_GT_CONSTRUCTION_CLOSED**.
- PILOT4 Final72: **PILOT4_FINAL72_GROUND_TRUTH_V1 / 72 RECORDS / 576 VALUES /
  DEVELOPMENT_AND_METHOD_ENGINEERING_SET / NOT_UNTOUCHED_FINAL_TEST / NOT_FORMAL_FROZEN_DATASET**.
- PAPER1_FORMAL_DOMAIN_SET: **OWNER_CONFIRMED / ENTERPRISE_HR / FINANCE / INFORMATION_SECURITY /
  PROCUREMENT_AND_R_AND_D / EDUCATION_AND_RESEARCH**.
- SCALE_PILOT_STRUCTURE: **5 DOMAINS × 4 HKP × 3 STEALTH × 4 INDEPENDENT CHAINS = 240 GROUPS /
  NOT EXECUTED / APPROX 720 DERIVED CANDIDATES NOT GENERATED / DATASET NOT FROZEN**.
- FIVE_VIEW_METHOD_CONTRACT: **ACCEPTED / SIGNAL_CONTRACT_V1_OWNER_FROZEN**；METHOD ENGINEERING:
  **SCHEMA_REGISTRY_INTERFACES_READY / SIGNAL_FEASIBILITY_EXECUTION_NOT_APPROVED**；FORMAL DETECTOR: **NOT IMPLEMENTED**；
  DETECTION EFFECTIVENESS: **NOT ESTABLISHED**.
- ANNOTATION_MODE: **TWO_INDEPENDENT_ANNOTATORS_WITH_OWNER_ADJUDICATION**.
- BLINDNESS_SUBISSUE: **RESOLVED_BY_OWNER_CONFIRMED_ACTUAL_DISTRIBUTION_ORDER**.
- REGISTRATION_METADATA_SUBISSUE: **DOCUMENTED_AND_EVIDENCE_BOUND / ORIGINAL_METADATA_PRESERVED**.
- REGISTRATION_METADATA_ERROR: **DOCUMENTED**.
- ANNOTATION_SCHEMA_SUBISSUE: **TARGETED_RETURNS_VALIDATED / LOGIC_CONFLICTS_ESCALATED_TO_OWNER_PACKET**.
- RETURN_FILE_CONTRACT_SUBISSUE: **V2_CONTRACT_EXECUTED / NON_SEMANTIC_DEFECTS_PRESERVED**.
- ROUND1_PRESERVATION: **APPROVED / PRESERVED_IMMUTABLE**.
- SCHEMA_V2_REREVIEW: **HUMAN_COMPLETED / FOUR_RETURNS_HASH_LOCKED / FORMAL_AGREEMENT_COMPLETED**.
- Historical S6.1-P1: **APPROVED_FOR_PILOT0_INFRASTRUCTURE_ONLY / NOT FORMAL_EXPERIMENT**；superseded by OR-023.
- Historical S6.1-P1-PILOT0: **COMPLETED_PENDING_REVIEW**；superseded by final owner acceptance under OR-023.
- HUMAN_ANNOTATION: **TARGETED A/B PHASE1+2 RETURNS RECEIVED / ORIGINAL XLSX IMMUTABLE**；
  ANNOTATION_AGREEMENT: **FORMAL_V2_ANALYSIS_COMPLETED / OWNER_ADJUDICATION_REQUIRED**.
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
- Next operational action: Owner reviews the Pilot4 A/B disagreement-only packet. Begin with the five
  `LATE_DISCOVERED_CANDIDATE_DEFECT` flags, then adjudicate the remaining material field disagreements. No automatic Ground Truth,
  Candidate/Evidence repair, 240-group scale-up、Dataset freeze、formal Detector、training、5090 or Formal Experiment is authorized.
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
- Everywhere: any unapproved owner-decision change, 240-group scale-up, Dataset formal freeze, formal Detector/Retrieval
  Intervention implementation, training, 5090 work, Paper Result, Formal Experiment or SOTA comparison.
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

Can claim: the four selected PILOT2 targeted returns were hash-locked; formal A/B V2 agreement preserves 47 disagreement records
and 37 schema-logic conflicts. Owner decisions plus a separately bound correction resolve all 84 issues across 26 candidates without
rewriting the workbook. The Pilot-only Ground Truth contains 36 executable records (Clean 1 / Poison 12 / Hard Negative 23), and
Pilot2 is closed only for annotation-protocol and Ground-Truth feasibility. A deterministic CPU-only Pilot3 generated 180 separated
five-view signal records; this establishes engineering/signal diagnostic execution, not detector effectiveness.

Can claim: the b705cc quality-convergence/Evidence Pool history remains unchanged and the additive hardened candidate version has
23 targeted text repairs. All 72 pools retain two distinct units and A/B deterministic slot-order separation; the human-visible pool
now has four columns with official page/document titles only. Schema V3.1 retains 4 Phase1 and 7 Phase2 manual fields. A separate
visible-input-only process locked one 72/72 semantic review before expected-contract comparison; attempt01 mismatches remain evidence,
final mismatch is zero, validator and all 10 rendered workbook Sheets pass. This is annotation-protocol readiness for Owner acceptance
only. It is explicitly not independent A/B evidence, human validity or distribution.

Can claim: the externally completed targeted R3 raw remains immutable at `12062 bytes` / SHA256 `80a10a1e...0b4441`. Expected V3
was independently derived from candidate、Guide and frozen Evidence and SHA-locked before reviewer values were parsed；its exact
diff is seven fields across six candidates. V3 agreement is overall `35/37` and exact relevant fields `35/37`; controls are 16/16,
M2 is 2/16, M4/M8 pass and frozen gates A–F pass. This supports `RECOMMEND_ACCEPT_WITH_NONBLOCKING_NOTES` and stopping calibration,
not Owner protocol acceptance or benchmark performance.

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

## Historical update — 2026-09-16

- Date: `2026-09-16`.
- Updated by: 本机 executing
  `P1-RETRIEVAL-BEHAVIOR-HARNESS-AND-DEPLOYABLE-SIGNAL-BOUNDARY-01 / REL-2026-0066`.
- Query/corpus/run/signal locks pass before labels. Sparse and frozen-offline Dense each preserve two complete traces. The R matrix
  computes rank/score/stability while version-aware composition remains input-missing. No Detector、threshold、240-group、5090、
  Formal Experiment or Paper Result occurred; Auto Continue=`NO`.
# 2026-09-16 — Trusted Evidence Retriever / Version Registry prototype

- Current task: `P1-TRUSTED-EVIDENCE-RETRIEVER-AND-VERSION-REGISTRY-PROTOTYPE-01` completed.
- Status: `TRUSTED_EVIDENCE_RETRIEVAL_COMPLETE / VERSION_REGISTRY_READY_WITH_LIMITATIONS / DOCUMENT_DETECTOR_READY_WITH_LIMITATIONS`.
- 57-doc trusted corpus and 72 Candidate-derived queries were locked before Oracle E1/E2 evaluation; label/oracle-query leakage is zero.
- Registry metadata remains partial; eight Temporal signals stay `ORACLE_ONLY`. No Detector training, threshold tuning, risk calibration, 240-group run or formal result occurred.
- Next gate: Owner approval for registry coverage repair and non-Oracle Document Detector feature freeze.

# 2026-09-17 — Registry V2, query robustness and Detector feature freeze

- Task `P1-TRUSTED-VERSION-REGISTRY-COVERAGE-REPAIR-QUERY-ROBUSTNESS-AND-DOCUMENT-DETECTOR-FEATURE-FREEZE-01` completed.
- Registry V2 uses only frozen Evidence/accepted metadata: current/history `5/5`, effective interval `26`, authority/issuer `55`, predecessor/successor `1/1`. Unsupported values remain missing; chronology alone is not supersession.
- Four query conditions and 12 deterministic runs were locked before Oracle evaluation. `Q_FULL→Q_NO_TITLE` Hybrid Any-R@1 delta is `-0.0139` and MRR delta `-0.0069` (`SOURCE_TITLE_RISK=NONE`). `Q_TEXT_ONLY→Q_STRUCTURED` deltas are `+0.1667/+0.0833` (`LEXICAL_OVERLAP_RISK=MATERIAL`).
- The deployment-realistic frozen setting is `Q_NO_TITLE + HYBRID`, not the best post-hoc setting. Feature Set V1 contains 23 raw non-Oracle S/E/P/T features; R remains Stage B and six Temporal features remain Oracle diagnostic only.
- Current gate: `DOCUMENT_DETECTOR_READY_WITH_LIMITATIONS`. No Detector was trained; no threshold, calibration, 240-group execution, 5090 run, formal test or result claim occurred.

# 2026-09-21 — First Document Detector Phase A blocked before fitting

- Current task: `P1-FIRST-DOCUMENT-DETECTOR-PROTOTYPE-PREFLIGHT-AND-DEVELOPMENT-EXECUTION-01`.
- Owner approved protocol freeze and prototype training only after every blocking Phase A gate passed.
- Input identity、23 frozen features、72 rows、R/Oracle exclusion、zero blocking leakage、24 matched groups and 24-fold LOGO all pass.
- Missingness gate fails: `host_publisher_relation` and `publisher_issuer_match` are `INPUT_MISSING` in 72/72 rows, have zero observed values and no frozen neutral representation. Training-fold mode is undefined.
- Status: `PHASE_A_BLOCKED / PHASE_B_NOT_AUTHORIZED / TRAINING_STARTED_FALSE / P1-FDD-PREFLIGHT-BLOCKER-01 / HUMAN_DECISION_REQUIRED / Auto Continue=NO`.
- No OOF prediction, metric, ablation, coefficient, bootstrap, permutation control, calibration, Risk or Retrieval Exposure model exists. Next gate is Owner selection of an additive upstream repair, explicit all-missing engineering representation, or versioned 21-feature contract.
