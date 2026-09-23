# D1 Canary R3/R4 Phase1 raw lock and targeted naturalness repair V1

Task: `P1-FORMAL240-D1-CANARY-R3R4-PHASE1-LOCK-AND-TARGETED-NATURALNESS-REPAIR-01`

Status: `R3_GPT_PHASE1_LOCKED / R4_CODEX_PHASE1_LOCKED / PHASE1_STRUCTURED_AGREEMENT_COMPLETE / TARGETED_NATURALNESS_REPAIR_PREPARED / WAITING_FOR_R3_R4_TARGETED_REVIEW / PHASE2_NOT_YET_RELEASED`
Owner decision: `PODR-112 / OR-068`; execution log: `REL-2026-0077`.

## Source, lock and reviewer provenance

Owner corrected the earlier pasted-answer mix-up: no `R3-gpt PREMATURE_PHASE2`, `SEQUENCE_INVALID` or reviewer incident occurred. No such R3 artifact had been created, so none was added or deleted. The historical R1/R2 process record concerns a different reviewer pair and remains intact.

Owner explicitly assigned **attachment 1** (`004edc62-10bd-4441-b8b7-10de349d80cb`) to `R4-codex` and **attachment 2** (`9fb344d2-ab2b-42db-b38e-fd64464b087a`) to `R3-gpt`, reversing the order in the task name. The original JSON bytes were copied, not parsed and reserialized, into the new Git-external directory `E:\LLMGuard-Handoff\paper1_formal240_d1_canary_r3r4_phase1_raw_lock_20260923`. Copy/source SHA parity passed:

| Reviewer | Immutable raw filename | Bytes | SHA256 | Copy time UTC |
| --- | --- | ---: | --- | --- |
| R3-gpt | `PAPER1_FORMAL_D1_CANARY_R3_GPT_PHASE1_RAW_V1.json` | 5,661 | `323584b020cad90e382c9d7b202e20acd5ecbe2acabb0111180d6d059b44f36d` | 2026-09-23T14:59:54.7223481Z |
| R4-codex | `PAPER1_FORMAL_D1_CANARY_R4_CODEX_PHASE1_RAW_V1.json` | 6,451 | `afb0af1b61e927af61c76620f0a2ef76443c2123c07704dd7a56144a08f60e74` | 2026-09-23T14:59:54.6872067Z |

Owner subsequently confirmed both were fresh independent Phase1 sessions, R4-codex was a new projectless task in an empty directory, each received only the Phase1 V2 packet/schema and matching prompt, and neither accessed the repository, prior reviews, Owner packet, labels/mapping, Phase2 or outside search. Owner explicitly authorized `OWNER_ATTESTED` as the evidence level. The two immutable `*_REVIEW_RUN_ATTESTATION_V1.json` records preserve this declaration; **no session URL or machine access log was supplied, and no technical isolation proof is claimed**. Their administrative lineage tokens explicitly say `NO_EXTERNAL_ID`. Attestation SHA256: R3 `4a7ebbf741f76c2cdae58635ba654b6c6ce29e4ab794038cc73edb2ca5d06ae1`; R4 `6cbb9dbea9cad96537b5498259b77cf8ba816cfeea4421e5d9124c7ce9f45bfa`.

## Blind-only QA result

Against frozen Phase1 V2 packet and import schema V2, each raw return has exactly 24 records, 24 unique IDs, exact ID order and seven exact keys, valid enum values, and string notes. Five categorical fields each agree `24/24`; all-five-field exact agreement is `24/24`, with no disagreement IDs. Raw `issue_note` wording was not normalized or required to match byte-for-byte. The independent read-only raw comparison was completed before consulting private construction roles; the machine-readable agreement result is in the private lock directory.

Both returns independently mark `local_internal_conflict=YES` for `D1BR-0A533F363A06` and `D1BR-F3FA4889DA53`. Both mark `text_naturalness=MINOR_ISSUE` only for `D1BR-F3FA4889DA53` and `D1BR-008E1E01060C`; each note attributes the minor phrasing defect to “第四条下”. This is construction QA, not Ground Truth or a model benchmark.

## Bounded V3 preparation

Frozen Candidate V2 remains byte-identical: SHA256 `bd5085e4ba25c54731b9d5201ab7c48d2689060fea48436c9c972a19d1524176`. Exactly two Candidate V3 texts replace only `《职工带薪年休假条例》第四条下，` with `根据《职工带薪年休假条例》第四条，`; the other 22 candidate records are unchanged. New opaque IDs are private-mapped `D1BR-F3FA4889DA53 -> D1BR-C9E69F1920D5` and `D1BR-008E1E01060C -> D1BR-5654C8EF39A1`. The exact inverse single-span transformation verifies that all other factual text, numbers, dates, conditions and authority/version wording are unchanged. The first revised text still literally says the same person both enjoys and does not enjoy annual leave. Candidate roles, group slots and frozen Evidence doc IDs are equal V2/V3. Phase2 V4 copies every Evidence object unchanged; its 22 other row objects are equal V3. These are mechanical/lineage checks, not a substitute for the targeted external rereview.

Private outputs and hashes are indexed in `PAPER1_FORMAL_D1_CANARY_R3_R4_PHASE1_REPAIR_SHA_MANIFEST_V1.json` (SHA256 `9f2482c7e5a4c4df99102d166baf4f7ae9db8d0bfc11e895be234f34988ae8fb`). Candidate V3 SHA256 is `6210a6de8f519fb4a58334ff531954b67e774375d021d099dea050f8fe47032e`; two-row targeted Phase1 package SHA256 is `d898e41a6a1a9ff7807a3b987fe5c05a5b666caa6d22c00d9440ee2f609bc48d`; **prebuilt withheld** Phase2 V4 SHA256 is `2daf08286581cb8d28e70ab95ea844e5cdf41e2a6916980bf41b0a90a548ac38`.

The coordinator must send **only the two-row targeted Phase1 package plus the same Phase1 field/schema guidance**, separately to the original R3-gpt and R4-codex sessions. Do not send the private mapping, V3 construction file, Owner record, agreement, prior reviewer raw, or Phase2 V4. Each reviewer must return the two revised IDs. Only after both targeted returns are separately locked and pass `NATURAL / PASS / NO / NO`, with the contradiction still `YES` for `D1BR-C9E69F1920D5` and `NO` for `D1BR-5654C8EF39A1`, may the Owner/next task accept V3 and authorize release of the hash-locked Phase2 V4. Current release flag remains `FALSE`. No Human A/B, remaining D1 40 groups, split, training, formal result or Canary Owner acceptance is implied.

## Forward and paper risk review

The material risk is answer leakage or confusing a changed candidate with its previously reviewed identity. New opaque IDs, private mapping, two-row rereview, and Phase2 withholding address that risk without changing the accepted schema or Evidence. Owner-only run attestation is explicitly weaker than system audit; no independent-access claim beyond Owner confirmation is made. The original 24-row returns and V2 remain immutable, and targeted review will be an overlay rather than a rewrite. This Canary QA agreement does **not** establish annotator agreement, candidate factual validity, detector performance or a publishable result. No result-based candidate selection, Formal240 split, training, or scale expansion occurred.
