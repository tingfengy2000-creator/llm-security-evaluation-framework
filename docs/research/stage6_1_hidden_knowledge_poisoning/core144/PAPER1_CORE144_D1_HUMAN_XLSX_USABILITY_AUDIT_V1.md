# D1 Full144 Human XLSX usability and leakage QA

Result: **PASS for Phase1 distribution preparation**, not evidence of actual distribution or annotation. The four final XLSX files and their checksums are in the four additive manifests beside this report. Phase2 remains `SEALED_WITHHELD`.

## Source receipt and lineage

- Accepted population source: [Full144 acceptance matrix](PAPER1_CORE144_D1_FULL144_ACCEPTANCE_MATRIX_V1.json), combining locked Canary 24 + HKP1 Batch-1 30 + remaining90 90. No Expected, GT, Owner semantic overlay or reviewer answer entered the workbook payload builder.
- Candidate text was checked against the three frozen Phase2 question packets and corresponding current Phase1 candidate records before workbook creation. The private ID mapping and random salts are held outside Git in a separate private handoff folder; no mapping is embedded in either XLSX.
- A and B each contain the same set of 144 Candidate texts, with different opaque IDs and independently randomized order. The within-annotator Phase1/Phase2 ID and order digests match; A/B ID sets are disjoint. Each person's Phase2 keeps exactly their Phase1 ID/order.

## Read-back and visual checks

`scripts/formal240_d1_human_workbooks_qa.py` reopened all four XLSX files using an independent OOXML reader. Phase1: 7 visible sheets, 144 rows, 5 canonical enum dropdowns, answer cells empty, no URL or Evidence. Phase2: 10 visible sheets, 144 rows, 8 canonical enum dropdowns, 225 clickable official-URL formula cells per workbook (144 E1 + 81 optional E2), answer cells empty, full frozen E1/E2 text in the visible same-ID evidence appendix. In each workbook, first row and first two main columns freeze at `C2`; the main table has a filter and no merged answer cells. Candidate text and full packet excerpts were checked byte-for-byte as Unicode strings after XLSX read-back. Neither hidden mapping nor original reviewer IDs appeared in workbook cells.

All 7 Phase1 and 10 Phase2 sheet previews were rendered for each annotator, plus Phase2 answer-column previews. The first main rows, guide, examples, and evidence appendix were visually inspected for legibility. The main Phase2 excerpt is a bounded navigation preview; the entire frozen text is preserved in the visible 【冻结证据全文】 sheet under the same ID. Rows are 180 points high; Candidate text is wrapped. A first internal draft had two sheet names containing `/`, which violates Excel's sheet-name grammar despite successful export. It was not distributed. The final `V1` workbook bytes were regenerated with equivalent valid names 【版本与历史判断】 and 【权威与机关判断】, then successfully reopened. This does not change annotation semantics.

No installed Excel/LibreOffice desktop executable was found on this host, so a native interactive Office open was **not independently performed**. The successful OOXML read-back and artifact-tool render are the available compatibility and visual evidence; do not misreport them as a native Excel session. Owner may perform a final local open check before sending without resaving the frozen source.

## Leakage, separations, and release decision

- Phase1 contains neither frozen Evidence nor Phase2 fields. The guides use only fictional teaching examples and do not expose D1 sample answers. There is no hidden answer sheet, mapping, target label, HKP, S or GT field.
- Phase2 contains only the allowed question-row E1/E2, including optional blank E2 rows. It is stored in a separate sealed directory; its existence is not authorization to send it.
- The A/B distribution-ready source files are byte-hashed and copied to separate named folders. The private mapping file SHA256 is `3d4ee3e8de55e014330b6f64441761ac2b120d22216e71f7a2372f7f425fb014`, held outside Git and never included in a workbook.
- `D1_HUMAN_AB_PHASE1_DISTRIBUTION_AUTHORIZED = TRUE`; `A_PHASE1_DISTRIBUTED = FALSE`; `B_PHASE1_DISTRIBUTED = FALSE`; `A_PHASE2_RELEASED = FALSE`; `B_PHASE2_RELEASED = FALSE`.

The only remaining human action for Lane A is for Owner to send **A's Phase1 V1 XLSX only to A** and **B's Phase1 V1 XLSX only to B**, after optional native open inspection. No Core GT, split or training follows automatically.
