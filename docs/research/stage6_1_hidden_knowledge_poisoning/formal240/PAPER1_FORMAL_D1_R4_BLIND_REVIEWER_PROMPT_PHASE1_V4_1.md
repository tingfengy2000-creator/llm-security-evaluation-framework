# D1 Canary blind quality review — R4 Phase1

You are reviewer R4 in a fresh, independent session. Work alone. Do not inspect a repository, other reviewers' work, coordinator notes, mappings, expected answers, later-phase evidence, or any external source. Do not ask another AI assistant. This is pre-annotation quality review, not Ground Truth annotation.

Read only the supplied `PAPER1_FORMAL_D1_BLIND_REVIEW_PACKAGE_PHASE1_V2.json` and `PAPER1_FORMAL_D1_BLIND_REVIEW_IMPORT_SCHEMA_V2.json`. For each opaque ID, assess the candidate text alone: `text_naturalness`, `local_internal_conflict`, `self_containment`, `ambiguous_referent`, `meta_or_template_language`, and a concise `issue_note` if needed. A suspected real-world error requiring a source is not a text-internal contradiction. Do not look up facts. Do not infer hidden design intent.

Return exactly one JSON array of 24 objects, in packet order, with exactly the Phase1 schema keys and canonical enums. Preserve every `blind_review_id` exactly and do not revise candidate wording. Submit the raw JSON to the coordinator. Wait for confirmation that **your own Phase1 return has been byte-locked** before viewing any Phase2 package or field guide. If you notice a session/routing mismatch, tell the coordinator outside the per-candidate JSON; do not convert it into a candidate issue.
