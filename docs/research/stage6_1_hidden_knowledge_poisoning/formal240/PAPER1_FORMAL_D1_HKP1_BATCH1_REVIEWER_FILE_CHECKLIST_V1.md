# D1 HKP1 Batch-1 reviewer handoff checklist

This checklist is for the Owner/coordinator. The current Batch-1 Phase2 release is authorized by the locked Phase1 QA and Owner's one-run R4 exception, not by this checklist alone. V4 is the sole distribution-authoritative Batch-1 candidate cohort; do not send V1–V3, Owner private construction/evidence records, identity mappings, C/P/H/HKP/S roles, Expected/GT, old reviewer responses or routing incidents.

## Current action — send Batch-1 Phase2 to the SAME R3/R4 sessions

**Do not create a new Project, task or conversation for this Phase2.** Send each list only to the respective new-session reviewer who produced the 6,353-byte R3 or 7,907-byte R4 locked Run02 Phase1 file. If either original session is unavailable or has seen hidden material, stop and request a new run plan; do not silently continue in another chat. Phase2 has **not** yet been performed, and its two raw returns must come back separately.

Send to **R3-gpt original Batch-1 Run02 conversation** exactly these six files:

1. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining40_hkp1_batch1_20260926\phase2_release_run02_20260926\PAPER1_FORMAL_D1_HKP1_BATCH1_PHASE2_PACKAGE_V4.json`
2. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining40_hkp1_batch1_20260926\phase2_release_run02_20260926\PAPER1_FORMAL_D1_HKP1_BATCH1_PHASE2_IMPORT_SCHEMA_V4.json`
3. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining40_hkp1_batch1_20260926\phase2_release_run02_20260926\PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md`
4. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining40_hkp1_batch1_20260926\phase2_release_run02_20260926\PAPER1_FORMAL_ANNOTATION_GUIDE_V4_1_CLARIFICATION.md`
5. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining40_hkp1_batch1_20260926\phase2_release_run02_20260926\PAPER1_FORMAL_ANNOTATION_GUIDE_V4_2_VERSION_SCOPE_DECISION.md`
6. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining40_hkp1_batch1_20260926\phase2_release_run02_20260926\PAPER1_FORMAL_D1_HKP1_BATCH1_R3_GPT_PHASE2_PROMPT_V4.md`

Send to **R4-codex original Batch-1 Run02 Project/task** exactly the same first five files above, plus **its own** sixth file (never the R3 prompt):

6. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining40_hkp1_batch1_20260926\phase2_release_run02_20260926\PAPER1_FORMAL_D1_HKP1_BATCH1_R4_CODEX_PHASE2_PROMPT_V4.md`

The first five paths are byte-identical for both reviewers; each receives only their own prompt. Ask R3 to return `PAPER1_FORMAL_D1_HKP1_BATCH1_R3_GPT_PHASE2_RAW_RETURN_V4.json` and R4 to return `PAPER1_FORMAL_D1_HKP1_BATCH1_R4_CODEX_PHASE2_RAW_RETURN_V4.json`, each as an unmodified UTF-8 JSON file with 30 objects in packet order. Keep their session-isolation confirmations at run level, not inside candidate `reviewer_note`. Do not send the release manifest, this checklist, either Phase1 raw, the prior routing incident, or any private Owner/construction file.

## Phase1 — only if a fresh run is required

For **R3-gpt**, send exactly these three files to a **new independent GPT conversation** with no previous project/conversation memory or imported history:

1. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining40_hkp1_batch1_20260926\preblind_v4\PAPER1_FORMAL_D1_HKP1_BATCH1_R3_GPT_PHASE1_PACKAGE_V4.json`
2. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining40_hkp1_batch1_20260926\preblind_v4\PAPER1_FORMAL_D1_HKP1_BATCH1_PHASE1_IMPORT_SCHEMA_V4.json`
3. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining40_hkp1_batch1_20260926\preblind_v4\PAPER1_FORMAL_D1_HKP1_BATCH1_R3_GPT_PHASE1_PROMPT_V4.md`

For **R4-codex**, send exactly these three files to a **new projectless Codex task in an empty directory**, not a Codex Project, repository worktree, fork or continuation:

1. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining40_hkp1_batch1_20260926\preblind_v4\PAPER1_FORMAL_D1_HKP1_BATCH1_R4_CODEX_PHASE1_PACKAGE_V4.json`
2. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining40_hkp1_batch1_20260926\preblind_v4\PAPER1_FORMAL_D1_HKP1_BATCH1_PHASE1_IMPORT_SCHEMA_V4.json`
3. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining40_hkp1_batch1_20260926\preblind_v4\PAPER1_FORMAL_D1_HKP1_BATCH1_R4_CODEX_PHASE1_PROMPT_V4.md`

Each reviewer returns the raw UTF-8 JSON file named in their own prompt, 30 rows in packet order, without resaving or normalization. Keep a separate run-level statement of new-session identity, supplied-file scope and no outside access. Owner statements are recorded as `OWNER_ATTESTED`, not machine proof. Do not mix that statement into candidate `issue_note`.

## When to start new sessions

- **Each new HKP batch's Phase1:** yes, start a fresh isolated session for R3 and a fresh projectless empty-directory task for R4, unless Owner explicitly versions and approves a different execution contract beforehand. Do not reuse this Batch-1 session for HKP2.
- **Same batch's Phase2:** no new session/project. Only after both Phase1 raws are locked, schema/ID/order/enum and run isolation pass, use the **same accepted reviewer sessions** for the separately released Phase2 files. The Phase2 file paths will be supplied only when that gate opens; none is authorized now.
- **Targeted repair of the same batch:** normally return only revised opaque IDs to the same accepted sessions. If a session has seen hidden information or violated isolation, restart that review chain from a new Phase1 session instead; do not pretend a targeted answer restores blinding.

For the current Run02, both new raws are structurally valid and Owner-attested. R4's new-Project execution differs from the frozen projectless condition, but the Owner explicitly accepted it **only for this one Batch-1 run** after the bounded directory check. The exception neither rewrites `PODR-111` nor authorizes new-Project R4 runs in HKP2–4. [Decision and limits](PAPER1_FORMAL_D1_HKP1_BATCH1_FRESH_PHASE1_LOCK_AND_R4_ENVIRONMENT_GATE_V2.md).
