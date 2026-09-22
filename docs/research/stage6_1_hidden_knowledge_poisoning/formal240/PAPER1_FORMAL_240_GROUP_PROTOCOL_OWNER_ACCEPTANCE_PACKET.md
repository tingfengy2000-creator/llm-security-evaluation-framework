# Formal240 protocol Owner acceptance packet

Status: `READY_FOR_OWNER_PROTOCOL_REVIEW / WAVE_D1_NOT_APPROVED`. This packet records the Control Plane's frozen protocol, not a statement that the Owner has accepted produced data or authorized the first wave.

## Decisions and scope

Owner's 2026-09-22 task approves additive Formal annotation V4 and construction protocol/matrix freeze. Final72 development is closed as a construction phase but remains available as exposed engineering evidence; its GT and Pilot4 raw/Guide are unchanged. Proposed Formal target is 240 independent matched groups, 720 candidates **not generated**. V4 changes future version-claim semantics and adds ZERO external Evidence while leaving historical Pilot minimum values intact.

## Review map

- Annotation: [Guide V4](PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md), [machine schema](PAPER1_FORMAL_ANNOTATION_SCHEMA_V4.json), [22 teaching cases](PAPER1_FORMAL_ANNOTATION_BOUNDARY_EXAMPLES_V1.json), [consistency rules](PAPER1_FORMAL_ANNOTATION_CONSISTENCY_RULES_V1.json).
- Construction: [protocol](PAPER1_FORMAL_240_GROUP_BENCHMARK_CONSTRUCTION_PROTOCOL_V1.md), [240 unfilled slots](PAPER1_FORMAL_240_GROUP_MATRIX_V1.jsonl), [benchmark schema](PAPER1_FORMAL_BENCHMARK_SCHEMA_V1.json), [triplets](PAPER1_FORMAL_TRIPLET_CONTRACT_V1.md), [version](PAPER1_FORMAL_VERSION_METADATA_CONTRACT_V1.md), [provenance](PAPER1_FORMAL_PROVENANCE_METADATA_CONTRACT_V1.md), [corpus difficulty](PAPER1_FORMAL_EVIDENCE_CORPUS_DIFFICULTY_CONTRACT_V1.md), [query](PAPER1_FORMAL_QUERY_CONTRACT_V1.md).
- Gates: [observability](PAPER1_FORMAL_FEATURE_OBSERVABILITY_GATE_V1.md), [variance](PAPER1_FORMAL_FEATURE_VARIANCE_GATE_V1.md), [annotation process](PAPER1_FORMAL_ANNOTATION_EXECUTION_PLAN_V1.md), [split algorithm/seed](PAPER1_FORMAL_SPLIT_PROTOCOL_V1.md), [hypothesis traceability](PAPER1_FORMAL_HYPOTHESIS_TRACEABILITY_MATRIX_V1.md), [domain waves](PAPER1_FORMAL_WAVE_GATE_V1.md).

## Owner's exact next choice

[Task-scoped QA and documentation closeout](PAPER1_FORMAL240_FREEZE_QA_AND_CLOSEOUT_V1.md) record the schema/matrix hashes, historical non-mutation evidence, scoped tests and known pre-existing architecture debt.

Review this packet and **separately approve or return for repair** `P1-FORMAL240-WAVE-D1-CONSTRUCTION-01` (D1 enterprise HR: 48 groups/144 candidates), including actual trusted Evidence/corpus, metadata, evidence path and candidate construction under the gates. Until then: `WAITING_FOR_OWNER_WAVE_D1_APPROVAL`; no candidate text, annotation, split execution, detector training, formal result, or automatic next domain.

## Risk and claims boundary

The leading risks are V4 annotation ambiguity, HN-history shortcut, four-chain pseudo-replication, insufficient distractor difficulty, inaccessible provenance/Temporal inputs, leakage and license. The protocol defines fail-closed gates but has not yet demonstrated actual data quality. Formal H1–H5 remain hypotheses that can be falsified. The split protocol is only an algorithm/seed, not a manifest. The 240-slot matrix is design metadata, not a frozen formal dataset. Owner review of this packet is distinct from accepting a wave, GT or paper effect.
