# D2/D3 targeted Phase1 raw lock and domain-local hold

Task: `P1-CORE144-D2-D3-TARGETED-PHASE1-RAW-LOCK-AND-DOMAIN-GATE-01`.
Date: 2026-10-05. Source HEAD: `cbe8e96705b3fbbf4f76d9d3f34efefccf881e9a`.
Authority: prior bounded defaults `PODR-130`, current receipt/attestation
`PODR-131 / OR-085 / REL-2026-0100`. This is raw validation and text-visible QA,
not Ground Truth, final Phase1 acceptance, factual verification or a new rule.

## Immutable originals and strict checks

| Domain / reviewer | Bytes | SHA256 |
|---|---:|---|
| D2 R3_GPT | 6,811 | `65351a2ef6ef1365eccedae54234d445d92c2b6c19838e53859bf15ff6010526` |
| D2 R4_CODEX | 6,253 | `36cd17c3d0a99f1c01ce6ac2cb6829181f7edc3d019cb19c537dfe39b0ab7e89` |
| D3 R3_GPT | 10,365 | `34f47a054e857a5e9cfcff50f7095d390f692f066bcb36c58e0f5a6ae99b4469` |
| D3 R4_CODEX | 10,266 | `7440b65c448c2503f5c4dc13010a92cb62e223f89928b0f69fa6235efa9ad0f5` |

All four source/copy hashes match; locked copies are read-only and were saved
before parsing. D2 each has 25/25, D3 each 32/32. Exact reviewer-specific ID sets
and orders, no missing/duplicate IDs, exact ordered seven keys, all-string
values, canonical enums, required notes, strict JSON/no duplicate keys or
non-JSON constants, UTF-8 without BOM pass. R4_CODEX stays the historical code;
actual provider is Doubao, not Codex. Owner confirms the four original isolated,
domain-specific sessions and authorized inputs; record `OWNER_ATTESTED`, never
machine-proven isolation. No new sessions or mixed D2/D3 context.

## Independently computed targeted agreement

| Field | D2 agree / 25 | D3 agree / 32 |
|---|---:|---:|
| text_naturalness | 24 (96%) | 26 (81.25%) |
| local_internal_conflict | 25 (100%) | 31 (96.875%) |
| self_containment | 25 (100%) | 32 (100%) |
| ambiguous_referent | 23 (92%) | 32 (100%) |
| meta_or_template_language | 24 (96%) | 32 (100%) |

D2: four disagreement rows/cells, one pure naturalness case; D3: seven
rows/cells, six naturalness cases. All targeted self-containment is PASS.
All targeted meta values are NO except one D2 R3 flag. The seven new
NATURAL/MINOR_ISSUE variances have recoverable core meaning/scope and are
nonblocking under Owner's frozen default after text/notes inspection. Preserve
both answers. Fifteen D3 mutually recognized local contradictions are not
construction defects merely for being contradictions. Literal note equality is
not an acceptance requirement; differing notes were inspected for text-visible
meaning, not forced into equal strings or automatically scored by another AI.

## Four open material-review items

| Domain / current opaque ID | R3 / R4 field | Control-plane disposition |
|---|---|---|
| D2 `CBR-3AD0693B1E6262` | referent YES / NO | Two upper-limit antecedents precede “该上限”; materiality/shared scope and explicit binding need Owner disposition. |
| D2 `CBR-376FEFA343762E` | referent YES / NO | Same two-antecedent issue; no automatic nearest-noun or vote-based answer. |
| D2 `CBR-1C3D8F52D82A22` | meta YES / NO | Circular clarification of original adopting bodies resembles residual scope narration; no single flag proves role exclusivity. |
| D3 `CBR-9496B4CB1090D3` | local UNCERTAIN / YES | Available alternative is now explicit, but “still can only use” could describe a practical restriction rather than a normative requirement; hard scope blocker remains. |

The D3 old ancestor is `CBR-81E40769899B68`. The prior repair removed the missing
alternative condition; the fresh review exposes a remaining normative versus
descriptive scope. A violation observed in practice can coexist with a rule
forbidding it. Do not force YES from intended S1 or construction role. Likewise
self-containment PASS does not prove logical-scope alignment or referent
uniqueness. The three D2 items are pending material-review decisions, not three
automatically established factual errors. Shared upper-limit qualifications
could be harmless to the main comparison but do not establish unique reference.

Recommendation **not executed**: Owner approves bounded surface/scope repair of
D2 three texts and D3 one, frozen atom/path/style recheck, new IDs/version and
targeted rereview in the original four sessions. No full144 rerun, R5 invocation,
new Guide version or vote. Alternatively Owner may provide individually
reasoned keep/disposition under existing rules. Unreasoned field overrides do
not close the gate.

## Current 144-row evidence views, not final answers

After targeted validation, identity-only lineage joins the unchanged historical
raw and changed targeted raw, preserving each reviewer's original order and
answer values. D2: 119 historical + 25 targeted; D3: 112 + 32, each 144/144.
These are `PROVISIONAL_NOT_FINAL_NOT_GT` views; no final accepted Phase1 overlay
is issued while these items remain open. Current full-view disagreements are
D2 11 (8 naturalness + 2 referent + 1 meta), D3 19 (18 naturalness + 1 local).
The 26 total naturalness variances include 19 previously designated cases and
seven newly inspected cases. They are retained, not silently normalized.

Reviewer evaluation reads only sealed raw and candidate-visible packets/schema.
Private old→new identity lineage/current text is loaded afterwards solely for
the evidence-view join. No construction class, HKP/S, Expected, GT, Human answers,
Evidence facts or detector feedback is used to choose reviewer values or close
the gate. Prior indexes and 329 baseline inputs are rechecked for preservation.
Candidates, metadata, evidence, workbook, IDs/order and V4–V4.3 are unchanged.

## Recovery and inspectable private evidence

Root: `experiments/core144_d2_d3_targeted_phase1_lock_20261005/` (Git ignored).
`RAW_LOCK_MANIFEST_V1.json` binds source identities, bytes, lock timestamps and
Owner attestation. `analysis_v2/` is the authoritative validation/evidence-view
namespace. First analysis completed structural validation but then failed on
an index adapter (historical list versus dictionary shape). Its partial output
and `ENGINEERING_INCIDENT_V1.json` are preserved; the adapter was corrected,
tested and rerun additively, without scientific/input changes.

`CANDIDATE_VISIBLE_TRIAGE_PLAN_V1.json`, `OWNER_DECISION_PACKET_V1.md`, domain
comparison/view files, gate, preservation receipt, command/QA receipt and sealed
evidence index provide physical recovery. The Owner packet has the twelve
PO-MHEP decision fields and exact texts/notes; never send it to reviewers.
Mirror: `{PRIVATE_HANDOFF_ROOT}/paper1_core144_d2_d3_targeted_phase1_lock_20261005/`.

Sealed `FINAL_EVIDENCE_INDEX_V1.json` SHA256:
`e9690c7802a2cc5e2c852b81d41ef5fb61a30ffaa0097df55df2669bbbac645a`,
22 evidence files plus the index itself. Later Git/mirror/command-delivery
receipts are additive extensions, not rewrites of this sealed index.
Final scoped result: 29 tests, Ruff, MyPy, UTF-8, public secret/private-path scan,
new local links, immutable baseline and mandatory documentation closeout PASS.

Tests cover frozen 25/32 counts, exact IDs/orders/keys/enums/notes, strict parse,
reviewer-ID joining, raw-value/lineage preservation and both index shapes.
Mechanical/code/documentation QA may PASS while scientific acceptance is HOLD.
No new scientific contract is introduced. Research Plan Authority is checked
but unchanged; the logical-scope lesson remains provisional. Unrelated design
Markdown and existing untracked master-guide PDF are excluded from commit.

## Stop / next action

`TARGETED_PHASE1_RAW_LOCK_COMPLETE / OWNER_ATTESTED / OWNER_DECISION_REQUIRED /
D2_D3_PHASE2_WITHHELD / CORE_GT_NOT_FROZEN / SPLIT_NOT_EXECUTED /
TRAINING_NOT_STARTED`.

Both domains: phase1_accepted=false, phase2_release_authorized=false. No new
Phase2 package, Human D2/D3 package, GT, Expected load, split or training.
D1 Human's existing individual gates remain independent and unchanged.
Owner now decides the four-item bounded repair/disposition; no further external
review files should be sent until a new approved version and exact checklist
exist. Any later Phase2 release remains domain-local.
