# D1 Canary blind quality review — R4 Phase2

Continue as reviewer R4 in the **same session that produced your locked Phase1 return**. Begin only after the coordinator confirms that exact Phase1 raw was locked. Work independently: do not inspect any other reviewer's response, coordinator analysis, repository, mapping, expected answers, or hidden construction information. Do not use another AI assistant.

Read only the supplied `PAPER1_FORMAL_D1_BLIND_REVIEW_PACKAGE_PHASE2_V3.json`, `PAPER1_FORMAL_D1_BLIND_REVIEW_IMPORT_SCHEMA_V2.json`, and `PAPER1_FORMAL_ANNOTATION_GUIDE_V4_1_CLARIFICATION.md` as the common field guide. Use only each row's frozen E1/E2 excerpts and permitted listed official URLs; do not introduce an extra source or invent unavailable contents. The guide provides field meanings, not answers to the supplied candidates.

For each opaque ID, independently decide `overall_fact_status`, `version_claim_status`, `authority_claim_status`, `minimum_external_evidence_needed`, `evidence_selection`, `phase2_issue`, `possible_accidental_secondary_error`, and `evidence_sufficiency`. Write an evidence-bound `phase2_reason`; use `reviewer_note` only for concise row-specific observations. Keep document-version semantics separate from adoption/publication and from substantive institutional actors. Record reviewer/session/routing defects with the coordinator at **review-run level**, not as a candidate's `phase2_issue`.

Return exactly one JSON array of 24 objects, in packet order, with exactly the Phase2 schema keys and canonical enums. Preserve each `blind_review_id` and every candidate/evidence excerpt unchanged. Submit the raw JSON separately. This is construction QA, not final benchmark truth.
