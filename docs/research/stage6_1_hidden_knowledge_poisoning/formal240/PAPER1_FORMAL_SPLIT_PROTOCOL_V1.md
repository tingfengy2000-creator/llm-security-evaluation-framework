# Formal240 group-aware split protocol V1

Status: `ALGORITHM_AND_SEED_FROZEN / SPLIT_NOT_EXECUTED / NO_ASSIGNMENTS`.

Assign and lock stable group IDs before annotation; post-label re-keying, replacing a group to influence allocation, or choosing the seed after seeing outcomes is prohibited.

Frozen seed: **20260922** (decimal integer; chosen at protocol freeze, before formal candidate labels, predictions or test results). Algorithm version: `F240_STRATIFIED_CHAIN_SHUFFLE_V1`. Prerequisites: all 240 independent groups, all 720 candidates, A/B plus Owner adjudication and GT, and **derived** S locked; target design S is not an allocation key. If a domain×HKP×derived-S cell does not contain exactly four independent chains, fail closed and return to candidate/evidence repair; do not silently rebalance or substitute target S.

For each of the 5×4×3 final cells, sort stable unique group IDs; deterministically permute the four IDs using a per-cell SHA-256 stream keyed by `seed | domain | HKP | derived S | group ID` (ascending digest, with group ID tie-break). The first two are Train, third Dev, fourth Test. A group and all its C/P/H siblings and version-chain evidence identity stay together. The algorithm has no result-dependent choice and does not use candidate text, coefficients, predictions or Expected.

Expected cardinality *if prerequisites pass*: 120/60/60 groups and 360/180/180 candidate records. No assignments are produced in this task. When eventually run, hash/lock split manifest before model development; Test labels and sample-level GT remain `SEALED_FOR_MODEL_DEVELOPMENT`. Finish all Train/Dev feature, model, hyperparameter, threshold and calibration decisions before one separately approved untouched formal Test evaluation. Never change seed in response to a result.
