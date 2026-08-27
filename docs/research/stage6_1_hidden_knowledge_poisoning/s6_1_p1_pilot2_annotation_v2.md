# S6.1-P1-PILOT2-ANNOTATION-V2

## 1. Task identity and boundary

- Task: `Pilot2 Annotation Schema Repair and Round1 Independent Re-review`.
- Machine: `本机`.
- Owner decisions: `PODR-064 / OR-026`.
- Base commit: `561750c6fc5706582dc547cc000271b981abed85`.
- Status: `ANNOTATION_SCHEMA_V2 = IMPLEMENTED`；`A_B_REREVIEW = READY_FOR_HUMAN_EXECUTION`.
- This task prepares the measurement contract and four independent re-review packages. It does not calculate agreement, generate a
  disagreement packet, adjudicate a label, contact 5090, freeze Dataset, implement Detector, start Training or run a Formal
  Experiment.

## 2. Additive owner correction and preserved history

The four raw return ZIPs, original GB18030 bytes, original headers and missing values, declarations, lookup logs, coordinator
registration metadata, original preflight workbook, timestamp-based inference and blocker snapshot remain immutable. The owner
correction is additive:

- `A_PHASE1_DISTRIBUTION_ORDER = OWNER_CONFIRMED_CORRECT`;
- `A_PHASE1_STRICT_BLINDNESS = OWNER_CONFIRMED_PRESERVED`;
- `REGISTRATION_TIMESTAMP_STATUS = INCORRECT_RECORDING / DOCUMENTATION_DEFECT_ONLY`;
- the original blind-contamination inference was based on incorrect registration metadata and is superseded by owner-confirmed
  actual distribution order.

The raw identities are:

| Return | SHA256 |
| --- | --- |
| A Phase1 | `c5976000abdbaf2bc66b002e0d1dfca0984653b48eea2127a76658fdf12b8ed2` |
| A Phase2 | `bd11e6648e0657923312a3620a7eae42ef54f536d619f8a7574f50967f5a6cc0` |
| B Phase1 | `e697f7d57520ed397cff6bf1f3502662f29cad3edce2ba1640fa3bdd8223224c` |
| B Phase2 | `2eeedcedb53bd629e67ec2faa987279059fd88ee0297001ee4738306c2aec4ae` |

The original preflight workbook remains SHA256
`adeb458629cde0e275c621de7cac4f88bff2dc0a19751ed0ff2fb220c394bae0`.
The raw typo `YEAS` remains unchanged；only derived V2 mapping records `YEAS -> YES` under `NORMALIZATION_RULE`. A Google search
results URL maps to `SEARCH_ENGINE`, never to an official-source type.

## 3. V2 executable contract

The executable contract is implemented in
[`annotation_v2.py`](../../../src/llmguard/domains/retrieval/hidden_poisoning/annotation_v2.py). It freezes Phase1/Phase2 column
order, response enums, lookup source types, retrospective declarations, revision reason codes, automatic applicability rules and
template/completed-response validation.

Conditional fields use `YES / NO / UNCERTAIN / NOT_APPLICABLE`. The three automatic rules are:

1. `version_relation_present = NO -> version_relation_correct = NOT_APPLICABLE`;
2. `history_or_update_claim_present = NO -> legitimate_update_or_history = NOT_APPLICABLE`;
3. `authority_claim_present = NO -> authority_matches = NOT_APPLICABLE`.

`claim_matches_source` and `fact_changed` are always applicable and reject `NOT_APPLICABLE`. `authority_matches` judges the
authority proposition expressed by the candidate, not the publisher of the page. `professional_lookup_used` is a process field；an
unrecoverable historical value is never inferred and must use `MISSING_NOT_RECOVERABLE` with the same `issue_flag`.

Future agreement logic is prepared but not executed. Conditional correctness is calculated only on the subset where both annotators
independently mark the corresponding `*_present = YES`. Applicability disagreement is reported separately；small applicable subsets
must not produce an interpreted kappa.

Every field passed `ANNOTATION_FIELD_APPLICABILITY_REVIEW`: universal/conditional applicability, no-applicability encoding,
YES/NO proposition, UNCERTAIN versus NOT_APPLICABLE, missing-mention behavior, need for a present field, three examples, simulated
interpretation risk, agreement subset and paper/data value. A future field with any unanswered item must stop at
`FIELD_SCHEMA_REVIEW_BLOCKER` and cannot enter human annotation.

## 4. Re-review package identity

Git-external handoff key:
`LLMGuard-Handoff/paper1_pilot2_round1_rereview_v2_20260827`.

| Package | Bytes | SHA256 |
| --- | ---: | --- |
| `A_round1_phase1_review_v2.zip` | 11325 | `0a8962266c77e83e6251a98b98abeca72546d1769d324e7f9a2ba964e87408a0` |
| `A_round1_phase2_review_v2.zip` | 17612 | `e3f7127bee345198f318eb8a79d5d98947c5e664e4c413c0aaa60e98c1eaf46e` |
| `B_round1_phase1_review_v2.zip` | 12332 | `3391ffc76c289de3fb69c1b539d84f98af20a628d3c88c40de7c6297f7b2ddf5` |
| `B_round1_phase2_review_v2.zip` | 18693 | `74390b5c20b92b4817b4bd1f5e52287616dd75ef760dc615803d2ec7ecf9f626` |

Each package contains only that annotator's V1 read-only reference, a blank V2 response table, a per-field `KEEP/REVISE` log, a
retrospective declaration and, for Phase2, a lookup-source review table. All V2 CSVs are UTF-8 BOM. A package contains no B data；B
contains no A data；neither contains evaluator-only mapping or label intent.

Coordinator files contain the complete field dictionary, four-value semantics, authority/version/history examples, overall fact
decision tree, Phase1 definitions, return register and owner correction notice. Owner-only files bind raw evidence, the correction,
V1-to-V2 mapping, package identities, quality gate and the original blocker snapshot.

## 5. Validation and completion state

- Raw ZIP SHA: `4/4 PASS`；original preflight workbook unchanged.
- A/B sample IDs and candidate text: `36/36 PASS` for each phase.
- UTF-8 BOM, frozen columns, package separation and evaluator-only leakage: `PASS`.
- Authority/version/history applicability, automatic `NOT_APPLICABLE`, response enums and schema validators: `PASS`.
- Targeted executable validation: `15 passed` before E-drive copy；the destination copy matched all 19 source file SHA256 values.
- `PILOT2_ROUND1_RAW = PRESERVED_IMMUTABLE`.
- `ANNOTATION_SCHEMA_SUBISSUE = REMEDIATION_IN_PROGRESS` until human V2 returns pass validation.
- `FORMAL_AGREEMENT_V2 = NOT_YET_ESTABLISHED`.
- Dataset `NOT FROZEN`；Detector `NOT IMPLEMENTED`；Training and Formal Experiment `NOT STARTED`.

## 6. Exact next gate

Coordinator sends only A packages to A and only B packages to B. Each annotator independently completes Phase1 V2, the per-field
change log and retrospective declaration；the coordinator locks each returned file and SHA256. The same independent procedure then
applies to Phase2, including lookup-source review. After all four V2 returns are locked, stop and request a separate owner approval for
return validation and any agreement calculation. `Auto Continue = NO`.
