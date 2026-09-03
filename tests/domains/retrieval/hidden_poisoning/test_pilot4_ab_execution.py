from __future__ import annotations

import hashlib

from scripts.research.build_pilot4_ab_execution import (
    FINAL_STATUS,
    PHASE1_HEADERS,
    PHASE2_HEADERS,
    _opaque_ids,
    _order_qa,
    _random_order,
)


def _row(index: int) -> dict[str, object]:
    triplet = f"T-{index // 3:02d}"
    kind = ("CLEAN_CURRENT", "POISON_FACT", "HARD_NEGATIVE")[index % 3]
    return {
        "sample_id": f"S-{index:02d}",
        "triplet_id": triplet,
        "owner_only": {
            "candidate_kind": kind,
            "domain": f"D-{index % 8}",
            "coverage_cell": f"HKP-{index // 6}|S{index % 3 + 1}",
        },
    }


def test_contract_schemas_are_exact() -> None:
    assert PHASE1_HEADERS == [
        "blind_review_id",
        "text_naturalness",
        "local_internal_conflict",
        "phase1_issue",
        "phase1_reason",
    ]
    assert len(PHASE2_HEADERS) == 8
    assert PHASE2_HEADERS[0] == "blind_review_id"


def test_opaque_namespaces_are_disjoint_and_not_order_encoded() -> None:
    rows = [_row(index) for index in range(72)]
    seed_a = hashlib.sha256(b"A").digest()
    seed_b = hashlib.sha256(b"B").digest()
    ids_a = _opaque_ids(rows, seed_a, "A")
    ids_b = _opaque_ids(list(reversed(rows)), seed_b, "B")
    assert len(set(ids_a.values())) == 72
    assert len(set(ids_b.values())) == 72
    assert set(ids_a.values()).isdisjoint(ids_b.values())
    assert ids_a["S-00"] == _opaque_ids(list(reversed(rows)), seed_a, "A")["S-00"]


def test_random_order_passes_leakage_constraints() -> None:
    rows = [_row(index) for index in range(72)]
    order, qa = _random_order(rows, hashlib.sha256(b"deterministic-test").digest())
    assert qa["status"] == "PASS"
    assert qa["matched_triplet_adjacency_count"] == 0
    assert _order_qa(order)["status"] == "PASS"


def test_final_status_keeps_downstream_gates_closed() -> None:
    assert "PHASE2_WITHHELD" in FINAL_STATUS
    assert "NO_GROUND_TRUTH_YET" in FINAL_STATUS
    assert "ANNOTATION_COMPLETED" not in FINAL_STATUS
