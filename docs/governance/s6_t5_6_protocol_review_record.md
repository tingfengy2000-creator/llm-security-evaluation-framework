# S6-T5.6-P1 Context Package 协议审查与设计冻结记录

## 1. 记录身份与当前状态

- Task ID: `S6-T5.6-P1`
- Task name: `ContextBuilder, Budget, RetrievedContextPackage and Structural Abstention Boundary Freeze`
- Task nature: `DESIGN_FREEZE / PROTOCOL_REVIEW`
- Baseline: `feature/stage6-rag` at `ee905cb`; the last accepted implementation commit remains `6da27a6`.
- Current execution status: `Completed, pending human acceptance`.
- Hardening task: `S6-T5.6-P1-H1 Sequential Resolution, Duplicate Semantics and Context Trace Protocol Hardening`.
- H1 execution status: `Completed, pending human acceptance`.
- Hardening task: `S6-T5.6-P1-H2 Active Specification, Trace Decision and Package Identity Protocol Closure`.
- H2 execution status: `Completed, pending human review`.
- Parent `S6-T5.6`: `NOT APPROVED`.
- `S6-T5.7+`: `NOT APPROVED`.
- Formal RAG security experiment: `NOT STARTED`.

This record freezes a future implementation contract only. It does not create or modify `ContextBuilder`,
`RetrievedContextPackage`, a budgeter, a Citation allocator, or any `src/` code.

## 2. Why This Review Exists

S6-T5.5 established the one-Evidence primitives: a verified `EvidenceEnvelope`, a package-local
`CitationBinding`, a fixed citation instruction, and a renderer that can only render one correctly bound block.
S6-T5.6 must decide how many such blocks enter a single context package without leaking bodies, assigning
incorrect citations, or converting integrity failures into benign abstention.

The central design hazard is a cycle: Citation IDs belong to the final package (`E1 ... En`), while the final
rendered string and its budget depend on the Citation ID length. This record resolves that cycle additively; it
does not change the historical S6-T5.5 statement that permanent Binding belongs to the final selected set.

## 3. Frozen Responsibility Boundary

The future `ContextBuilder` has one responsibility: transform one validated `RetrievalRequest` plus a sequence of
validated `RetrievalEvidence` into one deterministic `RetrievedContextPackage` or a classified structural
abstention package. It is neither a retriever, a trust engine, an evaluator, nor a generator.

The future unique interface is:

```python
class ContextBuilder(Protocol):
    def build(
        self,
        *,
        request: RetrievalRequest,
        evidence: Sequence[RetrievalEvidence],
        citation_mode: CitationMode,
        config: ContextBuildConfig,
    ) -> RetrievedContextPackage:
        ...
```

`citation_mode` is the sole authoritative mode input and is deliberately not duplicated in
`ContextBuildConfig`. Constructor injection is limited to `ContentResolver` and `EvidenceEnvelopeFactory`.
`RetrievalTrace 不属于 build 必需输入`: the builder validates each Evidence directly against the Request and
does not use an audit trace as a second mutable source of truth.

不得通过 build 参数传入 raw body、arbitrary renderer、dict metadata、Ground Truth、Evaluator、Trust score、Chroma、
`EmbeddingProvider` 或 LLM；ContextBuilder 不读取 Stage 6 fixture，只接收已创建的运行时 DTO。

The build API must not accept raw body, arbitrary renderer, dict metadata, Ground Truth, Evaluator, Trust score,
Chroma, `EmbeddingProvider`, LLM, `TrustAggregator`, or `RetrievalPolicy`. It does not read Stage 6 fixture data;
it receives only already-created runtime DTOs through the public contract.

## 4. ContextBuildConfig and Reproducibility

The future canonical contract owner is `contracts/`. `ContextBuildConfig` is frozen, slots-based and kw-only with
the following fields:

- `context_schema_version`
- `max_evidence_count`
- `max_context_characters`

Both limits are positive JSON-safe integers. Its deterministic `context_build_config_hash` is SHA-256 of canonical
UTF-8 JSON with sorted keys. The payload contains only these configuration fields; it excludes paths, time,
randomness, query text, body text, labels and Ground Truth.

`RetrievedContextPackage` must store `context_build_config_hash`, `max_evidence_count` and
`max_context_characters`. The hash identifies the complete semantic configuration; the two limits make an audit
record understandable without recovering sensitive text. Neither field is a trust decision.

## 5. Provenance Validation, Stable Sort and Deduplication

Before any content resolution, ContextBuilder validates every future cross-object invariant exactly:

```text
evidence.query_id == request.query_id
evidence.retrieval_request_id == request.request_id
evidence.collection_fingerprint == request.collection_fingerprint
1 <= evidence.rank <= request.top_k
```

`RetrievalRequest` intentionally has no `corpus_snapshot_id`; therefore ContextBuilder must **not** compare an
Evidence snapshot to a Request snapshot. Each Evidence first validates its own canonical UID, snapshot, ContentRef,
chunk, content hash and finite metrics through its existing contract. After exact UID deduplication, the current
single-collection baseline requires all surviving Evidence to have 相同 corpus_snapshot_id; a mixed snapshot
sequence is `REQUEST_EVIDENCE_MISMATCH`. An empty retrieval trace records the explicit empty snapshot state `""`,
not a fabricated snapshot identity. Any mismatch is an integrity error, never abstention.

The frozen candidate order is:

```text
(rank ascending, evidence_uid ascending)
```

The original Python sequence order is not semantic. Identical `evidence_uid` records are deduplicated only when the
following exact semantic projection is equal: `evidence_schema_version`, `evidence_uid`, `query_id`,
`retrieval_request_id`, `corpus_snapshot_id`, `doc_id`, `chunk_id`, `parent_doc_id`, canonical `content_ref`,
`content_hash`, `source_id`, `source_type`, `version`, `timestamp`, `rank`, `distance`, `similarity`,
`collection_fingerprint`, and public_metadata 的深层语义值. The first record in stable order is retained only for
an exact projection match. The same UID with any projection difference fails closed as
`DUPLICATE_EVIDENCE_CONFLICT`; it is neither selected nor resolved. Error/audit output may name only a safe UID or
hash and must not contain raw metadata, ContentRef or body text.

`NO_EVIDENCE_AFTER_DEDUPLICATION` is **removed from active baseline by S6-T5.6-P1**. Under the frozen exact duplicate
rule, a non-empty input retains at least one representative, so that code would be unreachable and must not be
preserved merely to manufacture a test. It remains only as a historical protocol snapshot, never as an active reason
code or implementation target.

因此，`NO_EVIDENCE_AFTER_DEDUPLICATION` 从 active baseline 语义中移除；未来实现不得伪造不可达 reason code。

## 6. Frozen Build Order and Citation/Budget Algorithm

H1 replaces the earlier P1 historical wording that resolved every count-selected candidate before applying the final
budget. The active contract is **sequential resolution**: a candidate that is never eligible for inclusion never
receives body-access capability. The future implementation must execute the following order exactly:

1. validate `ContextBuildConfig`;
2. validate Request, citation mode and Evidence sequence types;
3. validate all Request/Evidence provenance;
4. stable sort;
5. exact UID duplicate/conflict handling;
6. apply `max_evidence_count`, recording excluded UIDs as `MAX_EVIDENCE_COUNT_EXCLUDED`;
7. render the fixed citation instruction;
8. for empty raw input, return `EMPTY_RETRIEVAL` abstention;
9. if the instruction 本身超过预算, return `CONTEXT_BUDGET_EXHAUSTED` and 不得调用 ContentResolver;
10. for count-selected candidates, 逐条执行: resolve through `ContentResolver`; create an Envelope through
    `EvidenceEnvelopeFactory`; create temporary `E{included_count + 1}` Binding; render one complete block; test the
    full final Unicode code-point budget; commit only if it fits; on the first non-fit record `BUDGET_EXCLUDED` and
    stop;
11. every later count-selected candidate after that cutoff is `NOT_ATTEMPTED_AFTER_BUDGET_CUTOFF`: it must never call
    resolver, factory or renderer and must create no `ResolvedContent`, Envelope or Binding;
12. assemble Package and ContextBuildTrace.

The future test matrix must verify resolver call counts: empty input `0`; instruction-only over-budget `0`; first
candidate non-fit `1`; first fit then second non-fit `2`; later cutoff candidates remain uncalled. The implementation
must never resolve all count-selected candidates beforehand.

Resolution or Envelope creation failures are never skipped. Unknown ref, hash mismatch, snapshot integrity failure,
request mismatch, duplicate conflict, invalid metric and unexpected resolver/factory/renderer failure raise a
redacted exception and return no Package.

For step 10, this review freezes **stable prefix selection**:

1. Keep `included_count` and committed Envelopes, Bindings and rendered blocks.
2. For the next candidate, create a **临时 Binding** with `E{included_count + 1}`.
3. The temporary Binding exists only inside this one build call stack; it is not persisted, audited or exposed.
4. Call the existing unique `render_evidence_block()` to obtain the complete candidate block.
5. Test the exact candidate string: citation instruction plus all committed blocks plus this complete block.
6. If it fits, commit the Envelope, Binding and block, then increment `included_count`.
7. If it does not fit, do not commit and do not consume Citation ID; stop evaluating later candidates.

即：不消费 Citation ID 的临时候选不会进入最终状态；本协议采用稳定前缀选择，而不是按正文长度重新排序。

Stopping at the first non-fitting candidate intentionally prevents a lower-ranked, shorter block from leapfrogging a
higher-ranked block. Therefore the final Context is a deterministic stable prefix, permanent citations are exactly
continuous `E1 ... En`, and temporary bindings never appear in Package, audit or final Citation sequence. The
algorithm uses the renderer output, not an estimated length, and never truncates a block.

The safe `ContextBuildTrace` records all count-limited candidate UIDs, included UIDs, budget-excluded UIDs and
reason codes. The first non-fitting UID is `BUDGET_EXCLUDED`; later UIDs are
`NOT_ATTEMPTED_AFTER_BUDGET_CUTOFF`. These are safe decision records, not abstention reason codes unless no complete
block is included.

## 7. Budget and Exact Rendering Semantics

Budget is the Unicode code point count of the final rendered string (`len(rendered_context)`), not UTF-8 byte
length and not token count. `rendered_context_hash` is SHA-256 of the final string's UTF-8 bytes. All assembly uses
LF; `os.linesep` is forbidden.

The exact template is:

```text
rendered_context = citation_instruction + included_block_1 + included_block_2 + ...
```

The fixed instruction already has one trailing LF; every existing evidence renderer block has its frozen trailing
LF. No platform-dependent or extra separator is added. The budget includes the instruction, every complete block
and every resulting LF. It does not mutate `Envelope.content`, make a token budget, or create a character-level
partial block.

## 8. Structural Abstention versus Integrity Failure

Structural abstention means only that no usable Context can be built. It is not a trust judgement and never hides
an integrity exception. An abstention package has empty `rendered_context`, an SHA-256 hash of the empty UTF-8
string, empty Envelope and Binding tuples, `evidence_count == 0`, a deterministic `package_id`, and exactly one
reason code in the following priority order:

1. `EMPTY_RETRIEVAL`: input Evidence count is zero.
2. `CONTEXT_BUDGET_EXHAUSTED`: the fixed citation instruction alone exceeds the positive character budget.
3. `NO_COMPLETE_EVIDENCE_BLOCK_FITS`: the instruction fits, but the stable-prefix policy cannot admit the first candidate.
   This is not proof that every lower-ranked candidate would fail; stable ranking intentionally prevents
   lower evidence from leapfrogging the first candidate.

`CONTEXT_BUDGET_EXHAUSTED` is a structural abstention reason code, not an exception code. `NO_EVIDENCE_AFTER_DEDUPLICATION`
is not active. Hash mismatch, unknown ref, Binding mismatch and all provenance/integrity errors must raise, not
be converted to these reason codes.

Candidate decision codes are never abstention reason codes. `EMPTY_RETRIEVAL` has no candidate decisions;
instruction over-budget uses `NOT_ATTEMPTED_INSTRUCTION_BUDGET_EXHAUSTED` for all count-selected candidates while the
Package reason remains `CONTEXT_BUDGET_EXHAUSTED`; a first candidate non-fit uses `BUDGET_EXCLUDED` then
`NOT_ATTEMPTED_AFTER_BUDGET_CUTOFF` while the Package reason remains `NO_COMPLETE_EVIDENCE_BLOCK_FITS`.

## 9. Future RetrievedContextPackage and Safe Decision Trace

The future canonical owner is `contracts/`. `RetrievedContextPackage` is frozen, slots-based and kw-only. Its
fields are `package_id`, `request_id`, `query_id`, `citation_mode`, `evidence_envelopes`, `citation_bindings`,
`rendered_context`, `rendered_context_hash`, `evidence_count`, `abstention_required`,
`abstention_reason_codes`, `context_schema_version`, `context_build_config_hash`, `max_evidence_count`,
`max_context_characters`, and `build_trace`.

`build_trace` is the only persisted Trace DTO field. `context_build_trace_hash` is **not a second persisted DTO field**:
`to_audit_dict()` may derive it, and the package identity payload uses the canonical relation
`context_build_trace_hash = build_trace.trace_hash`.

`rendered_context` is `repr=False`; Envelopes, Bindings and reason codes are tuples. Evidence count must equal both
tuple lengths; Binding and Envelope must match one-to-one; citations must be continuous `E1 ... En`; and the stored
hash must exactly match the rendered string. `asdict()` is explicitly sensitive. Normal `repr()` and
`to_audit_dict()` exclude body text, rendered context and Query text; no ordinary sensitive export is provided.
The package contains no Trust score, label, Ground Truth or LLM output.

`ContextBuildTrace` has future canonical ownership in `contracts/`, is frozen, slots-based and kw-only, and contains
exactly these semantic fields: `trace_schema_version`, `trace_id`, `trace_hash`, `request_id`, `query_id`,
`corpus_snapshot_id` (or explicit empty state `""`), `context_build_config_hash`, `input_evidence_count`,
`deduplicated_evidence_count`, `count_selected_count`, `resolved_count`, `included_count`, `stable_candidate_uids`,
`count_selected_uids`, `max_count_excluded_uids`, `resolved_uids`, `included_uids`, `budget_excluded_uids`,
`instruction_budget_not_attempted_uids`, `not_attempted_after_budget_cutoff_uids`, and `decision_codes`. UID
collections and decision codes are tuples in stable order. `decision_codes[i]` corresponds to
`stable_candidate_uids[i]`; `len(decision_codes) == len(stable_candidate_uids)`, every stable candidate has exactly
one decision, all decision UID tuples form an ordered 不相交划分 of the stable candidates, and each tuple preserves
stable-candidate order. The permitted codes are `INCLUDED`, `MAX_EVIDENCE_COUNT_EXCLUDED`,
`NOT_ATTEMPTED_INSTRUCTION_BUDGET_EXHAUSTED`, `BUDGET_EXCLUDED`, and
`NOT_ATTEMPTED_AFTER_BUDGET_CUTOFF`.

The count invariants are: `input_evidence_count >= deduplicated_evidence_count`;
`deduplicated_evidence_count == len(stable_candidate_uids)`;
`count_selected_count == len(count_selected_uids)`; `resolved_count == len(resolved_uids)`;
`included_count == len(included_uids)`; and `included_count <= resolved_count <= count_selected_count <=
deduplicated_evidence_count <= input_evidence_count`. `max_count_excluded_uids` and `count_selected_uids` are
disjoint and, concatenated in stable order, equal `stable_candidate_uids`; `budget_excluded_uids 长度只能为 0 或 1`.

For all-fit, included and resolved UIDs equal count-selected UIDs, and all exclusion tuples are empty. For
instruction over-budget, `resolved_count == 0`, `included_count == 0`,
`instruction_budget_not_attempted_uids == count_selected_uids`, selected candidates use
`NOT_ATTEMPTED_INSTRUCTION_BUDGET_EXHAUSTED`, and the budget/cutoff tuples are empty. For first-block non-fit,
only the first selected UID is resolved and budget-excluded; later selected UIDs are
`NOT_ATTEMPTED_AFTER_BUDGET_CUTOFF`. For partial fit, included UIDs are a strict selected prefix, resolved UIDs equal
included UIDs plus the single budget-excluded UID, and all remaining selected UIDs are cutoff-not-attempted. For
`EMPTY_RETRIEVAL`, every UID tuple and `decision_codes` is empty, every count is zero, and
`corpus_snapshot_id == ""`.

Trace identity is independent of Package identity. `trace_hash` is SHA-256 over canonical UTF-8 JSON whose exact
payload keys are `trace_schema_version`, `request_id`, `query_id`, `corpus_snapshot_id`,
`context_build_config_hash`, `input_evidence_count`, `deduplicated_evidence_count`, `count_selected_count`,
`resolved_count`, `included_count`, `stable_candidate_uids`, `count_selected_uids`, `max_count_excluded_uids`,
`resolved_uids`, `included_uids`, `budget_excluded_uids`, `instruction_budget_not_attempted_uids`,
`not_attempted_after_budget_cutoff_uids`, and `decision_codes`. It excludes `trace_id`, `trace_hash`, and
`package_id`; `trace_id == "CT-" + trace_hash`. Historical H1 notation `trace_id = CT-<full_sha256>` means the same
full digest identity; trace hash 不包含 package_id.

The Package ID is `PK-<full_sha256>` over exactly `context_schema_version`, `request_id`, `query_id`,
`citation_mode`, `rendered_context_hash`, `evidence_uids`, `context_build_config_hash`, and
`context_build_trace_hash`, where `context_build_trace_hash = build_trace.trace_hash`. This one-way relation
prevents an identity cycle.

The trace is the approved no-body exclusion record, rather than putting routine budget exclusions in
`abstention_reason_codes`. It never includes body text, rendered blocks, ContentRef raw values, Query text, metadata
values, paths, labels or Ground Truth.

Package validation first validates `build_trace` itself, then requires `build_trace.request_id == package.request_id`,
`build_trace.query_id == package.query_id`, `build_trace.context_build_config_hash ==
package.context_build_config_hash`, and `build_trace.included_uids == tuple(envelope.evidence_uid for envelope in
package.evidence_envelopes)`. Binding/Envelope are one-to-one, Citations are continuous `E1 ... En`, and `package_id`
must be recomputable. It excludes text, paths, time, randomness, Ground Truth and evaluator labels.

## 10. Future Error Ownership and Dependency Direction

When separately approved, S6-T5.6 implementation may add a Context construction error hierarchy only under
`contracts/errors.py`, preserving fixed redacted public messages and `raise ... from error` internally. The frozen
semantic codes are `INVALID_CONTEXT_BUILD_CONFIG`, `REQUEST_EVIDENCE_MISMATCH`,
`DUPLICATE_EVIDENCE_CONFLICT`, `INVALID_RETRIEVED_CONTEXT_PACKAGE` and
`UNEXPECTED_CONTEXT_CONSTRUCTION_FAILURE`. It must not create a `CONTEXT_BUDGET_EXHAUSTED` exception because that
name is reserved for the structural reason code above.

ContextBuilder, Package, Build Trace, budget and audit must exclude `poisoned`, `poison_label`, `label`,
`attack_id`, `attack_goal`, `attack_category`, `expected_answer`, `expected_behavior`, `failure_type`,
`ground_truth`, `oracle`, `risk_goal` and `stealth_level`. The future implementation must not import Evaluator,
GroundTruthVault, TrustAggregator, RetrievalPolicy, a Chroma concrete class, SentenceTransformer, Groq or any LLM.

## 11. Scope and Approval Gate

This P1 record clarifies the earlier S6-T5.5 phrase “Binding after final selection”: temporary candidate bindings
are non-observable calculation values, while only committed bindings are final package state. The clarification is
additive and does not alter accepted historical contracts.

S6-T5.6-P1 is `Completed, pending human acceptance`; S6-T5.6-P1-H1 is `Completed, pending human acceptance`; and
S6-T5.6-P1-H2 is `Completed, pending human review`.
S6-T5.6 implementation requires separate approval. S6-T5.7+ remains `NOT APPROVED`; it may not introduce Trust,
policy, generation, LLM integration or formal RAG experiments. No source code, fixture data or formal experiment was
created by this review.

## 12. Teaching and Interview Boundary

**What and why**: the protocol separates “candidate calculation” from “committed context state”, preventing a
budget-rejected `E9` from leaving a gap before `E10`. **Enterprise relevance**: deterministic packages make incident
replay, audit and regression testing possible without putting sensitive body text into routine logs.

**Relation to the prior stage**: S6-T5.5 proves one block can be bound and rendered safely; S6-T5.6-P1 specifies
how many such blocks may coexist safely. **Interview question**: why not estimate length before rendering? Answer:
escaping, LF normalization and Citation ID width make estimates semantically different from the delivered Context.

**Common misconception**: structural abstention does not mean the model judged a source untrustworthy. It only says
the configured deterministic package construction found no complete usable block. Trust analysis remains a later,
separately approved layer.
