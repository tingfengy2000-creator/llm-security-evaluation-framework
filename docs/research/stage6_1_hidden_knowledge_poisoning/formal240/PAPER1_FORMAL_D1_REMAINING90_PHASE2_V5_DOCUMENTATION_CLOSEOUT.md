# Paper 1 mandatory documentation closeout — D1 remaining90 Phase2 V5 handoff

Date: 2026-09-27. Scope: targeted-four Phase1 raw lock, 90-row overlay, Owner-bounded frozen-Evidence projection, and **ready-for-Owner-distribution** Phase2 V5 reviewer files. `PAPER1_MANDATORY_DOCUMENTATION_CLOSEOUT=PASS_FOR_THIS_HANDOFF`. This does **not** mean either external Phase2 reviewer has returned, D1 Full48 passed, or Human A/B started.

| Required sync / check | Result |
| --- | --- |
| Human Ledger | Updated in ordinary Chinese: why four rows were repaired, what the reviewers confirmed, why the two-source decision mattered, what Owner now sends and what is still withheld. |
| Agent Ledger | Updated with immutable SHAs, 86+4 Phase1 lineage, two-group exception, provider `R4-codex` = Doubao and current gate. |
| Current Work State | Latest heading now says V5 ready for same-session Owner distribution; earlier pending states remain dated history. |
| Owner Requirement Register / Decision Register | Added `OR-078/079` and `PODR-123/124`, separating the naturalness decision from the later two-source projection and isolation attestation. |
| Research Execution Log | Added `REL-2026-0092/0093`, distinguishing raw-lock preflight from approved external handoff. |
| Experiment Master Record / Project Master Context | Latest status points to V5 release and precise Owner sending checklist, without claiming review completion. |
| Stage Process / Research Plan Authority | Updated D1 gate and scope boundaries; no semantic Guide amendment inferred. |
| Paper1 / Formal240 / Core144 READMEs | Latest navigation links the V5 handoff and explicitly labels earlier pending entries historical. |
| Accepted lessons | No new lesson promoted; raw immutability, blind isolation and evidence transparency remain operative. |
| Stage1–5 / Final72 | No files changed in those scopes. |
| Reviewer provenance | R3/R4 targeted-run isolation is `OWNER_ATTESTED`, not machine-proven. R4-codex remains the stable code for actual provider Doubao. |
| Distribution boundary | Owner sends only the seven reviewer-specific V5 files per the [exact checklist](PAPER1_FORMAL_D1_REMAINING90_PHASE2_OWNER_SEND_CHECKLIST_V5.md); private release manifest and projection audit stay out. |
| Downstream boundary | `EXTERNAL_PHASE2_RETURNS_PENDING / NO_HUMAN_AB / NO_D2_D3 / NO_GT / NO_SPLIT / NO_TRAINING`. |

Evidence: [targeted Phase1 lock/gate](PAPER1_FORMAL_D1_REMAINING90_TARGETED4_PHASE1_LOCK_AND_GATE_V1.md), [bounded source decision](PAPER1_FORMAL_D1_REMAINING90_PHASE2_EVIDENCE_PROJECTION_DECISION_V1.md), [V5 release QA](PAPER1_FORMAL_D1_REMAINING90_PHASE2_RELEASE_RECORD_V5.md). The private additive raw-lock namespace and V5 handoff namespace are read-only; source and locked-copy hashes remain equal. Independent V5 QA confirms 90 unique current IDs per reviewer, original reviewer-specific order, 86+4 Candidate parity, 45 E1-only/45 E1+E2 per packet, exact schema and four byte-identical Guide copies. Task-scoped Pytest: `19 passed` (one non-test-impacting cache-write warning); Ruff and MyPy pass. UTF-8, hidden-label-token scan, task Markdown links, Stage1–5 boundary and `git diff --check` pass. Git commit/push/remote parity are verified separately at task completion; the unrelated pre-existing design-spec modification remains excluded.
