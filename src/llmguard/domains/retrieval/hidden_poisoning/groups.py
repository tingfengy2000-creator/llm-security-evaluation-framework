"""Transitive independence-group construction for Pilot0 records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .schema import SCHEMA_VERSION, CanonicalRecord, SchemaValidationError, canonical_sha256


@dataclass(frozen=True, slots=True, kw_only=True)
class GroupIdentityRecord(CanonicalRecord):
    record_id: str
    entity_id: str
    claim_family: str
    version_chain_id: str
    source_document_family: str
    mutation_template_family: str
    near_duplicate_cluster: str
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        values = self.identity_values()
        if not self.record_id or any(not value for value in values):
            raise SchemaValidationError("group identity fields must not be empty")
        if self.schema_version != SCHEMA_VERSION:
            raise SchemaValidationError("unsupported schema_version")

    def identity_values(self) -> tuple[str, ...]:
        return (
            self.entity_id,
            self.claim_family,
            self.version_chain_id,
            self.source_document_family,
            self.mutation_template_family,
            self.near_duplicate_cluster,
        )


def build_independence_groups(
    records: Iterable[GroupIdentityRecord],
) -> dict[str, str]:
    ordered = sorted(records, key=lambda item: item.record_id)
    if len({item.record_id for item in ordered}) != len(ordered):
        raise SchemaValidationError("record_id must be unique")
    parent = {item.record_id: item.record_id for item in ordered}

    def find(item: str) -> str:
        while parent[item] != item:
            parent[item] = parent[parent[item]]
            item = parent[item]
        return item

    def union(left: str, right: str) -> None:
        left_root, right_root = find(left), find(right)
        if left_root == right_root:
            return
        low, high = sorted((left_root, right_root))
        parent[high] = low

    owners: dict[tuple[int, str], str] = {}
    for item in ordered:
        for index, value in enumerate(item.identity_values()):
            key = (index, value)
            existing = owners.get(key)
            if existing is None:
                owners[key] = item.record_id
            else:
                union(existing, item.record_id)

    members: dict[str, list[str]] = {}
    for item in ordered:
        members.setdefault(find(item.record_id), []).append(item.record_id)
    group_ids = {
        root: "IG-" + canonical_sha256(sorted(group_members))[:24]
        for root, group_members in members.items()
    }
    return {item.record_id: group_ids[find(item.record_id)] for item in ordered}


__all__ = ["GroupIdentityRecord", "build_independence_groups"]
