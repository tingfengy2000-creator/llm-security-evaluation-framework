# D1 Remaining90 Phase1 — R4-codex independent blind quality review (provider-corrected V2)

`R4-codex` is a stable reviewer **code**, not a claim that the Codex product is used. The actual reviewer platform/model for this run is **Doubao**. Start a fresh independent Doubao conversation with no prior D1/Canary chats, inherited project instructions, knowledge base, memory, repository, files, or other reviewer output. If a project/workspace is used, it must be newly isolated and contain only the three authorized Phase1 files below; a Codex `projectless` task is **not** required. If isolation cannot be established, stop and tell Owner before reviewing. Owner will attest the run boundary; a filename or code name is not platform proof.

Receive exactly these three files from Owner:

1. `PAPER1_FORMAL_D1_REMAINING90_R4_CODEX_PHASE1_PACKAGE_V1.json` — 90 candidate-only questions.
2. `PAPER1_FORMAL_D1_REMAINING90_PHASE1_IMPORT_SCHEMA_V1.json` — exact answer schema.
3. This `PAPER1_FORMAL_D1_REMAINING90_R4_CODEX_PHASE1_PROMPT_V2.md`.

Do not open a repository, E: handoff directory, Owner/construction files, older answers, R3/R5 output, Evidence/Phase2 files, mapping, labels, Expected, or GT. Do not browse the web or use another AI. If prohibited context becomes visible, stop and provide an incident report separately; do not submit it as an answer.

This is pre-annotation quality review, **not Ground Truth**. Read each `candidate_text` independently. Do not infer hidden intent or determine real-world legal correctness. For every opaque `blind_review_id`, fill exactly:

- `text_naturalness`: `NATURAL` = clear ordinary wording, even if a fact may be wrong; `MINOR_ISSUE` = slight awkwardness but understandable; `UNNATURAL` = serious wording/grammar defect.
- `local_internal_conflict`: `YES` only when two visible claims in the same candidate cannot both hold under the same subject, scope, time and condition; `NO` if verifying a suspected error needs outside facts; `UNCERTAIN` only when the text itself obscures whether there is an internal conflict.
- `self_containment`: `PASS` if the subject and core claim make sense without another candidate; `FLAG` if essential context is absent; `UNCERTAIN` if the text leaves this undecidable.
- `ambiguous_referent`: `YES` only if a key reference can point to multiple visible antecedents; `NO` otherwise; `UNCERTAIN` if unresolved from this text.
- `meta_or_template_language`: `YES` for visible experimental, placeholder or template residue; `NO` otherwise; `UNCERTAIN` if unclear.
- `issue_note`: a concise text-visible reason for any non-default/uncertain/flagged value, otherwise an empty string. Do not cite sources or guess the experimental label. A real-world fact suspicion is not an internal contradiction.

Save ONE original UTF-8 strict JSON file named `PAPER1_FORMAL_D1_REMAINING90_R4_CODEX_PHASE1_RAW_RETURN_V2.json`. It must be a JSON **array of exactly 90 objects**, in exactly the package order, with exactly the seven schema keys, canonical English enum strings, all supplied IDs unchanged and no extra fields. No Markdown fences, commentary, or explanation outside the JSON file. Before submission, self-check JSON parse, 90 unique IDs, exact ID set/order, enum spellings, nonblank issue notes when flagged, and no truncation. Send the original saved file to Owner; do not reformat or resave it. Do not view Phase2 until Owner confirms both Phase1 raw files were byte-locked and accepted. Remain in this SAME isolated Doubao conversation for later Phase2 if authorized.
