# D1 Canary blind quality review — R3-gpt Phase1

You are reviewer `R3-gpt` in a fresh, independent session. Work alone. Do not inspect a project repository, handoff folder, other reviewers' work, coordinator/owner notes, mappings, expected answers, later-phase evidence, previous chat or memory context, or any external source. Do not ask another AI assistant or search the web. This is pre-annotation quality review, not Ground Truth annotation.

Read only the supplied `PAPER1_FORMAL_D1_BLIND_REVIEW_PACKAGE_PHASE1_V2.json`, `PAPER1_FORMAL_D1_BLIND_REVIEW_IMPORT_SCHEMA_V2.json` and this prompt. For each opaque ID, assess candidate text alone: `text_naturalness`, `local_internal_conflict`, `self_containment`, `ambiguous_referent`, `meta_or_template_language`, and concise `issue_note` if needed. A suspected real-world error requiring a source is not a text-internal contradiction. Do not look up facts or infer hidden design intent.

Return exactly one JSON array of 24 objects, in packet order, with exactly the Phase1 schema keys and canonical enums. Preserve every `blind_review_id` and candidate wording. Submit raw JSON to the coordinator. Wait for confirmation that **both fresh reviewers' Phase1 returns have been byte-locked and run attestations passed** before viewing any Phase2 material. Report a session/routing incident separately from candidate JSON.
