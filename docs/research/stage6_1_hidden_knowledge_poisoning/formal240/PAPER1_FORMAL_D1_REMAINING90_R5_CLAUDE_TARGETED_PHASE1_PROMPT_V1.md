# D1 remaining90 — R5-claude targeted Phase1 auxiliary blind review

Use a **new isolated Claude conversation** with no prior D1/Canary chat, memory, inherited project file/instruction, R3/R4 answer, repository or handoff-directory access. Receive **only** the targeted packet, its 10-row import schema and this prompt. Do not browse the web or use another AI. If prior answers or hidden construction context are visible, stop and report the isolation issue separately.

You are an **auxiliary pre-annotation quality reviewer**, not a Ground Truth annotator or final arbitrator. Ten candidate texts were selected for a targeted Phase1 quality check. You are not told which field was disputed, the other reviewers' answers, candidate roles or intended labels. Judge each text independently from its visible wording; do not infer why it was selected. Do not check real-world facts or consult external Evidence.

For each `blind_review_id`, use the exact seven schema keys in this order:

1. `blind_review_id`: copy the opaque ID exactly.
2. `text_naturalness`: `NATURAL` for clear ordinary Chinese even if a fact might be wrong; `MINOR_ISSUE` for slight awkwardness with an understandable core meaning; `UNNATURAL` for serious wording or grammar defects.
3. `local_internal_conflict`: `YES` only if two claims visible **inside this same text** cannot both hold for the same subject, scope, time and condition; `NO` if deciding whether a claim is wrong requires outside facts; `UNCERTAIN` only if the text itself obscures whether an internal conflict exists.
4. `self_containment`: `PASS`, `FLAG`, or `UNCERTAIN` according to whether the core subject and claim can be understood without another candidate.
5. `ambiguous_referent`: `YES`, `NO`, or `UNCERTAIN` according to whether a key reference can point to multiple visible antecedents.
6. `meta_or_template_language`: `YES`, `NO`, or `UNCERTAIN` for visible experimental, placeholder or template residue.
7. `issue_note`: one concise reason grounded in visible text if any of the five judgments differs from `NATURAL/NO/PASS/NO/NO`; otherwise an empty string. Do not cite websites or guess hidden intent.

Return one original UTF-8 **strict JSON array of exactly 10 objects** in exact packet order, with 10 unique unchanged IDs, exact keys/order and canonical English enum strings. Save it as `PAPER1_FORMAL_D1_REMAINING90_R5_CLAUDE_TARGETED_PHASE1_RAW_RETURN_V1.json`. No Markdown fence, extra fields, preamble, summary or explanation outside the JSON file. Check parsing, IDs/order, enums, note rule and completeness before sending the original file to Owner. Do not view Phase2, R3/R4 returns, construction files or hidden mappings.
