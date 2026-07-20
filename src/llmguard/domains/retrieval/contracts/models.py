from __future__ import annotations

import json
import math
import re
import unicodedata
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from types import MappingProxyType
from typing import Callable, TypeAlias, TypeVar, cast

from .content_ref import ContentRef
from .errors import RetrievalInputError, RetrievalIntegrityError
from .identifiers import derive_evidence_uid, require_chunk_id, require_public_identifier, require_public_query_id, require_sha256
from .public_metadata import freeze_public_metadata, thaw_public_metadata


AuditValue: TypeAlias = (
    str
    | int
    | float
    | bool
    | None
    | list["AuditValue"]
    | dict[str, "AuditValue"]
)

_FORBIDDEN_PIPELINE_FIELD_NAMES = frozenset(
    {
        "poisoned",
        "label",
        "attack_goal",
        "expected_answer",
        "failure_type",
        "ground_truth",
    }
)
_NORMALIZED_FORBIDDEN_PIPELINE_FIELDS = frozenset(
    re.sub(
        r"[^a-z0-9]+",
        "",
        unicodedata.normalize("NFKC", name).casefold(),
    )
    for name in _FORBIDDEN_PIPELINE_FIELD_NAMES
)

GENERATOR_AUDIT_KEYS = frozenset(
    {
        "provider",
        "model",
        "model_name",
        "seed",
        "temperature",
        "max_tokens",
        "revision",
    }
)
DETECTOR_RESULT_AUDIT_KEYS = frozenset(
    {
        "detector_id",
        "detector_name",
        "detector_source",
        "passed",
        "score",
        "matched",
        "rule_ids",
        "output_hash",
        "output_length",
        "method_version",
    }
)
METRICS_AUDIT_KEYS = frozenset(
    {
        "rpr",
        "cir",
        "rmsr",
        "faithfulness",
        "cross_layer_leakage",
        "retrieval_poison_rate",
        "context_injection_rate",
        "retrieval_manipulation_success_rate",
        "cross_layer_leakage_rate",
    }
)
LATENCY_AUDIT_KEYS = frozenset(
    {
        "retrieval_ms",
        "evidence_ms",
        "trust_ms",
        "context_ms",
        "generation_ms",
        "evaluation_ms",
        "total_ms",
    }
)
VALIDATION_STATUS_AUDIT_KEYS = frozenset(
    {
        "status",
        "valid",
        "issue_codes",
        "method_version",
    }
)
TRUST_SIGNAL_SUMMARY_AUDIT_KEYS = frozenset(
    {
        "signal_count",
        "signal_types",
        "method_versions",
        "aggregate_score",
        "ranking_changed",
        "blocked_doc_ids",
    }
)

_NORMALIZED_GROUND_TRUTH_FIELDS = frozenset({"groundtruth"})
_SHA256_PATTERN = re.compile(r"\A[0-9a-f]{64}\Z")
_UTC_ISO8601_PATTERN = re.compile(
    r"\A\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    r"(?:\.\d+)?(?:Z|\+00:00)\Z"
)
_MAX_NESTING_DEPTH = 32
_JSON_SAFE_INTEGER_MAX = 2**53 - 1

FeatureRule: TypeAlias = str
ValidatedValue = TypeVar("ValidatedValue")
InstanceValue = TypeVar("InstanceValue")
MappingKey = TypeVar("MappingKey")

# Stage 6.1 signal extensions require an explicit feature contract.
EVIDENCE_FEATURE_CONTRACTS: Mapping[
    str,
    Mapping[str, FeatureRule],
] = MappingProxyType(
    {
        "provenance_signal": MappingProxyType(
            {
                "source_id": "id",
                "source_type": "string",
                "timestamp": "timestamp",
                "version": "string",
                "content_hash": "sha256",
                "source_count": "nonnegative_int",
                "document_count": "nonnegative_int",
                "age_days": "nonnegative_number",
            }
        ),
        "embedding_anomaly_signal": MappingProxyType(
            {
                "rank": "positive_int",
                "distance": "nonnegative_number",
                "similarity": "similarity",
                "mean_distance": "nonnegative_number",
                "std_distance": "nonnegative_number",
                "z_score": "finite_number",
                "top_k": "positive_int",
            }
        ),
        "semantic_conflict_signal": MappingProxyType(
            {
                "pair_count": "nonnegative_int",
                "conflict_count": "nonnegative_int",
                "max_conflict_score": "score",
                "mean_conflict_score": "score",
                "compared_doc_ids": "id_tuple",
            }
        ),
        "source_diversity_signal": MappingProxyType(
            {
                "source_count": "nonnegative_int",
                "document_count": "nonnegative_int",
                "diversity_ratio": "score",
                "source_types": "string_tuple",
            }
        ),
    }
)
EVIDENCE_FEATURE_ALLOWLISTS: Mapping[str, frozenset[str]] = MappingProxyType(
    {
        signal_type: frozenset(contract)
        for signal_type, contract in EVIDENCE_FEATURE_CONTRACTS.items()
    }
)

_AUDIT_MAPPING_CONTRACTS: Mapping[
    str,
    tuple[frozenset[str], frozenset[str]],
] = MappingProxyType(
    {
        "generator": (GENERATOR_AUDIT_KEYS, frozenset()),
        "detector_results item": (
            DETECTOR_RESULT_AUDIT_KEYS,
            frozenset({"rule_ids"}),
        ),
        "metrics": (METRICS_AUDIT_KEYS, frozenset()),
        "latency": (LATENCY_AUDIT_KEYS, frozenset()),
        "validation_status": (
            VALIDATION_STATUS_AUDIT_KEYS,
            frozenset({"issue_codes"}),
        ),
        "trust_signal_summary": (
            TRUST_SIGNAL_SUMMARY_AUDIT_KEYS,
            frozenset(
                {
                    "signal_types",
                    "method_versions",
                    "blocked_doc_ids",
                }
            ),
        ),
    }
)


def _normalize_field_name(value: str) -> str:
    return re.sub(
        r"[^a-z0-9]+",
        "",
        unicodedata.normalize("NFKC", value).casefold(),
    )


def _require_string_mapping_keys(
    value: Mapping[MappingKey, object],
    path: str,
) -> Mapping[str, object]:
    if not all(isinstance(key, str) for key in value):
        raise ValueError(f"{path} mapping keys must be strings")
    return cast(Mapping[str, object], value)


def _find_normalized_field(
    value: object,
    normalized_fields: frozenset[str],
    path: str = "$",
    *,
    _active_ids: set[int] | None = None,
    _depth: int = 0,
) -> tuple[str, str] | None:
    if _depth > _MAX_NESTING_DEPTH:
        raise ValueError(f"{path} exceeds maximum nesting depth")

    mapping: Mapping[str, object] | None = None
    sequence: Sequence[object] | set[object] | frozenset[object] | None = None
    if isinstance(value, Mapping):
        mapping = _require_string_mapping_keys(value, path)
    elif isinstance(value, (set, frozenset)):
        sequence = value
    elif isinstance(value, Sequence) and not isinstance(
        value,
        (str, bytes, bytearray),
    ):
        sequence = value
    else:
        return None

    active_ids = _active_ids if _active_ids is not None else set()
    value_id = id(value)
    if value_id in active_ids:
        raise ValueError(f"{path} contains a reference cycle")
    active_ids.add(value_id)
    try:
        if mapping is not None:
            for key, nested_value in mapping.items():
                normalized_key = _normalize_field_name(key)
                if normalized_key in normalized_fields:
                    return key, f"{path}.{key}"
                found = _find_normalized_field(
                    nested_value,
                    normalized_fields,
                    f"{path}.{key}",
                    _active_ids=active_ids,
                    _depth=_depth + 1,
                )
                if found is not None:
                    return found
        else:
            assert sequence is not None
            for index, nested_value in enumerate(sequence):
                found = _find_normalized_field(
                    nested_value,
                    normalized_fields,
                    f"{path}[{index}]",
                    _active_ids=active_ids,
                    _depth=_depth + 1,
                )
                if found is not None:
                    return found
        return None
    finally:
        active_ids.remove(value_id)


def _find_forbidden_pipeline_field(
    value: object,
    path: str = "$",
) -> tuple[str, str] | None:
    return _find_normalized_field(
        value,
        _NORMALIZED_FORBIDDEN_PIPELINE_FIELDS,
        path,
    )


def _require_json_safe_integer(value: int, path: str) -> int:
    if not -_JSON_SAFE_INTEGER_MAX <= value <= _JSON_SAFE_INTEGER_MAX:
        raise ValueError(
            f"{path} must be within the JSON safe integer range "
            f"[-{_JSON_SAFE_INTEGER_MAX}, {_JSON_SAFE_INTEGER_MAX}]"
        )
    return value


def _deep_freeze(
    value: object,
    path: str = "$",
    *,
    _active_ids: set[int] | None = None,
    _depth: int = 0,
) -> object:
    if _depth > _MAX_NESTING_DEPTH:
        raise ValueError(f"{path} exceeds maximum nesting depth")

    active_ids = _active_ids if _active_ids is not None else set()
    if isinstance(value, Mapping):
        mapping = _require_string_mapping_keys(value, path)
        value_id = id(value)
        if value_id in active_ids:
            raise ValueError(f"{path} contains a reference cycle")
        active_ids.add(value_id)
        try:
            return MappingProxyType(
                {
                    key: _deep_freeze(
                        mapping[key],
                        f"{path}.{key}",
                        _active_ids=active_ids,
                        _depth=_depth + 1,
                    )
                    for key in sorted(mapping)
                }
            )
        finally:
            active_ids.remove(value_id)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        value_id = id(value)
        if value_id in active_ids:
            raise ValueError(f"{path} contains a reference cycle")
        active_ids.add(value_id)
        try:
            return tuple(
                _deep_freeze(
                    item,
                    f"{path}[{index}]",
                    _active_ids=active_ids,
                    _depth=_depth + 1,
                )
                for index, item in enumerate(value)
            )
        finally:
            active_ids.remove(value_id)
    if isinstance(value, (set, frozenset)):
        value_id = id(value)
        if value_id in active_ids:
            raise ValueError(f"{path} contains a reference cycle")
        active_ids.add(value_id)
        try:
            frozen_items = tuple(
                _deep_freeze(
                    item,
                    f"{path}[{index}]",
                    _active_ids=active_ids,
                    _depth=_depth + 1,
                )
                for index, item in enumerate(value)
            )
            return tuple(sorted(frozen_items, key=_frozen_sort_key))
        finally:
            active_ids.remove(value_id)
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{path} must contain finite numbers")
    if isinstance(value, int) and not isinstance(value, bool):
        return _require_json_safe_integer(value, path)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise ValueError(
        f"{path} contains unsupported value type: {type(value).__name__}"
    )


def _frozen_sort_key(value: object) -> str:
    return json.dumps(
        _thaw_json_value(value),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )


def _thaw_json_value(value: object) -> AuditValue:
    if isinstance(value, Mapping):
        return {
            key: _thaw_json_value(value[key])
            for key in sorted(value)
        }
    if isinstance(value, tuple):
        return [_thaw_json_value(item) for item in value]
    return _audit_scalar(value, "value")


def _freeze_mapping(
    value: Mapping[str, object],
    field_name: str,
) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping")
    frozen = _deep_freeze(value, f"$.{field_name}")
    assert isinstance(frozen, Mapping)
    return frozen


def _require_nonblank_string(value: object, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path} must be a nonblank string")
    return value


def _require_optional_string(value: object, path: str) -> str | None:
    if value is None:
        return None
    return _require_nonblank_string(value, path)


def _require_bool(value: object, path: str) -> bool:
    if type(value) is not bool:
        raise ValueError(f"{path} must be a boolean")
    return value


def _require_int(
    value: object,
    path: str,
    *,
    minimum: int = 0,
) -> int:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{path} must be an integer >= {minimum}")
    return _require_json_safe_integer(value, path)


def _require_number(
    value: object,
    path: str,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{path} must be a finite number")
    if isinstance(value, int):
        number = float(_require_json_safe_integer(value, path))
    elif isinstance(value, float):
        number = value
    else:
        raise ValueError(f"{path} must be a finite number")
    if not math.isfinite(number):
        raise ValueError(f"{path} must be a finite number")
    if minimum is not None and number < minimum:
        raise ValueError(f"{path} must be >= {minimum}")
    if maximum is not None and number > maximum:
        raise ValueError(f"{path} must be <= {maximum}")
    return number


def _require_sha256(value: object, path: str) -> str:
    if not isinstance(value, str) or _SHA256_PATTERN.fullmatch(value) is None:
        raise ValueError(
            f"{path} must be a lowercase 64-character SHA-256 hex digest"
        )
    return value


def _require_utc_timestamp(value: object, path: str) -> str:
    if not isinstance(value, str) or _UTC_ISO8601_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{path} must use canonical UTC ISO-8601 syntax")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"{path} must be a valid UTC timestamp") from error
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise ValueError(f"{path} must include a UTC offset")
    return value


def _require_tuple(
    value: object,
    path: str,
    item_validator: Callable[[object, str], ValidatedValue],
) -> tuple[ValidatedValue, ...]:
    if not isinstance(value, Sequence) or isinstance(
        value,
        (str, bytes, bytearray),
    ):
        raise ValueError(f"{path} must be a deterministic sequence")
    return tuple(
        item_validator(item, f"{path}[{index}]")
        for index, item in enumerate(value)
    )


def _require_instance(
    expected_type: type[InstanceValue],
) -> Callable[[object, str], InstanceValue]:
    def validate(value: object, path: str) -> InstanceValue:
        if not isinstance(value, expected_type):
            raise ValueError(
                f"{path} must be {expected_type.__name__}"
            )
        return value

    return validate


def _require_mapping(value: object, path: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{path} must be a mapping")
    return value


def _audit_scalar(value: object, path: str) -> str | int | float | bool | None:
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, int):
        return _require_json_safe_integer(value, path)
    if isinstance(value, float) and math.isfinite(value):
        return value
    raise ValueError(f"{path} must contain only JSON-safe scalar values")


def _audit_sequence(value: object, path: str) -> list[AuditValue]:
    if not isinstance(value, tuple):
        raise ValueError(f"{path} must be a deterministic sequence")
    return [
        _require_nonblank_string(item, f"{path}[{index}]")
        for index, item in enumerate(value)
    ]


def _allowlisted_audit_mapping(
    value: Mapping[str, object],
    *,
    allowed_keys: frozenset[str],
    sequence_keys: frozenset[str] = frozenset(),
    field_name: str,
) -> dict[str, AuditValue]:
    mapping = _require_string_mapping_keys(value, f"$.{field_name}")
    unknown = set(mapping) - allowed_keys
    if unknown:
        raise ValueError(f"{field_name} contains unknown keys: {sorted(unknown)}")

    result: dict[str, AuditValue] = {}
    for key in sorted(mapping):
        item = mapping[key]
        if isinstance(item, Mapping):
            raise ValueError(f"{field_name}.{key} nested mappings are not allowed")
        if key in sequence_keys:
            result[key] = _audit_sequence(item, f"{field_name}.{key}")
        else:
            if isinstance(item, tuple):
                raise ValueError(f"{field_name}.{key} sequences are not allowed")
            result[key] = _audit_scalar(item, f"{field_name}.{key}")
    return result


def _audit_mapping_to_dict(
    value: Mapping[str, object],
    field_name: str,
) -> dict[str, AuditValue]:
    allowed_keys, sequence_keys = _AUDIT_MAPPING_CONTRACTS[field_name]
    return _allowlisted_audit_mapping(
        value,
        allowed_keys=allowed_keys,
        sequence_keys=sequence_keys,
        field_name=field_name,
    )


def _validate_and_freeze_allowlisted_mapping(
    value: Mapping[str, object],
    *,
    allowed_keys: frozenset[str],
    sequence_keys: frozenset[str] = frozenset(),
    field_name: str,
) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be a mapping")

    forbidden = _find_normalized_field(
        value,
        _NORMALIZED_GROUND_TRUTH_FIELDS,
        f"$.{field_name}",
    )
    if forbidden is not None:
        forbidden_name, path = forbidden
        raise ValueError(f"forbidden field '{forbidden_name}' at {path}")

    frozen = _freeze_mapping(value, field_name)
    _allowlisted_audit_mapping(
        frozen,
        allowed_keys=allowed_keys,
        sequence_keys=sequence_keys,
        field_name=field_name,
    )
    return frozen


def _validate_and_freeze_audit_mapping(
    value: Mapping[str, object],
    field_name: str,
) -> Mapping[str, object]:
    allowed_keys, sequence_keys = _AUDIT_MAPPING_CONTRACTS[field_name]
    return _validate_and_freeze_allowlisted_mapping(
        value,
        allowed_keys=allowed_keys,
        sequence_keys=sequence_keys,
        field_name=field_name,
    )


def _feature_sequence_keys(signal_type: str) -> frozenset[str]:
    contract = EVIDENCE_FEATURE_CONTRACTS[signal_type]
    return frozenset(
        key for key, rule in contract.items() if rule.endswith("_tuple")
    )


def _validate_feature_value(
    value: object,
    rule: FeatureRule,
    path: str,
) -> object:
    if isinstance(value, Mapping):
        raise ValueError(f"{path} nested mappings are not allowed")
    if rule in {"id", "string"}:
        return _require_nonblank_string(value, path)
    if rule == "timestamp":
        return _require_utc_timestamp(value, path)
    if rule == "sha256":
        return _require_sha256(value, path)
    if rule == "nonnegative_int":
        return _require_int(value, path)
    if rule == "positive_int":
        return _require_int(value, path, minimum=1)
    if rule == "nonnegative_number":
        return _require_number(value, path, minimum=0)
    if rule == "score":
        return _require_number(value, path, minimum=0, maximum=1)
    if rule == "similarity":
        return _require_number(value, path, minimum=-1, maximum=1)
    if rule == "finite_number":
        return _require_number(value, path)
    if rule in {"id_tuple", "string_tuple"}:
        return _require_tuple(value, path, _require_nonblank_string)
    raise RuntimeError(f"unknown evidence feature rule: {rule}")


def _validate_evidence_features(
    signal_type: str,
    features: object,
) -> Mapping[str, object]:
    if not isinstance(features, Mapping):
        raise ValueError("features must be a mapping")
    forbidden = _find_normalized_field(
        features,
        _NORMALIZED_GROUND_TRUTH_FIELDS,
        "$.features",
    )
    if forbidden is not None:
        forbidden_name, path = forbidden
        raise ValueError(f"forbidden field '{forbidden_name}' at {path}")

    feature_mapping = _require_string_mapping_keys(features, "$.features")
    contract = EVIDENCE_FEATURE_CONTRACTS[signal_type]
    unknown = set(feature_mapping) - set(contract)
    if unknown:
        raise ValueError(f"features contains unknown keys: {sorted(unknown)}")

    return MappingProxyType(
        {
            key: _validate_feature_value(
                feature_mapping[key],
                contract[key],
                f"features.{key}",
            )
            for key in sorted(feature_mapping)
        }
    )


def _validate_trust_signal_summary(
    summary: Mapping[str, object],
) -> None:
    signal_count = _require_int(
        summary.get("signal_count", 0),
        "trust_signal_summary.signal_count",
    )
    has_signal_types = "signal_types" in summary
    has_method_versions = "method_versions" in summary
    if has_signal_types != has_method_versions:
        raise ValueError(
            "trust_signal_summary signal_types and method_versions "
            "must be present together"
        )

    signal_types: tuple[str, ...] = ()
    method_versions: tuple[str, ...] = ()
    if has_signal_types:
        signal_types = _require_tuple(
            summary["signal_types"],
            "trust_signal_summary.signal_types",
            _require_nonblank_string,
        )
        unknown = set(signal_types) - set(EVIDENCE_FEATURE_CONTRACTS)
        if unknown:
            raise ValueError(f"unknown signal types: {sorted(unknown)}")
        method_versions = _require_tuple(
            summary["method_versions"],
            "trust_signal_summary.method_versions",
            _require_nonblank_string,
        )

    if signal_count != len(signal_types) or signal_count != len(method_versions):
        raise ValueError(
            "trust_signal_summary signal_count must equal the lengths of "
            "signal_types and method_versions"
        )
    if "aggregate_score" in summary and summary["aggregate_score"] is not None:
        raise ValueError("pass-through summary cannot claim aggregate_score")
    if "ranking_changed" in summary:
        ranking_changed = _require_bool(
            summary["ranking_changed"],
            "trust_signal_summary.ranking_changed",
        )
        if ranking_changed:
            raise ValueError("pass-through summary cannot change ranking")
    if "blocked_doc_ids" in summary:
        blocked_doc_ids = _require_tuple(
            summary["blocked_doc_ids"],
            "trust_signal_summary.blocked_doc_ids",
            _require_nonblank_string,
        )
        if blocked_doc_ids:
            raise ValueError("pass-through summary cannot block documents")


@dataclass(frozen=True)
class DocumentRecord:
    doc_id: str
    content: str
    source_id: str
    source_type: str
    timestamp: str
    version: str
    content_hash: str

    def __post_init__(self) -> None:
        _require_nonblank_string(self.doc_id, "doc_id")
        _require_nonblank_string(self.content, "content")
        _require_nonblank_string(self.source_id, "source_id")
        _require_nonblank_string(self.source_type, "source_type")
        _require_utc_timestamp(self.timestamp, "timestamp")
        _require_nonblank_string(self.version, "version")
        _require_sha256(self.content_hash, "content_hash")


@dataclass(frozen=True)
class QueryRecord:
    query_id: str
    attack_id: str | None
    category: str
    retrieval_query: str
    generation_question: str
    expected_clean_doc_ids: tuple[str, ...]
    metadata: Mapping[str, object]

    def __post_init__(self) -> None:
        _require_nonblank_string(self.query_id, "query_id")
        _require_optional_string(self.attack_id, "attack_id")
        _require_nonblank_string(self.category, "category")
        _require_nonblank_string(self.retrieval_query, "retrieval_query")
        _require_nonblank_string(
            self.generation_question,
            "generation_question",
        )
        expected_clean_doc_ids = _require_tuple(
            self.expected_clean_doc_ids,
            "expected_clean_doc_ids",
            _require_nonblank_string,
        )
        if not isinstance(self.metadata, Mapping):
            raise ValueError("metadata must be a mapping")
        forbidden = _find_forbidden_pipeline_field(self.metadata, "$.metadata")
        if forbidden is not None:
            field_name, path = forbidden
            raise ValueError(f"forbidden field '{field_name}' at {path}")
        object.__setattr__(
            self,
            "expected_clean_doc_ids",
            expected_clean_doc_ids,
        )
        object.__setattr__(
            self,
            "metadata",
            _freeze_mapping(self.metadata, "metadata"),
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class RetrievalEvidence:
    """Chunk-level retrieval result with no query or plaintext content."""

    evidence_schema_version: str
    evidence_uid: str
    query_id: str
    retrieval_request_id: str
    corpus_snapshot_id: str
    doc_id: str
    chunk_id: str
    parent_doc_id: str
    content_ref: str = field(repr=False)
    content_hash: str
    source_id: str
    source_type: str
    version: str
    timestamp: str
    rank: int
    distance: float
    similarity: float
    collection_fingerprint: str
    public_metadata: Mapping[str, object]

    def __post_init__(self) -> None:
        require_public_identifier(self.evidence_schema_version, "evidence_schema_version")
        expected_uid = derive_evidence_uid(
            evidence_schema_version=self.evidence_schema_version,
            corpus_snapshot_id=self.corpus_snapshot_id,
            chunk_id=self.chunk_id,
            content_hash=self.content_hash,
        )
        if self.evidence_uid != expected_uid:
            raise RetrievalIntegrityError("evidence identity mismatch", error_code="EVIDENCE_UID_MISMATCH")
        require_public_query_id(self.query_id)
        require_public_identifier(self.retrieval_request_id, "retrieval_request_id")
        require_public_identifier(self.corpus_snapshot_id, "corpus_snapshot_id")
        require_chunk_id(self.chunk_id)
        if self.doc_id != self.chunk_id:
            raise RetrievalInputError("doc_id must equal chunk_id for canonical evidence")
        require_public_identifier(self.parent_doc_id, "parent_doc_id")
        content_ref = ContentRef(self.content_ref)
        if content_ref.scheme != "corpus" or content_ref.corpus_snapshot_id != self.corpus_snapshot_id or content_ref.chunk_id != self.chunk_id:
            raise RetrievalIntegrityError("canonical content reference mismatch", error_code="INVALID_CONTENT_REF")
        require_sha256(self.content_hash, "content_hash")
        require_public_identifier(self.source_id, "source_id")
        require_public_identifier(self.source_type, "source_type")
        require_public_identifier(self.version, "version")
        _require_utc_timestamp(self.timestamp, "timestamp")
        _require_int(self.rank, "rank", minimum=1)
        distance = _require_retrieval_metric(self.distance, minimum=0)
        similarity = _require_retrieval_metric(self.similarity, minimum=-1, maximum=1)
        require_sha256(self.collection_fingerprint, "collection_fingerprint")
        object.__setattr__(self, "distance", distance)
        object.__setattr__(self, "similarity", similarity)
        object.__setattr__(self, "content_ref", content_ref)
        object.__setattr__(self, "public_metadata", freeze_public_metadata(self.public_metadata))

    def to_summary(self) -> object:
        from .retrieval import RetrievalEvidenceSummary

        return RetrievalEvidenceSummary.from_evidence(self)

    def to_audit_dict(self) -> dict[str, AuditValue]:
        return {
            "evidence_schema_version": self.evidence_schema_version,
            "evidence_uid": self.evidence_uid,
            "query_id": self.query_id,
            "retrieval_request_id": self.retrieval_request_id,
            "corpus_snapshot_id": self.corpus_snapshot_id,
            "doc_id": self.doc_id,
            "chunk_id": self.chunk_id,
            "parent_doc_id": self.parent_doc_id,
            "content_hash": self.content_hash,
            "source_id": self.source_id,
            "source_type": self.source_type,
            "version": self.version,
            "timestamp": self.timestamp,
            "rank": self.rank,
            "distance": self.distance,
            "similarity": self.similarity,
            "collection_fingerprint": self.collection_fingerprint,
            "public_metadata": cast(dict[str, AuditValue], thaw_public_metadata(self.public_metadata)),
        }


def _require_retrieval_metric(
    value: object,
    *,
    minimum: float,
    maximum: float | None = None,
) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise RetrievalInputError("distance or similarity is an invalid retrieval metric", error_code="INVALID_RETRIEVAL_METRIC")
    try:
        number = float(value)
    except OverflowError as error:
        raise RetrievalInputError("distance or similarity is an invalid retrieval metric", error_code="INVALID_RETRIEVAL_METRIC") from error
    if not math.isfinite(number) or number < minimum or (maximum is not None and number > maximum):
        raise RetrievalInputError("distance or similarity is an invalid retrieval metric", error_code="INVALID_RETRIEVAL_METRIC")
    return number


@dataclass(frozen=True)
class EvidenceSignal:
    signal_type: str
    query_id: str
    doc_ids: tuple[str, ...]
    value: float
    features: Mapping[str, object]
    method_version: str
    evidence_hash: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.signal_type, str)
            or self.signal_type not in EVIDENCE_FEATURE_CONTRACTS
        ):
            raise ValueError(f"unknown signal_type: {self.signal_type}")
        _require_nonblank_string(self.query_id, "query_id")
        object.__setattr__(
            self,
            "doc_ids",
            _require_tuple(
                self.doc_ids,
                "doc_ids",
                _require_nonblank_string,
            ),
        )
        object.__setattr__(
            self,
            "value",
            _require_number(self.value, "value", minimum=0, maximum=1),
        )
        object.__setattr__(
            self,
            "features",
            _validate_evidence_features(
                self.signal_type,
                self.features,
            ),
        )
        _require_nonblank_string(self.method_version, "method_version")
        _require_sha256(self.evidence_hash, "evidence_hash")

    def to_audit_dict(self) -> dict[str, AuditValue]:
        return {
            "signal_type": self.signal_type,
            "query_id": self.query_id,
            "doc_ids": list(self.doc_ids),
            "value": self.value,
            "features": _allowlisted_audit_mapping(
                self.features,
                allowed_keys=EVIDENCE_FEATURE_ALLOWLISTS[self.signal_type],
                sequence_keys=_feature_sequence_keys(self.signal_type),
                field_name="features",
            ),
            "method_version": self.method_version,
            "evidence_hash": self.evidence_hash,
        }


@dataclass(frozen=True)
class TrustAssessment:
    mode: str
    aggregate_score: float | None
    ranking_changed: bool
    blocked_doc_ids: tuple[str, ...]
    signals: tuple[EvidenceSignal, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.mode, str) or self.mode not in {"off", "observe"}:
            raise ValueError("mode must be 'off' or 'observe'")
        if self.aggregate_score is not None:
            raise ValueError("Stage 6 aggregate_score must be None")
        _require_bool(self.ranking_changed, "ranking_changed")
        blocked_doc_ids = _require_tuple(
            self.blocked_doc_ids,
            "blocked_doc_ids",
            _require_nonblank_string,
        )
        signals = _require_tuple(
            self.signals,
            "signals",
            _require_instance(EvidenceSignal),
        )
        object.__setattr__(self, "blocked_doc_ids", blocked_doc_ids)
        object.__setattr__(self, "signals", signals)

        if self.ranking_changed is not False:
            raise ValueError("Stage 6 ranking_changed must be False")
        if blocked_doc_ids:
            raise ValueError("Stage 6 blocked_doc_ids must be empty")
        if self.mode == "off" and signals:
            raise ValueError("off mode must not contain signals")

    @classmethod
    def off(cls) -> TrustAssessment:
        return cls(
            mode="off",
            aggregate_score=None,
            ranking_changed=False,
            blocked_doc_ids=(),
            signals=(),
        )

    @classmethod
    def observe(cls, signals: Sequence[EvidenceSignal]) -> TrustAssessment:
        return cls(
            mode="observe",
            aggregate_score=None,
            ranking_changed=False,
            blocked_doc_ids=(),
            signals=tuple(signals),
        )


@dataclass(frozen=True)
class RAGAttemptRecord:
    attempt_id: str
    run_id: str
    query_id: str
    attack_id: str | None
    guard_mode: str
    retrieval_policy: str
    retrieval_evidence: tuple[RetrievalEvidence, ...]
    evidence_signals: tuple[EvidenceSignal, ...]
    context_hash: str
    context_length: int
    generator: Mapping[str, object]
    final_answer_hash: str
    final_answer_length: int
    detector_results: tuple[Mapping[str, object], ...]
    metrics: Mapping[str, object]
    failure_types: tuple[str, ...]
    latency: Mapping[str, object]
    validation_status: Mapping[str, object]

    def __post_init__(self) -> None:
        _require_nonblank_string(self.attempt_id, "attempt_id")
        _require_nonblank_string(self.run_id, "run_id")
        _require_nonblank_string(self.query_id, "query_id")
        _require_optional_string(self.attack_id, "attack_id")
        _require_nonblank_string(self.guard_mode, "guard_mode")
        if (
            not isinstance(self.retrieval_policy, str)
            or self.retrieval_policy not in {"off", "observe"}
        ):
            raise ValueError("retrieval_policy must be 'off' or 'observe'")
        retrieval_evidence = _require_tuple(
            self.retrieval_evidence,
            "retrieval_evidence",
            _require_instance(RetrievalEvidence),
        )
        evidence_signals = _require_tuple(
            self.evidence_signals,
            "evidence_signals",
            _require_instance(EvidenceSignal),
        )
        if self.retrieval_policy == "off" and evidence_signals:
            raise ValueError("off retrieval_policy requires empty evidence_signals")
        _require_sha256(self.context_hash, "context_hash")
        _require_int(self.context_length, "context_length")
        _require_sha256(self.final_answer_hash, "final_answer_hash")
        _require_int(self.final_answer_length, "final_answer_length")
        detector_results = _require_tuple(
            self.detector_results,
            "detector_results",
            _require_mapping,
        )
        failure_types = _require_tuple(
            self.failure_types,
            "failure_types",
            _require_nonblank_string,
        )
        object.__setattr__(
            self,
            "retrieval_evidence",
            retrieval_evidence,
        )
        object.__setattr__(
            self,
            "evidence_signals",
            evidence_signals,
        )
        object.__setattr__(self, "failure_types", failure_types)
        object.__setattr__(
            self,
            "generator",
            _validate_and_freeze_audit_mapping(self.generator, "generator"),
        )
        object.__setattr__(
            self,
            "detector_results",
            tuple(
                _validate_and_freeze_audit_mapping(
                    result,
                    "detector_results item",
                )
                for result in detector_results
            ),
        )
        object.__setattr__(
            self,
            "metrics",
            _validate_and_freeze_audit_mapping(self.metrics, "metrics"),
        )
        object.__setattr__(
            self,
            "latency",
            _validate_and_freeze_audit_mapping(self.latency, "latency"),
        )
        object.__setattr__(
            self,
            "validation_status",
            _validate_and_freeze_audit_mapping(
                self.validation_status,
                "validation_status",
            ),
        )

    def to_audit_dict(self) -> dict[str, AuditValue]:
        return {
            "attempt_id": self.attempt_id,
            "run_id": self.run_id,
            "query_id": self.query_id,
            "attack_id": self.attack_id,
            "guard_mode": self.guard_mode,
            "retrieval_policy": self.retrieval_policy,
            "retrieval_evidence": [
                item.to_audit_dict() for item in self.retrieval_evidence
            ],
            "evidence_signals": [
                item.to_audit_dict() for item in self.evidence_signals
            ],
            "context_hash": self.context_hash,
            "context_length": self.context_length,
            "generator": _audit_mapping_to_dict(
                self.generator,
                "generator",
            ),
            "final_answer_hash": self.final_answer_hash,
            "final_answer_length": self.final_answer_length,
            "detector_results": [
                _audit_mapping_to_dict(
                    result,
                    "detector_results item",
                )
                for result in self.detector_results
            ],
            "metrics": _audit_mapping_to_dict(
                self.metrics,
                "metrics",
            ),
            "failure_types": list(self.failure_types),
            "latency": _audit_mapping_to_dict(
                self.latency,
                "latency",
            ),
            "validation_status": _audit_mapping_to_dict(
                self.validation_status,
                "validation_status",
            ),
        }


@dataclass(frozen=True)
class RAGSecurityEnvelope:
    query_id: str
    retrieved_doc_ids: tuple[str, ...]
    evidence_hashes: tuple[str, ...]
    trust_signal_summary: Mapping[str, object]
    retrieval_policy: str
    failure_types: tuple[str, ...]
    context_hash: str
    final_answer_hash: str
    run_id: str

    def __post_init__(self) -> None:
        _require_nonblank_string(self.query_id, "query_id")
        _require_nonblank_string(self.run_id, "run_id")
        if (
            not isinstance(self.retrieval_policy, str)
            or self.retrieval_policy not in {"off", "observe"}
        ):
            raise ValueError("retrieval_policy must be 'off' or 'observe'")
        retrieved_doc_ids = _require_tuple(
            self.retrieved_doc_ids,
            "retrieved_doc_ids",
            _require_nonblank_string,
        )
        evidence_hashes = _require_tuple(
            self.evidence_hashes,
            "evidence_hashes",
            _require_sha256,
        )
        failure_types = _require_tuple(
            self.failure_types,
            "failure_types",
            _require_nonblank_string,
        )
        _require_sha256(self.context_hash, "context_hash")
        _require_sha256(self.final_answer_hash, "final_answer_hash")
        trust_signal_summary = _validate_and_freeze_audit_mapping(
            self.trust_signal_summary,
            "trust_signal_summary",
        )
        _validate_trust_signal_summary(trust_signal_summary)

        if len(retrieved_doc_ids) != len(evidence_hashes):
            raise ValueError(
                "retrieved_doc_ids and evidence_hashes must have equal lengths"
            )

        if self.retrieval_policy == "off":
            if trust_signal_summary.get("signal_count", 0) != 0:
                raise ValueError("off retrieval_policy requires zero signals")
            for key in ("signal_types", "method_versions"):
                if trust_signal_summary.get(key, ()):
                    raise ValueError(
                        f"off retrieval_policy requires empty {key}"
                    )

        object.__setattr__(
            self,
            "retrieved_doc_ids",
            retrieved_doc_ids,
        )
        object.__setattr__(
            self,
            "evidence_hashes",
            evidence_hashes,
        )
        object.__setattr__(self, "failure_types", failure_types)
        object.__setattr__(
            self,
            "trust_signal_summary",
            trust_signal_summary,
        )

    def to_audit_dict(self) -> dict[str, AuditValue]:
        return {
            "query_id": self.query_id,
            "retrieved_doc_ids": list(self.retrieved_doc_ids),
            "evidence_hashes": list(self.evidence_hashes),
            "trust_signal_summary": _audit_mapping_to_dict(
                self.trust_signal_summary,
                "trust_signal_summary",
            ),
            "retrieval_policy": self.retrieval_policy,
            "failure_types": list(self.failure_types),
            "context_hash": self.context_hash,
            "final_answer_hash": self.final_answer_hash,
            "run_id": self.run_id,
        }
