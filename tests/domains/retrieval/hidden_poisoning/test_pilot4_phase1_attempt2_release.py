from __future__ import annotations

import csv
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
from typing import Any

import pytest

from llmguard.domains.retrieval.hidden_poisoning.external_blind_review import (
    PHASE1_FIELDS,
    PHASE1_RETURN_FIELDS,
    PHASE2_FIELDS,
    PHASE2_RETURN_FIELDS,
)
from scripts.research import release_pilot4_phase2_attempt2 as release


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def _fixture(tmp_path: Path) -> dict[str, Path]:
    ids = [f"BR-{index:010X}" for index in range(72)]
    phase1_rows = [
        {
            "blind_review_id": opaque_id,
            "candidate_text": f"《测试制度{index:02d}》自2024年1月1日起施行。",
            "source_title": f"测试制度{index:02d}",
            **{field: "" for field in PHASE1_FIELDS},
        }
        for index, opaque_id in enumerate(ids)
    ]
    phase1_packet = tmp_path / "phase1.jsonl"
    _write_jsonl(phase1_packet, phase1_rows)

    stream = StringIO()
    writer = csv.DictWriter(stream, fieldnames=PHASE1_RETURN_FIELDS)
    writer.writeheader()
    for index, opaque_id in enumerate(ids):
        yes = index < 7
        writer.writerow(
            {
                "blind_review_id": opaque_id,
                "text_naturalness": "MINOR_ISSUE" if index < 13 else "NATURAL",
                "local_internal_conflict": "YES" if yes else "NO",
                "phase1_issue": "NONE",
                "phase1_reason": "internal conflict" if yes else "",
            }
        )
    source = tmp_path / release.RAW_FILENAME
    source.write_bytes(stream.getvalue().encode("utf-8"))

    phase2_rows = []
    provenance_records = []
    for index, phase1 in enumerate(phase1_rows):
        evidence = []
        for slot in (1, 2):
            url = f"https://example.gov/{index}/{slot}"
            title = f"官方证据{index}-{slot}"
            evidence.append(
                {
                    "evidence_id": f"E{slot}",
                    "official_page_title": title,
                    "official_source_url": url,
                }
            )
            provenance_records.append(
                {
                    "source_url": url,
                    "source_identity": title,
                    "support_excerpt": f"{title} verified source text",
                    "http_status": 200,
                    "source_snapshot_hash": "a" * 64,
                }
            )
        phase2_rows.append(
            {
                "blind_review_id": phase1["blind_review_id"],
                "candidate_text": phase1["candidate_text"],
                "source_title": phase1["source_title"],
                "evidence_pool": evidence,
                **{field: "" for field in PHASE2_FIELDS},
            }
        )
    withheld = tmp_path / "withheld"
    _write_jsonl(
        withheld / "PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_PACKET.jsonl",
        phase2_rows,
    )
    (withheld / "PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_PACKET.md").write_text(
        "# Packet\n\nStatus: `DO_NOT_RELEASE_BEFORE_ATTEMPT2_PHASE1_LOCK_AND_TRIAGE`\n",
        encoding="utf-8",
    )
    (withheld / "PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_GUIDE.md").write_text(
        "# Guide\n\nStatus: `DO_NOT_RELEASE_BEFORE_PHASE1_LOCK`\n",
        encoding="utf-8",
    )
    template = StringIO()
    csv.DictWriter(template, fieldnames=PHASE2_RETURN_FIELDS).writeheader()
    (withheld / "PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_TEMPLATE.csv").write_text(
        template.getvalue(), encoding="utf-8"
    )

    source_registry = tmp_path / "source_registry.json"
    _write_json(
        source_registry,
        {"records": provenance_records},
    )
    attempt1 = tmp_path / "attempt1"
    attempt1_raw = attempt1 / "raw" / "PILOT4_EXTERNAL_BLIND_PHASE1_RETURN.csv"
    attempt1_raw.parent.mkdir(parents=True)
    attempt1_raw.write_bytes(b"attempt1")
    preparation = tmp_path / "preparation"
    _write_json(preparation / "manifest.json", {"status": "immutable"})
    corpus = tmp_path / "corpus.jsonl"
    corpus.write_bytes(b"final corpus")
    return {
        "source": source,
        "phase1_packet": phase1_packet,
        "withheld_phase2": withheld,
        "source_registries": [source_registry],
        "attempt1_return_root": attempt1,
        "attempt2_preparation_root": preparation,
        "final_corpus": corpus,
    }


def test_attempt2_lock_releases_only_after_all_six_facts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    paths = _fixture(tmp_path)
    monkeypatch.setattr(
        release, "EXPECTED_RAW_SHA256", sha256(paths["source"].read_bytes()).hexdigest()
    )
    monkeypatch.setattr(release, "ATTEMPT1_RAW_SHA256", sha256(b"attempt1").hexdigest())
    monkeypatch.setattr(
        release, "FINAL_CORPUS_SHA256", sha256(b"final corpus").hexdigest()
    )
    output = tmp_path / "output"
    result = release.build(
        output=output, expected_sha256=release.EXPECTED_RAW_SHA256, **paths
    )
    assert result["candidate_quality_gate"] == "PASS"
    assert result["phase2_release_approved"] is True
    assert result["row_count"] == result["unique_id_count"] == 72
    gate = json.loads(
        (output / "qa" / "phase2_release_gate.json").read_text(encoding="utf-8")
    )
    assert all(gate["requirements"].values())
    lock = json.loads(
        (output / "qa" / "phase1_attempt2_return_lock.json").read_text(encoding="utf-8")
    )
    assert lock["EXPECTED_CONTRACT_LOADED"] is False
    assert lock["IDENTITY_MAPPING_UNLOCKED"] is False
    assert (output / "raw" / release.RAW_FILENAME).read_bytes() == paths[
        "source"
    ].read_bytes()
    packet = (
        output / "release" / "PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_PACKET.md"
    ).read_text(encoding="utf-8")
    guide = (
        output / "release" / "PILOT4_EXTERNAL_BLIND_PHASE2_ATTEMPT2_GUIDE.md"
    ).read_text(encoding="utf-8")
    assert "RELEASED_TO_OWNER_FOR_EXTERNAL_PHASE2_REVIEW" in packet
    assert "Phase1 is locked and immutable" in guide


def test_attempt2_lock_fails_closed_when_any_candidate_issue_remains(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    paths = _fixture(tmp_path)
    text = paths["source"].read_text(encoding="utf-8")
    paths["source"].write_text(text.replace(",NONE,", ",OTHER,", 1), encoding="utf-8")
    monkeypatch.setattr(release, "ATTEMPT1_RAW_SHA256", sha256(b"attempt1").hexdigest())
    monkeypatch.setattr(
        release, "FINAL_CORPUS_SHA256", sha256(b"final corpus").hexdigest()
    )
    digest = sha256(paths["source"].read_bytes()).hexdigest()
    with pytest.raises(ValueError, match="CANDIDATE_DEFECT_GATE|DESCRIPTIVE_COUNT"):
        release.build(output=tmp_path / "blocked", expected_sha256=digest, **paths)
    assert not (tmp_path / "blocked").exists()


def test_release_builder_has_no_mapping_or_expected_contract_input() -> None:
    import inspect

    parameters = set(inspect.signature(release.build).parameters)
    assert not parameters.intersection(
        {"identity_mapping", "mapping", "expected_contract", "expected_answer"}
    )
