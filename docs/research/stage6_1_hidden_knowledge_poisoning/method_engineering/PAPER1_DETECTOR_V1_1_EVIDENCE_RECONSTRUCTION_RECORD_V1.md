# Detector V1.1 omitted-OOF evidence reconstruction (2026-09-22)

Status: `EXACT_EVIDENCE_RECONSTRUCTION_PASS / DEVELOPMENT_ONLY / NOT_AN_INDEPENDENT_REPLICATION`.
Owner authority: `A_FIRST_THEN_B_IF_NEEDED`; Option C not selected. Original prototype remains canonical.

## Step A: bounded original-artifact search

Read-only locations: original `paper1_final72_document_detector_v1_1_logo_20260922` namespace and its 10-file locked index; `scripts/research/run_document_detector_v1_1.py`; relevant worktree paths, `git ls-files` and `git log --all --name-only` for OOF/view/ablation artifacts. Filename patterns: `*OOF*`, `*oof*`, `*VIEW*`, `*ABLATION*`; the prior bounded handoff search recorded in blocker-01 was also considered. Found only the 72-row Full SEPT OOF. The eight comparison models had machine summaries but no attributable sample-level original OOF. `ORIGINAL_OOF_RECOVERY_INCOMPLETE=TRUE`; absence beyond the searched scope is not asserted.

## Step B: one-time exact evidence reconstruction

The unchanged original runner at commit `d9956c44f7e9eec03201a227416cc44d6c78d14c` has script SHA256 `22d46d9ef11ed261f7f694ef960462b264b644781756363a8d53dbb04407be7a`. Original result manifest SHA256 remains `e788af67ee1a67d8635ddb11a9a27feeb3d7c89009a87bb3d1788ddfd90737af`; original Full OOF SHA256 remains `eed87a32979cb2d1c85bbd67584cf5a3d2c9cd32789af933758530e65ba9d423`. Original pre-fit manifest supplied exact GT, 21-feature set, 72-row matrix, Candidate corpus, protocol, feature order, 24 validation group identities, fold-local preprocessing, `SEED=20260922`, Python `3.12.14`, sklearn `1.9.0` and fixed L2/liblinear LR configuration. Current NumPy is `2.5.0`; the historical pre-fit manifest did not record a NumPy version, so version identity cannot be asserted, but strict numerical parity passed.

Reconstruction ran the historical `fit_logo` path for exactly nine already-prescribed models, Full SEPT control first. The control's sample/fold/class identities and 72 decision scores/probabilities/predicted classes matched the canonical original (absolute tolerance fixed in code before execution: `1e-12`, relative tolerance `0`). The independently recomputed Full machine metrics and all eight other models' complete machine summary trees (metrics plus matched outcomes and margins) matched at the same precision. Each model has 72/72 OOF rows and 24 exact LOGO folds. No bootstrap, permutation, tuning, threshold search, calibration, new classifier or feature extraction occurred.

Additive private evidence namespace: `paper1_final72_detector_v1_1_evidence_reconstruction_20260922` under the Owner's handoff root; result manifest SHA256 `5924015e75d951223081925dc2ce7429cae23ea798cfbcef98aba5fe296f051b`. It contains nine explicitly `EVIDENCE_RECONSTRUCTION` OOF files and a machine identity-validation JSON. The reconstructed Full file is **control only**; subsequent analysis uses the **original canonical Full OOF** and validated reconstructed OOF for the eight views/ablations. All historical result hashes, including original bootstrap/permutation, remain unchanged.

This proves engineering reproducibility of the frozen development run within the numerical identity gate; it does not supply an independent replication, a formal model result, or population generalization evidence.
