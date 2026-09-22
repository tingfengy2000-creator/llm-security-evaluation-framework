# Formal240 A/B annotation execution plan V1

Status: `PLANNED_NOT_RELEASED`. This document does not distribute data or appoint annotators.

1. After a domain-wave Owner approval and candidate/evidence quality gates, make independent opaque-ID Phase1 packets with candidate and source title only. Hide candidate role, group, target S, HKP, E1/E2, Expected, mapping and the other human's return. A and B work independently without AI assistance or discussion.
2. Receive both Phase1 returns, byte-hash and index them, verify exact schema/ID parity and mandatory reasons, and **lock them before** releasing frozen official E1/E2 snapshots with URL provenance for Phase2. Releasing Phase2 early is a protocol blocker.
3. Obtain independent Phase2 returns using [Guide V4](PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md). Lock raw bytes before mapping/Expected unlock. Compare A/B, triage candidate defects and evidence issues. Owner adjudicates material disagreements without seeing Expected; keep adjudication raw immutable.
4. Apply explicit Owner-authorized consistency corrections as additive before/after/reason/evidence overlays. Re-run machine consistency and target-vs-derived S gates. Derive GT only from A/B consensus + Owner blind adjudication + approved overlays. Open Expected only after human GT closure for researcher QC; Expected never wins automatically.
5. A changed candidate text or Evidence Pool version must be treated as a new reviewed object with required blind rereview; do not silently splice old labels. Formal wave/GT/split gates each require separate Owner acceptance. No annotations have started in this task.

Phase1 schema remains canonical Pilot4 four judgment fields plus opaque ID; Phase2 retains seven accepted judgment fields plus opaque ID, with the V4 additional ZERO enum. A full standalone human manual/return package and each wave's actual identities/hashes must be reviewed before distribution.
