# Paper 1 Formal240 Annotation Guide V4.2 — Owner version-scope decision

Status: `OWNER_APPROVED_FORWARD_ONLY_CLARIFICATION / ENUMS_UNCHANGED`. Owner directive SHA256 `e6553e08cf05567ed1ab9598b5f18c3a08dfb17e50ca8e4954e10cc6a6554f39` (16,679 bytes) is preserved in the private `paper1_formal240_d1_canary_v4_2_owner_semantic_freeze_20260926` namespace. This additive decision supplements [V4](PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md) and [V4.1](PAPER1_FORMAL_ANNOTATION_GUIDE_V4_1_CLARIFICATION.md); it does not modify either guide, Schema V4, a candidate, frozen E1/E2, or any historical reviewer raw. It applies prospectively to Formal240 and to the current fifteen Phase2 disagreements through a separate Owner-semantic overlay. It is **not** Ground Truth.

## Candidate-only version-presence test

Before evaluating whether a version claim is correct, ask: **Does the candidate text itself explicitly assert a document-version proposition?** Evidence metadata may establish whether an asserted claim is correct; it must not create a claim that the candidate did not make. An official page showing “现行有效”, publication/effective dates or history does **not** make a bare article citation into a version assertion.

`version_claim_status=NOT_PRESENT` when the candidate merely names a law or article and states a substantive number, condition, subject, obligation, exception, benefit or procedure. “《某法》第X条规定……” and “依《某条例》第X条……” do not by themselves assert that the law is the current or a specific historical edition. A wrong substantive number can make `overall_fact_status=FACTUAL_CONFLICT` while version stays `NOT_PRESENT`.

Version presence requires explicit revision/amendment, repeal, replacement/supersession, effective/expiry transition, current/historical status, version identity, predecessor/successor relation or version binding in the **candidate**. Once presence is established, choose `PRESENT_CORRECT`, `PRESENT_INCORRECT` or `PRESENT_EVIDENCE_INSUFFICIENT` using only the supplied frozen Evidence. A wrong institutional actor remains a separate `authority_claim_status` question; wrong substantive content alone does not make version incorrect.

Adoption, meeting passage, an order number, promulgation and publication alone remain `NOT_PRESENT` for version. But a candidate that names an **amendment decision** such as “《关于修改〈某条例〉的决定》” explicitly asserts amendment-document identity even if it also gives only its meeting/publication details. That version claim is present; the frozen Evidence determines correctness.

## Overall status for explicit two-version comparison

If a supported statement explicitly compares an original/historical version with a revised/newer version, and its truth or core meaning depends on those bindings, `overall_fact_status=LEGITIMATE_VERSION_OR_HISTORY`. A true historical comparison does not become `CURRENTLY_CONSISTENT` merely because someone can still accurately state it today. Operational check: remove the version qualifiers; if the comparison loses its original meaning, the historical/version context is essential. A supported ordinary current substantive rule without historical/version qualification remains `CURRENTLY_CONSISTENT`. Evidence-insufficient and factual-conflict cases still follow V4's earlier decision order.

## Boundary teaching patterns — invented, not D1 answers

| Candidate pattern | Field boundary |
| --- | --- |
| “《示例培训法》第八条规定，申请人提交两份材料。” | Bare article and substantive rule: version `NOT_PRESENT`. |
| “《示例培训办法》经委员会会议通过，以第12号令公布。” | Adoption/publication only: version `NOT_PRESENT`; assess authority separately. |
| “《关于修改〈示例培训办法〉的决定》经委员会会议通过。” | Amendment-decision identity: version `PRESENT_*`, with exact correctness dependent on frozen Evidence. |
| “《示例培训法》2010年修订版规定申请人提交两份材料。” | Explicit edition identity: version `PRESENT_*`; the material-count assertion is judged separately. |
| “现行《示例培训法》规定申请人提交两份材料。” | Explicit current-version status: version `PRESENT_*`. |
| “对照2003年原版与2010年修订版《示例培训办法》，该补助标准提高。” | If both frozen versions support the comparison: overall `LEGITIMATE_VERSION_OR_HISTORY`. |
| Candidate only says “《示例培训法》第八条规定……”; Evidence page displays “现行有效”. | Candidate version remains `NOT_PRESENT`; Evidence metadata cannot reverse-create a claim. |

These patterns stipulate no actual law or evidence outcome. They are teaching material only and must not enter the Formal240 candidate population or reviewer-answer key.

## Current Canary and methodological boundary

The current R3/R4 Phase2 disagreement exposed an `EVIDENCE_METADATA_TO_CANDIDATE_CLAIM` reverse-propagation risk: seeing official version metadata may lead a reviewer to over-label a candidate that only states a substantive rule. Owner clarified the **global rule**, then authorized a mechanically applied, case-verified [fifteen-field overlay](PAPER1_FORMAL_D1_CANARY_PHASE2_OWNER_SEMANTIC_ADJUDICATION_OVERLAY_V1.json). This does not mean “R3 was correct” or “R4 was wrong”; their raw judgments retain their original provenance. The [targeted package](PAPER1_FORMAL_D1_CANARY_PHASE2_15ITEM_TARGETED_REREVIEW_PACKAGE_V1.json) tests whether the same two reviewers can apply V4.2 consistently; it is rule-confirmation, not fresh independent annotation. The earlier 24-row raw and V4/V4.1 remain immutable. No Canary acceptance, Human A/B release, other D1 groups, split, GT or training follows automatically.
