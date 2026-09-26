# Formal240 D1 Canary Phase1 final primary closeout

Task: `P1-FORMAL240-D1-CANARY-PHASE1-FINAL-CLOSEOUT-AND-PHASE2-RELEASE-PREP-01`. Owner decision `PODR-113 / OR-069`. Status: `D1_CANARY_PHASE1_PRIMARY_QA_ACCEPTED / TARGETED_NATURALNESS_REPAIR_ACCEPTED / CANDIDATE_V3_FROZEN / PHASE2_V4_READY / PHASE2_RELEASE_AUTHORIZED / R5_AUXILIARY_QA_RECORDED / NO_HUMAN_AB`.

## Primary raw and result

The new private namespace is `E:\LLMGuard-Handoff\paper1_formal240_d1_canary_phase1_final_closeout_20260926`. The Owner instruction attachment (SHA256 `6bcb66c2ab59cd7ab7632b425045a0e529d2eac20b467af71eb934e84d51f51b`) physically contains the two targeted JSON arrays. Exact UTF-8 byte slices, not reserialized JSON, are read-only locked with source byte offsets in `PAPER1_FORMAL_D1_CANARY_TARGETED_PHASE1_RAW_LOCK_MANIFEST_V1.json`:

| Reviewer | Role | Bytes | SHA256 | Source byte range |
| --- | --- | ---: | --- | --- |
| R3-gpt | primary gating 1 | 622 | `15a4ac45d6e42f36d36e77fffb430a26963ed531922291c404bb5c80b63f80f9` | `[1875,2497)` |
| R4-codex | primary gating 2 | 622 | `8197616e4cc8a9dbb7007011d246a577463f6634133fb6fda2c1a4e1a981eedd` | `[3659,4281)` |

Each has exact 2/2 IDs, order, seven fields and legal enums. Independently recomputed five-field exact agreement is 2/2 and each field agrees 2/2, no disagreement ID. Both mark `D1BR-C9E69F1920D5` `NATURAL/YES/PASS/NO/NO` and `D1BR-5654C8EF39A1` `NATURAL/NO/PASS/NO/NO`. R3's first raw `issue_note` contains a trailing file-name fragment. It is retained verbatim as `NON_BLOCKING_REVIEWER_NOTE_ARTIFACT_REFERENCE`; only its valid visible-text meaning is used in narrative, not as a cleaned replacement raw.

The two full 24-row R3/R4 raw files remain untouched at their earlier SHA identities. The new `PAPER1_FORMAL_D1_CANARY_PHASE1_FINAL_OVERLAY_V1.json` takes 22 unchanged rows from each reviewer's locked full Phase1 and replaces only the two old IDs with that reviewer's targeted raw values. No reviewer raw answer is overwritten; isolation remains `OWNER_ATTESTED_NOT_MACHINE_VERIFIED`, not a machine-proved session audit.

## Candidate and Phase2 gate

Candidate V2 remains SHA256 `bd5085e4ba25c54731b9d5201ab7c48d2689060fea48436c9c972a19d1524176`. Candidate V3 is frozen at 24 records, SHA256 `6210a6de8f519fb4a58334ff531954b67e774375d021d099dea050f8fe47032e`. Exactly two texts changed by the already recorded one-span phrase repair and got new opaque IDs; other 22 records are byte-identical. The designed internal contradiction remains, and extracted law titles, numbers and institutional mentions are unchanged in the repaired pair. The prior repair ledger is retained; the final overlay and this record are additive acceptance lineage.

The existing, previously withheld Phase2 V4 package is now accepted for release **without regeneration or overwrite**: 24/24 IDs and candidate text match V3; every E1/E2 evidence object, official URL, excerpt and snapshot SHA matches the pre-repair Phase2 package exactly. Its SHA256 remains `2daf08286581cb8d28e70ab95ea844e5cdf41e2a6916980bf41b0a90a548ac38`. A fresh bounded mechanical re-QA checked the 8 frozen matrix slots/24 triplets, 14/14 official snapshot raw/text hashes, metadata/fact-path/query source identities, title and obvious bare-reference checks, triplet length spread, the original S/E/P/T/R input preflight, and blind-package forbidden-field scan. A supplemental V2/V3 punctuation/template check found 24/24 exact punctuation-count parity, zero semicolon rows and zero template markers. It does **not** prove complete factual validity, Phase2 evidence sufficiency, all signal computation, or Canary acceptance. See the private `PAPER1_FORMAL_D1_CANARY_V3_MECHANICAL_REQA_V1.json`.

The [R3 prompt](PAPER1_FORMAL_D1_R3_GPT_PHASE2_PROMPT_V4_1.md) and [R4 prompt](PAPER1_FORMAL_D1_R4_CODEX_PHASE2_PROMPT_V4_1.md) are equivalent apart from reviewer identity and Codex-specific isolation instructions. Owner should separately send each same original session: Phase2 V4 packet, import schema V2, accepted Formal Guide V4, additive V4.1 clarification, and its own prompt. The [R5 auxiliary prompt](PAPER1_FORMAL_D1_R5_CLAUDE_PHASE2_AUX_PROMPT_V4_1.md) is optional/non-gating.

## R5 evidence boundary

Owner designated `R5-claude` auxiliary only and corrected the phrase “R5 second-stage” to **targeted Phase1**, not Evidence Phase2. After the initial primary lock, Owner supplied two actual source files in `E:\LLMGuard-Handoff`: `R5-claude24条.txt` (5,075 bytes, SHA256 `68e3d3cfa782d8b42b382a61c9d5a70e67fb9f1c46796dbf69b051dfd8d897ff`) and `R5-claude2条.txt` (520 bytes, SHA256 `0b9738c293d6873ee10cee7b12c0aadfa85a7c4a1d7b69183c08b71f2f53ad9b`). Exact byte copies are read-only locked in the new private namespace; their original formatting was **not** rewritten. Independent checks confirm 24/24 and 2/2 exact ID/order/keys/enums. Compared with each primary full return, R5 agrees on naturalness 21/24 and every other categorical field 24/24; the three naturalness disagreement IDs are `D1BR-0A533F363A06`, `D1BR-F3FA4889DA53`, `D1BR-008E1E01060C`. In the two-row repaired review, only `D1BR-C9E69F1920D5` naturalness differs (`UNNATURAL` vs primary `NATURAL`); all other fields agree 2/2. Its reason cites the designed contradiction itself. This is recorded as `AUXILIARY_NATURALNESS_CONFLICT_COUPLING`, not a new proven Candidate defect or a reason to weaken S1. The additive `PAPER1_FORMAL_D1_CANARY_R5_AUX_RAW_LOCK_MANIFEST_V1.json` and `PAPER1_FORMAL_D1_CANARY_R5_AUXILIARY_COMPARISON_V1.json` supersede the earlier primary-only manifest's `R5_AUXILIARY_RAW_PENDING` observation without rewriting it.

## Boundaries and next action

`PHASE2_RELEASE_AUTHORIZED=TRUE` means **permission to distribute**, not that this control-plane task has sent, performed, received or analyzed Phase2. The Owner/coordinator must send Phase2 materials separately to the original isolated R3-gpt and R4-codex sessions, then submit both Phase2 raw returns for exact-byte locks, schema/ID/enum validation, discrepancy analysis and an independent Owner Canary acceptance decision. R5 absence does not block that gate. No Human A/B package, remaining 40 D1 groups, split, detector training, Ground Truth or formal result is authorized here.

Forward/paper risk review: non-machine-verifiable R3/R4 session isolation, heuristic-only construction QA, R5's auxiliary rubric drift, and future Phase2 evidence sufficiency remain explicit limitations. V3 selection did not consult formal labels or detector performance; the repair preserves history and is not reviewer-unanimity optimization.
