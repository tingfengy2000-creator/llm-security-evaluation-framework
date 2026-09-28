# Core144 Human Master Guide V1 — documentation QA and closeout

Task: `P1-CORE144-HUMAN-ANNOTATION-MASTER-GUIDE-V1-01`. Machine: LOCAL. Role: explanation-only documentation repair and read-only schema inspection. Source HEAD: `77f877e062baea1e4f72c419cf8cac2142ff03e4`; dynamically selected branch: `research/stage6-1-hidden-poisoning`. Upstream preflight was 0/0. The pre-existing unrelated Stage6 design-spec edit is excluded, not reset or committed.

## Authority and source receipt

Owner's current directive is attachment `18419beb-8ffe-4b84-b423-2e37d0d829a0`, 36,789 bytes, SHA256 `d03d6734a260cc28d2e1f4e5f24bbdee1735060fbc7506804311e9828d64e28e`. Approval is for a self-contained Chinese human manual, not new annotation semantics, workbook editing, distribution or downstream experiments. `PODR-126 / OR-081 / REL-2026-0095` bind this scope.

The [machine receipt](PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_QA_V1.json) records exact source hashes, the four current workbook hashes, all actual headers/validation enums/sheet names, field→section→authority mapping and rule→section mapping. Workbooks were opened as OOXML for read-only inspection. No workbook save/export/regeneration was executed. A/B helper-sheet text matches after replacing only the person code; main-table contents were not displayed or used as answers.

No Expected, GT, private mapping, reviewer raw or Owner sample overlay was loaded. Actual Candidate texts were used only for a mechanical example-leakage screen, not annotated or copied into the manual. The manual has no live-data answer key. Its fictional examples cover distinct library/exhibition/storage topics, not renamed HR Candidate answers.

## Scope and quality results

- [Master Guide](PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_V1.md): 31 numbered sections; 30 complete fictional cases (9 Phase1, 21 Phase2); 20 high-risk rows; 18 FAQ answers. Approximately 15,812 Chinese characters; slightly above the suggested band to retain complete case explanations without omitting boundaries.
- Actual fields: Phase1 8 columns, Phase2 20 columns, 26 unique names (two shared). All fields have a Chinese explanation; all canonical validation values occur in the guide. Phase1 five categorical decisions plus conditional note, Phase2 eight categorical decisions plus mandatory reason and optional note match actual XLSX.
- Rule coverage: V4 base plus additive V4.1/V4.2/V4.3. Candidate-only version presence, amendment-decision identity, ordinary operational actor, host/repost/issuer separation, historical-without-version, ZERO/ONE/MULTI ablation, actual selection independence, row-level issue scope and overall/subfield insufficiency exception are expanded, not merely linked.
- Five historical conflict classes were identified and **not propagated**: old Phase1 columns; old optional expression-only reason; Pilot internal-conflict minimum workaround; revised-content/authority errors conflated with version; obsolete candidate-ambiguity enum. Source documents and past returns remain unchanged. Current semantic rules added/removed/changed: `0/0/0`.
- Normalized SequenceMatcher near-duplicate screen compares 30 teaching texts against 144 actual texts: 4,320 pairs, threshold ≥0.72, max ratio 0.368421, hits 0. This is a lexical screen supplemented by author semantic inspection, not proof that every possible future paraphrase detector will return zero.
- Four workbook bytes remain exactly manifest-matching, with answer cells still empty; ID/order cannot have changed because each complete XLSX SHA is unchanged. Phase1 `DISTRIBUTION_READY_NOT_DISTRIBUTED`; Phase2 `SEALED_WITHHELD`.

`FORWARD_RISK_REVIEW / PAPER_RISK_REVIEW`: old-rule carryover, hidden-answer teaching leakage, rule drift, Evidence expansion, workbook mutation, premature release and unverifiable quality claims were checked. No affected blocking conflict remains. The guide is a documentation deliverable; it does **not** establish measured reduction in human disagreement or reproducibility before actual human returns.

## Reproduce

From the unique research worktree, use the existing environment:

```powershell
.venv\Scripts\python.exe scripts/core144_human_master_guide_qa.py --output docs/research/stage6_1_hidden_knowledge_poisoning/core144/PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_QA_V1.json
.venv\Scripts\ruff.exe check scripts/core144_human_master_guide_qa.py
.venv\Scripts\mypy.exe --follow-imports=silent scripts/core144_human_master_guide_qa.py
git diff --check
```

The QA script reads the existing manifests to locate authorized workbooks; it emits neither local private paths nor actual Candidate text/IDs into the receipt. Initial read-only helper inspection had one Python one-liner syntax error, then was rerun successfully; no workbook was written during either attempt. Full QA, task-scoped Ruff/MyPy, strict UTF-8, new-file secret/private-path scan, link checks and Git diff checks pass. Stage1–5, Final72, all existing Core144 corpus/guide/evidence/manifest/workbook artifacts are unchanged.

## Mandatory documentation closeout

| Document | Decision and evidence |
|---|---|
| Human Ledger | Updated in ordinary Chinese: why the manual is needed, what it adds, no workbook/data/rule change, Owner review next. |
| Agent Ledger | Updated with exact task, counts, receipt, boundaries and next gate. |
| Current Work State | New dated entry: manual ready, workbooks unchanged, human distribution still unreported, Phase2 sealed. |
| Research Execution Log | Appended REL-2026-0095; does not rewrite earlier execution. |
| Project Master Context | Additive current entry supersedes stale opening “Phase2 returns pending”; does not rewrite history. |
| Owner Decision / Owner Requirement | PODR-126 / OR-081 records this documentation-only directive, not new scientific acceptance. |
| Core144 and Paper1 README | New guide navigation and present Owner-review step. |
| Experiment Master | Checked; no experiment/data/evidence/protocol/metric/gate change. Prior Full144 acceptance and workbook statuses remain accurate; no edit required. |
| Stage Process | Checked; no new annotation phase or changed scientific gate, no edit required. |
| Canonical Lessons | Read; history retained, no new empirical reusable lesson or promotion claimed. |
| Research Plan Authority | Frozen scientific contract unchanged; no edit. |
| Parallel workstream V1 and frozen manifests | Historical/accepted artifacts unchanged. D2/D3 construction not performed this turn. |

`DOCUMENTATION_CLOSEOUT_CHECKLIST`: Human Ledger checked/updated; Agent Ledger checked/updated; current state updated; execution log appended; conditional Experiment Master/Owner/Stage/Lessons/Research Authority/README decisions evaluated; current task/status/next step/blocker consistent; changed-document links valid. All required items PASS. `CONTEXT_PERSISTENCE_CHECK / PAPER1_DOCUMENT_STALENESS_GATE = PASS` through dated additive entries and this receipt. Git commit and sync are verified dynamically after the single docs commit, not invented as a self-referential hash here.

## Final boundary

`CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_READY / CURRENT_HUMAN_WORKBOOKS_UNCHANGED / HUMAN_AB_NOT_YET_DISTRIBUTED`.

Owner next action: review the master guide; decide later whether explanatory content should be synchronized into Excel and when to distribute each person's Phase1. No Excel mutation, human annotation, Phase2 release, D2/D3 construction, GT, split, detector, tuning, calibration or formal result is executed by this task.
