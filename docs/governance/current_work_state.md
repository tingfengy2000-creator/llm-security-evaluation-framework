# Current Work State

## Repository Facts

- Active branch: `feature/stage6-rag`.
- Worktree, HEAD, working-tree state and upstream synchronization are dynamic Git facts. Verify them with `git rev-parse`, `git status --short` and `git rev-list --left-right --count @{upstream}...HEAD` before every task.
- Historical Stage 1-5 assets and Stage 6 fixture data remain immutable. Corrections are additive records, never rewrites of evidence.
- Experiment route, historical runs, metrics and evidence indexes are recorded in `docs/governance/experiment_master_record.md`; this file remains the sole dynamic task and approval-gate source.

## Accepted Baseline

- Last accepted architecture task: `A1R` namespace migration and governance freeze.
- Last accepted stage task: `S6-T5.2 Retrieval Runtime Contracts and IDs`.
- Last accepted implementation commit: `4c12181`.
- Accepted capability boundary: deterministic chunking plus label-isolated retrieval runtime contracts and IDs; this is not yet a retriever, context builder, trust policy, LLM integration, or RAG experiment.

## Current Task

- Task ID: `S6-T5.3`.
- Task name: `Provider-Neutral DenseRetriever`.
- Status: **Blocked: DESIGN_OR_PROTOCOL_BLOCKER**.
- GOV-ER1: **HUMAN_ACCEPTED**.
- GOV-ER1-H1: **HUMAN_ACCEPTED**.
- S6-T5.2 `Retrieval Runtime Contracts and IDs`: **HUMAN_ACCEPTED**. Its completed scope is explicit safe query projection, canonical `RetrieverQueryRecord`, deterministic `RetrievalRequest`, `ContentRef`, evidence UID, chunk-level `RetrievalEvidence`, safe evidence summaries, deterministic `RetrievalTrace`, and legacy import/adapter compatibility.
- Approval fact: S6-T5.3 was approved to start, but implementation is paused before code is written because the frozen hit-to-evidence identity contract is incomplete.
- Blocker: `VectorSearchHit` and its public metadata whitelist do not expose the canonical `RetrievalEvidence.parent_doc_id` required to construct a safe evidence record. DenseRetriever may not read the corpus, invent parent identity, or weaken frozen contracts.
- Audit boundary: ordinary `repr()` and `to_audit_dict()` omit retrieval query text, document plaintext and content-reference expansion. Runtime query objects physically exclude evaluator fields.

## Approval Gate

- Human accepted: GOV-ER1, GOV-ER1-H1, and S6-T5.2.
- Approved but blocked: `S6-T5.3 DenseRetriever` (`DESIGN_OR_PROTOCOL_BLOCKER`).
- Not approved: `S6-T5.4 ContentResolver` and every later S6-T5 task.
- Next human decision: approve a safe, public, non-label carrier for parent-document identity in the hit-to-evidence contract, then restart S6-T5.3 from Red tests. S6-T5.4 remains separately unapproved.

## Must Not Start

- DenseRetriever implementation until the `parent_doc_id` protocol gap is resolved; ContentResolver, document-content access, ContextBuilder, evidence envelope, citation binding, abstention, Trust policy or retrieval guard.
- Groq, mock/real LLM invocation, evaluator, metrics, T10-T15, formal RAG attack matrix or report generation.
- New Stage 6 business code under `src/codeguarder/`, any mutation of Stage 1-5, or any mutation of Stage 6 data fixtures.

## Current Claims Boundary

Can claim: deterministic, label-isolated retrieval runtime contracts have been implemented and accepted; `S6-T5.3` was approved and correctly paused at a protocol blocker before unsafe implementation. Historical public loader imports remain compatible through the canonical `llmguard` type.

Cannot claim: retrieval quality, retrieval security effectiveness, context safety, citation accuracy, trustworthiness, RAG metrics, production readiness, or research-experiment outcomes.

## Known Technical Debt

- Historical CRLF/LF hash-baseline false positives remain historical facts; do not rewrite their files to silence checks.
- Dynamic Git state must not be represented as a static assertion in this document.
- S6-T5.3 must preserve all frozen contracts; any need to change them is a `DESIGN_OR_PROTOCOL_BLOCKER`.
- `DESIGN_OR_PROTOCOL_BLOCKER`: the frozen VectorStore hit boundary lacks `parent_doc_id`, while canonical `RetrievalEvidence` requires it. See [S6-T5.3 blocker record](s6_t5_3_protocol_blocker_record.md).

## Last Update

- Date: `2026-07-21`.
- Updated by: Codex under explicit project-owner approval. GOV-ER1, GOV-ER1-H1 and S6-T5.2 were accepted; S6-T5.3 was approved to start and then paused before implementation after a contract-level identity gap was verified.
