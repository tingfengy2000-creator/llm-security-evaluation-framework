"""Synthetic negative controls for construction mechanics; not real GT."""

from __future__ import annotations

import importlib.util
import json
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


def test_reviewer_prep_fails_closed_on_hidden_field(tmp_path: Path) -> None:
    """Synthetic packets test sealing mechanics, not candidate factual truth."""
    audit = module("core144_d2_d3_reviewer_prep_audit")

    def save(path: Path, value: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    for domain in ("D2", "D3"):
        release = tmp_path / domain.lower() / "domain_release_v1"
        reviewer_dir = release / "reviewer"
        corpus = [{"blind_review_id": f"TEST-{i:03d}", "candidate_text": f"fictional text {i}",
                   "group_id": f"TEST-G{i % 48:02d}"} for i in range(144)]
        corpus_path = release / "candidate_corpus_v1.jsonl"
        corpus_path.parent.mkdir(parents=True, exist_ok=True)
        corpus_path.write_text("\n".join(json.dumps(row) for row in corpus) + "\n", encoding="utf-8")
        save(release / "domain_acceptance_matrix.json", {
            "candidate_sha256": audit.sha(corpus_path), "counts": {"groups": 48},
            "all_internal_hard_gates_pass": True, "gates": {"synthetic_gate": True},
        })
        save(reviewer_dir / f"PAPER1_CORE144_{domain}_PHASE1_IMPORT_SCHEMA_V1.json", {
            "phase": "PHASE1_CANDIDATE_ONLY", "record_count": 144,
            "keys": audit.PHASE1_KEYS, "enums": audit.PHASE1_ENUMS,
        })
        packages = []
        for reviewer, order in (("R3_GPT", range(144)), ("R4_CODEX", range(143, -1, -1))):
            packet_path = reviewer_dir / f"{reviewer}_PACKAGE.json"
            prompt_path = reviewer_dir / f"{reviewer}_PROMPT.md"
            save(packet_path, [{"blind_review_id": corpus[i]["blind_review_id"],
                                "candidate_text": corpus[i]["candidate_text"]} for i in order])
            prompt_path.write_text("Synthetic blind prompt", encoding="utf-8")
            packages.append({"reviewer": reviewer,
                             "actual_provider": "GPT" if reviewer == "R3_GPT" else "DOUBAO",
                             "package": str(packet_path), "package_sha256": audit.sha(packet_path),
                             "prompt": str(prompt_path), "prompt_sha256": audit.sha(prompt_path),
                             "records": 144})
        save(reviewer_dir / "package_manifest.json", {
            "packages": packages, "external_execution_started": False,
            "fallback_96_48_used": False, "information_equivalent": True,
            "opaque_ids": True, "hidden_fields": 0,
        })

    result = audit.inspect(tmp_path)
    assert result["four_packages_ready"] and not result["failures"]
    packet_path = tmp_path / "d3" / "domain_release_v1" / "reviewer" / "R4_CODEX_PACKAGE.json"
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    packet[0]["construction_role"] = "POISON"
    save(packet_path, packet)
    result = audit.inspect(tmp_path)
    assert not result["four_packages_ready"]
    assert {row["code"] for row in result["failures"]} >= {
        "HIDDEN_FIELD_IN_PACKET", "PACKAGE_OR_PROMPT_SHA_MISMATCH"
    }
