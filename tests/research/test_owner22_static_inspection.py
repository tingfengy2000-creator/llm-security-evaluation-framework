from __future__ import annotations

import io
import struct
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner22_acquisition import endpoint
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner22_static_inspection import GGUF, validated_zip


@pytest.mark.parametrize("name", ["../x.exe", "C:/bad", "dir/CON.txt", "dir/trail. ", "dir\\script"])
def test_windows_paths_rejected(name: str) -> None:
    data = io.BytesIO()
    with ZipFile(data, "w") as bundle:
        node = ZipInfo(name)
        node.filename = name  # preserve a hostile central-directory spelling in the fixture
        bundle.writestr(node, b"test")
    with ZipFile(data) as bundle, pytest.raises(ValueError, match="ZIP_PATH"):
        validated_zip(bundle)


def test_case_and_reparse_rejected() -> None:
    data = io.BytesIO()
    with ZipFile(data, "w") as bundle:
        bundle.writestr("dir/A.txt", b"1")
        bundle.writestr("DIR/B.txt", b"2")
    with ZipFile(data) as bundle, pytest.raises(ValueError, match="ZIP_CASE_COLLISION"):
        validated_zip(bundle)
    data = io.BytesIO()
    node = ZipInfo("a.dll")
    node.create_system = 0
    node.external_attr = 0x400
    with ZipFile(data, "w") as bundle:
        bundle.writestr(node, b"x")
    with ZipFile(data) as bundle, pytest.raises(ValueError, match="ZIP_LINK_OR_SPECIAL_FILE"):
        validated_zip(bundle)


def test_zip_bomb_guard() -> None:
    data = io.BytesIO()
    with ZipFile(data, "w", ZIP_DEFLATED) as bundle:
        bundle.writestr("fake.bin", b"\x00" * 1_000_000)
    with ZipFile(data) as bundle, pytest.raises(ValueError, match="ZIP_COMPRESSION_GATE"):
        validated_zip(bundle)


def test_no_host_suffix_matching_or_http_downgrade() -> None:
    allowed = ("us.aws.cdn.hf.co",)
    assert endpoint("https://us.aws.cdn.hf.co/item", allowed) == allowed[0]
    for url in ("http://us.aws.cdn.hf.co/item", "https://us.aws.cdn.hf.co.example/item",
                "https://x@us.aws.cdn.hf.co/item", "https://us.aws.cdn.hf.co:444/item"):
        with pytest.raises(ValueError, match="UNAPPROVED_REDIRECT"):
            endpoint(url, allowed)


def test_gguf_bounded_embedded_strings() -> None:
    meta = GGUF(io.BytesIO(struct.pack("<IQQ", 8, 1, 3) + b"abc"))
    array = meta.value(9)
    assert (array["element_type"], array["count"]) == (8, 1)
    with pytest.raises(ValueError, match="GGUF_ARRAY_BUDGET"):
        GGUF(io.BytesIO(struct.pack("<IQ", 8, 1_000_001))).value(9)
