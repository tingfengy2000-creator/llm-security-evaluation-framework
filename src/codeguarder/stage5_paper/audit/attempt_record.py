from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ExperimentConfig:
    schema_version: str
    dataset_manifest_hash: str
    provider: str
    model: str
    seed: int
    generation_config: dict[str, Any]
    detector_config: tuple[str, ...]
    guard_version: str

    def canonical_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AttemptRecord:
    data: dict[str, Any]

    def to_canonical_dict(self) -> dict[str, Any]:
        excluded = {
            "execution_id",
            "started_at",
            "latency_ms",
            "retry_count",
            "upstream_request_id_hash",
        }
        return {key: value for key, value in self.data.items() if key not in excluded}
