"""Field-level HKP mutation descriptions; no natural-language generation."""

from __future__ import annotations

from dataclasses import dataclass

from .schema import AttackType, SCHEMA_VERSION, CanonicalRecord, SchemaValidationError


_COMMON_IDENTITY_FIELDS = frozenset({"record_id", "entity_id", "claim_family"})
ALLOWED_CHANGED_FIELDS: dict[AttackType, frozenset[str]] = {
    AttackType.HKP_1_NUMERIC_ENTITY: frozenset(
        {"numeric_value", "object_value", "entity_attribute", "unit"}
    ),
    AttackType.HKP_2_CONDITION_EXCEPTION: frozenset(
        {"conditions", "exceptions", "applicability_scope"}
    ),
    AttackType.HKP_3_TEMPORAL_VERSION: frozenset(
        {
            "effective_at",
            "expires_at",
            "repealed_at",
            "predecessor_record_id",
            "successor_record_id",
            "supersedes",
            "amends",
        }
    ),
    AttackType.HKP_4_PROVENANCE_AUTHORITY: frozenset(
        {
            "source_id",
            "source_type",
            "authority_level",
            "jurisdiction",
            "department",
            "citation_reference",
        }
    ),
}


@dataclass(frozen=True, slots=True, kw_only=True)
class MutationSpec(CanonicalRecord):
    attack_type: AttackType
    changed_fields: tuple[str, ...]
    preserved_fields: tuple[str, ...]
    source_record_id: str
    mutation_id: str
    expected_fact_change: str
    retrieval_relevance_constraint: str
    fluency_review_required: bool
    stealth_review_required: bool
    schema_version: str = SCHEMA_VERSION

    @property
    def semantic_attack_type(self) -> AttackType:
        """Expose the attack class determined by mutation semantics."""

        return self.attack_type

    def __post_init__(self) -> None:
        if not isinstance(self.attack_type, AttackType):
            raise SchemaValidationError("attack_type must be canonical")
        if not self.changed_fields:
            raise SchemaValidationError("changed_fields must not be empty")
        if not self.source_record_id or not self.mutation_id:
            raise SchemaValidationError("source_record_id and mutation_id are required")
        if not self.expected_fact_change or not self.retrieval_relevance_constraint:
            raise SchemaValidationError("mutation review contracts are required")
        overlap = set(self.changed_fields) & set(self.preserved_fields)
        if overlap:
            raise SchemaValidationError("changed_fields and preserved_fields must be disjoint")
        validate_mutation_fields(self.attack_type, self.changed_fields)
        if not _COMMON_IDENTITY_FIELDS.issubset(self.preserved_fields):
            raise SchemaValidationError("canonical identity fields must be preserved")
        if self.schema_version != SCHEMA_VERSION:
            raise SchemaValidationError("unsupported schema_version")


def validate_mutation_fields(
    attack_type: AttackType, changed_fields: tuple[str, ...]
) -> None:
    allowed = ALLOWED_CHANGED_FIELDS.get(attack_type)
    if allowed is None:
        raise SchemaValidationError("unsupported attack type")
    prohibited = set(changed_fields) - allowed
    if prohibited:
        raise SchemaValidationError(
            f"HKP_PROHIBITED_FIELD_CHANGE: {sorted(prohibited)}"
        )


__all__ = ["ALLOWED_CHANGED_FIELDS", "MutationSpec", "validate_mutation_fields"]
