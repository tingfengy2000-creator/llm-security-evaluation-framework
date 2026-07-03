from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import TypeVar

from codeguarder.stage6_rag.attacks.attack_renderer import render_query_record
from codeguarder.stage6_rag.contracts import (
    DocumentRecord,
    QueryRecord,
    validate_document,
)

RecordValue = TypeVar("RecordValue")


@dataclass(frozen=True)
class AttackDefinition:
    category: str
    name: str
    delivery_layer: str = "retrieval"
    sample_count: int = 2


ATTACK_MATRIX: Mapping[str, AttackDefinition] = MappingProxyType(
    {
        "R1": AttackDefinition("R1", "retrieval query manipulation"),
        "R2": AttackDefinition("R2", "keyword-stuffed document"),
        "R3": AttackDefinition("R3", "authority impersonation"),
        "R4": AttackDefinition("R4", "instruction-like context"),
        "R5": AttackDefinition("R5", "semantic contradiction"),
        "R6": AttackDefinition("R6", "cross-document context steering"),
    }
)


@dataclass(frozen=True)
class PublicRAGDataset:
    queries: tuple[QueryRecord, ...]
    documents: tuple[DocumentRecord, ...]

    def __post_init__(self) -> None:
        queries = tuple(self.queries)
        documents = tuple(self.documents)
        _require_instances(queries, QueryRecord, "queries")
        _require_instances(documents, DocumentRecord, "documents")
        _reject_duplicate_ids(
            (query.query_id for query in queries),
            "query_id",
        )
        _reject_duplicate_ids(
            (document.doc_id for document in documents),
            "doc_id",
        )
        object.__setattr__(self, "queries", queries)
        object.__setattr__(self, "documents", documents)


@dataclass(frozen=True)
class EvaluationGroundTruth:
    query_labels: Mapping[str, Mapping[str, object]]
    document_labels: Mapping[str, Mapping[str, object]]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "query_labels",
            _freeze_label_mapping(self.query_labels, "query_id"),
        )
        object.__setattr__(
            self,
            "document_labels",
            _freeze_label_mapping(self.document_labels, "doc_id"),
        )


@dataclass(frozen=True)
class LoadedRAGDataset:
    public: PublicRAGDataset
    ground_truth: EvaluationGroundTruth | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.public, PublicRAGDataset):
            raise ValueError("public must be a PublicRAGDataset")
        if self.ground_truth is not None and not isinstance(
            self.ground_truth,
            EvaluationGroundTruth,
        ):
            raise ValueError("ground_truth must be an EvaluationGroundTruth or None")


def load_public_dataset(root: str | Path) -> PublicRAGDataset:
    """Load retriever-visible records without opening evaluator-only paths."""
    data_root = Path(root)
    query_paths = (
        "queries/attack_queries.jsonl",
        "queries/benign_queries.jsonl",
    )
    document_paths = (
        "documents/clean_docs.jsonl",
        "documents/poisoned_docs.jsonl",
    )
    query_files = {
        relative_path: _load_jsonl(
            data_root / relative_path,
            render_query_record,
        )
        for relative_path in query_paths
    }
    document_files = {
        relative_path: _load_jsonl(
            data_root / relative_path,
            validate_document,
        )
        for relative_path in document_paths
    }
    raw_files: dict[str, Sequence[object]] = {}
    raw_files.update(query_files)
    raw_files.update(document_files)

    queries = tuple(
        record for relative_path in query_paths for record in query_files[relative_path]
    )
    documents = tuple(
        record
        for relative_path in document_paths
        for record in document_files[relative_path]
    )
    dataset = PublicRAGDataset(queries=queries, documents=documents)
    _validate_public_coverage(dataset)
    _validate_manifest(data_root, raw_files)
    return dataset


def load_evaluation_ground_truth(root: str | Path) -> EvaluationGroundTruth:
    data_root = Path(root)
    query_records = _load_jsonl(
        data_root / "ground_truth" / "query_labels.jsonl",
        _validate_query_label,
    )
    document_records = _load_jsonl(
        data_root / "ground_truth" / "document_labels.jsonl",
        _validate_document_label,
    )
    query_labels = _index_labels(
        query_records,
        "query_id",
        {
            "query_id",
            "attack_id",
            "category",
            "risk_goal",
            "expected_behavior",
        },
    )
    document_labels = _index_labels(
        document_records,
        "doc_id",
        {
            "doc_id",
            "poisoned",
            "attack_id",
            "attack_goal",
        },
    )
    return EvaluationGroundTruth(
        query_labels=query_labels,
        document_labels=document_labels,
    )


def load_dataset(
    root: str | Path,
    *,
    include_ground_truth: bool = False,
) -> LoadedRAGDataset:
    public = load_public_dataset(root)
    if not include_ground_truth:
        return LoadedRAGDataset(public=public)
    ground_truth = load_evaluation_ground_truth(root)
    _validate_ground_truth_references(public, ground_truth)
    return LoadedRAGDataset(public=public, ground_truth=ground_truth)


def _load_jsonl(
    path: Path,
    validator: Callable[[Mapping[str, object]], RecordValue],
) -> tuple[RecordValue, ...]:
    records: list[RecordValue] = []
    with path.open("r", encoding="utf-8", newline="") as input_file:
        for line_number, line in enumerate(input_file, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line, object_pairs_hook=_unique_object)
            except (json.JSONDecodeError, ValueError) as error:
                raise ValueError(f"{path}:{line_number}: {error}") from error
            if not isinstance(value, dict):
                raise ValueError(
                    f"{path}:{line_number}: JSONL record must be an object"
                )
            try:
                records.append(validator(value))
            except ValueError as error:
                raise ValueError(f"{path}:{line_number}: {error}") from error
    return tuple(records)


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _validate_manifest(
    root: Path,
    raw_files: Mapping[str, Sequence[object]],
) -> None:
    manifest_path = root / "documents" / "corpus_manifest.json"
    with manifest_path.open("r", encoding="utf-8") as manifest_file:
        try:
            manifest = json.load(manifest_file, object_pairs_hook=_unique_object)
        except (json.JSONDecodeError, ValueError) as error:
            raise ValueError(f"{manifest_path}: {error}") from error
    if not isinstance(manifest, dict):
        raise ValueError("corpus manifest must be an object")
    if set(manifest) != {
        "schema_version",
        "data_version",
        "files",
        "provenance",
    }:
        raise ValueError("corpus manifest has an unexpected schema")
    if manifest["schema_version"] != "1.0.0":
        raise ValueError("unsupported corpus manifest schema_version")
    files = manifest["files"]
    if not isinstance(files, dict) or set(files) != set(raw_files):
        raise ValueError("corpus manifest file coverage mismatch")
    for relative_path, records in raw_files.items():
        entry = files[relative_path]
        if not isinstance(entry, dict) or set(entry) != {"sha256", "count"}:
            raise ValueError(f"invalid manifest entry: {relative_path}")
        physical_path = root / relative_path
        digest = hashlib.sha256(physical_path.read_bytes()).hexdigest()
        if entry["sha256"] != digest:
            raise ValueError(f"manifest hash mismatch: {relative_path}")
        if entry["count"] != len(records):
            raise ValueError(f"manifest count mismatch: {relative_path}")


def _validate_public_coverage(dataset: PublicRAGDataset) -> None:
    attacks = tuple(query for query in dataset.queries if query.attack_id)
    benign = tuple(query for query in dataset.queries if query.attack_id is None)
    expected_query_ids = {
        f"R{category}-Q{sample:02d}"
        for category in range(1, 7)
        for sample in range(1, 3)
    }
    expected_attack_ids = {
        f"R{category}-A{sample:02d}"
        for category in range(1, 7)
        for sample in range(1, 3)
    }
    if {query.query_id for query in attacks} != expected_query_ids:
        raise ValueError("attack query ID coverage mismatch")
    if {query.attack_id for query in attacks} != expected_attack_ids:
        raise ValueError("attack ID coverage mismatch")
    if {query.query_id for query in benign} != {
        f"B-Q{sample:02d}" for sample in range(1, 11)
    }:
        raise ValueError("benign query ID coverage mismatch")
    category_counts = {
        category: sum(query.category == category for query in attacks)
        for category in ATTACK_MATRIX
    }
    if any(count != 2 for count in category_counts.values()):
        raise ValueError("each attack category must have exactly two samples")

    clean_ids = {
        document.doc_id
        for document in dataset.documents
        if document.doc_id.startswith("C-")
    }
    attack_ids = {
        document.doc_id
        for document in dataset.documents
        if document.doc_id.startswith("P-R")
    }
    if len(clean_ids) < 18 or len(attack_ids) != 10:
        raise ValueError("document coverage mismatch")
    for query in dataset.queries:
        if not query.expected_clean_doc_ids:
            raise ValueError(f"{query.query_id} has no expected clean documents")
        if not set(query.expected_clean_doc_ids) <= clean_ids:
            raise ValueError(f"{query.query_id} references an unknown clean document")
    for document in dataset.documents:
        digest = hashlib.sha256(document.content.encode("utf-8")).hexdigest()
        if document.content_hash != digest:
            raise ValueError(f"content_hash mismatch: {document.doc_id}")


def _validate_query_label(
    record: Mapping[str, object],
) -> Mapping[str, object]:
    expected_fields = {
        "query_id",
        "attack_id",
        "category",
        "risk_goal",
        "expected_behavior",
    }
    if set(record) != expected_fields:
        raise ValueError("query label has an unexpected schema")
    _require_nonblank_label_string(record["query_id"], "query_id")
    attack_id = record["attack_id"]
    if attack_id is not None:
        _require_nonblank_label_string(attack_id, "attack_id")
    _require_nonblank_label_string(record["category"], "category")
    _require_nonblank_label_string(record["risk_goal"], "risk_goal")
    expected_behavior = record["expected_behavior"]
    if not isinstance(expected_behavior, Sequence) or isinstance(
        expected_behavior,
        (str, bytes, bytearray),
    ):
        raise ValueError("expected_behavior must be a sequence")
    for index, item in enumerate(expected_behavior):
        _require_nonblank_label_string(
            item,
            f"expected_behavior[{index}]",
        )
    return record


def _validate_document_label(
    record: Mapping[str, object],
) -> Mapping[str, object]:
    expected_fields = {
        "doc_id",
        "poisoned",
        "attack_id",
        "attack_goal",
    }
    if set(record) != expected_fields:
        raise ValueError("document label has an unexpected schema")
    _require_nonblank_label_string(record["doc_id"], "doc_id")
    if type(record["poisoned"]) is not bool:
        raise ValueError("poisoned must be a boolean")
    for field_name in ("attack_id", "attack_goal"):
        value = record[field_name]
        if value is not None:
            _require_nonblank_label_string(value, field_name)
    return record


def _require_nonblank_label_string(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonblank string")
    return value


def _index_labels(
    records: Sequence[Mapping[str, object]],
    id_field: str,
    expected_fields: set[str],
) -> dict[str, Mapping[str, object]]:
    indexed: dict[str, Mapping[str, object]] = {}
    for record in records:
        if set(record) != expected_fields:
            raise ValueError(f"{id_field} label has an unexpected schema")
        record_id = record[id_field]
        if not isinstance(record_id, str) or not record_id.strip():
            raise ValueError(f"{id_field} must be a nonblank string")
        if record_id in indexed:
            raise ValueError(f"duplicate {id_field}: {record_id}")
        indexed[record_id] = record
    return indexed


def _validate_ground_truth_references(
    public: PublicRAGDataset,
    ground_truth: EvaluationGroundTruth,
) -> None:
    queries = {query.query_id: query for query in public.queries}
    documents = {document.doc_id: document for document in public.documents}
    attack_ids = {
        query.attack_id for query in public.queries if query.attack_id is not None
    }
    if set(ground_truth.query_labels) != set(queries):
        raise ValueError("query label coverage mismatch")
    if set(ground_truth.document_labels) != set(documents):
        raise ValueError("document label coverage mismatch")
    for query_id, query in queries.items():
        label = ground_truth.query_labels[query_id]
        if label["attack_id"] != query.attack_id:
            raise ValueError(f"query attack_id mismatch: {query_id}")
        if label["category"] != query.category:
            raise ValueError(f"query category mismatch: {query_id}")
    for doc_id in documents:
        label = ground_truth.document_labels[doc_id]
        is_attack_document = doc_id.startswith("P-R")
        if label["poisoned"] is not is_attack_document:
            raise ValueError(f"document classification mismatch: {doc_id}")
        attack_id = label["attack_id"]
        if attack_id is not None and attack_id not in attack_ids:
            raise ValueError(f"document attack_id mismatch: {doc_id}")


def _require_instances(
    values: Sequence[object],
    expected_type: type[object],
    field_name: str,
) -> None:
    if not all(isinstance(value, expected_type) for value in values):
        raise ValueError(
            f"{field_name} must contain only {expected_type.__name__} values"
        )


def _reject_duplicate_ids(values: Iterable[str], field_name: str) -> None:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            raise ValueError(f"duplicate {field_name}: {value}")
        seen.add(value)


def _freeze_label_mapping(
    labels: Mapping[str, Mapping[str, object]],
    id_field: str,
) -> Mapping[str, Mapping[str, object]]:
    if not isinstance(labels, Mapping):
        raise ValueError("labels must be a mapping")
    frozen: dict[str, Mapping[str, object]] = {}
    for key in sorted(labels):
        value = labels[key]
        if not isinstance(key, str) or not isinstance(value, Mapping):
            raise ValueError("label entries must map string IDs to mappings")
        if value.get(id_field) != key:
            raise ValueError(f"{id_field} label key mismatch: {key}")
        frozen_value = _deep_freeze(value)
        assert isinstance(frozen_value, Mapping)
        frozen[key] = frozen_value
    return MappingProxyType(frozen)


def _deep_freeze(value: object) -> object:
    if isinstance(value, Mapping):
        if not all(isinstance(key, str) for key in value):
            raise ValueError("label mapping keys must be strings")
        return MappingProxyType(
            {key: _deep_freeze(value[key]) for key in sorted(value)}
        )
    if isinstance(value, Sequence) and not isinstance(
        value,
        (str, bytes, bytearray),
    ):
        return tuple(_deep_freeze(item) for item in value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise ValueError(f"unsupported label value: {type(value).__name__}")
