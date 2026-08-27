# Paper 1 Experiment Ledger — agentUse

Document Role = `LLM_STRUCTURED_EXPERIMENT_LEDGER`<br>
Authority = `DERIVED_INFORMATION_VIEW`<br>
Can Override Owner Requirement = `NO`<br>
Can Override Research Plan = `NO`<br>
Can Override Raw Evidence = `NO`<br>
Primary Human Mirror = `../human/experiment_ledger_tingfeng.md`

## Context Identity

```yaml
project: LLMGuard Research Framework
paper: Paper 1 - Chinese version-aware stealthy knowledge poisoning
branch: research/stage6-1-hidden-poisoning
document_source_commit: PILOT2_ANNOTATION_V2_BASE_561750c6fc5706582dc547cc000271b981abed85
snapshot_date: 2026-08-27
authority_order:
  - raw Git and external evidence
  - owner_requirement_register
  - research_plan_authority
  - stage work process
  - human ledger
  - this derived ledger
```

## Current State Snapshot

```yaml
S6.1-LR1: HUMAN_ACCEPTED
Context_Recovery: HUMAN_ACCEPTED
S6.1-R0: HUMAN_ACCEPTED_WITH_BLOCKERS
S6.1-R0-FU1-P0: HUMAN_ACCEPTED
S6.1-R0-FU1-L1: HUMAN_ACCEPTED
S6.1-R0-FU1-W2-ATTEMPT1: VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER
W2_ATTEMPT1_EVIDENCE_BLOCKER: RESOLVED_BY_CORRECTION_02_CONTROL_PLANE_REVIEW
S6.1-R0-FU1-W2-H1: OFFLINE_MODEL_ARTIFACTS_VERIFIED_ON_5090 / COMPLETED
S6.1-R0-FU1-W2-H2: ENGINEERING_SMOKE_COMPLETED / CONTROL_PLANE_REVIEW_PASS / HUMAN_ACCEPTED_AS_W2_EVIDENCE
S6.1-R0-FU1-W2-H2-RESUME-01: VALID_BLOCKED_EVIDENCE / OFFLINE_BUNDLE_SHA_BLOCKER / H2-B NOT EXECUTED / call_count=0
S6.1-R0-FU1-W2-H2-RESUME-02: CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED / call_count=1
S6.1-R0-FU1-W2: HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED
S6.1-R0-FU1: HUMAN_ACCEPTED / CLOSED
W2_ENGINEERING_OBJECTIVE: SATISFIED
W2_RUNTIME_GATE: CLOSED
W2_ACCEPTANCE_SCOPE: FROZEN_SINGLE_SAMPLE_DETECTION_CORE_ENGINEERING_FEASIBILITY_ONLY
BLK-S6.1-FU1-W2-001: RESOLVED_BY_H2_RESUME02_AND_OWNER_ACCEPTANCE
GMTP_REPRODUCTION: NOT ESTABLISHED
DETECTION_EFFECTIVENESS: NOT ESTABLISHED
STRICT_BASELINE_COMPARISON: NOT ESTABLISHED
S6.1-P1-R1: HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK
S6.1-P1: PILOT2_SCHEMA_V2_REREVIEW_PREPARATION_ONLY / NOT FORMAL_EXPERIMENT
S6.1-P1-PILOT0: HUMAN_ACCEPTED / ENGINEERING_INFRASTRUCTURE_ONLY / CLOSED
S6.1-P1-PILOT1: HUMAN_ACCEPTED / REAL_PUBLIC_SOURCE_AND_PACKET_FEASIBILITY_ONLY / CLOSED
S6.1-P1-PILOT2: ROUND1_RAW_PRESERVED / SCHEMA_V2_REREVIEW_READY_FOR_HUMAN_EXECUTION
ANNOTATION_MODE: TWO_INDEPENDENT_ANNOTATORS_WITH_OWNER_ADJUDICATION
P1_NUMERIC_PARAMETERS: PENDING_PILOT_EVIDENCE
HUMAN_ANNOTATION: ROUND1_RETURNS_RECEIVED / V2_REREVIEW_READY / NOT_EXECUTED
BLINDNESS_SUBISSUE: RESOLVED_BY_OWNER_CONFIRMED_ACTUAL_DISTRIBUTION_ORDER
REGISTRATION_METADATA_SUBISSUE: DOCUMENTED_AND_EVIDENCE_BOUND / ORIGINAL_PRESERVED
ANNOTATION_SCHEMA_SUBISSUE: REMEDIATION_IN_PROGRESS
ANNOTATION_SCHEMA_V2: IMPLEMENTED
A_B_REREVIEW: READY_FOR_HUMAN_EXECUTION
ANNOTATION_AGREEMENT: PENDING_SCHEMA_V2_REREVIEW_AND_RETURN_VALIDATION / NOT ESTABLISHED
240_GROUP_PILOT: NOT APPROVED / NOT STARTED
Dataset: NOT FROZEN
Detector: NOT IMPLEMENTED
Retrieval_Intervention: NOT IMPLEMENTED
Training: NOT STARTED
Our_Method_Result: NONE
Formal_Experiment: NOT STARTED
H2_historical_preapproval: PROPOSED / NOT CANONICAL / NOT APPROVED
H2_auto_continue: CONSUMED_AND_STOPPED
DETOXIFICATION_OPTION: OPTION_B
DETOXIFICATION_TECHNICAL_SCOPE: OPTION_B_CONFIRMED
DETOXIFICATION_TECHNICAL_SCOPE_FULL: OPTION_B_DETECTION_AND_LIGHTWEIGHT_RETRIEVAL_INTERVENTION
P1_next_gate: HUMAN_AB_V2_REREVIEW_THEN_SEPARATE_RETURN_VALIDATION_AND_AGREEMENT_APPROVAL
```

## State Machine

`LR1 HUMAN_ACCEPTED -> R0 HUMAN_ACCEPTED_WITH_BLOCKERS -> FU1/W2 closed -> Option B selected -> P1-R1 framework accepted -> PILOT0 accepted/closed -> PILOT1 accepted/closed -> PILOT2 kit prepared -> A/B Round1 returns -> owner metadata correction -> Schema V2 implemented -> A/B human V2 gate`

The owner correction resolves only the timestamp-derived blindness inference. Schema V2 package preparation is separately approved
and complete；human re-review, return validation and agreement are not executed. The 240-group Pilot, Dataset freeze, Detector,
Training and Formal Experiment remain closed.

## Stage Registry

| stage_id | purpose | current_status | canonical_process |
| --- | --- | --- | --- |
| S6.1-LR1 | research route and external baseline alignment | `HUMAN_ACCEPTED` | `../stage_process/S6.1-LR1_work_process.md` |
| S6.1-R0 | engineering reproduction preflight | `HUMAN_ACCEPTED_WITH_BLOCKERS` | `../stage_process/S6.1-R0_work_process.md` |
| S6.1-R0-FU1 | targeted baseline feasibility resolution | `HUMAN_ACCEPTED / CLOSED` | `../stage_process/S6.1-R0-FU1_work_process.md` |
| S6.1-P1-R1 | protocol hardening and Option B scope freeze | `HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK` | source candidate `../s6_1_p1_r1_protocol_review_candidate.md`; numeric parameters pending |
| S6.1-P1 | PILOT0 accepted; PILOT1 public-source feasibility completed pending review; formal protocol not frozen | `REAL_PUBLIC_SOURCE_FEASIBILITY_ONLY / NOT FORMAL_EXPERIMENT` | `../stage_process/S6.1-P1_work_process.md` |

## Run Registry

Canonical per-run schema (every registered run MUST expose all fields):

```yaml
run_id: string
stage_id: string
task_id: string
run_type: planning | engineering_validation | evidence_correction | artifact_preparation | formal_experiment
machine: 本机 | 5090
approval_status: string
source_commit: git_sha_or_NA
source_blob: git_blob_or_NA
data_identity: string_or_NA
input_hash: sha256_or_NA
model_identity: string_or_NA
model_revision: revision_or_NA
environment_identity: string_or_NA
parameters: object_or_NA
start_status: string
final_status: string
result: string
artifact: filename_or_NA
artifact_sha256: sha256_or_NA
evidence_index: count_or_NA
claims_allowed: list
claims_prohibited: list
blocker: string_or_NONE
next_gate: string
```

| run_id | stage_id / task_id | run_type / machine | approval_status | identities and parameters | start_status -> final_status | result / artifact / evidence | claims | blocker / next_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN-LR1-01 | S6.1-LR1 / alignment | planning / 本机 | `HUMAN_ACCEPTED` | source_commit `1294632ca0501e7b999a29383780bec49eaa6b04`; source_blob `NA`; data/input/model/environment `NA`; parameters `document review` | `APPROVED` -> `HUMAN_ACCEPTED` | Baseline roles and route; artifact `paper1_benchmark_alignment_matrix.md`; artifact_sha256/evidence_index `NA` | allowed: planning/alignment; prohibited: reproduction/formal result | blocker `NONE`; next_gate R0 approval |
| RUN-R0-CORRECTED | S6.1-R0 / corrected evidence | engineering_validation / 5090 | `HUMAN_ACCEPTED_WITH_BLOCKERS` | source commits PoisonedRAG `f660d72174f06b13fae5163ce656e7b235db858f`, GMTP `15b48d150f93711371eb8da22c211cd84a0cf4df`, SafeRAG `e8f579743b23e0a3937076dcc0792fe29027cba3`; source_blob/data/input/model revisions in artifact registry; environment `R0 5090 snapshot`; parameters `preflight only` | `APPROVED_TO_START` -> `HUMAN_ACCEPTED_WITH_BLOCKERS` | corrected archive; artifact_sha256 `904d79c59e35c6aeb157540049b0f44262b86e5c1c5b3e8d4e96ee2fad3f1c6b`; evidence_index `12/12` | allowed: engineering feasibility; prohibited: strict reproduction/formal result | blocker `targeted execution blockers`; next_gate FU1 |
| RUN-W2-A1 | S6.1-R0-FU1 / W2-ATTEMPT1 | engineering_validation / 5090 | `VALID_BLOCKED_ENGINEERING_RUN` | source_commit GMTP `15b48d150f93711371eb8da22c211cd84a0cf4df`; source_blob `72fb52cda9ea794bafb5c114ee937a00f4d1728a`; data `GMTP packaged input, 200 records`; input_hash `0233a26ecc56d7baf1448b86a114e328beece60624aa88304fa3553e90421e44`; models/revisions as H1; environment `gmtp-compat`; parameters `ret_type=contriever, remove_threshold=0.2, remove_lambda=1.0` | `APPROVED_TO_START` -> `VALID_BLOCKED_ENGINEERING_RUN / MODEL_DOWNLOAD_BLOCKER` | artifact original archive; artifact_sha256 `6acdbb8038e57b1d3e88028350fc08046d73a826ba9dd167452bfc0dd834170f`; evidence_index `16/16` | allowed: blocker and preflight evidence; prohibited: W2 completion/detection result/formal result | blocker `MODEL_DOWNLOAD_BLOCKER`; next_gate evidence correction and H1 |
| RUN-W2-C02 | S6.1-R0-FU1 / W2-ATTEMPT1-CORRECTION-02 | evidence_correction / 5090 | `CONTROL_PLANE_REVIEW_PASS / FINAL_CLOSURE_APPLIED` | source_commit `b185b8fca74c68ef75a6150b62551f84759c0304`; source_blob/data/input/model `NA`; environment `same W2 environment evidence`; parameters `disk command provenance` | `EVIDENCE_BLOCKED` -> `RESOLVED_BY_CORRECTION_02_CONTROL_PLANE_REVIEW` | artifact correction02 archive; artifact_sha256 `fcfa3f14c98e0103cb5a1de2f0449fa000d179e2e01d74baa6fec4b013503622`; evidence_index `17/17 PASS` | allowed: evidence closure; prohibited: W2 completion/model load/formal result | blocker `NONE for evidence`; next_gate H1 5090 verification |
| RUN-H1-01 | S6.1-R0-FU1 / W2-H1 | artifact_preparation / 本机 | `PREPARED / NOT 5090 VERIFIED` | source_commit `b922fb9091159a01bd5baad8ee1224d36a665e0d`; source_blob/data/input `NA`; models `facebook/contriever-msmarco`, `google-bert/bert-base-uncased`; revisions `abe8c1493371369031bcb1e02acb754cf4e162fa`, `86b5e0934494bd15c9632b12f734a8a67f723594`; environment `本机 offline bundle preparation`; parameters `immutable revisions` | `APPROVED_TO_PREPARE` -> `OFFLINE_MODEL_ARTIFACTS_PREPARED_PENDING_5090_VERIFICATION` | artifact `s6_1_r0_fu1_w2_models_20260801.tar.gz`; artifact_sha256 `aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45`; evidence_index `19/19 PASS` | allowed: 本机 preparation/integrity; prohibited: 5090 verification/load/GMTP completion/formal result | blocker `5090 verification pending`; next_gate owner-approved 5090 verification |
| RUN-H2-APPROVAL | S6.1-R0-FU1 / W2-H2 | approval_and_contract_freeze / 本机 | `APPROVED_TO_START / NOT SENT / NOT EXECUTED` | source_commit `212911a21dc35bef05b15fb840542403c415dd13`; source_blob `84e69b3eadeb8adc0ce521501f8b560d6377b489`; data/input_hash `GMTP NQ index 0 test0 / 0233a26ecc56d7baf1448b86a114e328beece60624aa88304fa3553e90421e44`; models/revisions fixed as H1; environment `gmtp-compat frozen`; parameters `ret_type=contriever,N=5,M=5,remove_threshold=0.2,remove_lambda=1.0,topk=10,do_sort=false` | `PROPOSED / NOT APPROVED` -> `APPROVED_TO_START / NOT SENT / NOT EXECUTED` | result `governance approval only`; artifact/artifact_sha256/evidence_index `NA` | allowed: H2 contract and conditional gate; prohibited: claim of send/execution/model load/GMTP result/W2 acceptance/P1/formal result | blocker `H2 execution evidence absent by design`; next_gate 5090 H2-A, conditional H2-B, then 本机 review |
| RUN-H2-R01 | S6.1-R0-FU1 / W2-H2-RESUME-01 | engineering_validation / 5090 | `APPROVED` | approval commit `2f492dc763e865105510cc8cb141ebde5e109b3e`; bundle expected SHA `aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45`; environment spec pre/post `62981f4747156189f7870958da8ea7bc2fc0ead49c78bb6463e9fd284bb65961`; parameters frozen, not invoked | `APPROVED_TO_START` -> `VALID_BLOCKED_EVIDENCE / OFFLINE_BUNDLE_SHA_BLOCKER` | artifact `s6_1_r0_fu1_w2_resume01_evidence_20260801.tar.gz`; artifact_sha256 `941557aa00be58210015165078bbb3c1cbdd2250cab0755c37198e7b7e26e89d`; evidence_index `19/19 PASS`; call_count `0` | allowed: missing-transfer blocker and fail-closed behavior; prohibited: H2-A pass/model load/GMTP result/W2 acceptance | blocker `OFFLINE_BUNDLE_SHA_BLOCKER`; next_gate owner decision on additive evidence namespace |
| RUN-H2-R02-APPROVAL | S6.1-R0-FU1 / W2-H2-RESUME-02 | approval_and_contract_freeze / 本机 | `APPROVED_TO_START / NOT EXECUTED` | approval base `2f492dc763e865105510cc8cb141ebde5e109b3e`; bundle/sidecar reported synced and outer size/SHA matched; all source/input/model/environment/parameter identities unchanged | `EVIDENCE_CAPTURE_BLOCKER on nonempty resume_01` -> `RESUME_02 APPROVED_TO_START / NOT EXECUTED` | result `additive namespace rollover only`; artifact `resume02 pending`; evidence_index `NA`; H2-B call_count remains `0` | allowed: new evidence namespace and fresh H2-A; prohibited: overwrite resume_01/automatic resume_03/repeated H2-B/P1/formal result | blocker `NONE for approved rollover`; next_gate 5090 fresh H2-A in resume_02 |
| RUN-H2-R02 | S6.1-R0-FU1 / W2-H2-RESUME-02 | engineering_smoke / 5090 + review / 本机 | `CONTROL_PLANE_REVIEW_PASS / ENGINEERING_SMOKE_EVIDENCE_ACCEPTED` | main approval HEAD `38931d50bc3751eefc1dff100b2e901fc905ea3f`; GMTP commit/blob/source, input index/hash, two model revisions, environment SHA and official parameters all frozen | `APPROVED_TO_START` -> `W2_RESUME02_ENGINEERING_SMOKE_COMPLETED_PENDING_REVIEW` -> `CONTROL_PLANE_REVIEW_PASS` | artifact `s6_1_r0_fu1_w2_resume02_evidence_20260801.tar.gz`; artifact_sha256 `58da856a81ad89b858af2c041ff617e16156ec254410b07e6511c2888203f563`; evidence_index `25/25 PASS`; H2-A `18/18`; call_count `1` | allowed: exact minimal feasibility and redacted two-document observation; prohibited: reproduction/effectiveness/safety/paper result/W2 acceptance | blocker `BLK-S6.1-FU1-W2-001 resolved for minimal gate`; next_gate parent W2 owner decision |
| GOV-W2-ACCEPTANCE | S6.1-R0-FU1 / W2 owner acceptance | governance_acceptance / 本机 | `HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED` | acceptance base `b19fc59cc5ba771fd547430f6096403720ef1a7d`; evidence RUN-H2-R02; algorithm/data/model/parameter identities unchanged | `CONTROL_PLANE_REVIEW_PASS` -> `HUMAN_ACCEPTED / ENGINEERING_FEASIBILITY_ONLY / CLOSED` | result `W2_ENGINEERING_OBJECTIVE=SATISFIED`; artifact/evidence index `NA / references immutable RUN-H2-R02 25/25` | allowed: frozen single-sample engineering feasibility and FU1 closure; prohibited: reproduction/effectiveness/strict comparison/metrics/formal result | blocker `BLK-S6.1-FU1-W2-001 RESOLVED_BY_H2_RESUME02_AND_OWNER_ACCEPTANCE`; next_gate P1-R1 candidate review |
| DESIGN-P1-R1 | S6.1-P1 / P1-R1 | planning / 本机 | `REVIEW_CANDIDATE / NOT APPROVED / NOT STARTED` | base commit `aabe504d55626fb31008822b7bbabd3b32e2afd4`; no data/model/environment/run identity | `OPTION_B_SELECTED` -> `APPROVAL_GRADE_REVIEW_CANDIDATE` | Option B scope, RQ1-6, Benchmark/schema/split, baseline fairness, metrics/statistics, Pilot/resource/evidence/license candidates；artifact `../s6_1_p1_r1_protocol_review_candidate.md` | allowed: design and scope freeze；prohibited: P1/Pilot/Dataset/implementation/training/result | blocker `OWNER_REVIEW`; next_gate owner accepts/revises/rejects candidate |
| RUN-P1-PILOT0-SYNTHETIC | S6.1-P1 / PILOT0 | engineering_validation / 本机 | `COMPLETED_PENDING_REVIEW` | base commit `4b0395584627636f5f13658a990614d8f39561eb`; schema `paper1-pilot0-v1`; fixture SHA256 `4f381451688150016b1a518895ad75149cfdfdac4cd512dd6062becba04b2ed0`; seed/config explicit in tests; no data/model/environment identity | `APPROVED_TO_IMPLEMENT` -> `41 TARGETED TESTS PASSED` | schema/visibility/group/split/leakage/attack/hard-negative/intervention/manifest infrastructure and 24-record synthetic fixture | allowed: engineering feasibility only；prohibited: Benchmark/Detector/performance/Paper result | blocker none in approved scope；next_gate owner reviews PILOT0 evidence |
| RUN-P1-PILOT1-PUBLIC-SOURCE | S6.1-P1 / PILOT1 | engineering_validation / 本机 | `COMPLETED_PENDING_REVIEW / REAL_PUBLIC_SOURCE_FEASIBILITY_ONLY` | base commit `c555e7da4e5593f72cbf062823feda6bc7798e58`; 24 source SHA pairs in Git-external manifest; no model/environment identity | `PILOT0 HUMAN_ACCEPTED / PILOT1 APPROVED_TO_START` -> `PILOT1-A 15/15 PASS` | 12 chains / 3 domains / 24 HASH_ONLY sources；36 non-adjudicated candidates；12 HKP×S cells；12 matched hard negatives；2 blinded 36-row packets；evidence index `17/17 PASS` | allowed: real public-source/schema/packet feasibility；prohibited: Benchmark/annotation agreement/Detector/effectiveness/Paper result | blocker none in approved scope；next_gate owner reviews sources and packets |
| ART-P1-PILOT2-KIT | S6.1-P1 / PILOT2-KIT | artifact_preparation / 本机 | `ANNOTATION_KIT_PREPARED_PENDING_HUMAN_EXECUTION` | base `74b9afa954af56c5286c2fd4449281184ecce2fe`; Pilot1 summary `4952f166...ea6`; source index `17/17`; no model/environment identity | `PILOT1 HUMAN_ACCEPTED / PILOT2 APPROVED` -> `KIT VALIDATION 15/15 PASS` | A/B Phase 1+2 ZIP、6 synthetic practices、coordinator/owner-only controls；outer ZIP `a3c884ba...6463` | allowed: distributable kit identity only；prohibited: annotation/IAA/adjudication/Dataset/Detector/result | next_gate training + A/B Phase 1；lock both SHA before Phase 2 |
| GOV-P1-PILOT2-RETURN-CORRECTION-01 | S6.1-P1 / PILOT2 Return Correction | governance_correction / 本机 | `OWNER_CORRECTION_REGISTERED / AUTO_CONTINUE_NO` | base `561750c6fc5706582dc547cc000271b981abed85`; raw returns and original preflight preserved | timestamp-based blind-contamination inference -> `SUPERSEDED_BY_OWNER_CONFIRMED_ACTUAL_DISTRIBUTION_ORDER` | PODR-063/OR-025；artifact `../s6_1_p1_pilot2_return_owner_correction.md` | allowed: corrected order and blocker interpretation；prohibited: agreement/adjudication/raw mutation/result | blocker `PROTOCOL_AND_ANNOTATION_SCHEMA_BLOCKER`; next_gate Schema V2 + A/B re-review approval |
| ART-P1-PILOT2-ANNOTATION-V2 | S6.1-P1 / PILOT2 Annotation V2 | artifact_preparation / 本机 | `SCHEMA_V2_IMPLEMENTED / A_B_REREVIEW_READY` | raw return SHA `4/4` unchanged；preflight `adeb4586...bae0` unchanged；no model/environment identity | `APPROVED_TO_IMPLEMENT` -> `15 ARTIFACT/SCHEMA TESTS PASSED` | four isolated V2 ZIPs `0a896226...08a0` / `e3f7127b...f46e` / `3391ffc7...ddf5` / `74390b5c...f626`；artifact `../s6_1_p1_pilot2_annotation_v2.md` | allowed: schema/package readiness；prohibited: agreement/adjudication/Dataset/Detector/result | blocker `SCHEMA_REMEDIATION_IN_PROGRESS_UNTIL_HUMAN_RETURN`; next_gate A/B human V2 then separate validation/agreement approval |

## Artifact Registry

| artifact_id | identity | size / index | status |
| --- | --- | --- | --- |
| ART-C02 | Correction 02 archive SHA256 `fcfa3f14c98e0103cb5a1de2f0449fa000d179e2e01d74baa6fec4b013503622` | 17/17 PASS | evidence closure accepted |
| ART-H1 | `s6_1_r0_fu1_w2_models_20260801.tar.gz`, SHA256 `aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45` | 1222137698 bytes; 19/19 PASS | 本机 prepared; 5090 H2-A verified |
| ART-H2-R01 | `s6_1_r0_fu1_w2_resume01_evidence_20260801.tar.gz`, SHA256 `941557aa00be58210015165078bbb3c1cbdd2250cab0755c37198e7b7e26e89d` | 4570 bytes; evidence 19/19 PASS | 本机 accepted valid blocker evidence; immutable |
| ART-H2-R02 | `s6_1_r0_fu1_w2_resume02_evidence_20260801.tar.gz`, SHA256 `58da856a81ad89b858af2c041ff617e16156ec254410b07e6511c2888203f563` | 15625 bytes; evidence 25/25 PASS | Control Plane accepted engineering-smoke evidence |
| MODEL-ENC | `facebook/contriever-msmarco@abe8c1493371369031bcb1e02acb754cf4e162fa` | 8 files; 438708922 bytes | 5090 local CUDA load passed in frozen H2 |
| MODEL-MLM | `google-bert/bert-base-uncased@86b5e0934494bd15c9632b12f734a8a67f723594` | 9 files; 881643453 bytes | 5090 local CUDA load passed in frozen H2 |

Total model bytes: `1320352375`. Archives and models remain Git-external.

H2 bundle contract additionally freezes bundle source bytes `1320359518`, archive size `1222137698`, archive SHA256 `aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45`, and model index `19/19`. H2-A failure MUST terminate H2 and MUST NOT transition to H2-B.

## Evidence Map

| claim | authoritative evidence |
| --- | --- |
| LR1 acceptance | owner decision register + `S6.1-LR1_work_process.md` |
| R0 corrected acceptance | R0 review + corrected archive + `S6.1-R0_work_process.md` |
| W2 blocked run | W2 control-plane review + original/correction evidence |
| Correction 02 closure | SHA256 and 17/17 index in FU1 process and experiment master record |
| H1 prepared and 5090 verified | H1 manifest/index, SHA256, immutable model revisions and H2-A evidence |
| H2 approval and conditional execution | owner requirements OR-017/OR-018 + PODR-059/PODR-060 + `S6.1-R0-FU1_work_process.md` |
| H2 resume_01 blocker | returned archive SHA256 `941557aa...26e89d`, safe 20 files/1 directory, evidence index 19/19, `call_count=0` |
| H2 resume_02 review | returned archive SHA256 `58da856a...f563`, safe 27 files/1 directory, evidence index 25/25, H2-A 18/18, `call_count=1` |
| W2/FU1 final acceptance | PODR-061 + OR-020 + acceptance base `b19fc59...a7d` + immutable H2 resume_02 evidence |
| P1 protocol candidate | `../s6_1_p1_protocol_candidate.md`; non-authoritative, not approved, not started |
| P1-R1 protocol hardening candidate | `../s6_1_p1_r1_protocol_review_candidate.md`; Option B frozen at scope level; non-authoritative, not approved, not started |
| Option B scope authority | OR-021 + PODR-062；detection and lightweight retrieval intervention only |
| PILOT2 owner correction | PODR-063/OR-025 + `../s6_1_p1_pilot2_return_owner_correction.md`；raw/preflight history preserved |
| PILOT2 Annotation V2 | PODR-064/OR-026 + `../s6_1_p1_pilot2_annotation_v2.md`；four isolated ZIP hashes and `15 passed` artifact/schema validation |

## Claims Matrix

| category | current claim |
| --- | --- |
| Published Result | external paper statements only; not verified on 本机 as reproduction |
| Reproduced Result | none for complete strict external baseline reproduction |
| Engineering Validation | identities, schema, environment contracts, evidence closure and accepted exact two-document H2 smoke；W2/FU1 closed for engineering feasibility only |
| Our Formal Result | `NONE`; `FORMAL_EXPERIMENT = NOT STARTED` |

## Open Blockers

- S6.1-P1-R1 is `HUMAN_ACCEPTED_AS_PROTOCOL_FRAMEWORK`; numeric parameters and the formal protocol remain unfrozen.
- PILOT0 is `HUMAN_ACCEPTED / ENGINEERING_INFRASTRUCTURE_ONLY / CLOSED`；PILOT1 is `HUMAN_ACCEPTED / REAL_PUBLIC_SOURCE_AND_PACKET_FEASIBILITY_ONLY / CLOSED`.
- PILOT2 Round1 raw is preserved；blindness subissue is resolved by owner-confirmed actual order；registration error is documented
  and evidence-bound；Annotation Schema V2 and four isolated re-review packages are implemented. Human V2 returns, agreement and
  adjudication are not established. 240-group Pilot is not approved；Dataset is not frozen；Detector is not implemented；Training
  and Formal Experiment are not started.
- Option B is confirmed only for detection plus lightweight hard filtering / soft downweighting. Complete trusted retrieval/context construction remains excluded.

## Resolved Blockers

- R0 initial evidence mismatch: resolved by corrected R0 evidence, with history preserved.
- W2 Attempt 1 evidence gap: `RESOLVED_BY_CORRECTION_02_CONTROL_PLANE_REVIEW`; this did not resolve the model download blocker or complete W2.
- Minimal detector-core feasibility blocker: `RESOLVED_BY_H2_RESUME02_AND_OWNER_ACCEPTANCE`; this does not establish reproduction, effectiveness or strict comparison.

## Decision Gates

1. Preserve resume_01 and resume_02 as immutable evidence; do not overwrite, rerun, merge or create automatic resume_03.
2. The only authorized H2-B call is consumed (`call_count=1`); no retry or second call is authorized.
3. PILOT2 original kit/returns/registration/preflight remain immutable. Schema V2 package preparation is complete；next gate is A/B
   independent human V2 re-review and hash-lock, followed by separate owner approval for validation/agreement.
4. `DETOXIFICATION_OPTION = OPTION_B` is fixed. This does not authorize real data, annotation Pilot, dataset freeze, Detector, training or a formal run；every later gate remains separate.
5. `Auto Continue = CONSUMED_AND_STOPPED`; outside H2 it remains `NO`.

## Human-Confirmed Requirements Reference

Canonical authority: [`../human/owner_requirement_register.md`](../human/owner_requirement_register.md). This ledger may mirror but cannot add confirmed requirements.

## Research Plan Reference

Canonical authority: [`../human/research_plan_authority.md`](../human/research_plan_authority.md). Historical route: [`../paper1_research_route.md`](../paper1_research_route.md).

## Stage Process Map

- [`S6.1-LR1`](../stage_process/S6.1-LR1_work_process.md)
- [`S6.1-R0`](../stage_process/S6.1-R0_work_process.md)
- [`S6.1-R0-FU1`](../stage_process/S6.1-R0-FU1_work_process.md)
- [`S6.1-P1`](../stage_process/S6.1-P1_work_process.md)

## Canonical File Map

| information | canonical file |
| --- | --- |
| owner-confirmed requirements | `../human/owner_requirement_register.md` |
| current research plan | `../human/research_plan_authority.md` |
| human summary | `../human/experiment_ledger_tingfeng.md` |
| structured agent mirror | this file |
| context recovery | `llm_context_archive.md` |
| stage history | `../stage_process/<Stage-ID>_work_process.md` |
| raw evidence registry | `../../../governance/experiment_master_record.md` + Git-external archives |
| project audit timeline | `../../../governance/research_execution_log.md` |

## Recovery Procedure

1. Verify live branch, HEAD, upstream, ahead/behind and worktree; dynamic Git facts override this snapshot.
2. Read owner requirements, research plan, then the human ledger.
3. Read the current stage process and its evidence review; verify hashes against raw evidence.
4. Compare Current State Snapshot with governance current state and experiment master record; fail closed on conflict.
5. Do not infer approval from a plan, chat suggestion, prepared artifact or engineering smoke.
6. Stop at the next human decision gate.
