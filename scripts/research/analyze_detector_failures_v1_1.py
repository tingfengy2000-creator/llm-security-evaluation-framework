"""Post-lock, read-only Final72 detector failure diagnostics.

Consumes canonical Full OOF and validated reconstructed comparison OOF. Never fits.
"""
# mypy: disable-error-code=import-untyped

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from scipy.stats import spearmanr

PREFIX = "PAPER1_FINAL72_DOCUMENT_DETECTOR_"
HARD_GROUPS = {"EDU-06", "FIN-03", "FIN-04", "HR-03", "INF-01", "INF-04", "INF-05"}
TOL = 1e-12


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in ("original_run", "reconstruction", "feature_set", "matrix", "gt", "candidates", "trace", "pts", "output"):
        parser.add_argument("--" + name.replace("_", "-"), type=Path, required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("frozen_detector_runner", Path(__file__).with_name("run_document_detector_v1_1.py"))
    if spec is None or spec.loader is None:
        raise ValueError("ORIGINAL_RUNNER_IMPORT_FAIL")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    validation = json.loads((args.reconstruction / "PAPER1_DETECTOR_V1_1_RECONSTRUCTION_IDENTITY_VALIDATION_V1.json").read_text(encoding="utf-8"))
    if validation["status"] != "EVIDENCE_RECONSTRUCTION_ACCEPTED":
        raise ValueError("RECONSTRUCTION_NOT_ACCEPTED")
    manifest = json.loads((args.reconstruction / "result_hash_manifest.json").read_text(encoding="utf-8"))["files_sha256"]
    for name, expected in manifest.items():
        if runner.sha(args.reconstruction / name) != expected:
            raise ValueError(f"RECONSTRUCTION_HASH_FAIL:{name}")
    paths = {key: getattr(args, key) for key in ("gt", "feature_set", "matrix", "candidates")}
    rows, views, _, _ = runner.load_inputs(paths)
    feature_set = json.loads(args.feature_set.read_text(encoding="utf-8"))
    metadata = {item["feature_name"]: item for item in feature_set["features"]}
    candidates = {item["sample_id"]: item for item in runner.read_jsonl(args.candidates)}
    full_rows = runner.read_jsonl(args.original_run / (PREFIX + "OOF_PREDICTIONS_V1_1.jsonl"))
    by_model: dict[str, list[dict[str, Any]]] = {"Full SEPT": full_rows}
    files = {"S-only": "S_ONLY", "E-only": "E_ONLY", "P-only": "P_ONLY", "T-only": "T_ONLY", "Full-S": "FULL_MINUS_S", "Full-E": "FULL_MINUS_E", "Full-P": "FULL_MINUS_P", "Full-T": "FULL_MINUS_T"}
    for model, name in files.items():
        by_model[model] = runner.read_jsonl(args.reconstruction / (name + "_OOF_RECONSTRUCTED.jsonl"))
    ids = [row["sample_id"] for row in rows]
    for model, predictions in by_model.items():
        if len(predictions) != 72 or [row["sample_id"] for row in predictions] != ids:
            raise ValueError(f"OOF_ID_ORDER_FAIL:{model}")
    scores = {model: {row["sample_id"]: float(row["decision_score"]) for row in predictions} for model, predictions in by_model.items()}
    group_members: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        group_members[row["group_id"]][row["true_class"]] = row
    kind_to_short = {"POISON_CANDIDATE": "P", "CLEAN_CURRENT": "C", "MATCHED_HARD_NEGATIVE": "HN"}
    group_metadata = {}
    for group, members in group_members.items():
        p = members["POISON_CANDIDATE"]
        owner = candidates[p["sample_id"]]["owner_only"]
        group_metadata[group] = {"domain": owner["domain"], "hkp": owner["coverage_cell"].split("|")[0].split("_")[1], "stealth": owner["intended_stealth"]}

    def margin(group: str, model: str, comparator: str) -> float:
        members = group_members[group]
        return scores[model][members["POISON_CANDIDATE"]["sample_id"]] - scores[model][members[comparator]["sample_id"]]

    inventory = []
    directions = []
    for name, info in metadata.items():
        values = [row["features"][name] for row in rows]
        observed = [float(value) for value in values if value is not None]
        unique = sorted(set(observed))
        is_constant = len(unique) <= 1
        inventory.append({"feature_name": name, "view": info["view"], "type": "binary" if all(isinstance(value, bool) for value in values if value is not None) else "continuous", "orientation": info["orientation"], "observed_count": len(observed), "missing_count": 72 - len(observed), "not_applicable_count": "NOT_DERIVABLE_FROM_RAW_NUMERIC_MATRIX", "unique_values": unique if len(unique) <= 12 else {"count": len(unique), "min": min(unique), "max": max(unique)}, "variance_observed": statistics.pvariance(observed), "constant": is_constant, "near_constant_predeclared_rule": len(unique) == 2 and min(Counter(observed).values()) <= 3, "constant_cause_diagnostic": ("EXTRACTOR_LIMITATION_OR_BENCHMARK_COVERAGE" if info["view"] in {"ENTITY_CLAIM", "TEMPORAL_VERSION"} else "CORPUS_HOMOGENEITY_OR_SIGNAL_COARSENESS") if is_constant else None, "risk_semantics": info["orientation"]})
        counts: dict[str, Counter[str]] = {key: Counter() for key in ("P_HN", "P_C", "HN_C")}
        for members in group_members.values():
            for comparison, left, right in (("P_HN", "POISON_CANDIDATE", "MATCHED_HARD_NEGATIVE"), ("P_C", "POISON_CANDIDATE", "CLEAN_CURRENT"), ("HN_C", "MATCHED_HARD_NEGATIVE", "CLEAN_CURRENT")):
                a = members[left]["features"][name]
                b = members[right]["features"][name]
                if a is None or b is None:
                    outcome = "INPUT_MISSING_OR_NOT_APPLICABLE_UNSEPARATED"
                elif info["orientation"] == "NON_MONOTONIC":
                    outcome = "NON_MONOTONIC_NOT_SCORED"
                else:
                    delta = (float(a) - float(b)) * (1 if info["orientation"] == "HIGHER_IS_RISKIER" else -1)
                    outcome = "RISK_LEFT_HIGHER" if delta > TOL else "RISK_LEFT_LOWER" if delta < -TOL else "TIE"
                counts[comparison][outcome] += 1
        directions.append({"feature_name": name, "view": info["view"], "orientation": info["orientation"], "comparisons": {key: dict(value) for key, value in counts.items()}})

    exact_dupes = []
    numeric_names = list(metadata)
    for i, left in enumerate(numeric_names):
        for right in numeric_names[i + 1:]:
            if all(row["features"][left] == row["features"][right] for row in rows):
                exact_dupes.append([left, right])
    varying = [entry["feature_name"] for entry in inventory if not entry["constant"]]
    unique_vectors = {tuple(row["features"][name] for row in rows) for name in varying}
    high_corr = []
    for i, left in enumerate(varying):
        for right in varying[i + 1:]:
            pairs = [(float(row["features"][left]), float(row["features"][right])) for row in rows if row["features"][left] is not None and row["features"][right] is not None]
            if len(pairs) < 10 or len({a for a, _ in pairs}) < 2 or len({b for _, b in pairs}) < 2:
                continue
            corr = float(spearmanr([a for a, _ in pairs], [b for _, b in pairs]).statistic)
            if math.isfinite(corr) and abs(corr) >= 0.9:
                high_corr.append({"left": left, "right": right, "spearman": corr, "joint_observed": len(pairs)})

    shifts: dict[str, list[dict[str, Any]]] = {"T": [], "P": []}
    for view, minus in (("T", "Full-T"), ("P", "Full-P")):
        for group, members in sorted(group_members.items()):
            deltas = {kind_to_short[kind]: scores["Full SEPT"][row["sample_id"]] - scores[minus][row["sample_id"]] for kind, row in members.items()}
            ph = margin(group, "Full SEPT", "MATCHED_HARD_NEGATIVE") - margin(group, minus, "MATCHED_HARD_NEGATIVE")
            pc = margin(group, "Full SEPT", "CLEAN_CURRENT") - margin(group, minus, "CLEAN_CURRENT")
            classification = "HELPED" if ph > TOL else "HURT" if ph < -TOL else "NEUTRAL"
            shifts[view].append({"group_id": group, "class_score_shift_full_minus_ablated": deltas, "p_hn_margin_shift": ph, "p_clean_margin_shift": pc, "p_hn_diagnostic": classification, "full_p_hn_margin": margin(group, "Full SEPT", "MATCHED_HARD_NEGATIVE"), "ablated_p_hn_margin": margin(group, minus, "MATCHED_HARD_NEGATIVE"), "not_causal_effect": True})

    pts = {row["candidate_id"]: row for row in runner.read_jsonl(args.pts)}
    pts_counts = dict(Counter(row["status"] for row in pts.values()))
    temporal = {"available_temporal_features": views["T"], "excluded_oracle_temporal_features": feature_set["excluded_oracle_features"], "pts_v3_status_counts": pts_counts, "temporal_applicable_count": 72 - pts_counts.get("NOT_APPLICABLE", 0), "pts_computed_temporal_applicable": pts_counts.get("COMPUTED", 0), "direction_diagnostic": [item for item in directions if item["view"] == "TEMPORAL_VERSION"], "t_only_p_gt_hn": sum(margin(group, "T-only", "MATCHED_HARD_NEGATIVE") > 0 for group in group_members), "t_only_hn_gt_p": sum(margin(group, "T-only", "MATCHED_HARD_NEGATIVE") < 0 for group in group_members), "full_vs_full_t": dict(Counter(row["p_hn_diagnostic"] for row in shifts["T"])), "status": "PARTIALLY_SUPPORTED_OR_NOT_SUPPORTED_BY_FEATURE_DIRECTION_PENDING_INTERPRETATION"}
    provenance = {"available_provenance_features": views["P"], "deferred_relation_features": feature_set["deferred_features"], "direction_diagnostic": [item for item in directions if item["view"] == "PROVENANCE"], "constant_features": [item["feature_name"] for item in inventory if item["view"] == "PROVENANCE" and item["constant"]], "p_only_p_gt_hn": sum(margin(group, "P-only", "MATCHED_HARD_NEGATIVE") > 0 for group in group_members), "full_vs_full_p": dict(Counter(row["p_hn_diagnostic"] for row in shifts["P"])), "official_trusted_corpus_homogeneous_by_design": True}

    trace: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in runner.read_jsonl(args.trace):
        if item["rank"] <= 5:
            trace[item["candidate_id"]].append({"rank": item["rank"], "evidence_doc_id": item["evidence_doc_id"], "score": item["score"]})
    hard_ids = HARD_GROUPS | {group for group in group_members if margin(group, "Full SEPT", "MATCHED_HARD_NEGATIVE") <= 0 or margin(group, "Full SEPT", "CLEAN_CURRENT") <= 0}
    hard = []
    taxonomy = []
    for group in sorted(group_members):
        members = group_members[group]
        tags = []
        if margin(group, "Full SEPT", "MATCHED_HARD_NEGATIVE") <= 0:
            tags.append("F2_HISTORICALNESS_CONFUSION_CANDIDATE")
        if any(item["group_id"] == group and item["p_hn_diagnostic"] == "HURT" for item in shifts["T"]):
            tags.append("F3_CURRENT_VERSION_BINDING_MISSING_CANDIDATE")
        if any(item["group_id"] == group and item["p_hn_diagnostic"] == "HURT" for item in shifts["P"]):
            tags.append("F4_PROVENANCE_HOMOGENEITY_CANDIDATE")
        if margin(group, "S-only", "MATCHED_HARD_NEGATIVE") <= 0:
            tags.append("F1_SEMANTIC_INSUFFICIENCY_CANDIDATE")
        if pts[members["POISON_CANDIDATE"]["sample_id"]]["status"] in {"INPUT_MISSING", "EVIDENCE_INSUFFICIENT"}:
            tags.append("F5_METADATA_OR_EVIDENCE_COVERAGE_GAP")
        taxonomy.append({"group_id": group, **group_metadata[group], "tags": tags, "status": "DIAGNOSTIC_CANDIDATE_NOT_ADJUDICATED_CAUSE"})
        if group in hard_ids:
            sample = {}
            for kind, row in members.items():
                candidate = candidates[row["sample_id"]]
                sample[kind_to_short[kind]] = {"sample_id": row["sample_id"], "claim_excerpt": candidate["phase1_view"]["candidate_text"][:140], "retrieved_top5": sorted(trace[row["sample_id"]], key=lambda x: x["rank"]), "score_full": scores["Full SEPT"][row["sample_id"]], "score_s": scores["S-only"][row["sample_id"]], "score_t": scores["T-only"][row["sample_id"]], "score_p": scores["P-only"][row["sample_id"]], "feature_values_by_view": {view: {name: row["features"][name] for name in names} for view, names in views.items()}, "pts_status": pts[row["sample_id"]]["status"]}
            hard.append({"group_id": group, **group_metadata[group], "members": sample, "full_p_hn_margin": margin(group, "Full SEPT", "MATCHED_HARD_NEGATIVE"), "full_p_clean_margin": margin(group, "Full SEPT", "CLEAN_CURRENT"), "taxonomy_tags": tags})

    strata: dict[str, dict[str, Any]] = {}
    for key in ("hkp", "stealth", "domain"):
        result = {}
        for value in sorted({meta[key] for meta in group_metadata.values()}):
            subset = [group for group, meta in group_metadata.items() if meta[key] == value]
            result[value] = {"groups": len(subset), "p_gt_hn": {model: sum(margin(group, model, "MATCHED_HARD_NEGATIVE") > 0 for group in subset) for model in ("S-only", "P-only", "T-only", "Full SEPT")}, "full_p_gt_clean": sum(margin(group, "Full SEPT", "CLEAN_CURRENT") > 0 for group in subset), "failure_tags": dict(Counter(tag for item in taxonomy if item["group_id"] in subset for tag in item["tags"]))}
        strata[key] = result
    coefficient = json.loads((args.original_run / (PREFIX + "COEFFICIENT_ANALYSIS_V1_1.json")).read_text(encoding="utf-8"))["per_feature"]
    alignment = []
    for item in inventory:
        name = item["feature_name"]
        coef = coefficient[name]
        expected = 1 if item["orientation"] == "HIGHER_IS_RISKIER" else -1 if item["orientation"] == "LOWER_IS_RISKIER" else 0
        observed_sign = 1 if coef["median"] > TOL else -1 if coef["median"] < -TOL else 0
        status = "CONSTANT_NO_INFORMATION" if item["constant"] else "NON_MONOTONIC_NO_SIGN_EXPECTATION" if expected == 0 else "UNSTABLE" if coef["sign_stability"] < 0.75 else "SEMANTICALLY_ALIGNED" if observed_sign == expected else "SIGN_INVERTED"
        alignment.append({"feature_name": name, "view": item["view"], "orientation": item["orientation"], "median_coefficient": coef["median"], "sign_stability": coef["sign_stability"], "classification": status, "not_causal_importance": True})
    outputs = {
        "PAPER1_FINAL72_FEATURE_DIRECTION_DIAGNOSTIC_V1.json": {"inventory": inventory, "directions": directions, "nominal": 21, "constant": sum(item["constant"] for item in inventory), "varying": len(varying), "effective_unique_varying_vectors": len(unique_vectors), "exact_duplicate_pairs": exact_dupes, "high_spearman_pairs_abs_ge_0_9": high_corr},
        "PAPER1_TEMPORAL_CAPABILITY_GAP_REPORT_V1.json": temporal,
        "PAPER1_PROVENANCE_CAPABILITY_GAP_REPORT_V1.json": provenance,
        "PAPER1_FULL_VS_MINUS_VIEW_SCORE_SHIFT_V1.json": {"definition": "Full minus ablated held-out decision score; HELPED/HURT by signed P-HN margin delta with 1e-12 tie; not causal", "T": shifts["T"], "P": shifts["P"]},
        "PAPER1_DOCUMENT_DETECTOR_FAILURE_TAXONOMY_V1.json": {"items": taxonomy, "tag_counts": dict(Counter(tag for item in taxonomy for tag in item["tags"])), "not_causal": True},
        "PAPER1_DOCUMENT_DETECTOR_HARD_GROUP_ANALYSIS_V1.json": {"groups": hard, "retrieval_context": "Frozen Q_NO_TITLE HYBRID top5 trace; not oracle E1/E2"},
        "PAPER1_DOCUMENT_DETECTOR_HKP_S_DOMAIN_ANALYSIS_V1.json": strata,
        "PAPER1_DOCUMENT_DETECTOR_SIGN_ALIGNMENT_V1.json": {"items": alignment, "counts": dict(Counter(item["classification"] for item in alignment)), "collinearity": high_corr},
    }
    if args.output.exists() and any(args.output.iterdir()):
        raise ValueError("OUTPUT_NAMESPACE_NOT_EMPTY")
    args.output.mkdir(parents=True, exist_ok=False)
    for name, content in outputs.items():
        runner.dump(args.output / name, content)
    runner.dump(args.output / "result_hash_manifest.json", {"files_sha256": {path.name: runner.sha(path) for path in sorted(args.output.iterdir()) if path.is_file()}, "source_hashes": {"original_full_oof": runner.sha(args.original_run / (PREFIX + "OOF_PREDICTIONS_V1_1.jsonl")), "reconstruction_manifest": runner.sha(args.reconstruction / "result_hash_manifest.json"), "feature_set": runner.sha(args.feature_set), "matrix": runner.sha(args.matrix), "gt": runner.sha(args.gt), "candidates": runner.sha(args.candidates), "trace": runner.sha(args.trace), "pts": runner.sha(args.pts)}})
    print(json.dumps({"output": str(args.output), "manifest_sha256": runner.sha(args.output / "result_hash_manifest.json"), "constant": sum(item["constant"] for item in inventory), "effective_varying": len(unique_vectors), "T_shifts": dict(Counter(row["p_hn_diagnostic"] for row in shifts["T"])), "P_shifts": dict(Counter(row["p_hn_diagnostic"] for row in shifts["P"])), "hard_groups": len(hard), "hkp": strata["hkp"], "stealth": strata["stealth"], "domain": strata["domain"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
