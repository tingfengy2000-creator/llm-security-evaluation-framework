"""Bounded evaluator-only identity audit; never load Oracle or review material."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from llmguard.domains.retrieval.hidden_poisoning.rag_defense_reconstruction.evaluation_preparation import (
    audit_existing_packets,
    select_groups,
)

F5 = "c849260e2a41fa9186e6d69ed6442cbebdaa7ff272beece9dfadc22e61cf535c"
LABELS = "d904e349211ec7af648b68afadb31e46a30196ba20a53b5a40a382ec0df7afaf"
SELECTION = "2c16fd6915c2dee377631d311ff33fe0ad36fdc8928a86e8fcabdcbca01cf689"
MANIFEST = "a7e05d2ebedbc68abc21fff46a0ad1597747712020957ac30cf1445353714a60"


def pinned(path: Path, expected: str) -> bytes:
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError("INPUT_IDENTITY_MISMATCH")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    # A fixed signed private_input_v2 bundle is the only admitted source.
    if args.bundle.resolve().name != "private_input_v2" or args.selection.name != "SELECTION_EVALUATOR_ONLY.json":
        raise ValueError("BOUNDED_INPUT_PATHS_REQUIRED")
    if args.output.exists():
        raise ValueError("NEW_OUTPUT_REQUIRED")
    manifest = json.loads(pinned(args.bundle / "BUNDLE_MANIFEST.json", MANIFEST))
    rows = [json.loads(line) for line in pinned(args.bundle / "runtime/f5.jsonl", F5).splitlines()]
    labels = [json.loads(line) for line in pinned(args.bundle / "evaluation/labels.jsonl", LABELS).splitlines()]
    selected = json.loads(pinned(args.selection, SELECTION))
    groups = select_groups(labels)
    if groups != selected["selected_groups_evaluator_only"] or selected["selection_uses_model_outcomes"]:
        raise ValueError("PILOT_SELECTION_DRIFT")
    if {r["candidate_id"] for r in rows} != {r["candidate_id"] for r in labels}:
        raise ValueError("RUNTIME_EVALUATOR_PAIRING_MISMATCH")
    roles = Counter(r["role_evaluation_only"] for r in labels)
    s = Counter(r["derived_s_evaluation_only"] for r in labels if r["role_evaluation_only"] == "POISON")
    if roles != {"POISON": 40, "CLEAN_CURRENT": 40, "HARD_NEGATIVE": 40} or s != {"S1": 12, "S2": 15, "S3": 13}:
        raise ValueError("D1_DENOMINATOR_DRIFT")
    chosen = [r for r in labels if r["group_evaluation_only"] in groups]
    chosen_ids = {r["candidate_id"] for r in chosen}
    report = {
        "status": "SIGNED_D1_BUNDLE_AND_PRIOR_PILOT_IDENTITIES_VERIFIED",
        "data_status": "D1_DEV_EXPOSED_NOT_FORMAL_GT",
        "input_hashes": {"manifest": MANIFEST, "f5": F5, "evaluation_labels": LABELS, "pilot_selection": SELECTION},
        "D1": {"groups": len({r["group_evaluation_only"] for r in labels}), "candidates": len(labels),
               "families": len({r["family_evaluation_only"] for r in labels}), "roles": dict(roles), "poison_S": dict(s)},
        "HOLD": {"groups_declared_in_bundle": manifest["holds_groups"],
                 "candidates_declared_in_bundle": manifest["holds_candidates"], "hold_payload_opened": False},
        "Pilot12": {"groups": len(groups), "candidates": len(chosen),
                    "families": len({r["family_evaluation_only"] for r in chosen}),
                    "poison_S": dict(Counter(r["derived_s_evaluation_only"] for r in chosen if r["role_evaluation_only"] == "POISON")),
                    "seed": selected["seed"], "prior_selection_reused_not_resampled": True},
        "old_runtime_readiness": audit_existing_packets(rows),
        "selected_old_runtime_readiness": audit_existing_packets([r for r in rows if r["candidate_id"] in chosen_ids]),
        "query_drafts": "EXISTING_AI_PROVISIONAL_V2_NOT_OPENED_BY_THIS_AUDIT",
        "signature_original_reopened": False, "D2_D3_payload_opened": False,
        "reviewer_payload_opened": False, "Oracle_opened": False, "paid_calls": 0,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=True))


if __name__ == "__main__":
    main()
