"""Evaluation-side DESIGN schema/mapping audit; never create generator input or score answers."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_design import canonical_hash


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--runtime-plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.reference.read_bytes()
    if hashlib.sha256(raw).hexdigest() != "5c5f212ba16da97b114d897de910ab383a47d96db4cb7cd9b54e638f7f03cf31":
        raise ValueError("OWNER_PINNED_REFERENCE_SHA_REQUIRED")
    reference = json.loads(raw)
    cards = reference["cards"]
    if (len(cards) != 12 or {c["review_id"] for c in cards} != {f"REVIEW-{n:02}" for n in range(1, 13)}
            or reference["status"] != "AI_ASSISTED_PROVISIONAL_REFERENCE_NOT_HUMAN_GOLD"
            or reference["ground_truth_status"] != "HUMAN_GOLD_0" or reference["model_answers_available"] is not False):
        raise ValueError("PROVISIONAL_12_SCHEMA_DRIFT")
    plan_path = args.runtime_plan / "GENERATOR_REQUEST_PLAN_PRIVATE.json"
    before_sha = hashlib.sha256(plan_path.read_bytes()).hexdigest()
    plan = json.loads(plan_path.read_bytes())
    lock = json.loads((args.runtime_plan / "GENERATOR_DESIGN_LOCK.json").read_bytes())
    if lock["status"] != "DESIGN_ONLY_NOT_RUN" or canonical_hash(plan) != lock["private_plan_hash"]:
        raise ValueError("GENERATOR_DESIGN_LOCK_REQUIRED")
    if any(r["status"] != "NOT_RUN" for r in plan):
        raise ValueError("DESIGN_ONLY_INPUT_REQUIRED")
    mapping = []
    qhashes = {r["query_hash"] for r in plan}
    for card in cards:
        if not isinstance(card["provisional_answer"], str) or not card["provisional_answer"] or not isinstance(card["answer_scope"], str):
            raise ValueError("PROVISIONAL_ANSWER_SCOPE_REQUIRED")
        qhash = canonical_hash(card["question"])
        if qhash not in qhashes:
            raise ValueError("EXACT_ORIGINAL_QUESTION_MAPPING_REQUIRED_NO_NORMALIZATION")
        rows = [r for r in plan if r["query_hash"] == qhash]
        if len(rows) != 9 or len({r["world_hash"] for r in rows}) != 3:
            raise ValueError("THREE_WORLDS_THREE_ARMS_PER_QUESTION_REQUIRED")
        mapping.append({"review_id": card["review_id"], "question_hash": qhash,
            "world_hashes": sorted({r["world_hash"] for r in rows}), "request_ids": [r["request_id"] for r in rows]})
    if len({m["question_hash"] for m in mapping}) != 12:
        raise ValueError("REFERENCE_QUESTION_MAPPING_NOT_BIJECTIVE")
    args.output.mkdir(exist_ok=False)
    (args.output / "REFERENCE_TO_REQUEST_BINDING_PRIVATE.json").write_bytes((json.dumps(mapping, indent=2) + "\n").encode())
    summary = {"status": "RECEIVED_SHA_VERIFIED_SCHEMA_AND_PRIVATE_MAPPING_DESIGN_READY", "cards": 12,
        "review_ids": sorted(c["review_id"] for c in cards), "atoms": sum(len(c["proposed_atom_fields"]) for c in cards),
        "reference_sha256": hashlib.sha256(raw).hexdigest(), "source_package_sha256_declared": reference["source_package_sha256"],
        "exact_question_matches": 12, "worlds_per_reference": 3, "planned_requests_per_reference": 9,
        "HumanGold": 0, "attack_target": "UNKNOWN", "C3": "NOT_ADJUDICATED", "reference_in_generator_input": False,
        "actual_scoring_executed": False, "new_model_or_API_calls": 0,
        "design_phase_reference_audit_is_not_future_runtime_scorer_access": True,
        "private_mapping_sha256": hashlib.sha256((args.output / "REFERENCE_TO_REQUEST_BINDING_PRIVATE.json").read_bytes()).hexdigest()}
    if hashlib.sha256(plan_path.read_bytes()).hexdigest() != before_sha:
        raise ValueError("REFERENCE_AUDIT_MUST_NOT_WRITE_GENERATOR_PLAN")
    (args.output / "REFERENCE_SCHEMA_HANDOFF_PUBLIC.json").write_bytes((json.dumps(summary, ensure_ascii=False, indent=2) + "\n").encode())
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
