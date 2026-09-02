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
from io import BytesIO
import re
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
    "PHASE2_FIELDS",
    "TITLE_ORIGINS",
    "ExtractedTitle",
    "adjacent_same_group_count",
    "blind_review_id",
    "canonical_sha256",
    "deterministic_blind_order",
    "evidence_should_swap",
    "extract_html_title",
    "extract_pdf_title",
    "lexical_duplicate_qa",
    "order_profile",
    "validate_packet_rows",
]
