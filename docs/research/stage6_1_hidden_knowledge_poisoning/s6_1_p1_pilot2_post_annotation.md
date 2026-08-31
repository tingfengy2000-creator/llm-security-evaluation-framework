# S6.1-P1-PILOT2-POST-ANNOTATION

## 1. Scope and authority

- Task: `S6.1-P1-PILOT2-POST-ANNOTATION`.
- Date: `2026-08-31`.
- Machine: `LOCAL / CONTROL_PLANE`.
- Owner authority: `PODR-068 / OR-030`.
- Approved work: targeted return validation, A/B V2 formal agreement, disagreement classification, and a disagreement-only
  owner adjudication packet.
- Prohibited work: raw-return mutation, automatic adjudication, Ground Truth lock, Dataset freeze, Detector, Training, 5090,
  Formal Experiment, Paper Result or SOTA claim.

`V2_REREVIEW_VALUE` supersedes the same annotator's V1 value. V1 remains revision-history evidence only. A/B agreement uses
`A_V2_CURRENT_VALUE` versus `B_V2_CURRENT_VALUE`, matched by `sample_id + field` within each phase. Phase1 and Phase2 use
phase-specific sample IDs; cross-phase schema checks bind the unchanged candidate text identity.

## 2. Immutable inputs

| Return | Authoritative path | SHA256 | Records / samples |
| --- | --- | --- | --- |
| A Phase1 | `LLMGuard-Handoff/paper1_pilot2_targeted_rereview_20260827/annotator_A/A_phase1_targeted_rereview.xlsx` | `9e301816bfdd00a0028719679d629b8518bfc21dd9ce70c231de4b4ad7690424` | `108 / 36` |
| A Phase2 | `LLMGuard-Handoff/paper1_pilot2_targeted_rereview_20260827/annotator_A/A_phase2_targeted_rereview.xlsx` | `b7865999655928e574d946852245a9a3fe5ee4817df6c593ce2ea339dfc95096` | `252 / 36` |
| B Phase1 | `LLMGuard-Handoff/paper1_pilot2_targeted_rereview_correction01_20260828/annotator_B/B_phase1_targeted_rereview.xlsx` | `f4e1864e7f47c231f006c7a8750421129f4438e6e49164bd7760edd3e6392c8d` | `108 / 36` |
| B Phase2 | `LLMGuard-Handoff/paper1_pilot2_targeted_rereview_20260827/annotator_B/B_phase2_targeted_rereview.xlsx` | `0572a0c6aaf60a200755ae4de4de651b80bfb661ddc15eaeda598e0e9310989d` | `274 / 36` |

The unfilled `20260827/annotator_B/B_phase1_targeted_rereview.xlsx` is not a human return and was excluded. All four selected
workbooks opened successfully and had complete, legal V2 values, unique `sample_id + field` records and matching A/B sample sets
within phase. The source XLSX files were not modified.

The raw A/B Phase1 declarations contain `sample_id_changed=YES`; the owner explicitly corrected both effective process values to
`NO`. This correction is additive metadata only and does not rewrite the XLSX files.

## 3. Return validation

`RETURN_VALIDATION = PASS_FOR_AGREEMENT_WITH_NON_SEMANTIC_DEFECTS`.

- Blocking missing/illegal V2 values: `0`.
- A Phase2: one blank REVISE reason on `overall_fact_status`; the V2 value is legal.
- B Phase1: header A1 is blank, but all 108 task IDs and records remain intact.
- B Phase2: 72 known historical V1 display-mapping defects for `version_relation_correct` and `authority_matches`, plus two blank
  process/revision reasons. V2 values remain authoritative under the owner-frozen V2-over-V1 rule.
- B Phase2 process metadata: one Google Search URL remains classified `OFFICIAL_PRIMARY_SOURCE` instead of `SEARCH_ENGINE`.
  This is `PROCESS_METADATA_ONLY` and does not alter Ground Truth.
- Row order was ignored; A/B matching used `sample_id + field`.

These defects are preserved in the validation manifest; none was silently corrected and none caused a third blanket annotation
round.

## 4. Formal agreement on A/B V2 current values

| Phase | Field | Total N | Applicable N | Presence disagreement N | Exact agreement | Cohen's κ | Interpretation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Phase1 | `locally_detectable` | 36 | 36 | 0 | 28/36 = 77.8% | -0.075 | prevalence-sensitive; owner review required |
| Phase1 | `cross_document_evidence_needed` | 36 | 36 | 0 | 30/36 = 83.3% | 0.658 | Pilot estimate |
| Phase1 | `assigned_stealth_level` | 36 | 36 | 0 | 20/36 = 55.6% | 0.375 | substantive disagreement |
| Phase2 | `version_relation_present` | 36 | 36 | 0 | 34/36 = 94.4% | -0.029 | severe prevalence effect |
| Phase2 | `version_relation_correct` | 36 | 34 | 2 | 32/34 = 94.1% | 0.871 | applicable subset only |
| Phase2 | `history_or_update_claim_present` | 36 | 36 | 0 | 30/36 = 83.3% | 0.667 | Pilot estimate |
| Phase2 | `legitimate_update_or_history` | 36 | 18 | 6 | 16/18 = 88.9% | 0.788 | applicable subset only |
| Phase2 | `authority_claim_present` | 36 | 36 | 0 | 35/36 = 97.2% | 0.654 | Pilot estimate |
| Phase2 | `authority_matches` | 36 | 1 | 1 | 1/1 = 100.0% | N/A | `KAPPA_NOT_INTERPRETABLE_DUE_TO_SMALL_APPLICABLE_N` |
| Phase2 | `overall_fact_status` | 36 | 36 | 0 | 32/36 = 88.9% | 0.769 | substantive disagreement remains |

Conditional correctness is calculated only where both annotators set the corresponding presence field to `YES`. Presence
disagreement is classified as applicability disagreement, not correctness disagreement. These Pilot statistics are not a formal
Benchmark quality claim.

## 5. Disagreement and adjudication gate

- A/B V2 disagreement records: `47`.
- A/B classification: `24 STEALTH_LEVEL_DISAGREEMENT`, `9 APPLICABILITY_DISAGREEMENT`,
  `6 CROSS_DOCUMENT_COMPLEXITY_DISAGREEMENT`, `4 FACTUAL_EVIDENCE_DISAGREEMENT`, and
  `4 VERSION_HISTORY_INTERPRETATION`.
- Intra-annotator schema-logic conflicts: `37`, including `31 STEALTH_SCHEMA_LOGIC_CONFLICT` and
  `6 CONDITIONAL_APPLICABILITY_LOGIC_CONFLICT`.
- Minimal owner packet: `84` issue rows covering `26` unique candidate texts. Agreement-only candidates are excluded.

Git-external output root:

`LLMGuard-Handoff/paper1_pilot2_post_annotation_20260831`

The owner workbook is `minimal_owner_adjudication_packet.xlsx`, SHA256
`67081c0e3f7c32d42041ccc736316ed2f42fa979d417a76f577b4e90418d363a`. The directory also contains return-validation,
agreement, sample-level and issue-level CSV/JSON plus `evidence_index.sha256`; the index validates `11/11` entries.

## 6. Final status and claims boundary

```text
RETURN_VALIDATION = PASS_FOR_AGREEMENT_WITH_NON_SEMANTIC_DEFECTS
FORMAL_AGREEMENT_V2 = COMPLETED_ON_A_B_V2_CURRENT_VALUES
OWNER_ADJUDICATION = REQUIRED / NOT_EXECUTED
GROUND_TRUTH_CANDIDATE = NOT_GENERATED / BLOCKED_PENDING_OWNER_ADJUDICATION
POST_ANNOTATION_EXPERIMENT = NOT_AUTHORIZED
DATASET = NOT_FROZEN
DETECTOR = NOT_STARTED
TRAINING = NOT_STARTED
FORMAL_EXPERIMENT = NOT_STARTED
AUTO_CONTINUE = NO
```

Next gate: the project owner completes only the 26-candidate adjudication packet. No Ground Truth candidate, dataset or experiment
may proceed before that owner decision is returned and separately validated.
