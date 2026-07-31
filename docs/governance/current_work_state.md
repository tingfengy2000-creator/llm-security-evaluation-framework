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

- Task ID: `S6.1-R0`.
- Task name: `Paper 1 Reproduction Environment and Baseline Feasibility Validation`.
- Task type: **ENGINEERING_VALIDATION / REPRODUCTION_PREFLIGHT**.
- Status: **APPROVED_TO_START**.
- Execution machine: **RTX5090 / COMPUTE_WORKER**.
- Current ordered step: **R0-A Environment Fingerprint** after Worker pulls the latest Control Plane commit.
- Historical superseded snapshot: `DEFINED / NOT STARTED / PENDING OWNER EXECUTION APPROVAL`.
- Formal RAG security experiment: **NOT STARTED**.
- Canonical formal status: `FORMAL_EXPERIMENT = NOT STARTED`.
- Git-Native Research Context Recovery Governance: **HUMAN_ACCEPTED**.
- Paper-First Comparative Evidence Principle: **HUMAN_ACCEPTED**.
- Paper 1 canonical research route: **ACCEPTED AS CURRENT RESEARCH ROUTE**.
- RTX5090 Compute Worker Bootstrap: **HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY**.
- S6.1-R0: **APPROVED_TO_START**.
- S6.1-P1: **NOT STARTED / DEFERRED UNTIL R0 REVIEW**.
- Dataset Generation: **NOT APPROVED**.
- Detector Implementation: **NOT APPROVED**.
- Model Training: **NOT APPROVED**.
- Current blocker for starting R0-A after Worker sync: **NONE**. `BLK-S6.1-LR1-001` remains **OPEN** only for future strict
  reproduction/comparison eligibility because paper-result commits, revisions, baseline compatibility and baseline-specific resources remain incomplete;
  unconfirmed redistribution licenses do not by themselves block separately approved internal research execution.
- Environment observation: missing NumPy in `llmguard-paper1` is
  `NON_BLOCKING_ENVIRONMENT_COMPLETENESS_OBSERVATION`, not GPU/CUDA/PyTorch failure; R0-A may install and fingerprint its
  resolved version.
- LOCAL Control Plane did not run PoisonedRAG, GMTP or SafeRAG and did not download data/model or invoke an API.
- Canonical entry: [Stage 6.1 research README](../research/stage6_1_hidden_knowledge_poisoning/README.md).
- Canonical Paper 1 route: [Paper 1 Research Route](../research/stage6_1_hidden_knowledge_poisoning/paper1_research_route.md).
- Context recovery entry: [Context Authority Map](context_authority_map.md).

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
- `S6.1-R0 EXECUTION` is approved on RTX5090 under the canonical R0 order and stop conditions. The former pending-approval
  state is a superseded historical snapshot.
- Next operational action: RTX5090 pulls the latest Control Plane commit and begins R0-A. Next research gate: R0-I Control Plane
  Review. S6.1-P1, Detector, training and formal experiment remain separately gated.
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

- On LOCAL: any S6.1-R0 execution, external repo clone/install/smoke, dataset/model download or GPU computation.
- On RTX5090: out-of-order R0 work, all-three-repos-in-one-environment installation, full NQ/HotpotQA/MS MARCO or production
  indexes without `MINIMUM_DATA_REQUIREMENT` review, paid API/API key, unapproved large LLM download, silent algorithm change.
- Everywhere: S6.1-P1, Detector implementation, training, Paper Result, formal experiment or SOTA comparison.
- Additional ContentResolver changes, document-content access beyond synthetic test inputs, Trust policy, retrieval guard, or any S6-T5.8 behavior beyond the completed documentation closure.
- Groq, mock/real LLM invocation, evaluator, metrics, T10-T15, formal RAG attack matrix or report generation.
- New Stage 6 business code under `src/codeguarder/`, any mutation of Stage 1-5, or any mutation of Stage 6 data fixtures.

## Current Claims Boundary

Can additionally claim: S6.1-LR1, Context Recovery Governance and Paper-First are accepted；RTX5090 Bootstrap is
`HUMAN_ACCEPTED / RTX5090_BOOTSTRAP_READY` for WSL GPU、PyTorch cu130、FP16/BF16 basic tensor computation and Git
context sync；S6.1-R0 is `APPROVED_TO_START` on the Compute Worker.

Can claim: within the offline engineering-test scope, the `S6-T5 Controlled Retrieval and Traceable Context Baseline` is HUMAN_ACCEPTED. It comprises deterministic and label-isolated retrieval runtime contracts, provider-neutral DenseRetriever, the synthetic ContentResolver, EvidenceEnvelope/Citation boundaries, deterministic Context Package behavior, and S6-T5.7 controlled integration evidence including an opt-in fixed MiniLM plus temporary Chroma close/reopen check. `4ecf73a` is the accepted baseline content commit; the current governance acceptance commit is not an implementation or integration-evidence commit. Historical public loader imports remain compatible through the canonical `llmguard` type.

Cannot claim: any external baseline was reproduced；RTX5090 paper-level performance was benchmarked；dataset/Detector/Our
Method/training/result exists；or retrieval quality/security, SOTA, production readiness or formal-experiment outcomes are established.

## Known Technical Debt

- Historical CRLF/LF hash-baseline false positives remain historical facts; do not rewrite their files to silence checks.
- Dynamic Git state must not be represented as a static assertion in this document.
- S6-T5.3 must preserve all frozen contracts; any need to change them is a `DESIGN_OR_PROTOCOL_BLOCKER`.
- Resolved protocol record: the former hit boundary lacked `parent_doc_id`; schema `1.1` now carries it through the public metadata contract without changing legacy schema `1.0`. See [S6-T5.3 blocker record](s6_t5_3_protocol_blocker_record.md).

## Last Update

- Date: `2026-07-31`.
- Updated by: Codex recording RTX5090 Bootstrap human acceptance and project-owner approval for Worker-only S6.1-R0 execution.
  LOCAL remains governance-only; Formal Experiment remains not started.
