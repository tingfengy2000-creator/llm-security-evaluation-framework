# Current Work State

## Repository Facts

- Active branch: `feature/stage6-rag`.
- Worktree, HEAD, working-tree state and upstream synchronization are dynamic Git facts. Verify them with `git rev-parse`, `git status --short` and `git rev-list --left-right --count @{upstream}...HEAD` before every task.
- Historical Stage 1-5 assets and Stage 6 fixture data remain immutable. Corrections are additive records, never rewrites of evidence.
- Experiment route, historical runs, metrics and evidence indexes are recorded in `docs/governance/experiment_master_record.md`; this file remains the sole dynamic task and approval-gate source.

## Accepted Baseline

- Last accepted architecture task: `A1R` namespace migration and governance freeze.
- Last accepted stage task: `S6-T5.1 Chunking Contracts`.
- Last accepted commit: `09584c8`.
- Accepted capability boundary: deterministic `ChunkRecord` identity and chunking contracts only; this is not a retriever, context builder, trust policy, LLM integration, or RAG experiment.

## Current Task

- Task ID: `GOV-ER1`.
- Task name: `Experiment Master Record`.
- Status: **Completed, pending human review**.
- Implemented scope: one evidence-backed experiment master record, Stage 1-5 run ledger, Stage 6 engineering-status register, blocker/failed-run/approval registers, handoff guide and governance entrypoint tests.
- S6-T5.2 `Retrieval Runtime Contracts and IDs` remains: **Implemented, pending human acceptance**. Its completed scope is explicit safe query projection, canonical `RetrieverQueryRecord`, deterministic `RetrievalRequest`, `ContentRef`, evidence UID, chunk-level `RetrievalEvidence`, safe evidence summaries, deterministic `RetrievalTrace`, and legacy import/adapter compatibility.
- Audit boundary: ordinary `repr()` and `to_audit_dict()` omit retrieval query text, document plaintext and content-reference expansion. Runtime query objects physically exclude evaluator fields.

## Approval Gate

- Approved and completed: S6-T5.2 implementation and GOV-ER1 documentation governance task only.
- Not approved: `S6-T5.3 DenseRetriever` and every later S6-T5 task.
- Next human approval: review the Experiment Master Record and S6-T5.2 contracts, migration compatibility, label isolation, audit evidence and verification results before separately approving DenseRetriever work.

## Must Not Start

- DenseRetriever, vector-store query orchestration, embedding calls, ContentResolver, ContextBuilder, evidence envelope, citation binding, abstention, Trust policy or retrieval guard.
- Groq, mock/real LLM invocation, evaluator, metrics, T10-T15, formal RAG attack matrix or report generation.
- New Stage 6 business code under `src/codeguarder/`, any mutation of Stage 1-5, or any mutation of Stage 6 data fixtures.

## Current Claims Boundary

Can claim: a deterministic, label-isolated runtime contract boundary has been implemented and tested; historical public loader imports remain compatible through the canonical `llmguard` type.

Cannot claim: retrieval quality, retrieval security effectiveness, context safety, citation accuracy, trustworthiness, RAG metrics, production readiness, or research-experiment outcomes.

## Known Technical Debt

- Historical CRLF/LF hash-baseline false positives remain historical facts; do not rewrite their files to silence checks.
- Dynamic Git state must not be represented as a static assertion in this document.
- S6-T5.3 requires a new explicit approval even though S6-T5.2 contracts are complete.

## Last Update

- Date: `2026-07-20`.
- Updated by: Codex under explicit user approval for GOV-ER1; S6-T5.2 acceptance state was not changed.
