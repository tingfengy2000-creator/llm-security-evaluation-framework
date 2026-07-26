# Current Work State

## Repository Facts

- Active branch: `feature/stage6-rag`.
- Worktree, HEAD, working-tree state and upstream synchronization are dynamic Git facts. Verify them with `git rev-parse`, `git status --short` and `git rev-list --left-right --count @{upstream}...HEAD` before every task.
- Historical Stage 1-5 assets and Stage 6 fixture data remain immutable. Corrections are additive records, never rewrites of evidence.
- Experiment route, historical runs, metrics and evidence indexes are recorded in `docs/governance/experiment_master_record.md`; this file remains the sole dynamic task and approval-gate source.

## Accepted Baseline

- Last accepted architecture task: `A1R` namespace migration and governance freeze.
- Last accepted stage task: `S6-T5.4 Controlled Corpus ContentResolver`.
- Last accepted governance protocol task: `S6-T5.4-P1 Content Resolution Contract and Permission Boundary Freeze`.
- Last accepted implementation commit: `11a72f7`.
- Accepted capability boundary: deterministic, label-isolated provider-neutral DenseRetriever engineering behavior, including the S6-T5.3-H1 trace and failure-boundary hardening. This does not establish retrieval quality, security effectiveness, context safety, trust policy, LLM integration, or a RAG experiment.

## Current Task

- Task ID: `S6-T5.5-P1-H1`.
- Task name: `Evidence Canonical Binding and Citation Rendering Protocol Hardening`.
- Execution status: **Completed, pending human review**. This is a design-freeze hardening record, not a new retrieval capability, implementation approval or a formal RAG security experiment.
- S6-T5.5-P1: **Completed, pending human acceptance**.
- S6-T5.5-P1-H1: Factory only accepts canonical `corpus:` RetrievalEvidence; renderer only accepts Envelope + Binding and fails closed on seven-field mismatch.
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

- Human accepted: GOV-ER1, GOV-ER1-H1, GOV-PODR1, S6-T5.2, S6-T5.3-P1, S6-T5.3-H1, S6-T5.3 DenseRetriever, S6-T5.4-P1, S6-T5.4-I1, S6-T5.4-H1, and S6-T5.4.
- S6-T5.3 human acceptance is limited to its documented offline engineering scope and deterministic test behavior.
- `S6-T5.4` is **HUMAN_ACCEPTED**. This does not approve EvidenceEnvelope, citation, ContextBuilder or S6-T5.5; each remains a separate approval boundary.
- `S6-T5.5-P1` is **Completed, pending human acceptance**. It freezes a no-`citation_id` Envelope, future package-local Binding allocation, deterministic instruction/rendering rules and sensitive-export deny-by-default; it does not implement any of them.
- `S6-T5.5-P1-H1` is **Completed, pending human review**. It clarifies canonical Evidence-only Factory input, single-block renderer input and `CITATION_BINDING_MISMATCH`; it does not implement any of them.
- `S6-T5.5`: **NOT APPROVED**. Every later S6-T5 task is also **NOT APPROVED**.
- Formal RAG security experiment: **Not started**.
- Next human decision: review S6-T5.5-P1-H1, then accept, reject or amend S6-T5.5-P1; only after that may a separately scoped S6-T5.5 implementation be considered. S6-T5.5 remains unapproved.

## Must Not Start

- Additional ContentResolver changes, document-content access beyond synthetic test inputs, EvidenceEnvelope implementation, CitationBinding implementation, rendering, ContextBuilder, abstention, Trust policy or retrieval guard. S6-T5.5-P1 is a design record only; no follow-up implementation is approved.
- Groq, mock/real LLM invocation, evaluator, metrics, T10-T15, formal RAG attack matrix or report generation.
- New Stage 6 business code under `src/codeguarder/`, any mutation of Stage 1-5, or any mutation of Stage 6 data fixtures.

## Current Claims Boundary

Can claim: within the offline engineering-test scope, deterministic and label-isolated retrieval runtime contracts plus the provider-neutral DenseRetriever have been HUMAN_ACCEPTED. S6-T5.4-P1, I1, H1 and S6-T5.4 Controlled Corpus ContentResolver are HUMAN_ACCEPTED: they establish a minimal provider-neutral resolver over synthetic in-memory content, a closed public capability surface, and a redacted injected-error boundary. S6-T5.5-P1 has frozen the future EvidenceEnvelope/Citation time boundary but is still pending human acceptance. Historical public loader imports remain compatible through the canonical `llmguard` type.

Cannot claim: retrieval quality, retrieval security effectiveness, context safety, citation accuracy, trustworthiness, RAG metrics, production readiness, or research-experiment outcomes.

## Known Technical Debt

- Historical CRLF/LF hash-baseline false positives remain historical facts; do not rewrite their files to silence checks.
- Dynamic Git state must not be represented as a static assertion in this document.
- S6-T5.3 must preserve all frozen contracts; any need to change them is a `DESIGN_OR_PROTOCOL_BLOCKER`.
- Resolved protocol record: the former hit boundary lacked `parent_doc_id`; schema `1.1` now carries it through the public metadata contract without changing legacy schema `1.0`. See [S6-T5.3 blocker record](s6_t5_3_protocol_blocker_record.md).

## Last Update

- Date: `2026-07-25`.
- Updated by: Codex under explicit project-owner design-review hardening approval. S6-T5.4-P1, I1, H1 and parent S6-T5.4 remain HUMAN_ACCEPTED. S6-T5.5-P1 remains Completed, pending human acceptance; S6-T5.5-P1-H1 is Completed, pending human review; S6-T5.5 and later tasks are Not approved. No source/data change, model call or formal RAG security experiment occurred.
