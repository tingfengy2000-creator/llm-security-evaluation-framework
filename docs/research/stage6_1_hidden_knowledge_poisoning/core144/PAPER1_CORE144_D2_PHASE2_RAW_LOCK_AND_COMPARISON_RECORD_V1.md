# Core144 D2 Phase2 raw-lock and comparison record V1

2026-10-15; task `P1-CORE144-D2-PHASE2-RAW-LOCK-AND-COMPARISON-01`;
source HEAD `c741120d9be4c852d9d7c8dce92898a4f263d3d5`.
PODR-136 / OR-090 / REL-2026-0105. LOCAL evidence validation only.

## Outcome

Both original returns are byte-locked and structurally valid:144 rows each,
own V2 packet ID/order exact, eleven string fields,1152 canonical categorical
cells each,144 nonblank reasons each, strict UTF-8 no BOM, no duplicate JSON
keys/IDs, no additional fields. No raw rewrite, normalization, sorting or vote.

D2 is NOT machine-preannotation accepted.42 rows have semantic-category
differences (50 cells);15 further rows differ only in actual evidence selection.
Five quality flags refer to three unique candidates. The union of semantic
differences and quality flags is43 unique Owner review cases. These are review
items, not43 proven candidate defects. Two excerpt omissions are confirmed.
D3 retains its previous two S3 blockers; D1 Human gates remain unchanged.
[Current state V11](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V11.md),
[twelve-field decision](PAPER1_CORE144_D2_PHASE2_EVIDENCE_AND_REVIEW_BLOCKER_V1.md).

## Immutable original identities

| Reviewer | Actual provider | Bytes | SHA256 |
|---|---|---:|---|
|R3_GPT|GPT|97509|72ecab7524fa041706f951b9f0b3bc079c946ae3d36f3499f6a51c76c7edc505|
|R4_CODEX|Doubao|90977|6e24b476a6f939c560d63e68755f29e578385e0a0a749d72f93d218f32d87589|

Both byte-copies/read-only locks and RAW_LOCK_MANIFEST precede either raw parse.
Source bytes are checked stable at lock. The manifest records actual UTC lock
times, input path/size/hash and separate immutable-copy path. Original
delivery paths remain private, not in public Git.

Owner explicitly confirms original D2 R3/R4 sessions, corresponding seven V2
files/per-row frozen E1/E2 only, no other reviewer/mapping/labels/Expected/GT/
repository/external sources/web/other AI. Record OWNER_ATTESTED, not machine
proof. R4_CODEX remains a historical code, not a Codex provider assertion.
Receipt establishes Owner-reported distribution and returns. Complete144 JSON
outputs do not prove complete context ingestion, platform limits or isolation.

## Independent categorical comparison

| Field | Agree /144 | Differing cells |
|---|---:|---:|
|overall_fact_status|135|9|
|version_claim_status|115|29|
|authority_claim_status|135|9|
|minimum_external_evidence_needed|143|1|
|evidence_selection|118|26|
|phase2_issue|143|1|
|possible_accidental_secondary_error|144|0|
|evidence_sufficiency|143|1|

Eight categorical fields are compared by opaque ID after each own packet order
passes. Overlapping fields do not sum to distinct candidates.26 evidence-selection
differences include15 process-only rows and11 rows with other differences.
A process-only difference is not automatically wrong, nor exempt from a shared
quality flag:one such row is jointly evidence-insufficient. Reason wording is
preserved but literal equality is not an agreement gate.

Current locked Phase1 ZERO/nonconflict-N/A conditions and supplied E1/E2
references have0 detected mechanical cross-field violations. This is not
semantic proof of ONE/MULTI necessity or fact/authority/version correctness.
All possible-secondary-error values are NO; this agreement does not establish
that no hidden defect exists. No construction role/HKP/S/family, Expected,
GT or D1 Human answers are loaded into comparison.

## CORRECTION — two V2 presentation omissions confirmed

This corrects the scope of the October7
[excerpt preflight PASS](PAPER1_CORE144_D2_D3_PHASE2_PREFLIGHT_AND_RELEASE_RECORD_V1.md)
additively. That old record, all74 sealed files, original full-body V1,
V2 packets/source hashes and raw returns remain byte-unchanged.

- D2-EXCERPT-OMISSION-01:《中华人民共和国银行业监督管理法》第二条
  national supervision-duty body exists in the original frozen full text,
  but the V2 document ends at its heading/table-of-contents preamble.
- D2-EXCERPT-OMISSION-02:《非银行支付机构监督管理条例》第八条
  capital-requirement body exists in original frozen full text, but V2 preserves
  only its promulgation identity/preamble and final effective-date article.

Each source is referenced by three current rows:dependency impact is six distinct
row references, not six proven defective candidates. Both reviewers independently
report insufficient supplied evidence for the two identified substantive rows.
Their inability to confirm from the allowed excerpts must not be blamed on a
failure to search or remember external facts.

Root cause:the excerpt selector retained complete articles around registered
anchors, but its required-anchor set did not cover every supplementary candidate
atom. Passing range/hash/anchor tests therefore did not establish complete
candidate-to-visible-evidence coverage. These are presentation defects, not
official-source absence or bad snapshot hashes. Original full text is used only
to diagnose omitted material, not to grade a reviewer as though it was supplied.
No new source is needed for these two witnesses. No V3 repair is executed.

A third unique quality-flagged candidate asserts a specific meeting-record
carrier. One reviewer requires that carrier; the other accepts the supplied
promulgation wording as sufficient for adoption/issuer claims. The frozen visible
promulgation text names the meeting but does not contain the exact carrier
assertion. This is a separate proposition-scope/evidence-sufficiency review,
not silently resolved as an excerpt omission, new rule or false-fact label.

## Physical evidence / checks / reproducibility

Private `experiments/core144_d2_phase2_raw_lock_20261015/` contains:
input and Owner attestation; output_v1/raw originals; lock manifest; structural/
cross-field reports; categorical comparison; shared/individual quality flags;
fulltext-versus-V2 literal source witnesses;43-case Owner packet/summary;
command/test receipts, read-only reproduction notebook, closeout and sealed index.
`FINAL_EVIDENCE_INDEX_V1.json` seals18 files, SHA
`940796ca4632a078ceb64ece728a109da19218c96d3856a2358b82dcf08ce3cf`.
Later mirror/Git receipts are additive, not index rewrites. Owner archive identity:
`paper1_core144_d2_phase2_raw_lock_owner_only_20261015`.
The Owner-only E-drive mirror contains the same private evidence and readable
review packet; do not send it to R3/R4/Human.

Frozen packet SHA7e06...1201 / fcae...08c2 and all74 original preparation files
reverified. Tests reject malformed/duplicate-key/BOM/NaN/extra-field/blank-reason/
wrong-ID-order inputs, check ZERO/supplied-evidence consistency and prove
lock-before-parse/no-overwrite. Synthetic data only; no production answers
in public tests. Initial test-first missing-module and fixture typing failures
are retained with successful reruns. No new dependencies or downloads.
Actual results:39 scoped regression tests PASS; Ruff/MyPy PASS;139 local links
checked; UTF-8/secret/private-path/ignore/diff checks PASS; raw source/copy and
unrelated design/PDF hashes unchanged; read-only notebook execution PASS.

## Risk review / mandatory closeout

Forward risks:cleaning raw before lock, wrong own packet, inherited session
claims, partial output, evidence-selection voting and silently repairing bad
excerpts. Mitigations:both locks before parse; frozen own packet hashes; explicit
Owner attestation level; exact return counts; process/semantic separation;
additive witnessed correction and fail-closed Human gate.
Paper risk:missing evidence can confound benchmark difficulty and create false
acceptance. No detector or formal population claim is derived from agreement.

Human/Agent Ledgers, Current State, Execution Log, Owner receipt register,
Experiment Master, Stage Process, Master Context and Paper1/Core144 navigation
are synchronized. Research Plan Authority, accepted V4–V4.3, long-term needs,
frozen corpus/snapshots/IDs and canonical lessons remain unchanged:the findings
are unresolved QA evidence, not new accepted rules. D1 Human and D3 gates are
not altered. Stage1–5/Final72 and existing design Markdown/PDF remain untouched.
No repair, annotation override, new Reviewer/R5 call, Human D2/D3 workbook,
Expected/GT, split, detector or calibration is executed.

## Stop / next gate

`D2_PHASE2_RAW_LOCKED / D2_PHASE2_STRUCTURAL_VALIDATION_PASS /
D2_PHASE2_SEMANTIC_REVIEW_AND_EVIDENCE_REPAIR_REQUIRED /
HUMAN_D2_NOT_AUTHORIZED / D3_PHASE2_WITHHELD / HUMAN_DECISION_REQUIRED`.

Recommend Owner separately approve (a) bounded V3 repair of the two excerpt
documents using only original frozen sources, complete relevant articles and all
candidate-atom coverage, with reuse impact and original-session re-review;
(b)43-case bounded V4–V4.3 triage, with process-only differences retained.
No automatic correction or Guide revision. Do not resend old D2 V2 as defect-free.
