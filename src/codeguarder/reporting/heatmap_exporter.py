from __future__ import annotations

from pathlib import Path
from typing import Any

from .csv_exporter import write_csv


def write_heatmap(path: Path, rows: list[dict[str, Any]]) -> None:
    columns = (
        "category",
        "guard_mode",
        "attack_attempt_count",
        "asr_percent",
        "input_block_rate_percent",
        "output_block_rate_percent",
        "detector_miss_rate_percent",
        "guard_bypass_rate_percent",
    )
    compact = [{column: row.get(column) for column in columns} for row in rows]
    write_csv(path, compact)
