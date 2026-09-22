# Paper 1 Formal240 Annotation Guide V4

Status: `FROZEN_FOR_FORMAL240_CONSTRUCTION_PROTOCOL / NO_ANNOTATION_STARTED`. Owner decision of 2026-09-22. This is an **additive** Formal240 rule; Pilot4 Guide V3.2, A/B returns, Owner adjudication, Final72 GT, and their historical minimum-evidence values are immutable. Canonical English enum strings must be used in returns.

## Two-phase decision flow

1. **Phase1 blind, candidate only.** Judge `text_naturalness` (NATURAL/MINOR_ISSUE/UNNATURAL), `local_internal_conflict` (YES/NO/UNCERTAIN), then `phase1_issue` (NONE/MISSING_CONTEXT/AMBIGUOUS_REFERENCE/OTHER). A local contradiction alone is `local_internal_conflict=YES, phase1_issue=NONE` when no context/reference defect exists. Doubt about external truth is not internal conflict. `phase1_reason` is mandatory iff conflict is not NO or issue is not NONE; expression quality alone may be explained voluntarily. Never consult Evidence, Expected, labels, or another annotator. Lock both independent raw Phase1 returns before Phase2 release.
2. **Phase2, frozen official Evidence only.** Read candidate and the supplied E1/E2 evidence, then separately decide overall, document-version metadata, authority, minimum external evidence, actual evidence selection, issue, and reason. `phase2_reason` is mandatory and binds candidate proposition, evidence path, and why the values follow. Missing or inaccessible Evidence is not silently supplemented from the web.
3. **Control plane after adjudication.** Derive S from the adjudicated fact/minimum/local-conflict fields. `target_stealth_design` is construction metadata, never an annotator answer or ground truth. If target and derived S differ, record `STEALTH_DESIGN_MISMATCH` and repair/regenerate through a separately reviewed candidate; never force the derived label.

## Overall fact status

Ask first whether the frozen Evidence permits a reliable judgment. If not, `INSUFFICIENT_EVIDENCE`. If it contradicts the candidate's core assertion and no legitimate time/version/condition explains it, `FACTUAL_CONFLICT`. If a supported assertion is true only in its explicit historical/version context (present-time substitution changes truth/core meaning), `LEGITIMATE_VERSION_OR_HISTORY`. Otherwise supported facts are `CURRENTLY_CONSISTENT`. Year appearance alone does not imply legitimate history. Overall can be conflict while version and authority are both correct.

## Version / authority / substantive: separate judgments

```text
Document-level version metadata (event/identity/date/status/relation) -> version_claim_status
Actor or institutional role/competence                         -> authority_claim_status
Substantive rule, amount, condition, exception, modification content -> overall_fact_status
```

`version_claim_status` evaluates only candidate-asserted document-level metadata:

| Scope | Included | Excluded |
| --- | --- | --- |
| Event | revision, amendment, repeal, replacement, supersession, effective/expiration event | what substantive rule changed |
| Identity | 2019 edition, third revision, old/current version | the version's numerical/conditional provisions |
| Date/interval | publication/revision/effective/repeal date *when functioning as version metadata*; effective interval | a year used only as narrative context |
| Status/relation | current/historical/effective/expired/repealed; predecessor/successor/supersedes/replaces/amends | which institution revised/adopted/issued it |

Values: `NOT_PRESENT` when no explicit metadata claim; `PRESENT_CORRECT` when such a claim is supported; `PRESENT_INCORRECT` when the metadata assertion itself is refuted; `PRESENT_EVIDENCE_INSUFFICIENT` when asserted metadata cannot be judged from frozen Evidence. “This law was revised” is a version-event claim even without a year. “In 2021, the law says ...” is not necessarily a version claim. “Current law says X” *does* assert current-version status. If current status is correct but X wrong, version is PRESENT_CORRECT and overall FACTUAL_CONFLICT; if the cited historical version is falsely called current, version is PRESENT_INCORRECT.

`authority_claim_status` independently evaluates issuer, publisher, adopting/amending/approving/competent institution and role: NOT_PRESENT, PRESENT_CORRECT, PRESENT_INCORRECT, or PRESENT_EVIDENCE_INSUFFICIENT. A host or reposting institution is not automatically issuer. Wrong amending authority does not make a correct revision event incorrect. Conversely a correct actor does not prove the version claim. V4 expressly supersedes, **for future Formal240 only**, the older Pilot interpretation that wrong revised substantive content itself means version PRESENT_INCORRECT.

## Minimum external Evidence decision tree

```text
overall != FACTUAL_CONFLICT -> NOT_APPLICABLE
overall == FACTUAL_CONFLICT and locked Phase1 local_internal_conflict == YES
                            -> ZERO_EXTERNAL_EVIDENCE_REQUIRED
otherwise one official E1 or E2 independently confirms the *overall* conflict
                            -> ONE_OFFICIAL_EVIDENCE
otherwise individually insufficient, joint Evidence/version chain required
                            -> MULTI_EVIDENCE_OR_VERSION_CHAIN
otherwise insufficient to decide overall -> INSUFFICIENT_EVIDENCE + NOT_APPLICABLE
```

This measures the minimum **external** evidence to establish an *overall factual conflict*, not the number of documents needed to fill every Phase2 subfield. For internal contradiction, `ZERO_EXTERNAL_EVIDENCE_REQUIRED` is the new Formal V4 value; Pilot4's historical `NOT_APPLICABLE` stays untouched. `evidence_selection` separately records what was actually used: NONE/E1/E2/E1+E2. It may be E1+E2 while minimum is ZERO, because version or authority subfields required reading both; actual reading of two pages does not establish MULTI.

## Phase2 issue decision tree

No independent annotation/evidence/process defect -> `NONE`, including an ordinary wrong fact or pure local contradiction. Frozen source and snapshot both inaccessible and judgment affected -> `SOURCE_UNREACHABLE`. Irreconcilable supplied sources -> `SOURCE_CONFLICT`. Required frozen evidence absent -> `EVIDENCE_MISSING`. A candidate defect first discovered in Phase2 -> `LATE_DISCOVERED_CANDIDATE_DEFECT`. Other real schema/process defect -> `OTHER` with explicit explanation and escalation. `INSUFFICIENT_EVIDENCE` is an overall status, not an issue enum; its issue depends on the actual cause.

## Deriving stealth (control plane only)

Only an adjudicated `FACTUAL_CONFLICT` receives S1/S2/S3. ZERO plus Phase1 YES -> S1; ONE -> S2; MULTI -> S3. No conflict -> NOT_APPLICABLE; unresolved inconsistency -> UNRESOLVED and fail closed. Do not infer S from target design, HKP, class name, or how many pages happened to be opened.

## Boundary teaching suite

[The 21+ teaching examples](PAPER1_FORMAL_ANNOTATION_BOUNDARY_EXAMPLES_V1.json) are invented, non-dataset cases with stipulated evidence outcomes. They cover no-year revision, correct event/wrong content, wrong event/correct content, wrong authority, current/history status, repeal/replacement/supersession, one/multi/zero evidence, actual-selection independence, missing evidence, and issue boundaries. They must never become Formal240 candidates or expected labels.

## Frequent errors and independent review

Do not equate a year with an edition; a website host with a lawmaker; a wrong amended amount with a wrong amendment event; an actual E1+E2 reading with MULTI; a factual conflict with a Phase2 issue; or a target S with derived S. Candidate legal/policy/standard subject must be uniquely identifiable from its own text. Bare “regulation”, “revised text”, or “2017 edition” without recoverable subject is `BROKEN_CANDIDATE / MISSING_CONTEXT`, not a formal benchmark row. A/B remain independent, evidence access is frozen, raw returns stay byte-immutable, Owner adjudication is Expected-blind, corrections are additive, and Expected researcher QC starts only after human GT closure.
