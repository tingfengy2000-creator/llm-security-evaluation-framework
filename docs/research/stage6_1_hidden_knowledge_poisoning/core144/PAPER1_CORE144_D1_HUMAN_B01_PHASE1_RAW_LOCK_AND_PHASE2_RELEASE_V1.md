# Core144 D1 HUMAN-B01 Phase1 raw lock and Phase2 release V1

Date: 2026-10-06. Task: `P1-CORE144-D1-B01-PHASE1-RAW-LOCK-AND-PHASE2-RELEASE-01`.
Source HEAD: `64e1152e627e1d2d9bb3e1547cb4b0fa3c3a1eb0`.
Authority: PODR-125 per-human conditional release plus Owner's current B01 return
and request to enter Phase2; `PODR-134 / OR-088 / REL-2026-0103`.

`B01_PHASE1_RAW_LOCKED / B01_PHASE1_GATE_PASS / B01_PHASE2_RELEASE_AUTHORIZED /
B01_PHASE2_DISTRIBUTION_READY / B01_PHASE2_NOT_YET_DISTRIBUTED / NO_GT`.
Actual distribution is not observed; Owner still performs the send operation.

## Immutable original and identity

Owner designates the received `PAPER1_CORE144_D1_HUMAN_B01_PHASE1_V1(1).xlsx`
as HUMAN-B01's return. Its bytes were copied and made read-only before opening
the locked workbook for validation. The source is never renamed or resaved.
The separately synchronized handoff-root copy has the same SHA; it is not a
second independent annotation return. Workbook identity is checked against
the frozen **B01** manifest, not inferred from its filename or from A01.

| Item | Locked value |
|---|---|
| Raw filename | `PAPER1_CORE144_D1_HUMAN_B01_PHASE1_RAW_RETURN_V1.xlsx` |
| Bytes | `37,202` |
| SHA256 | `df423484092733066cbed628dde7ced0494dcb8a024c16bd35c0f1d9edfcbc6a` |
| Copy / filesystem | byte-for-byte, no Excel resave; read-only |
| Private archive | `experiments/core144_d1_b01_phase1_raw_lock_20261006/` |
| Owner mirror | `E:\LLMGuard-Handoff\paper1_core144_d1_human_b01_phase1_raw_lock_20261006` |
| Lock manifest | `PAPER1_CORE144_D1_HUMAN_B01_PHASE1_RAW_LOCK_MANIFEST_V1.json` |
| Additive validation | `PAPER1_CORE144_D1_HUMAN_B01_PHASE1_VALIDATION_V1.json` |

Evidence index: `PAPER1_CORE144_D1_B01_PHASE1_EVIDENCE_INDEX_V1.json`,
SHA `cacd9daf483dd5615ebe9726d3af77f462d6af111140bd3630984dfb8f540059`,
sealing13 artifacts. Later QA/Git/mirror command receipts are additive, not
retroactively inserted into the frozen index. Exact source command/environment
are retained in the private command receipts and lock manifest.

Owner's annotator attribution is a human declaration, not machine proof of
independent cognition, no AI use or platform history. No additional declaration
is fabricated. The historic A01 `(2)` raw and `(3)` routing artifact are untouched.

## Phase1 mechanical gate

- 144/144 rows and unique B01 IDs; exact original B01 ID order and Candidate
  text order. Eight original columns; seven visible worksheets unchanged.
- All 720 categorical cells contain legal canonical enums.
- 16/16 nondefault rows have a nonblank `issue_note`; 16 nonblank notes total.
- `issue_note` is plain text or blank; no answer formulas, hidden sheets,
  macros or external-link parts. All non-answer cell values/formulas match.
- Ordered-ID SHA: `8c97601a770d70dc47338280213370ff181c9ff347ff5046bd984354e51cc067`.
- Candidate text/order SHA: `00f872b5da59e88f9f03d6df5cf8f710093a14c91e38e92fd66dbb22d26d6a52`.

| Field | B01 raw counts |
|---|---|
| text_naturalness | NATURAL=144 |
| local_internal_conflict | YES=16; NO=128 |
| self_containment | PASS=144 |
| ambiguous_referent | NO=144 |
| meta_or_template_language | NO=144 |

This is structural/process validation, not adjudication or factual acceptance.
Internal-conflict YES is a valid annotation value, not a schema defect. No row
is rejudged, corrected, compared with A01 or forced to match construction labels.

## B01 Phase2 preflight and distribution materials

The existing sealed B01 workbook remains exactly manifest-matching: 523,102
bytes, SHA `bad9c6459dc163cd085517a8964deac6c950115486d15b4237d7273f8e138cdf`.
All 144 ID/order/text entries match the locked Phase1. All 1,440 answer cells
are blank; 225 official Evidence links. Ten visible sheets, no private mapping
or label leakage found by the source-ID/private-field scan, macros or external
links. This rechecks an unchanged previously QA-approved workbook; no new
workbook authoring, rendering claim or annotation is performed.

The detailed Chinese Phase2 manual is reused without modification: 74,078
bytes, SHA `a3131c56d791111b5bfdf43b80da396fdf069ab840595e4588e565376af72232`.
It explains all Phase2 fields, version/authority/content independence, ZERO/ONE/
MULTI evidence paths, actual selection versus minimum, reasons and common errors.

Both are copied byte-for-byte into a **B01-only** distribution-ready folder.
[Exact two-file send checklist](PAPER1_CORE144_D1_HUMAN_B01_PHASE2_OWNER_SEND_CHECKLIST_V1.md).
Do not send private raw/receipts, A01 materials, mappings, construction labels,
Expected/GT or external AI reviewer returns.

## Risk review, checks and documentation closeout

Forward/paper risks: earlier A/B routing confusion, raw normalization, missing
notes, identity/order drift, premature Phase2 release and claims inflation.
Mitigations: B01-specific manifest guard, lock-before-parse, fail-closed receipt,
exact send list and separation of ready/authorized from actual distribution.
No new semantic rule or scientific acceptance is introduced.

Scoped tests include raw preservation on failure, A01-manifest rejection,
no overwrite/save, historic A01 gate and current B01-only release. The private
QA receipt records actual tests, Ruff/MyPy, UTF-8, secret/path/link/diff checks,
input hashes, command output/exit codes and final evidence index.
Results: ten scoped tests PASS; task-scoped Ruff/MyPy PASS; closeout QA PASS.
Bundled Python3.12.14/openpyxl3.1.5 performs all actual workbook reads. It lacks
pytest, so tests use the existing repository runtime without installing anything;
the initial missing-pytest receipt is preserved alongside the passing rerun.

Required closeout: Human/Agent Ledgers, Current State, Execution Log, Master
Context, Owner Register, Experiment Master, Stage Process, and README navigation
updated; [state V9](PAPER1_CORE144_PARALLEL_WORKSTREAM_STATE_V9.md) preserves D2/D3
Phase2 withheld. Lessons require no new methodological rule; Research Plan
Authority and long-term requirements remain unchanged because scope/contracts
did not change. Historic manifests/records/workbooks, Stage1–5 and Final72 remain
unchanged. Unrelated design Markdown and pre-existing PDF stay excluded.

No A/B consensus, Owner adjudication, GT, split, detector or calibration. A01's
existing authorization is unchanged; its actual delivery/return is not inferred.
Next: Owner sends only the two listed files to the same HUMAN-B01 annotator,
then returns the completed original without an intermediary Excel resave.
