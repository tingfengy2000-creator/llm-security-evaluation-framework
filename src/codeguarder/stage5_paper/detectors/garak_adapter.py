from __future__ import annotations

import importlib
import os
from pathlib import Path

from .verdict import DetectorVerdict


class GarakDetectorAdapter:
    def __init__(self, detector_names: tuple[str, ...], threshold: float = 0.5):
        self.detector_names = detector_names
        self.threshold = threshold

    @staticmethod
    def _prepare_environment() -> None:
        root = Path(__file__).resolve().parents[4]
        runtime = root / "deliverables" / "stage5_paper" / "runtime"
        os.environ.setdefault("XDG_CONFIG_HOME", str(runtime / "xdg_config"))
        os.environ.setdefault("XDG_DATA_HOME", str(runtime / "xdg_data"))
        os.environ.setdefault("XDG_CACHE_HOME", str(runtime / "xdg_cache"))

    def not_applicable(self, target: str) -> DetectorVerdict:
        return DetectorVerdict(
            detector_source="garak",
            detector_name="none",
            target=target,
            score=None,
            threshold=self.threshold,
            risk=None,
            coverage="not_applicable",
        )

    def evaluate(
        self,
        prompt: str,
        output: str,
        notes: dict,
        target: str,
    ) -> list[DetectorVerdict]:
        if not self.detector_names:
            return [self.not_applicable(target)]
        self._prepare_environment()
        from garak.attempt import Attempt, Message

        attempt = Attempt(
            prompt=Message(text=prompt),
            notes=dict(notes),
            probe_classname="codeguarder.stage5_paper.DatasetRunner",
        )
        attempt.outputs = [output]
        verdicts = []
        for detector_name in self.detector_names:
            module_name, class_name = detector_name.rsplit(".", 1)
            module = importlib.import_module(f"garak.detectors.{module_name}")
            detector = getattr(module, class_name)()
            scores = list(detector.detect(attempt))
            score = scores[0] if scores else None
            verdicts.append(
                DetectorVerdict(
                    detector_source="garak",
                    detector_name=detector_name,
                    target=target,
                    score=None if score is None else float(score),
                    threshold=self.threshold,
                    risk=None if score is None else float(score) >= self.threshold,
                    coverage="error" if score is None else "applicable",
                )
            )
        return verdicts
