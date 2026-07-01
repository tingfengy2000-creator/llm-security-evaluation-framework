from __future__ import annotations

import json
from pathlib import Path

from .attack_schema import AttackSample, SchemaError


ATTACK_CATEGORIES = (
    "prompt_injection",
    "role_confusion",
    "encoding_obfuscation",
    "context_injection",
    "data_exfiltration",
    "tool_injection",
)


def _load_jsonl(path: Path) -> list[AttackSample]:
    if not path.is_file():
        raise FileNotFoundError(path)
    samples: list[AttackSample] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            samples.append(AttackSample.from_dict(json.loads(line)))
        except (json.JSONDecodeError, SchemaError) as exc:
            raise SchemaError(f"{path}:{line_number}: {exc}") from exc
    return samples


def _ensure_unique_ids(samples: list[AttackSample]) -> None:
    ids = [sample.id for sample in samples]
    duplicates = sorted({sample_id for sample_id in ids if ids.count(sample_id) > 1})
    if duplicates:
        raise SchemaError(f"duplicate sample ids: {duplicates}")


def load_attack_matrix(data_root: Path, per_category: int = 2) -> list[AttackSample]:
    if per_category < 1:
        raise ValueError("per_category must be positive")
    samples: list[AttackSample] = []
    for category in ATTACK_CATEGORIES:
        category_samples = _load_jsonl(data_root / "attacks" / f"{category}.jsonl")
        if any(sample.category != category for sample in category_samples):
            raise SchemaError(f"category mismatch in {category}.jsonl")
        if len(category_samples) < per_category:
            raise SchemaError(
                f"{category} has {len(category_samples)} samples; "
                f"{per_category} required"
            )
        samples.extend(category_samples[:per_category])
    _ensure_unique_ids(samples)
    return samples


def load_benign_requests(data_root: Path) -> list[AttackSample]:
    samples = _load_jsonl(data_root / "benign" / "benign_requests.jsonl")
    if any(not sample.benign for sample in samples):
        raise SchemaError("benign_requests.jsonl contains a non-benign category")
    _ensure_unique_ids(samples)
    return samples
