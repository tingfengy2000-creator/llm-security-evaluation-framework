from __future__ import annotations

import pytest

from llmguard.domains.retrieval.hidden_poisoning import (
    AttackType,
    BenchmarkLabel,
    BenchmarkRecord,
    ClaimRecord,
    HardNegativeType,
    ProvenanceRecord,
    StealthLevel,
    VersionRelation,
    canonical_sha256,
)


def _record(
    *,
    index: int,
    label: BenchmarkLabel,
    attack_type: AttackType | None = None,
    stealth_level: StealthLevel | None = None,
    hard_negative_type: HardNegativeType | None = None,
) -> BenchmarkRecord:
    record_id = f"SYN-{index:02d}"
    version_chain_id = f"VC-{index:02d}"
    claim = ClaimRecord(
        record_id=f"CL-{index:02d}",
        entity_id=f"ENTITY-{index:02d}",
        claim_family=f"CLAIM-{index:02d}",
        subject=f"合成机构{index}",
        predicate="适用合成条件",
        object_value=f"合成值{index}",
        numeric_value=float(index),
        unit="合成单位",
        conditions=("仅用于离线测试",),
    )
    version = VersionRelation(
        relation_id=f"VR-{index:02d}",
        version_chain_id=version_chain_id,
        current_record_id=record_id,
        predecessor_record_id=None,
        successor_record_id=None,
        effective_at=f"2099-01-{index:02d}T00:00:00Z",
        expires_at=None,
        repealed_at=("2100-01-01T00:00:00Z" if index % 4 == 0 else None),
    )
    provenance = ProvenanceRecord(
        provenance_id=f"PV-{index:02d}",
        source_id=f"SOURCE-{index:02d}",
        source_document_family=f"SF-{index:02d}",
        source_type="synthetic",
        authority_level="synthetic-test-only",
        jurisdiction="虚构区域",
        department=f"合成部门{index % 3}",
        citation_reference=f"SYNTHETIC-{index:02d}",
    )
    return BenchmarkRecord(
        record_id=record_id,
        claim=claim,
        version=version,
        provenance=provenance,
        document_text=f"这是第{index}条纯合成中文测试文档，不对应任何真实政策、个人或机构。",
        entity_id=claim.entity_id,
        claim_family=claim.claim_family,
        version_chain_id=version_chain_id,
        source_document_family=provenance.source_document_family,
        mutation_template_family=f"MT-{index:02d}",
        near_duplicate_cluster=f"ND-{index:02d}",
        label=label,
        attack_type=attack_type,
        stealth_level=stealth_level,
        mutation_operation=("field-level synthetic mutation" if attack_type else None),
        changed_claim_fields=(("object_value",) if attack_type else ()),
        annotator_labels=(label.value, label.value),
        adjudicated_label=label.value,
        rationale="纯合成测试标签",
        hard_negative_type=hard_negative_type,
        split=None,
        evaluator_notes="不得进入模型可见输出",
    )


@pytest.fixture
def synthetic_records() -> tuple[BenchmarkRecord, ...]:
    attacks = tuple(AttackType)
    stealth = tuple(StealthLevel)
    poison_records = tuple(
        _record(
            index=index + 1,
            label=BenchmarkLabel.POISON,
            attack_type=attacks[index // 3],
            stealth_level=stealth[index % 3],
        )
        for index in range(12)
    )
    hard_negative_records = tuple(
        _record(
            index=index + 13,
            label=BenchmarkLabel.HARD_NEGATIVE,
            hard_negative_type=hard_negative_type,
        )
        for index, hard_negative_type in enumerate(HardNegativeType)
    )
    return poison_records + hard_negative_records


@pytest.fixture
def synthetic_fixture_hash(synthetic_records: tuple[BenchmarkRecord, ...]) -> str:
    return canonical_sha256(
        [record.canonical_payload() for record in sorted(synthetic_records, key=lambda item: item.record_id)]
    )
