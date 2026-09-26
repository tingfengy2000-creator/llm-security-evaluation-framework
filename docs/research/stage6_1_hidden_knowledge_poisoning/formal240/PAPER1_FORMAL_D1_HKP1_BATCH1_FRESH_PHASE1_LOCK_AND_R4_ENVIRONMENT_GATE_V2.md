# D1 HKP1 Batch-1 fresh Phase1 lock and R4 execution-environment gate

Date: 2026-09-26. This is an additive second run; the first R3/R4 raw returns and R3's self-reported session-routing incident remain immutable [history](PAPER1_FORMAL_D1_HKP1_BATCH1_PHASE1_RAW_LOCK_AND_ROUTING_BLOCKER_V1.md). The V4 Candidate, packet, import schema and both prompts are unchanged.

## Fresh raw cohort

The Owner supplied new-session R3 and R4 files. The originals were copied byte-for-byte into read-only `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining40_hkp1_batch1_20260926\phase1_raw_lock_fresh_r3r4_run02_20260926`:

| Reviewer | Bytes | SHA256 | Mechanical QA |
| --- | ---: | --- | --- |
| R3-gpt | 6,353 | `3488273ffa7bb8a4b0d563933b878f1dced406e1577b0f8f350d52d7f3597ef5` | 30/30 PASS |
| R4-codex | 7,907 | `52930e9ff2e59d42565a51feda744ab92c50da6ab5e7ab0f83e9485f67c675dd` | 30/30 PASS |

Both decode as strict UTF-8 JSON and pass exactly 30 objects, 30 unique/nonblank IDs, exact V4 packet ID set/order, seven exact keys, legal enums and string notes. Source-copy SHA/byte parity and read-only status pass. Five categorical fields agree 30/30. Three `issue_note` pairs differ in wording but each pair describes the same candidate-visible internal contradiction; no literal-note equality was imposed. [Machine validation](PAPER1_FORMAL_D1_HKP1_BATCH1_FRESH_PHASE1_VALIDATION_V2.json). No hidden C/P/H, HKP/S, Expected/GT, Owner mapping or Phase2 Evidence was used in this Phase1 QA.

The Owner attested both new conversations saw only the matching V4 Phase1 package/schema/prompt and did not see old answers, incidents, Owner/constructor material, mapping/labels, Phase2, the other answer, repository/handoff material, web or another AI. This is `OWNER_ATTESTED_NOT_MACHINE_VERIFIED`, not a platform access log. The Owner then clarified R4 ran in a **new Codex Project**, not a `projectless` empty-directory task. A new Project may be isolated in practice, but it is not the literal frozen R4 execution condition in `PODR-111`. The present return is structurally valid and useful for diagnostic QA; it cannot silently satisfy the primary double-blind gate.

## Decision-ready escalation

1. **Issue ID:** `D1-HKP1-BATCH1-R4-PROJECTLESS-DEVIATION-01`.
2. **Issue name:** fresh R4-codex run used a new Codex Project instead of the frozen projectless/empty-directory execution mode.
3. **Discovery stage/task:** Formal240 D1 remaining40 / HKP1 Batch-1, fresh Phase1 Run02 lock.
4. **Facts:** `OBSERVED_FACT`: both new JSON files are immutable and mechanically valid, with five fields 30/30 equal; Owner directly says R4 used a new Project. A read-only `-Force -Recurse` inspection of the Owner-specified Project directory found only the 7,907-byte R4 return JSON (matching SHA above), no hidden files and no `.git`. `SOURCE_DERIVED_FACT`: `PODR-111` requires projectless isolated Codex R4, while the current Batch-1 V4 prompt requires fresh independence and no repository/hidden-context access. `INFERENCE`: this presently empty Project directory is a plausible bounded equivalent, but is not literally projectless. `UNKNOWN`: platform-level Project history/inherited settings cannot be machine-verified from the directory; there is no independent session run log.
5. **Affected constraints:** reviewer identity/isolation, exact execution contract, Phase1-before-Phase2 gate, no hidden label/context exposure and append-only provenance.
6. **Why now:** Phase2 release would treat a nonliteral execution mode as accepted precedent; this must be resolved before evidence-bearing review continues.
7. **Downstream risks:** unrecognized Project context could bias annotation and undermine independence/reproducibility; premature Phase2 and batch acceptance could propagate into Human A/B or paper claims. No current evidence shows actual hidden-label exposure; the bounded cost is a possible 30-row R4 rerun.
8. **Options:** A — R4 reruns the unchanged V4 Phase1 in a new projectless empty-directory task; advantage: exact frozen compliance; disadvantage/cost: one 30-row review; risk: new discrepancies may require ordinary triage; later-stage/paper impact: clean provenance; reversible: yes, both old raws remain. B — Owner explicitly accepts this one new Project as a bounded equivalent after verifying it had no inherited files/instructions/memory and no repo/handoff access; advantage: preserves current 30/30 result; disadvantage/cost: an explicit documented exception and extra governance check; risk: human attestation is not machine proof; later-stage/paper impact: exception must remain visible; reversible: prospective work can return to projectless, but historical context cannot be independently proven.
9. **LOCAL recommendation before decision:** A for exact protocol compliance. Do not relabel a new Codex Project as projectless. B required a direct Owner exception decision and could not be inferred from the existing content-isolation attestation.
10. **Rationale/confidence:** high confidence in mechanical 30/30 checks and the runtime-mode mismatch; no claim of actual answer contamination. The data-quality check isolates a process-integrity defect from candidate-level content.
11. **Owner decision:** Owner explicitly approved B **only for this D1 HKP1 Batch-1 R4 Run02**, after the directory check, accepting that platform-level inheritance remains Owner-attested rather than machine-proven. This is not a general amendment of `PODR-111`; future R4 batch runs remain projectless. The decision authorizes the current pair's Phase1 gate and Phase2 release after package QA.
12. **After decision:** allowed: treat the two locked Run02 returns as the primary Phase1 pair, prepare/release frozen Phase2 only to the same respective isolated conversations, then await raw Phase2 returns. Prohibited: alter Candidate/Evidence/answers, accept Batch-1 or start HKP2/Human A/B/GT/split/training before Phase2 and remaining hard gates pass.

Current gate: `PHASE1_PRIMARY_PAIR_PASS_WITH_BOUNDED_R4_EXCEPTION / PHASE2_RELEASE_AUTHORIZED=TRUE / BATCH1_NOT_ACCEPTED / HKP2_NOT_STARTED`. `PHASE2_RELEASE_AUTHORIZED` does not assert that a new Phase2 packet has yet been built or distributed.
