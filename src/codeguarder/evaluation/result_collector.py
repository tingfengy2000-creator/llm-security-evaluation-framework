from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from typing import Any

from codeguarder.metrics.metrics import compute_metrics, group_metrics
from codeguarder.taxonomy.failure_taxonomy import FAILURE_TYPE_NAMES


def collect_metrics(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    mode_rows = group_metrics(records, ("guard_mode",))
    mode_baseline = next(
        (row["mean_latency_ms"] for row in mode_rows if row["guard_mode"] == "passthrough"),
        0.0,
    )
    rows = []
    for row in mode_rows:
        row["scope"] = "mode"
        row["category"] = "all"
        row["latency_overhead_percent"] = _latency_overhead(
            row["mean_latency_ms"], mode_baseline
        )
        rows.append(row)
    category_rows = group_metrics(records, ("category", "guard_mode"))
    category_baselines = {
        row["category"]: row["mean_latency_ms"]
        for row in category_rows
        if row["guard_mode"] == "passthrough"
    }
    for row in category_rows:
        row["scope"] = "category_mode"
        row["latency_overhead_percent"] = _latency_overhead(
            row["mean_latency_ms"],
            category_baselines.get(row["category"], 0.0),
        )
        rows.append(row)
    return rows


def _latency_overhead(value: float, baseline: float) -> float:
    if baseline <= 0:
        return 0.0
    return round((value - baseline) * 100.0 / baseline, 2)


def collect_heatmap(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    attacks = [record for record in records if not record.get("benign_sample")]
    return group_metrics(attacks, ("category", "guard_mode"))


def collect_taxonomy(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    counts = Counter(
        failure_type
        for record in records
        for failure_type in record.get("failure_types", [])
    )
    by_mode = {}
    for mode in sorted({str(record.get("guard_mode")) for record in records}):
        mode_counts = Counter(
            failure_type
            for record in records
            if record.get("guard_mode") == mode
            for failure_type in record.get("failure_types", [])
        )
        by_mode[mode] = dict(sorted(mode_counts.items()))
    return {
        "definitions": FAILURE_TYPE_NAMES,
        "counts": {key: counts.get(key, 0) for key in FAILURE_TYPE_NAMES},
        "by_mode": by_mode,
    }


def collect_overall(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return compute_metrics(records)
