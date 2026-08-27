# S6.1-P1-PILOT2 Return Preflight Owner Correction

## Record identity

- Task ID: `S6.1-P1-PILOT2-RETURN-CORRECTION-01`.
- Date: `2026-08-27`.
- Record type: `OWNER_FACT_CORRECTION / SUPERSEDING_INTERPRETATION / GOVERNANCE_ONLY`.
- Owner decision: `PODR-063`.
- Owner requirement: `OR-025`.
- Auto Continue: `NO`.

## Preserved original evidence and inference

The following records remain immutable and must not be edited to make the issue appear never to have existed:

- original coordinator registration CSV, including its recorded timestamps and `NOT_DISTRIBUTED` values;
- original A/B Phase 1 and Phase 2 return ZIP files and their SHA256 identities;
- the original preflight inference that A Phase 2 appeared to begin before A Phase 1 was received;
- the original preflight workbook, SHA256
  `adeb458629cde0e275c621de7cac4f88bff2dc0a19751ed0ff2fb220c394bae0`.

Return identities preserved by the correction:

| Return | SHA256 |
| --- | --- |
| A Phase 1 | `c5976000abdbaf2bc66b002e0d1dfca0984653b48eea2127a76658fdf12b8ed2` |
| A Phase 2 | `bd11e6648e0657923312a3620a7eae42ef54f536d619f8a7574f50967f5a6cc0` |
| B Phase 1 | `e697f7d57520ed397cff6bf1f3502662f29cad3edce2ba1640fa3bdd8223224c` |
| B Phase 2 | `2eeedcedb53bd629e67ec2faa987279059fd88ee0297001ee4738306c2aec4ae` |

## Owner-confirmed operational fact

The project owner manually confirmed the actual order:

1. Annotator A completed and submitted `A01_phase1_stealth`.
2. The coordinator received the Phase 1 return.
3. The Phase 1 return was locked.
4. Only after that lock was `A01_phase2_fact_version` distributed to Annotator A.
5. Annotator A did not see Phase 2 materials while performing Phase 1.

Therefore:

```text
A_PHASE1_DISTRIBUTION_ORDER = OWNER_CONFIRMED_CORRECT
A_PHASE1_STRICT_BLINDNESS = PRESERVED_BY_OWNER_CONFIRMED_OPERATIONAL_FACT
REGISTRATION_TIMESTAMP_STATUS = INCORRECT_RECORDING / DOCUMENTATION_DEFECT_ONLY
```

The original blind-contamination inference was based on incorrect registration metadata and is superseded by owner-confirmed
actual distribution order. This superseding interpretation does not delete or rewrite the original registration metadata or the
historical preflight inference.

## Corrected blocker interpretation

`PILOT2-RETURN-PROTOCOL-BLOCKER-01` must no longer be described as irreversible blind contamination. Its current interpretation is:

```text
PILOT2-RETURN-PROTOCOL-BLOCKER-01 = PROTOCOL_AND_ANNOTATION_SCHEMA_BLOCKER
BLINDNESS_SUBISSUE = RESOLVED_BY_OWNER_CONFIRMED_ACTUAL_DISTRIBUTION_ORDER
REGISTRATION_METADATA_SUBISSUE = OPEN_FOR_CORRECTION_AND_EVIDENCE_BINDING
ANNOTATION_SCHEMA_SUBISSUE = OPEN
RETURN_FILE_CONTRACT_SUBISSUE = OPEN
FORMAL_AGREEMENT = PENDING_SCHEMA_V2_REREVIEW_AND_RETURN_VALIDATION
Auto Continue = NO
```

Round 1 remains eligible as a future formal-agreement candidate; it is not currently accepted agreement evidence and no agreement
or adjudication is established by this correction.

## Remaining open issues

- `YES / NO / UNCERTAIN` semantics are ambiguous and lack `NOT_APPLICABLE` where applicability is conditional.
- `authority_matches`, `version_relation_correct`, and `legitimate_update_or_history` require explicit applicability rules.
- all four independence declarations remain incomplete and unbound to return SHA256 identities;
- coordinator registration metadata remains incorrect and requires an additive correction/evidence-binding record;
- returned annotation CSVs are GB18030 rather than the frozen UTF-8 BOM contract;
- B changed frozen headers;
- B Phase 1 lacks `time_seconds`;
- B Phase 2 lacks 21 `professional_lookup_used` values;
- lookup source-type classification contains an incorrect official-source classification;
- owner-confirmed normalization `YEAS -> YES` applies only in derived analysis; the raw return remains immutable.

## Next gate and prohibited continuation

The preferred next route is `ANNOTATION_SCHEMA_V2 + A/B INDEPENDENT RE-REVIEW`, not
`STRICT_RERUN_WITH_NEW_ANNOTATORS`. This is a priority decision, not execution approval. A separate approved task must freeze the
Schema V2 applicability/enumeration contract, correction/evidence-binding procedure and re-review package before work begins.

Before that approval, do not calculate formal agreement, generate a disagreement packet, execute owner adjudication, modify any raw
return, contact RTX5090, freeze the Dataset, implement the Detector, train a model or start a Formal Experiment.
