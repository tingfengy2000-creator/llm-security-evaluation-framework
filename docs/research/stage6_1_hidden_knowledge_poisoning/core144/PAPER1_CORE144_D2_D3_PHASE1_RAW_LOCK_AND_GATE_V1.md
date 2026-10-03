# Core144 D2/D3 Phase1 raw lock, comparison and held gate V1

Task: `P1-CORE144-D2-D3-PHASE1-RAW-LOCK-AND-GATE-01`.
Date: 2026-10-03. Source HEAD: `79c65219845379a710a076ee50f791b0faad9c1c`.
Authority: `PODR-129 / OR-083 / REL-2026-0098`. Owner supplied four originals
and confirms completely fresh isolated sessions. This is `OWNER_ATTESTED`,
not machine-proven isolation; platform session IDs were not supplied.
`R4_CODEX` remains the historical code, actual provider **Doubao**.

## Raw identity and lock

All originals were byte-copied to a fresh private namespace and made read-only
before validation/comparison. No editing, formatting, sorting or resaving.
SHA manifests plus read-only attributes are a process lock, not an OS WORM guarantee.
Private namespace: `experiments/core144_d2_d3_phase1_raw_lock_20261003/`.
Owner mirror: `{PRIVATE_HANDOFF_ROOT}/paper1_core144_d2_d3_phase1_raw_lock_20261003/`.

| Filename under `raw/` | Bytes | SHA256 |
|---|---:|---|
| PAPER1_CORE144_D2_R3_GPT_PHASE1_RAW_RETURN_V1.json | 40337 | `71098c2264023408d253248c6bb8c654c08aa9c85fd5ead30a2e58aa9c9a5e55` |
| PAPER1_CORE144_D2_R4_CODEX_PHASE1_RAW_RETURN_V1.json | 39541 | `6fb101fd1f359397d387d225a6164812b594abfb166c79fa2942fbb43a78c06c` |
| PAPER1_CORE144_D3_R3_GPT_PHASE1_RAW_RETURN_V1.json | 39041 | `e0c5c95a6de770f4aee692a4c5cc4e35c79786184acc006224caa079e9fb28aa` |
| PAPER1_CORE144_D3_R4_CODEX_PHASE1_RAW_RETURN_V1.json | 39572 | `c2adf1b01ff25e8b2b22ac5980abf99106e07ecab5690f00681ad7d2b5c8f211` |

`RAW_LOCK_MANIFEST_V1.json` binds exact source/copy paths, byte counts and UTC
lock times. `PHASE1_VALIDATION_AND_COMPARISON_V1.json` begins validation after
all four locks. Initial `INPUT_OUTPUT_INDEX_V1.json` remains unchanged; later
triage/gate/check artifacts are included by `FINAL_EVIDENCE_INDEX_V1.json`.
Final index SHA256:
`f7502705956fa6252de04f978a0a4b7fbc14c40538633a7d0a61f0936325818d`.
All 12 private artifacts were mirrored to the Owner handoff namespace with
per-file SHA parity PASS; all four raw mirror copies remain read-only.

## Structural validation and independent agreement

All four PASS: strict UTF-8 JSON array without BOM; 144 records/unique IDs;
reviewer-specific ID set/order exact; exact seven keys in schema order;
canonical enums; no added fields, duplicate JSON keys or non-JSON constants;
all required `issue_note` present. Default-valued rows may have optional notes.
All four packet SHAs match the frozen manifests. R3/R4 ID-to-text maps match
within each domain while retaining their separate frozen orders.
Shared schema SHA:
`d143d5edce1434ac2e0be0e3a818c0ebe2fd0d58499c6962a7ca68e443aa3307`.

| Field | D2 | D3 |
|---|---:|---:|
| text_naturalness | 133/144 (92.3611%) | 128/144 (88.8889%) |
| local_internal_conflict | 144/144 (100%) | 143/144 (99.3056%) |
| self_containment | 139/144 (96.5278%) | 141/144 (97.9167%) |
| ambiguous_referent | 144/144 (100%) | 144/144 (100%) |
| meta_or_template_language | 134/144 (93.0556%) | 130/144 (90.2778%) |

D2: 22 distinct disagreement rows/26 cells. D3: 30 rows/34 cells. These counts
are not confirmed defect counts. Per-field disagreement IDs and original
values/notes are traceable in the private comparison. `issue_note` is reviewed
semantically; literal equality is not required. Raw-identical notes are
D2 100/144 and D3 111/144, not estimates of semantic agreement.
Including shared text-quality flags, Owner triage covers D2 29 and D3 33 rows.
Shared internal-conflict YES alone does not establish a construction defect.

## Candidate-visible findings

D2: both mark eight rows meta/template language, chiefly comparison-scope or
text-processing narration. Necessary factual scope qualifications must be
distinguished from task narration; agreement does not prove all eight defects.
Five self-containment disagreements involve income lists or unspecified fact
scope. Eleven naturalness disagreements require preference-versus-defect review.

D3: both flag `CBR-4ACFA6997441EE` and `CBR-B2137BC0C9CDA1` for missing
necessary scope/document identity. Both flag `CBR-FF1903111EE14A` and
`CBR-4C7EBF4CCB0937` for literal sentence-level commentary; both mark
`CBR-AD70D8C3B740D1` MINOR_ISSUE. In `CBR-81E40769899B68`, R3 gives
UNCERTAIN/FLAG and R4 gives YES/PASS. Refusal of face verification does not
by itself establish an available alternative; the same-condition test is
incomplete from this Candidate alone. This is text diagnosis, not a legal
ruling or an altered construction label.

Only candidate-only packages/schema and locked Phase1 raw returns were loaded.
No C/P/H, HKP, S, mapping, Evidence, Expected, GT or Human answer was used.
No role-specific shortcut rate is claimed without a separate construction-side
audit. No repair or new rule is made in this task.

## Held gates and decision-ready blocker

Both domains: `PHASE1_RAW_LOCKED=TRUE`, `PHASE1_STRUCTURE_VALID=TRUE`,
`PHASE1_SEMANTIC_GATE_PASS=FALSE`, `PHASE2_RELEASE_AUTHORIZED=FALSE`.
Status: `D2_D3_PHASE1_RAW_LOCK_COMPLETE / PHASE1_STRUCTURE_VALID /
OWNER_PHASE1_TRIAGE_REQUIRED / D2_D3_PHASE2_WITHHELD`.
D1 Human gates remain independently recorded. No new Human authorization,
Core GT, formal split, training or paper result. Retain the original reviewer
sessions for later authorized same-session rereview/Phase2.

1. Issue ID: `CORE144-D2-D3-PHASE1-TEXT-QUALITY-GATE-01`.
2. Name: open text-quality flags and categorical disagreements.
3. Discovery: post-lock independent external Phase1 comparison.
4. Facts: OBSERVED = structural PASS, 22/30 differing rows and shared flags;
   SOURCE_DERIVED = text/notes examples above; INFERENCE = some need repair;
   UNKNOWN = final Owner decisions and role-specific shortcut rates.
5. Constraints: frozen V4–V4.3, immutable raw/candidate versions, candidate-only
   Phase1, independent fields and semantic closure before Phase2.
6. Why now: later Evidence may mask text defects and increase human rework.
7. Risks: ambiguous decisions, avoidable withdrawal/relabeling, exposure to
   old answers, broken version lineage and overstated acceptance.
8. Options: A = bounded repair of confirmed context/commentary defects plus
   targeted rereview (more work, versioned/reversible, best quality control);
   B = item-level nonblocking Owner overlay for demonstrated preference/legal
   scope statements (less work, residual wording disclosed); C = separately
   authorized auxiliary blind reviewer (extra time/account cost; no automatic
   voting). All retain raw values; scientific meaning and lineage remain explicit.
9. Recommendation: A for confirmed context/commentary defects; B only after
   item-level scope/preference assessment, not blanket acceptance.
10. Rationale/confidence: missing antecedents and conditional entailment have
    direct text evidence; meta-scope judgments need bounded human review.
11. Owner decision needed: exact rows to repair versus preserve with rationale,
    then targeted rereview scope. No repair decision has yet been supplied.
12. Allowed until decision: preservation, read-only diagnosis and governance;
    no candidate/rule rewrite, Phase2/Human release, GT, split, training or new reviewer.

Concrete private artifact:
`PAPER1_CORE144_D2_D3_PHASE1_OWNER_DECISION_PACKET_V1.md`, containing 62 full
text-and-original-answer cases. **Owner-only; do not send it to blind reviewers.**

## Checks and documentation closeout

Implementation: `scripts/research/lock_core144_d2_d3_phase1_returns.py`.
Tests: `tests/research/test_core144_d2_d3_phase1_lock.py` (10): exact ID order,
duplicates, extra keys, missing row/note, illegal enums, optional default notes,
ID-based comparison, strict JSON and raw byte preservation/no overwrite even
for invalid originals. Scoped Ruff/MyPy, UTF-8, secret/private-path and
protected-history checks plus `git diff --check` are recorded before commit.
Raw and derived evidence stay Git-ignored. Runtime commands/results are in
`QA_AND_EXECUTION_RECEIPT_V1.json`.

Human/Agent ledgers, Current State and Execution Log are mandatory updates.
Experiment Master, Owner Register, Master Context and Stage Process receive
new checkpoints because raw evidence, Owner attestation and a gate changed.
Core144/Paper1 README navigation and additive parallel state V4 are updated.
Research Plan Authority and canonical lessons stay unchanged: no method,
schema, scope decision or accepted new lesson occurred. Workbooks, candidate
corpora, evidence pools and Stage1–5 are unchanged. Raw ingestion/comparison
is complete; scientific/text acceptance remains pending Owner decision.
