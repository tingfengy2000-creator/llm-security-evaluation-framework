# Paper 1 Core144 domain-pipelined execution plan V1

This Owner-approved workflow supersedes the former all-domains-then-all-human sequence. Parallelism shortens elapsed time; it does not waive any evidence, construction, blind-review or human gate.

1. Finish D1 remaining90 machine pre-annotation QA: R3-gpt and R4-codex (provider Doubao) targeted four-row Phase1 rereview, then the same isolated sessions review one 90-row Phase2 package. Lock both raw returns, resolve blocking differences, run the D1 Full48 cross-batch audit and obtain `D1_PREANNOTATION_ACCEPTANCE=PASS`.
2. Only then build D1 Human A/B Phase1 Excel packages for different humans, with distinct opaque IDs/order, usable validation/instructions and private mappings. Prebuild Phase2 workbooks only as sealed/withheld. `D1_HUMAN_AB_PHASE1_DISTRIBUTION_READY` is a file-quality state, not proof of actual distribution or annotation.
3. At that readiness gate, D2 and D3 evidence-first construction/machine QA may begin as the dataset lane while D1 human annotation proceeds independently. Human returns may be locked and processed asynchronously. D2/D3 are **not started now**.
4. Each domain may separately enter human A/B only after its own machine pre-annotation acceptance. D1/D2/D3 domain GT may close independently; Core144 GT needs all three plus cross-domain consistency. No split or model-informed construction until Core144 GT and dataset freeze.

External review uses R3-gpt and reviewer code `R4-codex` with actual provider **Doubao**, session isolation `OWNER_ATTESTED`. R5-Claude remains auxiliary and non-gating. For a domain, prefer 144-row Phase1 and capacity-assessed Phase2; fall back to 96+48 only for actual transfer/context/serialization failure. Retain same reviewer session across Phase1/Phase2. Never use an external reviewer return as human GT.

Two lane states are tracked separately: Lane A `HUMAN_ANNOTATION`; Lane B `CORE_DATA_CONSTRUCTION`. At present both future lanes are waiting on D1's targeted machine-review gate. No Human A/B, D2/D3 construction, GT, split or training has begun by this plan.
