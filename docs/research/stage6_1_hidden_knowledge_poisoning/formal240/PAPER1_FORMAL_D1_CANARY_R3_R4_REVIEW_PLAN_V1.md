# D1 Canary fresh R3/R4 independent blind review plan V1

Historical plan, superseded **only for fresh reviewer naming, platform isolation and the both-Phase1-lock release gate** by the additive [R3-gpt/R4-codex V2 plan](PAPER1_FORMAL_D1_CANARY_R3_GPT_R4_CODEX_REVIEW_PLAN_V2.md). The V1 text below is retained as the pre-rename record; do not distribute its old prompts as current authority.

Status: `PLAN_READY / NOT_DISTRIBUTED / CANARY_ACCEPTANCE_PENDING`. Owner requires two **new** independent GPT sessions/accounts; reusing the old R1/R2 sessions or merely relabeling their answers is prohibited. The Owner/coordinator records an opaque account/session identifier for each slot, verifies they differ, and keeps review-run metadata separate from all candidate-level fields. Neither reviewer sees any earlier R1/R2 raw return, diagnostic difference, incident record, Owner packet, hidden mapping or construction labels. This control-plane plan must not be included in reviewer packets.

| Gate | R3 | R4 | Required proof |
| --- | --- | --- | --- |
| Fresh isolated session assigned | Required | Required | Distinct opaque session/account identity, no shared context |
| Phase1 candidate-only distribution | Frozen Phase1 V2 | Frozen Phase1 V2 | Packet SHA256 `7967437231a4bc3990a7cd870a3dc8117517948f92a73bcc2dae79c3df8170ac`; import schema V2 |
| Phase1 raw return | Lock before Phase2 | Lock before Phase2 | 24/24 exact ID/order/schema/enum, source bytes/SHA/time, no overwrite |
| Phase2 release | Only after that reviewer's Phase1 lock | Same | Frozen Phase2 V3 packet plus V4.1 field clarification, same package hashes/wording across reviewers |
| Phase2 raw return | Lock separately | Lock separately | 24/24 validation, bytes/SHA/time, reviewer-run provenance |
| Inter-reviewer QA | After all four locks | After all four locks | Genuine R3/R4 agreement, issue triage, blocker resolution, Owner Canary decision |

Use the paired [R3 Phase1](PAPER1_FORMAL_D1_R3_BLIND_REVIEWER_PROMPT_PHASE1_V4_1.md), [R4 Phase1](PAPER1_FORMAL_D1_R4_BLIND_REVIEWER_PROMPT_PHASE1_V4_1.md), [R3 Phase2](PAPER1_FORMAL_D1_R3_BLIND_REVIEWER_PROMPT_PHASE2_V4_1.md), and [R4 Phase2](PAPER1_FORMAL_D1_R4_BLIND_REVIEWER_PROMPT_PHASE2_V4_1.md) prompts. Within each phase, the two prompts differ only in reviewer slot. The Phase1 prompts do not distribute Phase2 evidence or its field guide. The Phase2 prompts apply [V4.1 clarification](PAPER1_FORMAL_ANNOTATION_GUIDE_V4_1_CLARIFICATION.md) as a common field guide while keeping the original candidate/evidence packets unchanged. Do not tell either reviewer why V4.1 was written or which opaque IDs differed earlier.

Coordinator register per slot: reviewer ID; opaque session/account identifier; Phase1 packet hash and send time; Phase1 raw source/hash/lock time; Phase2 packet hash and release time; Phase2 raw source/hash/lock time; no cross-reviewer sharing attestation; any routing/session incident. Candidate-level `phase2_issue` never stores this run metadata. If either session lineage fails or any blocking content discrepancy remains, stop and seek Owner disposition; do not accept the Canary or release Human A/B. Remaining D1 40 groups, formal split and Detector training remain prohibited.
