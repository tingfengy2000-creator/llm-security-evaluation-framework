"""Build the D1 remaining90 Phase2 handoff after explicit Owner gates.

The builder keeps the original R3/R4 row permutations, changes only the four
versioned candidate IDs/texts, and uses SHA-verified frozen official snapshots.
It refuses to replace any existing release directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from formal240_batch1_phase2_release import official_text
from formal240_remaining90_phase2_evidence_preflight import PROPOSED_TWO_SOURCE_PROJECTION


GUIDES = (
    "PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md",
    "PAPER1_FORMAL_ANNOTATION_GUIDE_V4_1_CLARIFICATION.md",
    "PAPER1_FORMAL_ANNOTATION_GUIDE_V4_2_VERSION_SCOPE_DECISION.md",
    "PAPER1_FORMAL_ANNOTATION_GUIDE_V4_3_TEMPORAL_VS_VERSION_SCOPE.md",
)
REPAIR_IDS = {
    "D1BR-4F3F138D2EE3", "D1BR-56C613D63D51",
    "D1BR-BCD9105161AD", "D1BR-6357D4382C66",
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load(path: Path) -> tuple[Any, str]:
    raw = path.read_bytes()
    return json.loads(raw.decode("utf-8-sig")), sha(raw)


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def reviewer_prompt(code: str, packet: str, schema: str, return_name: str) -> str:
    provider = "GPT" if code == "R3-gpt" else "Doubao"
    return (
        f"# D1 remaining90 Phase2 V5 — {code} ({provider})\n\n"
        "Continue in the **same isolated conversation** that produced your accepted "
        "remaining90 Phase1 and targeted-four Phase1 return. Do not start a new "
        "conversation or project for this Phase2. If that session is unavailable, "
        "stop and inform the Owner. Remain independent of the other reviewer.\n\n"
        f"Read only `{packet}`, `{schema}`, "
        + ", ".join(f"`{name}`" for name in GUIDES)
        + ", and this prompt. The packet is one authoritative 90-row MegaWave "
        "in your original Phase1 order. For each row use only "
        "that row's E1/E2 frozen official snapshot extracts. Official URLs and "
        "snapshot SHA256 are provenance, not permission to search or introduce "
        "outside sources. The text extracts are derived from locked raw snapshots. "
        "Do not access the repository, handoff directory beyond the sent files, "
        "construction/Owner packets, mapping, C/P/H, HKP, target/derived S, "
        "Expected/GT, other reviewer output, web, or another AI. Your own earlier "
        "Phase1 judgments are the only permitted previous review context.\n\n"
        "Apply Formal Guide V4 plus V4.1/V4.2/V4.3 in order. A bare law/article "
        "citation does not itself create a version claim; separate substantive, "
        "document-version, and authority claims. If a locked Phase1 internal "
        "contradiction alone establishes FACTUAL_CONFLICT, the minimum is "
        "ZERO_EXTERNAL_EVIDENCE_REQUIRED. `evidence_selection` records what you "
        "actually used, not the minimum needed. An ordinary factual conflict is "
        "not itself a Phase2 issue. If the supplied frozen evidence is insufficient, "
        "say so; never infer a missing official fact.\n\n"
        f"Save exactly one UTF-8 strict JSON array of 90 objects as `{return_name}`. "
        "Use exactly the schema keys, canonical English enums and packet-specific "
        "ID order; include a concise evidence-bound reason. No Markdown wrapper. "
        "Self-check count, unique IDs, key set/order, enums and file encoding. "
        "Preserve the submitted raw file without post-submission reformatting. "
        "This is pre-annotation construction QA, not Ground Truth.\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    for field in (
        "candidate", "repair", "mapping", "r3_old_packet", "r4_old_packet",
        "r3_targeted_packet", "r4_targeted_packet", "phase1_overlay",
        "evidence_manifest", "group_manifest", "evidence_preflight",
        "source_schema", "guide_dir", "out",
    ):
        parser.add_argument(f"--{field.replace('_', '-')}", type=Path, required=True)
    parser.add_argument("--owner-session-attested", action="store_true")
    parser.add_argument("--owner-two-source-projection-approved", action="store_true")
    args = parser.parse_args()
    require(args.owner_session_attested, "Owner reviewer-session attestation required")
    require(args.owner_two_source_projection_approved, "Owner bounded two-source projection approval required")
    require(not args.out.exists(), "refusing to overwrite prior release")

    current, current_sha = load(args.candidate)
    repair, repair_sha = load(args.repair)
    mapping, mapping_sha = load(args.mapping)
    old_r3, old_r3_sha = load(args.r3_old_packet)
    old_r4, old_r4_sha = load(args.r4_old_packet)
    target_r3, target_r3_sha = load(args.r3_targeted_packet)
    target_r4, target_r4_sha = load(args.r4_targeted_packet)
    overlay, overlay_sha = load(args.phase1_overlay)
    evidence, evidence_sha = load(args.evidence_manifest)
    groups, groups_sha = load(args.group_manifest)
    preflight, preflight_sha = load(args.evidence_preflight)
    source_schema, source_schema_sha = load(args.source_schema)

    require(current_sha == "428548caba9d613de52f4f8d3a35260a89679ecc4c5a7c0cb8b6013543c2c44a", "candidate SHA drift")
    require(repair_sha == "fd1e1b38d02c97520b316c0969edfb40f83c7361051de4f25bc0ebe3903de6ff", "repair SHA drift")
    require(mapping_sha == "14595f10049421dbea29464a04c2b8b45c70eeff5dda45a96d866462a47d8c57", "mapping SHA drift")
    require(old_r3_sha == "4d4c346bebb7933af6c5bdd7a7c7e5b4f6619b7f36508d80520015d2c5d516ed", "R3 Phase1 packet SHA drift")
    require(old_r4_sha == "9097342b22fa27dafba3258129a31edf563ecb67017894b5b2c13cd2528b3a8a", "R4 Phase1 packet SHA drift")
    require(target_r3_sha == "61724939d035e7ffbb5cd2bae784b859d37e0bb6962ddc7ed5274fc3d5e7e9e4", "R3 targeted packet SHA drift")
    require(target_r4_sha == "2316fd4197314ebc61568128665831693678232717a61c5de240bb8ee5d1ab13", "R4 targeted packet SHA drift")
    require(source_schema_sha == "121e4ad53fdbc09cacf69bc5e476dcdc09b0ee96cd1265f049aaa719d2332f4a", "Phase2 source schema SHA drift")
    require(preflight["source_manifest_sha256"] == evidence_sha and preflight["group_manifest_sha256"] == groups_sha, "preflight source lineage drift")
    require(preflight["mapping_sha256"] == mapping_sha and preflight["candidate_sha256"] == current_sha, "preflight candidate lineage drift")
    require(preflight["raw_snapshot_hashes_pass"] == 23 and preflight["release_status"].startswith("WITHHELD_"), "preflight not passed")
    require(overlay["record_count"] == 90 and overlay["unchanged_full90_count"] == 86 and overlay["targeted_repair_count"] == 4, "Phase1 overlay population drift")
    require(overlay["agreement"]["local_internal_conflict"] == 90, "Phase1 conflict agreement drift")
    require(list(source_schema["phase2"]) == [
        "blind_review_id", "overall_fact_status", "version_claim_status",
        "authority_claim_status", "minimum_external_evidence_needed",
        "evidence_selection", "phase2_issue", "phase2_reason",
        "possible_accidental_secondary_error", "evidence_sufficiency", "reviewer_note",
    ], "Phase2 schema drift")

    current_by = {row["blind_review_id"]: row["candidate_text"] for row in current["records"]}
    require(len(current_by) == 90, "candidate ID duplication")
    repaired_by_old = {row["old_blind_review_id"]: row["new_blind_review_id"] for row in repair["records"]}
    require(set(repaired_by_old.values()) == REPAIR_IDS and len(repaired_by_old) == 4, "repair lineage mismatch")
    old_order_r3 = [row["blind_review_id"] for row in old_r3["records"]]
    old_order_r4 = [row["blind_review_id"] for row in old_r4["records"]]
    require(len(old_order_r3) == len(old_order_r4) == len(set(old_order_r3)) == len(set(old_order_r4)) == 90, "original reviewer packet population")
    require(set(old_order_r3) == set(old_order_r4), "original reviewer ID sets differ")
    require(old_r3["records"] != old_r4["records"], "reviewer permutation unexpectedly equal")
    for targeted in (target_r3, target_r4):
        require({row["blind_review_id"] for row in targeted["records"]} == REPAIR_IDS, "targeted packet ID set")
        require(all(current_by[row["blind_review_id"]] == row["candidate_text"] for row in targeted["records"]), "targeted candidate text drift")

    sample_by_old = {row["blind_review_id"]: row for row in mapping["records"]}
    require(len(sample_by_old) == 90 and set(sample_by_old) == set(old_order_r3), "private mapping drift")
    group_by_id = {row["group_slot_id"]: row for row in groups["records"]}
    require(len(group_by_id) == 30, "group duplication")
    sources: dict[str, dict[str, Any]] = {}
    for row in evidence["records"]:
        path = Path(row["private_snapshot_path"])
        raw = path.read_bytes()
        require(sha(raw) == row["sha256"], f"frozen snapshot changed: {path.name}")
        snapshot = {
            "evidence_doc_id": "ES-" + row["sha256"][:12].upper(),
            "official_url": row["official_url"],
            "snapshot_raw_sha256": row["sha256"],
            "snapshot_text_extract": official_text(path),
        }
        require(bool(snapshot["snapshot_text_extract"]), f"empty source text: {path.name}")
        for alias in row["aliases"]:
            key = alias["evidence_id"]
            require(key not in sources or sources[key] == snapshot, f"alias collision: {key}")
            sources[key] = snapshot

    selection: dict[str, list[str]] = {}
    projections: list[dict[str, Any]] = []
    for slot, group in group_by_id.items():
        refs = group["evidence_refs"]
        selected = PROPOSED_TWO_SOURCE_PROJECTION.get(slot, refs)
        require(1 <= len(selected) <= 2 and set(selected).issubset(refs), f"invalid E1/E2 selection: {slot}")
        require(all(ref in sources for ref in selected), f"unresolved official source: {slot}")
        selection[slot] = selected
        if len(refs) == 3:
            projections.append({
                "group_slot_id": slot,
                "original_refs": refs,
                "reviewer_e1_e2_refs": selected,
                "private_retained_ref": [ref for ref in refs if ref not in selected],
                "selected_snapshot_sha256": [sources[ref]["snapshot_raw_sha256"] for ref in selected],
                "owner_approved_bounded_projection": True,
            })
    require(len(projections) == 2, "three-source projection count")

    def packet_for(old_order: list[str]) -> dict[str, Any]:
        records: list[dict[str, Any]] = []
        for old_id in old_order:
            new_id = repaired_by_old.get(old_id, old_id)
            slot = sample_by_old[old_id]["group_slot_id"]
            source_refs = selection[slot]
            public_evidence = [
                {"evidence_selection_id": f"E{index}", **sources[ref]}
                for index, ref in enumerate(source_refs, start=1)
            ]
            records.append({"blind_review_id": new_id, "candidate_text": current_by[new_id], "evidence": public_evidence})
        require(len(records) == len({r["blind_review_id"] for r in records}) == 90, "release population")
        require({r["blind_review_id"] for r in records} == set(current_by), "release/candidate identity parity")
        serialized = json.dumps(records, ensure_ascii=False).lower()
        forbidden = ("construction_role", "group_slot_id", "target_s", "derived_s", "expected", "ground_truth", "hkp1", "hkp2", "hkp3", "hkp4")
        require(not any(token in serialized for token in forbidden), "hidden constructor/label token in reviewer packet")
        return {
            "status": "D1_REMAINING90_PHASE2_PREANNOTATION_BLIND_QA_NOT_GT",
            "evidence_scope": "Only each row's E1/E2 text extracts from SHA-verified frozen official snapshots; URLs are provenance",
            "record_count": 90,
            "records": records,
        }

    args.out.mkdir(parents=True)
    r3_packet_name = "PAPER1_FORMAL_D1_REMAINING90_PHASE2_PACKAGE_V5.json"
    r4_packet_name = "PAPER1_FORMAL_D1_REMAINING90_R4_CODEX_PHASE2_PACKAGE_V5.json"
    write_json(args.out / r3_packet_name, packet_for(old_order_r3))
    write_json(args.out / r4_packet_name, packet_for(old_order_r4))
    schema_name = "PAPER1_FORMAL_D1_REMAINING90_PHASE2_IMPORT_SCHEMA_V5.json"
    schema = {
        "status": "D1_REMAINING90_PHASE2_V5_PREANNOTATION_BLIND_QA_IMPORT_SCHEMA",
        "phase2": source_schema["phase2"],
        "each_return": "One UTF-8 JSON array of exactly 90 objects; exact keys, legal enums, unique IDs and reviewer-specific packet order",
        "reviewer_independence": "R3/R4 each continue their own accepted remaining90 Phase1 conversation; no new Phase2 session",
        "not_ground_truth": True,
    }
    write_json(args.out / schema_name, schema)
    for name in GUIDES:
        shutil.copyfile(args.guide_dir / name, args.out / name)
    for code, prefix, packet_name in (
        ("R3-gpt", "R3_GPT", r3_packet_name),
        ("R4-codex", "R4_CODEX", r4_packet_name),
    ):
        return_name = f"PAPER1_FORMAL_D1_REMAINING90_{prefix}_PHASE2_RAW_RETURN_V5.json"
        prompt_name = f"PAPER1_FORMAL_D1_REMAINING90_{prefix}_PHASE2_PROMPT_V5.md"
        (args.out / prompt_name).write_text(reviewer_prompt(code, packet_name, schema_name, return_name), encoding="utf-8")

    files = {path.name: {"bytes": path.stat().st_size, "sha256": sha(path.read_bytes())} for path in sorted(args.out.iterdir())}
    manifest = {
        "status": "READY_FOR_OWNER_SAME_SESSION_R3_R4_PHASE2_DISTRIBUTION",
        "owner_reviewer_session_isolation": "OWNER_ATTESTED",
        "reviewers": {"R3-gpt": "GPT", "R4-codex": "Doubao"},
        "owner_two_source_projection": "BOUNDED_APPROVED_FOR_TWO_FROZEN_THREE_SNAPSHOT_GROUPS_ONLY",
        "projection_audit_private_do_not_send": projections,
        "candidate_count": 90,
        "repaired_count": 4,
        "unchanged_count": 86,
        "phase1_overlay_sha256": overlay_sha,
        "evidence_preflight_sha256": preflight_sha,
        "source_schema_sha256": source_schema_sha,
        "old_r4_phase1_packet_sha256": old_r4_sha,
        "frozen_evidence_manifest_sha256": evidence_sha,
        "files": files,
        "phase2_review_not_executed": True,
        "no_ground_truth_or_human_annotation": True,
    }
    write_json(args.out / "PAPER1_FORMAL_D1_REMAINING90_PHASE2_RELEASE_MANIFEST_V5_PRIVATE_DO_NOT_SEND.json", manifest)
    print(json.dumps({"status": manifest["status"], "records": 90, "projection_groups": len(projections), "out": str(args.out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
