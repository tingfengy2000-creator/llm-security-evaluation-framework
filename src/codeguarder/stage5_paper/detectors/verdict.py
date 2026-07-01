from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class DetectorVerdict:
    detector_source: Literal["garak", "stage5_pattern"]
    detector_name: str
    target: Literal["raw", "final"]
    score: float | None
    threshold: float
    risk: bool | None
    coverage: Literal["applicable", "not_applicable", "error"]
    matches: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "detector_source": self.detector_source,
            "detector_name": self.detector_name,
            "target": self.target,
            "score": self.score,
            "threshold": self.threshold,
            "risk": self.risk,
            "coverage": self.coverage,
            "matches": list(self.matches),
        }
