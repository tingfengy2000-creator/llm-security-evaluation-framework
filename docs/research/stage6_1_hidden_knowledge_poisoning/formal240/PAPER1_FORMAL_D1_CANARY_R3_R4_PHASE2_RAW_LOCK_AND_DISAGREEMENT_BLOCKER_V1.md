# Formal240 D1 Canary R3/R4 Phase2 raw lock and disagreement gate

Task: `P1-FORMAL240-D1-CANARY-R3R4-PHASE2-RAW-LOCK-AND-DISAGREEMENT-TRIAGE-01`. Date: 2026-09-26. Type: independent blind-review evidence intake and protocol QA, **not** Canary acceptance, formal human annotation, GT or model evaluation. Input research HEAD `4ab378ceafa877f079751ce6ab1c173795b0d472`; origin ahead/behind `0/0`. The unrelated pre-existing design-spec edit was not touched. Primary pair is `R3-gpt` and `R4-codex`; `R5-claude` remains optional, non-gating.

## Immutable inputs and transport lineage

Exact byte copies are in the Owner handoff drive under `paper1_formal240_d1_canary_phase2_r3r4_raw_lock_20260926`. Each copy was re-hashed against its Owner-supplied source; none of the original files or earlier Phase1/Evidence artifacts was modified.

| Role | Source | Bytes | SHA256 | Classification |
| --- | --- | ---: | --- | --- |
| R3 first transport | `R3-gpt.txt` | 17,199 | `121776bece1048be3a11c4569bfb4e0e0d48d7cbcfa422772e63a5affa0abeb5` | real reviewer response transport; invalid JSON because string/key quotes were stripped; preserved as historical process evidence, not a parseable analysis return |
| R3 valid re-export | `R3-gpt-phase2-valid.json` | 18,396 | `29392396f705345e6213e50d5f457cc5881316ead52d706fc8d51d52024fd4fd` | superseding structured transport for Phase2 comparison; not represented as byte-identical to the first transport |
| R4 original | `R4-codex.txt` | 17,607 | `a1f8f4a50739d230770f7bb56920ea367a9171f1e581283105f33c9bd37c379d` | parseable original Phase2 return |

R3 re-export vs first transport: an in-memory, read-only extraction of the malformed text yielded 24 IDs in the same order and **zero differences across ID plus eight categorical fields**. All 24 reason bodies compare exactly after removal of transport/UI citation markers; all 24 `reviewer_note` strings compare exactly. Citation marker bytes and JSON serialization changed, so this is a content-lineage check, **not** a raw-byte equivalence claim. Both source versions remain immutable. R3's re-export includes UI `filecite` markers; these are not substitute Evidence Pool documents or independent proof of access.

Owner subsequently confirmed in this task conversation that each Phase2 reply came from the same isolated session as its respective Phase1, that each reviewer used only the frozen Phase2 V4 E1/E2 evidence, and that neither accessed the repository, mapping, Expected/GT, another reviewer's answer or out-of-packet factual sources. Evidence class: `PHASE2_RUN_SCOPE=OWNER_ATTESTED_NOT_MACHINE_VERIFIED`; no platform session log or independent access audit was supplied. This attestation resolves the pending run-scope question, **not** the substantive field disagreements.

## Structural validation and observed agreement

Comparison used only the two returned Phase2 files, the frozen Phase2 V4 packet (SHA256 `2daf08286581cb8d28e70ab95ea844e5cdf41e2a6916980bf41b0a90a548ac38`), import schema V2 and locked Phase1 final overlay. No C/P/H, HKP, target S, Expected, GT, Owner mapping or construction role was loaded to evaluate reviewers.

Both R3 and R4: JSON parse PASS; 24/24 rows; 24 unique blind IDs; exact packet ID set and order; exact eleven keys; canonical enum validity; 24/24 nonblank `phase2_reason`; Formal V4 internal-conflict/ZERO external-evidence consistency PASS. R3 reports 14 `CURRENTLY_CONSISTENT`, 8 `FACTUAL_CONFLICT`, 2 `LEGITIMATE_VERSION_OR_HISTORY`; R4 reports 16, 8, 0 respectively. Both report `phase2_issue=NONE` on all 24 rows. These counts describe pre-annotation reviewer QA, not Ground Truth.

| Categorical field | Exact agreement |
| --- | ---: |
| `overall_fact_status` | 22/24 |
| `version_claim_status` | 11/24 |
| `authority_claim_status` | 24/24 |
| `minimum_external_evidence_needed` | 24/24 |
| `evidence_selection` | 24/24 |
| `phase2_issue` | 24/24 |
| `possible_accidental_secondary_error` | 24/24 |
| `evidence_sufficiency` | 24/24 |

There are **15 differing field decisions across 15 blind IDs**: two overall/history classifications and thirteen version-scope classifications. Twelve version differences are R3 `NOT_PRESENT` vs R4 `PRESENT_CORRECT` on bare article/substantive statements; one is R3 `PRESENT_CORRECT` vs R4 `NOT_PRESENT` for `D1BR-89AF72FC0DA1`, whose candidate names an amendment decision. The two overall differences are `D1BR-EB126783B95E` and `D1BR-F64D9CDAF252`, where R3 selected `LEGITIMATE_VERSION_OR_HISTORY` and R4 `CURRENTLY_CONSISTENT` for an explicit two-version comparison. All fifteen exact values appear in the accompanying comparison JSON. No raw reviewer answer was rewritten to resolve them.

## Decision-ready escalation — `D1-CANARY-PHASE2-VERSION-SCOPE-BLOCKER-01`

1. **Issue ID:** `D1-CANARY-PHASE2-VERSION-SCOPE-BLOCKER-01`.
2. **Issue name:** Systematic version-claim boundary disagreement plus two historical-overall disagreements in a pre-annotation Canary.
3. **Discovery:** This Phase2 R3/R4 raw-lock and comparison task, after both structured transports passed mechanical QA.
4. **Facts:** `OBSERVED_FACT`: 13/24 version and 2/24 overall field differences; the other six categorical fields have 24/24 agreement. `OWNER_ATTESTED_FACT`: Phase2 same-session and frozen-E1/E2-only scope, without machine verification. `SOURCE_DERIVED_FACT`: Formal V4/V4.1 separates document-version metadata from substantive content and uses a present-time substitution test for legitimate history. `INFERENCE`: reviewers likely applied the implicit-current/version-scope boundary differently; this is not proof that either reviewer is wrong. `UNKNOWN`: which interpretation Owner will freeze for future Formal240 human A/B.
5. **Affected constraints:** Formal V4/V4.1 scope, two-phase independent blind QA, zero human annotation rework goal, Owner-only Canary acceptance, immutable reviewer raw.
6. **Why now:** Expanding to remaining40 or distributing Human A/B before resolving a systematic field boundary risks repeated annotation disagreement and rework.
7. **Downstream risks:** Benchmark labels and derived stealth may diverge; version-aware method evaluation and paper claims become unstable. Engineering fix cost grows after full D1 construction. Reproducibility requires preserving both raw judgments and an explicit rule/decision lineage. No new privacy, license or external-service action is required to triage these supplied files.
8. **Options:** (A) Owner clarifies the two global boundaries and adjudicates the fifteen field decisions in an additive, Expected-blind overlay: low construction cost and reversible as an overlay, but requires careful case review and may reveal a need for targeted re-review. (B) After a prospective Guide clarification, commission fresh independent targeted blind review: higher time/coordination cost, cleaner replication evidence, and versioned rather than silent changes; no automatic value precedence. (C) Leave all fifteen unresolved and hold the Canary: minimal immediate cost, but no Full48/Human A/B progression. None of these makes the present raw returns disappear or creates formal GT.
9. **LOCAL recommendation:** Prefer A as a decision-preparation path; if Owner finds the boundary cannot be deterministically applied, use B. Keep C as the fail-closed state until a separate Owner decision. Do not choose R3 or R4 merely by majority or assumed expected labels.
10. **Rationale/confidence:** The numerical differences and packet text are directly observed; the *cause* is a plausible but not yet Owner-confirmed guide-application explanation. Confidence is high for counts, limited for interpretation. Formal V4/V4.1 has not been amended in this task.
11. **Owner questions:** Does a bare present-tense citation of a named law/article, without an explicit current-version assertion, count as `version_claim_status=PRESENT_CORRECT`? Does naming an amendment decision while stating its passage/publication assert a version event? For a supported comparison of two explicitly named historical editions, should `overall_fact_status` be `LEGITIMATE_VERSION_OR_HISTORY` or `CURRENTLY_CONSISTENT` under the present-time substitution test? Should these be resolved by Owner additive adjudication or targeted fresh blind re-review?
12. **Until decision:** Allowed: read-only evidence review, exact raw-hash recheck, comparison and governance preservation. Prohibited: silently editing reviewer values, loading construction labels/Expected as answer precedence, Canary acceptance, Human A/B package distribution, D1 remaining40, split, GT, training or formal-result claims. `HUMAN_DECISION_REQUIRED / Auto Continue=NO`.

## Forward and paper risk; next gate

The Phase1 isolation and Phase2 run-scope lineage remains `OWNER_ATTESTED_NOT_MACHINE_VERIFIED`. R5's new-session Phase2 text is auxiliary only, never a third primary vote. The systematic version boundary should be resolved **before** formal human distribution; treating raw agreement as Canary acceptance would be a paper/protocol risk. Next gate: Owner gives an explicit resolution path for the version-scope and historical-overall questions; only then can an additive adjudication or targeted prospective clarification be prepared. No Candidate V3, Evidence Pool, matrix, Formal Guide or historical raw was changed. Future reviewer prompts should request a named UTF-8 strict-JSON output file and exact schema/row/order self-check before transfer; this is a prospective transport practice, not a change to current raw.
