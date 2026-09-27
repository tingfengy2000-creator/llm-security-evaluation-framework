# D1 HKP4 remaining-batch internal gate (not external acceptance)

Status: `HKP4_INTERNAL_CONSTRUCTION_GATE_PASS / EXTERNAL_REVIEW_PENDING / MEGAWAVE_NOT_RELEASED`.

Ten frozen HKP4 slots (`S1/S2/S3 = 4/2/4`) contain 30 private construction draft records. No candidate is accepted as Formal Ground Truth or separately released to a reviewer under this record.

## Evidence-first authority path

The [preconstruction authority/evidence contract](PAPER1_FORMAL_D1_HKP4_EVIDENCE_PRECONTRACT_V1.json) was authored before candidate text. It specifies the original issuing or promulgating institution, the official host/display role, the primary mechanism, neutral group query and precommitted zero/one/two-source path for every frozen slot. The private `PAPER1_FORMAL_D1_HKP4_PRECONSTRUCTION_AUTHORITY_EVIDENCE_AUDIT_V1.json` passed all ten source-byte identity checks before draft creation. The ten-source set contains eight previously locked official snapshots and two new raw official artifacts: a State Administration for Market Regulation official repost of the Social Insurance Law and an original Human Resources and Social Security Ministry PDF of the Work Injury Identification Measures. New raw files retain their capture manifests and SHA256 values in the private handoff namespace.

The [source-role audit](PAPER1_FORMAL_D1_HKP4_AUTHORITY_METADATA_AUDIT_V1.json) separates host, page publisher, adoption authority and original promulgating institution. A law republished by a government site is **not** a law issued by that site. The Jilin official repost's page-publisher identity is not independently established in the frozen evidence and stays `NOT_OBSERVED_WITH_FROZEN_EVIDENCE`; original lawmaking authority is supported by the official legal-text header. The S3 pair claims compare two separately documented institutions, rather than assuming the authority of one document from the host of the other.

## Construction-side results and limitations

The private draft `PAPER1_FORMAL_D1_HKP4_CANDIDATE_DRAFT_V1_NOT_RELEASED.jsonl` in `paper1_formal240_d1_remaining90_hkp4_20260927` has SHA256 `90d1fadc7aa40dc65a6ad6e263caf3e7bafd1ff6fe38141eed4e6452adca6507`. Author-side atom audit records 37 supported and ten deliberately corrupted atoms, no *identified* accidental or ambiguous atom. This is not independent factual adjudication.

The private `PAPER1_FORMAL_D1_HKP4_INTERNAL_MECHANICAL_QA_V2.json`, SHA256 `67e4c44a98eb0884e538ad1800eafacbfa66da2056c1b1e227e37deb10ff87d5`, reports 10/10 group-neutral queries executed on ten hash-locked official documents using the fixed character-bigram BM25 smoke harness (`k1=1.2`, `b=0.75`). Its traces are engineering diagnostics, not retrieval-performance estimates or a candidate-selection signal. The V1 smoke is retained; V2 additively corrects its overly broad claim that all provenance metadata are present.

S/E and core issuing-authority inputs are observed for 30/30; R has neutral queries and corpus membership. T is legitimately not applicable where the candidate has no version assertion, even if the official evidence has a date or version header. One group (three candidates) has an unknown page-publisher field; it is explicitly missing for all three roles, so it is not a C/P/H missingness shortcut. No surface-attention or mechanical blocking flag remains. Reviewer naturalness, true fact validity, and authority-path judgment remain pending.

## Boundary and next gate

No R3/R4 package or raw return, Phase2 release, Human A/B package, Ground Truth, split, detector or model run was produced for HKP4. HKP2/HKP3/HKP4 now have internal mechanical passes; the next step is a cross-batch 90-record integrity and leakage audit, followed by a single shuffled Phase1 MegaWave if that combined gate passes. It must go to two fresh isolated R3/R4 sessions. External Phase2 remains withheld until two valid Phase1 raw returns are locked.
