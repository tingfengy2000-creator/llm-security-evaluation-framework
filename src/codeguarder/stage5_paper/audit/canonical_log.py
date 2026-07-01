from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


GUARD_ORDER = {"P": 0, "I": 1, "O": 2, "F": 3}


def write_canonical_attempts(path: Path, records: Iterable[dict[str, Any]]) -> None:
    ordered = sorted(
        records,
        key=lambda record: (
            record.get("attack_id", ""),
            record.get("sample_id", ""),
            GUARD_ORDER.get(record.get("guard_code", ""), 99),
            record.get("repetition_index", 0),
        ),
    )
    lines = [
        json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        for record in ordered
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8", newline="\n")
