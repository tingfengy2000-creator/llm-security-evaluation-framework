# D1 remaining90 Phase1 — Owner sending checklist V2

`R4-codex` remains the fixed reviewer code; the reviewer actually runs in **Doubao**. This V2 checklist supersedes the V1 checklist for distribution. Send exactly three files to each reviewer, individually, not an entire folder.

## R3-gpt — fresh independent GPT conversation

1. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining90_megawave_20260927\phase1_release_v1\reviewer_release\PAPER1_FORMAL_D1_REMAINING90_R3_GPT_PHASE1_PACKAGE_V1.json`
2. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining90_megawave_20260927\phase1_release_v1\reviewer_release\PAPER1_FORMAL_D1_REMAINING90_PHASE1_IMPORT_SCHEMA_V1.json`
3. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining90_megawave_20260927\phase1_release_v1\reviewer_release\PAPER1_FORMAL_D1_REMAINING90_R3_GPT_PHASE1_PROMPT_V1.md`

## R4-codex code / Doubao platform — fresh independent Doubao conversation

1. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining90_megawave_20260927\phase1_release_v2_r4_provider_correction\reviewer_release\PAPER1_FORMAL_D1_REMAINING90_R4_CODEX_PHASE1_PACKAGE_V1.json`
2. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining90_megawave_20260927\phase1_release_v2_r4_provider_correction\reviewer_release\PAPER1_FORMAL_D1_REMAINING90_PHASE1_IMPORT_SCHEMA_V1.json`
3. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining90_megawave_20260927\phase1_release_v2_r4_provider_correction\reviewer_release\PAPER1_FORMAL_D1_REMAINING90_R4_CODEX_PHASE1_PROMPT_V2.md`

The R4 package and schema above are **byte-for-byte copies** of V1. Only the R4 prompt and distribution route are corrected. **Never send `PAPER1_FORMAL_D1_REMAINING90_R4_CODEX_PHASE1_PROMPT_V1.md`.** Do not send earlier Canary/HKP1 answers or the other reviewer's files. Neither conversation may inherit project instructions, prior chats, knowledge, repository content, Owner construction files, mappings, labels, Expected/GT, Evidence/Phase2, or web-search results. Owner should attest what each received and the isolation conditions; without independent platform logs, record `OWNER_ATTESTED`, not machine verification.

Each reviewer returns one original strict UTF-8 90-row JSON file in its own package order and in the exact filename stated in its prompt. Owner forwards the **original file**, without pasting/reconstructing/re-saving. Keep each reviewer's isolated conversation for its Phase2 only after the Phase1 lock and release gate pass. If 90-row transport fails, retain the incident and request the approved 60+30 fallback; never silently split 30+30+30. Phase2, Human A/B, GT, formal split and training are withheld. Status: `STOP_EXTERNAL_REVIEW_REQUIRED`.
