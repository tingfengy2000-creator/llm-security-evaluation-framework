# S6.1-P1 Pilot2 Closure and Pilot3 Signal Feasibility

## Scope and authority

- Date: `2026-08-31`; machine: `LOCAL / CONTROL_PLANE`; no 5090 contact.
- Owner authority: `PODR-069 / PODR-070 / OR-031 / OR-032`.
- The owner confirmed five field corrections across four candidates. They are stored as a separate owner-correction record; the
  completed workbook, its SHA256 and original cells remain unchanged.
- Prohibited scope remains Dataset formal freeze, 240-group Pilot, formal detector training, 5090, Formal Experiment and Paper
  Result.

## Owner correction and Ground Truth

- Preserved workbook SHA256:
  `cf47a6c3ffada717a2a0dee2b67d6b92ebfb6236d599fb8a4daf2957e292dcb1`.
- Completion: issue rows `84/84`; candidate rows `26/26`; residual PENDING `0`.
- Corrected consistency: residual owner inconsistency `0`; remaining schema-logic conflict `0`.
- `PILOT2_GROUND_TRUTH_CANDIDATE_V1`: `36` deterministic records; source-chain and independence-group coverage `12/12`.
- Human-validated roles: `CLEAN_CURRENT=1`, `POISON_VALIDATED=12`, `HARD_NEGATIVE_VALIDATED=23`, excluded/insufficient `0`.
- Across the 84 issue rows, executable owner resolutions select A's complete issue value `17` times, B's `53` times and a
  third/composite value `14` times; none are unresolved. These counts describe resolution provenance, not agreement improvement.
- Original A/B agreement remains exactly `47` disagreements and `37` schema-logic conflicts. Owner resolution does not alter or
  improve the pre-adjudication agreement statistic.
- Historical self-containment limitations are recorded for six candidates without rewriting them. Semantic near-duplicate scan
  remains `NOT_IMPLEMENTED / FAIL_IF_REQUIRED`: it does not block this feasibility closure, but blocks formal Dataset freeze.

## Pilot2 closure

`S6.1-P1-PILOT2 = HUMAN_ACCEPTED / ANNOTATION_PROTOCOL_AND_GROUND_TRUTH_FEASIBILITY_ONLY / CLOSED`.

This establishes public versioned-Chinese-source, controlled-candidate, two-annotator Schema V2, owner-adjudication and Pilot-only
Ground-Truth construction feasibility. It does not establish a formal Benchmark, detector/intervention effectiveness,
generalization or SOTA.

Git-external evidence: `LLMGuard-Handoff/paper1_pilot2_closure_20260831`. The historical blocker files and original `5/5` index are
preserved; closure evidence uses the additive `closure_evidence_index.sha256`.

## Pilot3 local smoke

- Input: all `36` executable included Pilot2 candidates; `180` SignalRecord rows (`36 × 5 views`).
- Runtime: deterministic CPU-only rules; no large model, download, GPU or training.
- Label isolation: PASS. Signal extraction consumes candidate/reference/provenance/query text only; Ground Truth is joined after
  extraction solely for diagnostic aggregation.
- Semantic: available `36/36`; descriptive poison-vs-nonpoison AUROC `0.432`; weak and hard-negative-sensitive.
- Entity-Claim: available `36/36`; AUROC `0.396`; hard-negative false-positive behavior remains material.
- Provenance: available `1/36`, `NOT_APPLICABLE=35/36`; not useful in this candidate set without explicit authority claims.
- Temporal-Version: available `36/36`; AUROC `0.465`; current year-overlap probe does not separate roles.
- Retrieval-Behavior: available `36/36`; only an engineering query-overlap diagnostic, not a formal retrieval benchmark.
- Threshold-based diagnostic events: `FALSE_POSITIVE_ON_HARD_NEGATIVE=46` signal-view events, including Semantic `23`,
  Entity-Claim `15` and Temporal-Version `8`; `FAIL_TO_DETECT_POISON=17`, including Entity-Claim `8` and Temporal-Version `9`.

`S6.1-P1-PILOT3 = ENGINEERING_AND_SIGNAL_FEASIBILITY_ESTABLISHED / PILOT_DIAGNOSTIC_ONLY`.

This status means the five-view contract, availability semantics, deterministic loader and grouped diagnostics run. It explicitly
does not mean `DETECTOR_EFFECTIVENESS_ESTABLISHED`.

Git-external evidence: `LLMGuard-Handoff/paper1_pilot3_signal_feasibility_20260831`, `7` files total with evidence index `6/6`.

## Research recommendation and stop gate

Recommendation: `FIRST_REPAIR_SIGNAL_METHOD_AND_CLASS_BALANCE / THEN_OWNER_DECIDE_SMALL_DETECTOR_PROTOTYPE / DO_NOT_ENTER_240_GROUP_YET`.
The immediate research value is in implementing structured predecessor/successor/effective-date reasoning, richer authority/source
family evidence, a semantic near-duplicate scanner and a less collapsed Clean control set. Temporal-Version remains a promising
Paper 1 hypothesis, but this smoke does not support calling it an established innovation. Stop here pending the owner's next route
decision.
