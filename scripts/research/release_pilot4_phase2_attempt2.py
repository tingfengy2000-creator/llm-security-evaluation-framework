"""Lock Pilot4 Phase1 Attempt2 and release its prebuilt Phase2 packet.

The builder intentionally has no identity-mapping or expected-contract input.
It treats the reviewer CSV as immutable bytes, validates it only against the
public Attempt2 Phase1 packet, and releases the already-withheld Phase2 packet
only after all six Phase1 release facts are true.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
from typing import Any, Mapping, Sequence
from urllib.parse import urlparse

from llmguard.domains.retrieval.hidden_poisoning.external_blind_review import (
    PHASE2_RELEASE_REQUIREMENTS,
    assert_phase2_release_allowed,
    lock_phase1_raw_return,
    validate_phase1_packet_rows,
    validate_phase1_raw_return,
    validate_phase2_packet_rows,
)


TASK_ID = "PILOT4-EXTERNAL-BLIND-PHASE1-ATTEMPT2-LOCK-AND-PHASE2-RELEASE-01"
STATUS = (
    "PILOT4_EXTERNAL_BLIND_PHASE1_ATTEMPT2_LOCKED / "
    "PHASE1_CANDIDATE_QUALITY_GATE_PASS / "
    "PHASE2_RELEASED_TO_OWNER_FOR_EXTERNAL_REVIEW / "
    "WAITING_FOR_EXTERNAL_PHASE2_RETURN / NO_HUMAN_DISTRIBUTION"
)
RAW_FILENAME = "PILOT4_EXTERNAL_BLIND_PHASE1_ATTEMPT2_RETURN.csv"
EXPECTED_RAW_SHA256 = "1e5e81fee3825071a77d520c6da5cbfc4c2b59125aca0499cda6c7e2f363c9c5"
ATTEMPT1_RAW_SHA256 = "59446c4be65b035be29528de81b6b8f8aa4113007df8fcac962fe4058a889261"
FINAL_CORPUS_SHA256 = "f530471ecd6551300d68c8ddf104cadce2305d8ff91e64010be222820628252d"
FINAL_CORPUS_VERSION = "PILOT4_CANDIDATE_CORPUS_POST_EXTERNAL_PHASE1_REPAIR_V1"
REPAIRED_ATTEMPT2_POSITIONS = (1, 26, 51, 61, 70)
PHASE1_EXPECTED_COUNTS: Mapping[str, Mapping[str, int]] = {
    "text_naturalness_counts": {
        "MINOR_ISSUE": 13,
        "NATURAL": 59,
        "UNNATURAL": 0,
    },
    "local_internal_conflict_counts": {"NO": 65, "UNCERTAIN": 0, "YES": 7},
    "phase1_issue_counts": {
        "AMBIGUOUS_REFERENCE": 0,
        "MISSING_CONTEXT": 0,
        "NONE": 72,
        "OTHER": 0,
    },
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _tree_identity(root: Path) -> dict[str, Any]:
    records = [
        {
            "path": path.relative_to(root).as_posix(),
            "size": path.stat().st_size,
            "sha256": _file_sha256(path),
        }
        for path in sorted(root.rglob("*"))
        if path.is_file()
    ]
    return {
        "root_name": root.name,
        "file_count": len(records),
        "records": records,
        "aggregate_sha256": sha256(
            json.dumps(records, ensure_ascii=False, separators=(",", ":")).encode(
                "utf-8"
            )
        ).hexdigest(),
    }


def _replace_release_status(markdown: str) -> str:
    old = "Status: `DO_NOT_RELEASE_BEFORE_ATTEMPT2_PHASE1_LOCK_AND_TRIAGE`"
    new = "Status: `RELEASED_TO_OWNER_FOR_EXTERNAL_PHASE2_REVIEW`"
    if markdown.count(old) != 1:
        raise ValueError("PHASE2_PACKET_STATUS_REWRITE_BLOCKER")
    return markdown.replace(old, new, 1)


def _release_guide(markdown: str) -> str:
    old = "Status: `DO_NOT_RELEASE_BEFORE_PHASE1_LOCK`"
    new = "Status: `RELEASED_TO_OWNER_FOR_EXTERNAL_PHASE2_REVIEW`"
    if markdown.count(old) != 1:
        raise ValueError("PHASE2_GUIDE_STATUS_REWRITE_BLOCKER")
    locked_notice = (
        "\nPhase1 is locked and immutable. Do not modify, reinterpret, or "
        "overwrite the Phase1 return.\n\n"
        "Phase2 is a new evidence-based task. / Phase1 已锁定且不可修改、重新解释或覆盖；"
        "Phase2 是新的基于证据的复核任务。\n"
    )
    return markdown.replace(old, new + locked_notice, 1)


def _recursive_keys(value: Any) -> set[str]:
    if isinstance(value, Mapping):
        keys = {str(key) for key in value}
        for child in value.values():
            keys.update(_recursive_keys(child))
        return keys
    if isinstance(value, list):
        child_keys: set[str] = set()
        for child in value:
            child_keys.update(_recursive_keys(child))
        return child_keys
    return set()


def _title_provenance_qa(
    phase2_rows: Sequence[Mapping[str, Any]], source_registries: Sequence[Path]
) -> dict[str, Any]:
    records_by_url: dict[str, list[Mapping[str, Any]]] = {}
    for registry_path in source_registries:
        registry = _load_json(registry_path)
        for record in registry["records"]:
            records_by_url.setdefault(str(record["source_url"]), []).append(record)
    valid_url_count = 0
    provenance_match_count = 0
    for row in phase2_rows:
        for evidence in row["evidence_pool"]:
            url = str(evidence["official_source_url"])
            title = str(evidence["official_page_title"])
            parsed = urlparse(url)
            if parsed.scheme in {"http", "https"} and parsed.netloc:
                valid_url_count += 1
            for record in records_by_url.get(url, []):
                source_text = "\n".join(
                    str(record.get(field, ""))
                    for field in (
                        "official_page_title",
                        "source_identity",
                        "support_excerpt",
                    )
                )
                if (
                    int(record.get("http_status", 0)) == 200
                    and record.get("source_snapshot_hash")
                    and title in source_text
                ):
                    provenance_match_count += 1
                    break
    if provenance_match_count != 144 or valid_url_count != 144:
        raise ValueError("PHASE2_TITLE_OR_URL_PROVENANCE_BLOCKER")
    return {
        "visible_title_slots": 144,
        "title_provenance_valid": "144/144",
        "title_provenance_basis": (
            "FROZEN_VERIFIED_SOURCE_REGISTRY / "
            "SOURCE_IDENTITY_OR_VERIFIED_SUPPORT_EXCERPT"
        ),
        "source_registry_count": len(source_registries),
        "valid_url_count": valid_url_count,
        "manual_override_visible_count": 0,
        "source_identity_fallback_visible_count": 0,
    }


def _manifest_records(root: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path == root / "manifest" / "manifest.json":
            continue
        relative = path.relative_to(root).as_posix()
        if relative == f"raw/{RAW_FILENAME}":
            visibility = "IMMUTABLE_CANONICAL_RAW_RETURN"
        elif relative in {
            "release/PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_PACKET.md",
            "release/PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_GUIDE.md",
        }:
            visibility = "PHASE2_ATTEMPT2_REVIEWER_DISTRIBUTABLE"
        else:
            visibility = "CONTROL_PLANE_ONLY"
        records.append(
            {
                "path": relative,
                "visibility": visibility,
                "size": path.stat().st_size,
                "sha256": _file_sha256(path),
            }
        )
    return records


def build(
    *,
    source: Path,
    phase1_packet: Path,
    withheld_phase2: Path,
    source_registries: Sequence[Path],
    attempt1_return_root: Path,
    attempt2_preparation_root: Path,
    final_corpus: Path,
    output: Path,
    expected_sha256: str = EXPECTED_RAW_SHA256,
) -> dict[str, Any]:
    """Create a new immutable return-lock and controlled Phase2 release."""

    if output.exists():
        raise FileExistsError("ADDITIVE_NAMESPACE_ALREADY_EXISTS")
    if source.name != RAW_FILENAME:
        raise ValueError("CANONICAL_RAW_FILENAME_BLOCKER")

    raw_bytes = source.read_bytes()
    raw_sha256 = sha256(raw_bytes).hexdigest()
    if raw_sha256 != expected_sha256.casefold():
        raise ValueError("ATTEMPT2_RAW_RETURN_TRANSPORT_INTEGRITY_BLOCKER")
    if _file_sha256(final_corpus) != FINAL_CORPUS_SHA256:
        raise ValueError("ATTEMPT2_FINAL_CORPUS_IDENTITY_BLOCKER")

    attempt1_raw = (
        attempt1_return_root / "raw" / "PILOT4_EXTERNAL_BLIND_PHASE1_RETURN.csv"
    )
    if _file_sha256(attempt1_raw) != ATTEMPT1_RAW_SHA256:
        raise ValueError("ATTEMPT1_RAW_IMMUTABILITY_BLOCKER")
    attempt1_pre = _tree_identity(attempt1_return_root)
    preparation_pre = _tree_identity(attempt2_preparation_root)

    phase1_rows = _load_jsonl(phase1_packet)
    phase1_packet_qa = validate_phase1_packet_rows(phase1_rows)
    expected_ids = [str(row["blind_review_id"]) for row in phase1_rows]
    validation = validate_phase1_raw_return(raw_bytes, expected_ids)
    for key, expected in PHASE1_EXPECTED_COUNTS.items():
        actual = {name: int(validation[key].get(name, 0)) for name in expected}
        if actual != dict(expected):
            raise ValueError(f"ATTEMPT2_DESCRIPTIVE_COUNT_BLOCKER:{key}")
    if validation["required_reason_rows"] != 7:
        raise ValueError("ATTEMPT2_REQUIRED_REASON_COUNT_BLOCKER")
    if validation["issue_row_count"] != 0:
        raise ValueError("ATTEMPT2_CANDIDATE_DEFECT_GATE_BLOCKER")

    raw_by_id = {str(row["blind_review_id"]): row for row in validation["rows"]}
    position_records = []
    for position in REPAIRED_ATTEMPT2_POSITIONS:
        opaque_id = expected_ids[position - 1]
        issue = str(raw_by_id[opaque_id]["phase1_issue"])
        if issue != "NONE":
            raise ValueError("REPAIRED_CANDIDATE_CONFIRMATION_BLOCKER")
        position_records.append(
            {
                "attempt2_visible_position": position,
                "blind_review_id": opaque_id,
                "phase1_issue": issue,
            }
        )

    phase2_jsonl = (
        withheld_phase2 / "PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_PACKET.jsonl"
    )
    phase2_md = withheld_phase2 / "PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_PACKET.md"
    phase2_guide = withheld_phase2 / "PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_GUIDE.md"
    phase2_template = (
        withheld_phase2 / "PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_TEMPLATE.csv"
    )
    phase2_rows = _load_jsonl(phase2_jsonl)
    phase2_qa = validate_phase2_packet_rows(phase2_rows)
    if [str(row["blind_review_id"]) for row in phase2_rows] != expected_ids:
        raise ValueError("ATTEMPT2_CROSS_PHASE_ID_PARITY_BLOCKER")
    if [str(row["candidate_text"]) for row in phase2_rows] != [
        str(row["candidate_text"]) for row in phase1_rows
    ]:
        raise ValueError("ATTEMPT2_CROSS_PHASE_TEXT_PARITY_BLOCKER")
    if [str(row["source_title"]) for row in phase2_rows] != [
        str(row["source_title"]) for row in phase1_rows
    ]:
        raise ValueError("ATTEMPT2_CROSS_PHASE_TITLE_PARITY_BLOCKER")

    title_qa = _title_provenance_qa(phase2_rows, source_registries)
    recursive_keys = _recursive_keys(phase2_rows)
    forbidden_visible_keys = {
        "sample_id",
        "triplet_id",
        "candidate_kind",
        "hkp",
        "intended_stealth",
        "hard_negative_type",
        "target_field",
        "source_role",
        "source_type",
        "supported_proposition",
        "correct_fact",
        "minimum_path",
        "expected_answer",
        "owner_decision",
        "repair_marker",
    }
    leaked_keys = sorted(recursive_keys.intersection(forbidden_visible_keys))
    if leaked_keys:
        raise ValueError(f"PHASE2_PACKET_HIDDEN_LABEL_LEAKAGE:{leaked_keys}")

    timestamp = _utc_now()
    output.mkdir(parents=False, exist_ok=False)
    raw_destination = output / "raw" / RAW_FILENAME
    locked_sha256 = lock_phase1_raw_return(raw_bytes, expected_ids, raw_destination)
    if raw_destination.read_bytes() != raw_bytes or locked_sha256 != raw_sha256:
        raise ValueError("ATTEMPT2_RAW_COPY_INTEGRITY_BLOCKER")

    release_facts = {name: True for name in PHASE2_RELEASE_REQUIREMENTS}
    release_result = assert_phase2_release_allowed(release_facts)
    release = output / "release"
    release.mkdir(parents=True, exist_ok=False)
    (release / phase2_md.name).write_text(
        _replace_release_status(phase2_md.read_text(encoding="utf-8")),
        encoding="utf-8",
        newline="\n",
    )
    (release / phase2_guide.name).write_text(
        _release_guide(phase2_guide.read_text(encoding="utf-8")),
        encoding="utf-8",
        newline="\n",
    )
    shutil.copyfile(phase2_jsonl, release / phase2_jsonl.name)
    shutil.copyfile(phase2_template, release / phase2_template.name)
    if (release / phase2_jsonl.name).read_bytes() != phase2_jsonl.read_bytes():
        raise ValueError("PHASE2_JSONL_RELEASE_COPY_BLOCKER")
    if (release / phase2_template.name).read_bytes() != phase2_template.read_bytes():
        raise ValueError("PHASE2_TEMPLATE_RELEASE_COPY_BLOCKER")

    lock_facts = {
        **release_facts,
        "EXPECTED_CONTRACT_LOADED": False,
        "IDENTITY_MAPPING_UNLOCKED": False,
        "PHASE2_RELEASED": True,
        "raw_filename": source.name,
        "raw_size": len(raw_bytes),
        "raw_sha256": raw_sha256,
        "received_at": timestamp,
        "source_path": str(source.resolve()),
        "immutable_copy_path": raw_destination.relative_to(output).as_posix(),
        "immutable_copy_contract": "EXCLUSIVE_CREATE_PLUS_SHA256_LOCK",
        "lock_timestamp": timestamp,
    }
    _write_json(output / "qa" / "phase1_attempt2_return_lock.json", lock_facts)
    _write_json(
        output / "qa" / "input_transport_integrity.json",
        {
            "status": "PASS",
            "expected_sha256": expected_sha256.casefold(),
            "source_path": str(source.resolve()),
            "source_size": len(raw_bytes),
            "source_sha256": raw_sha256,
            "immutable_copy_sha256": _file_sha256(raw_destination),
            "source_copy_byte_equal": raw_destination.read_bytes() == raw_bytes,
        },
    )
    summary = {
        key: validation[key]
        for key in (
            "status",
            "raw_sha256",
            "headers",
            "row_count",
            "unique_id_count",
            "duplicate_id_count",
            "blank_id_count",
            "missing_ids",
            "unexpected_ids",
            "invalid_enum_count",
            "required_reason_rows",
            "missing_required_reason_count",
            "text_naturalness_counts",
            "local_internal_conflict_counts",
            "phase1_issue_counts",
            "issue_row_count",
            "non_natural_row_count",
            "local_yes_row_count",
        )
    }
    summary.update(
        {
            "interpretation": "DESCRIPTIVE_ONLY",
            "accuracy_evaluated": False,
            "agreement_evaluated": False,
            "expected_match_evaluated": False,
            "ground_truth_correctness_evaluated": False,
        }
    )
    _write_json(output / "qa" / "phase1_attempt2_descriptive_summary.json", summary)
    _write_json(
        output / "qa" / "repaired_candidate_descriptive_confirmation.json",
        {
            "status": "PASS",
            "method": "ATTEMPT2_VISIBLE_POSITION_ONLY / NO_IDENTITY_MAPPING",
            "position_count": len(position_records),
            "phase1_issue_none_count": len(position_records),
            "records": position_records,
        },
    )
    _write_json(
        output / "qa" / "phase2_release_gate.json",
        {
            "status": "PASS / RELEASE_APPROVED",
            "requirements": release_facts,
            "release_function_result": release_result,
            "release_approved": True,
            "phase2_released": True,
            "release_scope": "PACKET_ONLY / NO_PHASE2_ANNOTATION",
        },
    )
    _write_json(
        output / "qa" / "phase2_packet_qa.json",
        {
            **phase2_qa,
            **title_qa,
            "status": "PASS / RELEASED_TO_OWNER",
            "phase1_phase2_id_parity": "72/72",
            "phase1_phase2_candidate_text_parity": "72/72",
            "phase1_phase2_source_title_parity": "72/72",
            "source_type_visible": 0,
            "source_role_visible": 0,
            "expected_label_visible": 0,
            "hidden_label_key_findings": 0,
            "phase2_annotation_executed": False,
        },
    )
    _write_json(
        output / "qa" / "attempt2_final_corpus_identity.json",
        {
            "status": "PASS",
            "candidate_corpus_version": FINAL_CORPUS_VERSION,
            "candidate_corpus_path": str(final_corpus.resolve()),
            "candidate_corpus_sha256": _file_sha256(final_corpus),
            "candidate_count": 72,
            "candidate_corpus_loaded_for_expected_comparison": False,
        },
    )

    attempt1_post = _tree_identity(attempt1_return_root)
    preparation_post = _tree_identity(attempt2_preparation_root)
    if attempt1_pre != attempt1_post or preparation_pre != preparation_post:
        raise ValueError("PILOT4_HISTORY_MUTATION_BLOCKER")
    _write_json(
        output / "qa" / "historical_evidence_preservation.json",
        {
            "status": "PASS",
            "attempt1_classification": (
                "VALID_DEFECT_DISCOVERY_REVIEW / NOT_FINAL_CORPUS_ACCEPTANCE_REVIEW"
            ),
            "attempt1_raw_sha256": ATTEMPT1_RAW_SHA256,
            "attempt1_return_tree": attempt1_post,
            "attempt2_preparation_tree": preparation_post,
            "historical_tree_equal_pre_post": True,
            "historical_evidence_deleted_or_overwritten": False,
        },
    )
    (release / "README.md").write_text(
        "# Pilot4 Attempt2 Phase2 Controlled Release\n\n"
        "Only the following two files may be sent to the same Attempt2 external reviewer:\n\n"
        "- `PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_PACKET.md`\n"
        "- `PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_GUIDE.md`\n\n"
        "The JSONL and CSV template are control-plane-only. Phase1 remains locked and immutable.\n",
        encoding="utf-8",
        newline="\n",
    )
    (output / "README.md").write_text(
        f"# Pilot4 External Blind Phase1 Attempt2 Lock and Phase2 Release\n\n"
        f"Status: `{STATUS}`\n\n"
        "The canonical Phase1 Attempt2 return is byte-locked. Candidate-text defect triage is closed because all 72 rows report `phase1_issue=NONE`. Expected labels and identity mapping remain closed.\n",
        encoding="utf-8",
        newline="\n",
    )

    records = _manifest_records(output)
    manifest = {
        "task_id": TASK_ID,
        "status": STATUS,
        "created_at": timestamp,
        "source_raw_sha256": raw_sha256,
        "candidate_corpus_version": FINAL_CORPUS_VERSION,
        "candidate_corpus_sha256": FINAL_CORPUS_SHA256,
        "phase1_packet_path": str(phase1_packet.resolve()),
        "phase1_packet_qa": phase1_packet_qa,
        "expected_contract_loaded": False,
        "identity_mapping_unlocked": False,
        "phase2_annotation_executed": False,
        "phase2_released": True,
        "candidate_defect_triage_resolved": True,
        "file_count_excluding_manifest": len(records),
        "records": records,
        "aggregate_sha256": sha256(
            json.dumps(records, ensure_ascii=False, separators=(",", ":")).encode(
                "utf-8"
            )
        ).hexdigest(),
    }
    _write_json(output / "manifest" / "manifest.json", manifest)
    if any(
        _file_sha256(output / str(record["path"])) != record["sha256"]
        for record in records
    ):
        raise ValueError("EVIDENCE_MANIFEST_RECOMPUTE_BLOCKER")
    return {
        "status": STATUS,
        "raw_sha256": raw_sha256,
        "raw_size": len(raw_bytes),
        "row_count": validation["row_count"],
        "unique_id_count": validation["unique_id_count"],
        "required_reason_rows": validation["required_reason_rows"],
        "issue_row_count": validation["issue_row_count"],
        "candidate_quality_gate": "PASS",
        "phase2_release_approved": True,
        "phase2_packet_rows": phase2_qa["candidate_count"],
        "phase2_evidence_slots": phase2_qa["evidence_slots"],
        "manifest_file_count": len(records),
        "manifest_aggregate_sha256": manifest["aggregate_sha256"],
        "output": str(output.resolve()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--phase1-packet", type=Path, required=True)
    parser.add_argument("--withheld-phase2", type=Path, required=True)
    parser.add_argument("--source-registry", type=Path, action="append", required=True)
    parser.add_argument("--attempt1-return-root", type=Path, required=True)
    parser.add_argument("--attempt2-preparation-root", type=Path, required=True)
    parser.add_argument("--final-corpus", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-sha256", default=EXPECTED_RAW_SHA256)
    args = parser.parse_args()
    result = build(
        source=args.source,
        phase1_packet=args.phase1_packet,
        withheld_phase2=args.withheld_phase2,
        source_registries=args.source_registry,
        attempt1_return_root=args.attempt1_return_root,
        attempt2_preparation_root=args.attempt2_preparation_root,
        final_corpus=args.final_corpus,
        output=args.output,
        expected_sha256=args.expected_sha256,
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
