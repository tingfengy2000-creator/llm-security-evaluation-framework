# Formal240 D1 remaining40 / HKP1 Batch-1 preblind status

Task: `P1-FORMAL240-D1-REMAINING40-CONSTRUCTION-01`
Date: 2026-09-26
Authority: Owner direct approval, `PODR-116`
Status: `STOP_EXTERNAL_REVIEW_REQUIRED`; **Batch-1 is not accepted**.

## Scope and lineage

The ten frozen D1/HKP1 slots are `F240-D1-HKP1-S1-C2/C3/C4`, `S2-C2/C3/C4`, and `S3-C1/C2/C3/C4`: 3/3/4 target-S allocation, 30 C/P/H candidates, ten distinct within-batch factual/evidence family clusters. This is exactly the remaining HKP1 allocation after the accepted eight-group Canary. The full D1 target remains 48 groups/144 candidates; only 8 Canary groups are accepted. These ten Batch-1 groups are **constructed but not externally reviewed or accepted**. HKP2–4 have not started.

Private immutable/additive evidence namespace: `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining40_hkp1_batch1_20260926`. The authoritative preblind cohort is `construction_v4` + `preblind_v4`, indexed by `closeout_v4/PAPER1_FORMAL_D1_HKP1_BATCH1_PRIVATE_MANIFEST_V4.json` (SHA256 `ccd22fbdd0da52c2adca6f8615249fec725688cc6b3423e599ac918065a4ce00`). Candidate V4 JSONL SHA256 `9ae18121d78d491bd82f78c1971e9bfcd85679b1e3eecfe0123481d60ca69a00`; preblind gate SHA256 `00f2f3f20c024ba6cf801f1edf6970fc90743b9fb89fa397079d8d24427f2965`.

Evidence-first chronology is physical: 17 verified official raw snapshots (14 reviewer E1/E2 and three metadata-only) and canonical fact records were locked before candidate construction. Failed anti-bot/TLS/HTTP captures are retained but excluded from evidence. Host, page publisher and issuer are separated; unsupported metadata remains explicitly unobserved. V1 was preliminary before an amendment effective-date metadata repair. V2 (not distributed) exposed an S3 Hard Negative-only explicit-number surface pattern. V3 repaired four S3 HN texts but a later official-text audit found that one S1 HN broadened a narrow Article 13 exception into generic “professional personnel.” V4 repairs **only that HN** using the already-frozen Article 2 age boundary, assigns a new opaque ID to that changed row, keeps evidence/slots and the other 29 texts unchanged, and retains V1–V3 plus private before/after ledgers. V1–V3 were never distributed and are not authoritative.

## Bounded local QA

- Frozen matrix and Canary non-overlap: 10/10; 30 unique blind IDs; C/P/H 10/10/10; S1/S2/S3 3/3/4.
- Snapshot bytes/SHA: 17/17. Preliminary surface-anchored fact inventory: ten designed controlled atoms, zero *detected* accidental or ambiguous atoms. This construction-side check is **not** independent factual validation or Ground Truth.
- Four S3 evidence paths have two frozen official sources and version/temporal metadata; the other six paths have one. Target/derived-S checks are provisional until independent Phase2.
- Triplet maximum character-length ratio 1.151; S3 numeric-surface disparity at most one count after V3 repair. No Candidate-side authority assertion in this HKP1 batch, so P is legitimately N/A for all 30; T is applicable to the 12 S3 candidates. S/E candidate inputs and shared neutral R query inputs are present for all 30. These are observability checks, not signal-effectiveness claims.
- Role-wise input-missingness is symmetric. Ten fixed Chinese character-bigram BM25 neutral-query smoke traces execute against 17 sources and retain rank/score/source hashes; this is not retrieval recall or a formal result.
- Both Phase1 reviewer packages contain only opaque ID and Candidate text, have identical SHA256 `09dde30b0ce9aa029664107711ec32071cda8ed9363657c7c6d8251a8eef4772`, and expose no role, HKP, target/derived S, mapping, Expected or GT.

## External gate and exact next action

Owner sends **V4 only**, separately to the original independent primary reviewer identities. For R3-gpt: `preblind_v4/PAPER1_FORMAL_D1_HKP1_BATCH1_R3_GPT_PHASE1_PACKAGE_V4.json`, shared `preblind_v4/PAPER1_FORMAL_D1_HKP1_BATCH1_PHASE1_IMPORT_SCHEMA_V4.json`, and `preblind_v4/PAPER1_FORMAL_D1_HKP1_BATCH1_R3_GPT_PHASE1_PROMPT_V4.md`. For R4-codex: the corresponding `R4_CODEX` package and prompt, plus the same schema. The reviewer must not see the private Owner packet, evidence manifest, mapping, construction files, V1–V3 packets, other reviewer's answer or Phase2 material. Run isolation needs fresh Owner attestation; the package alone does not prove it.

Both 30-row raw returns must be delivered unchanged, byte-locked and validated for exact schema/ID/order/enums before any Phase2 release. R3/R4 Phase1 raw: **not received**. Phase2: **not released**. Batch acceptance matrix: `all_hard_gates_pass=false`, `next_batch_allowed=false`. The next task action is to ingest those two raw files, resolve blocking Phase1 defects additively if any, then consider Phase2 release. Do not start HKP2 or Human A/B, GT, formal split, detector training or paper-result claims.
