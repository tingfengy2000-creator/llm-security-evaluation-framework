# Paper 1 Core144 benchmark contract V1

## Population and provenance

The active scope comprises only D1/D2/D3 from the frozen Formal240 matrix: 3 domains × 4 HKP × 3 target stealth levels × 4 independent chains = 144 group slots; one Clean Current, Poison and Hard Negative candidate per completed group gives 432 **planned** candidates. A slot is not a completed candidate. D4/D5 remain versioned historical design and possible future external extensions, never part of the core train/dev/test population without a separate Owner decision.

The 144-line view must preserve the original group-slot identity and order. Construction retains evidence-first ordering, official snapshot provenance, canonical fact atoms, one controlled Poison mechanism, true Clean/HN support, candidate independence, family clusters, neutral shared queries, S/E/P/T/R observability and two independent pre-annotation reviewers. R is query-conditioned Stage B, not a Stage A document feature. V4/V4.1/V4.2/V4.3 annotation boundaries remain in force; this scope decision does not change them.

## Future split and leakage gate

Each of 36 Domain×HKP×S cells has four independent chains. Only after D1, D2 and D3 human Ground Truth and cross-domain consistency are frozen, plus dataset and family-cluster audits pass, may the seed `20260922` assign 2/1/1 chains per cell to train/dev/test: 72/36/36 groups (216/108/108 candidates). Members of the same factual/version/source family cluster cannot cross a split. No D1-only split or detector training is authorized while later domains are built.

Current state: `CORE144_SCOPE_FROZEN / SPLIT_NOT_EXECUTED / GT_NOT_CREATED / TRAINING_NOT_STARTED`. The [parallel execution plan](PAPER1_CORE144_PARALLEL_EXECUTION_PLAN_V1.md) controls domain handoffs.
