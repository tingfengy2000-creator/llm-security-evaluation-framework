"""Predict A0 once from locked candidate-only bytes, then seal before evaluation."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.surface_baseline import (
    RULE_SETS,
    predict_surface,
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    args = parser.parse_args()
    base = args.run_root.resolve()
    lock = json.loads((base / "RULE_INPUT_SOURCE_LOCK_V1.json").read_text(encoding="utf-8"))
    for record in lock["locked_files"]:
        assert sha(Path(record["path"])) == record["sha256"]
    source = base / "CANDIDATES_ONLY_V1.jsonl"
    assert sha(source) == lock["candidate_only_sha256"]
    rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == len({r["candidate_id"] for r in rows}) == 120
    assert all(set(row) == {"candidate_id", "candidate_text"} for row in rows)
    output = []
    for name in RULE_SETS:
        for row in rows:
            flag, hit_ids = predict_surface(row["candidate_text"], name)
            output.append({"candidate_id": row["candidate_id"], "method": name,
                           "predicted_flag": flag, "rule_hit_ids": list(hit_ids),
                           "score_kind": "BINARY_CUE_FLAG_NOT_CONTINUOUS_RISK",
                           "run_id": lock["run_id"]})
    predictions = base / "A0_PREDICTIONS_PRE_EVALUATION_V1.jsonl"
    with predictions.open("x", encoding="utf-8", newline="\n") as handle:
        for row in output:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (base / "A0_PREDICTION_LOCK_V1.json").open("x", encoding="utf-8") as handle:
        json.dump({"rows": len(output), "prediction_sha256": sha(predictions),
                   "rule_input_source_lock_sha256": sha(base / "RULE_INPUT_SOURCE_LOCK_V1.json"),
                   "label_S_group_family_oracle_loaded_by_predictor": False,
                   "no_training_or_OOF_claim": True,
                   "locked_utc": datetime.now(timezone.utc).isoformat()}, handle, indent=2)
    print(json.dumps({"rows_locked": len(output), "prediction_sha256": sha(predictions)}))


if __name__ == "__main__":
    main()
