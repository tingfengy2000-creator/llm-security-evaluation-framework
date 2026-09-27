"""Lock and release one candidate-only, 90-row D1 Phase1 blind MegaWave.

Role-bearing mapping and construction audits remain outside reviewer_release.
No reviewer response, Expected/GT, or Phase2 material is read here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from formal240_d1_remaining90_megawave_audit import FILES, run, sha


SEED = 2026092701
ENUMS = {
    "text_naturalness": ["NATURAL", "MINOR_ISSUE", "UNNATURAL"],
    "local_internal_conflict": ["YES", "NO", "UNCERTAIN"],
    "self_containment": ["PASS", "FLAG", "UNCERTAIN"],
    "ambiguous_referent": ["YES", "NO", "UNCERTAIN"],
    "meta_or_template_language": ["YES", "NO", "UNCERTAIN"],
}
REVIEWER_NAMES = {"R3": "R3_GPT", "R4": "R4_CODEX"}


def write_new(path: Path, content: str) -> None:
    if path.exists():
        raise ValueError(f"Refusing to overwrite immutable output: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content.encode("utf-8"))


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def opaque_id(sample_id: str) -> str:
    digest = hashlib.sha256(f"D1_REMAINING90_PHASE1_V1|{sample_id}".encode()).hexdigest()
    return f"D1BR-{digest[:12].upper()}"


def shuffled(rows: list[dict[str, Any]], seed: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    for _ in range(100_000):
        result = rows.copy()
        rng.shuffle(result)
        if any(result[i]["group_slot_id"] == result[i + 1]["group_slot_id"] for i in range(89)):
            continue
        if any(len({result[i + j]["hkp"] for j in range(3)}) == 1 for i in range(88)):
            continue
        return result
    raise ValueError("Could not construct cross-group, cross-HKP shuffle")


def prompt(reviewer: str, package: str, schema: str, output: str) -> str:
    environment = (
        "Create a fresh, independent GPT session/account for this review."
        if reviewer == "R3"
        else "Create a NEW projectless Codex task in an empty directory, not a new Codex Project. "
        "Do not attach any saved Git project or reuse a previous task. The earlier HKP1 new-Project "
        "exception does not apply to this MegaWave."
    )
    return f"""# D1 Remaining90 Phase1 — {reviewer} independent blind quality review

{environment} Work alone. Receive exactly these three files: `{package}`, `{schema}`, and this prompt. Do not open any repository, E: handoff directory, AGENTS/project instructions, Owner/construction files, older answers, other reviewers' output, Evidence/Phase2 files, mapping, labels, Expected, or GT. Do not browse the web or use another AI. If any prohibited context is visible, stop and tell Owner in a separate incident file.

This is pre-annotation quality review, **not Ground Truth**. Read each `candidate_text` on its own. Do not infer hidden intent or determine real-world legal correctness. For every opaque `blind_review_id` fill exactly:

- `text_naturalness`: `NATURAL` = clear ordinary wording, even if a fact may be wrong; `MINOR_ISSUE` = slight awkwardness but understandable; `UNNATURAL` = serious wording/grammar defect.
- `local_internal_conflict`: `YES` only when two visible claims in the same candidate cannot both hold under the same subject, scope, time and condition; `NO` if verifying a suspected error needs outside facts; `UNCERTAIN` only when the text itself obscures whether there is an internal conflict.
- `self_containment`: `PASS` if the subject and core claim make sense without another candidate; `FLAG` if essential context is absent; `UNCERTAIN` if the text leaves this undecidable.
- `ambiguous_referent`: `YES` only if a key reference can point to multiple visible antecedents; `NO` otherwise; `UNCERTAIN` if unresolved from this text.
- `meta_or_template_language`: `YES` for visible experimental, placeholder or template residue; `NO` otherwise; `UNCERTAIN` if unclear.
- `issue_note`: a concise text-visible reason for any non-default/uncertain/flagged value, otherwise an empty string. Do not cite sources or guess the experimental label. A real-world fact suspicion is not an internal contradiction.

Save ONE UTF-8 strict JSON file named `{output}`. It must be a JSON **array of exactly 90 objects**, in exactly the package order, with exactly the seven schema keys, canonical English enum strings, all supplied IDs unchanged and no extra fields. No Markdown fences, commentary, or explanation outside the JSON file. Before submission, self-check JSON parse, 90 unique IDs, exact ID set/order, enum spellings, nonblank issue notes when flagged, and no truncation. Send the original saved file to Owner; do not reformat or resave it. Do not view Phase2 until Owner confirms both Phase1 raw files were byte-locked and accepted. Remain in this SAME isolated session for later Phase2 if authorized.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    for hkp in ("hkp2", "hkp3", "hkp4"):
        parser.add_argument(f"--{hkp}-root", required=True, type=Path)
    parser.add_argument("--audit", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()
    roots = {h.upper(): getattr(args, f"{h}_root") for h in ("hkp2", "hkp3", "hkp4")}
    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    fresh = run(roots)
    if audit["status"] != "REMAINING90_INTERNAL_CROSS_BATCH_GATE_PASS_EXTERNAL_REVIEW_PENDING":
        raise ValueError("Locked cross-batch audit did not pass")
    for key in ("source_artifact_hashes", "candidate_count", "group_count", "role_counts", "target_s_candidate_counts"):
        if audit[key] != fresh[key]:
            raise ValueError(f"Audit/source drift in {key}")
    if fresh["errors"] or fresh["alerts_requiring_owner_reading_not_automatic_failure"]:
        raise ValueError("Cross-batch gate failed or needs reading")
    if args.output_root.exists():
        raise ValueError("Refusing to reuse reviewer release namespace")

    rows: list[dict[str, Any]] = []
    for hkp, root in roots.items():
        path = root / FILES[hkp][0]
        for line in path.read_text(encoding="utf-8").splitlines():
            rows.append({"hkp": hkp, **json.loads(line)})
    if len(rows) != 90 or len({row["sample_id"] for row in rows}) != 90:
        raise ValueError("Invalid population")
    mapping = [
        {
            "blind_review_id": opaque_id(row["sample_id"]),
            "sample_id": row["sample_id"],
            "group_slot_id": row["group_slot_id"],
            "role": row["role"],
            "hkp": row["hkp"],
            "target_s": row["target_s"],
            "candidate_version": row["candidate_version"],
            "family_cluster_id": row["family_cluster_id"],
        }
        for row in rows
    ]
    if len({item["blind_review_id"] for item in mapping}) != 90:
        raise ValueError("Blind ID collision")

    private = args.output_root / "control_only_do_not_send"
    release = args.output_root / "reviewer_release"
    release.mkdir(parents=True, exist_ok=False)
    mapping_path = private / "PAPER1_FORMAL_D1_REMAINING90_PHASE1_IDENTITY_MAPPING_PRIVATE_V1.json"
    write_new(mapping_path, json_text({"status": "SEALED_CONTROL_ONLY", "records": mapping}))

    schema_name = "PAPER1_FORMAL_D1_REMAINING90_PHASE1_IMPORT_SCHEMA_V1.json"
    schema = {
        "status": "PHASE1_ONLY_NOT_GROUND_TRUTH",
        "phase1": {"blind_review_id": "exact supplied ID", **ENUMS, "issue_note": "string; concise text-visible basis or empty"},
        "each_return": "JSON array of exactly 90 objects; exact seven keys, ID set and reviewer-specific packet order",
    }
    write_new(release / schema_name, json_text(schema))
    package_names = {}
    for offset, reviewer in enumerate(("R3", "R4")):
        name = REVIEWER_NAMES[reviewer]
        package_name = f"PAPER1_FORMAL_D1_REMAINING90_{name}_PHASE1_PACKAGE_V1.json"
        prompt_name = f"PAPER1_FORMAL_D1_REMAINING90_{name}_PHASE1_PROMPT_V1.md"
        output_name = f"PAPER1_FORMAL_D1_REMAINING90_{name}_PHASE1_RAW_RETURN_V1.json"
        ordered = shuffled(rows, SEED + offset)
        records = [{"blind_review_id": opaque_id(row["sample_id"]), "candidate_text": row["candidate_text"]} for row in ordered]
        if len(records) != 90 or len({r["blind_review_id"] for r in records}) != 90:
            raise ValueError("Package population failure")
        write_new(release / package_name, json_text({"status": "PHASE1_CANDIDATE_ONLY_PREANNOTATION_QA_NOT_GT", "records": records}))
        write_new(release / prompt_name, prompt(reviewer, package_name, schema_name, output_name))
        package_names[reviewer] = {"package": package_name, "prompt": prompt_name, "raw_return_expected": output_name}

    r3 = json.loads((release / package_names["R3"]["package"]).read_text(encoding="utf-8"))["records"]
    r4 = json.loads((release / package_names["R4"]["package"]).read_text(encoding="utf-8"))["records"]
    if {r["blind_review_id"]: r["candidate_text"] for r in r3} != {
        r["blind_review_id"]: r["candidate_text"] for r in r4
    }:
        raise ValueError("R3/R4 content parity failure")
    if [r["blind_review_id"] for r in r3] == [r["blind_review_id"] for r in r4]:
        raise ValueError("Reviewer order should differ")
    forbidden = ("sample_id", "group_slot_id", "CLEAN_CURRENT", "HARD_NEGATIVE", "POISON", "HKP", "target_s", "mapping", "Expected", "Ground Truth")
    for path in release.iterdir():
        body = path.read_text(encoding="utf-8")
        if path.suffix == ".json" and "PACKAGE" in path.name:
            data = json.loads(body)
            if any(set(record) != {"blind_review_id", "candidate_text"} for record in data["records"]):
                raise ValueError(f"Blind package schema leakage: {path}")
            if any(word in body for word in forbidden):
                raise ValueError(f"Blind package string leakage: {path}")
    manifest = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "D1_REMAINING90_PHASE1_READY_STOP_EXTERNAL_REVIEW_REQUIRED",
        "cross_batch_audit_path": str(args.audit),
        "cross_batch_audit_sha256": sha(args.audit),
        "source_artifact_hashes": audit["source_artifact_hashes"],
        "identity_mapping_path": str(mapping_path),
        "identity_mapping_sha256": sha(mapping_path),
        "record_count": 90,
        "group_count": 30,
        "role_counts_control_only": dict(Counter(row["role"] for row in rows)),
        "reviewer_file_hashes": {path.name: sha(path) for path in release.iterdir()},
        "reviewer_files": package_names,
        "schema": schema_name,
        "R4_environment": "NEW_PROJECTLESS_EMPTY_DIRECTORY_NO_REPOSITORY; OWNER_ATTESTATION_REQUIRED",
        "Phase2_release": False,
        "Human_AB": False,
        "Ground_Truth": False,
        "formal_split": False,
        "detector_training": False,
    }
    manifest_path = private / "PAPER1_FORMAL_D1_REMAINING90_PHASE1_RELEASE_LOCK_MANIFEST_V1.json"
    write_new(manifest_path, json_text(manifest))
    print(manifest["status"], len(rows), sha(manifest_path), str(args.output_root))


if __name__ == "__main__":
    main()
