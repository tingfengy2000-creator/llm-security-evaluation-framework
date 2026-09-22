"""Reconstruct omitted V1.1 OOF evidence using the unchanged original runner.

This is an additive, one-time evidence reconstruction, not model selection.
The original Full OOF and nine machine-readable summaries are validation oracles.
"""
# mypy: disable-error-code=import-untyped

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import platform
from pathlib import Path
from typing import Any

import numpy as np
import sklearn

TOLERANCE = 1e-12  # frozen before inspecting reconstruction results
ORIGINAL_SCRIPT_SHA = "22d46d9ef11ed261f7f694ef960462b264b644781756363a8d53dbb04407be7a"
ORIGINAL_MANIFEST_SHA = "e788af67ee1a67d8635ddb11a9a27feeb3d7c89009a87bb3d1788ddfd90737af"
ORIGINAL_FULL_SHA = "eed87a32979cb2d1c85bbd67584cf5a3d2c9cd32789af933758530e65ba9d423"
ORIGINAL_RUN = "P1-FIRST-DOCUMENT-DETECTOR-V1_1-LOGO-PROTOTYPE-EXECUTION-01"
PREFIX = "PAPER1_FINAL72_DOCUMENT_DETECTOR_"


def check_equal(actual: Any, expected: Any, path: str) -> None:
    """Compare every summary leaf without relaxing machine precision."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict) or set(actual) != set(expected):
            raise ValueError(f"SUMMARY_STRUCTURE_MISMATCH:{path}")
        for key, value in expected.items():
            check_equal(actual[key], value, f"{path}.{key}")
    elif isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) != len(expected):
            raise ValueError(f"SUMMARY_LIST_MISMATCH:{path}")
        for index, value in enumerate(expected):
            check_equal(actual[index], value, f"{path}[{index}]")
    elif isinstance(expected, float):
        if not math.isclose(float(actual), expected, rel_tol=0, abs_tol=TOLERANCE):
            raise ValueError(f"SUMMARY_NUMERIC_MISMATCH:{path}")
    elif actual != expected:
        raise ValueError(f"SUMMARY_VALUE_MISMATCH:{path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--original-run", type=Path, required=True)
    parser.add_argument("--gt", type=Path, required=True)
    parser.add_argument("--feature-set", type=Path, required=True)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    runner_path = Path(__file__).with_name("run_document_detector_v1_1.py")
    spec = importlib.util.spec_from_file_location("frozen_detector_runner", runner_path)
    if spec is None or spec.loader is None:
        raise ValueError("ORIGINAL_RUNNER_IMPORT_FAIL")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    original = args.original_run
    if runner.sha(runner_path) != ORIGINAL_SCRIPT_SHA:
        raise ValueError("ORIGINAL_SCRIPT_SHA_MISMATCH")
    if runner.sha(original / "result_hash_manifest.json") != ORIGINAL_MANIFEST_SHA:
        raise ValueError("ORIGINAL_MANIFEST_SHA_MISMATCH")
    manifest = json.loads((original / "run_manifest_pre_fit.json").read_text(encoding="utf-8"))
    locked = json.loads((original / "result_hash_manifest.json").read_text(encoding="utf-8"))
    for name, expected in locked["files_sha256"].items():
        if runner.sha(original / name) != expected:
            raise ValueError(f"ORIGINAL_RESULT_CHANGED:{name}")
    if runner.sha(original / (PREFIX + "OOF_PREDICTIONS_V1_1.jsonl")) != ORIGINAL_FULL_SHA:
        raise ValueError("ORIGINAL_FULL_OOF_SHA_MISMATCH")
    paths = {key: getattr(args, key) for key in ("gt", "feature_set", "matrix", "candidates", "protocol")}
    if {key: runner.sha(paths[key]) for key in runner.HASHES} != manifest["frozen_input_sha256"]:
        raise ValueError("FROZEN_INPUT_IDENTITY_MISMATCH")
    if runner.sha(paths["protocol"]) != manifest["protocol_sha256"]:
        raise ValueError("FROZEN_PROTOCOL_IDENTITY_MISMATCH")
    if manifest["script_sha256"] != ORIGINAL_SCRIPT_SHA or manifest["model"] != "LogisticRegression(l2,C=1.0,liblinear,max_iter=2000,class_weight=balanced)":
        raise ValueError("ORIGINAL_CONFIG_IDENTITY_MISMATCH")
    if manifest["seed"] != runner.SEED or manifest["python_version"] != platform.python_version() or manifest["sklearn_version"] != sklearn.__version__:
        raise ValueError("ENVIRONMENT_IDENTITY_MISMATCH")
    rows, views, binary, continuous = runner.load_inputs(paths)
    folds = runner.fold_indices(rows)
    observed_folds = [
        {"fold_id": group, "train_groups": 23, "train_rows": 69, "validation_rows": 3, "validation_sample_ids": [rows[i]["sample_id"] for i in test]}
        for group, _, test in folds
    ]
    if observed_folds != manifest["folds"] or binary != manifest["binary_features"] or continuous != manifest["continuous_features"]:
        raise ValueError("FOLD_OR_PREPROCESSING_IDENTITY_MISMATCH")
    models = {model: [name for view in membership for name in views[view]] for model, membership in runner.model_names().items()}
    if {model: len(names) for model, names in models.items()} != manifest["model_feature_counts"]:
        raise ValueError("MODEL_FEATURE_IDENTITY_MISMATCH")
    if args.output.exists() and any(args.output.iterdir()):
        raise ValueError("OUTPUT_NAMESPACE_NOT_EMPTY")

    # Fit the control first. No other fit occurs unless original Full parity passes.
    y = np.asarray([row["target"] for row in rows], dtype=int)
    full = runner.fit_logo(rows, models["Full SEPT"], binary, continuous, folds, y)
    original_oof = runner.read_jsonl(original / (PREFIX + "OOF_PREDICTIONS_V1_1.jsonl"))
    if len(original_oof) != 72:
        raise ValueError("ORIGINAL_FULL_COUNT_MISMATCH")
    for index, old in enumerate(original_oof):
        row = rows[index]
        for key, value in (("sample_id", row["sample_id"]), ("group_id", row["group_id"]), ("fold_id", row["group_id"]), ("true_class", row["true_class"]), ("binary_target", row["target"]), ("predicted_class_at_0_5", int(full["probability"][index] >= 0.5))):
            if old[key] != value:
                raise ValueError(f"FULL_OOF_IDENTITY_MISMATCH:{index}:{key}")
        for key, value in (("decision_score", full["score"][index]), ("uncalibrated_probability", full["probability"][index])):
            if not math.isclose(old[key], float(value), rel_tol=0, abs_tol=TOLERANCE):
                raise ValueError(f"FULL_OOF_NUMERIC_MISMATCH:{index}:{key}")
    original_all = json.loads((original / (PREFIX + "METRICS_V1_1.json")).read_text(encoding="utf-8"))["all_models"]

    def summary(model: str, run: dict[str, Any]) -> dict[str, Any]:
        matched = runner.matched(rows, run["score"])
        return {"feature_count": len(models[model]), "metrics": runner.metrics(y, run["score"], run["probability"], rows), "matched": {key: value for key, value in matched.items() if key != "groups"}}

    check_equal(summary("Full SEPT", full), original_all["Full SEPT"], "Full SEPT")
    runs: dict[str, dict[str, Any]] = {"Full SEPT": full}
    for model, names in models.items():
        if model == "Full SEPT":
            continue
        run = runner.fit_logo(rows, names, binary, continuous, folds, y)
        check_equal(summary(model, run), original_all[model], model)
        runs[model] = run
    if len(runs) != 9 or any(len(run["score"]) != 72 or len(run["folds"]) != 24 for run in runs.values()):
        raise ValueError("RECONSTRUCTION_COMPLETENESS_FAIL")

    args.output.mkdir(parents=True, exist_ok=False)
    file_names = {"S-only": "S_ONLY", "E-only": "E_ONLY", "P-only": "P_ONLY", "T-only": "T_ONLY", "Full SEPT": "FULL_SEPT_CONTROL", "Full-S": "FULL_MINUS_S", "Full-E": "FULL_MINUS_E", "Full-P": "FULL_MINUS_P", "Full-T": "FULL_MINUS_T"}
    for model, run in runs.items():
        output_rows = [
            {"artifact_origin": "EVIDENCE_RECONSTRUCTION", "original_experiment": ORIGINAL_RUN, "model_id": model, "sample_id": row["sample_id"], "group_id": row["group_id"], "true_class": row["true_class"], "binary_target": row["target"], "fold_id": row["group_id"], "decision_score": float(run["score"][index]), "uncalibrated_probability": float(run["probability"][index]), "predicted_class_at_0_5": int(run["probability"][index] >= 0.5)}
            for index, row in enumerate(rows)
        ]
        runner.dump_jsonl(args.output / (file_names[model] + "_OOF_RECONSTRUCTED.jsonl"), output_rows)
    validation = {"status": "EVIDENCE_RECONSTRUCTION_ACCEPTED", "artifact_origin": "EVIDENCE_RECONSTRUCTION", "original_experiment": ORIGINAL_RUN, "original_run_manifest_sha256": runner.sha(original / "run_manifest_pre_fit.json"), "original_result_manifest_sha256": ORIGINAL_MANIFEST_SHA, "original_full_oof_sha256": ORIGINAL_FULL_SHA, "original_code_commit": manifest["code_commit"], "original_script_sha256": ORIGINAL_SCRIPT_SHA, "input_sha256": manifest["frozen_input_sha256"], "python_version": platform.python_version(), "sklearn_version": sklearn.__version__, "numpy_version_current_not_recorded_original": np.__version__, "fold_count": 24, "models": list(runs), "rows_per_model": 72, "full_control_numeric_tolerance_absolute": TOLERANCE, "summary_numeric_tolerance_absolute": TOLERANCE, "canonical_full_source": str(original / (PREFIX + "OOF_PREDICTIONS_V1_1.jsonl")), "no_bootstrap_or_permutation": True, "no_model_tuning": True}
    runner.dump(args.output / "PAPER1_DETECTOR_V1_1_RECONSTRUCTION_IDENTITY_VALIDATION_V1.json", validation)
    runner.dump(args.output / "result_hash_manifest.json", {"files_sha256": {p.name: runner.sha(p) for p in sorted(args.output.iterdir()) if p.is_file()}})
    print(json.dumps({"status": validation["status"], "output": str(args.output), "manifest_sha256": runner.sha(args.output / "result_hash_manifest.json")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
