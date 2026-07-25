# Current Work State

## Repository Facts

- Active branch: `feature/stage6-rag`.
- Worktree, HEAD, working-tree state and upstream synchronization are dynamic Git facts. Verify them with `git rev-parse`, `git status --short` and `git rev-list --left-right --count @{upstream}...HEAD` before every task.
- Historical Stage 1-5 assets and Stage 6 fixture data remain immutable. Corrections are additive records, never rewrites of evidence.
- Experiment route, historical runs, metrics and evidence indexes are recorded in `docs/governance/experiment_master_record.md`; this file remains the sole dynamic task and approval-gate source.

## Accepted Baseline

- Last accepted architecture task: `A1R` namespace migration and governance freeze.
- Last accepted stage task: `S6-T5.3 Provider-Neutral DenseRetriever`.
- Last accepted implementation commit: `72a2445`.
- Accepted capability boundary: deterministic, label-isolated provider-neutral DenseRetriever engineering behavior, including the S6-T5.3-H1 trace and failure-boundary hardening. This does not establish retrieval quality, security effectiveness, context safety, trust policy, LLM integration, or a RAG experiment.

## Current Task

- Task ID: `GOV-S6-T5.3-ACCEPTANCE`.
- Task name: `S6-T5.3 Provider-Neutral DenseRetriever Human Acceptance Record`.
- Status: **Completed under explicit project-owner decision**.
- Scope: record the approved engineering boundary only; it creates no new retrieval capability, does not invoke a model, and does not run a formal RAG security experiment.
- GOV-PODR1: **HUMAN_ACCEPTED**.

## Stage 6 Implementation State

- Task ID: `S6-T5.3`.
- Task name: `Provider-Neutral DenseRetriever`.
- Status: **HUMAN_ACCEPTED**.
- GOV-ER1: **HUMAN_ACCEPTED**.
- GOV-ER1-H1: **HUMAN_ACCEPTED**.
- S6-T5.2 `Retrieval Runtime Contracts and IDs`: **HUMAN_ACCEPTED**. Its completed scope is explicit safe query projection, canonical `RetrieverQueryRecord`, deterministic `RetrievalRequest`, `ContentRef`, evidence UID, chunk-level `RetrievalEvidence`, safe evidence summaries, deterministic `RetrievalTrace`, and legacy import/adapter compatibility.
- S6-T5.3-P1: **HUMAN_ACCEPTED**. Public metadata schema `1.1` carries a validated, non-label, no-body `parent_doc_id` from VectorDocument to VectorSearchHit; schema `1.0` remains legacy-compatible.
- S6-T5.3: **HUMAN_ACCEPTED**. DenseRetriever accepts only schema `1.1` hits, validates request/store provenance, and produces canonical `RetrievalEvidence` plus `RetrievalTrace` without reading the corpus.
- S6-T5.3-H1: **HUMAN_ACCEPTED**. Trace `candidate_count` means raw query hits before sorting/deduplication; store provenance and provider/store failure boundaries fail closed with redacted Retrieval errors.
- Audit boundary: ordinary `repr()` and `to_audit_dict()` omit retrieval query text, document plaintext and content-reference expansion. Runtime query objects physically exclude evaluator fields.

## Approval Gate

- Human accepted: GOV-ER1, GOV-ER1-H1, GOV-PODR1, S6-T5.2, S6-T5.3-P1, S6-T5.3-H1, and S6-T5.3 DenseRetriever.
- S6-T5.3 human acceptance is limited to its documented offline engineering scope and deterministic test behavior.
- Not approved: `S6-T5.4 ContentResolver` and every later S6-T5 task.
- Formal RAG security experiment: **Not started**.
- Next human approval: a new, independent scope approval is required before S6-T5.4. S6-T5.4 remains separately unapproved.

## Must Not Start

- ContentResolver, document-content access, ContextBuilder, evidence envelope, citation binding, abstention, Trust policy or retrieval guard.
- Groq, mock/real LLM invocation, evaluator, metrics, T10-T15, formal RAG attack matrix or report generation.
- New Stage 6 business code under `src/codeguarder/`, any mutation of Stage 1-5, or any mutation of Stage 6 data fixtures.

## Current Claims Boundary

Can claim: within the offline engineering-test scope, deterministic and label-isolated retrieval runtime contracts plus the provider-neutral DenseRetriever have been HUMAN_ACCEPTED. S6-T5.3-P1 repaired the metadata carrier with schema `1.1`; H1 fixed candidate-count semantics and redacted failure boundaries. Historical public loader imports remain compatible through the canonical `llmguard` type.

Cannot claim: retrieval quality, retrieval security effectiveness, context safety, citation accuracy, trustworthiness, RAG metrics, production readiness, or research-experiment outcomes.

## Known Technical Debt

- Historical CRLF/LF hash-baseline false positives remain historical facts; do not rewrite their files to silence checks.
- Dynamic Git state must not be represented as a static assertion in this document.
- S6-T5.3 must preserve all frozen contracts; any need to change them is a `DESIGN_OR_PROTOCOL_BLOCKER`.
- Resolved protocol record: the former hit boundary lacked `parent_doc_id`; schema `1.1` now carries it through the public metadata contract without changing legacy schema `1.0`. See [S6-T5.3 blocker record](s6_t5_3_protocol_blocker_record.md).

## Last Update

- Date: `2026-07-25`.
- Updated by: Codex under explicit project-owner approval. GOV-PODR1, S6-T5.3-P1, S6-T5.3-H1 and S6-T5.3 are HUMAN_ACCEPTED. The historical `parent_doc_id` blocker remains resolved by the versioned public metadata contract; S6-T5.4 and formal RAG security experiments remain unapproved and not started.
