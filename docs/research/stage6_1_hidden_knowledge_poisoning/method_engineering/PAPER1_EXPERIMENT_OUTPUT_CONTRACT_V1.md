# Paper 1 experiment output retention contract V1

Status: `FORMAL_SCALE_DESIGN_REQUIREMENT / NOT_YET_A_FORMAL_RUN`. This contract records the V1.1 evidence-granularity lesson; it does not authorize a new run or change a frozen result.

Every future single-view, ablation, baseline and formal model run must retain, for **each sample and model**: sample ID, held-out fold/group identity, model ID, raw decision score, uncalibrated or calibrated probability **with calibration state**, predicted class if a predeclared threshold exists, input artifact hashes, model/config/code/environment identity and a result manifest. Per-fold train/validation group membership and preprocessing fit scope must be auditable. Do not publish only aggregate AUROC/AUPRC/matched rates. Keep raw predictions immutable and make later analyses additive; never infer missing per-sample scores from summaries.

Acceptance gates: exact sample and fold parity; one OOF per sample where applicable; finite scores; all model/file hashes in an immutable index; original-versus-derived provenance explicitly separated; no label or oracle inputs in inference features; no test-set tuning. This applies to Formal 240-group design, but that benchmark, detector training and untouched-test evaluation still need separate Owner authorization.
