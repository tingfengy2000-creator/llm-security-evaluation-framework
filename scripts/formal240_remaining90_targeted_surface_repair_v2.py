"""Supersede an unreleased targeted-four draft with a parity-safe V2 package."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from formal240_remaining90_phase1_validate import read_json, sha256
from formal240_remaining90_targeted_surface_repair import (
    ENUMS,
    json_text,
    prompt,
    write_new,
)


SOURCE_MANIFEST_SHA = "08b31c2ee366d4ab04f2756c409d3020fb7c0a838471862abf49ea5b8ba84abc"
SOURCE_CURRENT90_SHA = "657b585f7e33abc8eca06e61c68cd5d349b36b64efa688ead3199da456eb4e75"
OLD_BLIND_ID = "D1BR-194520C78747"
OLD_REPAIR_ID = "D1BR-5B7E94AC7D66"
V2_TEXT = "《工伤认定办法》由人力资源社会保障部公布，文号为人力资源社会保障部令第8号；同一次公布又由国务院作出。"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--v1-manifest", required=True, type=Path)
    parser.add_argument("--v1-current90", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    source_manifest, manifest_raw = read_json(args.v1_manifest)
    source_current, current_raw = read_json(args.v1_current90)
    if sha256(manifest_raw) != SOURCE_MANIFEST_SHA or sha256(current_raw) != SOURCE_CURRENT90_SHA:
        raise ValueError("unreleased V1 source hash mismatch")
    if len(source_manifest["records"]) != 4 or len(source_current["records"]) != 90:
        raise ValueError("unreleased V1 population mismatch")
    new_id = "D1BR-" + hashlib.sha256(
        f"D1_AUTHORITY_SURFACE_V3|{OLD_BLIND_ID}".encode()
    ).hexdigest()[:12].upper()
    if new_id in {row["blind_review_id"] for row in source_current["records"]}:
        raise ValueError("replacement ID collision")
    new_records = []
    for row in source_current["records"]:
        if row["blind_review_id"] == OLD_REPAIR_ID:
            new_records.append({"blind_review_id": new_id, "candidate_text": V2_TEXT})
        else:
            new_records.append(row)
    if sum(a == b for a, b in zip(source_current["records"], new_records)) != 89:
        raise ValueError("V2 changed more than one unreleased draft row")
    if len({row["blind_review_id"] for row in new_records}) != 90:
        raise ValueError("V2 ID duplication")
    updated_manifest = []
    for row in source_manifest["records"]:
        if row["old_blind_review_id"] == OLD_BLIND_ID:
            updated = dict(row)
            updated["new_blind_review_id"] = new_id
            updated["new_text"] = V2_TEXT
            updated["new_text_sha256"] = sha256(V2_TEXT.encode("utf-8"))
            updated["candidate_version"] = "AUTHORITY_SURFACE_V3_PENDING_R3_R4_TARGETED_PHASE1"
            updated["triplet_length_ratio"] = round(53 / 50, 4)
            updated_manifest.append(updated)
        else:
            updated_manifest.append(row)
    root = args.output_dir
    private = root / "control_only_do_not_send"
    released = root / "reviewer_release"
    outputs = {}
    outputs["private_repair_manifest"] = write_new(
        private / "PAPER1_FORMAL_D1_REMAINING90_AUTHORITY_TARGETED4_REPAIR_MANIFEST_V2.json",
        json_text({
            "status": "V2_SUPERSEDES_UNRELEASED_V1_PENDING_EXTERNAL_REVIEW",
            "source_v1_manifest_sha256": SOURCE_MANIFEST_SHA,
            "records": updated_manifest,
        }),
    )
    outputs["private_current90_candidate_only"] = write_new(
        private / "PAPER1_FORMAL_D1_REMAINING90_CURRENT_CANDIDATE_ONLY_V3.json",
        json_text({"status": "FOUR_REPAIRS_PENDING_EXTERNAL_REVIEW", "records": new_records}),
    )
    schema_name = "PAPER1_FORMAL_D1_REMAINING90_TARGETED4_PHASE1_IMPORT_SCHEMA_V2.json"
    outputs["reviewer_schema"] = write_new(
        released / schema_name,
        json_text({
            "status": "TARGETED_PHASE1_ONLY_NOT_GROUND_TRUTH",
            "phase1": {"blind_review_id": "exact supplied ID", **ENUMS, "issue_note": "string; text-visible basis or empty"},
            "each_return": "JSON array of exactly four objects; exact seven keys, ID set and packet order",
        }),
    )
    selected_ids = {item["new_blind_review_id"] for item in updated_manifest}
    selected = [row for row in new_records if row["blind_review_id"] in selected_ids]
    if len(selected) != 4:
        raise ValueError("V2 targeted population mismatch")
    for reviewer, order, stem in (
        ("R3-gpt", (0, 2, 1, 3), "R3_GPT"),
        ("R4-codex", (3, 1, 2, 0), "R4_CODEX"),
    ):
        rows = [selected[index] for index in order]
        packet_name = f"PAPER1_FORMAL_D1_REMAINING90_{stem}_TARGETED4_PHASE1_PACKAGE_V2.json"
        prompt_name = f"PAPER1_FORMAL_D1_REMAINING90_{stem}_TARGETED4_PHASE1_PROMPT_V2.md"
        return_name = f"PAPER1_FORMAL_D1_REMAINING90_{stem}_TARGETED4_PHASE1_RAW_RETURN_V2.json"
        outputs[f"{stem.lower()}_packet"] = write_new(
            released / packet_name,
            json_text({"status": "TARGETED_PHASE1_CANDIDATE_ONLY_NOT_GT", "records": rows}),
        )
        outputs[f"{stem.lower()}_prompt"] = write_new(
            released / prompt_name,
            prompt(reviewer, packet_name, schema_name, return_name),
        )
    manifest = {
        "status": "V2_DISTRIBUTION_AUTHORITATIVE_TARGETED4_PHASE1_REVIEW_REQUIRED",
        "supersedes_unreleased_v1": True,
        "source_v1_manifest_sha256": SOURCE_MANIFEST_SHA,
        "source_v1_current90_sha256": SOURCE_CURRENT90_SHA,
        "changed_from_v1_draft": [OLD_REPAIR_ID],
        "new_repair_id": new_id,
        "repaired_count": 4,
        "unchanged_from_original_candidate_count": 86,
        "outputs": outputs,
        "phase2_release_authorized": False,
    }
    record = write_new(
        private / "PAPER1_FORMAL_D1_REMAINING90_AUTHORITY_TARGETED4_RELEASE_MANIFEST_V2.json",
        json_text(manifest),
    )
    print(json_text({"manifest": record, "summary": manifest}))


if __name__ == "__main__":
    main()
