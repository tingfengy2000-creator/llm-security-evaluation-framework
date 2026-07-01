from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            for row in rows
        )
        + ("\n" if rows else ""),
        encoding="utf-8",
        newline="\n",
    )


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def metric_rows(metrics: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for name, value in metrics.items():
        if isinstance(value, dict):
            rows.append({"metric": name, **value})
    return rows


def taxonomy_result(records: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(
        failure for record in records for failure in record.get("failure_types", [])
    )
    return {"counts": {f"T{i}": counts.get(f"T{i}", 0) for i in range(1, 10)}}


def heatmap_rows(records: list[dict[str, Any]], dimension: str) -> list[dict[str, Any]]:
    rows = []
    values = sorted({str(record.get(dimension)) for record in records if not record.get("benign_sample")})
    for value in values:
        for code in ("P", "I", "O", "F"):
            group = [
                record
                for record in records
                if str(record.get(dimension)) == value
                and record.get("guard_code") == code
                and not record.get("benign_sample")
            ]
            risky = sum(bool(record.get("final_risk")) for record in group)
            rows.append(
                {
                    dimension: value,
                    "guard_code": code,
                    "attempts": len(group),
                    "risk_count": risky,
                    "asr_percent": round(100 * risky / len(group), 2) if group else 0.0,
                }
            )
    return rows


def write_summary(
    path: Path,
    execution_id: str,
    fingerprint: str,
    status: str,
    attempts: int,
    metrics: dict[str, Any],
) -> None:
    path.write_text(
        "\n".join(
            [
                "# Stage 5 Paper 运行摘要",
                "",
                f"- execution_id: `{execution_id}`",
                f"- experiment_fingerprint: `{fingerprint}`",
                f"- run_status: `{status}`",
                f"- attempt_count: {attempts}",
                f"- ASR: {metrics['asr']['rate_percent']:.2f}%",
                f"- DMR: {metrics['dmr']['rate_percent']:.2f}%",
                f"- GBR: {metrics['gbr']['rate_percent']:.2f}%",
                f"- Over-block: {metrics['overblock']['rate_percent']:.2f}%",
                "",
                "结论仅适用于当前攻击矩阵、当前模型与当前 rule-based baseline。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
