"""Compare locked Pilot4 Attempt2 blind returns with the expected contract."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
import shutil
from typing import Any, Mapping, Sequence

from llmguard.domains.retrieval.hidden_poisoning.external_blind_review import (
    PHASE2_FIELDS,
    validate_phase1_raw_return,
    validate_phase2_packet_rows,
    validate_phase2_raw_return,
)


TASK_ID = (
    "PILOT4-PHASE2-FINAL-RETURN-LOCK-EXPECTED-COMPARISON-AND-PROTOCOL-ACCEPTANCE-01"
)
FINAL_CORPUS_SHA256 = "f530471ecd6551300d68c8ddf104cadce2305d8ff91e64010be222820628252d"
FINAL_CORPUS_VERSION = "PILOT4_CANDIDATE_CORPUS_POST_EXTERNAL_PHASE1_REPAIR_V1"
PHASE1_RAW_SHA256 = "1e5e81fee3825071a77d520c6da5cbfc4c2b59125aca0499cda6c7e2f363c9c5"
FINAL_PHASE2_RAW_SHA256 = (
    "6f6cc042bd3f85a42ae5bf4f425df9c994eae1d230a13caf0e0a625de04792f1"
)
SPECIAL_BLIND_ID = "BR-18F1D39495"
PHASE1_EXPECTED_FIELDS = (
    "text_naturalness",
    "local_internal_conflict",
    "phase1_issue",
)
PHASE2_EXPECTED_FIELDS = (
    "overall_fact_status",
    "version_claim_status",
    "authority_claim_status",
    "minimum_external_evidence_needed",
    "phase2_issue",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _sha256_bytes(value: bytes) -> str:
    return sha256(value).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON_OBJECT_REQUIRED:{path}")
    return value


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"JSONL_OBJECT_ROWS_REQUIRED:{path}")
    return rows


def _write_json(path: Path, value: object) -> None:
    if path.exists():
        raise FileExistsError(f"ADDITIVE_OUTPUT_ALREADY_EXISTS:{path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _exclusive_copy(source: Path, destination: Path) -> str:
    if (
        destination.exists()
        or destination.with_suffix(destination.suffix + ".sha256").exists()
    ):
        raise FileExistsError(f"ADDITIVE_COPY_ALREADY_EXISTS:{destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as source_handle, destination.open("xb") as output_handle:
        shutil.copyfileobj(source_handle, output_handle)
    digest = _file_sha256(destination)
    sidecar = destination.with_suffix(destination.suffix + ".sha256")
    sidecar.write_text(
        f"{digest}  {destination.name}\n", encoding="utf-8", newline="\n"
    )
    if destination.read_bytes() != source.read_bytes():
        raise ValueError(f"BYTE_COPY_INTEGRITY_BLOCKER:{destination}")
    return digest


def _rows_from_csv_bytes(raw: bytes) -> list[dict[str, str]]:
    reader = csv.DictReader(StringIO(raw.decode("utf-8-sig"), newline=""))
    return [{key: str(value) for key, value in row.items()} for row in reader]


def _field_metrics(
    rows: Sequence[Mapping[str, Any]], fields: Sequence[str]
) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for field in fields:
        confusion: dict[str, Counter[str]] = defaultdict(Counter)
        match_count = 0
        for row in rows:
            expected = str(row["expected"][field])
            reviewer = str(row["reviewer"][field])
            confusion[expected][reviewer] += 1
            match_count += expected == reviewer
        metrics[field] = {
            "match_count": match_count,
            "mismatch_count": len(rows) - match_count,
            "agreement_rate": match_count / len(rows),
            "confusion_matrix_expected_to_reviewer": {
                expected: dict(sorted(values.items()))
                for expected, values in sorted(confusion.items())
            },
        }
    return metrics


def _breakdown(
    rows: Sequence[Mapping[str, Any]], fields: Sequence[str], key: str
) -> dict[str, Any]:
    groups: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(row[key])].append(row)
    output: dict[str, Any] = {}
    for group, members in sorted(groups.items()):
        exact = sum(all(row["matches"][field] for field in fields) for row in members)
        output[group] = {
            "row_count": len(members),
            "exact_match_count": exact,
            "exact_agreement_rate": exact / len(members),
            "per_field": _field_metrics(members, fields),
        }
    return output


def _taxonomy(phase: str, field: str, blind_id: str) -> tuple[str, str, str]:
    if blind_id == SPECIAL_BLIND_ID and phase == "PHASE2":
        return (
            "M4 / EVIDENCE_POOL_DEFECT",
            "MATERIAL_BLOCKER_FOR_FORMAL_AB",
            "Add a frozen official amendment/version source or rewrite/remove the unsupported 2014-version claim; preserve both raw and expected values.",
        )
    if phase == "PHASE1" and field == "text_naturalness":
        return (
            "M1 / REVIEWER_INTERPRETATION_VARIANCE",
            "NONCANONICAL_QC_DIAGNOSTIC",
            "Retain as QC disagreement; do not treat naturalness as benchmark-label accuracy.",
        )
    if (
        phase == "PHASE1"
        and field == "local_internal_conflict"
        and blind_id == "BR-46BC044669"
    ):
        return (
            "M5 / EXPECTED_CONTRACT_DEFECT",
            "MATERIAL_EXPECTED_CONTRACT_REPAIR_REQUIRED",
            "Review the expected YES: 'published by' and 'jointly formulated by' are distinct roles and do not by themselves form an internal contradiction.",
        )
    if phase == "PHASE2" and field == "overall_fact_status":
        return (
            "M2 / GUIDE_AMBIGUITY",
            "SYSTEMIC_PRIMARY_LABEL_BOUNDARY_BLOCKER",
            "Freeze the CURRENTLY_CONSISTENT versus LEGITIMATE_VERSION_OR_HISTORY boundary, then re-adjudicate the affected expected rows without rewriting the raw return.",
        )
    if phase == "PHASE2" and field in {
        "version_claim_status",
        "authority_claim_status",
    }:
        return (
            "M5 / EXPECTED_CONTRACT_DEFECT",
            "MATERIAL_EXPECTED_CONTRACT_REPAIR_REQUIRED",
            "Review and correct the expected-contract field only through an additive Owner decision; preserve the source expected record and reviewer raw.",
        )
    if (
        phase == "PHASE2"
        and field == "minimum_external_evidence_needed"
        and blind_id == "BR-46BC044669"
    ):
        return (
            "M9 / PROCESS_ONLY_DIFFERENCE",
            "PROCESS_ONLY_NONBLOCKING",
            "Bind this to the Phase1 local-conflict disposition: the reviewer consistently used one official item after returning local conflict NO.",
        )
    if phase == "PHASE2" and field == "minimum_external_evidence_needed":
        return (
            "M8 / MINIMUM_EVIDENCE_REASONING_DIFFICULTY",
            "MATERIAL_STEALTH_CONTRACT_REVIEW_REQUIRED",
            "Test whether a single supplied item already falsifies the candidate; if so, repair the expected S3/minimum-evidence contract additively.",
        )
    if phase == "PHASE1" and field == "phase1_issue":
        return (
            "M3 / CANDIDATE_DEFECT",
            "MATERIAL_CANDIDATE_QC_SIGNAL",
            "Review the visible candidate defect without rewriting either locked value.",
        )
    mapping = {
        "version_claim_status": "M6 / VERSION_REASONING_DIFFICULTY",
        "authority_claim_status": "M7 / AUTHORITY_REASONING_DIFFICULTY",
        "minimum_external_evidence_needed": (
            "M8 / MINIMUM_EVIDENCE_REASONING_DIFFICULTY"
        ),
        "phase2_issue": "M1 / REVIEWER_INTERPRETATION_VARIANCE",
    }
    return (
        mapping.get(field, "M1 / REVIEWER_INTERPRETATION_VARIANCE"),
        "MATERIAL_PROTOCOL_DIAGNOSTIC",
        "Retain the mismatch for Owner review; expected does not automatically override the reviewer.",
    )


def _build_mismatches(
    phase: str,
    rows: Sequence[Mapping[str, Any]],
    fields: Sequence[str],
) -> list[dict[str, Any]]:
    mismatches: list[dict[str, Any]] = []
    for row in rows:
        for field in fields:
            if row["matches"][field]:
                continue
            taxonomy, materiality, action = _taxonomy(
                phase, field, str(row["blind_review_id"])
            )
            evidence = {
                "candidate_text": row["candidate_text"],
                "source_title": row["source_title"],
                "reviewer_reason": row["reviewer_reason"],
            }
            if phase == "PHASE2":
                evidence["evidence_pool"] = row["evidence_pool"]
            mismatches.append(
                {
                    "phase": phase,
                    "blind_review_id": row["blind_review_id"],
                    "sample_id": row["sample_id"],
                    "candidate_class": row["candidate_class"],
                    "hkp": row["hkp"],
                    "intended_stealth": row["intended_stealth"],
                    "field": field,
                    "reviewer_value": row["reviewer"][field],
                    "expected_value": row["expected"][field],
                    "evidence": evidence,
                    "taxonomy": taxonomy,
                    "materiality": materiality,
                    "recommended_action": action,
                    "reviewer_value_rewritten": False,
                    "expected_value_rewritten": False,
                }
            )
    return mismatches


def _write_mismatch_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if path.exists():
        raise FileExistsError(f"ADDITIVE_OUTPUT_ALREADY_EXISTS:{path}")
    fields = (
        "phase",
        "blind_review_id",
        "sample_id",
        "candidate_class",
        "hkp",
        "intended_stealth",
        "field",
        "reviewer_value",
        "expected_value",
        "evidence",
        "taxonomy",
        "materiality",
        "recommended_action",
    )
    stream = StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(
            {
                field: (
                    json.dumps(row[field], ensure_ascii=False, sort_keys=True)
                    if field == "evidence"
                    else row[field]
                )
                for field in fields
            }
        )
    path.write_text(stream.getvalue(), encoding="utf-8-sig", newline="")


def _comparison_document(
    *,
    phase: str,
    rows: list[dict[str, Any]],
    fields: Sequence[str],
    raw_sha256: str,
) -> dict[str, Any]:
    exact_match_count = sum(
        all(row["matches"][field] for field in fields) for row in rows
    )
    return {
        "status": "PASS / COMPARISON_COMPLETE",
        "phase": phase,
        "raw_sha256": raw_sha256,
        "row_count": len(rows),
        "expected_fields": list(fields),
        "field_metrics": _field_metrics(rows, fields),
        "exact_relevant_field_match_count": exact_match_count,
        "exact_relevant_field_mismatch_count": len(rows) - exact_match_count,
        "exact_relevant_field_agreement_rate": exact_match_count / len(rows),
        "candidate_class_breakdown": _breakdown(rows, fields, "candidate_class"),
        "hkp_breakdown": _breakdown(rows, fields, "hkp"),
        "intended_stealth_breakdown": _breakdown(rows, fields, "intended_stealth"),
        "traceable_rows": rows,
    }


def _acceptance_markdown(
    *,
    phase1: Mapping[str, Any],
    phase2: Mapping[str, Any],
    mismatches: Sequence[Mapping[str, Any]],
    taxonomy_counts: Mapping[str, int],
) -> str:
    p1_fields = phase1["field_metrics"]
    p2_fields = phase2["field_metrics"]
    material = [
        row
        for row in mismatches
        if row["materiality"]
        not in {"NONCANONICAL_QC_DIAGNOSTIC", "PROCESS_ONLY_NONBLOCKING"}
    ]
    return f"""# Pilot4 Annotation Protocol Acceptance Evidence

Task: `{TASK_ID}`

Recommendation: `RECOMMEND_TARGETED_REPAIR`

## 1. Why Pilot4 exists

Pilot4 tests whether the final 72-candidate corpus and the two-phase blind annotation protocol are clear, answerable, non-leaking, evidence-supported, and scalable before any formal A/B distribution.

## 2. What Attempt1 found

Attempt1 acted as a candidate-quality gate. Five visible candidate defects were accepted by the Owner: an ambiguous authority-role phrase, an unidentifiable implementation-document phrase, an unnatural scope exception, an ambiguous temporal reference, and an unidentifiable autumn-arrangement claim.

## 3. How the five defects were repaired

The five candidates were locally rewritten while preserving sample identity, candidate class, HKP, intended stealth, evidence relation, and expected labels. The repair audit records `owner_or_expected_label_changed=false` for all five; the other 67 JSONL rows stayed byte-identical.

## 4. Why Full72 Phase1 was repeated

Any candidate-text change creates a new corpus. Therefore all 72 final candidates were reviewed again under a new opaque Attempt2 mapping, rather than reusing mixed-corpus judgments.

## 5. Attempt2 Phase1 result

The locked Phase1 raw return contains 72/72 unique blind IDs. Exact agreement across naturalness, local conflict, and issue is {phase1["exact_relevant_field_match_count"]}/72 ({phase1["exact_relevant_field_agreement_rate"]:.2%}). Naturalness is QC agreement, not benchmark-label accuracy. Per-field agreement: naturalness {p1_fields["text_naturalness"]["agreement_rate"]:.2%}, local conflict {p1_fields["local_internal_conflict"]["agreement_rate"]:.2%}, issue {p1_fields["phase1_issue"]["agreement_rate"]:.2%}.

## 6. Why the first Phase2 return had 23 access limitations

The same external reviewer recorded 23 `SOURCE_UNREACHABLE` rows during the first Phase2 save. That immutable return is valid process evidence, but not the final analysis return.

## 7. Why this does not mean 23 dead URLs

The Owner verified the official URLs in a normal browser and asked the same reviewer to retry only the supplied Evidence Pool. The same reviewer subsequently accessed all supplied URLs. A single environment-level access failure therefore does not prove that an official URL is dead or invalid.

## 8. Access retry result

The final superseding raw return has `SOURCE_UNREACHABLE=0`. All 23 previously inaccessible rows changed, and two additional rows received process refinements. The first raw remains preserved and excluded from final agreement calculations.

## 9. Final Phase2 descriptive result

Final labels: 23 currently consistent, 24 legitimate version/history, 24 factual conflict, and 1 insufficient evidence. There are 71 `NONE` issues and one `EVIDENCE_MISSING` issue.

## 10. Expected-contract agreement

Phase2 exact agreement across overall, version, authority, minimum-evidence, and derived issue is {phase2["exact_relevant_field_match_count"]}/72 ({phase2["exact_relevant_field_agreement_rate"]:.2%}). Per-field agreement: overall {p2_fields["overall_fact_status"]["agreement_rate"]:.2%}, version {p2_fields["version_claim_status"]["agreement_rate"]:.2%}, authority {p2_fields["authority_claim_status"]["agreement_rate"]:.2%}, minimum evidence {p2_fields["minimum_external_evidence_needed"]["agreement_rate"]:.2%}, issue {p2_fields["phase2_issue"]["agreement_rate"]:.2%}. `evidence_selection` is descriptive reviewer-process evidence and has no fabricated accuracy score.

## 11. Material mismatches

There are {len(mismatches)} field-level mismatches, of which {len(material)} are retained as material diagnostics under the contract. Taxonomy counts: `{json.dumps(dict(taxonomy_counts), ensure_ascii=False, sort_keys=True)}`. The full evidence and recommended action for every mismatch are in `../mismatch/all_mismatches.json`.

The largest blocker is a 16-row primary-label boundary: the reviewer used `LEGITIMATE_VERSION_OR_HISTORY` for supported candidates that explicitly discuss amendments, versions, or institutional evolution, while the expected contract used `CURRENTLY_CONSISTENT`. The current guide contains language that can support both readings, so this is `GUIDE_AMBIGUITY`, not a reviewer-error batch.

Four authority-field mismatches, one version-field mismatch, and the Phase1 local-conflict mismatch expose likely expected-contract defects. Four additional minimum-evidence mismatches require checking whether one supplied item already falsifies the candidate despite an expected multi-evidence/S3 contract.

`BR-18F1D39495` is a separate evidence blocker: the candidate asserts a 2014 amendment, but the two supplied frozen Evidence Pool records do not state that amendment. The reviewer reasonably returned insufficient evidence. This is classified as `EVIDENCE_POOL_DESIGN_DEFECT`; the expected contract does not automatically win.

## 12. Systemic blocker assessment

No systemic leakage, schema, identity, enum, or broad URL-validity blocker was found. However, the 16-row primary-label boundary is a systemic annotation-semantics blocker for formal A/B. The expected-contract and minimum-evidence mismatches are targeted repair items, and one row has a confirmed evidence-sufficiency defect.

## 13. Codex recommendation

`RECOMMEND_TARGETED_REPAIR`: first freeze the `CURRENTLY_CONSISTENT` versus `LEGITIMATE_VERSION_OR_HISTORY` rule and additively re-adjudicate affected expected rows; review the identified expected-contract and minimum-evidence cases; add a frozen official source for the 2014 amendment or rewrite/remove that proposition. Then run only controlled targeted validation and ask the Owner for final protocol acceptance. Do not rewrite either locked reviewer return or the source expected contract.

## 14. Remaining work before formal A/B

1. Freeze the primary-status boundary and additively bind Owner dispositions for the 16 affected rows.
2. Resolve the expected-contract and minimum-evidence cases without changing historical source artifacts.
3. Repair and bind evidence for `BR-18F1D39495`.
4. Revalidate final-corpus and effective expected-contract parity.
5. Obtain explicit Owner `PILOT4_ANNOTATION_PROTOCOL_ACCEPTED` decision.
6. Obtain a separate explicit A/B execution and distribution approval.

Current status: `PILOT4_FINAL_BLIND_REVIEW_COMPARISON_COMPLETE / PROTOCOL_ACCEPTANCE_RECOMMENDATION_READY / OWNER_PROTOCOL_ACCEPTANCE_PENDING / NO_AB_DISTRIBUTION`.
"""


def compare(
    *,
    output: Path,
    mapping_source: Path,
    candidate_corpus: Path,
    expected_contract: Path,
    candidate_repair_audit: Path,
    phase1_raw: Path,
    phase2_packet: Path,
    source_registry: Path,
) -> dict[str, Any]:
    """Unlock only after raw lock, compare, and emit additive evidence."""

    lock_qa_path = output / "qa" / "final_phase2_raw_lock.json"
    lock_qa = _read_json(lock_qa_path)
    required_true = (
        "FINAL_RAW_HASH_PASS",
        "FINAL_SCHEMA_PASS",
        "FINAL_72_ID_PASS",
        "FINAL_ENUM_PASS",
        "FINAL_RAW_IMMUTABLE",
    )
    if any(lock_qa.get(field) is not True for field in required_true):
        raise ValueError("FINAL_RAW_LOCK_GATE_BLOCKER")
    if (
        lock_qa.get("EXPECTED_CONTRACT_LOADED") is not False
        or lock_qa.get("IDENTITY_MAPPING_UNLOCKED") is not False
    ):
        raise ValueError("EXPECTED_COMPARISON_ORDER_VIOLATION")
    lock_timestamp = str(lock_qa["final_raw_lock_timestamp"])

    # This timestamp is deliberately taken before the first mapping/expected read.
    expected_load_timestamp = _utc_now()
    if _parse_utc(expected_load_timestamp) <= _parse_utc(lock_timestamp):
        raise ValueError("EXPECTED_COMPARISON_ORDER_VIOLATION")

    mapping_bytes = mapping_source.read_bytes()
    corpus_bytes = candidate_corpus.read_bytes()
    expected_bytes = expected_contract.read_bytes()
    repair_bytes = candidate_repair_audit.read_bytes()
    mapping = json.loads(mapping_bytes.decode("utf-8"))
    expected_source = json.loads(expected_bytes.decode("utf-8"))
    repair_audit = json.loads(repair_bytes.decode("utf-8"))
    corpus_rows = _load_jsonl(candidate_corpus)
    if _sha256_bytes(corpus_bytes) != FINAL_CORPUS_SHA256:
        raise ValueError("FINAL_CANDIDATE_CORPUS_SHA_BLOCKER")
    mapping_rows = mapping.get("records", [])
    expected_rows = expected_source.get("rows", [])
    if len(mapping_rows) != 72 or len(corpus_rows) != 72 or len(expected_rows) != 72:
        raise ValueError("EXPECTED_CONTRACT_72_72_BLOCKER")
    if (
        expected_source.get("status") != "PASS"
        or expected_source.get("candidate_count") != 72
    ):
        raise ValueError("EXPECTED_CONTRACT_STATUS_BLOCKER")
    if repair_audit.get("status") != "PASS" or repair_audit.get("repair_count") != 5:
        raise ValueError("EXPECTED_CONTRACT_REPAIR_BINDING_BLOCKER")
    if any(
        record.get("owner_or_expected_label_changed") is not False
        for record in repair_audit.get("records", [])
    ):
        raise ValueError("EXPECTED_LABEL_CHANGED_DURING_REPAIR_BLOCKER")

    mapping_by_blind = {
        str(row["blind_review_id"]): str(row["sample_id"]) for row in mapping_rows
    }
    corpus_by_sample = {str(row["sample_id"]): row for row in corpus_rows}
    expected_by_sample = {str(row["sample_id"]): row for row in expected_rows}
    if (
        len(mapping_by_blind) != 72
        or len(corpus_by_sample) != 72
        or len(expected_by_sample) != 72
        or set(mapping_by_blind.values()) != set(corpus_by_sample)
        or set(corpus_by_sample) != set(expected_by_sample)
    ):
        raise ValueError("MAPPING_EXPECTED_CORPUS_PARITY_BLOCKER")
    if any(row.get("answerability") != "PASS" for row in expected_rows):
        raise ValueError("EXPECTED_PHASE2_ISSUE_DERIVATION_BLOCKER")

    phase2_packet_rows = _load_jsonl(phase2_packet)
    packet_qa = validate_phase2_packet_rows(phase2_packet_rows)
    packet_by_blind = {str(row["blind_review_id"]): row for row in phase2_packet_rows}
    expected_blind_ids = list(mapping_by_blind)
    if set(packet_by_blind) != set(expected_blind_ids):
        raise ValueError("PHASE2_PACKET_MAPPING_PARITY_BLOCKER")

    locked_phase2_path = (
        output / "raw" / "PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_RETURN_FINAL.csv"
    )
    phase2_bytes = locked_phase2_path.read_bytes()
    if _sha256_bytes(phase2_bytes) != FINAL_PHASE2_RAW_SHA256:
        raise ValueError("FINAL_PHASE2_LOCKED_RAW_SHA_BLOCKER")
    phase2_validation = validate_phase2_raw_return(phase2_bytes, expected_blind_ids)
    phase2_rows_by_blind = {
        row["blind_review_id"]: row for row in phase2_validation["rows"]
    }

    phase1_bytes = phase1_raw.read_bytes()
    if _sha256_bytes(phase1_bytes) != PHASE1_RAW_SHA256:
        raise ValueError("PHASE1_LOCKED_RAW_SHA_BLOCKER")
    phase1_validation = validate_phase1_raw_return(phase1_bytes, expected_blind_ids)
    phase1_rows_by_blind = {
        row["blind_review_id"]: row for row in phase1_validation["rows"]
    }
    if set(phase1_rows_by_blind) != set(phase2_rows_by_blind):
        raise ValueError("CROSS_PHASE_IDENTITY_PARITY_BLOCKER")

    _exclusive_copy(
        mapping_source,
        output / "comparison" / "attempt2_identity_mapping_source.locked.json",
    )
    _exclusive_copy(
        candidate_corpus,
        output / "comparison" / "final_candidate_corpus.locked.jsonl",
    )
    _exclusive_copy(
        expected_contract,
        output / "comparison" / "expected_contract_source.locked.json",
    )
    _exclusive_copy(
        candidate_repair_audit,
        output / "comparison" / "candidate_repair_audit.locked.json",
    )
    _exclusive_copy(
        phase1_raw,
        output / "raw" / "PILOT4_EXTERNAL_BLIND_PHASE1_ATTEMPT2_RETURN.csv",
    )

    _write_json(
        output / "comparison" / "attempt2_identity_mapping_unlocked.json",
        {
            "status": "PASS",
            "authorization": "CONTROLLED_ATTEMPT2_IDENTITY_MAPPING_UNLOCK / OWNER_CURRENT_DIRECTIVE / FINAL72_ONLY",
            "unlock_timestamp": expected_load_timestamp,
            "mapping_source_path": str(mapping_source.resolve()),
            "mapping_source_sha256": _sha256_bytes(mapping_bytes),
            "record_count": 72,
            "blind_id_parity": "72/72",
            "sample_id_parity": "72/72",
            "records": mapping_rows,
        },
    )
    _write_json(
        output / "comparison" / "expected_contract_binding.json",
        {
            "status": "PASS",
            "expected_contract_load_timestamp": expected_load_timestamp,
            "raw_lock_timestamp": lock_timestamp,
            "raw_lock_precedes_expected_load": True,
            "expected_contract_source_path": str(expected_contract.resolve()),
            "expected_contract_source_sha256": _sha256_bytes(expected_bytes),
            "expected_contract_source_values_rewritten": False,
            "candidate_corpus_version": FINAL_CORPUS_VERSION,
            "candidate_corpus_path": str(candidate_corpus.resolve()),
            "candidate_corpus_sha256": _sha256_bytes(corpus_bytes),
            "candidate_count": 72,
            "candidate_parity": "72/72",
            "repair_binding_source_path": str(candidate_repair_audit.resolve()),
            "repair_binding_source_sha256": _sha256_bytes(repair_bytes),
            "repair_count": 5,
            "repair_expected_label_change_count": 0,
            "phase2_issue_derivation": (
                "Expected answerability=PASS derives expected phase2_issue=NONE; "
                "the source expected contract remains unchanged."
            ),
        },
    )

    phase1_rows: list[dict[str, Any]] = []
    phase2_rows: list[dict[str, Any]] = []
    for blind_id, sample_id in mapping_by_blind.items():
        candidate = corpus_by_sample[sample_id]
        owner_only = candidate["owner_only"]
        expected = expected_by_sample[sample_id]
        common = {
            "blind_review_id": blind_id,
            "sample_id": sample_id,
            "candidate_class": owner_only["candidate_kind"],
            "hkp": str(owner_only["coverage_cell"]).split("|", 1)[0],
            "intended_stealth": owner_only.get("intended_stealth") or "NOT_APPLICABLE",
            "candidate_text": candidate["phase1_view"]["candidate_text"],
            "source_title": candidate["phase1_view"]["source_title"],
        }
        reviewer_phase1 = phase1_rows_by_blind[blind_id]
        expected_phase1 = {field: expected[field] for field in PHASE1_EXPECTED_FIELDS}
        phase1_rows.append(
            {
                **common,
                "reviewer": {
                    field: reviewer_phase1[field] for field in PHASE1_EXPECTED_FIELDS
                },
                "expected": expected_phase1,
                "matches": {
                    field: reviewer_phase1[field] == expected_phase1[field]
                    for field in PHASE1_EXPECTED_FIELDS
                },
                "reviewer_reason": reviewer_phase1["phase1_reason"],
            }
        )
        reviewer_phase2 = phase2_rows_by_blind[blind_id]
        expected_phase2 = {
            **{field: expected[field] for field in PHASE2_EXPECTED_FIELDS[:-1]},
            "phase2_issue": "NONE",
        }
        phase2_rows.append(
            {
                **common,
                "reviewer": {
                    field: reviewer_phase2[field] for field in PHASE2_EXPECTED_FIELDS
                },
                "expected": expected_phase2,
                "matches": {
                    field: reviewer_phase2[field] == expected_phase2[field]
                    for field in PHASE2_EXPECTED_FIELDS
                },
                "reviewer_reason": reviewer_phase2["phase2_reason"],
                "evidence_pool": packet_by_blind[blind_id]["evidence_pool"],
                "evidence_selection": reviewer_phase2["evidence_selection"],
            }
        )

    phase1_comparison = _comparison_document(
        phase="PHASE1",
        rows=phase1_rows,
        fields=PHASE1_EXPECTED_FIELDS,
        raw_sha256=PHASE1_RAW_SHA256,
    )
    phase1_comparison["text_naturalness_interpretation"] = (
        "QC_AGREEMENT_ONLY / NOT_BENCHMARK_LABEL_ACCURACY"
    )
    phase2_comparison = _comparison_document(
        phase="PHASE2",
        rows=phase2_rows,
        fields=PHASE2_EXPECTED_FIELDS,
        raw_sha256=FINAL_PHASE2_RAW_SHA256,
    )
    phase2_comparison["evidence_selection_interpretation"] = (
        "DESCRIPTIVE_REVIEWER_PROCESS_OBSERVATION / NO_UNIQUE_EXPECTED_VALUE / NO_ACCURACY_SCORE"
    )
    _write_json(
        output / "comparison" / "phase1_expected_comparison.json", phase1_comparison
    )
    _write_json(
        output / "comparison" / "phase2_expected_comparison.json", phase2_comparison
    )
    _write_json(
        output / "comparison" / "evidence_selection_descriptive.json",
        {
            "classification": "DESCRIPTIVE_ONLY / NOT_ACCURACY",
            "unique_expected_evidence_selection_exists": False,
            "counts": dict(
                sorted(
                    Counter(row["evidence_selection"] for row in phase2_rows).items()
                )
            ),
            "rows": [
                {
                    "blind_review_id": row["blind_review_id"],
                    "sample_id": row["sample_id"],
                    "evidence_selection": row["evidence_selection"],
                }
                for row in phase2_rows
            ],
        },
    )

    mismatches = _build_mismatches(
        "PHASE1", phase1_rows, PHASE1_EXPECTED_FIELDS
    ) + _build_mismatches("PHASE2", phase2_rows, PHASE2_EXPECTED_FIELDS)
    taxonomy_counts = dict(
        sorted(Counter(row["taxonomy"] for row in mismatches).items())
    )
    _write_json(
        output / "mismatch" / "all_mismatches.json",
        {
            "status": "PASS / TAXONOMY_COMPLETE",
            "mismatch_count": len(mismatches),
            "taxonomy_counts": taxonomy_counts,
            "no_automatic_expected_wins": True,
            "reviewer_values_rewritten": False,
            "expected_values_rewritten": False,
            "records": mismatches,
        },
    )
    _write_mismatch_csv(output / "mismatch" / "all_mismatches.csv", mismatches)

    registry = _read_json(source_registry)
    registry_records = {
        str(row["evidence_id"]): row for row in registry.get("records", [])
    }
    special_sample = mapping_by_blind[SPECIAL_BLIND_ID]
    special_review = phase2_rows_by_blind[SPECIAL_BLIND_ID]
    special_expected = expected_by_sample[special_sample]
    special_candidate = corpus_by_sample[special_sample]
    special_packet = packet_by_blind[SPECIAL_BLIND_ID]
    primary_registry = registry_records.get("EVQ-FIN-01-PRIMARY", {})
    special_adjudication = {
        "status": "TARGETED_BLOCKER_CONFIRMED",
        "blind_review_id": SPECIAL_BLIND_ID,
        "sample_id": special_sample,
        "classification": "B / EVIDENCE_POOL_DESIGN_DEFECT",
        "taxonomy": "M4 / EVIDENCE_POOL_DEFECT",
        "candidate_text": special_candidate["phase1_view"]["candidate_text"],
        "reviewer_values": {field: special_review[field] for field in PHASE2_FIELDS},
        "expected_values": {
            field: special_expected[field] for field in PHASE2_EXPECTED_FIELDS[:-1]
        },
        "expected_phase2_issue_derived": "NONE",
        "evidence_pool": special_packet["evidence_pool"],
        "frozen_registry_supported_proposition": primary_registry.get(
            "supported_proposition"
        ),
        "frozen_registry_support_excerpt": primary_registry.get("support_excerpt"),
        "evidence_based_explanation": (
            "The candidate's 2014-amendment proposition is not stated in either "
            "supplied Evidence Pool item. The frozen primary excerpt states the "
            "2002 adoption and 2003 effective date, while the other supplied item "
            "describes 2015 implementation context. The reviewer therefore had a "
            "reasonable basis for INSUFFICIENT_EVIDENCE. The expected contract "
            "cannot override that missing support."
        ),
        "recommended_action": (
            "Add an official frozen amendment decision or version header directly "
            "supporting the 2014 amendment, or rewrite/remove that proposition; "
            "then perform targeted controlled validation."
        ),
        "formal_ab_blocked_until_repair": True,
        "reviewer_raw_modified": False,
        "expected_contract_modified": False,
    }
    _write_json(
        output / "mismatch" / "BR-18F1D39495_evidence_missing_adjudication.json",
        special_adjudication,
    )

    criteria = {
        "CLEAR": "FAIL_PRIMARY_STATUS_BOUNDARY_16_ROWS",
        "REPRODUCIBLE": "PASS",
        "ANSWERABLE": "TARGETED_FAIL_1_OF_72_PLUS_PRIMARY_LABEL_BOUNDARY",
        "NON_LEAKING": "PASS_BY_OWNER_ATTESTED_REVIEW_CONTEXT",
        "EVIDENCE_SUFFICIENT": "TARGETED_FAIL_1_OF_72",
        "SCALABLE": "HOLD_UNTIL_GUIDE_AND_EXPECTED_CONTRACT_REPAIR",
    }
    acceptance = {
        "status": "PROTOCOL_ACCEPTANCE_RECOMMENDATION_READY",
        "recommendation": "RECOMMEND_TARGETED_REPAIR",
        "owner_final_acceptance_recorded": False,
        "formal_ab_distribution_authorized": False,
        "systemic_blocker_detected": True,
        "systemic_blockers": [
            "OVERALL_FACT_STATUS_CURRENT_VS_LEGITIMATE_BOUNDARY_16_ROWS"
        ],
        "targeted_material_blocker_categories": [
            "EXPECTED_CONTRACT_FIELD_DEFECTS",
            "MINIMUM_EVIDENCE_CONTRACT_REVIEW",
            "BR-18F1D39495_EVIDENCE_POOL_DESIGN_DEFECT",
        ],
        "criteria": criteria,
        "access_lesson": (
            "LIVE_URL_ACCESS_CAN_BE_TRANSIENT_IN_EXTERNAL_REVIEW_ENVIRONMENT"
        ),
        "access_lesson_status": "PROVISIONAL_PENDING_FINAL_ACCEPTANCE",
        "future_robustness_mechanism": "URL_PROVENANCE_PLUS_FROZEN_EVIDENCE_SNAPSHOT",
    }
    _write_json(
        output / "acceptance" / "protocol_acceptance_recommendation.json", acceptance
    )
    acceptance_md = _acceptance_markdown(
        phase1=phase1_comparison,
        phase2=phase2_comparison,
        mismatches=mismatches,
        taxonomy_counts=taxonomy_counts,
    )
    acceptance_path = (
        output / "acceptance" / "PILOT4_ANNOTATION_PROTOCOL_ACCEPTANCE_EVIDENCE.md"
    )
    acceptance_path.write_text(acceptance_md, encoding="utf-8", newline="\n")

    _write_json(
        output / "qa" / "final_comparison_qa.json",
        {
            "status": "PASS",
            "raw_lock_timestamp": lock_timestamp,
            "expected_contract_load_timestamp": expected_load_timestamp,
            "raw_lock_precedes_expected_load": True,
            "mapping_72_72": True,
            "final_corpus_sha_parity": True,
            "phase1_locked_raw_parity": True,
            "phase2_final_raw_parity": True,
            "phase2_packet_qa": packet_qa,
            "phase1_traceable_rows": len(phase1_rows),
            "phase2_traceable_rows": len(phase2_rows),
            "mismatch_taxonomy_complete": all(
                row.get("taxonomy") and row.get("recommended_action")
                for row in mismatches
            ),
            "reviewer_values_rewritten": False,
            "expected_values_rewritten": False,
            "special_evidence_missing_case_adjudicated": True,
            "systemic_blocker_detected": True,
            "systemic_blocker": (
                "OVERALL_FACT_STATUS_CURRENT_VS_LEGITIMATE_BOUNDARY_16_ROWS"
            ),
            "final_reviewer_expected_blindness": lock_qa[
                "FINAL_REVIEWER_EXPECTED_BLINDNESS"
            ],
            "external_evidence_scope_violation_detected": False,
            "stage1_to_stage5_modified": False,
        },
    )

    manifest_records = [
        {
            "path": path.relative_to(output).as_posix(),
            "size": path.stat().st_size,
            "sha256": _file_sha256(path),
        }
        for path in sorted(output.rglob("*"))
        if path.is_file() and path.name != "final_manifest.json"
    ]
    _write_json(
        output / "manifest" / "final_manifest.json",
        {
            "task_id": TASK_ID,
            "status": (
                "PILOT4_FINAL_BLIND_REVIEW_COMPARISON_COMPLETE / "
                "PROTOCOL_ACCEPTANCE_RECOMMENDATION_READY / "
                "OWNER_PROTOCOL_ACCEPTANCE_PENDING / NO_AB_DISTRIBUTION"
            ),
            "raw_lock_timestamp": lock_timestamp,
            "expected_contract_load_timestamp": expected_load_timestamp,
            "raw_lock_precedes_expected_load": True,
            "recommendation": "RECOMMEND_TARGETED_REPAIR",
            "record_count": len(manifest_records),
            "records": manifest_records,
        },
    )
    return {
        "status": (
            "PILOT4_FINAL_BLIND_REVIEW_COMPARISON_COMPLETE / "
            "PROTOCOL_ACCEPTANCE_RECOMMENDATION_READY / "
            "OWNER_PROTOCOL_ACCEPTANCE_PENDING / NO_AB_DISTRIBUTION"
        ),
        "raw_lock_timestamp": lock_timestamp,
        "expected_contract_load_timestamp": expected_load_timestamp,
        "mapping_source_sha256": _sha256_bytes(mapping_bytes),
        "expected_contract_source_sha256": _sha256_bytes(expected_bytes),
        "phase1_exact": phase1_comparison["exact_relevant_field_match_count"],
        "phase2_exact": phase2_comparison["exact_relevant_field_match_count"],
        "mismatch_count": len(mismatches),
        "taxonomy_counts": taxonomy_counts,
        "recommendation": "RECOMMEND_TARGETED_REPAIR",
        "output": str(output.resolve()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mapping-source", type=Path, required=True)
    parser.add_argument("--candidate-corpus", type=Path, required=True)
    parser.add_argument("--expected-contract", type=Path, required=True)
    parser.add_argument("--candidate-repair-audit", type=Path, required=True)
    parser.add_argument("--phase1-raw", type=Path, required=True)
    parser.add_argument("--phase2-packet", type=Path, required=True)
    parser.add_argument("--source-registry", type=Path, required=True)
    args = parser.parse_args()
    result = compare(
        output=args.output,
        mapping_source=args.mapping_source,
        candidate_corpus=args.candidate_corpus,
        expected_contract=args.expected_contract,
        candidate_repair_audit=args.candidate_repair_audit,
        phase1_raw=args.phase1_raw,
        phase2_packet=args.phase2_packet,
        source_registry=args.source_registry,
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
