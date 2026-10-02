# Core144 D1 HUMAN-A01 Phase1 raw lock and Phase2 release V1

Date: 2026-10-02
Status: `A01_PHASE1_RAW_LOCKED / A01_PHASE1_GATE_PASS / A01_PHASE2_RELEASE_AUTHORIZED / A01_PHASE2_NOT_YET_DISTRIBUTED / B01_PHASE1_IN_PROGRESS / B01_PHASE2_WITHHELD / NO_GT`

## Owner identity decision and immutable preservation

Owner identified the workbook whose received filename ended in `(2)` as the
actual HUMAN-A01 Phase1 return. The source was copied byte-for-byte without an
Excel open/save cycle into the following additive Git-external namespace:

`E:\LLMGuard-Handoff\paper1_core144_d1_human_a01_phase1_raw_lock_20261002`

| Item | Locked value |
|---|---|
| Canonical raw filename | `PAPER1_CORE144_D1_HUMAN_A01_PHASE1_RAW_RETURN_V1.xlsx` |
| Bytes | `36,361` |
| SHA256 | `d752d27451fcbae9ffba82b6bb33445452ef8b51e35f68877793687216f21b28` |
| Copy rule | byte-for-byte; no Excel resave |
| Filesystem state | read-only |
| Lock manifest | `PAPER1_CORE144_D1_HUMAN_A01_PHASE1_RAW_LOCK_MANIFEST_V1.json` |
| Validation receipt | `PAPER1_CORE144_D1_HUMAN_A01_PHASE1_VALIDATION_V1.json` |

The separately received workbook whose filename ended in `(3)` is not used as
HUMAN-A01's authoritative return. It is neither overwritten nor deleted by this
lock operation and remains separate routing/history evidence.

## Phase1 validation

The locked raw return has 144 rows, 144 unique HUMAN-A01 opaque IDs and the
original eight columns. ID order and Candidate text order exactly match the
distributed HUMAN-A01 Phase1 manifest. All five categorical columns use legal
canonical enum values. All 15 rows with at least one nondefault categorical
value have a nonblank `issue_note`; there are 15 nonblank notes in total.

| Field | Counts |
|---|---|
| `text_naturalness` | `NATURAL=143`, `UNNATURAL=1`, `MINOR_ISSUE=0` |
| `local_internal_conflict` | `NO=130`, `YES=14`, `UNCERTAIN=0` |
| `self_containment` | `PASS=144` |
| `ambiguous_referent` | `NO=144` |
| `meta_or_template_language` | `NO=144` |

No answer formula, hidden worksheet, macro or external-link part was found.
Every non-answer cell value/formula matches the original distribution workbook.
This is structural/process validation of the returned annotation artifact, not
an agreement calculation, adjudication or Ground Truth decision.

## A01 Phase2 release file

The prebuilt A01 Phase2 workbook satisfies its own frozen manifest and matches
the locked Phase1 return on all 144 opaque IDs, their order and Candidate text.
All 1,440 Phase2 answer cells remain blank. It contains 225 clickable official
Evidence URLs, no private mapping/label field, no hidden worksheet, no macro and
no external-link part.

| Item | Release value |
|---|---|
| Exact file | `E:\LLMGuard-Handoff\paper1_core144_d1_human_phase2_sealed_20260927\HUMAN-A01\PAPER1_CORE144_D1_HUMAN_A01_PHASE2_V1.xlsx` |
| Bytes | `527,949` |
| SHA256 | `76d43b8b48fbab4595b4d561bc09f41046a1ca5cd2f39118fd85de3875baef8a` |
| Release scope | `HUMAN-A01_ONLY` |
| Required return filename | `PAPER1_CORE144_D1_HUMAN_A01_PHASE2_RETURN_V1.xlsx` |

The exact Owner sending instructions are in
[the A01-only checklist](PAPER1_CORE144_D1_HUMAN_A01_PHASE2_OWNER_SEND_CHECKLIST_V1.md).
This authorization does not release B01 Phase2. B01 must independently finish,
return and pass lock/validation of the correct B01 Phase1 workbook first.

## Boundaries

- No Phase1 raw value was changed or normalized.
- No Phase2 answer was generated.
- No A/B comparison, consensus, adjudication or Ground Truth was produced.
- No B01 answer, package or release state was inferred from A01.
- No Candidate, opaque ID, row order, Evidence, schema or accepted protocol was changed.
