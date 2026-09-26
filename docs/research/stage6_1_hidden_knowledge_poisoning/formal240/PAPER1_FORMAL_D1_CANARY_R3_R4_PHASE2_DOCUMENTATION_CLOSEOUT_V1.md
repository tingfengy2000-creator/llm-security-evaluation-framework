# D1 Canary R3/R4 Phase2 raw-lock documentation closeout

Task: `P1-FORMAL240-D1-CANARY-R3R4-PHASE2-RAW-LOCK-AND-DISAGREEMENT-TRIAGE-01`. This closes documentation for bounded raw intake, structural QA and disagreement escalation only. It does **not** accept the Canary, authorize Human A/B or settle reviewer values. Primary evidence and all fifteen value differences are indexed in the [raw-lock/blocker record](PAPER1_FORMAL_D1_CANARY_R3_R4_PHASE2_RAW_LOCK_AND_DISAGREEMENT_BLOCKER_V1.md) and [comparison JSON](PAPER1_FORMAL_D1_CANARY_R3_R4_PHASE2_COMPARISON_V1.json).

## Mandatory closeout matrix

| Document | Condition | Action |
| --- | --- | --- |
| Human Ledger | Mandatory | Updated: plain-language intake, disagreement and next Owner gate. |
| Agent Ledger | Mandatory | Updated: raw lineage, exact statuses, Owner-attested run scope and constraints. |
| Current Work State | Mandatory | Updated with newest Phase2 gate above historical Phase1 snapshots. |
| Research Execution Log | Mandatory | `REL-2026-0079` appended. |
| Experiment Master Record | Conditional; Evidence/annotation gate changed | Updated with current indexed gate. |
| Owner Decision Register | Conditional; no new adjudication/approval/freeze decision | Not changed: run-scope confirmation is Owner testimony, not acceptance or a method decision. |
| Stage Process | Conditional; Phase2 gate changed | Updated with additive stage snapshot. |
| Canonical Lessons | Conditional; no Owner-accepted reusable lesson | Not changed; future strict-JSON-file handoff is a prospective practice, not a promoted methodological lesson. |
| Research Plan Authority | Only if research contract changes | Not changed: V4/V4.1 and Formal240 matrix remain frozen. |
| Paper 1 and Formal240 README | Navigation changed | Both updated. |
| Project Master Context | Project-current gate changed | Updated with Phase2 status and Owner decision boundary. |

## DOCUMENTATION_CLOSEOUT_CHECKLIST

```text
human_ledger_checked=true
human_ledger_updated_if_required=true
agent_ledger_checked=true
agent_ledger_updated=true
current_work_state_updated=true
execution_log_appended=true
experiment_master_condition_evaluated=true
owner_decision_condition_evaluated=true
stage_process_condition_evaluated=true
lessons_condition_evaluated=true
research_authority_condition_evaluated=true
README_condition_evaluated=true
cross_document_current_task_consistent=true
cross_document_status_consistent=true
cross_document_next_action_consistent=true
cross_document_blocker_consistent=true
markdown_links_valid=true
```

`PAPER1_DOCUMENT_STALENESS_GATE=PASS`: new top/current sections supersede older Phase2-not-executed snapshots without rewriting their historical statements. Across the current human, agent, state, master, execution and process records, the next action is the same: Owner resolves version-scope and historical-overall interpretation; `HUMAN_DECISION_REQUIRED / Auto Continue=NO`. The Owner-confirmed run scope is `OWNER_ATTESTED_NOT_MACHINE_VERIFIED`, not a system audit. No reviewer raw, Candidate V3, Evidence Pool, Formal Guide, matrix, historical Stage1–5 or Final72 artifact was changed.

## Bounded QA and known repository debt

- Re-hash of all three new private raw copies matched the source values; R3 and R4 each had 24 rows, unique packet IDs, exact order and keys, and nonblank reasons. The independently recomputed fifteen field differences exactly match the JSON comparison. The first R3 transport remains invalid JSON and historical.
- Strict UTF-8 decoding and JSON parse pass for task files; `git diff --check` passes; no Stage1–5 file changed. No model, retriever, annotation, split, training or new formal result was run.
- Focused Formal240/context re-run after this file was added produced `31 passed / 2 baseline failures / 193 subtests passed`: the only failures are absolute drive paths in the earlier Phase1 final-closeout record and an older current-state entry. `git show HEAD` confirmed both path patterns already exist in the input commit; neither was introduced by this task. The task's own initially missing closeout link is now valid.
- Broad Ruff on `src tests` and broad MyPy on `src` still find pre-existing Stage5/style/type/dependency errors; no Python source or tests were edited in this task. They are not attributed to this Phase2 intake and do not justify changing frozen or unrelated code.

Documentation status for this bounded task: `PASS_WITH_REPOSITORY_BASELINE_TEST_DEBT`. Scientific/protocol status remains `D1-CANARY-PHASE2-VERSION-SCOPE-BLOCKER-01 / HUMAN_DECISION_REQUIRED`, independently of documentation closeout.
