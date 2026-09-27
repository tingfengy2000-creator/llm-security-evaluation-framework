# D1 remaining90 Phase1 — corrected R3/R4 raw lock, QA and auxiliary-review gate

Status (2026-09-27): `R3_R4_PHASE1_RAW_LOCKED / STRUCTURAL_QA_PASS / SUBSTANTIVE_DISAGREEMENT_PENDING / PHASE2_WITHHELD`. This is pre-annotation quality review, not Formal Ground Truth or D1 pre-annotation acceptance. No hidden C/P/H, HKP, target/derived S, Expected, mapping, Owner construction result or Phase2 Evidence was loaded for this comparison.

## Superseding input and immutable provenance

Owner explicitly withdrew the earlier message that mistakenly supplied `PAPER1_FORMAL_D1_REMAINING90_R3_GPT_PHASE1_ISOLATION_INCIDENT_V1.json`. A read-only copy had already been made in `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining90_phase1_r3_incident_r4_raw_lock_20260927`, SHA256 `b4e5a0d256f689b0ebf70ba8840e0faca3bc3b9be1b3d78cedc6790aa83b412d`. Preserve it as `WITHDRAWN_WRONG_ATTACHMENT / NOT_CURRENT_R3_RUN_EVIDENCE`, **not** as proof that this R3 Phase1 run failed isolation. Its presence does not override the corrected Owner message or the new R3 raw return. Do not delete or silently reuse it.

The authoritative corrected pair was copied byte-for-byte to read-only `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining90_phase1_r3r4_raw_lock_run02_20260927` at `2026-09-27T05:43:49.4938994Z`:

| Reviewer | Locked filename | Bytes | SHA256 |
| --- | --- | ---: | --- |
| R3-gpt | `PAPER1_FORMAL_D1_REMAINING90_R3_GPT_PHASE1_RAW_RETURN_V1.json` | 23457 | `36a14d40f530bd2f9566f18f36acdce07a11a43b0c56142b8bb41e6af84f1e14` |
| R4-codex code / Doubao platform | `PAPER1_FORMAL_D1_REMAINING90_R4_CODEX_PHASE1_RAW_RETURN_V2.json` | 24302 | `d3aa0c1470b5dffab91217157a6b808f73531ae9fc3bbee21ef8626500759f04` |

Owner separately confirmed the corrected R3 run used a fresh isolated GPT session with only its authorized Phase1 package/schema/prompt and no web or other AI: `OWNER_ATTESTED`, not platform-log proof. R4's additional statement says its Doubao run was fresh and isolated and accessed only its authorized three files. This is `REVIEWER_SELF_ATTESTED` unless separately confirmed by Owner. The code `R4-codex` remains a stable identifier, not a model claim.

## Mechanical QA before hidden construction load

The inspectable validator is `scripts/formal240_remaining90_phase1_validate.py`; machine output is the read-only private `qa/PAPER1_FORMAL_D1_REMAINING90_PHASE1_R3_R4_QA_V1.json`, SHA256 `a7b49c64fedac84543fb6df7e31e4c5bc8036421017ce107efd21cce028094a9`. Both original files: strict UTF-8 JSON without BOM or duplicate keys; exactly 90 records, 90 unique IDs, exact reviewer-specific ID set/order, seven keys in canonical order, legal enums, string fields and required notes all pass. R3 and R4 candidate-only packets have exact ID/text-set parity. R3 packet SHA256 `4d4c346bebb7933af6c5bdd7a7c7e5b4f6619b7f36508d80520015d2c5d516ed`; R4 packet SHA256 `9097342b22fa27dafba3258129a31edf563ecb67017894b5b2c13cd2528b3a8a`; common Schema SHA256 `a91ab57b2eab2123f07fff7c97f7da01f904d05d900c3ffd9a0cdea54b04efa5`.

| Field | R3 distribution | R4 distribution | Exact agreement |
| --- | --- | --- | ---: |
| `text_naturalness` | 84 `NATURAL`, 6 `MINOR_ISSUE` | 90 `NATURAL` | 84/90 |
| `local_internal_conflict` | 83 `NO`, 7 `YES` | 79 `NO`, 11 `YES` | 86/90 |
| `self_containment` | 90 `PASS` | 90 `PASS` | 90/90 |
| `ambiguous_referent` | 90 `NO` | 90 `NO` | 90/90 |
| `meta_or_template_language` | 90 `NO` | 90 `NO` | 90/90 |

`issue_note` is free text, not a field for literal exact-match agreement. R3 has 12 nonblank flagged notes and R4 has 11; every note/flag rule passes. R4's separately supplied descriptive counts are confirmed by raw-file computation, but its summary is not used as the source of record.

## Candidate-only disagreement triage

Six naturalness disagreements (`D1BR-7F2FFE8B0B69`, `D1BR-AFAC6C1524F3`, `D1BR-88F9543EBF7B`, `D1BR-9966C6FDD551`, `D1BR-156165CA568A`, `D1BR-9A33FC80EF11`) are R3 `MINOR_ISSUE` versus R4 `NATURAL`. R3 cites slight wording or sentence-structure awkwardness while still finding the claim understandable; no self-containment, referent or meta-language defect was identified by either reviewer. Treat as **provisional expression-boundary variance**, not an automatic Candidate repair or a reason to rewrite raw.

Four substantive `local_internal_conflict` disagreements (`D1BR-FB2590D87D27`, `D1BR-194520C78747`, `D1BR-566391C110ED`, `D1BR-67D572512767`) are R3 `NO` versus R4 `YES`. In each visible Candidate, the same document's promulgating organ is explicitly asserted as both one institution and another. Under the existing candidate-only same-subject/scope/time/condition test, this is a plausible internal contradiction; R3 left no explanatory note for its `NO`. The repeated sentence surface across four candidates also merits a style-shortcut check after blind review. Do **not** automatically declare either reviewer the final authority, edit either raw return, or silently change construction labels. These four are a material unresolved Phase1 gate pending bounded Owner adjudication or additional independent review.

## Claude auxiliary path and release boundary

At Owner's suggestion, a separate R5-claude **auxiliary** Phase1 package was created in `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining90_claude_aux_phase1_20260927\reviewer_release`, containing exactly ten selected opaque IDs and Candidate texts, a ten-row import schema and one common prompt. The selected union is derived solely from R3/R4 categorical differences in R3 packet order. Packet SHA256 `4ec24e2a2e432fbd7e12104f14a4d75eec3a80aea1ca68318ce24008645555b2`; Schema SHA256 `c53d527652fbc5d2415ec7e11b1a2654e7a8f116482f193fe736d505a53e43e9`; prompt SHA256 `31b0c1b61507adc09ba97ffca6dc3933afb474eab578436173d804b1fee9e8bc`. Private manifest SHA256 `2787749eec99c56ae7022ae106d115b4fb382a283b5980644596eee1746d068e` is **not** for Claude. Release files contain no previous reviewer values, hidden labels, Evidence or Phase2. Claude's answer is not Ground Truth and cannot by majority vote rewrite R3/R4. Owner adjudicates any material remaining conflict after its raw is locked and validated.

Until that decision and any candidate-side style/defect check: `PHASE2_RELEASE_AUTHORIZED=FALSE`. No Human A/B, GT, split, training or formal result is authorized.
