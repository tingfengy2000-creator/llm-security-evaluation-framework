# Formal annotation Guide V4.3 — temporal comparison versus document-version claim

Status: Owner-approved additive, forward-going clarification. Inherits V4, V4.1 and V4.2; no enum, candidate, evidence or historical reviewer return is changed. This rule is applied to the locked HKP1 Batch-1 returns only through a separately attributed Owner overlay.

## Candidate-only scope test

First read the candidate text **without using Evidence metadata to invent a claim**. A temporal or historical proposition is not necessarily a claim about a document version. `overall_fact_status=LEGITIMATE_VERSION_OR_HISTORY` and `version_claim_status=NOT_PRESENT` can coexist.

`version_claim_status=PRESENT_*` only when the candidate explicitly asserts a document-level revision/amendment, original or revised version identity, version state (including a document's current validity), repeal, replacement, predecessor/successor, supersession, amendment-decision identity, or an effective/expiry transition of that document. Frozen Evidence then determines whether that explicit assertion is correct or insufficiently supported. Explicit wording such as “2013年版”, “2024年修订版”, “1994年原版”, “现行版”, “经修改后的版本”, or “被废止” remains within scope.

Mere dates, two time points, a comparison of substantive numbers or conditions in two distinct dated documents, or a statement that a **substantive value** is “目前” in a dated reply do **not** by themselves assert document-version identity or relation. A title containing “调整通知” does not by itself say that this document is a revision of another document. Likewise, a 1988 regulation compared with a differently titled 2012 regulation can be a legitimate historical comparison without a stated original/revised-document relationship.

Decision flow: (1) isolate what the candidate says about the *document*, rather than what Evidence pages say; (2) look for an explicit version event/identity/state/relation/transition; (3) if absent, select `NOT_PRESENT` even if the overall proposition requires historical Evidence; (4) if present, use only frozen Evidence to select the appropriate `PRESENT_*` value. Keep authority and substantive-content judgments independent. Do not relabel an incorrect numerical comparison as an incorrect version claim merely because both involve dates.

This clarification resolves a field-scope disagreement, not a factual or evidence-sufficiency disagreement. It does not authorize post-hoc evidence expansion, new Reviewer rounds for ordinary covered differences, or Ground Truth creation.
