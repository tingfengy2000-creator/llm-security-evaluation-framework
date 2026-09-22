# Formal240 H1–H5 traceability matrix V1

Source: [development-derived hypotheses](../method_engineering/PAPER1_FORMAL_SCALE_HYPOTHESES_V1.json). Status: `PREDECLARED_DESIGN_TRACE / NO_FORMAL_RESULTS`. Each hypothesis may be rejected; none is a benchmark label or candidate-construction target.

| Hypothesis | Benchmark factor | Required metadata | Signal requirement | Future evaluation | Falsification condition |
| --- | --- | --- | --- | --- | --- |
| H1 lexical/corpus shortcut | same-domain and lexically similar irrelevant official distractors; locked query variants | corpus membership, title/text/query hashes, official provenance | S under identical retriever settings | untouched group test S-only vs SEPT, query-variant deltas | S-only remains competitive or SEPT fails to improve under difficult distractors |
| H2 temporal/HN | legitimate historical HN and current/history near-duplicate | version family/ID, interval, current role, explicit successor, source refs | T applicability plus PTS and version binding | HN-FPR and matched P>HN by temporal applicability | T does not reduce HN errors or improves only via history-is-poison shortcut |
| H3 provenance | same-host/different issuer, repost, same authority/different claim | host, publisher, issuer, roles, document/version relation | P candidate-bound relations with actual variance | P-only/full-minus-P and availability on untouched groups | P remains constant/missing or yields no robust separation |
| H4 heterogeneous effects | balanced HKP1–4 × derived S1–S3 and independent chains | HKP and derived S in evaluator only, chain ID | S/E/P/T per-view availability | predeclared stratum matched metrics with uncertainty | no reliable pattern or reversed/mixed contributions |
| H5 hard negatives | official-supported, lexically/structurally close HN | HN fact evidence, version role, query, similarity audit | all views, especially T/P | HN-FPR and P>HN on untouched groups | valid HN are frequently scored above Poison |

Do not select easy Formal candidates from Final72 coefficient/AUROC/error groups. A failure taxonomy may flag missing coverage only. All future models and ablations retain per-sample scores/probabilities, group/split/fold/config/input SHA/environment under [output contract](../method_engineering/PAPER1_EXPERIMENT_OUTPUT_CONTRACT_V1.md).
