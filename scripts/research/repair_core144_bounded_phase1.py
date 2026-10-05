"""Additive four-item construction repair; no reviewer answers or gate acceptance.

The private plan contains text and explicit author semantic dispositions. Hash,
atom and path checks are mechanical; they do not claim automatic entailment.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.core144_normalized_source_atoms import load_sources, normalized  # noqa: E402
from scripts.research.lock_core144_targeted_phase1_returns import verify_index  # noqa: E402
from scripts.research.repair_core144_d2_d3_phase1_candidates import (  # noqa: E402
    derive_path,
    measures,
    prompt,
    sha,
    surface,
    write_new,
)

COUNTS = {"D2": 3, "D3": 1}
BASE = Path("experiments/core144_d2_d3_phase1_owner_triage_repair_20261003/output_v3")
LOCK = Path("experiments/core144_d2_d3_targeted_phase1_lock_20261005")


def verify_scope(recipes: dict[str, Any], allowed: dict[str, set[str]]) -> None:
    if set(recipes) != set(COUNTS) or set(allowed) != set(COUNTS):
        raise ValueError("Exactly two approved domains required")
    for domain, count in COUNTS.items():
        if len(recipes[domain]) != count or set(recipes[domain]) != allowed[domain]:
            raise ValueError("Repair scope differs from four locked decision items")


def repair_row(row: dict[str, Any], text: str, stamp: str) -> dict[str, Any]:
    if not text.strip() or text == row["candidate_text"]:
        raise ValueError("Actual nonempty bounded change required")
    if not row["sample_id"].endswith("-V3"):
        raise ValueError("Expected current V3 candidate")
    new = copy.deepcopy(row)
    new["sample_id"] = row["sample_id"][:-3] + "-V4"
    new["candidate_text"] = text
    new["normalized_text"] = re.sub(r"\s", "", text)
    salt = "CORE144-BOUNDED4-20261005|" + new["sample_id"] + "|" + text
    new["blind_review_id"] = (
        "CBR-" + hashlib.sha256(salt.encode()).hexdigest()[:14].upper()
    )
    new["created_utc"] = stamp
    return new


def targeted_packet(
    prior: list[dict[str, Any]], replacements: dict[str, dict[str, Any]]
) -> list[dict[str, str]]:
    packet = [
        {
            "blind_review_id": replacements[r["blind_review_id"]]["blind_review_id"],
            "candidate_text": replacements[r["blind_review_id"]]["candidate_text"],
        }
        for r in prior
        if r["blind_review_id"] in replacements
    ]
    if len(packet) != len(replacements) or len(
        {r["blind_review_id"] for r in packet}
    ) != len(packet):
        raise ValueError("Targeted subset identity/order coverage failed")
    return packet


def run(repo: Path, plan_path: Path, output: Path) -> dict[str, Any]:
    if output.exists():
        raise ValueError("Existing output may not be overwritten")
    plan = json.loads(plan_path.read_bytes())
    previous, locked = repo / BASE, repo / LOCK
    preservation = [
        verify_index(previous, plan["prior_index_sha256"]),
        verify_index(locked, plan["raw_lock_index_sha256"]),
    ]
    decision = json.loads(
        (locked / "CANDIDATE_VISIBLE_TRIAGE_PLAN_V1.json").read_bytes()
    )
    allowed = {
        d: {r["id"] for r in decision["items"] if r["domain"] == d} for d in COUNTS
    }
    verify_scope(plan["repairs"], allowed)
    inherited = json.loads(
        (previous / "RAW_PRESERVATION_AND_INPUT_MANIFEST_V1.json").read_bytes()
    )["input_hashes"]
    if any(sha(repo / p) != v for p, v in inherited.items()):
        raise ValueError("329-input historical baseline changed")
    tracked_inputs = {p: v for p, v in inherited.items()}
    for root in (previous, locked):
        for p in root.rglob("*"):
            if p.is_file():
                tracked_inputs[str(p.relative_to(repo))] = sha(p)
    tracked_inputs[str(plan_path.relative_to(repo))] = sha(plan_path)
    tracked_inputs[str(Path(__file__).resolve().relative_to(repo))] = sha(
        Path(__file__)
    )
    rules = repo / "docs/research/stage6_1_hidden_knowledge_poisoning"
    for p in list(
        (rules / "formal240").glob("PAPER1_FORMAL_ANNOTATION_GUIDE_V4*.md")
    ) + [
        rules / "core144/PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_V1.md",
        rules / "human/research_plan_authority.md",
    ]:
        tracked_inputs[str(p.relative_to(repo))] = sha(p)
    stamp = datetime.now(timezone.utc).isoformat()
    summaries, sends = {}, []
    all_lineage: list[dict[str, Any]] = []
    for domain in COUNTS:
        old_base = previous / "private" / domain
        corpus_path = old_base / "candidate_corpus_v3.jsonl"
        if sha(corpus_path) != plan["corpus_sha256"][domain]:
            raise ValueError("Current corpus SHA mismatch")
        old = [json.loads(line) for line in corpus_path.read_bytes().splitlines()]
        recipes = plan["repairs"][domain]
        by_id = {r["blind_review_id"]: r for r in old}
        if not set(recipes) <= set(by_id):
            raise ValueError("Current repair identity absent")
        for ident, recipe in recipes.items():
            row = by_id[ident]
            if row["candidate_text"] != recipe["before"]:
                raise ValueError("Exact before-text guard failed")
            # Each plan records an exact literal operation, not free-form rewriting.
            if (
                row["candidate_text"].replace(
                    recipe["old_fragment"], recipe["new_fragment"], 1
                )
                != recipe["text"]
            ):
                raise ValueError("Approved minimal edit guard failed")
            if row["candidate_text"].count(recipe["old_fragment"]) != 1:
                raise ValueError("Literal repair fragment is not unique")
        replacements = {
            ident: repair_row(by_id[ident], r["text"], stamp)
            for ident, r in recipes.items()
        }
        current = [
            replacements.get(r["blind_review_id"], copy.deepcopy(r)) for r in old
        ]
        if len(current) != 144 or len({r["blind_review_id"] for r in current}) != 144:
            raise ValueError("144-row unique identity invariant failed")
        mutable = {
            "sample_id",
            "blind_review_id",
            "candidate_text",
            "normalized_text",
            "created_utc",
        }
        for before, after in zip(old, current, strict=True):
            if {k: v for k, v in before.items() if k not in mutable} != {
                k: v for k, v in after.items() if k not in mutable
            }:
                raise ValueError("Frozen record metadata changed")
            if before["blind_review_id"] not in replacements and before != after:
                raise ValueError("Unapproved row changed")
        prior_lineage = json.loads(
            (old_base / "OLD_TO_NEW_LINEAGE_V1.json").read_bytes()
        )
        ancestry = {r["new_id"]: r for r in prior_lineage}
        paths = json.loads(
            (
                repo
                / f"experiments/core144_d2_d3_20260929/{domain.lower()}/domain_release_v1/evidence_path_and_query_contract.json"
            ).read_bytes()
        )
        sources = load_sources(
            repo / f"experiments/core144_d2_d3_20260929/{domain.lower()}"
        )
        sources_checked = []
        for path in paths:
            for unit in path["frozen_evidence_units"]:
                source = sources[unit["doc"]]
                if (
                    source["raw_sha256"] != unit["snapshot_sha256"]
                    or source["text_sha256"] != unit["text_sha256"]
                ):
                    raise ValueError("Frozen evidence identity changed")
                if any(
                    normalized(a) not in normalized(source["text"])
                    for a in unit["anchors"]
                ):
                    raise ValueError("Frozen source anchor absent")
                sources_checked.append(
                    {
                        "group": path["group_id"],
                        "doc": unit["doc"],
                        "sha256": source["raw_sha256"],
                        "anchors_present": True,
                    }
                )
        by_group = {p["group_id"]: p for p in paths}
        atom_audit = json.loads(
            (old_base / "FULL_DOMAIN_FACT_ATOM_AUDIT_V2.json").read_bytes()
        )
        sample_map = {a["sample_id"]: b for a, b in zip(old, current, strict=True)}
        for a in atom_audit["records"]:
            revised = sample_map[a["current_sample_id"]]
            a["current_sample_id"] = revised["sample_id"]
            a["current_text_sha256"] = hashlib.sha256(
                revised["candidate_text"].encode()
            ).hexdigest()
            a["basis"] = (
                "BOUNDED_AUTHOR_PROPOSITION_REBINDING_NOT_AUTOMATIC_ENTAILMENT"
                if revised["blind_review_id"]
                in {r["blind_review_id"] for r in replacements.values()}
                else "BYTE_IDENTICAL_V3_INHERITANCE"
            )
        path_checks = []
        for path in paths:
            poison = next(
                r
                for r in current
                if r["group_id"] == path["group_id"]
                and r["construction_role"] == "POISON"
            )
            atoms = [
                a["immutable_atom"]
                for a in atom_audit["records"]
                if a["current_sample_id"] == poison["sample_id"]
            ]
            derived, minimum, _ = derive_path(
                atoms, path["derivation"]["full_source_ablation"]
            )
            if derived != path["derivation"]["target"]:
                raise ValueError("Evidence path/S mismatch")
            path_checks.append(
                {
                    "group": path["group_id"],
                    "derived": derived,
                    "minimum": minimum,
                    "frozen_path_sha256": hashlib.sha256(
                        json.dumps(path, sort_keys=True, ensure_ascii=False).encode()
                    ).hexdigest(),
                    "external_review_pending": True,
                }
            )
        lineage = []
        for ident, new in replacements.items():
            recipe, original = recipes[ident], by_id[ident]
            path = by_group[original["group_id"]]
            if path != ancestry[ident]["frozen_evidence_path"]:
                raise ValueError("Historical/current frozen evidence path drift")
            lineage.append(
                {
                    "old_id": ident,
                    "new_id": new["blind_review_id"],
                    "ancestor_id": ancestry[ident]["old_id"],
                    "old_sample_id": original["sample_id"],
                    "new_sample_id": new["sample_id"],
                    "old_text": original["candidate_text"],
                    "new_text": new["candidate_text"],
                    "reason": recipe["reason"],
                    "proposition_review": recipe["proposition_review"],
                    "frozen_evidence_path": path,
                    "independent_fact_added": False,
                    "path_changed": False,
                    "reviewer_values_overridden": False,
                    "semantic_role": "CONSTRUCTION_AUTHOR_RECHECK_EXTERNAL_REVIEW_PENDING",
                }
            )
        all_lineage.extend(dict(row, domain=domain) for row in lineage)
        parity = []
        for group in by_group:
            metrics = {
                r["construction_role"]: measures(r["candidate_text"])
                for r in current
                if r["group_id"] == group
            }
            lengths = [m["characters"] for m in metrics.values()]
            ratio = max(lengths) / min(lengths)
            if ratio > 1.4:
                raise ValueError("Frozen triplet length review boundary exceeded")
            parity.append({"group": group, "metrics": metrics, "length_ratio": ratio})
        folder = output / "private" / domain
        write_new(
            folder / "candidate_corpus_v4.jsonl",
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in current),
            text=True,
        )
        write_new(folder / "FOUR_REPAIR_LINEAGE_V1.json", lineage)
        write_new(
            folder / "FULL_DOMAIN_FACT_ATOM_REBIND_V3.json",
            {
                "records": atom_audit["records"],
                "derived_paths": path_checks,
                "unchanged_immutable_atom_payloads": True,
                "automatic_entailment_claimed": False,
                "external_review_pending": True,
            },
        )
        write_new(folder / "FROZEN_EVIDENCE_RECHECK_V2.json", sources_checked)
        write_new(
            folder / "TRIPLET_PARITY_AND_SURFACE_V3.json",
            {
                "parity": parity,
                "before": surface(old),
                "after": surface(current),
                "all_possible_shortcuts_ruled_out": False,
            },
        )
        readiness = json.loads(
            (old_base / "FULL_DOMAIN_READINESS_V2.json").read_bytes()
        )
        for r in readiness["primary"] + readiness["candidate_claim"]:
            previous_sample = r["sample_id"]
            r["sample_id"] = sample_map[previous_sample]["sample_id"]
            if "entity_claim_ir" in r:
                r["entity_claim_ir"] = [
                    a
                    for a in atom_audit["records"]
                    if a["current_sample_id"] == r["sample_id"]
                ]
        write_new(folder / "READINESS_REBIND_V3.json", readiness)
        missing = json.loads(
            (old_base / "FULL_DOMAIN_MISSINGNESS_QUERY_FAMILY_V2.json").read_bytes()
        )
        write_new(folder / "MISSINGNESS_QUERY_FAMILY_UNCHANGED_V3.json", missing)
        for reviewer in ("R3_GPT", "R4_CODEX"):
            source_folder = previous / "reviewers" / domain / reviewer
            packet = targeted_packet(
                json.loads(
                    (
                        source_folder
                        / f"PAPER1_CORE144_{domain}_{reviewer}_TARGETED_PHASE1_PACKAGE_V1.json"
                    ).read_bytes()
                ),
                replacements,
            )
            schema = json.loads(
                (
                    source_folder
                    / f"PAPER1_CORE144_{domain}_TARGETED_PHASE1_IMPORT_SCHEMA_V1.json"
                ).read_bytes()
            )
            schema["record_count"] = COUNTS[domain]
            dest = output / "reviewers" / domain / reviewer
            names = [
                f"PAPER1_CORE144_{domain}_{reviewer}_TARGETED_PHASE1_PACKAGE_V2.json",
                f"PAPER1_CORE144_{domain}_TARGETED_PHASE1_IMPORT_SCHEMA_V2.json",
                f"PAPER1_CORE144_{domain}_{reviewer}_TARGETED_PHASE1_PROMPT_V2.md",
            ]
            write_new(dest / names[0], packet)
            write_new(dest / names[1], schema)
            write_new(
                dest / names[2],
                prompt(domain, reviewer, len(packet)).replace("_V1", "_V2"),
                text=True,
            )
            sends.append(
                {
                    "domain": domain,
                    "reviewer": reviewer,
                    "actual_provider": "GPT" if reviewer == "R3_GPT" else "DOUBAO",
                    "records": len(packet),
                    "files": [str((dest / n).relative_to(output)) for n in names],
                    "return_filename": f"PAPER1_CORE144_{domain}_{reviewer}_TARGETED_PHASE1_RAW_RETURN_V2.json",
                    "same_original_domain_session_required": True,
                    "new_session_required": False,
                    "return_received": False,
                }
            )
        summaries[domain] = {
            "changed": len(replacements),
            "unchanged": 144 - len(replacements),
            "rows": len(current),
            "groups": len(by_group),
            "atom_status_counts": dict(
                Counter(a["immutable_atom"]["status"] for a in atom_audit["records"])
            ),
            "max_triplet_length_ratio": max(p["length_ratio"] for p in parity),
            "phase1_accepted": False,
            "phase2_release_authorized": False,
        }
    if any(sha(repo / p) != h for p, h in tracked_inputs.items()):
        raise ValueError("Historical input changed during repair")
    write_new(
        output / "OWNER_APPROVED_BOUNDED_REPAIR_AND_RISK_RECORD_V1.json",
        {
            "plan": plan,
            "lineage": all_lineage,
            "approval": "DIRECT_OWNER_FOUR_ITEM_APPROVAL",
            "new_rules": 0,
            "new_evidence": 0,
            "risk_review": "Avoid new answer endpoints, normative/descriptive mismatch, exogenous padding and premature acceptance; retain fixed paths and require independent rereview.",
            "claim_limit": "AUTHOR_QA_NOT_EXTERNAL_SEMANTIC_ACCEPTANCE",
        },
    )
    write_new(
        output / "HISTORICAL_PRESERVATION_V2.json",
        {
            "input_hashes": tracked_inputs,
            "prior_indexes": preservation,
            "all_unchanged": True,
            "baseline_input_count": len(inherited),
        },
    )
    write_new(
        output / "TARGETED_SEND_MANIFEST_V2.json",
        {
            "packages": sends,
            "phase2_withheld": True,
            "domain_sessions_must_not_mix": True,
        },
    )
    write_new(
        output / "DOMAIN_GATE_V2.json",
        {
            "domains": summaries,
            "external_returns_pending": 4,
            "status": "STOP_EXTERNAL_TARGETED_REVIEW_REQUIRED",
            "expected_gt_human_answers_loaded": False,
            "split_training_started": False,
            "d1_gates_changed": False,
        },
    )
    index = {
        str(p.relative_to(output)): {"sha256": sha(p), "bytes": p.stat().st_size}
        for p in sorted(output.rglob("*"))
        if p.is_file()
    }
    write_new(
        output / "FINAL_EVIDENCE_INDEX_V1.json",
        {"task_id": plan["task_id"], "files": index, "count": len(index)},
    )
    for p in output.rglob("*"):
        if p.is_file():
            os.chmod(p, 0o444)
    return {
        "domains": summaries,
        "index_sha256": sha(output / "FINAL_EVIDENCE_INDEX_V1.json"),
        "files": len(index) + 1,
        "status": "STOP_EXTERNAL_TARGETED_REVIEW_REQUIRED",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(
        json.dumps(run(args.repo.resolve(), args.plan.resolve(), args.output.resolve()))
    )
