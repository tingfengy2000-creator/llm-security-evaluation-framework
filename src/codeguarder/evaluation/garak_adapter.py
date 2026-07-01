from __future__ import annotations

from dataclasses import dataclass

from codeguarder.attacks.attack_schema import AttackSample
from codeguarder.taxonomy.classifier import classify_risk


@dataclass(frozen=True)
class DetectorVerdict:
    garak_pass: bool
    detector_source: str
    detector_name: str
    detector_matches: tuple[str, ...]


def evaluate_final_text(
    final_text: str,
    sample: AttackSample,
    official_garak_pass: bool | None = None,
) -> DetectorVerdict:
    assessment = classify_risk(
        final_text,
        sample.expected_risk_patterns,
        sample.category,
    )
    if official_garak_pass is None:
        return DetectorVerdict(
            garak_pass=not assessment.risk,
            detector_source="stage5_pattern",
            detector_name=f"stage5.{sample.category}",
            detector_matches=assessment.matches,
        )
    return DetectorVerdict(
        garak_pass=official_garak_pass,
        detector_source="garak_official",
        detector_name=f"garak.{sample.category}",
        detector_matches=assessment.matches,
    )
