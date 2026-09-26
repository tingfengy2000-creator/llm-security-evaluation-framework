# Formal D1 Canary V4.2 targeted rule-stability intake

Status: `VERSION_SCOPE_RULE_STABILITY_PASS / CANARY_OWNER_ACCEPTANCE_PENDING / HUMAN_AB_NOT_AUTHORIZED`.

This is the original R3-gpt and R4-codex sessions' **targeted confirmation of 15 Owner-clarified fields**, not a new independent blind annotation round, Ground Truth, or Canary acceptance. Owner attested that both original isolated sessions received the same 15-item package and V4/V4.1/V4.2 rules and saw neither each other's answers nor the Owner overlay. Session isolation and access scope are `OWNER_ATTESTED`, **not machine verified**.

## Immutable return intake

The source files were copied byte-for-byte, without parsing/resaving, to the new read-only Git-external namespace `E:\LLMGuard-Handoff\paper1_formal240_d1_canary_v4_2_targeted_raw_lock_20260926`. Source and locked bytes are identical:

| Reviewer | Raw filename | Bytes | SHA256 |
| --- | --- | ---: | --- |
| R3-gpt | `PAPER1_FORMAL_D1_R3_GPT_PHASE2_V4_2_TARGETED_RETURN.json` | 4,655 | `24bf845e98e2fae8c9193fac8c584be1e7a36130ff2b595d3a88c1ced4f9885a` |
| R4-codex | `PAPER1_FORMAL_D1_R4_CODEX_PHASE2_V4_2_TARGETED_RETURN.json` | 5,699 | `e2eefbc4435a6cf250a3e1b67e5e337927c4d738e957bf461d9772fa14343fe8` |

Raw lock verified at `2026-09-26T05:07:12Z`. Both are strict UTF-8 JSON arrays without BOM or duplicate keys. Each passes 15 rows, exact four-key schema, 15 unique blind IDs, frozen-package ID/order/target-field parity, canonical values, and nonblank reasons. The [validation artifact](PAPER1_FORMAL_D1_CANARY_V4_2_TARGETED_R3_R4_VALIDATION_V1.json) is reproducible with [validator](../../../../scripts/research/validate_formal_d1_v4_2_targeted_returns.py); it contains a per-ID comparison and hashes of both reasons, not rewritten raw answers.

## Bounded comparison

The [targeted package](PAPER1_FORMAL_D1_CANARY_PHASE2_15ITEM_TARGETED_REREVIEW_PACKAGE_V1.json) SHA is `92360d2415687129521c92df2cf3be0898b8e3b800f14ea48d5e82fa664ed6dc`. Both returns were structurally validated before loading the [Owner semantic overlay](PAPER1_FORMAL_D1_CANARY_PHASE2_OWNER_SEMANTIC_ADJUDICATION_OVERLAY_V1.json), SHA `f5c4c899de2e48c9c453a857e22bfba065fb2020aba71fc057532d994ced9b8e`, for post-lock comparison.

- `version_claim_status`: 13/13 R3/R4 target values agree and match the Owner overlay: 12 bare substantive claims are `NOT_PRESENT`, one explicit amendment-decision identity is `PRESENT_CORRECT`.
- `overall_fact_status`: 2/2 agree and match the Owner overlay: the supported historical-version comparisons are `LEGITIMATE_VERSION_OR_HISTORY`.
- Total categorical target agreement: 15/15. Disagreement IDs: none. Overlay mismatch IDs: none. The 30 submitted short reasons were reviewed as explanations of these target fields; no new blocking factual or Evidence-pool claim was identified in this **bounded** review. Different wording was not treated as a mismatch.

The result supports V4.2 **rule stability in these original sessions**. It does not retroactively rewrite their first 24-row Phase2 returns or establish performance on new annotators. Raw R3/R4 first returns, the Owner overlay, Candidate V3 and frozen E1/E2 stay unchanged. R5 remains optional/non-gating.

## Gate and next action

`D1_CANARY_TARGETED_VERSION_SCOPE_GATE=PASS` is narrower than `D1_CANARY_ACCEPTED`. The Owner must separately inspect the accumulated Candidate/Evidence/Phase1/Phase2/repair/view-QA record and explicitly accept or return the Canary. Until that decision, do not generate Human A/B packages, remaining 40 D1 groups, Ground Truth, split, detector training, or formal results. `Auto Continue=NO`.
