# Paper 1 Detector evidence reconstruction and failure-analysis closeout

Date: 2026-09-22. Scope: Owner `PODR-106` A-first/conditional-B resolution and resumed V1.1 **development-set** diagnosis. This record does not accept a formal Detector result.

## Evidence and risk gates

- `FORWARD_RISK_REVIEW / PAPER_RISK_REVIEW`: Original Full OOF and summaries remain canonical; reconstructed eight-model OOF is secondary evidence only; no Oracle/GT label enters inference features; no test-set tuning, calibration, model replacement or causal claim. Final72 is development-exposed and 57-document evidence corpus is too easy for formal retrieval-effectiveness claims.
- Original result manifest SHA256 `e788af67ee1a67d8635ddb11a9a27feeb3d7c89009a87bb3d1788ddfd90737af` and canonical Full OOF SHA256 `eed87a32979cb2d1c85bbd67584cf5a3d2c9cd32789af933758530e65ba9d423` were rechecked after analysis. Original indexed files `10/10` unchanged.
- Reconstruction manifest SHA256 `5924015e75d951223081925dc2ce7429cae23ea798cfbcef98aba5fe296f051b`; nine model files each `72/72`, Full control sample/fold/value parity and all nine machine summaries PASS at fixed absolute `1e-12`.
- Analysis manifest SHA256 `5d9edc8c1031ad9a42fa15a77a85eaa6e0aa7703d89c8f774b2304f979c4f6c8`; two 24-group T/P shift records, feature inventory, hard groups, strata, taxonomy and coefficient signs are indexed and hash-valid. The separate 21×72 applicability overlay was checked against frozen availability source SHA256 `93beba0093821785c2303fe722cb2d5e7da1a99381b5786305e17fe57a68d7b2`.
- Stage 1–5 paths: none modified. The sole unrelated pre-existing dirty trustworthy-retrieval design file was not staged or altered by this task. Secret scan of new code/report found no credential matches; generated Markdown/JSON are UTF-8. `git diff --check`, targeted Ruff and MyPy passed.

## Documentation closeout matrix

| Check | Status / evidence |
| --- | --- |
| Human Ledger checked / updated | TRUE / new plain-Chinese top entry distinguishes recovery from improvement. |
| Agent Ledger checked / updated | TRUE / identities, hashes, source hierarchy, next gate. |
| Current Work State updated | TRUE / previous blocker now historical, next Owner gate explicit. |
| Research Execution Log appended | TRUE / `REL-2026-0071`, prior `REL-2026-0070` preserved. |
| Experiment Master condition evaluated / updated | TRUE / new evidence namespace, original-versus-reconstructed boundary, analysis status. |
| Owner Register condition evaluated / updated | TRUE / `PODR-106`. |
| Stage Process condition evaluated / updated | TRUE / recovery and diagnosis phase appended. |
| Canonical lesson condition evaluated | TRUE / forward-only output-retention contract plus Scale Spec V3; no Pilot4 annotation lesson changed. |
| Research Plan Authority condition evaluated / updated | TRUE / forward-only evidence-retention contract, no method semantics change. |
| README condition evaluated / updated | TRUE / points to current analysis and next gate. |
| Project Master Context and Scale Spec updated | TRUE / current narrative, formal observability and evidence-retention gates. |
| Cross-document current task/status/blocker/next action/claims | TRUE / previous blocker snapshots explicitly marked historical. |
| New Markdown links | TRUE / relative paths to repository artifacts checked. |

`PAPER1_MANDATORY_DOCUMENTATION_CLOSEOUT = PASS_WITH_REPOSITORY_BASELINE_TEST_DEBT`. Task-scoped detector/reconstruction tests: `23 passed`; Ruff/MyPy and evidence/hash gates pass. The broader context-recovery test selection returned `56 passed / 4 failed`, but all four failing predicates were already false in **HEAD before this task**: human research-plan Chinese/English ratio `3355/5474`, one stage-process `LOCAL` token, five absolute-path occurrences in the existing Agent Ledger, and one existing execution-log absolute path. No historical document or governance test was rewritten to make those pre-existing failures green. These four are repository-level baseline QA debt, not evidence-reconstruction parity failures; do not report full repository test suite as passing.

`CONTEXT_PERSISTENCE_CHECK`: Owner decision, original/reconstructed identity boundary, development-only claims, remaining formal gate and private evidence manifests can be recovered from Git plus the Owner handoff root. `PAPER1_DOCUMENT_STALENESS_GATE`: the previous blocker is explicitly superseded, not erased; Formal Experiment remains `NOT_STARTED`. Next required human action: review the failure-analysis/scale-hypothesis package and separately approve or revise 240-group benchmark construction. No automatic execution follows.
