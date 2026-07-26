# S6-T5.6-P1 Context Package 协议审查与设计冻结记录

## 1. 记录身份与当前状态

- Task ID: `S6-T5.6-P1`
- Task name: `ContextBuilder, Budget, RetrievedContextPackage and Structural Abstention Boundary Freeze`
- Task nature: `DESIGN_FREEZE / PROTOCOL_REVIEW`
- Baseline: `feature/stage6-rag` at `ee905cb`; the last accepted implementation commit remains `6da27a6`.
- Current execution status: `Completed, pending human acceptance`.
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

Before any content resolution, ContextBuilder validates that every Evidence belongs to the supplied Request:
`query_id`, `retrieval_request_id`, `collection_fingerprint`, schema-compatible snapshot identity and canonical
`corpus:` ContentRef must agree with the Request/Evidence contracts. Any mismatch is the future integrity error
`REQUEST_EVIDENCE_MISMATCH`, never abstention.

The frozen candidate order is:

```text
(rank ascending, evidence_uid ascending)
```

The original Python sequence order is not semantic. Identical `evidence_uid` records with every stable identity
field equal are deduplicated by keeping the first record in this stable order. If the same UID conflicts in chunk,
hash, source, version, rank, request, snapshot or ContentRef, building fails closed with
`DUPLICATE_EVIDENCE_CONFLICT`; it must not silently choose one record.

`NO_EVIDENCE_AFTER_DEDUPLICATION` is removed from the active baseline reason-code set. Under the frozen exact
duplicate rule, a non-empty input retains at least one representative, so that code would be unreachable and must
not be preserved merely to manufacture a test.

因此，`NO_EVIDENCE_AFTER_DEDUPLICATION` 从 active baseline 语义中移除；未来实现不得伪造不可达 reason code。

## 6. Frozen Build Order and Citation/Budget Algorithm

The future implementation follows exactly this order:

1. validate Request/Evidence provenance;
2. stable sort;
3. UID deduplication;
4. apply `max_evidence_count`;
5. resolve each remaining body through `ContentResolver`;
6. verify hash through the resolver result and create each Envelope through `EvidenceEnvelopeFactory`;
7. render the fixed citation instruction;
8. select complete blocks under the final rendered-string budget;
9. assemble the Package and its safe trace.

Resolution or Envelope creation failures are never skipped. Unknown ref, hash mismatch, snapshot integrity failure,
request mismatch, duplicate conflict, invalid metric and unexpected resolver/factory/renderer failure raise a
redacted exception and return no Package.

For step 8, this review freezes **stable prefix selection**:

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
3. `NO_COMPLETE_EVIDENCE_BLOCK_FITS`: the instruction fits, but the first complete candidate block does not.

`CONTEXT_BUDGET_EXHAUSTED` is a structural abstention reason code, not an exception code. `NO_EVIDENCE_AFTER_DEDUPLICATION`
is not active. Hash mismatch, unknown ref, Binding mismatch and all provenance/integrity errors must raise, not
be converted to these reason codes.

## 9. Future RetrievedContextPackage and Safe Decision Trace

The future canonical owner is `contracts/`. `RetrievedContextPackage` is frozen, slots-based and kw-only. Its
fields are `package_id`, `request_id`, `query_id`, `citation_mode`, `evidence_envelopes`, `citation_bindings`,
`rendered_context`, `rendered_context_hash`, `evidence_count`, `abstention_required`,
`abstention_reason_codes`, `context_schema_version`, `context_build_config_hash`, `max_evidence_count`,
`max_context_characters`, and `build_trace`.

`rendered_context` is `repr=False`; Envelopes, Bindings and reason codes are tuples. Evidence count must equal both
tuple lengths; Binding and Envelope must match one-to-one; citations must be continuous `E1 ... En`; and the stored
hash must exactly match the rendered string. `asdict()` is explicitly sensitive. Normal `repr()` and
`to_audit_dict()` exclude body text, rendered context and Query text; no ordinary sensitive export is provided.
The package contains no Trust score, label, Ground Truth or LLM output.

`ContextBuildTrace` is the approved no-body exclusion record, rather than putting routine budget exclusions in
`abstention_reason_codes`. It contains only counts, Evidence UIDs, safe decision reason codes, config hash and
package identity fields. It never includes body text, rendered blocks, ContentRef raw values, Query text, metadata
values, paths, labels or Ground Truth.

`package_id` uses `PK-<full_sha256>` over canonical UTF-8 JSON containing context schema version, request ID, query
ID, citation mode, rendered context hash, final Evidence UID order and context-build config hash. It excludes text,
paths, time, randomness, Ground Truth and evaluator labels. Identical Request, Evidence, Config and CitationMode
must therefore produce identical Package identity.

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

S6-T5.6-P1 is `Completed, pending human acceptance`. S6-T5.6 implementation requires separate approval. S6-T5.7+
remains `NOT APPROVED`; it may not introduce Trust, policy, generation, LLM integration or formal RAG experiments.
No source code, fixture data or formal experiment was created by this review.

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
