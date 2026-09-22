"""Audit frozen provenance observability and apply the Owner-approved A→C gate.

No class, GT, annotation, Expected, or Oracle field is read until the versioned
label-blind feature matrix has been written and hashed. This script never fits a
model, imputes a value, or changes the V1 inputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TASK = "P1-DOCUMENT-DETECTOR-MISSINGNESS-CONTRACT-OWNER-RESOLUTION-01"
BLOCKED = ("host_publisher_relation", "publisher_issuer_match")
EXPECTED_HASHES = {
    "matrix_v1": "c1a8dfa250ab62843d9234754f27936667c2a760dbdae8be4f5405bb47dc30c0",
    "feature_set_v1": "585350c79d014997f649532549703aa57950e2cd35c724fbd9025442db01ce06",
    "candidates": "f530471ecd6551300d68c8ddf104cadce2305d8ff91e64010be222820628252d",
    "gt": "9e6224ef2cb2cb8e729f9ab569d09589c951e6df4ed3327c63c82913066d720a",
    "corpus": "331705332f7785ef0c7cd39dbfb294f912e0bb94954974b985e5967dafe8ff7b",
    "registry_v2": "1e76808efd3bf30115d399ac96ea2777eddd47a36cef693d569b2344acba20dc",
}
FORBIDDEN = {
    "label", "target", "candidate_class", "hkp", "stealth", "expected",
    "owner", "annotator", "sample_id", "group_id", "path", "file",
    "evidence_selection", "risk_goal", "ground_truth", "oracle",
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in records), encoding="utf-8")


def row_id(text: str) -> str:
    return "FR-" + hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def metadata_audit(
    corpus: list[dict[str, Any]], trace: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Inspect frozen top-five roles without consulting Candidate labels."""
    by_doc = {doc["evidence_doc_id"]: doc for doc in corpus}
    if len(by_doc) != len(corpus) or len(corpus) != 57:
        raise ValueError("trusted corpus identity or cardinality violation")
    top: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for hit in trace:
        if hit["rank"] <= 5:
            top[hit["candidate_id"]].append(hit)
    if len(top) != 72 or any(sorted(h["rank"] for h in hits) != [1, 2, 3, 4, 5] for hits in top.values()):
        raise ValueError("locked Top5 is not exactly 72 x 5")
    if any(hit["evidence_doc_id"] not in by_doc for hits in top.values() for hit in hits):
        raise ValueError("retrieval reference not in trusted corpus")

    audit = []
    doc_role_counts: Counter[str] = Counter()
    for candidate_id, hits in sorted(top.items()):
        details = []
        for hit in sorted(hits, key=lambda item: item["rank"]):
            doc = by_doc[hit["evidence_doc_id"]]
            host, publisher, issuer = (doc.get(key) for key in ("source_host", "publisher", "issuer"))
            doc_role_counts["top5_documents"] += 1
            doc_role_counts["host"] += bool(host)
            doc_role_counts["publisher"] += bool(publisher)
            doc_role_counts["issuer"] += bool(issuer)
            doc_role_counts["publisher_and_issuer"] += bool(publisher and issuer)
            details.append({
                "rank": hit["rank"], "evidence_doc_id": doc["evidence_doc_id"],
                "source_host_available": bool(host), "publisher_available": bool(publisher),
                "issuer_available": bool(issuer),
                "publisher_provenance": doc.get("metadata_source") if publisher else None,
                "issuer_provenance": doc.get("metadata_status", {}).get("issuer") if issuer else None,
                "snapshot_id": doc.get("snapshot_id"), "snapshot_sha256": doc.get("snapshot_sha256"),
            })
        audit.append({
            "candidate_id": candidate_id,
            "source_host_available": any(d["source_host_available"] for d in details),
            "publisher_available": any(d["publisher_available"] for d in details),
            "issuer_available": any(d["issuer_available"] for d in details),
            "publisher_issuer_same_doc_available": any(
                d["publisher_available"] and d["issuer_available"] for d in details
            ),
            "host_publisher_relation": {
                "status": "INPUT_MISSING", "candidate_level_computable": False,
                "reason": "No frozen host-to-publisher institution relation taxonomy or mapping; categorical output cannot be cast to the V1 binary slot.",
            },
            "publisher_issuer_match": {
                "status": "INPUT_MISSING", "candidate_level_computable": False,
                "reason": "Document-level roles exist in some retrieved items, but no frozen, meaning-preserving candidate-level Top5 aggregation binds the compared roles to one candidate source document.",
            },
            "retrieved_top5_metadata": details,
        })
    corpus_counts = {
        key: sum(bool(doc.get(key)) for doc in corpus)
        for key in ("source_host", "publisher", "issuer")
    }
    corpus_counts["publisher_and_issuer_same_doc"] = sum(
        bool(doc.get("publisher") and doc.get("issuer")) for doc in corpus
    )
    return audit, {"corpus": corpus_counts, "top5": dict(doc_role_counts)}


def project_v1_to_c(
    feature_set: dict[str, Any], matrix: list[dict[str, Any]]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    names = [row["feature_name"] for row in feature_set["features"]]
    if len(names) != 23 or len(set(names)) != 23 or not set(BLOCKED) <= set(names):
        raise ValueError("Feature Set V1 identity/shape mismatch")
    if len(matrix) != 72 or len({row["feature_row_id"] for row in matrix}) != 72:
        raise ValueError("Matrix V1 row identity/shape mismatch")
    if any(set(row["features"]) != set(names) for row in matrix):
        raise ValueError("Matrix V1 feature keys mismatch")
    if any(row["features"][name] is not None for row in matrix for name in BLOCKED):
        raise ValueError("Option C trigger is not the expected all-missing defect")
    if any((set(row) | set(row["features"])) & FORBIDDEN for row in matrix):
        raise ValueError("V1 matrix contains a forbidden model field")

    retained = [name for name in names if name not in BLOCKED]
    c_set = {
        **feature_set,
        "features": [row for row in feature_set["features"] if row["feature_name"] in retained],
        "version": "V1.1",
        "owner_decision": "OPTION_A_FIRST_CONDITIONAL_C_APPROVED_OPTION_B_REJECTED",
        "exclusion_basis": "MEASURABILITY_ONLY_NO_LABEL_OR_PERFORMANCE_SELECTION",
        "deferred_features": list(BLOCKED),
    }
    c_matrix = [
        {"feature_row_id": row["feature_row_id"], "features": {name: row["features"][name] for name in retained}}
        for row in matrix
    ]
    if any(
        c_row["features"] != {name: old["features"][name] for name in retained}
        for old, c_row in zip(matrix, c_matrix, strict=True)
    ):
        raise AssertionError("retained V1 values changed")
    return c_set, c_matrix


def post_lock_preflight(
    candidates: list[dict[str, Any]], matrix: list[dict[str, Any]],
    feature_set: dict[str, Any], audit: list[dict[str, Any]], lock_at: str,
) -> dict[str, Any]:
    by_row = {row["feature_row_id"]: row for row in matrix}
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_candidate = {row["sample_id"]: row for row in candidates}
    if len(candidates) != 72 or len(by_candidate) != 72:
        raise ValueError("candidate population invalid")
    if len({row_id(row["phase1_view"]["candidate_text"]) for row in candidates}) != 72:
        raise ValueError("Candidate text to feature-row identity is not unique")
    for row in candidates:
        if row_id(row["phase1_view"]["candidate_text"]) not in by_row:
            raise ValueError("Candidate/Feature row mapping invalid")
        groups[row["triplet_id"]].append(row)
    if len(groups) != 24 or any(len(rows) != 3 for rows in groups.values()):
        raise ValueError("LOGO group structure invalid")
    if any(
        {r["owner_only"]["candidate_kind"] for r in rows}
        != {"CLEAN_CURRENT", "POISON_CANDIDATE", "MATCHED_HARD_NEGATIVE"}
        for rows in groups.values()
    ):
        raise ValueError("matched group class composition invalid")

    names = [row["feature_name"] for row in feature_set["features"]]
    folds = []
    for group_id in sorted(groups):
        train_rows = [
            by_row[row_id(candidate["phase1_view"]["candidate_text"])]
            for other_group, members in groups.items() if other_group != group_id
            for candidate in members
        ]
        observed = {name: sum(row["features"][name] is not None for row in train_rows) for name in names}
        folds.append({
            "held_out_group": group_id, "train_candidates": len(train_rows),
            "validation_candidates": len(groups[group_id]), "observed_training_values": observed,
            "all_train_fold_statistics_exist": all(value > 0 for value in observed.values()),
        })
    class_audit: dict[str, Counter[str]] = defaultdict(Counter)
    domain_audit: dict[str, Counter[str]] = defaultdict(Counter)
    group_audit: dict[str, Counter[str]] = defaultdict(Counter)
    for row in audit:
        candidate = by_candidate[row["candidate_id"]]
        cls = candidate["owner_only"]["candidate_kind"]
        domain = candidate["owner_only"]["domain"]
        group = candidate["triplet_id"]
        for name in BLOCKED:
            status = row[name]["status"]
            class_audit[cls][f"{name}:{status}"] += 1
            domain_audit[domain][f"{name}:{status}"] += 1
            group_audit[group][f"{name}:{status}"] += 1
    class_audit_plain = {key: dict(value) for key, value in sorted(class_audit.items())}
    missingness_class_proxy = any(
        counts.get(f"{name}:INPUT_MISSING", 0) != 24
        for counts in class_audit_plain.values() for name in BLOCKED
    )
    return {
        "label_load_after_matrix_lock": True,
        "matrix_locked_at": lock_at,
        "labels_loaded_at": stamp(),
        "candidate_count": 72, "group_count": 24, "fold_count": len(folds),
        "every_candidate_held_out_once": True,
        "group_crossing_zero": True,
        "folds": folds,
        "all_fold_statistics_exist": all(fold["all_train_fold_statistics_exist"] for fold in folds),
        "excluded_feature_missingness_by_class": class_audit_plain,
        "excluded_feature_missingness_by_domain": {key: dict(value) for key, value in sorted(domain_audit.items())},
        "excluded_feature_missingness_by_group": {key: dict(value) for key, value in sorted(group_audit.items())},
        "excluded_missingness_class_proxy": missingness_class_proxy,
    }


def manifest(output: Path) -> dict[str, Any]:
    files = [
        {"path": path.relative_to(output).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}
        for path in sorted(output.rglob("*")) if path.is_file() and path.name != "final_manifest.json"
    ]
    return {"task_id": TASK, "created_at": stamp(), "files": files}


def run(args: argparse.Namespace) -> dict[str, Any]:
    sources = {
        "matrix_v1": args.matrix_v1, "feature_set_v1": args.feature_set_v1,
        "candidates": args.candidates, "gt": args.gt, "corpus": args.corpus,
        "registry_v2": args.registry_v2,
    }
    actual = {key: sha(path) for key, path in sources.items()}
    if actual != EXPECTED_HASHES:
        raise ValueError(f"frozen identity mismatch: {actual}")
    if args.output.exists():
        raise FileExistsError(f"immutable namespace already exists: {args.output}")
    corpus = read_jsonl(args.corpus)
    registry = json.loads(args.registry_v2.read_text(encoding="utf-8"))
    if len(registry) != 57:
        raise ValueError("Registry V2 cardinality mismatch")
    trace = read_jsonl(args.hybrid_trace)
    feature_set = json.loads(args.feature_set_v1.read_text(encoding="utf-8"))
    matrix = read_jsonl(args.matrix_v1)
    audit, metadata_counts = metadata_audit(corpus, trace)
    c_set, c_matrix = project_v1_to_c(feature_set, matrix)
    args.output.mkdir(parents=True)
    write_jsonl(args.output / "audit/PAPER1_PROVENANCE_METADATA_RECOVERY_AUDIT_V1.jsonl", audit)
    write_json(args.output / "audit/PAPER1_PROVENANCE_METADATA_COVERAGE_V1.json", metadata_counts)
    write_json(args.output / "decision/PAPER1_OPTION_A_FEASIBILITY_DECISION_V1.json", {
        "owner_policy": "A_THEN_CONDITIONAL_C", "option_b_rejected_by_owner": True,
        "option_a_success": False, "option_c_triggered": True,
        "basis": [
            "host_publisher_relation is categorical/undefined-orientation in accepted registry; no frozen host-to-publisher institution relation mapping or numeric encoding exists",
            "publisher_issuer_match has some document-level role pairs, but no frozen candidate-source binding and no meaning-preserving Top5-to-candidate aggregation",
            "both V1 candidate-level values are null for 72/72; inventing a relation or constant would change the accepted feature meaning",
        ],
        "no_new_external_evidence": True, "no_labels_or_performance_used": True,
        "doc_level_metadata_does_not_establish_candidate_level_feature": True,
    })
    write_json(args.output / "features/PAPER1_DOCUMENT_DETECTOR_FEATURE_SET_V1_1.json", c_set)
    matrix_path = args.output / "features/PAPER1_FINAL72_DOCUMENT_DETECTOR_FEATURE_MATRIX_RAW_V1_1.jsonl"
    write_jsonl(matrix_path, c_matrix)
    lock_at = stamp()
    write_json(args.output / "lock/feature_matrix_v1_1_lock.json", {
        "locked_at": lock_at, "matrix_sha256": sha(matrix_path), "rows": 72,
        "feature_count": 21, "model_fit_started": False, "labels_loaded": False,
        "source_matrix_sha256": actual["matrix_v1"], "retained_values_parity": True,
    })

    # The first class/domain/group access is deliberately below the matrix lock.
    candidates = read_jsonl(args.candidates)
    preflight = post_lock_preflight(candidates, c_matrix, c_set, audit, lock_at)
    preflight["input_hashes"] = {**actual, "hybrid_trace": sha(args.hybrid_trace)}
    preflight["feature_set_v1_1_sha256"] = sha(args.output / "features/PAPER1_DOCUMENT_DETECTOR_FEATURE_SET_V1_1.json")
    preflight["feature_matrix_v1_1_sha256"] = sha(matrix_path)
    preflight["feature_count_by_view"] = dict(Counter(row["view"] for row in c_set["features"]))
    preflight["option_b_used"] = False
    preflight["model_fit_started"] = False
    preflight["pass"] = (
        preflight["all_fold_statistics_exist"]
        and not preflight["excluded_missingness_class_proxy"]
        and preflight["group_count"] == 24
        and preflight["feature_count_by_view"]
        == {"PROVENANCE": 6, "ENTITY_CLAIM": 9, "SEMANTIC": 3, "TEMPORAL_VERSION": 3}
    )
    preflight["status"] = "PHASE_A_PREFLIGHT_PASS" if preflight["pass"] else "OPTION_C_ALSO_BLOCKED"
    write_json(args.output / "preflight/PAPER1_DOCUMENT_DETECTOR_PHASE_A_PREFLIGHT_V1_1.json", preflight)
    write_json(args.output / "deferred/PAPER1_DEFERRED_PROVENANCE_FEATURES_V1.json", {
        "status": "DEFERRED_UNTIL_FORMAL_SCALE_METADATA", "features": list(BLOCKED),
        "reason": "No lawful, reproducible candidate-level observed representation under the frozen Pilot input contract",
        "not_performance_selection": True,
        "formal_scale_required_metadata": ["source_host", "page_publisher", "document_issuer", "authority_role", "document_binding", "role_provenance", "host_institution_mapping", "relation_taxonomy"],
    })
    write_json(args.output / "manifest/final_manifest.json", manifest(args.output))
    return {
        "status": preflight["status"], "option_a_success": False,
        "option_c_applied": True, "matrix_sha256": sha(matrix_path),
        "feature_set_sha256": preflight["feature_set_v1_1_sha256"],
        "metadata_counts": metadata_counts,
        "folds_passed": sum(fold["all_train_fold_statistics_exist"] for fold in preflight["folds"]),
        "class_proxy": preflight["excluded_missingness_class_proxy"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in ("output", "matrix_v1", "feature_set_v1", "candidates", "gt", "corpus", "registry_v2", "hybrid_trace"):
        parser.add_argument("--" + name.replace("_", "-"), type=Path, required=True)
    print(json.dumps(run(parser.parse_args()), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
