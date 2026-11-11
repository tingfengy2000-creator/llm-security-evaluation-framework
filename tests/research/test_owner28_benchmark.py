"""Engineering-only tests of the Owner28 handoff and seal boundaries."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner28_benchmark import (
    ARMS,
    AUTHORITY,
    EXCLUDED,
    assemble_masks,
    parse_json,
    sha,
    validate_curator,
    validate_payload,
)

sys.path.insert(0, str(Path("scripts/research").resolve()))
import run_chinese5060_owner28 as runner  # noqa: E402


def identifier(prefix: str, n: int) -> str:
    return f"{prefix}-{n:024x}"


def invented(count: int = 2) -> dict[str, Any]:
    worlds = []
    for i in range(count):
        documents = []
        for j in range(11):
            text = f"虚构纸鹤展览的示例说明。展台编号为{i * 11 + j}。"
            documents.append({"document_id": identifier("d", i * 11 + j), "source_id": identifier("s", j),
                              "text": text, "content_sha256": sha(text.encode()), "source_uri": None})
        worlds.append({"world_id": identifier("w", i), "fact_uid": identifier("f", i // 8),
                       "event_date": "2025-02-01", "query_text": "怎样参观虚构纸鹤展？", "documents": documents})
    return {"schema_version": "OWNER28_ROLE_FREE_V1", "main": worlds, "mirrors": []}


def curator(payload_sha: str) -> dict[str, Any]:
    return {
        "schema_version": "OWNER28_CURATOR_V1", "authority": AUTHORITY,
        "producer_branch": "research/paper1-ragdefender-repro-5090",
        "role_free_sha256": payload_sha, "private_custody_sha256": "b" * 64,
        "query_view_sha256": "c" * 64, "selection_sha256": "d" * 64,
        "main_worlds": 32, "mirror_worlds": 0, "label_status": "AGENT_PROVISIONAL", "human_gold": 0,
        "dev_outputs_accessed": False, "source_type": "SOURCE_GROUNDED_PARAPHRASE",
        "attestation": "INDEPENDENT_SOURCE_AND_QUERY_AUDIT_PASSED", "excluded_lineages": sorted(EXCLUDED),
        "source_audits": [
            {"fact_uid": identifier("f", i), "lineage_id": f"FICTION_LINE_{i // 2}", "issuer_class": f"CLASS_{i // 2}",
             "old_uri": "https://test.gov.cn/example/old", "new_uri": "https://test.gov.cn/example/new",
             "old_effective_from": "2024-01-01", "old_effective_until": "2025-01-01", "new_effective_from": "2025-01-01",
             "old_locator": "fictional section 1", "new_locator": "fictional section 2",
             "transition_check": "NO_UNRESOLVED_TRANSITION_FOR_THIS_SCOPE",
             "scope_check": "MATCHED_SAME_OBJECT_PREDICATE", "rights": "SELF_AUTHORED_PRIVATE_LOCAL_ONLY"}
            for i in range(4)
        ],
    }


@pytest.mark.parametrize("field", ["labels", "ground_truth", "expected_answer", "normalized_value_sha256", "role"])
def test_unknown_document_keys_rejected(field: str) -> None:
    payload = invented()
    payload["main"][0]["documents"][0][field] = "untrusted extra field"
    with pytest.raises(ValueError, match="ROLE_FREE_SCHEMA"):
        validate_payload(payload, fixture=True)


def test_hash_mismatch_and_duplicate_keys_fail_closed() -> None:
    payload = invented()
    payload["main"][0]["documents"][0]["text"] += " changed"
    with pytest.raises(ValueError, match="DOCUMENT_BYTES"):
        validate_payload(payload, fixture=True)
    with pytest.raises(ValueError, match="DUPLICATE_JSON_KEY"):
        parse_json(b'{"event_date":"2020-01-01","event_date":"2021-01-01"}')


def test_actual_size_and_group_partition() -> None:
    assert len(validate_payload(invented(32))) == 32
    with pytest.raises(ValueError, match="WORLD_DENOMINATOR"):
        validate_payload(invented())
    payload = invented(32)
    payload["main"][0]["fact_uid"] = identifier("f", 4)
    with pytest.raises(ValueError, match="FOUR_FACTS_EIGHT_WORLDS"):
        validate_payload(payload)


def test_worlds_cannot_share_document_uid() -> None:
    payload = invented()
    payload["main"][1]["documents"][0]["document_id"] = payload["main"][0]["documents"][0]["document_id"]
    with pytest.raises(ValueError, match="CROSS_WORLD_DOCUMENT_ID"):
        validate_payload(payload, fixture=True)


def test_curator_manifest_requires_exclusion_rights_and_hash() -> None:
    manifest = curator("a" * 64)
    validate_curator(manifest, "a" * 64, 0)
    with pytest.raises(ValueError, match="CURATOR_PAYLOAD_BINDING"):
        validate_curator(manifest, "e" * 64, 0)
    for field, value, code in (("lineage_id", "DRIVING_LICENSE", "LINEAGE_OR_SCOPE_GATE"),
                               ("rights", "UNKNOWN", "RIGHTS_GATE")):
        wrong = copy.deepcopy(manifest)
        wrong["source_audits"][0][field] = value
        with pytest.raises(ValueError, match=code):
            validate_curator(wrong, "a" * 64, 0)


def test_blind_predictor_refuses_custody_and_network() -> None:
    with pytest.raises(PermissionError, match="EVALUATION_CUSTODY_DENIED"):
        runner.offline_guard("open", ("EVAL_LABEL_CUSTODY.json",))
    with pytest.raises(PermissionError, match="OWNER28_NO_NETWORK"):
        runner.offline_guard("socket.connect", ())


def test_no_rank_reordering_or_mask_expansion() -> None:
    texts = ["无明确日期", "自2024年1月1日起", "自2025年1月1日起", "旧日志", "备注"]
    masks = assemble_masks(5, "2025-02-01", texts, [2, 0], [4, 2, 0])
    assert tuple(masks) == ARMS
    assert masks["RD_B2"] == [1, 3, 4]
    assert masks["RD_ZH"] == [1, 3]
    assert masks["DATE_ONLY"] == [0, 2, 3, 4]
    with pytest.raises(ValueError, match="INVALID_RD_MASK"):
        assemble_masks(5, "2025-02-01", texts, [5], [])


def test_fixture_cannot_export_scientific_readiness(tmp_path: Path) -> None:
    source = tmp_path / "fixture.json"
    source.write_text(json.dumps(invented()), encoding="utf-8")
    opts = SimpleNamespace(out=tmp_path, input=source)
    sha_seal = runner.fixture(opts)
    seal = parse_json((tmp_path / "PREDICTION_SEAL.json").read_bytes())
    assert seal["fixture"] and seal["new_scientific_results"] == 0
    assert sha_seal == hashlib.sha256((tmp_path / "PREDICTION_SEAL.json").read_bytes()).hexdigest()
    assert seal["prediction_sha256"] == sha((tmp_path / "PREDICTIONS_ROLE_FREE.json").read_bytes())
    with pytest.raises(ValueError, match="SCIENTIFIC_PREDICTION_SEAL_REQUIRED"):
        runner.export_receipt(tmp_path, sha_seal)
    with pytest.raises(FileExistsError):
        runner.fixture(opts)


def test_check_requires_freeze_before_reading_unseen_bytes(monkeypatch: pytest.MonkeyPatch) -> None:
    def block(_commit: str) -> dict[str, str]:
        raise ValueError("FROZEN_BRANCH_AND_HEAD_REQUIRED")

    monkeypatch.setattr(runner, "check_freeze", block)
    with pytest.raises(ValueError, match="FROZEN_BRANCH_AND_HEAD_REQUIRED"):
        runner.admit(SimpleNamespace(code_commit="a" * 40))
