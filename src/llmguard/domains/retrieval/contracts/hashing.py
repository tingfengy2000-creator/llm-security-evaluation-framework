"""Canonical hashing primitives for stable Retrieval-domain contracts."""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping, Sequence


def canonical_json(payload: Mapping[str, object]) -> str:
    """Return canonical JSON with a deterministic, UTF-8-safe representation.

    Callers must validate domain semantics before hashing. This helper only makes
    the byte representation deterministic; it deliberately knows nothing about
    documents, labels, paths, or evaluation state.
    """

    return json.dumps(
        _json_safe_value(payload, path="$"),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        allow_nan=False,
    )


def canonical_json_sha256(payload: Mapping[str, object]) -> str:
    """Return a SHA-256 digest of :func:`canonical_json` bytes."""

    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def _json_safe_value(value: object, *, path: str) -> object:
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        if not -(2**53 - 1) <= value <= 2**53 - 1:
            raise ValueError(f"{path} integer is outside the JSON-safe range")
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{path} must contain finite floating-point values")
        return value
    if isinstance(value, Mapping):
        result: dict[str, object] = {}
        for key in sorted(value):
            if not isinstance(key, str):
                raise ValueError(f"{path} mapping keys must be strings")
            result[key] = _json_safe_value(value[key], path=f"{path}.{key}")
        return result
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return [
            _json_safe_value(item, path=f"{path}[{index}]")
            for index, item in enumerate(value)
        ]
    raise ValueError(f"{path} contains an unsupported canonical JSON value")
