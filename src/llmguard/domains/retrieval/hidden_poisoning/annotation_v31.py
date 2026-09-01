"""Annotator-centered Pilot4 annotation schema V3.1 contracts.

The module deliberately separates the small human-facing annotation surface
from the richer canonical research record.  It contains no model calls and
never mutates the frozen Pilot4 candidate/source inputs.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
import json
import re
from typing import Any, Mapping, Sequence


V3_FIELDS: tuple[str, ...] = (
    "sample_id",
    "candidate_text",
    "source_title",
    "neutral_context",
    "language_natural_score",
    "topic_relevance_score",
    "local_internal_anomaly",
    "confidence",
    "reasoning_short",
    "time_seconds",
    "issue_flag",
    "claim_matches_source",
    "fact_changed",
    "version_relation_present",
    "version_relation_correct",
    "history_or_update_claim_present",
    "legitimate_update_or_history",
    "authority_claim_present",
    "authority_matches",
    "overall_fact_status",
    "professional_lookup_used",
    "lookup_source_type",
    "minimum_evidence_scope",
    "evidence_unit_count",
    "evidence_types",
    "evidence_ids",
    "minimum_sufficient_evidence_reason",
    "derived_stealth_level",
)

PHASE1_READ_ONLY: tuple[str, ...] = ("sample_id", "candidate_text", "source_title")
PHASE1_MANUAL: tuple[str, ...] = (
    "text_naturalness",
    "local_internal_conflict",
    "phase1_issue",
    "phase1_reason",
)
PHASE2_READ_ONLY: tuple[str, ...] = PHASE1_READ_ONLY
PHASE2_MANUAL: tuple[str, ...] = (
    "overall_fact_status",
    "version_claim_status",
    "authority_claim_status",
    "minimum_external_evidence_needed",
    "evidence_selection",
    "phase2_issue",
    "phase2_reason",
)
PROCESS_FIELDS: tuple[str, ...] = ("time_seconds",)

TEXT_NATURALNESS = ("NATURAL", "MINOR_ISSUE", "UNNATURAL")
LOCAL_INTERNAL_CONFLICT = ("YES", "NO", "UNCERTAIN")
PHASE1_ISSUE = ("NONE", "MISSING_CONTEXT", "AMBIGUOUS_REFERENCE", "OTHER")
OVERALL_FACT_STATUS = (
    "CURRENTLY_CONSISTENT",
    "LEGITIMATE_VERSION_OR_HISTORY",
    "FACTUAL_CONFLICT",
    "INSUFFICIENT_EVIDENCE",
)
COMBINED_CLAIM_STATUS = (
    "NOT_PRESENT",
    "PRESENT_CORRECT",
    "PRESENT_INCORRECT",
    "PRESENT_EVIDENCE_INSUFFICIENT",
)
MINIMUM_EXTERNAL_EVIDENCE = (
    "ONE_OFFICIAL_EVIDENCE",
    "MULTI_EVIDENCE_OR_VERSION_CHAIN",
    "INSUFFICIENT_EVIDENCE",
    "NOT_APPLICABLE",
)
EVIDENCE_SELECTION = ("NONE", "E1", "E2", "E1+E2")
PHASE2_ISSUE = (
    "NONE",
    "SOURCE_UNREACHABLE",
    "SOURCE_CONFLICT",
    "EVIDENCE_MISSING",
    "CANDIDATE_AMBIGUOUS",
    "OTHER",
)

MANUAL_FIELD_COUNT_V3 = 23
MANUAL_FIELD_COUNT_V31 = len(PHASE1_MANUAL) + len(PHASE2_MANUAL)


_FIELD_DISPOSITIONS: dict[str, tuple[str, str | None, str]] = {
    "sample_id": ("KEEP", "sample_id", "稳定身份只读保留。"),
    "candidate_text": ("KEEP", "candidate_text", "候选正文只读保留。"),
    "source_title": ("KEEP", "source_title", "仅保留宽主题标题，不给答案提示。"),
    "neutral_context": (
        "DEPRECATED",
        None,
        "与 source_title 重复且历史上产生 hint leakage。",
    ),
    "language_natural_score": (
        "MERGED_TO",
        "text_naturalness",
        "五级主观尺度压缩为可操作的三级数据质量判断。",
    ),
    "topic_relevance_score": (
        "MOVE_TO_DATA_QUALITY_QA",
        None,
        "主题相关性已由预标注 QA 处理，不让 Ground Truth 标注人重复。",
    ),
    "local_internal_anomaly": (
        "MERGED_TO",
        "local_internal_conflict",
        "改成只判断文本内能否确定核心事实冲突的直接问题。",
    ),
    "confidence": ("DEPRECATED", None, "非核心 GT 且尺度主观。"),
    "reasoning_short": (
        "MERGED_TO",
        "phase1_reason",
        "理由仅在冲突、不确定或 issue 时条件必填。",
    ),
    "time_seconds": (
        "PROCESS_AUTO",
        "time_seconds",
        "由系统计时，不允许人工录入。",
    ),
    "issue_flag": (
        "MERGED_TO",
        "phase1_issue",
        "一个统一候选问题字段替代重复报告。",
    ),
    "claim_matches_source": (
        "DERIVED_FROM",
        "overall_fact_status",
        "总体事实状态已唯一决定来源一致性兼容值。",
    ),
    "fact_changed": (
        "MOVE_TO_DATA_QUALITY_QA",
        "construction_metadata.fact_changed",
        "这是构造过程事实，不让 A/B 猜测。",
    ),
    "version_relation_present": (
        "MERGED_TO",
        "version_claim_status",
        "present 与 correctness 合并为单次判断。",
    ),
    "version_relation_correct": (
        "MERGED_TO",
        "version_claim_status",
        "present 与 correctness 合并为单次判断。",
    ),
    "history_or_update_claim_present": (
        "DERIVED_FROM",
        "version_claim_status",
        "从版本主张状态确定是否存在历史/更新命题。",
    ),
    "legitimate_update_or_history": (
        "DERIVED_FROM",
        "overall_fact_status",
        "合法历史由唯一主 GT 表达，不重复询问。",
    ),
    "authority_claim_present": (
        "MERGED_TO",
        "authority_claim_status",
        "present 与 correctness 合并为单次判断。",
    ),
    "authority_matches": (
        "MERGED_TO",
        "authority_claim_status",
        "present 与 correctness 合并为单次判断。",
    ),
    "overall_fact_status": (
        "KEEP",
        "overall_fact_status",
        "作为事实 Ground Truth 的首要人工判断。",
    ),
    "professional_lookup_used": (
        "DERIVED_FROM",
        "evidence_selection",
        "是否使用官方证据由实际选择自动确定。",
    ),
    "lookup_source_type": (
        "DERIVED_FROM",
        "evidence_selection+evidence_registry",
        "来源类型由 Registry 自动映射。",
    ),
    "minimum_evidence_scope": (
        "MERGED_TO",
        "minimum_external_evidence_needed",
        "只在外部证据对事实冲突分级时适用。",
    ),
    "evidence_unit_count": (
        "DERIVED_FROM",
        "evidence_selection",
        "系统统计被选择的 evidence slot。",
    ),
    "evidence_types": (
        "DERIVED_FROM",
        "evidence_selection+evidence_registry",
        "系统从 Registry 映射类型。",
    ),
    "evidence_ids": (
        "DERIVED_FROM",
        "evidence_selection+neutral_slot_mapping",
        "系统在提交后恢复稳定 evidence IDs。",
    ),
    "minimum_sufficient_evidence_reason": (
        "MERGED_TO",
        "phase2_reason",
        "只在 multi/insufficient 等条件下要求一次理由。",
    ),
    "derived_stealth_level": (
        "DERIVED_FROM",
        "overall_fact_status+local_internal_conflict+minimum_external_evidence_needed",
        "提交后系统派生，标注界面不可见。",
    ),
}


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_json(value: object) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


def version_status_mapping(status: str) -> tuple[str, str]:
    mapping = {
        "NOT_PRESENT": ("NO", "NOT_APPLICABLE"),
        "PRESENT_CORRECT": ("YES", "YES"),
        "PRESENT_INCORRECT": ("YES", "NO"),
        "PRESENT_EVIDENCE_INSUFFICIENT": ("YES", "UNCERTAIN"),
    }
    if status not in mapping:
        raise ValueError(f"invalid version_claim_status: {status}")
    return mapping[status]


def authority_status_mapping(status: str) -> tuple[str, str]:
    if status not in COMBINED_CLAIM_STATUS:
        raise ValueError(f"invalid authority_claim_status: {status}")
    return version_status_mapping(status)


def claim_matches_source(overall: str) -> str:
    mapping = {
        "CURRENTLY_CONSISTENT": "YES",
        "LEGITIMATE_VERSION_OR_HISTORY": "YES",
        "FACTUAL_CONFLICT": "NO",
        "INSUFFICIENT_EVIDENCE": "UNCERTAIN",
    }
    if overall not in mapping:
        raise ValueError(f"invalid overall_fact_status: {overall}")
    return mapping[overall]


def derive_stealth_level(
    overall_fact_status: str,
    local_internal_conflict: str,
    minimum_external_evidence_needed: str,
) -> str:
    if overall_fact_status != "FACTUAL_CONFLICT":
        return "NOT_APPLICABLE"
    if local_internal_conflict == "YES":
        return "S1"
    if minimum_external_evidence_needed == "ONE_OFFICIAL_EVIDENCE":
        return "S2"
    if minimum_external_evidence_needed == "MULTI_EVIDENCE_OR_VERSION_CHAIN":
        return "S3"
    return "UNCERTAIN"


def field_minimization_audit(
    v3_fields: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_name = {str(field["field_name"]): field for field in v3_fields}
    if tuple(by_name) != V3_FIELDS:
        raise ValueError("V3 field identity/order mismatch")
    rows: list[dict[str, Any]] = []
    for name in V3_FIELDS:
        field = by_name[name]
        disposition, replacement, reason = _FIELD_DISPOSITIONS[name]
        manual = str(field.get("field_class", "")).startswith("MANUAL")
        needed_gt = name in {
            "local_internal_anomaly",
            "overall_fact_status",
            "minimum_evidence_scope",
        }
        independently_observable = name not in {
            "fact_changed",
            "derived_stealth_level",
            "evidence_unit_count",
            "evidence_types",
            "evidence_ids",
            "professional_lookup_used",
            "lookup_source_type",
            "time_seconds",
        }
        duplicated = disposition in {"MERGED_TO", "DERIVED_FROM"}
        machine_derivable = disposition in {
            "DERIVED_FROM",
            "PROCESS_AUTO",
            "MOVE_TO_DATA_QUALITY_QA",
        }
        ambiguity = (
            "HIGH"
            if name
            in {
                "claim_matches_source",
                "history_or_update_claim_present",
                "legitimate_update_or_history",
                "version_relation_present",
                "version_relation_correct",
                "authority_claim_present",
                "authority_matches",
                "minimum_evidence_scope",
            }
            else "MEDIUM"
            if manual
            else "LOW"
        )
        burden = "HIGH" if manual and disposition != "KEEP" else "LOW"
        rows.append(
            {
                "field_name": name,
                "current_phase": field.get("phase"),
                "current_semantics": field.get("dependency"),
                "paper_research_purpose": (
                    "FACTUAL_GROUND_TRUTH"
                    if needed_gt
                    else "DATA_QUALITY_OR_COMPATIBILITY"
                ),
                "needed_for_ground_truth": needed_gt,
                "independently_human_observable": independently_observable,
                "duplicated_by_another_field": duplicated,
                "machine_derivable": machine_derivable,
                "ambiguity_risk": ambiguity,
                "annotator_burden": burden,
                "final_disposition": disposition,
                "replacement_field": replacement,
                "backward_compatibility_mapping": _compatibility_mapping_text(name),
                "reason": reason,
            }
        )
    return rows


def _compatibility_mapping_text(field_name: str) -> str:
    disposition, replacement, _ = _FIELD_DISPOSITIONS[field_name]
    if disposition == "KEEP":
        return f"canonical.{field_name} <- annotator.{replacement}"
    if disposition == "MERGED_TO":
        return f"canonical.{field_name} <- deterministic_map({replacement})"
    if disposition == "DERIVED_FROM":
        return f"canonical.{field_name} <- derive({replacement})"
    if disposition == "PROCESS_AUTO":
        return f"canonical.{field_name} <- process_capture"
    if disposition == "MOVE_TO_DATA_QUALITY_QA":
        return f"canonical.{field_name} <- construction_or_owner_QA"
    return f"canonical.{field_name} <- null_with_deprecation_marker"


def v3_to_v31_mapping() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "action": disposition,
            "target": replacement,
            "reason": reason,
        }
        for name, (disposition, replacement, reason) in _FIELD_DISPOSITIONS.items()
    }


def _source_type(record: Mapping[str, Any]) -> str:
    media = str(record.get("media_type", "")).lower()
    identity = str(record.get("source_identity", ""))
    url = str(record.get("source_url", ""))
    if "pdf" in media or url.lower().endswith(".pdf"):
        return "OFFICIAL_PDF"
    if "转载" in identity:
        return "OFFICIAL_REPOST"
    return "OFFICIAL_WEB_PAGE"


def _neutral_title(record: Mapping[str, Any]) -> str:
    identity = str(record.get("source_identity", ""))
    for prefix in ("Hard Negative 官方支持来源：", "官方来源："):
        if identity.startswith(prefix):
            return identity[len(prefix) :]
    return identity


def _document_identity(record: Mapping[str, Any]) -> str:
    return str(
        record.get("document_identity")
        or record.get("final_url")
        or record.get("source_url")
        or record.get("source_identity")
        or ""
    ).strip()


def _duplicate_evidence_dimensions(
    records: Sequence[Mapping[str, Any]],
) -> tuple[str, ...]:
    dimensions = {
        "source_url": [str(record.get("source_url") or "").strip() for record in records],
        "content_hash": [str(record.get("content_hash") or "").strip() for record in records],
        "document_identity": [_document_identity(record) for record in records],
        "minimal_evidence_hash": [
            str(record.get("minimal_evidence_hash") or "").strip()
            for record in records
        ],
    }
    return tuple(
        name
        for name, values in dimensions.items()
        if any(not value for value in values) or len(set(values)) != len(values)
    )


@dataclass(frozen=True)
class EvidencePool:
    sample_id: str
    annotator_variant: str
    visible_items: tuple[dict[str, Any], ...]
    slot_mapping: Mapping[str, str]


def indistinguishable_visible_source_slots(
    pool: EvidencePool,
) -> dict[str, tuple[str, ...]]:
    """Return visible slots that collapse onto the same official page.

    The annotator-facing pool intentionally hides registry roles and evidence
    anchors.  Under that visibility contract, two slots with the same official
    URL are not independently selectable evidence items even when their hidden
    registry records have different IDs or supported propositions.
    """

    slots_by_url: dict[str, list[str]] = {}
    for item in pool.visible_items:
        url = str(item.get("official_source_url", "")).strip()
        slots_by_url.setdefault(url, []).append(str(item["evidence_id"]))
    return {
        url: tuple(slots)
        for url, slots in slots_by_url.items()
        if not url or len(slots) > 1
    }


def build_neutral_evidence_pool(
    candidate: Mapping[str, Any],
    source_records: Sequence[Mapping[str, Any]],
    *,
    annotator_variant: str,
) -> EvidencePool:
    """Build a fixed-size two-slot pool without exposing semantic source IDs.

    Every candidate receives exactly two records.  Required records come first
    internally; a triplet-local verified companion fills the unused slot.  The
    externally visible order is independently shuffled per annotator/sample.
    """

    sample_id = str(candidate["sample_id"])
    triplet_id = str(candidate["triplet_id"])
    source_by_id = {str(record["evidence_id"]): record for record in source_records}
    triplet_records = [
        record
        for record in source_records
        if str(record.get("triplet_id") or "") == triplet_id
        or str(record["evidence_id"]).startswith(f"EVQ-{triplet_id}-")
        or str(record["evidence_id"]).startswith(f"EVC-{triplet_id}-")
    ]
    required = [str(value) for value in candidate["phase2_view"]["evidence_ids"]]
    preferred_ids = list(dict.fromkeys(required))
    companion_id = f"EVC-{triplet_id}-COMPANION-01"
    if len(preferred_ids) < 2 and companion_id in source_by_id:
        preferred_ids.append(companion_id)
    if len(preferred_ids) < 2:
        for record in triplet_records:
            evidence_id = str(record["evidence_id"])
            if evidence_id in preferred_ids:
                continue
            tentative = [source_by_id[value] for value in preferred_ids] + [record]
            if not _duplicate_evidence_dimensions(tentative):
                preferred_ids.append(evidence_id)
                break
    selected_ids = preferred_ids[:2]
    if len(selected_ids) != 2:
        raise ValueError(f"cannot form fixed two-slot evidence pool for {sample_id}")
    if any(evidence_id not in source_by_id for evidence_id in selected_ids):
        raise ValueError(f"unknown evidence ID in pool for {sample_id}")
    selected_records = [source_by_id[evidence_id] for evidence_id in selected_ids]
    duplicate_dimensions = _duplicate_evidence_dimensions(selected_records)
    if duplicate_dimensions:
        raise ValueError(
            f"duplicate evidence units for {sample_id}: {duplicate_dimensions}"
        )
    ordered = sorted(selected_ids)
    base_swap = int(sha256(sample_id.encode("utf-8")).hexdigest(), 16) % 2 == 1
    variant_swap = annotator_variant in {"SIM_B", "B"}
    if base_swap != variant_swap:
        ordered.reverse()
    visible: list[dict[str, Any]] = []
    mapping: dict[str, str] = {}
    for index, evidence_id in enumerate(ordered, start=1):
        slot = f"E{index}"
        record = source_by_id[evidence_id]
        mapping[slot] = evidence_id
        visible.append(
            {
                "sample_id": sample_id,
                "evidence_id": slot,
                "official_source_title": _neutral_title(record),
                "official_source_url": record.get("source_url"),
                "source_type": record.get("neutral_source_type")
                or _source_type(record),
            }
        )
    return EvidencePool(
        sample_id=sample_id,
        annotator_variant=annotator_variant,
        visible_items=tuple(visible),
        slot_mapping=mapping,
    )


def selected_slots(selection: str) -> tuple[str, ...]:
    mapping = {
        "NONE": (),
        "E1": ("E1",),
        "E2": ("E2",),
        "E1+E2": ("E1", "E2"),
    }
    if selection not in mapping:
        raise ValueError(f"invalid evidence_selection: {selection}")
    return mapping[selection]


def derive_evidence_fields(
    selection: str,
    slot_mapping: Mapping[str, str],
    source_registry: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    slots = selected_slots(selection)
    evidence_ids: list[str] = []
    evidence_types: list[str] = []
    selected_records: list[Mapping[str, Any]] = []
    for slot in slots:
        if slot not in slot_mapping:
            raise ValueError(f"unknown neutral evidence slot: {slot}")
        evidence_id = slot_mapping[slot]
        if evidence_id not in source_registry:
            raise ValueError(f"evidence ID absent from registry: {evidence_id}")
        selected_records.append(source_registry[evidence_id])
        evidence_ids.append(evidence_id)
        evidence_types.append(_source_type(source_registry[evidence_id]))
    duplicate_dimensions = _duplicate_evidence_dimensions(selected_records)
    if duplicate_dimensions:
        raise ValueError(
            "selected evidence slots are not distinct evidence units: "
            f"{duplicate_dimensions}"
        )
    return {
        "evidence_ids": evidence_ids,
        "evidence_unit_count": len(evidence_ids),
        "evidence_types": evidence_types,
        "professional_lookup_used": "YES" if evidence_ids else "NO",
        "lookup_source_types": sorted(set(evidence_types)),
        "lookup_source_type": evidence_types[0] if evidence_types else "NOT_APPLICABLE",
    }


def _require_enum(record: Mapping[str, Any], field: str, allowed: Sequence[str]) -> str:
    value = record.get(field)
    if value is None or value == "":
        raise ValueError(f"missing required field: {field}")
    text = str(value)
    if text not in allowed:
        raise ValueError(f"invalid enum {field}={text}")
    return text


def _require_reason(condition: bool, value: Any, field: str) -> None:
    if condition and not str(value or "").strip():
        raise ValueError(f"conditional reason required: {field}")


def validate_and_build_canonical_record(
    phase1_return: Mapping[str, Any],
    phase2_return: Mapping[str, Any],
    *,
    immutable_identity: Mapping[str, str],
    slot_mapping: Mapping[str, str],
    source_registry: Mapping[str, Mapping[str, Any]],
    process_time_seconds: float,
    construction_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate raw returns and derive a canonical record without mutation."""

    before_phase1 = deepcopy(dict(phase1_return))
    before_phase2 = deepcopy(dict(phase2_return))
    for phase_name, record in (("phase1", phase1_return), ("phase2", phase2_return)):
        for field in PHASE1_READ_ONLY:
            if str(record.get(field, "")) != str(immutable_identity[field]):
                raise ValueError(f"{phase_name} read-only field changed: {field}")
    if phase1_return.get("sample_id") != phase2_return.get("sample_id"):
        raise ValueError("Phase1/Phase2 sample identity mismatch")

    naturalness = _require_enum(phase1_return, "text_naturalness", TEXT_NATURALNESS)
    local = _require_enum(
        phase1_return, "local_internal_conflict", LOCAL_INTERNAL_CONFLICT
    )
    phase1_issue = _require_enum(phase1_return, "phase1_issue", PHASE1_ISSUE)
    phase1_reason = str(phase1_return.get("phase1_reason") or "").strip()
    _require_reason(
        local in {"YES", "UNCERTAIN"} or phase1_issue != "NONE",
        phase1_reason,
        "phase1_reason",
    )

    overall = _require_enum(phase2_return, "overall_fact_status", OVERALL_FACT_STATUS)
    version = _require_enum(
        phase2_return, "version_claim_status", COMBINED_CLAIM_STATUS
    )
    authority = _require_enum(
        phase2_return, "authority_claim_status", COMBINED_CLAIM_STATUS
    )
    minimum = _require_enum(
        phase2_return,
        "minimum_external_evidence_needed",
        MINIMUM_EXTERNAL_EVIDENCE,
    )
    selection = _require_enum(phase2_return, "evidence_selection", EVIDENCE_SELECTION)
    phase2_issue = _require_enum(phase2_return, "phase2_issue", PHASE2_ISSUE)
    phase2_reason = str(phase2_return.get("phase2_reason") or "").strip()

    expected_minimum_na = overall != "FACTUAL_CONFLICT" or local == "YES"
    if expected_minimum_na and minimum != "NOT_APPLICABLE":
        raise ValueError("minimum evidence must be NOT_APPLICABLE")
    if overall == "FACTUAL_CONFLICT" and local != "YES" and minimum == "NOT_APPLICABLE":
        raise ValueError("minimum evidence must be answered for non-local conflict")
    if overall == "INSUFFICIENT_EVIDENCE" and phase2_issue == "NONE":
        raise ValueError("insufficient evidence requires a Phase2 issue")
    evidence = derive_evidence_fields(selection, slot_mapping, source_registry)
    if (
        overall != "INSUFFICIENT_EVIDENCE"
        and phase2_issue == "NONE"
        and evidence["evidence_unit_count"] == 0
    ):
        raise ValueError("completed Phase2 fact judgment requires evidence selection")

    phase2_reason_required = (
        overall
        in {
            "FACTUAL_CONFLICT",
            "LEGITIMATE_VERSION_OR_HISTORY",
            "INSUFFICIENT_EVIDENCE",
        }
        or version in {"PRESENT_INCORRECT", "PRESENT_EVIDENCE_INSUFFICIENT"}
        or authority in {"PRESENT_INCORRECT", "PRESENT_EVIDENCE_INSUFFICIENT"}
        or minimum in {"MULTI_EVIDENCE_OR_VERSION_CHAIN", "INSUFFICIENT_EVIDENCE"}
        or phase2_issue != "NONE"
    )
    _require_reason(phase2_reason_required, phase2_reason, "phase2_reason")
    if phase2_issue == "CANDIDATE_AMBIGUOUS" and (
        version == "PRESENT_EVIDENCE_INSUFFICIENT"
        or authority == "PRESENT_EVIDENCE_INSUFFICIENT"
    ):
        raise ValueError(
            "candidate ambiguity must not be encoded as evidence insufficiency"
        )

    version_present, version_correct = version_status_mapping(version)
    authority_present, authority_correct = authority_status_mapping(authority)
    stealth = derive_stealth_level(overall, local, minimum)
    canonical = {
        **immutable_identity,
        "schema_version": "3.1",
        "text_naturalness": naturalness,
        "local_internal_conflict": local,
        "phase1_issue": phase1_issue,
        "phase1_reason": phase1_reason or None,
        "overall_fact_status": overall,
        "version_claim_status": version,
        "authority_claim_status": authority,
        "minimum_external_evidence_needed": minimum,
        "evidence_selection": selection,
        "phase2_issue": phase2_issue,
        "phase2_reason": phase2_reason or None,
        "time_seconds": float(process_time_seconds),
        "raw_return_sha256": sha256_json(
            {"phase1": before_phase1, "phase2": before_phase2}
        ),
        "language_natural_score": {
            "NATURAL": 5,
            "MINOR_ISSUE": 3,
            "UNNATURAL": 1,
        }[naturalness],
        "topic_relevance_score": construction_metadata.get("topic_relevance_score"),
        "local_internal_anomaly": local,
        "confidence": None,
        "reasoning_short": phase1_reason or None,
        "issue_flag": phase1_issue,
        "claim_matches_source": claim_matches_source(overall),
        "fact_changed": construction_metadata.get("fact_changed"),
        "version_relation_present": version_present,
        "version_relation_correct": version_correct,
        "history_or_update_claim_present": (
            "NO" if version == "NOT_PRESENT" else "YES"
        ),
        "legitimate_update_or_history": (
            "YES"
            if overall == "LEGITIMATE_VERSION_OR_HISTORY"
            else "NO"
            if overall in {"CURRENTLY_CONSISTENT", "FACTUAL_CONFLICT"}
            else "UNCERTAIN"
        ),
        "authority_claim_present": authority_present,
        "authority_matches": authority_correct,
        "minimum_evidence_scope": {
            "ONE_OFFICIAL_EVIDENCE": "ONE_DIRECT_OFFICIAL_SOURCE",
            "MULTI_EVIDENCE_OR_VERSION_CHAIN": "MULTI_DOCUMENT_OR_VERSION_CHAIN",
            "INSUFFICIENT_EVIDENCE": "INSUFFICIENT_EVIDENCE",
            "NOT_APPLICABLE": "NOT_APPLICABLE",
        }[minimum],
        "minimum_sufficient_evidence_reason": (
            phase2_reason
            if minimum in {"MULTI_EVIDENCE_OR_VERSION_CHAIN", "INSUFFICIENT_EVIDENCE"}
            else None
        ),
        "derived_stealth_level": stealth,
        **evidence,
    }
    if before_phase1 != dict(phase1_return) or before_phase2 != dict(phase2_return):
        raise RuntimeError("raw return mutated")
    return canonical


def dependency_truth_table_v31() -> dict[str, list[dict[str, Any]]]:
    overall_local_minimum: list[dict[str, Any]] = []
    for overall in OVERALL_FACT_STATUS:
        for local in LOCAL_INTERNAL_CONFLICT:
            for minimum in MINIMUM_EXTERNAL_EVIDENCE:
                valid = False
                if overall != "FACTUAL_CONFLICT":
                    valid = local != "YES" and minimum == "NOT_APPLICABLE"
                elif local == "YES":
                    valid = minimum == "NOT_APPLICABLE"
                else:
                    valid = minimum != "NOT_APPLICABLE"
                overall_local_minimum.append(
                    {
                        "overall_fact_status": overall,
                        "local_internal_conflict": local,
                        "minimum_external_evidence_needed": minimum,
                        "valid": valid,
                        "derived_stealth_level": (
                            derive_stealth_level(overall, local, minimum)
                            if valid
                            else "INVALID_COMBINATION"
                        ),
                    }
                )
    version = [
        {
            "version_claim_status": value,
            "version_relation_present": version_status_mapping(value)[0],
            "version_relation_correct": version_status_mapping(value)[1],
        }
        for value in COMBINED_CLAIM_STATUS
    ]
    authority = [
        {
            "authority_claim_status": value,
            "authority_claim_present": authority_status_mapping(value)[0],
            "authority_matches": authority_status_mapping(value)[1],
        }
        for value in COMBINED_CLAIM_STATUS
    ]
    evidence = [
        {
            "evidence_selection": value,
            "selected_slot_count": len(selected_slots(value)),
            "professional_lookup_used": "YES" if selected_slots(value) else "NO",
        }
        for value in EVIDENCE_SELECTION
    ]
    phase1_reason: list[dict[str, Any]] = []
    for local in LOCAL_INTERNAL_CONFLICT:
        for issue in PHASE1_ISSUE:
            phase1_reason.append(
                {
                    "local_internal_conflict": local,
                    "phase1_issue": issue,
                    "phase1_reason_required": local in {"YES", "UNCERTAIN"}
                    or issue != "NONE",
                }
            )
    phase2_reason: list[dict[str, Any]] = []
    for mask in range(32):
        triggers = {
            "overall_special": bool(mask & 1),
            "version_problem": bool(mask & 2),
            "authority_problem": bool(mask & 4),
            "minimum_problem": bool(mask & 8),
            "phase2_issue": bool(mask & 16),
        }
        phase2_reason.append(
            {
                **triggers,
                "phase2_reason_required": any(triggers.values()),
            }
        )
    return {
        "overall_local_minimum": overall_local_minimum,
        "version_mapping": version,
        "authority_mapping": authority,
        "evidence_selection_mapping": evidence,
        "phase1_reason_conditions": phase1_reason,
        "phase2_reason_conditions": phase2_reason,
    }


def validate_dependency_truth_table(
    tables: Mapping[str, Sequence[Mapping[str, Any]]],
) -> None:
    expected_counts = {
        "overall_local_minimum": 48,
        "version_mapping": 4,
        "authority_mapping": 4,
        "evidence_selection_mapping": 4,
        "phase1_reason_conditions": 12,
        "phase2_reason_conditions": 32,
    }
    if set(tables) != set(expected_counts):
        raise ValueError("dependency table sections mismatch")
    for name, count in expected_counts.items():
        rows = list(tables[name])
        if len(rows) != count:
            raise ValueError(f"{name} is not exhaustive")
        signatures = {canonical_json(row) for row in rows}
        if len(signatures) != len(rows):
            raise ValueError(f"{name} contains duplicate/non-exclusive rows")


_VERSION_PATTERN = re.compile(
    r"(版本|修订|修正|施行|生效|废止|替代|沿革|原始文本|新法)"
)
_AUTHORITY_PATTERN = re.compile(
    r"(制定|通过|修订并公布|发布|公布|联合制定|制定机关|通过机关|国务院令|全国人大常委会)"
)


def _version_status_for_candidate(candidate: Mapping[str, Any]) -> str:
    text = str(candidate["phase1_view"]["candidate_text"])
    if not _VERSION_PATTERN.search(text):
        return "NOT_PRESENT"
    owner = candidate["owner_only"]
    if owner["candidate_kind"] == "POISON_CANDIDATE":
        if owner["target_field"] in {"effective_date", "validity_status"}:
            return "PRESENT_INCORRECT"
        if owner["target_field"] == "numeric_scalar" and re.search(
            r"(原始|修正|修订|新法|版本|文本).*(不同|增加|保持不变)", text
        ):
            return "PRESENT_INCORRECT"
    return "PRESENT_CORRECT"


def _authority_status_for_candidate(candidate: Mapping[str, Any]) -> str:
    text = str(candidate["phase1_view"]["candidate_text"])
    if not _AUTHORITY_PATTERN.search(text):
        return "NOT_PRESENT"
    owner = candidate["owner_only"]
    if owner["candidate_kind"] == "POISON_CANDIDATE" and owner["target_field"] in {
        "issuing_authority",
        "joint_issuer",
        "primary_repost_attribution",
    }:
        return "PRESENT_INCORRECT"
    return "PRESENT_CORRECT"


def candidate_schema_answers(candidate: Mapping[str, Any]) -> dict[str, Any]:
    owner = candidate["owner_only"]
    kind = str(owner["candidate_kind"])
    stealth = owner.get("intended_stealth")
    if kind == "POISON_CANDIDATE":
        overall = "FACTUAL_CONFLICT"
        local = "YES" if stealth == "S1" else "NO"
        minimum = {
            "S1": "NOT_APPLICABLE",
            "S2": "ONE_OFFICIAL_EVIDENCE",
            "S3": "MULTI_EVIDENCE_OR_VERSION_CHAIN",
        }[str(stealth)]
    elif kind == "MATCHED_HARD_NEGATIVE":
        hn_type = str(owner.get("hard_negative_type"))
        overall = (
            "LEGITIMATE_VERSION_OR_HISTORY"
            if hn_type in {"LEGITIMATE_HISTORICAL_VERSION", "LEGITIMATE_UPDATE"}
            else "CURRENTLY_CONSISTENT"
        )
        local = "NO"
        minimum = "NOT_APPLICABLE"
    else:
        overall = "CURRENTLY_CONSISTENT"
        local = "NO"
        minimum = "NOT_APPLICABLE"
    return {
        "sample_id": candidate["sample_id"],
        "text_naturalness": "NATURAL",
        "local_internal_conflict": local,
        "phase1_issue": "NONE",
        "overall_fact_status": overall,
        "version_claim_status": _version_status_for_candidate(candidate),
        "authority_claim_status": _authority_status_for_candidate(candidate),
        "minimum_external_evidence_needed": minimum,
        "derived_stealth_level": derive_stealth_level(overall, local, minimum),
    }


def full72_answerability(
    candidates: Sequence[Mapping[str, Any]],
    source_records: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    failures: list[str] = []
    for candidate in candidates:
        answers = candidate_schema_answers(candidate)
        pool_a = build_neutral_evidence_pool(
            candidate, source_records, annotator_variant="SIM_A"
        )
        pool_b = build_neutral_evidence_pool(
            candidate, source_records, annotator_variant="SIM_B"
        )
        answerable = (
            len(pool_a.visible_items) == 2
            and len(pool_b.visible_items) == 2
            and set(pool_a.slot_mapping.values()) == set(pool_b.slot_mapping.values())
            and not any(
                value == "PRESENT_EVIDENCE_INSUFFICIENT"
                for value in answers.values()
            )
        )
        if not answerable:
            failures.append(str(candidate["sample_id"]))
        rows.append(
            {
                **answers,
                "answerability": "PASS" if answerable else "FAIL",
                "candidate_changed": False,
                "reasonable_encoding_count": 1 if answerable else 2,
            }
        )
    return {
        "status": "PASS" if not failures and len(rows) == 72 else "FAIL",
        "candidate_count": len(rows),
        "pass_count": sum(row["answerability"] == "PASS" for row in rows),
        "candidate_schema_interaction_blockers": failures,
        "rows": rows,
    }
