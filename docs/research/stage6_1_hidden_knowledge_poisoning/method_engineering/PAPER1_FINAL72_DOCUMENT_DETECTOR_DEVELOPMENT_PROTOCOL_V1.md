# Paper 1 Final72 Document Detector Development Protocol V1

Status: `FROZEN / PHASE_A_BLOCKED / PHASE_B_NOT_AUTHORIZED`

## Scientific role

This protocol covers a small-N engineering diagnostic on the development-exposed Final72 only: 24 matched groups, 72 candidates and 23 frozen non-Oracle S/E/P/T features. It cannot establish an untouched-test result, formal benchmark performance, generalization, superiority, calibration or production effectiveness.

## Target and group isolation

- `Poison=1`; `Clean Current=0`; `Hard Negative=0`.
- Validation is exactly 24-fold Leave-One-Group-Out (LOGO).
- Every held-out fold is one complete Clean/Poison/Hard-Negative triplet; 23 whole groups train and one whole group validates.
- `sample_id`, `group_id`, class and binary target are evaluation metadata only and never model inputs.
- Candidate-level random splitting is prohibited.

## Frozen model

- Logistic Regression only; L2; `C=1.0`; `solver=liblinear`; `max_iter=2000`; `class_weight=balanced`; `random_state=20260921`.
- No search/tuning, calibration or learned threshold. Threshold-dependent diagnostics use the fixed `0.5` threshold only.
- Output probability, if Phase B is later authorized, is an uncalibrated prototype probability.

## Fold-local preprocessing

- Continuous features: training-fold median imputation and training-fold StandardScaler.
- Binary features: training-fold mode imputation and no scaler.
- No missingness-indicator feature is added.
- `NOT_APPLICABLE`, `INPUT_MISSING` and `EVIDENCE_INSUFFICIENT` are not interpreted as safe.
- If a feature has no observed training value and the frozen contract has no neutral value, preprocessing fails closed; no 0/-1 constant may be invented and the feature may not be silently deleted.

## Metrics boundary

Pooled OOF AUROC/AUPRC/precision/recall/F1/balanced accuracy, fixed-threshold HN-FPR and matched win/tie/loss are development diagnostics only. Recall@1%FPR is not reliably estimable from 48 negatives. Recall@5%FPR is descriptive. Any bootstrap resamples matched groups; any permutation control preserves one permuted positive per triplet.

## Current blocking result

The label-blind policy lock found two frozen Provenance features with `72/72 INPUT_MISSING` and zero observed values: `host_publisher_relation` and `publisher_issuer_match`. Their contracts define neither a neutral value nor an authorized all-missing representation. Therefore Phase A does not pass and no fit, OOF prediction, ablation, bootstrap, coefficient analysis or permutation control was executed.

Blocker: `P1-FDD-PREFLIGHT-BLOCKER-01 / HUMAN_DECISION_REQUIRED / Auto Continue=NO`.
