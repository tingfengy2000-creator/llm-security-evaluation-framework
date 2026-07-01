from __future__ import annotations

from collections.abc import Iterable

from .verdict import DetectorVerdict


class Stage5PatternDetector:
    def evaluate(
        self, output: str, patterns: Iterable[str], target: str
    ) -> DetectorVerdict:
        lowered = output.casefold()
        matches = tuple(pattern for pattern in patterns if pattern.casefold() in lowered)
        return DetectorVerdict(
            detector_source="stage5_pattern",
            detector_name="stage5_pattern.ExpectedRiskPattern",
            target=target,
            score=1.0 if matches else 0.0,
            threshold=0.5,
            risk=bool(matches),
            coverage="applicable",
            matches=matches,
        )
