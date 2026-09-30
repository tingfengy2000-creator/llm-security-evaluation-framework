"""Synthetic negative controls for construction mechanics; not real GT."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


def module(name: str) -> Any:
    path = Path(__file__).parents[2] / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def test_claim_ir_checks_literal_truth_not_role() -> None:
    audit = module("core144_claim_ir_audit")
    atoms = {"a": {"value": 5, "doc": "fictional-source-a"},
             "b": {"value": 10, "doc": "fictional-source-b"}}
    assert audit.evaluate({"op": "LT", "refs": ["a", "b"]}, atoms) == (True, ["fictional-source-a", "fictional-source-b"])
    assert audit.evaluate({"op": "IDENTITY", "refs": ["a"], "asserted_value": 10}, atoms)[0] != 10


def test_family_capacity_not_actual_split() -> None:
    audit = module("core144_family_capacity_audit")
    facts = [{"fact_id": f"HKP1-S1-C{i}", "family": f"synthetic-{i}",
              "core": f"core-{i}", "family_cluster_id": f"cluster-{i}"} for i in range(1, 5)]
    result = audit.inspect(facts)
    assert result["feasible_anonymous_capacity_count"] > 0
    assert not result["split_executed"] and not result["assignment_exported"]
    facts[1]["family"] = facts[0]["family"]
    assert audit.inspect(facts)["failures"]


def test_draft_counts_do_not_imply_acceptance() -> None:
    qa = module("core144_domain_draft_qa")
    result = qa.inspect({"domain": "SYNTHETIC", "triplets": []})
    assert not result["structural_counts_pass"]
    assert not result["domain_accepted"] and not result["semantic_atoms_validated"]
    assert not result["reviewer_release_allowed"]
