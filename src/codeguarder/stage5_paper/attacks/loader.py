from __future__ import annotations

import json
from pathlib import Path

from .schema import AttackSample, SchemaError


ATTACK_IDS = ("A1", "A2", "A3", "A4", "A5", "A6")


def _load(path: Path) -> list[AttackSample]:
    samples: list[AttackSample] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            samples.append(AttackSample.from_dict(json.loads(line)))
        except (json.JSONDecodeError, SchemaError) as exc:
            raise SchemaError(f"{path}:{line_number}: {exc}") from exc
    ids = [sample.sample_id for sample in samples]
    if len(ids) != len(set(ids)):
        raise SchemaError(f"duplicate sample IDs in {path}")
    return samples


def load_attack_matrix(data_root: Path) -> list[AttackSample]:
    samples = _load(data_root / "attack_matrix.jsonl")
    if any(sample.attack_id not in ATTACK_IDS for sample in samples):
        raise SchemaError("attack matrix contains non-attack rows")
    return sorted(samples, key=lambda sample: (sample.attack_id, sample.sample_id))


def load_benign_requests(data_root: Path) -> list[AttackSample]:
    samples = _load(data_root / "benign_requests.jsonl")
    if any(not sample.benign for sample in samples):
        raise SchemaError("benign dataset contains attack rows")
    return sorted(samples, key=lambda sample: sample.sample_id)
