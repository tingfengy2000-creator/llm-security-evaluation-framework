"""Fair input, index correspondence, and seal-before-evaluation regression tests."""
import hashlib
import json

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.b12 import (
    require_pair_seal,
    validate_packets,
    validate_removed,
)


def packets():
    return [{"world_id": f"w-{i}", "query": "测试", "original_TopK_file_sha256": "0" * 64,
        "snapshot_hash": "1" * 64, "chunks": [{"chunk_id": str(j), "text": "测试",
        "content_hash": hashlib.sha256("测试".encode()).hexdigest()} for j in range(5)]} for i in range(36)]


def test_packet_metadata_cannot_add_label():
    values = packets()
    validate_packets(values)
    values[0]["role"] = "SECRET"
    with pytest.raises(ValueError, match="UNEXPECTED_PACKET_METADATA"):
        validate_packets(values)


def test_text_mutation_or_missing_world_fails():
    values = packets()
    values[0]["chunks"][0]["text"] = "变更"
    with pytest.raises(ValueError, match="CHUNK_TEXT_CHANGED"):
        validate_packets(values)
    with pytest.raises(ValueError, match="EXACT_36"):
        validate_packets(values[:-1])


@pytest.mark.parametrize("removed,safe", [([0, 0], ["b"]), ([2], ["a", "b"]), ([0], ["changed"])])
def test_removed_index_and_original_text_correspondence(removed, safe):
    with pytest.raises(ValueError):
        validate_removed(["a", "b"], safe, removed)


def test_duplicate_texts_must_be_removed_by_index():
    validate_removed(["a", "a", "b"], ["a", "b"], [1])


def test_tampered_or_incomplete_seal_fails(tmp_path):
    with pytest.raises(FileNotFoundError):
        require_pair_seal(tmp_path)
    (tmp_path / "out.json").write_text("original")
    seal = {"worlds": 36, "outcomes": 72, "status": "SEALED_ALL_OUTCOMES", "records": [
        {"path": "out.json", "sha256": hashlib.sha256(b"original").hexdigest()}]}
    (tmp_path / "PAIR_OUTPUT_SEAL.json").write_text(json.dumps(seal))
    require_pair_seal(tmp_path)
    (tmp_path / "out.json").write_text("tamper")
    with pytest.raises(ValueError, match="SEALED_PAIR_OUTPUT_CHANGED"):
        require_pair_seal(tmp_path)
