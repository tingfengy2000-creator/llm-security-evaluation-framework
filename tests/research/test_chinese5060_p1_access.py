from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.d1_access import Binding, D1Reader


@pytest.fixture
def reader(tmp_path: Path) -> D1Reader:
    (tmp_path / "allowed.json").write_bytes(b'{"fixture":true}')
    return D1Reader(tmp_path, {"fixture": Binding("allowed.json", hashlib.sha256(b'{"fixture":true}').hexdigest())})


@pytest.mark.parametrize("path_case", ["D2/data.json", "D3/data.json", "Reviewer/answers.json",
    "evaluation/oracle.jsonl", "../allowed.json", "sub/../allowed.json", "allowed.json:secret",
    "D:/D2/data.json", "/D2/data.json", "allowed.json/", "ALLOWED.JSON", "*.json", "."])
def test_denied_paths_fail_before_content_read_or_resolution(reader: D1Reader, path_case: str, monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: object, **kwargs: object) -> bytes:
        raise AssertionError("unlisted path must not touch filesystem")
    monkeypatch.setattr(Path, "read_bytes", forbidden)
    monkeypatch.setattr(Path, "resolve", forbidden)
    with pytest.raises(PermissionError, match="D1_PATH_NOT_ALLOWLISTED"):
        reader.read_relative(path_case)
    assert reader.events[-1]["status"] == "DENIED_BEFORE_IO"


def test_valid_exact_path_and_hash(reader: D1Reader) -> None:
    assert reader.read("fixture") == b'{"fixture":true}'
    assert reader.events == [{"request": "fixture", "status": "PINNED_READ"}]


def test_changed_authorized_file_is_not_silently_accepted(reader: D1Reader) -> None:
    (reader.workspace / "allowed.json").write_bytes(b'{"fixture":false}')
    with pytest.raises(ValueError, match="D1_PIN_MISMATCH"):
        reader.read("fixture")


def test_symlink_in_authorized_chain_fails_before_content_read(reader: D1Reader, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Path, "is_symlink", lambda self: self.name == "allowed.json")
    monkeypatch.setattr(Path, "read_bytes", lambda self: (_ for _ in ()).throw(AssertionError("read forbidden")))
    with pytest.raises(PermissionError, match="D1_LINK_NOT_ALLOWED"):
        reader.read("fixture")


def test_unlisted_key_cannot_register_its_own_file(reader: D1Reader) -> None:
    with pytest.raises(PermissionError):
        reader.read("D2")


def test_junction_is_rejected_before_read(reader: D1Reader, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Path, "is_junction", lambda self: self.name == "allowed.json")
    monkeypatch.setattr(Path, "read_bytes", lambda self: (_ for _ in ()).throw(AssertionError("read forbidden")))
    with pytest.raises(PermissionError, match="D1_LINK_NOT_ALLOWED"):
        reader.read("fixture")
