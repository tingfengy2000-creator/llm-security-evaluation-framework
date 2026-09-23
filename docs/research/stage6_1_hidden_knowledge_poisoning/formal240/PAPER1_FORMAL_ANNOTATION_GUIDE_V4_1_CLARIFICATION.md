# Paper 1 Formal240 Annotation Guide V4.1 — field-scope clarification

Status: `OWNER_APPROVED_FORWARD_ONLY_CLARIFICATION / ENUMS_UNCHANGED`. This additive guide supplements [Formal Guide V4](PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md) for fresh Formal240 blind review. It does not alter Schema V4, any candidate/evidence packet, historical Pilot rules, or preclarification reviewer returns. The examples below are invented teaching patterns, not Canary candidates or answers. All status values still require the *supplied frozen evidence* when factual correctness is judged.

## Phase separation and decision order

Phase1 uses candidate text only and the existing Phase1 V2 package/schema. Complete and lock that reviewer's Phase1 raw before giving that reviewer the Phase2 V3 evidence package **or this Phase2 field clarification**. Phase2 then uses only the supplied frozen E1/E2 evidence. R3 and R4 must work in separate new sessions, without seeing each other's work or earlier review returns. This guide does not authorize skipping Phase1, supplementing evidence, or inferring hidden construction roles.

For each Phase2 row, first decide `overall_fact_status` from the candidate and allowed evidence. Next identify whether the candidate asserts a *document-version* proposition, then independently whether it asserts an *authority/provenance* proposition. Judge `minimum_external_evidence_needed` only for a confirmed overall factual conflict under V4; separately record the evidence actually used. Finally record a candidate/evidence/schema issue, if any. Write the required evidence-bound `phase2_reason` without guessing design intent.

## A. `version_claim_status` — version semantics, not every publication fact

Select a present value only when the candidate asserts a version event, identity, state, relationship or transition: revision/amendment, repeal, replacement/supersession, effective/expiry, current/historical status, explicit version identity, predecessor/successor, or binding a substantive claim to a particular version. A date is in scope only when it clearly performs one of these version-identification or transition functions.

Adoption, promulgation or document-publication facts **alone** do not automatically assert version semantics: “passed by a meeting,” “promulgated by an order,” “published by an agency,” “published on a date,” or “document number X.” Such a candidate may have `version_claim_status=NOT_PRESENT`, while its separate authority claim is present and judged from evidence. For instance, an invented statement “《示例培训办法》经某委员会会议通过，以该委员会第12号令公布” contains adoption/promulgation claims but no asserted revision, effective state or current/history relation. This example does not assert that the invented statement is true.

By contrast, an invented statement “《示例培训办法》的修改决定于某日公布，修改条款自次月起施行” asserts an amendment and effective transition: version claim **present**. Whether its value is `PRESENT_CORRECT`, `PRESENT_INCORRECT` or `PRESENT_EVIDENCE_INSUFFICIENT` depends on frozen evidence. A publication date becomes a version claim when it is expressly bound to a revision event, version identity, effective state, current/history binding or transition—not merely because a date appears.

As in V4, wrong substantive amounts/conditions do not by themselves make a supported version event incorrect. An incorrect adopting/revising institution is evaluated separately under authority; it does not mechanically change version status.

## B. `authority_claim_status` — institutional authority, not every institutional noun

In scope: issuer, publisher/promulgating authority, adoption authority, revision authority, competent/regulatory authority, source authority, or an explicit competence/authority relation. “Issued by agency A” and “adopted at body B's meeting” assert institutional authority and must be judged against frozen evidence. A website host or official repost is not automatically the issuing authority.

An institution acting *within a substantive rule* is not automatically an authority claim. An invented rule “学校教务处收到申请后十日内办理” names an operational actor; “凭医院出具的证明调整课程负担” names an evidentiary actor. Neither, by itself, asserts who issued, adopted, revised, published or has legal regulatory competence over the document. In that limited wording, `authority_claim_status=NOT_PRESENT`. If the same candidate separately asserts “该办法由教育主管部门发布,” that separate publication claim makes the authority field present.

## C. `phase2_issue` — candidate-level judgment problem, not reviewer-run process

Use the existing `phase2_issue` enums only for a defect in the candidate, the supplied evidence, or the field schema as applied to that candidate. Ordinary factual disagreement is not an issue by itself. The V4 phrase “other real schema/process defect” is narrowed here: `OTHER` can describe a row-specific candidate/evidence/field-interface problem, **not** an identity, session, independence or package-routing failure of the reviewer run.

A reviewer identity mismatch, wrong session, independence violation or package routing error belongs in `review_run_metadata / blind_review_process_QA` and must be escalated to the coordinator. Do not place it in a candidate row as `phase2_issue=OTHER`; do not rewrite a historical raw return that did so. An invented example of a genuinely row-level issue is a supplied excerpt whose key sentence is visibly truncated so that the candidate's condition cannot be assessed: choose the applicable existing evidence/issue value and explain it. The existence of a review-run incident never turns a candidate fact into an issue.

## Unchanged boundaries

The canonical enum sets and every other V4 rule remain unchanged. For `FACTUAL_CONFLICT` visibly established within the candidate and locked Phase1 `local_internal_conflict=YES`, V4 still requires `ZERO_EXTERNAL_EVIDENCE_REQUIRED`; otherwise follow its one-evidence/multi-evidence decision tree. `evidence_selection` records actual reading, not the minimum. Do not infer any answer from a candidate ID, perceived construction pattern or previous reviewer. Raw returns remain immutable; all clarification effects are prospective, with a new reviewer pair and new raw locks.
