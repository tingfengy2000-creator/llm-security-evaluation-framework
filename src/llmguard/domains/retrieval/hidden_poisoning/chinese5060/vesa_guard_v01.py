"""Conservative, role-blind rescue of already retrieved numeric evidence."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from datetime import date
from decimal import Decimal
from itertools import combinations

VERSION = "VESA_GUARD_V0.1"
_SCOPE = (
    r"《(?P<subject>[^《》\r\n]+)》[ \t]*(?P<year>[0-9]{4})年(?P<edition>修订|原)?版[ \t]*"
    r"第(?P<article>[0-9一二三四五六七八九十百零]+)条"
)
_CONDITION = r"在(?P<condition>[^，,。；;\r\n]{1,40})条件下[，,][ \t]*"
_PROPERTY = r"(?P<attribute>[\u4e00-\u9fff]{1,30})"
_QUERY = re.compile(
    rf"(?:截至(?P<as_of>[0-9]{{4}}年[0-9]{{1,2}}月[0-9]{{1,2}}日)[，,][ \t]*)?"
    rf"(?:依据|根据)?{_SCOPE}[，,:：]?[ \t]*{_CONDITION}{_PROPERTY}(?:是多少|为多少)[？?]?"
)
_CLAIM = re.compile(
    rf"{_SCOPE}(?:规定|明确)[，,:：][ \t]*{_CONDITION}{_PROPERTY}(?:为|是)"
    r"(?P<number>[0-9]{1,12}(?:\.[0-9]{1,6})?)(?P<unit>%|％|[\u4e00-\u9fff]{1,5})[。.]?"
)
_VISIBLE = re.compile(
    r"《[^《》\r\n]+》|[0-9]{4}年(?:[0-9]{1,2}月(?:[0-9]{1,2}日)?|(?:修订|原)?版)?"
    r"|第[0-9一二三四五六七八九十百零]+条|[0-9]+(?:\.[0-9]+)?[%％]"
)
_SHA = re.compile(r"[a-f0-9]{64}")
_WITNESS_FORMAT = re.compile(r"[\s，,:：。]")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class Modules:
    scope: bool = True
    graph: bool = True
    rescue: bool = True


def rule_sha256(modules: Modules = Modules()) -> str:
    return sha(json.dumps({
        "version": VERSION, "modules": asdict(modules), "query": _QUERY.pattern, "claim": _CLAIM.pattern,
        "visible_scope": _VISIBLE.pattern, "max_topk": 5, "min_independent_retained_witnesses": 1,
        "max_rescues_for_single_requested_fact": 1, "date_interval": "START_INCLUSIVE_END_EXCLUSIVE",
        "unknown_policy": "KEEP_B2_ISOLATION", "distinct_normalized_text_required": True,
        "witness_format": _WITNESS_FORMAT.pattern,
    }, sort_keys=True, ensure_ascii=False).encode())


@dataclass(frozen=True)
class SourceAttestation:
    """Issued by an upstream verified registry, never built from text or a self-claimed publisher."""

    content_sha256: str
    publisher_id: str
    lineage_id: str
    version_year: int
    version_key: str
    edition: str = ""
    valid_from: date | None = None
    valid_until: date | None = None


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    rank: int
    text: str
    content_sha256: str
    source: SourceAttestation | None = None


@dataclass(frozen=True)
class Scope:
    subject: str
    year: int
    edition: str
    article: str
    condition: str
    attribute: str


@dataclass(frozen=True)
class Span:
    start: int
    end: int
    sha256: str


@dataclass(frozen=True)
class Claim:
    scope: Scope
    value: Decimal
    unit: str
    span: Span


@dataclass(frozen=True)
class Relation:
    left_id: str
    right_id: str
    status: str
    independent: bool


@dataclass(frozen=True)
class ChunkTrace:
    chunk_id: str
    visible_spans: tuple[Span, ...]
    claim_span: Span | None
    scope: str
    source: str
    risk: str
    reason: str
    witness_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class Decision:
    retained_chunk_ids: tuple[str, ...]
    removed_ids: tuple[str, ...]
    restored_ids: tuple[str, ...]
    unknown_claims: tuple[str, ...]
    query_scope: str
    query_spans: tuple[Span, ...]
    reasons_by_chunk: tuple[ChunkTrace, ...]
    relations: tuple[Relation, ...]
    algorithm_version_hash: str


def _span(text: str, match: re.Match[str]) -> Span:
    return Span(match.start(), match.end(), sha(text[match.start():match.end()].encode()))


def _scope(match: re.Match[str]) -> Scope:
    return Scope(match["subject"], int(match["year"]), match["edition"] or "", match["article"],
                 match["condition"], match["attribute"])


def _claim(text: str) -> Claim | None:
    # A restored chunk must be a single fully parsed assertion, with no extra text or instructions.
    found = _CLAIM.fullmatch(text)
    if found is None:
        return None
    return Claim(_scope(found), Decimal(found["number"]), found["unit"].replace("％", "%"), _span(text, found))


def _applicable(chunk: Chunk, claim: Claim | None, demand: Scope | None, as_of: date | None) -> str:
    if claim is None or demand is None:
        return "UNKNOWN"
    if claim.scope != demand:
        return "DIFFERENT_SCOPE"
    source = chunk.source
    if source is None or (source.version_year, source.edition) != (demand.year, demand.edition):
        return "UNKNOWN_VERSION_BINDING"
    if as_of is not None:
        if source.valid_from is None:
            return "UNKNOWN_VALIDITY_PERIOD"
        if as_of < source.valid_from or (source.valid_until is not None and as_of >= source.valid_until):
            return "OUTSIDE_VALIDITY_PERIOD"
    return "APPLICABLE"


def _independent(a: Chunk, b: Chunk) -> bool:
    left, right = a.source, b.source
    return bool(left is not None and right is not None and left.publisher_id != right.publisher_id
                and left.lineage_id != right.lineage_id and left.version_key == right.version_key
                and _WITNESS_FORMAT.sub("", a.text.rstrip(".")) != _WITNESS_FORMAT.sub("", b.text.rstrip(".")))


def _relation(a: Chunk, b: Chunk, ca: Claim | None, cb: Claim | None) -> Relation:
    if (ca is None or cb is None or ca.scope != cb.scope or ca.unit != cb.unit
            or (a.source is not None and b.source is not None and a.source.version_key != b.source.version_key)):
        return Relation(a.chunk_id, b.chunk_id, "UNKNOWN", False)
    if ca.value != cb.value:
        return Relation(a.chunk_id, b.chunk_id, "EXPLICIT_CONFLICT", False)
    return Relation(a.chunk_id, b.chunk_id, "EXPLICIT_COMPATIBLE", _independent(a, b))


def _validate(topk: Sequence[Chunk], retained: Sequence[str]) -> dict[str, Chunk]:
    ids: dict[str, Chunk] = {}
    for rank, chunk in enumerate(topk, 1):
        if (type(chunk) is not Chunk or not chunk.chunk_id or chunk.chunk_id in ids or type(chunk.rank) is not int
                or chunk.rank != rank or sha(chunk.text.encode()) != chunk.content_sha256):
            raise ValueError("TOPK_CHUNK_ID_RANK_OR_HASH_DRIFT")
        proof = chunk.source
        if proof is not None and (
            type(proof) is not SourceAttestation or not _SHA.fullmatch(proof.content_sha256)
            or proof.content_sha256 != chunk.content_sha256 or not proof.publisher_id or not proof.lineage_id
            or not proof.version_key
            or (proof.valid_from is not None and proof.valid_until is not None
                and proof.valid_from >= proof.valid_until)
        ):
            raise ValueError("INVALID_UPSTREAM_SOURCE_ATTESTATION")
        ids[chunk.chunk_id] = chunk
    if len(ids) > 5 or tuple(retained) != tuple(cid for cid in ids if cid in retained):
        raise ValueError("B2_NOT_AN_ORDERED_TOPK_SUBSET")
    return ids


def vesa_select(
    query: str, topk: Sequence[Chunk], b2_retained_ids: Sequence[str], *, modules: Modules = Modules(),
) -> Decision:
    ids = _validate(topk, b2_retained_ids)
    found = _QUERY.fullmatch(query) if modules.scope else None
    demand = _scope(found) if found else None
    as_of = None
    if found is not None and found["as_of"]:
        try:
            as_of = date(*(int(value) for value in re.findall(r"[0-9]+", found["as_of"])))
        except ValueError:
            demand = None
    claims = {cid: _claim(chunk.text) if modules.scope else None for cid, chunk in ids.items()}
    scope = {cid: _applicable(chunk, claims[cid], demand, as_of) for cid, chunk in ids.items()}
    relations = tuple(
        _relation(a, b, claims[a.chunk_id], claims[b.chunk_id])
        if "OUTSIDE_VALIDITY_PERIOD" not in (scope[a.chunk_id], scope[b.chunk_id])
        else Relation(a.chunk_id, b.chunk_id, "UNKNOWN", False)
        for a, b in combinations(topk, 2)
    ) if modules.graph else ()
    compatible = {frozenset((edge.left_id, edge.right_id)) for edge in relations
                  if edge.status == "EXPLICIT_COMPATIBLE" and edge.independent}
    before = set(b2_retained_ids)
    eligible = {cid for cid, verdict in scope.items() if verdict == "APPLICABLE"}
    versions = {cid: c.source.version_key for cid, c in ids.items() if c.source is not None}
    retained_anchor = before & eligible
    already_independent = any(pair <= retained_anchor for pair in compatible)
    restored: list[str] = []
    traces = []
    for cid, chunk in ids.items():
        claim = claims[cid]
        source = chunk.source
        witnesses: tuple[str, ...] = ()
        if cid in before:
            reason = "B2_RETAINED"
        elif not (modules.scope and modules.graph and modules.rescue):
            reason = "MODULE_DISABLED"
        elif source is None:
            reason = "NO_VERIFIED_SOURCE_ATTESTATION"
        elif cid not in eligible or claim is None:
            reason = "SCOPE_OR_VERSION_NOT_VERIFIED"
        elif any(edge.status == "EXPLICIT_CONFLICT" and cid in (edge.left_id, edge.right_id) for edge in relations):
            reason = "EXPLICIT_CONFLICT"
        elif any(
            (other_claim is None and claim.scope.subject in ids[other].text and claim.scope.attribute in ids[other].text)
            or (other_claim is not None and other_claim.scope == claim.scope and other_claim.unit != claim.unit)
            or (other_claim is not None and other_claim.scope == claim.scope
                and other in versions and versions[other] != versions[cid])
            for other, other_claim in claims.items() if other != cid
        ):
            reason = "UNRESOLVED_RELEVANT_EVIDENCE"
        elif already_independent or restored:
            reason = "NO_ADDITIONAL_REQUIRED_COVERAGE"
        else:
            witnesses = tuple(other for other in ids if other in retained_anchor
                              and frozenset((cid, other)) in compatible)
            if witnesses:
                reason = "RESTORED_WITH_APPLICABLE_INDEPENDENT_WITNESS"
                restored.append(cid)
            else:
                reason = "NO_INDEPENDENT_RETAINED_WITNESS"
        traces.append(ChunkTrace(
            cid, tuple(_span(chunk.text, match) for match in _VISIBLE.finditer(chunk.text)),
            claim.span if claim else None, scope[cid],
            "VERIFIED_REGISTRY_BOUND" if chunk.source else "UNVERIFIED",
            "INHERITED_B2_RETAINED" if cid in before else "RESCUE_AUDITABLE" if cid in restored else "B2_ISOLATED",
            reason, witnesses,
        ))
    kept = before | set(restored)
    return Decision(
        tuple(cid for cid in ids if cid in kept), tuple(cid for cid in ids if cid not in kept),
        tuple(restored), tuple(cid for cid in ids if scope[cid].startswith("UNKNOWN")),
        "EXPLICIT_SCOPE" if demand is not None else "UNKNOWN",
        tuple(_span(query, match) for match in _VISIBLE.finditer(query)), tuple(traces),
        relations, rule_sha256(modules),
    )
