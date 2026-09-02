"""Machine-only contracts for preparing an external blind review packet.

This module performs structural work only: title extraction, opaque identity
generation, deterministic shuffling, leakage checks, and lexical duplicate
checks.  It does not infer factual correctness or annotation answers.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
import hmac
from html.parser import HTMLParser
from io import BytesIO, StringIO
import csv
import re
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from charset_normalizer import from_bytes


TITLE_ORIGINS = (
    "HTML_TITLE",
    "PAGE_H1",
    "OFFICIAL_DOCUMENT_HEADING",
    "PDF_DOCUMENT_HEADING",
)

PHASE1_FIELDS = (
    "text_naturalness",
    "local_internal_conflict",
    "phase1_issue",
    "phase1_reason",
)

PHASE2_FIELDS = (
    "overall_fact_status",
    "version_claim_status",
    "authority_claim_status",
    "minimum_external_evidence_needed",
    "evidence_selection",
    "phase2_issue",
    "phase2_reason",
)

PHASE1_PACKET_ROW_FIELDS = (
    "blind_review_id",
    "candidate_text",
    "source_title",
) + PHASE1_FIELDS

PHASE2_PACKET_ROW_FIELDS = (
    "blind_review_id",
    "candidate_text",
    "source_title",
    "evidence_pool",
) + PHASE2_FIELDS

PHASE1_RETURN_FIELDS = ("blind_review_id",) + PHASE1_FIELDS
PHASE2_RETURN_FIELDS = ("blind_review_id",) + PHASE2_FIELDS

PHASE2_RELEASE_REQUIREMENTS = (
    "PHASE1_RETURN_RECEIVED",
    "PHASE1_RETURN_SCHEMA_VALID",
    "PHASE1_RETURN_72_72",
    "PHASE1_RETURN_HASH_LOCKED",
    "PHASE1_RETURN_IMMUTABLE",
    "PHASE1_CANDIDATE_DEFECT_TRIAGE_RESOLVED",
)

PHASE1_RETURN_ENUMS = {
    "text_naturalness": frozenset({"NATURAL", "MINOR_ISSUE", "UNNATURAL"}),
    "local_internal_conflict": frozenset({"YES", "NO", "UNCERTAIN"}),
    "phase1_issue": frozenset(
        {"NONE", "MISSING_CONTEXT", "AMBIGUOUS_REFERENCE", "OTHER"}
    ),
}

MANUAL_FIELDS = PHASE1_FIELDS + PHASE2_FIELDS

PACKET_ROW_FIELDS = (
    "blind_review_id",
    "candidate_text",
    "source_title",
    "phase1_questions",
    "evidence_pool",
    "phase2_questions",
)

PACKET_EVIDENCE_FIELDS = (
    "evidence_id",
    "official_page_title",
    "official_source_url",
)

FORBIDDEN_PACKET_KEYS = frozenset(
    {
        "sample_id",
        "triplet_id",
        "independence_group",
        "domain",
        "candidate_kind",
        "hkp",
        "intended_stealth",
        "hard_negative_type",
        "hn_type",
        "target_field",
        "owner_only",
        "expected_contract",
        "expected_answer",
        "ground_truth",
    }
)

FORBIDDEN_CANDIDATE_CUES = (
    "S1/S2/S3",
    "需要几个证据",
    "最少几个证据",
    "最低证据",
    "minimum evidence",
    "evidence path",
    "核验路径",
    "实验标签",
    "owner label",
    "target field",
)


def canonical_sha256(value: bytes) -> str:
    """Return a lowercase SHA-256 hex digest."""

    return sha256(value).hexdigest()


def normalized_text(value: str) -> str:
    """Normalize spacing and punctuation for structural duplicate checks."""

    return re.sub(r"[\W_]+", "", value.casefold(), flags=re.UNICODE)


class _TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._title_depth = 0
        self._h1_depth = 0
        self._title_parts: list[str] = []
        self._current_h1: list[str] = []
        self.h1_values: list[str] = []
        self.body_text_values: list[str] = []
        self._ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        lowered = tag.casefold()
        if lowered == "title":
            self._title_depth += 1
        if lowered == "h1":
            self._h1_depth += 1
            if self._h1_depth == 1:
                self._current_h1 = []
        if lowered in {"script", "style", "noscript"}:
            self._ignored_depth += 1

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.casefold()
        if lowered == "title" and self._title_depth:
            self._title_depth -= 1
        if lowered == "h1" and self._h1_depth:
            self._h1_depth -= 1
            if self._h1_depth == 0:
                value = _compact("".join(self._current_h1))
                if value:
                    self.h1_values.append(value)
        if lowered in {"script", "style", "noscript"} and self._ignored_depth:
            self._ignored_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._title_depth:
            self._title_parts.append(data)
        if self._h1_depth:
            self._current_h1.append(data)
        if not self._ignored_depth:
            value = _compact(data)
            if value:
                self.body_text_values.append(value)

    @property
    def title(self) -> str:
        return _compact("".join(self._title_parts))


def _compact(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _declared_encoding(content: bytes, content_type: str) -> str | None:
    header_match = re.search(r"charset=([^;\s]+)", content_type, re.I)
    if header_match:
        return header_match.group(1).strip("\"'").casefold()
    head = content[:8192].decode("ascii", errors="ignore")
    meta_match = re.search(r"charset=[\"']?([a-zA-Z0-9_-]+)", head, re.I)
    return meta_match.group(1).casefold() if meta_match else None


def decode_html(content: bytes, content_type: str) -> str:
    """Decode government HTML without using a researcher-authored title fallback."""

    declared = _declared_encoding(content, content_type)
    candidates = [declared, "utf-8", "gb18030"]
    for encoding in dict.fromkeys(item for item in candidates if item):
        try:
            return content.decode(encoding, errors="strict")
        except (LookupError, UnicodeDecodeError):
            continue
    # Some official pages declare UTF-8 and have a strictly decodable title,
    # yet contain isolated legacy bytes later in the body.  Surrogate escape is
    # lossless: it preserves those bytes instead of inventing replacement text,
    # while allowing the parser to bind the actual source title above them.
    if declared:
        try:
            return content.decode(declared, errors="surrogateescape")
        except LookupError:
            pass
    detected = from_bytes(content).best()
    if detected is not None:
        decoded = str(detected)
        if decoded:
            return decoded
    raise ValueError("SOURCE_TEXT_DECODING_BLOCKER")


_TITLE_MEANINGFUL_MARKERS = (
    "法",
    "条例",
    "规定",
    "办法",
    "通知",
    "意见",
    "解读",
    "答记者问",
    "决定",
    "学位",
    "教育",
    "数据",
    "证券",
    "会计",
    "采购",
    "档案",
    "职工",
    "保险",
    "主席令",
    "公司",
    "停工留薪",
)


def is_generic_portal_title(value: str) -> bool:
    compact = _compact(value)
    if not compact:
        return True
    normalized = normalized_text(compact)
    exact_generic = {
        "首页",
        "中国政府网",
        "中华人民共和国教育部政府门户网站",
        "国家市场监督管理总局",
        "国家互联网信息办公室",
    }
    if compact in exact_generic or normalized.endswith("首页"):
        return True
    return not any(marker in compact for marker in _TITLE_MEANINGFUL_MARKERS)


@dataclass(frozen=True)
class ExtractedTitle:
    display_title: str
    title_origin: str
    exact_source_text: str

    @property
    def title_source_text_hash(self) -> str:
        return canonical_sha256(self.exact_source_text.encode("utf-8"))


def extract_html_title(content: bytes, content_type: str) -> ExtractedTitle:
    decoded = decode_html(content, content_type)
    parser = _TitleParser()
    parser.feed(decoded)
    if parser.title and not is_generic_portal_title(parser.title):
        return ExtractedTitle(parser.title, "HTML_TITLE", parser.title)
    h1_candidates = [
        value for value in parser.h1_values if not is_generic_portal_title(value)
    ]
    if h1_candidates:
        heading = h1_candidates[0]
        return ExtractedTitle(heading, "PAGE_H1", heading)
    ignored_body_values = {
        "首页",
        "登录",
        "注册",
        "政务公开",
        "无障碍浏览",
        "网站地图",
        "联系我们",
    }
    document_headings = [
        value
        for value in parser.body_text_values
        if value not in ignored_body_values
        and 6 <= len(value) <= 150
        and any(marker in value for marker in _TITLE_MEANINGFUL_MARKERS)
    ]
    if document_headings:
        heading = document_headings[0]
        return ExtractedTitle(heading, "OFFICIAL_DOCUMENT_HEADING", heading)
    raise ValueError("SOURCE_TITLE_NEUTRALITY_BLOCKER")


_PDF_HEADING_PATTERN = re.compile(
    r"中华人民共和国.{0,24}(?:法|条例|规定|办法)(?:（[^）]{1,20}）)?"
)


def extract_pdf_title(content: bytes) -> ExtractedTitle:
    """Extract an actual heading from PDF text, never from its filename."""

    import importlib

    pypdf = importlib.import_module("pypdf")
    reader = pypdf.PdfReader(BytesIO(content))
    text = "\n".join((page.extract_text() or "") for page in reader.pages[:3])
    lines = [_compact(line) for line in text.splitlines() if _compact(line)]
    for line in lines:
        match = _PDF_HEADING_PATTERN.search(line.replace(" ", ""))
        if match:
            heading = match.group(0)
            return ExtractedTitle(heading, "PDF_DOCUMENT_HEADING", heading)
    raise ValueError("SOURCE_TITLE_NEUTRALITY_BLOCKER")


def opaque_digest(seed: bytes, purpose: str, identity: str) -> bytes:
    message = f"{purpose}\0{identity}".encode("utf-8")
    return hmac.new(seed, message, "sha256").digest()


def blind_review_id(seed: bytes, internal_identity: str) -> str:
    """Create a non-sequential stable ID for one frozen blind-review run."""

    return f"BR-{opaque_digest(seed, 'blind-id', internal_identity).hex()[:10].upper()}"


def deterministic_blind_order(
    identities: Sequence[str],
    group_by_identity: Mapping[str, str],
    seed: bytes,
) -> list[str]:
    """Shuffle cryptographically and avoid adjacent members of one group."""

    ranked = sorted(
        identities,
        key=lambda item: opaque_digest(seed, "blind-order", item),
    )
    remaining = list(ranked)
    output: list[str] = []
    while remaining:
        previous_group = group_by_identity[output[-1]] if output else None
        index = next(
            (
                position
                for position, identity in enumerate(remaining)
                if group_by_identity[identity] != previous_group
            ),
            None,
        )
        if index is None:
            raise ValueError("BLIND_ORDER_ADJACENCY_BLOCKER")
        output.append(remaining.pop(index))
    return output


def deterministic_constrained_blind_order(
    identities: Sequence[str],
    group_by_identity: Mapping[str, str],
    profiles: Mapping[str, Mapping[str, str]],
    seed: bytes,
    *,
    maximum_run: int = 2,
) -> list[str]:
    """Cryptographically rank rows, then enforce blind-order run constraints."""

    ranked = sorted(
        identities,
        key=lambda item: opaque_digest(seed, "blind-order", item),
    )
    remaining = list(ranked)
    output: list[str] = []
    while remaining:
        previous_group = group_by_identity[output[-1]] if output else None

        def eligible(identity: str) -> bool:
            if group_by_identity[identity] == previous_group:
                return False
            if len(output) < maximum_run:
                return True
            tail = output[-maximum_run:]
            return not any(
                all(profiles[item][field] == profiles[identity][field] for item in tail)
                for field in profiles[identity]
            )

        index = next(
            (
                position
                for position, identity in enumerate(remaining)
                if eligible(identity)
            ),
            None,
        )
        if index is None:
            raise ValueError("BLIND_ORDER_CONSTRAINT_BLOCKER")
        output.append(remaining.pop(index))
    return output


def evidence_should_swap(seed: bytes, opaque_id: str) -> bool:
    return bool(opaque_digest(seed, "evidence-order", opaque_id)[0] & 1)


def adjacent_same_group_count(
    order: Sequence[str], group_by_identity: Mapping[str, str]
) -> int:
    return sum(
        group_by_identity[left] == group_by_identity[right]
        for left, right in zip(order, order[1:], strict=False)
    )


def maximum_run(values: Sequence[str]) -> int:
    if not values:
        return 0
    best = current = 1
    for previous, current_value in zip(values, values[1:], strict=False):
        current = current + 1 if current_value == previous else 1
        best = max(best, current)
    return best


def exact_periods(values: Sequence[str], maximum_period: int = 12) -> list[int]:
    return [
        period
        for period in range(2, min(maximum_period, len(values) // 2) + 1)
        if all(value == values[index % period] for index, value in enumerate(values))
    ]


def order_profile(values: Sequence[str]) -> dict[str, Any]:
    return {
        "distribution": dict(sorted(Counter(values).items())),
        "maximum_run": maximum_run(values),
        "exact_periods_2_to_12": exact_periods(values),
    }


def iter_mapping_keys(value: Any) -> Iterable[str]:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            yield str(key)
            yield from iter_mapping_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from iter_mapping_keys(nested)


def validate_packet_rows(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if len(rows) != 72:
        raise ValueError("BLIND_PACKET_CANDIDATE_COUNT_BLOCKER")
    identities = [str(row.get("blind_review_id", "")) for row in rows]
    if len(set(identities)) != 72 or any(
        not re.fullmatch(r"BR-[0-9A-F]{10}", item) for item in identities
    ):
        raise ValueError("BLIND_REVIEW_ID_BLOCKER")
    for row in rows:
        if tuple(row) != PACKET_ROW_FIELDS:
            raise ValueError("BLIND_PACKET_ROW_SCHEMA_BLOCKER")
        forbidden = FORBIDDEN_PACKET_KEYS.intersection(iter_mapping_keys(row))
        if forbidden:
            raise ValueError(f"BLIND_PACKET_KEY_LEAKAGE:{sorted(forbidden)}")
        evidence = row["evidence_pool"]
        if len(evidence) != 2:
            raise ValueError("BLIND_PACKET_EVIDENCE_COUNT_BLOCKER")
        if any(tuple(item) != PACKET_EVIDENCE_FIELDS for item in evidence):
            raise ValueError("BLIND_PACKET_EVIDENCE_SCHEMA_BLOCKER")
        if len({item["official_source_url"] for item in evidence}) != 2:
            raise ValueError("BLIND_PACKET_EVIDENCE_DUPLICATE_BLOCKER")
        questions = list(row["phase1_questions"]) + list(row["phase2_questions"])
        if any(item.get("response") != "" for item in questions):
            raise ValueError("BLIND_PACKET_NONEMPTY_RESPONSE_BLOCKER")
        if any(
            cue.casefold() in str(row["candidate_text"]).casefold()
            for cue in FORBIDDEN_CANDIDATE_CUES
        ):
            raise ValueError("BLIND_PACKET_CANDIDATE_META_CUE_BLOCKER")
    return {
        "status": "PASS",
        "candidate_count": len(rows),
        "blind_id_unique_count": len(set(identities)),
        "machine_semantic_answer_generation": 0,
    }


def _validate_opaque_ids(rows: Sequence[Mapping[str, Any]]) -> list[str]:
    if len(rows) != 72:
        raise ValueError("PHASE_PACKET_CANDIDATE_COUNT_BLOCKER")
    identities = [str(row.get("blind_review_id", "")) for row in rows]
    if len(set(identities)) != 72 or any(
        not re.fullmatch(r"BR-[0-9A-F]{10}", item) for item in identities
    ):
        raise ValueError("PHASE_PACKET_IDENTITY_BLOCKER")
    return identities


def validate_phase1_packet_rows(
    rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Validate the candidate-only Phase1 visibility contract."""

    identities = _validate_opaque_ids(rows)
    for row in rows:
        if tuple(row) != PHASE1_PACKET_ROW_FIELDS:
            raise ValueError("PHASE1_PACKET_ROW_SCHEMA_BLOCKER")
        if any(row[field] != "" for field in PHASE1_FIELDS):
            raise ValueError("PHASE1_PACKET_NONEMPTY_RESPONSE_BLOCKER")
        forbidden = FORBIDDEN_PACKET_KEYS.intersection(iter_mapping_keys(row))
        if forbidden:
            raise ValueError(f"PHASE1_PACKET_KEY_LEAKAGE:{sorted(forbidden)}")
    serialized = "\n".join(str(dict(row)) for row in rows)
    url_count = len(re.findall(r"https?://", serialized, flags=re.I))
    if url_count:
        raise ValueError("PHASE1_PACKET_URL_LEAKAGE_BLOCKER")
    return {
        "status": "PASS",
        "candidate_count": 72,
        "phase1_visibility_contract": "72/72",
        "blind_id_unique_count": len(set(identities)),
        "evidence_url_count": 0,
        "evidence_title_count": 0,
        "evidence_id_count": 0,
        "phase2_field_count": 0,
        "sample_id_count": 0,
        "owner_label_count": 0,
        "expected_contract_count": 0,
        "review_result_filled_count": 0,
    }


def validate_phase2_packet_rows(
    rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Validate an unfilled Phase2 packet without authorizing its release."""

    identities = _validate_opaque_ids(rows)
    evidence_slot_count = 0
    for row in rows:
        if tuple(row) != PHASE2_PACKET_ROW_FIELDS:
            raise ValueError("PHASE2_PACKET_ROW_SCHEMA_BLOCKER")
        forbidden = FORBIDDEN_PACKET_KEYS.intersection(iter_mapping_keys(row))
        if forbidden:
            raise ValueError(f"PHASE2_PACKET_KEY_LEAKAGE:{sorted(forbidden)}")
        evidence = row["evidence_pool"]
        if len(evidence) != 2:
            raise ValueError("PHASE2_PACKET_EVIDENCE_COUNT_BLOCKER")
        if any(tuple(item) != PACKET_EVIDENCE_FIELDS for item in evidence):
            raise ValueError("PHASE2_PACKET_EVIDENCE_SCHEMA_BLOCKER")
        if len({str(item["official_source_url"]) for item in evidence}) != 2:
            raise ValueError("PHASE2_PACKET_EVIDENCE_DUPLICATE_BLOCKER")
        if any(row[field] != "" for field in PHASE2_FIELDS):
            raise ValueError("PHASE2_PACKET_NONEMPTY_RESPONSE_BLOCKER")
        evidence_slot_count += len(evidence)
    return {
        "status": "PASS",
        "candidate_count": 72,
        "blind_id_unique_count": len(set(identities)),
        "evidence_slots": evidence_slot_count,
        "e1_e2_distinct": "72/72",
        "review_result_filled_count": 0,
    }


def assert_phase2_release_allowed(gate: Mapping[str, bool]) -> str:
    """Fail closed until every independently recorded Phase1 lock fact is true."""

    missing = [
        name for name in PHASE2_RELEASE_REQUIREMENTS if gate.get(name) is not True
    ]
    if missing:
        raise ValueError(f"PHASE2_RELEASE_GATE_BLOCKER:{','.join(missing)}")
    return "PHASE2_RELEASE_APPROVED"


def lock_phase1_raw_return(
    raw_csv: bytes, expected_ids: Sequence[str], destination: Path
) -> str:
    """Validate and create an immutable raw-return file without normalizing bytes.

    The exclusive create mode makes a repeated or overwriting lock attempt fail.
    This helper is deliberately not called during packet preparation.
    """

    validation = validate_phase1_raw_return(raw_csv, expected_ids)
    destination.parent.mkdir(parents=True, exist_ok=True)
    sidecar = destination.with_suffix(destination.suffix + ".sha256")
    if destination.exists() or sidecar.exists():
        raise FileExistsError("PHASE1_RETURN_LOCK_ALREADY_EXISTS")
    with destination.open("xb") as handle:
        handle.write(raw_csv)
    digest = str(validation["raw_sha256"])
    with sidecar.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(f"{digest}  {destination.name}\n")
    return digest


def validate_phase1_raw_return(
    raw_csv: bytes, expected_ids: Sequence[str]
) -> dict[str, Any]:
    """Validate a Phase1 return without changing its bytes or unlocking identity.

    The returned rows retain the exact decoded field values.  They may be used
    only for derived blind-ID reports; the raw bytes remain authoritative.
    """

    try:
        decoded = raw_csv.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ValueError("PHASE1_RETURN_UTF8_BLOCKER") from error
    reader = csv.DictReader(StringIO(decoded, newline=""))
    if tuple(reader.fieldnames or ()) != PHASE1_RETURN_FIELDS:
        raise ValueError("PHASE1_RETURN_SCHEMA_BLOCKER")
    raw_rows = list(reader)
    if any(tuple(row) != PHASE1_RETURN_FIELDS for row in raw_rows) or any(
        value is None for row in raw_rows for value in row.values()
    ):
        raise ValueError("PHASE1_RETURN_SCHEMA_BLOCKER")
    rows = [
        {field: str(row[field]) for field in PHASE1_RETURN_FIELDS} for row in raw_rows
    ]
    returned_ids = [row["blind_review_id"] for row in rows]
    returned_id_set = set(returned_ids)
    expected_id_set = set(expected_ids)
    missing_ids = sorted(expected_id_set - returned_id_set)
    unexpected_ids = sorted(returned_id_set - expected_id_set)
    duplicate_id_count = len(returned_ids) - len(returned_id_set)
    blank_id_count = sum(not item for item in returned_ids)
    if (
        len(rows) != 72
        or len(expected_ids) != 72
        or len(expected_id_set) != 72
        or duplicate_id_count
        or blank_id_count
        or missing_ids
        or unexpected_ids
    ):
        raise ValueError("PHASE1_RETURN_72_72_BLOCKER")

    invalid_enum_rows: list[dict[str, str]] = []
    required_reason_rows = 0
    missing_required_reason_rows: list[str] = []
    for row in rows:
        for field, values in PHASE1_RETURN_ENUMS.items():
            if row[field] not in values:
                invalid_enum_rows.append(
                    {
                        "blind_review_id": row["blind_review_id"],
                        "field": field,
                        "value": row[field],
                    }
                )
        reason_required = (
            row["local_internal_conflict"] in {"YES", "UNCERTAIN"}
            or row["phase1_issue"] != "NONE"
        )
        if reason_required:
            required_reason_rows += 1
            if not row["phase1_reason"].strip():
                missing_required_reason_rows.append(row["blind_review_id"])
    if invalid_enum_rows:
        raise ValueError("PHASE1_RETURN_ENUM_BLOCKER")
    if missing_required_reason_rows:
        raise ValueError("PHASE1_RETURN_REASON_BLOCKER")

    naturalness_counts = Counter(row["text_naturalness"] for row in rows)
    conflict_counts = Counter(row["local_internal_conflict"] for row in rows)
    issue_counts = Counter(row["phase1_issue"] for row in rows)
    issue_rows = [row for row in rows if row["phase1_issue"] != "NONE"]
    non_natural_rows = [row for row in rows if row["text_naturalness"] != "NATURAL"]
    local_yes_rows = [row for row in rows if row["local_internal_conflict"] == "YES"]
    return {
        "status": "PASS",
        "raw_sha256": canonical_sha256(raw_csv),
        "headers": list(PHASE1_RETURN_FIELDS),
        "row_count": len(rows),
        "unique_id_count": len(returned_id_set),
        "duplicate_id_count": duplicate_id_count,
        "blank_id_count": blank_id_count,
        "missing_ids": missing_ids,
        "unexpected_ids": unexpected_ids,
        "invalid_enum_count": 0,
        "required_reason_rows": required_reason_rows,
        "missing_required_reason_count": len(missing_required_reason_rows),
        "text_naturalness_counts": dict(sorted(naturalness_counts.items())),
        "local_internal_conflict_counts": dict(sorted(conflict_counts.items())),
        "phase1_issue_counts": dict(sorted(issue_counts.items())),
        "issue_row_count": len(issue_rows),
        "non_natural_row_count": len(non_natural_rows),
        "local_yes_row_count": len(local_yes_rows),
        "rows": rows,
    }


def lexical_duplicate_qa(
    texts: Sequence[str], groups: Sequence[str] | None = None
) -> dict[str, Any]:
    if groups is not None and len(groups) != len(texts):
        raise ValueError("DUPLICATE_GROUP_CARDINALITY_BLOCKER")
    normalized = [normalized_text(text) for text in texts]
    exact_pairs: list[tuple[int, int]] = []
    near_pairs: list[dict[str, Any]] = []
    for left in range(len(normalized)):
        for right in range(left + 1, len(normalized)):
            if normalized[left] == normalized[right]:
                exact_pairs.append((left, right))
                continue
            if groups is not None and groups[left] == groups[right]:
                # Matched triplets are intentionally parallel cases.  The gate
                # rejects accidental cross-triplet template reuse instead.
                continue
            left_grams = {
                normalized[left][index : index + 4]
                for index in range(max(0, len(normalized[left]) - 3))
            }
            right_grams = {
                normalized[right][index : index + 4]
                for index in range(max(0, len(normalized[right]) - 3))
            }
            denominator = len(left_grams | right_grams)
            score = len(left_grams & right_grams) / denominator if denominator else 0.0
            if score >= 0.88:
                near_pairs.append({"left": left, "right": right, "score": score})
    return {
        "status": "PASS" if not exact_pairs and not near_pairs else "BLOCKED",
        "candidate_count": len(texts),
        "exact_duplicate_pair_count": len(exact_pairs),
        "cross_group_lexical_near_duplicate_pair_count": len(near_pairs),
        "near_duplicate_threshold": 0.88,
    }


__all__ = [
    "FORBIDDEN_PACKET_KEYS",
    "MANUAL_FIELDS",
    "PACKET_EVIDENCE_FIELDS",
    "PACKET_ROW_FIELDS",
    "PHASE1_FIELDS",
    "PHASE1_PACKET_ROW_FIELDS",
    "PHASE1_RETURN_ENUMS",
    "PHASE1_RETURN_FIELDS",
    "PHASE2_FIELDS",
    "PHASE2_PACKET_ROW_FIELDS",
    "PHASE2_RELEASE_REQUIREMENTS",
    "PHASE2_RETURN_FIELDS",
    "TITLE_ORIGINS",
    "ExtractedTitle",
    "adjacent_same_group_count",
    "assert_phase2_release_allowed",
    "blind_review_id",
    "canonical_sha256",
    "deterministic_blind_order",
    "evidence_should_swap",
    "extract_html_title",
    "extract_pdf_title",
    "lexical_duplicate_qa",
    "lock_phase1_raw_return",
    "order_profile",
    "validate_packet_rows",
    "validate_phase1_packet_rows",
    "validate_phase1_raw_return",
    "validate_phase2_packet_rows",
]
