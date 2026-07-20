"""One recursive validator for public metadata crossing retrieval boundaries."""

from __future__ import annotations

import math
import re
import unicodedata
from collections.abc import Mapping, Sequence
from types import MappingProxyType

from .errors import RetrievalInputError

_MAX_DEPTH = 32
_JSON_SAFE_INTEGER = 2**53 - 1
_ABSOLUTE_PATH = re.compile(r"(?:\A[A-Za-z]:[\\/]|\A[\\/]{2}|\A/|\Afile:)", re.IGNORECASE)
_FORBIDDEN = frozenset(
    {
        "poisoned", "poison_label", "label", "attack_id", "attack_goal",
        "attack_category", "expected_answer", "expected_behavior",
        "expected_clean_doc_ids", "failure_type", "ground_truth", "oracle",
        "risk_goal", "stealth_level",
    }
)
_NORMALIZED_FORBIDDEN = frozenset(
    re.sub(r"[^a-z0-9]+", "", unicodedata.normalize("NFKC", item).casefold())
    for item in _FORBIDDEN
)


def normalize_metadata_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", unicodedata.normalize("NFKC", value).casefold())


def freeze_public_metadata(
    value: Mapping[str, object],
    *,
    allowed_keys: frozenset[str] | None = None,
    error_type: type[ValueError] = RetrievalInputError,
) -> Mapping[str, object]:
    """Deep-freeze JSON-safe metadata after label and path isolation checks."""

    active: set[int] = set()
    return _freeze_mapping(value, active=active, depth=0, allowed_keys=allowed_keys, error_type=error_type)


def thaw_public_metadata(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: thaw_public_metadata(value[key]) for key in sorted(value)}
    if isinstance(value, tuple):
        return [thaw_public_metadata(item) for item in value]
    return value


def _freeze_mapping(
    value: Mapping[str, object], *, active: set[int], depth: int,
    allowed_keys: frozenset[str] | None, error_type: type[ValueError],
) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise error_type("public_metadata must be a mapping")
    if depth > _MAX_DEPTH:
        raise error_type("public_metadata exceeds maximum nesting depth")
    value_id = id(value)
    if value_id in active:
        raise error_type("public_metadata contains a reference cycle")
    active.add(value_id)
    try:
        keys = tuple(value.keys())
        if not all(isinstance(key, str) for key in keys):
            raise error_type("public_metadata keys must be strings")
        frozen: dict[str, object] = {}
        for key in sorted(keys):
            if _ABSOLUTE_PATH.search(key) is not None:
                raise error_type("public_metadata keys must not be absolute paths")
            if normalize_metadata_key(key) in _NORMALIZED_FORBIDDEN:
                raise error_type("public_metadata contains a forbidden field")
            if allowed_keys is not None and key not in allowed_keys:
                raise error_type("public_metadata contains a non-allowlisted field")
            frozen[key] = _freeze_value(value[key], active=active, depth=depth + 1, error_type=error_type)
        return MappingProxyType(frozen)
    finally:
        active.remove(value_id)


def _freeze_value(value: object, *, active: set[int], depth: int, error_type: type[ValueError]) -> object:
    if depth > _MAX_DEPTH:
        raise error_type("public_metadata exceeds maximum nesting depth")
    if isinstance(value, str):
        if _ABSOLUTE_PATH.search(value) is not None:
            raise error_type("public_metadata values must not be absolute paths")
        return value
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        if not -_JSON_SAFE_INTEGER <= value <= _JSON_SAFE_INTEGER:
            raise error_type("public_metadata integer is outside the JSON-safe range")
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise error_type("public_metadata must contain finite numbers")
        return value
    if isinstance(value, Mapping):
        return _freeze_mapping(value, active=active, depth=depth, allowed_keys=None, error_type=error_type)
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        value_id = id(value)
        if value_id in active:
            raise error_type("public_metadata contains a reference cycle")
        active.add(value_id)
        try:
            return tuple(_freeze_value(item, active=active, depth=depth + 1, error_type=error_type) for item in value)
        finally:
            active.remove(value_id)
    raise error_type("public_metadata contains an unsupported value type")
