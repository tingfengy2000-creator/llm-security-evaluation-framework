from __future__ import annotations

import pytest

from llmguard.domains.retrieval.hidden_poisoning import (
    GroupIdentityRecord,
    LabelLeakageBlocker,
    LeakageBlocker,
    LeakageDocument,
    RuntimeAudience,
    SplitAssignment,
    SplitConfig,
    SplitName,
    UnimplementedSemanticNearDuplicateScanner,
    assert_embedding_input_isolated,
    assert_metadata_isolated,
    assert_no_label_leakage,
    build_independence_groups,
    deterministic_group_split,
    split_assignment_hash,
    validate_group_split,
)
from llmguard.domains.retrieval.hidden_poisoning.leakage import (
    scan_exact_duplicates,
    scan_identity_leakage,
    scan_normalized_duplicates,
)


def _group(
    record_id: str,
    *,
    version: str,
    mutation: str,
    entity: str | None = None,
) -> GroupIdentityRecord:
    return GroupIdentityRecord(
        record_id=record_id,
        entity_id=entity or f"E-{record_id}",
        claim_family=f"C-{record_id}",
        version_chain_id=version,
        source_document_family=f"S-{record_id}",
        mutation_template_family=mutation,
        near_duplicate_cluster=f"N-{record_id}",
    )


def test_transitive_group_closure_joins_indirect_relations() -> None:
    records = (
        _group("A", version="V-SHARED", mutation="M-A"),
        _group("B", version="V-SHARED", mutation="M-SHARED"),
        _group("C", version="V-C", mutation="M-SHARED"),
    )
    groups = build_independence_groups(records)
    assert len(set(groups.values())) == 1
    assert groups == build_independence_groups(reversed(records))


def test_group_split_is_deterministic_order_independent_and_configurable() -> None:
    groups = {f"R-{index}": f"IG-{index}" for index in range(60)}
    config = SplitConfig(train_ratio=0.70, dev_ratio=0.15, test_ratio=0.15, seed=20260802)
    first = deterministic_group_split(groups, config=config)
    second = deterministic_group_split(dict(reversed(tuple(groups.items()))), config=config)
    assert first == second
    assert split_assignment_hash(first) == split_assignment_hash(second)
    assert {item.split for item in first} == {SplitName.TRAIN, SplitName.DEV, SplitName.TEST}


def test_cross_split_group_overlap_fails_closed() -> None:
    assignments = (
        SplitAssignment(record_id="A", independence_group_id="IG-1", split=SplitName.TRAIN),
        SplitAssignment(record_id="B", independence_group_id="IG-1", split=SplitName.TEST),
    )
    with pytest.raises(LeakageBlocker, match="CROSS_SPLIT_GROUP_LEAKAGE_BLOCKER"):
        validate_group_split(assignments)


def test_duplicate_and_identity_scans_detect_cross_split_leakage() -> None:
    left_group = _group("A", version="V", mutation="M", entity="ENTITY")
    right_group = _group("B", version="V2", mutation="M2", entity="ENTITY")
    documents = (
        LeakageDocument(record_id="A", text="合成 文本。", group_identity=left_group, split="train"),
        LeakageDocument(record_id="B", text="合成文本", group_identity=right_group, split="test"),
    )
    assert not scan_exact_duplicates(documents)
    assert scan_normalized_duplicates(documents)[0].check_name == "normalized_duplicate"
    assert scan_identity_leakage(documents, attribute="entity_id")[0].check_name == "entity_id_leakage"


def test_semantic_near_duplicate_interface_fails_if_required() -> None:
    scanner = UnimplementedSemanticNearDuplicateScanner()
    assert scanner.scan((), required=False) == ()
    with pytest.raises(LeakageBlocker, match="SEMANTIC_NEAR_DUPLICATE_NOT_IMPLEMENTED"):
        scanner.scan((), required=True)


def test_metadata_embedding_and_fingerprint_inputs_fail_on_labels() -> None:
    for operation in (
        lambda: assert_metadata_isolated({"label": "POISON"}),
        lambda: assert_embedding_input_isolated(["safe", {"attack_id": "A-1"}]),
        lambda: assert_no_label_leakage(
            {"oracle": True}, audience=RuntimeAudience.FINGERPRINT
        ),
    ):
        with pytest.raises(LabelLeakageBlocker, match="LABEL_LEAKAGE_BLOCKER"):
            operation()
