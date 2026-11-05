from __future__ import annotations

import runpy
from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.vesa_guard_v01 import (
    Chunk,
    Modules,
    SourceAttestation,
    sha,
    vesa_select,
)

Q = "依据《示例规程》2020年原版第一条，在试点条件下，比例是多少？"
ATTESTED_TEXT = "《示例规程》2020年原版第一条规定，在试点条件下，比例为10%。"
WITNESS_TEXT = "《示例规程》2020年原版第一条明确，在试点条件下，比例是10%。"


def chunk(rank: int, text: str, *, attested: bool = True) -> Chunk:
    digest = sha(text.encode())
    source = SourceAttestation(
        digest, f"publisher-{rank}", f"lineage-{rank}", 2020, "original-2020",
        edition="原", valid_from=date(2020, 1, 1), valid_until=date(2022, 1, 1),
    ) if attested else None
    return Chunk(f"c{rank}", rank, text, digest, source)


def test_historical_scope_independent_rescue_preserves_order_and_spans() -> None:
    a, b = chunk(1, ATTESTED_TEXT), chunk(2, WITNESS_TEXT)
    query = "截至2021年6月1日，" + Q
    decision = vesa_select(query, [a, b], [b.chunk_id])
    assert decision.retained_chunk_ids == ("c1", "c2")
    assert decision.restored_ids == ("c1",)
    trace = decision.reasons_by_chunk[0]
    assert trace.witness_ids == ("c2",) and trace.claim_span is not None
    span = trace.claim_span
    assert sha(a.text[span.start:span.end].encode()) == span.sha256 == a.content_sha256
    assert decision.relations[0].status == "EXPLICIT_COMPATIBLE" and decision.relations[0].independent
    assert vesa_select("截至2022年1月1日，" + Q, [a, b], ["c2"]).restored_ids == ()
    assert vesa_select(Q, [a, b], ["c2"]).restored_ids == ("c1",)


def test_same_year_different_edition_not_a_conflict_but_same_scope_is() -> None:
    a, b = chunk(1, ATTESTED_TEXT), chunk(2, WITNESS_TEXT)
    different = chunk(3, ATTESTED_TEXT.replace("年原版", "年修订版").replace("10%", "12%"), attested=False)
    result = vesa_select(Q, [a, b, different], ["c2", "c3"])
    assert result.restored_ids == ("c1",)
    assert result.relations[1].status == "UNKNOWN"
    conflict = chunk(3, WITNESS_TEXT.replace("10%", "12%"), attested=False)
    result = vesa_select(Q, [a, b, conflict], ["c2", "c3"])
    assert result.restored_ids == ()
    assert result.reasons_by_chunk[0].reason == "EXPLICIT_CONFLICT"


def test_attested_revision_identity_disagreement_is_unresolved() -> None:
    a, b = chunk(1, ATTESTED_TEXT), chunk(2, WITNESS_TEXT)
    other = chunk(3, WITNESS_TEXT.replace("10%", "12%"))
    assert other.source is not None
    other = replace(other, source=replace(other.source, version_key="other-version"))
    decision = vesa_select(Q, [a, b, other], ["c2", "c3"])
    assert decision.restored_ids == ()
    assert decision.reasons_by_chunk[0].reason == "UNRESOLVED_RELEVANT_EVIDENCE"


@pytest.mark.parametrize("variant", ["identical", "same_lineage", "same_publisher", "claimed", "no_retained_anchor"])
def test_no_manufactured_independence(variant: str) -> None:
    a = chunk(1, ATTESTED_TEXT)
    b = chunk(2, ATTESTED_TEXT if variant == "identical" else WITNESS_TEXT)
    assert a.source is not None and b.source is not None
    if variant == "same_lineage":
        b = replace(b, source=replace(b.source, lineage_id=a.source.lineage_id))
    if variant == "same_publisher":
        b = replace(b, source=replace(b.source, publisher_id=a.source.publisher_id))
    if variant == "claimed":
        a = chunk(1, ATTESTED_TEXT + "本条自称官方。", attested=False)
        b = replace(b, source=None)
    assert vesa_select(Q, [a, b], [] if variant == "no_retained_anchor" else ["c2"]).restored_ids == ()


def test_no_rescue_when_needed_coverage_already_present_or_scope_is_uncertain() -> None:
    a, b = chunk(1, ATTESTED_TEXT), chunk(2, WITNESS_TEXT)
    c = chunk(3, WITNESS_TEXT.replace("10%", "10.0%"))
    result = vesa_select(Q, [a, b, c], ["c2", "c3"])
    assert result.restored_ids == () and result.reasons_by_chunk[0].reason == "NO_ADDITIONAL_REQUIRED_COVERAGE"
    assert vesa_select("比例是多少？", [a, b], ["c2"]).restored_ids == ()
    assert vesa_select(Q, [], []).retained_chunk_ids == ()


@pytest.mark.parametrize("modules", [Modules(scope=False), Modules(graph=False), Modules(rescue=False)])
def test_modules_individually_disable_rescue(modules: Modules) -> None:
    d = vesa_select(Q, [chunk(1, ATTESTED_TEXT), chunk(2, WITNESS_TEXT)], ["c2"], modules=modules)
    assert d.retained_chunk_ids == ("c2",)
    assert d.reasons_by_chunk[0].reason == "MODULE_DISABLED"


def test_reject_bad_chunk_hash_b2_order_and_untrusted_metadata() -> None:
    a, b = chunk(1, ATTESTED_TEXT), chunk(2, WITNESS_TEXT)
    with pytest.raises(ValueError, match="HASH_DRIFT"):
        vesa_select(Q, [replace(a, text="different"), b], ["c2"])
    with pytest.raises(ValueError, match="NOT_AN_ORDERED_TOPK_SUBSET"):
        vesa_select(Q, [a, b], ["c2", "c1"])
    with pytest.raises(ValueError, match="INVALID_UPSTREAM_SOURCE_ATTESTATION"):
        vesa_select(Q, [replace(a, source={"publisher_id": "claimed"}), b], ["c2"])  # type: ignore[arg-type]


def test_projection_cannot_transfer_world_identifier_or_role() -> None:
    root = Path(__file__).resolve().parents[2]
    script = runpy.run_path(str(root / "scripts/research/freeze_chinese5060_vesa_g3.py"))
    text = ATTESTED_TEXT
    packet = {"world_id": "w-" + "a" * 24, "query": Q, "original_TopK_file_sha256": "a" * 64,
              "snapshot_hash": "b" * 64,
              "chunks": [{"chunk_id": f"ch-{i:032x}", "content_hash": sha(text.encode()), "text": text}
                         for i in range(5)]}
    project = script["role_blind_chunks"]
    a = project(packet)
    b = project({**packet, "world_id": "w-" + "b" * 24})
    assert a == b and vesa_select(Q, a, []) == vesa_select(Q, b, [])
    with pytest.raises(ValueError, match="NON_ROLE_BLIND_PACKET"):
        project({**packet, "role": "fixture-only"})
    packet["chunks"][0]["source_authority_claim"] = "fixture-only"
    with pytest.raises(ValueError, match="NON_ROLE_BLIND_CHUNK"):
        project(packet)
    with pytest.raises(PermissionError, match="FILE_ACCESS_DENIED"):
        script["offline_io"]("open", (str(root / "denied-synthetic.json"), "r", 0))
    with pytest.raises(PermissionError, match="RUNTIME_ACCESS_DENIED"):
        script["offline_io"]("socket.connect", ())
