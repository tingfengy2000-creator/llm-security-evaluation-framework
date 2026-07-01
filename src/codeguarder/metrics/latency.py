from __future__ import annotations

from collections.abc import Mapping, Sequence
from statistics import fmean
from typing import Any


def mean_latency_ms(records: Sequence[Mapping[str, Any]]) -> float:
    values = [float(record["latency_ms"]) for record in records if "latency_ms" in record]
    return round(fmean(values), 2) if values else 0.0
