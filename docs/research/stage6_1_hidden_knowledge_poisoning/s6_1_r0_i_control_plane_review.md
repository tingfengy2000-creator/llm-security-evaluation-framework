# S6.1-R0-I Control Plane Review

## Superseding Corrected-Evidence Decision — 2026-07-31

- Task: `S6.1-R0-I / Control Plane Review`
- Machine: `LOCAL / CONTROL_PLANE`
- Decision: `S6.1-R0 = HUMAN_ACCEPTED_WITH_BLOCKERS`
- Task type remains: `ENGINEERING_VALIDATION / REPRODUCTION_PREFLIGHT`
- `S6.1-R0-I = HUMAN_ACCEPTED_WITH_BLOCKERS`
- `R0-FU1 = APPROVAL_RECOMMENDED / NOT APPROVED`
- `S6.1-P1 = NOT STARTED`
- `FORMAL_EXPERIMENT = NOT STARTED`
- Dataset: `NOT FROZEN`; Detector: `NOT IMPLEMENTED`; Training: `NOT STARTED`; Our Method Result: `NONE`

This supersedes the current-state effect of the historical first-review decision below without deleting or rewriting that
`RETURNED_FOR_WORKER_CORRECTION` snapshot. `WITH_BLOCKERS` means the R0 engineering-preflight objective is complete and its
remaining external-baseline decisions are now auditable. It does not mean any baseline was reproduced or that strict comparison
is ready.

### Corrected Evidence Integrity

- Private corrected archive SHA-256:
  `904d79c59e35c6aeb157540049b0f44262b86e5c1c5b3e8d4e96ee2fad3f1c6b`.
- External sidecar and actual archive digest matched exactly.
- Archive layout: 39 safe entries; no absolute path, traversal component, symlink or hardlink.
- Corrected inner index: `12/12` files verified.
- Corrected feasibility matrix SHA-256:
  `fd7617eca689fa46fc6908f94aa4fa158aaae4d277bb17943bbcc1baf74db9bc`.
- The raw corrected archive, external source repositories and complete Worker logs remain private LOCAL evidence outside Git.

### Corrected Baseline Verification

| Baseline | Corrected command-derived finding | Final R0 qualification |
| --- | --- | --- |
| PoisonedRAG | official commit `f660d72174f06b13fae5163ce656e7b235db858f`; NQ, HotpotQA or MS MARCO can be selected individually; a custom BEIR-format path and named result artifacts exist; `API_FREE_ATTACK_GENERATION = NOT ESTABLISHED` | `ENGINEERING_FEASIBILITY_IDENTIFIED / P1_PROTOCOL_BLOCKED`; `NOT_STRICT_COMPARISON_READY` |
| GMTP | official commit `15b48d150f93711371eb8da22c211cd84a0cf4df`; mode-160000 `beir` gitlink `f062f038c4bfd19a8ca942a9910b1e0d218759d4`; root `.gitmodules` absent; 18 `*-200.json` artifacts available; Docker is `RECOMMENDED_CONVENIENCE_ENVIRONMENT`; detection-only and generation/end-to-end dependencies are separated | `ENGINEERING_FEASIBILITY_IDENTIFIED / TARGETED_EXECUTION_BLOCKERS_REMAIN`; `NOT_STRICT_COMPARISON_READY` |
| SafeRAG | official commit `e8f579743b23e0a3937076dcc0792fe29027cba3`; pre/post/executed script SHA-256 all equal `8a38c9f54b963703ae3279f36f53c49083fd76b0f7e96ea27707b728b915db7e`; exact timed command bound that script; SN `100/100` and ICC `93/93` all-record required-key validation passed; exit `0`, wall `0.02 s`, Max RSS `17,628 KiB` | `PARTIAL_REPRODUCTION_READY / DATASET_ARTIFACT_ONLY`; `BENCHMARK_ARTIFACT_AVAILABLE`; full pipeline `NOT_STRICT_COMPARISON_READY` |

The former phrase `advertised samples absent` remains below only as a quoted historical false claim and correction rationale. It
is not a current GMTP fact or blocker. Docker is not mandatory. SafeRAG remains only
`ENGINEERING_DATASET_SMOKE_RESULT_ONLY / DATASET_ARTIFACT_ONLY`; neither its pipeline nor benchmark result was reproduced.

### Normalized Remaining Blockers After R0 Acceptance

| Class | Items |
| --- | --- |
| `P1_PROTOCOL_BLOCKER` | PoisonedRAG external dataset choice and attack-generation identity; GMTP modified-BEIR source identity and exact detection-only comparison path |
| `FORMAL_EXPERIMENT_ENVIRONMENT_BLOCKER` | GMTP Java/Pyserini/FAISS compatibility; selected local/API generator path and any ultimately selected model/service requirements |
| `REDISTRIBUTION_ONLY_ISSUE` | GMTP/SafeRAG license uncertainty; explicit upstream terms still govern |
| `NON_BLOCKING` | SafeRAG full-pipeline reproduction when Paper 1 uses only the SN/ICC benchmark artifacts under a frozen usage contract |

### R0-FU1 Recommendation and Stop Gate

`S6.1-R0-FU1 / Targeted External Baseline Feasibility Resolution` is `APPROVAL_RECOMMENDED`, but remains
`NOT APPROVED`. Its proposed scope is narrowly limited to one PoisonedRAG dataset plus attack-generation executable identity,
the GMTP modified-BEIR identity plus detection-only minimal path and necessary Java/Pyserini/FAISS compatibility, and a SafeRAG
benchmark-artifact usage contract. The Control-Plane-First Token Economy Principle remains active: LOCAL prepares the source
analysis and exact execution plan before any short Worker instruction.

No R0-FU1, S6.1-P1, Dataset, Detector, Training or Formal Experiment work starts from this acceptance. The next owner decision is
whether to approve R0-FU1. Auto Continue = NO.

## Historical First Review Identity

- Task: `S6.1-R0-I / Control Plane Review`
- Machine: `LOCAL / CONTROL_PLANE`
- Date: `2026-07-31`
- Decision: `RETURNED_FOR_WORKER_CORRECTION`
- Parent R0 status: `REVIEW_PENDING_CORRECTED_WORKER_EVIDENCE`
- This is not `R0 FAILED` and not `HUMAN_ACCEPTED_WITH_BLOCKERS`.
- `FORMAL_EXPERIMENT = NOT STARTED`
- `S6.1-P1 = NOT STARTED`
- `R0-FU1 = NOT APPROVED`

The engineering-feasibility objective remains valid, and finding blockers is valid R0 evidence. Acceptance is withheld because
the verified archive contains one material upstream-fact mismatch and one smoke-provenance/coverage gap. Baseline roles are not
changed by this return.

## Evidence Integrity

- Private archive SHA-256:
  `0ce85a2bfe24e0456f9d29edc40659786d4273fcfc634df8749aee6d0e3aa9cc`.
- External `.sha256` sidecar: exact match.
- Archive layout: 25 safe entries; no absolute path, traversal component, symlink or hardlink.
- Internal index: `EVIDENCE_INDEX_VERIFIED: 18/18`.
- Component sidecars: R0-A `1/1`；PoisonedRAG `1/1`；GMTP `1/1`；SafeRAG `4/4`.
- Raw archive remains LOCAL private evidence and is not committed to Git. Only this redacted review and digests are persisted.

Hash integrity proves that the reviewed bytes match the delivered archive. It does not by itself prove that hard-coded audit
statements are correct; those statements were cross-checked against the official repositories at the exact commits.

## Main Repository and Environment Evidence

- Worker main repo branch: `research/stage6-1-hidden-poisoning`.
- Worker main repo HEAD: `6f5e23484002681e3e1a6db30c2f2d4cd68499d6`.
- Worker tree evidence: clean; baseline tag peeled to
  `18cf2741c8383d35604715af6ebf8cbaa2a3ddf1`.
- R0-A: Ubuntu 24.04.4 LTS under WSL2；Python 3.11.15；NumPy 2.4.6；PyTorch 2.13.0+cu130；CUDA
  Runtime 13.0；RTX 5090；CUDA available；BF16 supported.
- This fingerprint supports environment identity only. It is not a formal experiment or baseline result.

## Exact Upstream Commit Verification

| Baseline | Role preserved | Exact official commit | Control Plane finding |
| --- | --- | --- | --- |
| PoisonedRAG | `PRIMARY_ATTACK_BASELINE` | `f660d72174f06b13fae5163ce656e7b235db858f` | commit exists; MIT, README environment and result artifacts are present |
| GMTP | `PRIMARY_DETECTION_BASELINE` | `15b48d150f93711371eb8da22c211cd84a0cf4df` | commit exists; `beir` is a gitlink without root `.gitmodules`, but multiple 200-sample JSON artifacts are present |
| SafeRAG | `PRIMARY_BENCHMARK_REFERENCE` | `e8f579743b23e0a3937076dcc0792fe29027cba3` | commit exists; `nctd.json`, SN/ICC knowledge-base artifacts and service/API-dependent pipeline code are present |

Official source links: [PoisonedRAG](https://github.com/sleeepeer/PoisonedRAG/tree/f660d72174f06b13fae5163ce656e7b235db858f),
[GMTP](https://github.com/mountinyy/GMTP/tree/15b48d150f93711371eb8da22c211cd84a0cf4df), and
[SafeRAG](https://github.com/IAAR-Shanghai/SafeRAG/tree/e8f579743b23e0a3937076dcc0792fe29027cba3).

## Material Mismatch and Evidence Gaps

### GMTP artifact contradiction

The Worker matrix and audit report `advertised samples absent`. The official exact-commit tree instead contains
`data/poisoned_documents` with multiple `hotpotqa-200.json`, `msmarco-200.json` and `nq-200.json` artifacts across attack and
retriever combinations. Therefore `advertised samples absent` is not supported and must not remain a blocker.

The `beir` entry is still a mode `160000` gitlink, while the root tree has no `.gitmodules` mapping. That is a narrower missing
source-identity/artifact issue. It may block the official modified-BEIR execution path, but it does not prove that the poisoned
sample artifacts are absent.

The official README says Docker is recommended for Java 21/Pyserini and then gives a native Conda path. Therefore
`Docker is a convenience environment`, not an algorithm requirement. Java/Pyserini/FAISS may still be real environment
dependencies for indexing and detection.

### SafeRAG smoke provenance and coverage

The archive supports exit code 0, SN count 100, ICC count 93, empty stderr, 17,476 KiB maximum RSS, 0.05 s wall time and no
GPU use for the dataset-only script. Its only permissible result is
`ENGINEERING_DATASET_SMOKE_RESULT_ONLY / DATASET_ARTIFACT_ONLY`.

The timed command names a script outside the archived `worker_tools` location, while the evidence index hashes only the copied
script. The executed bytes are therefore `EXECUTED_SCRIPT_HASH_NOT_BOUND`. In addition, the script checks required keys only on
the first record of each task, so it does not support an all-record schema claim.

### PoisonedRAG data/API scope

The official repository supports choosing NQ, HotpotQA or MS MARCO individually and documents a BEIR-format custom-dataset
path. Full acquisition of all three corpora is not automatically a formal-comparison requirement. The Control Plane must choose
one approved external dataset in the future protocol and separately determine whether repo-provided result artifacts can support
an API-free attack-generation path. No data/model/API action is authorized by this review.

## Baseline Decisions

| Baseline | R0 engineering status | Paper 1 role | `STRICT_COMPARISON_ELIGIBILITY` |
| --- | --- | --- | --- |
| PoisonedRAG | `PROVISIONAL_BLOCKED_BY_EXTERNAL_DEPENDENCY / CORRECTION_REQUIRED` | keep `PRIMARY_ATTACK_BASELINE` | `NOT_STRICT_COMPARISON_READY` |
| GMTP | `PROVISIONAL_BLOCKED_BY_MISSING_ARTIFACT / CORRECTION_REQUIRED` limited to the modified-BEIR identity/path | keep `PRIMARY_DETECTION_BASELINE` | `NOT_STRICT_COMPARISON_READY` |
| SafeRAG | `PROVISIONAL_PARTIAL_REPRODUCTION_READY / DATASET_ARTIFACT_ONLY / CORRECTION_REQUIRED` | keep `PRIMARY_BENCHMARK_REFERENCE` | `NOT_STRICT_COMPARISON_READY` |

SafeRAG may later be used as an `EXTERNAL_BENCHMARK_TASK / DATASET REFERENCE` for Silver Noise and Inter-context Conflict.
If its pipeline is not reproduced, publication wording must be “evaluated on SafeRAG benchmark/task”, never “reproduced
SafeRAG”. `SafeRAG Published Result` and `Our Method on SafeRAG Task` remain separate columns.

## Normalized Blockers

| Item | Normalized class | Scope |
| --- | --- | --- |
| PoisonedRAG external dataset choice and attack-generation identity | `P1_PROTOCOL_BLOCKER` | must be frozen before P1; not evidence that all three BEIR corpora are required |
| PoisonedRAG paid API or large local generator path | `FORMAL_EXPERIMENT_BLOCKER` | no API key, paid API or large model is approved |
| GMTP missing mapping for modified `beir` gitlink | `R0_SMOKE_BLOCKER` + `P1_PROTOCOL_BLOCKER` | source identity/execution path must be recovered without reimplementation |
| GMTP Java/Pyserini/FAISS compatibility | `R0_SMOKE_BLOCKER` | Docker itself is not mandatory; native WSL remains possible |
| GMTP 200-sample absence claim | `EVIDENCE_CORRECTION_REQUIRED` | not a real artifact blocker at the audited commit |
| SafeRAG executed-script hash and all-row schema coverage | `R0_SMOKE_BLOCKER` | narrow offline evidence correction only |
| SafeRAG services/API/full pipeline | `FORMAL_EXPERIMENT_BLOCKER` | does not block benchmark-artifact reference use |
| GMTP/SafeRAG missing root license | `REDISTRIBUTION_ONLY_ISSUE` | not an internal research blocker; explicit upstream terms still govern |

## Minimal Worker Correction Task

Only the following correction is requested; no broad environment exploration is authorized:

1. Reissue GMTP audit/matrix from command-derived evidence: record the `beir` gitlink SHA and absent mapping, explicitly record
   `GMTP_200_SAMPLE_ARTIFACTS_PRESENT`, remove the false sample-absence and Docker-required claims, and separate
   detection-only dependencies from generation/API dependencies.
2. Re-run the SafeRAG dataset-only smoke from the archived `worker_tools` path, hash the exact executed script before/after,
   validate required keys for every SN/ICC record, and regenerate its small resource/hash evidence.
3. Add command-derived `git ls-tree`/relevant-file hashes for PoisonedRAG and GMTP so static-audit facts are not supported only by
   hard-coded echo text; state whether PoisonedRAG formal comparison can use one selected external dataset.
4. Regenerate the feasibility matrix, evidence index, archive and external archive SHA-256. Do not install new baseline
   environments, download data/models, call APIs or start formal work.

## R0-FU1 Recommendation

`R0-FU1: RECOMMEND`, but `R0-FU1 = NOT APPROVED`.

Reason: after the narrow evidence correction, Paper 1 still needs a targeted decision on one PoisonedRAG dataset/attack path and
a GMTP detection-only executable path. SafeRAG should remain benchmark-artifact oriented unless scientific comparison later
requires its full pipeline. This recommendation does not authorize execution.

## Claims Boundary and Next Gate

Allowed: archive and internal hashes verified；R0-A fingerprint supported；three official commits verified；SafeRAG dataset-only
smoke bytes exist；material GMTP mismatch and narrow provenance gaps identified；baseline roles preserved.

Prohibited: R0 accepted；any baseline reproduced；strict comparison ready；SafeRAG pipeline ready；Paper Result；Dataset frozen；
Detector implemented；training started；SOTA/security effectiveness；formal experiment started.

Next action: RTX5090 returns only the minimal corrected evidence package. Then LOCAL repeats R0-I evidence verification. The
project owner decides whether to accept R0 and whether to approve the recommended R0-FU1. Auto Continue = NO.
