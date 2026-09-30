# Core144 D2 finance: internal construction checkpoint

Task: `P1-CORE144-D2-D3-FULL-DOMAIN-CONSTRUCTION-AND-PHASE1-MEGAWAVE-PREP-01`.
Scope: D2 only. This is construction-author/internal QA, **not** independent
blind review, Human Ground Truth, a formal split, or a detector result. D3 must
be built separately; this record does not imply that D3 passed.

## Frozen population and evidence lineage

The 48 unchanged D2 Core144 matrix slots contain 144 candidates: 48 each of
Clean Current, controlled Poison and evidence-backed Hard Negative. Each HKP
has 12 groups; each target S has 16; each HKP × S cell has four distinct
source-bound factual cores. The internal source corpus contains 25 captured
official documents across 13 factual families and 11 conservative family
clusters. Raw bytes, extracted text and SHA-256 are retained additively in the
Git-ignored `experiments/core144_d2_d3_20260929/d2/` namespace. Unknown
optional metadata stay unknown; in particular, a missing end date does not
prove an open-ended validity interval.

Evidence was locked before canonical facts and formal candidate release. The
48 neutral queries were each executed against the 25-document local corpus
with a deterministic, engineering-only character 2/3-gram BM25 Top-5 smoke
run. These traces do not evaluate retrieval quality and were not used to
select candidates. The 16 S3 cases have explicit E1-alone/E2-alone/joint
necessity records within the supplied, frozen official corpus; they do not
claim that no other official source could exist on the wider web. HKP3's 12
groups have source-bound temporal paths; HKP4's 12 groups have explicit
authority/provenance paths rather than host-as-issuer inference.

## Internal quality gate

The source-bound author review covers 48/48 groups. The explicit claim audit
records 330 factual atoms: 282 `SUPPORTED`, 48 designed
`CONTROLLED_POISON`, zero `UNSUPPORTED_ACCIDENTAL` and zero ambiguous atoms.
All 48 derived-S values match their target S. The bounded surface audit has
zero flagged triplet-parity cases and zero frequent role-exclusive 4-grams.
The 48-query retrieval smoke is deterministic. Primary required S/E/P/T/R
inputs have no missing cases, but 57 *optional* document-metadata fields are
not observed and are not silently treated as safe or zero. Candidate-visible
P/T applicability varies by role and must remain visible in downstream
shortcut analysis; the present check is an upstream readiness audit, not a
claim that every planned signal is computable or that a detector is fair.

Private `domain_release_v1/domain_acceptance_matrix.json` records all 15
listed internal gates as true. The immutable D2 candidate corpus SHA-256 is
`1435138d8227f4c09ae1c170a2c74dfddd7df89a1fe3d84312f7daa941926ad8`.
The evidence manifest SHA-256 is
`40291da3885f847bbf274fd499689ef5e6a5a69ca064ec2ec641eed3d070137d`.
Earlier source catalogs, failed prechecks, drafts and repairs remain in their
separate versions; V9 draft and V8 evidence contract feed this release.

## Reviewer boundary

The two candidate-only Phase1 packets each contain 144 opaque IDs and the
same text set in different cross-group orders, with no adjacent group members.
The exact seven answer keys and canonical enums are frozen in the accompanying
import schema. The packets contain only `blind_review_id` and
`candidate_text`; role, HKP, target/derived S, mapping, Expected and GT are
absent. `R4_CODEX` is a reviewer code; the actual provider is Doubao.

These are prepared files, **not yet sent**. R3/R4 raw returns and subsequent
Phase2 do not exist for D2. The combined D2/D3 external send gate remains
closed until D3 passes its own internal QA and four reviewer packets are
checked together. The Owner must not distribute the private construction
corpus, evidence manifest or acceptance records as Phase1 material.

## File index and scope

- Private domain acceptance: `experiments/core144_d2_d3_20260929/d2/domain_release_v1/domain_acceptance_matrix.json`.
- Private candidate corpus: `experiments/core144_d2_d3_20260929/d2/domain_release_v1/candidate_corpus_v1.jsonl`.
- Private R3/R4 candidate-only packets, prompts, common import schema and
  package hash manifest: `experiments/core144_d2_d3_20260929/d2/domain_release_v1/reviewer/`.
- Public construction and verification programs: `scripts/core144_*.py` and
  `tests/research/test_core144_domain_construction.py`.

Current D2 state: `D2_FULL144_INTERNAL_QA_ACCEPTED /
D2_PHASE1_PACKETS_PREPARED_NOT_DISTRIBUTED /
D3_CONSTRUCTION_PENDING /
CORE_GT_NOT_FROZEN /
SPLIT_NOT_EXECUTED /
TRAINING_NOT_STARTED`.
