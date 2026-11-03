"""Freeze a private 12-group selection and audit D1 readiness, without inference."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from llmguard.domains.retrieval.hidden_poisoning.rag_defense_reconstruction.evaluation_preparation import (  # noqa: E402
    SEED, TASK, audit_existing_packets, select_groups,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise RuntimeError("NEW_OUTPUT_REQUIRED")
    manifest = json.loads((args.bundle / "BUNDLE_MANIFEST.json").read_text("utf-8"))
    for record in manifest["files"]:
        path = args.bundle / record["path"]
        if not path.resolve().is_relative_to(args.bundle.resolve()):
            raise ValueError("BUNDLE_PATH_ESCAPE")
        if hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
            raise ValueError("BUNDLE_IDENTITY_CHANGED")
    labels = [json.loads(line) for line in (args.bundle / "evaluation/labels.jsonl").read_text("utf-8").splitlines()]
    rows = [json.loads(line) for line in (args.bundle / "runtime/f5.jsonl").read_text("utf-8").splitlines()]
    groups = select_groups(labels)
    chosen = [r for r in labels if r["group_evaluation_only"] in groups]
    ids = {r["candidate_id"] for r in chosen}
    if len(ids) != 36:
        raise ValueError("36_UNIQUE_CANDIDATES_REQUIRED")
    selected_rows = [r for r in rows if r["candidate_id"] in ids]
    args.output.mkdir(parents=True)
    selection = {"task": TASK, "seed": SEED, "rule": "sha256(TASK|SEED|S|group), ascending, first four per S", "selected_groups_evaluator_only": groups, "selected_candidates_evaluator_only": chosen, "selection_uses_model_outcomes": False}
    selection_path = args.output / "SELECTION_EVALUATOR_ONLY.json"
    selection_path.write_text(json.dumps(selection, ensure_ascii=False, indent=2), "utf-8")
    summary = {"task": TASK, "full_signed_bundle": audit_existing_packets(rows), "selected_12_groups": audit_existing_packets(selected_rows), "selection_sha256": hashlib.sha256(selection_path.read_bytes()).hexdigest(), "source_manifest_sha256": hashlib.sha256((args.bundle / "BUNDLE_MANIFEST.json").read_bytes()).hexdigest(), "source_f5_sha256": hashlib.sha256((args.bundle / "runtime/f5.jsonl").read_bytes()).hexdigest(), "no_prediction_files_opened_for_selection": True, "paid_calls": 0}
    (args.output / "D1_QUERY_READINESS.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), "utf-8")
    print(json.dumps(summary, ensure_ascii=True))


if __name__ == "__main__":
    main()
