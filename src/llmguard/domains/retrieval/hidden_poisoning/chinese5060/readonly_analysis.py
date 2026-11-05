"""Pure old-output statistics and exact-path readers; no scientific runtime imports."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class VerifiedReader:
    def __init__(self, root: Path, allow: dict[str, str]):
        self.root = root.resolve()
        self.allow = dict(allow)
        self.events: list[dict[str, str]] = []

    def read(self, relative: str) -> bytes:
        if relative not in self.allow:
            raise PermissionError("DENIED_BEFORE_IO")
        path = self.root / relative
        if not path.resolve().is_relative_to(self.root) or path.is_symlink():
            raise PermissionError("PATH_ESCAPE")
        raw = path.read_bytes()
        actual = hashlib.sha256(raw).hexdigest()
        if actual != self.allow[relative]:
            raise ValueError("INPUT_HASH_MISMATCH")
        self.events.append({"path": relative, "sha256": actual, "status": "LOCAL_PRIVATE_EVIDENCE_VERIFIED"})
        return raw

    def json(self, relative: str) -> Any:
        return json.loads(self.read(relative))


def stage_features(row: dict[str, Any]) -> dict[str, Any]:
    obs = row["observations"]
    n = obs["n_adv"]
    scores = obs.get("frequency_scores")
    removed = row["removed_indices"]
    if row["status"] != "PASS" or not isinstance(n, int) or not 0 < n < 5:
        raise ValueError("UNSUPPORTED_OR_FAILED_TRACE")
    result = {"world_id": row["world_id"], "n_adv": n, "n_tfidf": obs.get("n_tfidf"),
        "removed_indices": removed, "kept_indices": [i for i in range(5) if i not in removed],
        "latency_seconds": row["latency_seconds"], "raw_any_score_tie_pairs": obs.get("equal_frequency_score_pairs"),
        "coverage": {"cluster_assignments": False, "embeddings": False, "top_similar_pairs": False,
            "per_term_tfidf_weights": False, "frequency_scores": scores is not None,
            "n_adv": True, "n_tfidf": "n_tfidf" in obs, "removed_indices": True}}
    if scores is None:
        result["stage2_status"] = "INSUFFICIENT_TRACE"
        return result
    if len(scores) != 5 or len(removed) != n:
        raise ValueError("STAGE_TRACE_SHAPE_MISMATCH")
    order = sorted(range(5), key=lambda i: (-scores[i], i))
    if sorted(order[:n]) != removed:
        raise ValueError("SAVED_SCORES_DO_NOT_REPRODUCE_SAVED_SELECTION")
    pairs = sum(scores[i] == scores[j] for i in range(5) for j in range(i + 1, 5))
    if pairs != obs["equal_frequency_score_pairs"]:
        raise ValueError("SAVED_TIE_COUNT_MISMATCH")
    cutoff = scores[order[n - 1]]
    tie_group = [i for i in range(5) if scores[i] == cutoff]
    cut_tie = bool(set(tie_group) & set(removed)) and bool(set(tie_group) - set(removed))
    result.update({"frequency_scores": scores, "score_order": order, "cutoff_tie_group": tie_group,
        "boundary_tie": cut_tie, "any_score_tie": pairs > 0, "stage2_status": "SAVED_SELECTION_RECOMPUTED_EXACTLY"})
    return result


def flip_key(before: bool, after: bool) -> str:
    return f"{int(before)}{int(after)}"
