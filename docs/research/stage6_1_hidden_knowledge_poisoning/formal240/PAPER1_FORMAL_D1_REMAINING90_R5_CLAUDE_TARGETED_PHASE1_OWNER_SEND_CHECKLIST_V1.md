# Owner sending checklist — independent Claude auxiliary Phase1 review

Use one **new isolated Claude conversation**. Send **only** these three files, in this order:

1. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining90_claude_aux_phase1_20260927\reviewer_release\PAPER1_FORMAL_D1_REMAINING90_R5_CLAUDE_TARGETED_PHASE1_PACKET_V1.json`
2. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining90_claude_aux_phase1_20260927\reviewer_release\PAPER1_FORMAL_D1_REMAINING90_R5_CLAUDE_TARGETED_PHASE1_IMPORT_SCHEMA_V1.json`
3. `E:\LLMGuard-Handoff\paper1_formal240_d1_remaining90_claude_aux_phase1_20260927\reviewer_release\PAPER1_FORMAL_D1_REMAINING90_R5_CLAUDE_TARGETED_PHASE1_PROMPT_V1.md`

Do not send the whole parent folder, especially `control_only_do_not_send`. Do not send R3/R4 raw answers, their notes or summaries, the list of which field disagreed, old R5 responses, construction dossiers, role/HKP/S mapping, Expected/GT, Evidence or Phase2. Claude should not browse the web or use another AI. If the Claude chat/project inherits any D1 history or prior materials, start a new isolated environment before sending. The `R5-claude` code is **auxiliary pre-annotation QA**, not a third Ground Truth annotator or final Owner adjudicator.

Ask for one original file named `PAPER1_FORMAL_D1_REMAINING90_R5_CLAUDE_TARGETED_PHASE1_RAW_RETURN_V1.json`: strict UTF-8 JSON array of 10 objects, exact schema and packet order. Forward the unchanged saved file to this task for byte lock and validation. Do not paste/reconstruct/resave its raw contents. Keep Phase2 withheld pending Owner adjudication of any material disagreement.
