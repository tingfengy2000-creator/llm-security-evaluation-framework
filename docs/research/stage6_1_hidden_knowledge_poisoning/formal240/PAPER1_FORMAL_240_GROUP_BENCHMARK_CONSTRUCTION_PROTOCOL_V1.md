# Paper 1 Formal240 benchmark construction protocol V1

Status: `PROTOCOL_FROZEN / MATRIX_SLOTS_FROZEN / CANDIDATE_GENERATION_NOT_STARTED`. Owner task `P1-FORMAL240-ANNOTATION-SCHEMA-V4-AND-CONSTRUCTION-PROTOCOL-FREEZE-01`. This is **not** a formal run, Ground Truth freeze, detector claim, or approval for D1 execution.

## Population, grain and boundaries

Five domains (D1 enterprise HR, D2 finance, D3 information security, D4 procurement/R&D, D5 education/research) × HKP1 numeric/entity, HKP2 condition/exception, HKP3 temporal/version, HKP4 source/authority × target S1/S2/S3 × four independent chains = 60 design cells and 240 **unfilled group slots**. Each later group will have Clean Current, Poison and matched Hard Negative: 720 *target* records, zero generated now. HKP and target S are design metadata, never model inputs or GT. Formal derived S must be adjudicated from V4 minimum Evidence, not from target S.

## Construction order and gates

1. Freeze a unified trusted official corpus and source license/redistribution status. Build [difficult distractors](PAPER1_FORMAL_EVIDENCE_CORPUS_DIFFICULTY_CONTRACT_V1.md); do not supply only answer-bearing E1/E2 per candidate.
2. Bind independently supported [version metadata](PAPER1_FORMAL_VERSION_METADATA_CONTRACT_V1.md) and [provenance metadata](PAPER1_FORMAL_PROVENANCE_METADATA_CONTRACT_V1.md), including explicit unknowns. Chronology alone does not prove supersession; a website host is not a publisher or issuer.
3. Author an evidence path showing how current, historical, conditional, authority and substantive claims would be supported or refuted. Evidence first; do not write Poison and then search for confirming sources.
4. Run the [feature observability preflight](PAPER1_FORMAL_FEATURE_OBSERVABILITY_GATE_V1.md) *before* candidate generation; materially unobservable S/E/P/T inputs fail closed or require Owner-approved design repair.
5. Only after a separate D1 approval, write a self-contained, natural, matched C/P/H triplet under [triplet](PAPER1_FORMAL_TRIPLET_CONTRACT_V1.md) and [neutral-query](PAPER1_FORMAL_QUERY_CONTRACT_V1.md) contracts. A legal/policy subject must be uniquely identifiable inside each candidate.
6. Apply [Guide V4](PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md) using [independent A/B](PAPER1_FORMAL_ANNOTATION_EXECUTION_PLAN_V1.md). Validate target versus **derived** S; mismatches require repair/new candidate and new blind review, not label forcing.
7. Before any GT freeze, run [variance](PAPER1_FORMAL_FEATURE_VARIANCE_GATE_V1.md), corpus-difficulty, leakage, candidate-quality, provenance, query and wave gates. Never delete a feature because a development model coefficient or AUROC was inconvenient.

## Independence and leakage

The four chains within every domain×HKP×target-S cell must differ in primary subject, factual core and evidence/version family; paraphrases of one fact are not independent chains. All three siblings share one information need and one neutral query, with length/style/entity/date/authority surface traits audited for class shortcuts. No class, HKP, S, GT, expected answer, Owner decision, A/B field or artificial ID encoding enters trusted-corpus retrieval query, feature extraction or model inference. Keep Final72 coefficients/AUROC/error identities out of candidate construction; its failure taxonomy may only inform coverage checklists. Version-chain siblings cannot cross a future split.

## Forward and paper risk review

Main foreseeable risks: annotation V3.2 ambiguity, S target-label contamination, overly easy official corpus, all-missing or constant metadata features, legal-history false positives, class-specific phrasing, post-hoc split/model feedback and paper overclaim. The V4 separation, evidence-first path, difficult corpus, observability/variance gates, neutral query and sealed test are the predeclared mitigations. License and official-source provenance must be checked before a future wave; any unresolved external-source, answerability, chain-independence or scientific fairness issue is `HUMAN_DECISION_REQUIRED / Auto Continue=NO`. This protocol is designed to allow all [H1–H5](PAPER1_FORMAL_HYPOTHESIS_TRACEABILITY_MATRIX_V1.md) to be falsified. Final72 remains development-exposed and never an untouched test.

## Output and approval

Future runs must obey [output retention V1](../method_engineering/PAPER1_EXPERIMENT_OUTPUT_CONTRACT_V1.md): per-sample scores/probabilities for every model/view/ablation, fold/group/config/input SHA/environment and immutable manifest. [Split protocol](PAPER1_FORMAL_SPLIT_PROTOCOL_V1.md) is frozen but **not executed**. D1 candidate production, A/B annotation, GT, formal dataset freeze, split execution, detector fit and formal test each require separate authorized gates. This task ends at the [Owner acceptance packet](PAPER1_FORMAL_240_GROUP_PROTOCOL_OWNER_ACCEPTANCE_PACKET.md), not at automatic dataset acceptance.
