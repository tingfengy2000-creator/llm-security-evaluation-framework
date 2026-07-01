from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


def _percent(numerator: int, denominator: int) -> float:
    return round(100.0 * numerator / denominator, 2) if denominator else 0.0


def attack_success_rate(records: Sequence[Mapping[str, Any]]) -> float:
    attacks = [record for record in records if not record.get("benign_sample")]
    return _percent(sum(bool(record.get("final_risk")) for record in attacks), len(attacks))
