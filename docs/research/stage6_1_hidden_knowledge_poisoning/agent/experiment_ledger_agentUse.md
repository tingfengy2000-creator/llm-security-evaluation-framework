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
document_source_commit: 2f492dc763e865105510cc8cb141ebde5e109b3e
snapshot_date: 2026-08-01
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
S6.1-R0-FU1-W2-H1: OFFLINE_MODEL_ARTIFACTS_PREPARED_PENDING_5090_VERIFICATION
S6.1-R0-FU1-W2-H2-RESUME-01: VALID_BLOCKED_EVIDENCE / OFFLINE_BUNDLE_SHA_BLOCKER / H2-B NOT EXECUTED / call_count=0
S6.1-R0-FU1-W2-H2-RESUME-02: APPROVED_TO_START / NOT EXECUTED
S6.1-R0-FU1-W2: APPROVED_TO_START / NOT COMPLETED / NOT ACCEPTED
S6.1-P1: NOT STARTED
Dataset: NOT FROZEN
Detector: NOT IMPLEMENTED
Training: NOT STARTED
Our_Method_Result: NONE
Formal_Experiment: NOT STARTED
H2_historical_preapproval: PROPOSED / NOT CANONICAL / NOT APPROVED
H2_auto_continue: CONDITIONAL_WITHIN_H2_ONLY
```

## State Machine

`LR1 HUMAN_ACCEPTED -> R0 HUMAN_ACCEPTED_WITH_BLOCKERS -> FU1 {P0 HUMAN_ACCEPTED, L1 HUMAN_ACCEPTED, W2 INCOMPLETE} -> H1 prepared -> H2 resume_01 OFFLINE_BUNDLE_SHA_BLOCKER/call_count=0 -> bundle synced + immutable evidence conflict -> resume_02 owner-approved -> H2-A PASS ? exactly one H2-B call : STOP -> 本机 review`

No transition authorizes S6.1-P1, Dataset Construction, Detector Implementation, Training, or Formal Experiment.

## Stage Registry

| stage_id | purpose | current_status | canonical_process |
| --- | --- | --- | --- |
| S6.1-LR1 | research route and external baseline alignment | `HUMAN_ACCEPTED` | `../stage_process/S6.1-LR1_work_process.md` |
| S6.1-R0 | engineering reproduction preflight | `HUMAN_ACCEPTED_WITH_BLOCKERS` | `../stage_process/S6.1-R0_work_process.md` |
| S6.1-R0-FU1 | targeted baseline feasibility resolution | `H2 RESUME_02 APPROVED / NOT EXECUTED` | `../stage_process/S6.1-R0-FU1_work_process.md` |
| S6.1-P1 | formal protocol freeze | `NOT STARTED` | none; not approved |

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

## Artifact Registry

| artifact_id | identity | size / index | status |
| --- | --- | --- | --- |
| ART-C02 | Correction 02 archive SHA256 `fcfa3f14c98e0103cb5a1de2f0449fa000d179e2e01d74baa6fec4b013503622` | 17/17 PASS | evidence closure accepted |
| ART-H1 | `s6_1_r0_fu1_w2_models_20260801.tar.gz`, SHA256 `aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45` | 1222137698 bytes; 19/19 PASS | 本机 prepared; 5090 verification pending |
| ART-H2-R01 | `s6_1_r0_fu1_w2_resume01_evidence_20260801.tar.gz`, SHA256 `941557aa00be58210015165078bbb3c1cbdd2250cab0755c37198e7b7e26e89d` | 4570 bytes; evidence 19/19 PASS | 本机 accepted valid blocker evidence; immutable |
| MODEL-ENC | `facebook/contriever-msmarco@abe8c1493371369031bcb1e02acb754cf4e162fa` | 8 files; 438708922 bytes | bundled, not loaded on 5090 |
| MODEL-MLM | `google-bert/bert-base-uncased@86b5e0934494bd15c9632b12f734a8a67f723594` | 9 files; 881643453 bytes | bundled, not loaded on 5090 |

Total model bytes: `1320352375`. Archives and models remain Git-external.

H2 bundle contract additionally freezes bundle source bytes `1320359518`, archive size `1222137698`, archive SHA256 `aa06e4cd03cb4d1eeb008514d81bc4d41e98f88614df046e008ac1f1544def45`, and model index `19/19`. H2-A failure MUST terminate H2 and MUST NOT transition to H2-B.

## Evidence Map

| claim | authoritative evidence |
| --- | --- |
| LR1 acceptance | owner decision register + `S6.1-LR1_work_process.md` |
| R0 corrected acceptance | R0 review + corrected archive + `S6.1-R0_work_process.md` |
| W2 blocked run | W2 control-plane review + original/correction evidence |
| Correction 02 closure | SHA256 and 17/17 index in FU1 process and experiment master record |
| H1 prepared only | H1 manifest/index, SHA256, immutable model revisions |
| H2 approval and conditional execution | owner requirements OR-017/OR-018 + PODR-059/PODR-060 + `S6.1-R0-FU1_work_process.md` |
| H2 resume_01 blocker | returned archive SHA256 `941557aa...26e89d`, safe 20 files/1 directory, evidence index 19/19, `call_count=0` |
| H2 resume_02 rollover | owner-confirmed bundle sync and additive namespace approval; execution evidence pending |

## Claims Matrix

| category | current claim |
| --- | --- |
| Published Result | external paper statements only; not verified on 本机 as reproduction |
| Reproduced Result | none for complete strict external baseline reproduction |
| Engineering Validation | identities, schema, environment contracts, evidence closure, 本机 bundle, blocked smoke |
| Our Formal Result | `NONE`; `FORMAL_EXPERIMENT = NOT STARTED` |

## Open Blockers

- Bundle/sidecar presence and outer size/SHA are reported on 5090, but full H2-A and model identity verification are still pending.
- H2 resume_02 is approved but not executed; H2-B has never executed and call_count remains zero.
- GMTP detection-core has not completed; parent W2 remains incomplete and unaccepted.
- S6.1-P1 protocol, Dataset, Detector, Training and Formal Experiment are not approved or started.
- Detoxification technical scope remains `SCOPE_CONFIRMATION_REQUIRED`.

## Resolved Blockers

- R0 initial evidence mismatch: resolved by corrected R0 evidence, with history preserved.
- W2 Attempt 1 evidence gap: `RESOLVED_BY_CORRECTION_02_CONTROL_PLANE_REVIEW`; this did not resolve the model download blocker or complete W2.

## Decision Gates

1. Preserve resume_01 as immutable blocker evidence; resume_02 must be absent or empty before execution, otherwise stop without automatic resume_03.
2. H2 resume_02 approval exists only for 5090: verify H2-A from the beginning; any mismatch stops without H2-B.
3. H2-B is conditionally authorized only after complete H2-A pass and is limited to one frozen two-document call.
4. H2-B completion or any blocker stops and returns evidence to 本机; no autonomous repair or repetition.
5. Human acceptance of W2 is still required before any S6.1-P1 proposal can advance.
6. Separate owner confirmation remains required for detoxification scope and every formal experiment gate.
7. `Auto Continue = CONDITIONAL_WITHIN_H2_ONLY`; outside H2 it is `NO`.

## Human-Confirmed Requirements Reference

Canonical authority: [`../human/owner_requirement_register.md`](../human/owner_requirement_register.md). This ledger may mirror but cannot add confirmed requirements.

## Research Plan Reference

Canonical authority: [`../human/research_plan_authority.md`](../human/research_plan_authority.md). Historical route: [`../paper1_research_route.md`](../paper1_research_route.md).

## Stage Process Map

- [`S6.1-LR1`](../stage_process/S6.1-LR1_work_process.md)
- [`S6.1-R0`](../stage_process/S6.1-R0_work_process.md)
- [`S6.1-R0-FU1`](../stage_process/S6.1-R0-FU1_work_process.md)

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
