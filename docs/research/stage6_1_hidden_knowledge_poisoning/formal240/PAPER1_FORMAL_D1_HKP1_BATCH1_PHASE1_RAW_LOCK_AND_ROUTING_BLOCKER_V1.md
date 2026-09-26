# D1 HKP1 Batch-1 Phase1 raw lock and R3 routing blocker

Date: 2026-09-26. Task: `P1-FORMAL240-D1-REMAINING40-CONSTRUCTION-01`. Owner-approved scope: first of four ordered batches, not Phase2 or HKP2 acceptance.

## Raw evidence and bounded validation

The three supplied source files were copied byte-for-byte into the new read-only Git-external `paper1_formal240_d1_remaining40_hkp1_batch1_20260926/phase1_raw_lock_20260926` directory. Source and copy bytes/SHA256 match; the original source files, V4 Candidate, package, schema and prior V1–V3 history were not changed.

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| R3-gpt Phase1 JSON | 7,920 | `01fb665eb225d225cd538b67d8579532d4559e028b044255212e3823240d4fe5` |
| R3-gpt session-routing incident | 1,621 | `d491428970067894ab65d226bd7335b96f68fba69796bc94691f965e0ccb10f7` |
| R4-codex Phase1 JSON | 7,970 | `5e654ecf157a47bfd6aabf53cea6a1df892b604f38d71d6b9bedac22cb4d5952` |

Strict UTF-8 decoding, JSON parse, 30/30 rows, 30 unique IDs, exact V4 packet ID set and order, seven exact keys, legal enums and string `issue_note` all pass for each JSON. There is no detected additional field. The two supplied answers show diagnostic-only agreement of 26/30 for `text_naturalness`, and 30/30 for each of `local_internal_conflict`, `self_containment`, `ambiguous_referent`, and `meta_or_template_language`. Naturalness differs at `D1BR-C7D610617A1C`, `D1BR-BF83B4122122`, `D1BR-33BD2836BA90`, `D1BR-5133E1A44A11`. Five notes differ literally; note identity was not a required agreement condition. [Machine validation](PAPER1_FORMAL_D1_HKP1_BATCH1_PHASE1_VALIDATION_V1.json) records all IDs and gates. No hidden role mapping, Expected, GT, Phase2 Evidence, HKP/S or construction labels were used to evaluate these returns.

## Decision-ready escalation

1. **Issue ID:** `D1-HKP1-BATCH1-R3-SESSION-ISOLATION-BLOCKER-01`.
2. **Issue name:** R3-gpt Phase1 structurally valid but not a fresh isolated blind-review run.
3. **Discovery stage/task:** Formal240 D1 remaining40, HKP1 Batch-1 Phase1 raw lock.
4. **Facts:** `OBSERVED_FACT`: R3's separate 1,621-byte incident states that the actual answering session already held Canary review history and Phase2 material; both raw JSONs pass mechanical checks. `SOURCE_DERIVED_FACT`: the V4 prompt requires a fresh independent session seeing only this batch's Phase1 materials. `INFERENCE`: previous context may bias R3's judgments, so the answer cannot count as a primary independent review even if the reviewer says it did not deliberately use that material. `UNKNOWN`: whether R4's new run was genuinely projectless/isolated; no current-batch Owner attestation or system session logs were supplied.
5. **Affected constraints:** R3/R4 independent primary gating pair, Phase1-before-Phase2 release, no hidden-label exposure, immutable raw and fail-closed batch progression.
6. **Why now:** releasing Phase2 on a merely parseable but non-isolated R3 return would contaminate the formal pre-annotation gate and invalidate later R3/R4 independence claims.
7. **Downstream risks:** reviewer-context shortcut and unrepeatable agreement; invalid Phase2 lineage, batch acceptance, Human A/B rework minimization and eventual Paper 1 evidence. No safety/licensing or model-training event occurred; time cost is a bounded 30-row rerun.
8. **Options:** A — rerun R3 in a truly fresh isolated session using unchanged V4 package/schema/prompt; advantage: preserves frozen Candidate and R4 work if independently attested; disadvantage/cost: one extra 30-row review; risk: new result may reveal substantive discrepancies; later-stage/paper impact: restores valid evidence if all gates pass; reversible: yes, all originals retained. B — repeat both R3 and R4 in two fresh isolated sessions; advantage: strongest symmetric provenance; disadvantage/cost: two reviews; risk: delay without a demonstrated R4 defect; later-stage/paper impact: maximal independence assurance; reversible: yes. Treating the current R3 return as valid primary review is **not** a compliant option without an explicit new Owner protocol decision and paper-risk review.
9. **LOCAL recommendation:** option A if Owner can attest R4's run-specific isolation; otherwise option B. Preserve current R3 only as `AUXILIARY_PROCESS_EVIDENCE`, never as a vote or tie-breaker.
10. **Rationale/confidence:** high confidence in the R3 isolation failure because the reviewer explicitly self-reported it; R4's process status is unknown, independent of its mechanical 30/30 pass. The four naturalness differences are only diagnostic, not valid pairwise agreement or automatic repair grounds.
11. **Owner questions:** confirm the R4-codex run's fresh projectless/empty-directory isolation and exact material/access boundary, either with run evidence or explicitly `OWNER_ATTESTED`; provide a new isolated R3-gpt 30-row raw return and run attestation, or direct a symmetric fresh-pair rerun. No new scientific approval is needed to *submit* a compliant replacement under the existing approved reviewer workflow; accepting a noncompliant run would require an explicit separate decision.
12. **Before decision:** allowed: raw preservation, byte/schema QA, run-risk analysis, documentation and Git governance. Prohibited: count this pair as valid independent agreement, change Candidate/Evidence/answers, release Phase2, accept Batch-1, start HKP2, Human A/B, GT, split, training or formal claims.

Final gate: `HUMAN_DECISION_REQUIRED / Auto Continue=NO / PHASE2_RELEASE_AUTHORIZED=FALSE / BATCH1_NOT_ACCEPTED / HKP2_NOT_STARTED`.
