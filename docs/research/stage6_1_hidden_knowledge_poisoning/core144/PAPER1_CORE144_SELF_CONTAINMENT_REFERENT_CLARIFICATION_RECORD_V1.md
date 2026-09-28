# Core144 self-containment / referent clarification — audit and closeout V1

Task: `P1-CORE144-SELF-CONTAINMENT-REFERENT-CLARIFICATION-01`

Date: 2026-09-28

Authority: Owner's explicit current instruction; `PODR-127 / OR-082 / REL-2026-0096`

Scope: explanation-only additive clarification of the [Master Guide](PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_V1.md). No new schema, field, enum or accepted-protocol revision; no workbook authoring/export.

## 1. Identity and preservation

Unique branch-bound worktree: `research/stage6-1-hidden-poisoning`. Source HEAD: `4a838585b08308b8e70b172f9ccdaf2a1ed7dd2c`. Git is the final commit/sync authority; this source HEAD is not described as the post-task HEAD.

| Artifact | SHA256 | Treatment |
| --- | --- | --- |
| Master Guide before clarification | `89bf7e65dd2d600fb73f4e51419c59da688e1132ff89a3313812b6fdb71485cd` | Prior content recoverable at source HEAD |
| Master Guide after clarification | `8fa295899d5d64692350ee62e574802d2917bc6161ba24ff2a050bf1b0903478` | Owner-requested documentation update |
| [New read-only QA receipt](PAPER1_CORE144_SELF_CONTAINMENT_REFERENT_CLARIFICATION_QA_V1.json) | `83b5a73e09555b4f33845ffd129e80ba3dac4a146d0305adc433c3389c442020` | Additive namespace |
| [Historical QA V1](PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_QA_V1.json) | `594ee7a7d707ae95155c866a2b502ee3b57e3ab1bc19c0acd116b300674e9bd7` | Unchanged; its 30-case counts describe the earlier guide |
| [Historical QA record V1](PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_QA_RECORD_V1.md) | `f5a3202dd6780e2b0e0983ea3c140c7aadf0516c76d37f5bb120a37dd177dd8e` | Unchanged |

All original cases01–30 are compared verbatim against the source commit and preserved. No actual Candidate, opaque ID, row order, evidence snapshot, accepted V4–V4.3 file, Phase2 workbook, reviewer raw, Owner overlay or historical return is edited. Stage1–5 and Final72 assets are outside the task diff. Existing unrelated design edits and the pre-existing untracked Master Guide PDF are excluded and left unchanged; PDF content was not reviewed, regenerated or certified as matching the new Markdown. Owner should review the updated Markdown rather than assume PDF parity.

## 2. Exact clarification and coverage

`self_containment`: only the current Candidate must supply the key object/document/core proposition/necessary conditions sufficiently for independent understanding. `ambiguous_referent`: a referring expression already in the Candidate has two or more reasonable antecedents. Missing identity is not by itself a multiple-antecedent choice. The two judgments are independent, including where the text has both problems.

口诀：“self_containment 看对象有没有交代；ambiguous_referent 看已有对象中到底指哪一个是否唯一。”

The conspicuous 2×2 table contains PASS/NO, PASS/YES, FLAG/NO and FLAG/YES. It is a general boundary, not a keyword rule; actual Candidate text controls each judgment. Two simultaneous abnormal values require separately identifiable reasons.

| Guide locations | Additive coverage |
| --- | --- |
| Quick Start; sections5/6 | Reading sequence and field dictionary use independent tests |
| 7.3 / 7.4 | Exact field questions, canonical values, absent-object versus multiple-antecedent boundary, mnemonic and 2×2 |
| 7.6 | Three recommended `issue_note` patterns; separate reasons when both abnormal |
| 8 | Six prohibited mistakes, including both forbidden automatic implications |
| 9 | Four clearly fictional boundary cases A–D, each with full Phase1 fields and reasons |
| 26 | Two additional high-risk rows; historical rows retained |
| 28 / 29 | FAQ and one-page quick reference synchronize the same four combinations |
| 30 / 31 | Final independent-check item and dated Owner explanation lineage |

| New fictional case | self_containment | ambiguous_referent | Teaching purpose |
| --- | --- | --- | --- |
| A | FLAG | NO | Unidentified “该文件”, no competing antecedents |
| B | PASS | YES | Two named files, last “该文件” has two reasonable antecedents |
| C | FLAG | YES | Two unnamed file objects plus ambiguous later “此文件” |
| D | FLAG | NO | Unidentified “该办法”, no later competing antecedent |

No D1 real Candidate is used as a teaching example. The supplied A–D texts are explicitly fictional and assume no earlier context. Original case05 remains FLAG/NO; original case06 remains PASS/YES. All 30 old cases are verbatim, not merely relabeled. Total now: 31 sections, 34 fictional cases (13 Phase1 / 21 Phase2), 22 high-risk rows, 19 FAQs. Actual workbook field coverage stays 8 Phase1 / 20 Phase2 columns, 26 distinct names; no new field.

## 3. Read-only workbook enum/byte audit

OOXML is inspected in memory only: no Excel opening/save, artifact export or authoring path. Current schema/ID/order and empty answer cells remain unchanged through full-byte parity with the frozen manifests, and before/after read hashes agree.

| Existing workbook | Bytes | Unchanged SHA256 |
| --- | ---: | --- |
| HUMAN-A01 Phase1 V1 | 27608 | `eca6265f10a4afa78c8744d500eff83d147e49cfc5123dab2c8cfa2377e4df73` |
| HUMAN-B01 Phase1 V1 | 27458 | `7736aa431c5b5e94c0059152bc186a314f928401f03df3c00e21b8673ba5a087` |
| HUMAN-A01 Phase2 V1 | 527949 | `76d43b8b48fbab4595b4d561bc09f41046a1ca5cd2f39118fd85de3875baef8a` |
| HUMAN-B01 Phase2 V1 | 523102 | `bad9c6459dc163cd085517a8964deac6c950115486d15b4237d7273f8e138cdf` |

Both Phase1 books retain exactly `self_containment = PASS / FLAG / UNCERTAIN` and `ambiguous_referent = YES / NO / UNCERTAIN`. Other enum and header coverage remain exact. A/B helper parity is retained; the clarification is in the shared Master Guide only. Phase1 remains `DISTRIBUTION_READY_NOT_DISTRIBUTED`; each person's Phase2 is `SEALED_WITHHELD`.

## 4. QA, risk review and claim boundaries

Task-scoped checks pass: guide/enum coverage, original30-case preservation, four new fictional cases, 2×2 and no forced field coupling, current workbook byte parity, guide links, UTF-8, Ruff, MyPy and diff hygiene. Final closeout verifies13 task paths and23 new/added Markdown links, with no added secret/private-path pattern. Near-duplicate screen compares34 teaching examples against144 existing text rows (4,896 pairs, normalized SequenceMatcher threshold0.72): 0 near-duplicates, maximum0.395604. This is a lexical screen plus fictional-topic author inspection, not a statistical leakage proof or annotation result. Neither Expected/GT, private role mapping nor reviewer returns is loaded for this task.

Hash semantics: the artifact SHA values above bind inspected local bytes. An initial direct old-QA-versus-Git byte test hit pre-existing CRLF/LF normalization; the corrected read-only check verifies unchanged startup SHA plus line-ending-neutral Git content parity. No historical file or hash is rewritten to make that check pass. All four XLSX are binary exact-byte comparisons, without normalization.

Forward risk review: (a) avoid replacing one mistaken forced implication with the opposite forced implication; all four combinations explicitly permitted; (b) identify fictional examples and never borrow actual D1 answers; (c) bind old/new hashes without overwriting old QA; (d) retain PDF mismatch limitation and do not edit it outside scope; (e) scope commit paths so pre-existing design/PDF changes are excluded. No unresolved blocker for this documentation-only scope. Existing workbook explanations are not silently rewritten by this Markdown clarification.

No Human annotation, distribution, Phase2 release, new Candidate construction, Ground Truth, split, detector run/training, tuning or calibration occurs. No claim of measured disagreement/rework reduction. This is not V4.4, a reopened calibration, formal benchmark performance or detector superiority.

Reproducible commands (from the branch-bound worktree):

```powershell
python scripts/core144_human_master_guide_qa.py --output docs/research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_SELF_CONTAINMENT_REFERENT_CLARIFICATION_QA_V1.json
.venv\Scripts\ruff.exe check scripts/core144_human_master_guide_qa.py
.venv\Scripts\mypy.exe scripts/core144_human_master_guide_qa.py --follow-imports=skip
git diff --check
git check-ignore .venv .pytest_cache
```

Execution uses the available bundled Python runtime for read-only OOXML/JSON checking; no installation or model download. A separate final task-path check covers new/added Markdown links, strict UTF-8, secret/private-path patterns, expected changed-file allowlist and unrelated-file hash preservation. Git sync is checked after the explicit commit/push, not inferred from this source-HEAD record.

## 5. Mandatory documentation closeout

| Document | Condition / action |
| --- | --- |
| Human Ledger / Agent Ledger / Current State / Execution Log | Mandatory; additive current clarification, counts, scope and next action |
| Project Master Context | Mandatory; additive current boundary and approval limits |
| Owner Decision / Owner Requirement registers | Required by this explicit Owner clarification; PODR-127 / OR-082 |
| Paper1 / Core144 README | Entry counts/navigation changed; latest dated note and new record link |
| Experiment Master | Condition false: no experiment, dataset, schema/protocol, Evidence, metric, run, scientific acceptance or approval-gate change; historical evidence remains valid |
| Stage Process | Condition false: no new phase/gate/stage acceptance or rollback |
| Canonical Lessons | Condition false: only the requested Master Guide clarification; no new accepted methodological lesson or lesson promotion |
| Research Plan Authority | Condition false: frozen research contract unchanged |
| Long-term research requirements | Condition false: no long-term goal/capability change |

```text
human_ledger_checked = TRUE
human_ledger_updated_if_required = TRUE
agent_ledger_checked = TRUE
agent_ledger_updated = TRUE
current_work_state_updated = TRUE
execution_log_appended = TRUE
experiment_master_condition_evaluated = TRUE
owner_decision_condition_evaluated = TRUE
stage_process_condition_evaluated = TRUE
lessons_condition_evaluated = TRUE
research_authority_condition_evaluated = TRUE
README_condition_evaluated = TRUE
cross_document_current_task_consistent = TRUE
cross_document_status_consistent = TRUE
cross_document_next_action_consistent = TRUE
cross_document_blocker_consistent = TRUE
markdown_links_valid = TRUE
DOCUMENTATION_CLOSEOUT_PASS = TRUE
```

Current/task/status/Owner authority, frozen fields, scope exclusions, hashes, evidence links, blocker state, next gate and claim limits are physically recoverable. Current headings explicitly supersede older same-day counts rather than altering historical records. No semantic/approval drift is introduced; optional future Excel explanation synchronization requires a separate Owner instruction. Next action: Owner reviews updated Markdown; no automatic distribution.

Final status:

`CORE144_SELF_CONTAINMENT_REFERENT_BOUNDARY_CLARIFIED / MASTER_GUIDE_UPDATED / HUMAN_WORKBOOKS_UNCHANGED / HUMAN_AB_NOT_YET_DISTRIBUTED`
