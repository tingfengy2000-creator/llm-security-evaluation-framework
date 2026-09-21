"""Fail-closed preflight for the first Final72 document detector prototype.

This module intentionally separates the label-blind missingness-policy lock from
label/group loading.  Phase B is not allowed when a frozen feature has no
observed value and no contract-defined neutral value.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASK_ID = (
    "P1-FIRST-DOCUMENT-DETECTOR-PROTOTYPE-PREFLIGHT-AND-"
    "DEVELOPMENT-EXECUTION-01"
)
FEATURE_MATRIX_SHA256 = (
    "c1a8dfa250ab62843d9234754f27936667c2a760dbdae8be4f5405bb47dc30c0"
)
FEATURE_SET_SHA256 = (
    "585350c79d014997f649532549703aa57950e2cd35c724fbd9025442db01ce06"
)
FINAL72_GT_SHA256 = (
    "9e6224ef2cb2cb8e729f9ab569d09589c951e6df4ed3327c63c82913066d720a"
)
CANDIDATE_CORPUS_SHA256 = (
    "f530471ecd6551300d68c8ddf104cadce2305d8ff91e64010be222820628252d"
)
EXPECTED_FEATURE_COUNT = 23
EXPECTED_ROWS = 72
EXPECTED_GROUPS = 24

LR_CONFIG: dict[str, Any] = {
    "estimator": "LogisticRegression",
    "penalty": "l2",
    "C": 1.0,
    "solver": "liblinear",
    "max_iter": 2000,
    "class_weight": "balanced",
    "random_state": 20260921,
    "hyperparameter_search": False,
    "probability_semantics": "UNCALIBRATED_MODEL_PROBABILITY",
}

BINARY_FEATURES = {
    "claimed_authority_match",
    "condition_conflict",
    "date_conflict",
    "document_identity_match",
    "entity_conflict",
    "exception_conflict",
    "host_publisher_relation",
    "negation_flip",
    "numeric_conflict",
    "official_repost",
    "official_source",
    "predicate_match",
    "publisher_issuer_match",
    "relation_conflict",
    "subject_match",
    "version_identity_match",
}

FORBIDDEN_MATRIX_KEYS = {
    "target",
    "label",
    "candidate_class",
    "hkp",
    "stealth",
    "expected",
    "owner",
    "annotator",
    "sample_id",
    "group_id",
    "path",
    "file",
    "evidence_selection",
}

CLASS_ALIASES = {
    "CLEAN_CURRENT": "CLEAN_CURRENT",
    "POISON_CANDIDATE": "POISON",
    "MATCHED_HARD_NEGATIVE": "HARD_NEGATIVE",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def row_id(candidate_text: str) -> str:
    digest = hashlib.sha256(candidate_text.encode()).hexdigest()[:16]
    return f"FR-{digest}"


@dataclass(frozen=True)
class MissingnessDecision:
    feature_name: str
    feature_type: str
    missing_count: int
    observed_count: int
    raw_contract_policy: str
    fold_local_policy: str
    scaler_policy: str
    blocking: bool
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "feature_name": self.feature_name,
            "feature_type": self.feature_type,
            "missing_count": self.missing_count,
            "observed_count": self.observed_count,
            "raw_contract_policy": self.raw_contract_policy,
            "fold_local_policy": self.fold_local_policy,
            "scaler_policy": self.scaler_policy,
            "blocking": self.blocking,
            "reason": self.reason,
        }


def freeze_missingness_policy(
    feature_set: dict[str, Any], matrix: list[dict[str, Any]]
) -> list[MissingnessDecision]:
    contracts = {row["feature_name"]: row for row in feature_set["features"]}
    decisions: list[MissingnessDecision] = []
    for name in contracts:
        values = [row["features"][name] for row in matrix]
        observed = [value for value in values if value is not None]
        feature_type = "BINARY" if name in BINARY_FEATURES else "CONTINUOUS"
        contract = contracts[name]
        if not observed:
            decisions.append(
                MissingnessDecision(
                    feature_name=name,
                    feature_type=feature_type,
                    missing_count=len(values),
                    observed_count=0,
                    raw_contract_policy=contract["missing_value_policy"],
                    fold_local_policy="UNRESOLVED_ALL_MISSING_NO_NEUTRAL_VALUE",
                    scaler_policy=(
                        "NO_SCALER" if feature_type == "BINARY" else "TRAIN_FOLD_STANDARD_SCALER"
                    ),
                    blocking=True,
                    reason=(
                        "No observed value exists in Final72, so a training-fold mode/median "
                        "does not exist. The frozen contract defines no neutral value."
                    ),
                )
            )
            continue
        decisions.append(
            MissingnessDecision(
                feature_name=name,
                feature_type=feature_type,
                missing_count=len(values) - len(observed),
                observed_count=len(observed),
                raw_contract_policy=contract["missing_value_policy"],
                fold_local_policy=(
                    "TRAIN_FOLD_MODE"
                    if feature_type == "BINARY"
                    else "TRAIN_FOLD_MEDIAN"
                ),
                scaler_policy=(
                    "NO_SCALER"
                    if feature_type == "BINARY"
                    else "TRAIN_FOLD_STANDARD_SCALER"
                ),
                blocking=False,
                reason="Statistic is fitted on the training fold and applied to held-out group.",
            )
        )
    return decisions


def validate_feature_inputs(
    feature_set: dict[str, Any], matrix: list[dict[str, Any]]
) -> dict[str, Any]:
    names = [row["feature_name"] for row in feature_set["features"]]
    excluded = set(feature_set["excluded_oracle_features"])
    matrix_keys = {key.lower() for row in matrix for key in row}
    feature_keys = {
        key.lower() for row in matrix for key in row.get("features", {}).keys()
    }
    row_ids = [row.get("feature_row_id") for row in matrix]
    checks = {
        "feature_count_exact": len(names) == EXPECTED_FEATURE_COUNT,
        "feature_names_unique": len(names) == len(set(names)),
        "matrix_rows_exact": len(matrix) == EXPECTED_ROWS,
        "matrix_row_ids_unique": len(row_ids) == len(set(row_ids)),
        "matrix_feature_keys_exact": all(
            set(row.get("features", {})) == set(names) for row in matrix
        ),
        "retrieval_behavior_excluded": not feature_set["retrieval_behavior_included"],
        "oracle_features_excluded": not (excluded & set(names)),
        "forbidden_top_level_keys_zero": not (matrix_keys & FORBIDDEN_MATRIX_KEYS),
        "forbidden_feature_keys_zero": not (feature_keys & FORBIDDEN_MATRIX_KEYS),
        "selection_used_performance_false": not feature_set["selection_used_performance"],
    }
    return {"checks": checks, "pass": all(checks.values())}


def validate_groups(
    candidates: list[dict[str, Any]], matrix: list[dict[str, Any]]
) -> dict[str, Any]:
    by_row = {row_id(row["phase1_view"]["candidate_text"]): row for row in candidates}
    matrix_ids = {row["feature_row_id"] for row in matrix}
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in candidates:
        groups[row["triplet_id"]].append(row)
    expected_classes = {"CLEAN_CURRENT", "POISON", "HARD_NEGATIVE"}
    normalized_groups = {
        group: [CLASS_ALIASES.get(row["owner_only"]["candidate_kind"], "UNKNOWN") for row in rows]
        for group, rows in groups.items()
    }
    holdout_counts: Counter[str] = Counter()
    no_group_crossing = True
    fold_plan = []
    all_groups = sorted(groups)
    for fold_index, held_out in enumerate(all_groups, start=1):
        validation = groups[held_out]
        train_groups = [group for group in all_groups if group != held_out]
        no_group_crossing = no_group_crossing and held_out not in train_groups
        for row in validation:
            holdout_counts[row["sample_id"]] += 1
        fold_plan.append(
            {
                "fold_id": f"LOGO-{fold_index:02d}",
                "held_out_group": held_out,
                "train_group_count": len(train_groups),
                "train_candidate_count": sum(len(groups[group]) for group in train_groups),
                "validation_candidate_count": len(validation),
                "validation_classes": sorted(normalized_groups[held_out]),
            }
        )
    checks = {
        "candidate_rows_exact": len(candidates) == EXPECTED_ROWS,
        "feature_row_mapping_exact": set(by_row) == matrix_ids,
        "matched_group_count_exact": len(groups) == EXPECTED_GROUPS,
        "each_group_has_three_candidates": all(len(rows) == 3 for rows in groups.values()),
        "each_group_has_clean_poison_hn": all(
            set(values) == expected_classes for values in normalized_groups.values()
        ),
        "logo_fold_count_exact": len(fold_plan) == EXPECTED_GROUPS,
        "each_candidate_held_out_once": len(holdout_counts) == EXPECTED_ROWS
        and set(holdout_counts.values()) == {1},
        "no_group_crosses_train_validation": no_group_crossing,
    }
    return {
        "checks": checks,
        "pass": all(checks.values()),
        "class_counts": dict(
            Counter(
                CLASS_ALIASES.get(row["owner_only"]["candidate_kind"], "UNKNOWN")
                for row in candidates
            )
        ),
        "fold_plan": fold_plan,
    }


def protocol_markdown() -> str:
    return f"""# Paper 1 Final72 Document Detector Development Protocol V1

Status: `FROZEN_PENDING_BLOCKING_PREFLIGHT`

## Scientific role

This is a `SMALL-N DEVELOPMENT EXPERIMENT`: 24 independent matched groups, 72 candidates and 23 frozen non-Oracle S/E/P/T features. It cannot be presented as an untouched-test, formal benchmark, generalization or paper-final result.

## Split and target

- Target: Poison=1; Clean Current and Hard Negative=0.
- Split: exactly 24 Leave-One-Group-Out folds. Each held-out fold contains one complete Clean/Poison/HN triplet.
- Group/sample identifiers and labels are evaluation-only and never model features.

## Frozen estimator

`{json.dumps(LR_CONFIG, ensure_ascii=False, sort_keys=True)}`

No grid/random/Bayesian search, manual C tuning, threshold optimization or calibration is allowed. Probability means uncalibrated prototype model output.

## Fold-local preprocessing

- Continuous: training-fold median imputation followed by training-fold StandardScaler.
- Binary: training-fold mode imputation, no scaling.
- No missingness indicator is added.
- A feature with no observed training value and no contract-defined neutral value is a blocking preflight failure; no constant is invented.

## Evaluation boundary

Pooled OOF metrics are development diagnostics. Recall@1%FPR is not reliably estimable with 48 negatives. Recall@5%FPR is descriptive. HN-FPR uses the fixed 0.5 threshold. Matched comparisons report win/tie/loss and within-group margins. Any eventual bootstrap must resample matched groups, and the negative control must preserve one permuted positive per triplet.

## Phase gate

Phase B may begin only when every Phase A blocking gate passes. A missingness-policy conflict, identity mismatch, group leakage or forbidden feature causes fail-closed stop before fitting.
"""


def blocker_markdown(blocking_features: list[dict[str, Any]]) -> str:
    names = ", ".join(f"`{row['feature_name']}`" for row in blocking_features)
    return f"""# P1-FDD-PREFLIGHT-BLOCKER-01

1. **Issue ID**: `P1-FDD-PREFLIGHT-BLOCKER-01`
2. **Issue name**: Frozen all-missing features have no authorized model representation.
3. **Discovery task**: `{TASK_ID}` / Phase A preflight.
4. **Facts**: `OBSERVED_FACT`: {names} are null in 72/72 raw rows and their availability is `INPUT_MISSING`; the frozen contracts define `LEAVE_NULL` and no neutral value. `SOURCE_DERIVED_FACT`: Logistic Regression requires numeric finite inputs. `INFERENCE`: silent constant fill, feature deletion or missingness indicators would change the frozen feature/missingness semantics. `UNKNOWN`: which repair the Owner prefers.
5. **Affected constraints**: exact 23-feature use, no feature selection, fold-local mode/median only, no missingness shortcut, no frozen-contract change.
6. **Why now**: Phase B would otherwise encode an unauthorized value or train fewer than 23 frozen features.
7. **Downstream risks**: invalid reproducibility, coefficient/intercept distortion, label-proxy claims, unfair ablation and paper-review challenge.
8. **Options**: A) repair upstream evidence/registry and regenerate a versioned Feature Matrix V2; highest rigor, higher cost, reversible/additive. B) Owner-authorize a constant non-informative representation for globally all-missing columns; cheap and reversible but changes missingness semantics and requires explicit coefficient/invariance checks. C) Owner-authorize exclusion and freeze Feature Set V1.1 with 21 inputs; transparent but changes the 23-feature contract and view budget.
9. **LOCAL recommendation**: Option A for formal-route integrity; Option B only for a clearly labeled engineering diagnostic if speed is prioritized.
10. **Rationale/confidence**: high confidence; the absence is exact and the contract supplies no fold statistic or neutral value.
11. **Owner decision required**: choose A, B or C and explicitly authorize the resulting versioned contract.
12. **Before decision**: allowed—read-only verification, blocker evidence, governance/docs and Git synchronization. Prohibited—any Detector fit, OOF metric, ablation, bootstrap, permutation run, threshold/calibration, Risk or Stage-B model.
"""


def build_manifest(output: Path) -> dict[str, Any]:
    files = []
    for path in sorted(output.rglob("*")):
        if path.is_file() and path.name != "final_manifest.json":
            files.append(
                {
                    "path": path.relative_to(output).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    return {"task_id": TASK_ID, "created_at": utc_now(), "files": files}


def prepare(args: argparse.Namespace) -> None:
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing evidence: {output}")
    output.mkdir(parents=True)

    identities = {
        "feature_matrix": sha256(args.feature_matrix),
        "feature_set": sha256(args.feature_set),
        "final72_gt": sha256(args.final72_gt),
        "candidate_corpus": sha256(args.candidates),
    }
    expected = {
        "feature_matrix": FEATURE_MATRIX_SHA256,
        "feature_set": FEATURE_SET_SHA256,
        "final72_gt": FINAL72_GT_SHA256,
        "candidate_corpus": CANDIDATE_CORPUS_SHA256,
    }
    identity_checks = {key: identities[key] == expected[key] for key in expected}

    # This is the label-blind policy lock. No candidate class/group/GT value has
    # been loaded at this point.
    feature_set = read_json(args.feature_set)
    matrix = read_jsonl(args.feature_matrix)
    feature_validation = validate_feature_inputs(feature_set, matrix)
    decisions = freeze_missingness_policy(feature_set, matrix)
    policy_locked_at = utc_now()
    policy = {
        "task_id": TASK_ID,
        "locked_at": policy_locked_at,
        "labels_loaded": False,
        "no_missingness_indicators": True,
        "decisions": [decision.as_dict() for decision in decisions],
    }
    write_json(
        output / "policy/PAPER1_DOCUMENT_DETECTOR_MISSINGNESS_POLICY_V1.json",
        policy,
    )
    write_text(
        output
        / "protocol/PAPER1_FINAL72_DOCUMENT_DETECTOR_DEVELOPMENT_PROTOCOL_V1.md",
        protocol_markdown(),
    )

    candidates = read_jsonl(args.candidates)
    gt = read_json(args.final72_gt)
    labels_loaded_at = utc_now()
    group_validation = validate_groups(candidates, matrix)
    gt_checks = {
        "gt_record_count_exact": gt.get("record_count") == EXPECTED_ROWS,
        "gt_role_development_only": gt.get("role")
        == "DEVELOPMENT_AND_METHOD_ENGINEERING_SET",
        "gt_not_untouched_test": gt.get("untouched_final_test_set") is False,
    }
    blocking_features = [decision.as_dict() for decision in decisions if decision.blocking]
    gates = {
        "input_identities_exact": all(identity_checks.values()),
        "feature_input_validation": feature_validation["pass"],
        "gt_validation": all(gt_checks.values()),
        "group_logo_validation": group_validation["pass"],
        "missingness_policy_resolved": not blocking_features,
        "retrieval_behavior_excluded": feature_validation["checks"][
            "retrieval_behavior_excluded"
        ],
        "oracle_features_excluded": feature_validation["checks"][
            "oracle_features_excluded"
        ],
        "blocking_leakage_zero": feature_validation["pass"],
        "fixed_lr_configuration": LR_CONFIG["hyperparameter_search"] is False,
        "no_calibration": True,
        "no_threshold_tuning": True,
    }
    pass_all = all(gates.values())
    preflight = {
        "task_id": TASK_ID,
        "phase": "PHASE_A",
        "created_at": utc_now(),
        "policy_locked_at": policy_locked_at,
        "labels_loaded_at": labels_loaded_at,
        "policy_locked_before_labels": policy_locked_at <= labels_loaded_at,
        "identities": identities,
        "identity_checks": identity_checks,
        "feature_validation": feature_validation,
        "gt_checks": gt_checks,
        "group_validation": group_validation,
        "lr_config": LR_CONFIG,
        "blocking_features": blocking_features,
        "blocking_gates": gates,
        "blocking_gates_pass": pass_all,
        "phase_b_authorized": pass_all,
        "training_started": False,
        "status": (
            "PHASE_A_PASS_PHASE_B_AUTHORIZED"
            if pass_all
            else "PHASE_A_BLOCKED_PHASE_B_NOT_AUTHORIZED"
        ),
    }
    write_json(
        output / "preflight/PAPER1_FIRST_DOCUMENT_DETECTOR_PREFLIGHT_V1.json",
        preflight,
    )
    if blocking_features:
        write_text(
            output / "blocker/PAPER1_FIRST_DOCUMENT_DETECTOR_MISSINGNESS_BLOCKER_01.md",
            blocker_markdown(blocking_features),
        )
        write_json(
            output / "blocker/PAPER1_FIRST_DOCUMENT_DETECTOR_MISSINGNESS_BLOCKER_01.json",
            {
                "issue_id": "P1-FDD-PREFLIGHT-BLOCKER-01",
                "status": "HUMAN_DECISION_REQUIRED",
                "auto_continue": False,
                "blocking_features": blocking_features,
                "phase_b_started": False,
            },
        )
    write_json(output / "manifest/final_manifest.json", build_manifest(output))
    print(json.dumps({"status": preflight["status"], "blocking_features": [row["feature_name"] for row in blocking_features]}, ensure_ascii=False))


def execute(args: argparse.Namespace) -> None:
    preflight_path = (
        args.output.resolve()
        / "preflight/PAPER1_FIRST_DOCUMENT_DETECTOR_PREFLIGHT_V1.json"
    )
    preflight = read_json(preflight_path)
    if not preflight.get("blocking_gates_pass"):
        names = [row["feature_name"] for row in preflight["blocking_features"]]
        raise RuntimeError(
            "PHASE_B_BLOCKED_BY_PREFLIGHT: unresolved missingness for "
            + ", ".join(names)
        )
    raise RuntimeError(
        "PHASE_B_IMPLEMENTATION_NOT_REACHED_IN_THIS_FAIL_CLOSED_RUN; "
        "a superseding Owner-authorized missingness contract is required"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    prepare_parser = sub.add_parser("prepare")
    prepare_parser.set_defaults(handler=prepare)
    prepare_parser.add_argument("--output", type=Path, required=True)
    prepare_parser.add_argument("--feature-matrix", type=Path, required=True)
    prepare_parser.add_argument("--feature-set", type=Path, required=True)
    prepare_parser.add_argument("--final72-gt", type=Path, required=True)
    prepare_parser.add_argument("--candidates", type=Path, required=True)
    execute_parser = sub.add_parser("execute")
    execute_parser.set_defaults(handler=execute)
    execute_parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
