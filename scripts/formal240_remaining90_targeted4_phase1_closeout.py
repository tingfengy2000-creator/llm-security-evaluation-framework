"""Lock-QA targeted D1 Phase1 returns and audit the repaired 90-row surface.

This construction-side script does not produce or release a Phase2 packet.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any

from formal240_remaining90_authority_surface_audit import (
    FOUR_IDS,
    MAPPING_SHA,
    PACKET_SHA,
    pattern_flags,
)
from formal240_remaining90_phase1_validate import FIELDS, DEFAULTS, read_json, sha256


R3_SHA = "da2f9491f53d5df840af4487d3411e79c9dc72b71649d5af72c1a1269e249d6d"
R4_SHA = "ad9e7a8a5042b2a2654291bd98def6ed2665e940471a3d33605ddef50d7ec6c2"
OLD_R3_SHA = "36a14d40f530bd2f9566f18f36acdce07a11a43b0c56142b8bb41e6af84f1e14"
OLD_R4_SHA = "d3aa0c1470b5dffab91217157a6b808f73531ae9fc3bbee21ef8626500759f04"
CURRENT_SHA = "428548caba9d613de52f4f8d3a35260a89679ecc4c5a7c0cb8b6013543c2c44a"
REPAIR_SHA = "fd1e1b38d02c97520b316c0969edfb40f83c7361051de4f25bc0ebe3903de6ff"
EXPECTED_IDS = {
    "D1BR-4F3F138D2EE3", "D1BR-56C613D63D51",
    "D1BR-BCD9105161AD", "D1BR-6357D4382C66",
}
NATURALNESS_ID = "D1BR-6357D4382C66"
ROLE_NAMES = ("CLEAN_CURRENT", "POISON", "HARD_NEGATIVE")


def locked(path: Path, expected: str) -> tuple[Any, bytes]:
    obj, raw = read_json(path)
    if sha256(raw) != expected:
        raise ValueError(f"frozen SHA256 mismatch: {path.name}")
    return obj, raw


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def write_new(path: Path, value: Any) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with path.open("xb") as stream:
        stream.write(raw)
    os.chmod(path, 0o444)
    return {"file": path.name, "bytes": len(raw), "sha256": sha256(raw)}


def validate_targeted(
    label: str, rows: Any, packet: Any, allowed: dict[str, Any], raw: bytes
) -> tuple[dict[str, Any], dict[str, dict[str, str]]]:
    require(isinstance(packet, dict) and isinstance(packet.get("records"), list), f"{label} packet shape")
    packet_rows = packet["records"]
    require(len(packet_rows) == 4 and all(list(r) == ["blind_review_id", "candidate_text"] for r in packet_rows), f"{label} packet rows")
    require(isinstance(rows, list) and len(rows) == 4, f"{label} return count")
    expected_ids = [r["blind_review_id"] for r in packet_rows]
    require(set(expected_ids) == EXPECTED_IDS and len(set(expected_ids)) == 4, f"{label} packet ID set")
    ids: list[str] = []
    for index, row in enumerate(rows):
        require(isinstance(row, dict) and list(row) == list(allowed), f"{label} key order {index}")
        ident = row["blind_review_id"]
        require(isinstance(ident, str), f"{label} ID type {index}")
        ids.append(ident)
        for field, legal in allowed.items():
            value = row[field]
            require(isinstance(value, str), f"{label} non-string {field} {index}")
            if isinstance(legal, list):
                require(value in legal, f"{label} illegal {field} {index}")
        flagged = any(row[field] != default for field, default in zip(FIELDS, DEFAULTS))
        require(flagged == bool(row["issue_note"].strip()), f"{label} note contract {ident}")
    require(ids == expected_ids and len(set(ids)) == 4, f"{label} ID/order mismatch")
    return (
        {
            "reviewer_code": label,
            "records": 4,
            "unique_ids": 4,
            "id_order_exact": True,
            "seven_keys_enum_note_contract": True,
            "bytes": len(raw),
            "sha256": sha256(raw),
            "distributions": {field: dict(Counter(r[field] for r in rows)) for field in FIELDS},
        },
        {r["blind_review_id"]: r for r in rows},
    )


def surface_audit(
    old: list[dict[str, str]], current: list[dict[str, str]],
    mapping: list[dict[str, str]], repairs: list[dict[str, Any]],
) -> dict[str, Any]:
    role_by_old = {r["blind_review_id"]: r["role"] for r in mapping}
    require(len(role_by_old) == 90 and set(role_by_old) == {r["blind_review_id"] for r in old}, "sealed role mapping mismatch")
    new_to_old = {r["new_blind_review_id"]: r["old_blind_review_id"] for r in repairs}
    require(set(new_to_old) == EXPECTED_IDS and set(new_to_old.values()) == FOUR_IDS, "repair ID lineage mismatch")
    role_by_current = {r["blind_review_id"]: role_by_old[new_to_old.get(r["blind_review_id"], r["blind_review_id"])] for r in current}
    require(Counter(role_by_current.values()) == {role: 30 for role in ROLE_NAMES}, "role denominator drift")

    def hit_report(rows: list[dict[str, str]], roles: dict[str, str], pattern: str) -> dict[str, Any]:
        def hit(text: str) -> bool:
            if pattern == "old_authority_fixed_clause":
                return pattern_flags(text)["authority_exact_clause"]
            if pattern == "old_authority_normalized_clause":
                return pattern_flags(text)["authority_normalized_clause"]
            if pattern == "old_authority_comma_template":
                return pattern_flags(text)["authority_comma_pattern"]
            if pattern == "old_generic_ji_shi_tongshi":
                return pattern_flags(text)["exact_ji_shi_tongshi_you_shi"]
            if pattern == "new_same_publication_exact":
                return "同一次公布" in text
            if pattern == "new_publication_event_exact":
                return "公布行为" in text
            if pattern == "new_this_publication_exact":
                return "这次公布" in text
            if pattern == "new_semantic_dual_authority":
                return "公布" in text and "国务院" in text and "人力资源社会保障部" in text
            if pattern == "semicolon_surface":
                return "；" in text
            raise ValueError(pattern)

        ids = [r["blind_review_id"] for r in rows if hit(r["candidate_text"])]
        return {"hit_count": len(ids), "counts_by_role": {role: sum(roles[i] == role for i in ids) for role in ROLE_NAMES}, "hit_ids": ids}

    patterns = (
        "old_authority_fixed_clause", "old_authority_normalized_clause",
        "old_authority_comma_template", "old_generic_ji_shi_tongshi",
        "new_same_publication_exact", "new_publication_event_exact",
        "new_this_publication_exact", "new_semantic_dual_authority",
        "semicolon_surface",
    )
    before = {p: hit_report(old, role_by_old, p) for p in patterns}
    after = {p: hit_report(current, role_by_current, p) for p in patterns}
    require(before["old_authority_fixed_clause"]["counts_by_role"] == {"CLEAN_CURRENT": 0, "POISON": 4, "HARD_NEGATIVE": 0}, "old shortcut baseline drift")
    for name in ("old_authority_fixed_clause", "old_authority_normalized_clause", "old_authority_comma_template"):
        require(after[name]["hit_count"] == 0, f"old authority shortcut survived: {name}")
    require(after["new_semantic_dual_authority"]["hit_count"] >= 4, "intended authority contradiction lost")
    # A repeated fixed surface shared by >=3 of the four repaired rows, with
    # zero controls, would be an obvious new shortcut. Distinct expressions of
    # the intended dual-authority semantics are not by themselves a surface cue.
    for name in ("new_same_publication_exact", "new_publication_event_exact", "new_this_publication_exact"):
        counts = after[name]["counts_by_role"]
        require(not (counts["POISON"] >= 3 and counts["CLEAN_CURRENT"] == counts["HARD_NEGATIVE"] == 0), f"new repeated surface shortcut: {name}")
    repaired = [r for r in current if r["blind_review_id"] in EXPECTED_IDS]
    require(len(repaired) == 4, "repaired corpus population")
    punctuation = Counter("；" if "；" in r["candidate_text"] else "，" for r in repaired)
    require(len(punctuation) >= 2, "repaired punctuation template still uniform")
    return {
        "scope": "CONTROL_ONLY_SEALED_ROLE_AUDIT_NOT_REVIEWER_MATERIAL",
        "records": 90,
        "role_denominators": {role: 30 for role in ROLE_NAMES},
        "before": before,
        "after": after,
        "repaired_punctuation_forms": dict(punctuation),
        "old_four_of_four_fixed_template_removed": True,
        "semantic_authority_contradiction_is_intended_mechanism_not_a_surface_string": True,
        "residual_two_row_phrase_watch": after["new_same_publication_exact"]["hit_count"] == 2,
        "surface_shortcut_blocker_resolved": True,
        "limitations": "Small 90-row construction audit; absence of the fixed wording does not prove every possible lexical shortcut absent.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    for key in ("r3", "r4", "r3_packet", "r4_packet", "schema", "old_r3", "old_r4", "old_packet", "mapping", "current", "repair", "owner_overlay", "output_dir"):
        parser.add_argument(f"--{key.replace('_', '-')}", required=True, type=Path)
    args = parser.parse_args()
    r3, r3_raw = locked(args.r3, R3_SHA)
    r4, r4_raw = locked(args.r4, R4_SHA)
    packet3, packet3_raw = read_json(args.r3_packet)
    packet4, packet4_raw = read_json(args.r4_packet)
    schema, schema_raw = read_json(args.schema)
    require(isinstance(schema, dict) and isinstance(schema.get("phase1"), dict), "targeted schema invalid")
    allowed = schema["phase1"]
    qa3, by3 = validate_targeted("R3-gpt", r3, packet3, allowed, r3_raw)
    qa4, by4 = validate_targeted("R4-codex", r4, packet4, allowed, r4_raw)
    require({r["blind_review_id"]: r["candidate_text"] for r in packet3["records"]} == {r["blind_review_id"]: r["candidate_text"] for r in packet4["records"]}, "reviewer packet ID/text parity")
    for ident in EXPECTED_IDS:
        for result in (by3[ident], by4[ident]):
            require(result["local_internal_conflict"] == "YES", f"contradiction not preserved: {ident}")
            require(result["self_containment"] == "PASS", f"self-containment defect: {ident}")
            require(result["ambiguous_referent"] == "NO", f"ambiguous referent: {ident}")
            require(result["meta_or_template_language"] == "NO", f"meta/template language: {ident}")
    naturalness_diff = [i for i in EXPECTED_IDS if by3[i]["text_naturalness"] != by4[i]["text_naturalness"]]
    require(naturalness_diff == [NATURALNESS_ID], "unexpected naturalness differences")
    require(by3[NATURALNESS_ID]["text_naturalness"] == "MINOR_ISSUE" and by4[NATURALNESS_ID]["text_naturalness"] == "NATURAL", "Owner naturalness basis drift")
    require(all(by3[i]["text_naturalness"] == by4[i]["text_naturalness"] == "NATURAL" for i in EXPECTED_IDS - {NATURALNESS_ID}), "other naturalness disagreement")
    old3, _ = locked(args.old_r3, OLD_R3_SHA)
    old4, _ = locked(args.old_r4, OLD_R4_SHA)
    old_packet, _ = locked(args.old_packet, PACKET_SHA)
    mapping, _ = locked(args.mapping, MAPPING_SHA)
    current, _ = locked(args.current, CURRENT_SHA)
    repair, _ = locked(args.repair, REPAIR_SHA)
    owner, _ = read_json(args.owner_overlay)
    old_rows = old_packet["records"]
    new_rows = current["records"]
    repairs = repair["records"]
    require(len(old_rows) == len(new_rows) == len(old3) == len(old4) == len(mapping["records"]) == 90 and len(repairs) == 4, "90/4 population drift")
    require(sum(a == b for a, b in zip(old_rows, new_rows)) == 86, "86 unchanged candidate parity")
    old3_by = {r["blind_review_id"]: r for r in old3}
    old4_by = {r["blind_review_id"]: r for r in old4}
    require(set(old3_by) == set(old4_by) == {r["blind_review_id"] for r in old_rows}, "old raw/packet IDs")
    require({r["old_blind_review_id"] for r in repairs} == FOUR_IDS, "repair old IDs")
    require({r["new_blind_review_id"] for r in repairs} == EXPECTED_IDS, "repair new IDs")
    for rep in repairs:
        require(not rep["evidence_changed"] and not rep["fact_atoms_changed"], "repair evidence/fact invariant")
    surface = surface_audit(old_rows, new_rows, mapping["records"], repairs)

    old_to_new = {r["old_blind_review_id"]: r["new_blind_review_id"] for r in repairs}
    final_rows: list[dict[str, Any]] = []
    for old_row, new_row in zip(old_rows, new_rows):
        old_id, new_id = old_row["blind_review_id"], new_row["blind_review_id"]
        require(new_id == old_to_new.get(old_id, old_id), "90-row ID order lineage")
        r3_value = by3[new_id] if old_id in FOUR_IDS else old3_by[old_id]
        r4_value = by4[new_id] if old_id in FOUR_IDS else old4_by[old_id]
        final_rows.append({
            "blind_review_id": new_id,
            "source_old_blind_review_id": old_id if old_id in FOUR_IDS else None,
            "source_scope": "TARGETED4_V2" if old_id in FOUR_IDS else "ORIGINAL_LOCKED_FULL90",
            "r3": {field: r3_value[field] for field in FIELDS},
            "r4": {field: r4_value[field] for field in FIELDS},
            "issue_note_presence": {"r3": bool(r3_value["issue_note"].strip()), "r4": bool(r4_value["issue_note"].strip())},
            "nonblocking_naturalness_variance": r3_value["text_naturalness"] != r4_value["text_naturalness"],
        })
    require(len(final_rows) == 90 and len({r["blind_review_id"] for r in final_rows}) == 90, "final overlay IDs")
    agreement = {field: sum(row["r3"][field] == row["r4"][field] for row in final_rows) for field in FIELDS}
    require(agreement == {"text_naturalness": 83, "local_internal_conflict": 90, "self_containment": 90, "ambiguous_referent": 90, "meta_or_template_language": 90}, "final agreement drift")
    require(len(owner["naturalness_decisions"]) == 6, "prior Owner six variance decisions")
    require(sum(r["nonblocking_naturalness_variance"] for r in final_rows) == 7, "final seven naturalness variances")
    comparison = {
        "status": "TARGETED4_STRUCTURAL_AND_SUBSTANTIVE_QA_PASS",
        "r3": qa3, "r4": qa4,
        "package_sha256": {"r3": sha256(packet3_raw), "r4": sha256(packet4_raw)},
        "schema_sha256": sha256(schema_raw),
        "targeted_ids": sorted(EXPECTED_IDS),
        "categorical_agreement": {field: sum(by3[i][field] == by4[i][field] for i in EXPECTED_IDS) for field in FIELDS},
        "naturalness_variance": {"blind_review_id": NATURALNESS_ID, "r3": "MINOR_ISSUE", "r4": "NATURAL", "owner_disposition": "NONBLOCKING_NATURALNESS_VARIANCE", "further_repair": False},
        "four_contradictions_preserved": True,
        "r5_tiebreak_required": False,
        "not_ground_truth": True,
    }
    overlay = {
        "status": "D1_REMAINING90_PHASE1_FINAL_OVERLAY_NOT_GT",
        "records": final_rows,
        "record_count": 90,
        "unchanged_full90_count": 86,
        "targeted_repair_count": 4,
        "agreement": agreement,
        "naturalness_variance_count": 7,
        "majority_vote_used": False,
        "raw_reviewer_values_rewritten": False,
        "phase2_release_depends_on_owner_run_attestation": True,
    }
    out = args.output_dir
    require(not out.exists(), "refusing to overwrite closeout output")
    out.mkdir(parents=True)
    outputs = {}
    for label, name, obj in (
        ("r3_lock", "PAPER1_FORMAL_D1_REMAINING90_R3_GPT_TARGETED4_PHASE1_RAW_LOCK_MANIFEST_V2.json", {"source": str(args.r3), **qa3, "immutable_copy": True}),
        ("r4_lock", "PAPER1_FORMAL_D1_REMAINING90_R4_CODEX_TARGETED4_PHASE1_RAW_LOCK_MANIFEST_V2.json", {"source": str(args.r4), **qa4, "immutable_copy": True, "provider": "Doubao", "isolation_evidence": "OWNER_ATTESTED_PENDING_EXPLICIT_TARGETED_RUN_CONFIRMATION"}),
        ("comparison", "PAPER1_FORMAL_D1_REMAINING90_TARGETED4_PHASE1_COMPARISON_V1.json", comparison),
        ("surface", "PAPER1_FORMAL_D1_REMAINING90_POST_REPAIR_SURFACE_SHORTCUT_AUDIT_V1.json", surface),
        ("overlay", "PAPER1_FORMAL_D1_REMAINING90_PHASE1_FINAL_OVERLAY_V1.json", overlay),
    ):
        outputs[label] = write_new(out / name, obj)
    print(json.dumps({"status": "MECHANICAL_QA_PASS_OWNER_SESSION_ATTESTATION_PENDING", "agreement": agreement, "outputs": outputs}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
