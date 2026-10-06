"""Lock bounded V2 rereviews without labels, voting or Phase2 release.

Comparison consumes only reviewer raw, candidate-only packets and schemas.
After that, an identity-only approved projection joins prior per-reviewer views.
No construction lineage/facts, Expected, GT or Human answers are parsed here.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from scripts.research.lock_core144_d2_d3_phase1_returns import (
    FIELDS,
    digest,
    now,
    parse,
    save_new,
)
from scripts.research.lock_core144_targeted_phase1_returns import (
    compare_targeted,
    validate_targeted,
    verify_index,
)

REPAIR = Path("experiments/core144_d2_d3_bounded4_repair_20261005/output_v1")
PRIOR = Path("experiments/core144_d2_d3_targeted_phase1_lock_20261005")
INDEX_HASHES = {
    REPAIR: "857b0e0f1e088b3b83603ef15a78dbc220ae61655432c8d0e041d740639fda50",
    PRIOR: "e9690c7802a2cc5e2c852b81d41ef5fb61a30ffaa0097df55df2669bbbac645a",
}
PACKET_HASHES = {
    "D2": "db4ee7d02172fae4f3df011c1891591d3e4c753754d7be99abcd4e8eff8e325d",
    "D3": "3129183e72187c2e789ff1b071dbb759758bb47d41f4021c92f8b92fb2d41024",
}
SCHEMA_HASHES = {
    "D2": "f534e568187d8eb2957ffa8cac9e9c81fc381cd0bbe0647efe9eb29f9340b41f",
    "D3": "4a194de6c61b827fe0a10b8880ebeaab399e19723cb348d603bf27e21dede959",
}


def require_source_pairs(sources: list[dict[str, Any]]) -> None:
    expected = {(d, r) for d in ("D2", "D3") for r in ("R3_GPT", "R4_CODEX")}
    if len(sources) != 4 or {(s["domain"], s["reviewer"]) for s in sources} != expected:
        raise ValueError("four distinct domain/reviewer source pairs required")


def merge_prior_view(
    previous: list[dict[str, Any]],
    targeted: list[dict[str, Any]],
    lineage: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Substitute only new-version answers; never overwrite a raw or prior view."""
    mapping = {s["old_id"]: s["new_id"] for s in lineage}
    targets = {s["blind_review_id"]: s for s in targeted}
    if (
        len(mapping) != len(lineage)
        or len(targets) != len(targeted)
        or set(mapping.values()) != set(targets)
    ):
        raise ValueError("new-version coverage must equal identity substitution")
    previous_ids = [s["answer"]["blind_review_id"] for s in previous]
    if len(set(previous_ids)) != len(previous_ids) or not set(mapping) <= set(previous_ids):
        raise ValueError("each substitution must have one unique prior ancestor")
    result = []
    for prior in previous:
        ident = prior["answer"]["blind_review_id"]
        item = deepcopy(prior)
        if ident in mapping:
            item = {
                "answer": deepcopy(targets[mapping[ident]]),
                "source": "TARGETED_V2",
                "previous_blind_review_id": ident,
                "superseded_evidence_record": deepcopy(prior),
                "raw_values_unchanged": True,
            }
        result.append(item)
    if len({s["answer"]["blind_review_id"] for s in result}) != len(previous):
        raise ValueError("substitution produced duplicate current IDs")
    return result


def run(repo: Path, output: Path) -> dict[str, Any]:
    if (output / "RAW_LOCK_MANIFEST_V1.json").exists():
        raise ValueError("fresh immutable analysis namespace required")
    plan_path = output / "INPUT_AND_OWNER_ATTESTATION_V1.json"
    plan = parse(plan_path.read_bytes())
    require_source_pairs(plan["sources"])
    if plan["owner_attestation"]["status"] != "OWNER_ATTESTED":
        raise ValueError("run-level attestation missing")
    locks = []
    for source in plan["sources"]:
        target = output / "raw" / Path(source["source_path"]).name
        raw = target.read_bytes()
        if (
            raw != Path(source["source_path"]).read_bytes()
            or digest(raw) != source["sha256"]
            or len(raw) != source["bytes"]
            or target.stat().st_mode & 0o222
        ):
            raise ValueError("raw source/copy/hash/readonly parity failed")
        locks.append(dict(source, locked_path=str(target.relative_to(output)),
                          provider="DOUBAO" if source["reviewer"] == "R4_CODEX" else "GPT",
                          readonly=True, byte_parity=True))
    # All originals are already byte-copied/read-only; this precedes raw parsing.
    save_new(output / "RAW_LOCK_MANIFEST_V1.json", {
        "raw_artifacts": locks, "lock_verified_utc": now(),
        "raw_locked_before_validation": True,
        "input_plan_sha256": digest(plan_path.read_bytes()),
        "owner_attestation": plan["owner_attestation"],
    })
    preservation = {
        str(root): verify_index(repo / root, sha)
        for root, sha in INDEX_HASHES.items()
    }
    save_new(output / "HISTORICAL_INDEX_PRESERVATION_V1.json", preservation)
    result: dict[str, Any] = {
        "scope": "BOUNDED_PHASE1_REVIEW_QA_NOT_GT",
        "comparison_started_utc": now(), "domains": {},
        "evaluation_reads_candidate_only": True,
        "phase2_release_authorized": False,
        "authority_for_phase2_preparation_or_release": False,
    }
    packets: dict[tuple[str, str], list[dict[str, Any]]] = {}
    valid: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for domain, count in (("D2", 3), ("D3", 1)):
        reports = {}
        for reviewer in ("R3_GPT", "R4_CODEX"):
            folder = repo / REPAIR / "reviewers" / domain / reviewer
            packet_raw = (folder / f"PAPER1_CORE144_{domain}_{reviewer}_TARGETED_PHASE1_PACKAGE_V2.json").read_bytes()
            schema_raw = (folder / f"PAPER1_CORE144_{domain}_TARGETED_PHASE1_IMPORT_SCHEMA_V2.json").read_bytes()
            if digest(packet_raw) != PACKET_HASHES[domain] or digest(schema_raw) != SCHEMA_HASHES[domain]:
                raise ValueError("frozen V2 packet/schema identity mismatch")
            packet, schema = parse(packet_raw), parse(schema_raw)
            if len(packet) != count:
                raise ValueError("bounded count not 3/1")
            packets[domain, reviewer] = packet
            raw = (output / "raw" / f"PAPER1_CORE144_{domain}_{reviewer}_TARGETED_PHASE1_RAW_RETURN_V2.json").read_bytes()
            reports[reviewer], valid[domain, reviewer] = validate_targeted(raw, packet, schema)
        a = {r["blind_review_id"]: r["candidate_text"] for r in packets[domain, "R3_GPT"]}
        b = {r["blind_review_id"]: r["candidate_text"] for r in packets[domain, "R4_CODEX"]}
        if a != b:
            raise ValueError("reviewer information parity failed")
        item: dict[str, Any] = {"validation": reports, "information_parity": True}
        if all(r["validation_pass"] for r in reports.values()):
            item["comparison"] = compare_targeted(packets[domain, "R3_GPT"], valid[domain, "R3_GPT"], valid[domain, "R4_CODEX"])
        item["phase2_release_authorized"] = False
        result["domains"][domain] = item
    result["comparison_completed_utc"] = now()
    save_new(output / "TARGETED_RAW_VALIDATION_AND_COMPARISON_V2.json", result)
    if not all(all(s["validation_pass"] for s in d["validation"].values()) for d in result["domains"].values()):
        return result
    # Identity-only joins run ONLY AFTER the candidate-visible comparison is saved.
    for domain in ("D2", "D3"):
        views = {}
        for reviewer in ("R3_GPT", "R4_CODEX"):
            prior_path = repo / PRIOR / "analysis_v2" / f"{domain}_{reviewer}_CURRENT_PHASE1_EVIDENCE_VIEW_V1.json"
            prior = parse(prior_path.read_bytes())
            merged = merge_prior_view(prior["records"], valid[domain, reviewer], plan["identity_substitutions"][domain])
            if len(merged) != 144:
                raise ValueError("joined current view not 144")
            views[reviewer] = {r["answer"]["blind_review_id"]: r["answer"] for r in merged}
            save_new(output / f"{domain}_{reviewer}_CURRENT_PHASE1_EVIDENCE_VIEW_V2.json", {
                "status": "REVIEWER_EVIDENCE_VIEW_NOT_ADJUDICATED_NOT_GT",
                "phase2_release_authorized": False, "records": merged,
                "prior_view_sha256": digest(prior_path.read_bytes()),
                "prior_view_path": str(prior_path.relative_to(repo)),
                "same_original_order_after_identity_substitution": True,
                "counts": dict(Counter(r["source"] for r in merged)),
            })
        if set(views["R3_GPT"]) != set(views["R4_CODEX"]):
            raise ValueError("full current reviewer identity parity failed")
        disagreement = {
            f: [i for i in views["R3_GPT"] if views["R3_GPT"][i][f] != views["R4_CODEX"][i][f]]
            for f in FIELDS
        }
        save_new(output / f"{domain}_CURRENT_144_COMPARISON_V2.json", {
            "records": 144, "disagreement_ids_by_field": disagreement,
            "disagreement_cells": sum(len(ids) for ids in disagreement.values()),
            "answers_preserved_without_vote": True, "phase2_release_authorized": False,
        })
    return result


def main() -> None:
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.repo.resolve(), args.output.resolve())
    print(json.dumps({d: {"validation_pass": all(r["validation_pass"] for r in v["validation"].values()),
                         "agreement": v.get("comparison", {}).get("categorical_agreement"),
                         "phase2_release_authorized": False} for d, v in result["domains"].items()}, indent=2))


if __name__ == "__main__":
    main()
