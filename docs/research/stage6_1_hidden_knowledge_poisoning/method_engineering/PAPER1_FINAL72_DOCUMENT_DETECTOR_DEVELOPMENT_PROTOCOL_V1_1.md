# Paper 1 Final72 Document Detector Development Protocol V1.1

Status: `OWNER_APPROVED / PRE-FIT FROZEN / DEVELOPMENT ONLY` (2026-09-22).
Supersedes V1 **only for this versioned run**. V1 and its all-missing preflight blocker remain historical evidence.

## Inputs and boundary

- Accepted Final72 GT SHA256: `9e6224ef2cb2cb8e729f9ab569d09589c951e6df4ed3327c63c82913066d720a`.
- Feature Set V1.1 SHA256: `a3190b3b3fd6f3323229a83f9c919143fdba9efe06f209ef492242cdc1e37ee8`.
- Raw Matrix V1.1 SHA256: `2d418ae2fd6d22f848fcf812a6126fd68ff9b7b880c389a2ca510a5c94dd5b2d`.
- Final72 candidate corpus SHA256: `f530471ecd6551300d68c8ddf104cadce2305d8ff91e64010be222820628252d`.
- Exactly 72 rows, 21 frozen S/E/P/T features (3/9/6/3). No R, oracle-only Temporal features, or deferred Provenance relations. No feature selection after seeing labels.
- Final72 is development-exposed. Every metric is `DEVELOPMENT-SET OOF DIAGNOSTIC`, never an untouched test, formal benchmark or paper final result.

## Model and split

Binary target: Poison=1; Clean Current and Hard Negative=0. Exactly 24 complete matched triplets. Leave-One-Group-Out (LOGO), 24 folds of 69 train / 3 validation; group/sample/class/target are never model features. Each candidate receives one OOF prediction per model.

Nine prespecified models: S-only (3), E-only (9), P-only (6), T-only (3), Full SEPT (21), Full-S (18), Full-E (12), Full-P (15), Full-T (18). Each uses `LogisticRegression(penalty="l2", C=1.0, solver="liblinear", max_iter=2000, class_weight="balanced", random_state=20260922)`. No search, nonlinear model or baseline download.

Within every fold, continuous features use **train-only** median imputation then StandardScaler; binary features use **train-only** most-frequent imputation and no scaling. No constant invented for all-missing, no indicator, no global imputation/scaler. Missing/non-applicable is not interpreted as safe. The nine models share the same fold identities and configuration. The model probability is uncalibrated. The only classification threshold is the frozen 0.5 operational diagnostic.

## Metrics and controls

- Pooled OOF AUROC, average precision (AUPRC), precision/recall/F1/balanced accuracy/specificity/MCC at 0.5, and HN-FPR at 0.5.
- Recall@1%FPR = `NOT_RELIABLY_ESTIMABLE_ON_FINAL72`: 48 negatives make one FP 2.0833% FPR. Recall@5%FPR is only descriptive: examine **observed unique score cutoffs**, choose the greatest recall among those with at most `floor(0.05*48)=2` false positives; no interpolation or classifier threshold tuning follows from it.
- Matched metrics use decision score and strict `>`; exact ties are separate, never wins. Report Poison>HN, Poison>Clean, Poison highest in triplet, and P−HN/P−Clean margin mean/median/IQR.
- 2,000 group bootstrap resamples with replacement, fixed seed 20260922, for descriptive percentile 95% intervals on AUROC, AUPRC and three matched rates. This is development uncertainty, not population generalization inference.
- 200 within-triplet poison-identity permutations, fixed seed 20260922. Each group retains exactly one pseudo-positive; retrain the full 24-fold pipeline on each permutation. Report AUROC/AUPRC distribution and empirical p-like exceedance for diagnostic only, not formal significance.
- Save all 24 Full SEPT coefficient vectors. Sign stability is `max(positive_fold_fraction, negative_fold_fraction)`; coefficients are not causal importance.
- If AUROC≥0.95, AUPRC≥0.90, or Poison>HN≥0.90, trigger high-performance sanity audit. Check feature/ID/label leakage, missingness and source/domain shortcuts, group isolation, retrieved-corpus simplicity, version identity and near-duplicate features. Also check convergence, coefficient magnitude/variance, and p<.01 or p>.99.

## Run gate and claims

Before first fit, write a run manifest with exact input/protocol/code identities, Python/sklearn versions, seed and 24 fold IDs. Block on hash, shape, leakage, or legal preprocessing failure. Do not repair frozen inputs, change features, hyperparameters, split or threshold in response to results. Hash-lock every result. Preserve raw/previous artifacts. No calibration, Stage B, GMTP/PPL/MLM, XGBoost, 240-group or formal claim. Owner review is the next gate.
