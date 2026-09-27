# D1 remaining90 — R5-Claude targeted Phase1 raw lock and bounded triage

Date: 2026-09-27. Status: `R5_AUXILIARY_RAW_LOCKED / STRUCTURAL_QA_PASS / OWNER_ADJUDICATION_PENDING / PHASE2_WITHHELD`. This is pre-annotation Candidate-quality evidence, neither Ground Truth nor a majority-vote replacement for the R3/R4 originals.

## Provenance and immutable input

Owner supplied `C:\Users\Admin\Downloads\PAPER1_FORMAL_D1_REMAINING90_R5_CLAUDE_TARGETED_PHASE1_RAW_RETURN_V1.json`. The 3,563 original bytes were copied without parsing, reformatting or sorting to read-only `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining90_r5_claude_targeted_raw_lock_20260927\PAPER1_FORMAL_D1_REMAINING90_R5_CLAUDE_TARGETED_PHASE1_RAW_RETURN_V1.json` at `2026-09-27T06:35:18.7801030Z`. Source and locked copy both hash to SHA256 `788061588e4a42cbb80fda6aaf866944bc2cc027bbc589076f2313820ad463e3`. The previous R3/R4 raws, the withdrawn wrong-attachment incident and their QA remain unchanged.

Owner confirms the R5-Claude run was an independent blind session, given only the ten-row candidate-only Phase1 packet, schema and prompt; it did not see R3/R4 answers, hidden construction/Expected/GT, Phase2, repository or web. Provenance level: `OWNER_ATTESTED`, **not** platform-log verified. The R5 code is auxiliary only. R4-codex remains a stable code for the Doubao reviewer; the prior R4 self-attestation is not silently upgraded to Owner attestation here.

## Reproducible structural validation

`scripts/formal240_remaining90_r5_targeted_validate.py` checks the original packet and schema hashes, strict UTF-8 JSON (no BOM, duplicate keys or non-JSON numeric constants), exactly 10 objects, 10 unique IDs, exact packet ID set **and order**, exact seven keys in order, legal enums, string types and the flag-to-`issue_note` rule. It also checks the frozen R3 and R4 reference hashes before comparing candidate-only Phase1 values. The private read-only result is `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining90_r5_claude_targeted_raw_lock_20260927\qa\PAPER1_FORMAL_D1_REMAINING90_R5_CLAUDE_TARGETED_PHASE1_QA_V1.json`, 15,946 bytes, SHA256 `4baeff5127f29fa622258a90fd7e68379fd33956344830aa1d3aadc92fe0927c`. All listed mechanical checks pass.

R5 categorical profile: `text_naturalness=NATURAL` 10/10; `local_internal_conflict=YES` 5/10 and `NO` 5/10; `self_containment=PASS`, `ambiguous_referent=NO` and `meta_or_template_language=NO` each 10/10. Five YES rows have nonblank, candidate-visible notes; the five unflagged rows have blank notes. Notes are compared semantically, not required to match R3/R4 byte-for-byte.

## Ten-row comparison and interpretation

The ten rows are the union of six R3/R4 naturalness differences and four R3/R4 internal-conflict differences. R5 matches R4 on all ten `text_naturalness` values and all ten `local_internal_conflict` values. For the **six actual naturalness disagreements**, R5 sides with R4's `NATURAL` against R3's `MINOR_ISSUE`. For the **four actual internal-conflict disagreements**, R5 sides with R4's `YES` against R3's `NO`:

| Disagreement field | IDs | R3 | R4 | R5 | Bounded reading |
| --- | --- | --- | --- | --- | --- |
| `local_internal_conflict` | `D1BR-FB2590D87D27`, `D1BR-194520C78747`, `D1BR-566391C110ED`, `D1BR-67D572512767` | `NO` | `YES` | `YES` | In each Candidate, the same document's promulgating organ is asserted as two different institutions under the same scope. R5's notes independently cite this text-visible incompatibility. Strong evidence for a candidate-only `YES` interpretation, but Owner must adjudicate. |
| `text_naturalness` | `D1BR-7F2FFE8B0B69`, `D1BR-AFAC6C1524F3`, `D1BR-88F9543EBF7B`, `D1BR-9966C6FDD551`, `D1BR-156165CA568A`, `D1BR-9A33FC80EF11` | `MINOR_ISSUE` | `NATURAL` | `NATURAL` | R3's notes identify mild phrasing awkwardness while finding text understandable. The 2:1 split is a naturalness boundary preference, not proof that R3 is invalid or that Candidate repair is required. |

R5 also marks `D1BR-AFAC6C1524F3` as `local_internal_conflict=YES`, but R3 and R4 already agreed on YES there; it is **not** a fifth new disagreement. Its note correctly identifies the candidate's two incompatible effective dates. The other three categorical fields agree among R3/R4/R5 on all ten selected rows. No hidden C/P/H, HKP, target/derived S, mapping, Expected, Owner construction result or Phase2 Evidence was loaded for this triage.

The four promulgating-organ Candidates share a conspicuously repeated `既是…同时又是…` surface. This is a **potential** style/role shortcut requiring a separate sealed-construction triplet-parity check before pre-annotation acceptance. R5's `NATURAL`/`PASS` values do not certify whole-wave style parity, and we have not used labels here to establish a class correlation. This concern is not resolved by majority vote.

## Gate and exact Owner decision needed

Recommended bounded decision: Owner reviews the four quoted Candidate-only contradictions and either confirms `local_internal_conflict=YES` in an **additive adjudication overlay** (without rewriting R3's `NO`) or returns specified rows for repair/re-review. Owner may treat the six naturalness differences as nonblocking expression variance, or name a specific material readability defect requiring versioned repair. The repeated authority-contradiction wording should receive a separate construction-side shortcut audit before Phase2 release. This is a recommendation, **not** an Owner decision.

`PHASE2_RELEASE_AUTHORIZED=FALSE` pending that adjudication, any required Candidate repair and reviewer-session provenance closure. Do not send Phase2 to R3/R4 yet. No Human A/B, GT, split, detector training or formal result is authorized. R5 raw is auxiliary evidence only, and none of the three reviewer raw files is rewritten.
