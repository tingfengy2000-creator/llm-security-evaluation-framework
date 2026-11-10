
import struct
import time
from pathlib import Path

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner23a_pe import (
    PE,
    ApiSet,
    Import,
    StaticError,
    forward_target,
    is_contract,
)


def namespace(entries: dict[str, dict[str, str]]) -> bytes:
    data = bytearray(28 + len(entries) * 24)

    def put(text: str) -> tuple[int, int]:
        encoded = text.encode("utf-16-le")
        pos = len(data)
        data.extend(encoded)
        return pos, len(encoded)

    for index, (contract, aliases) in enumerate(entries.items()):
        name, size = put(contract)
        values = len(data)
        data.extend(b"\0" * (20 * len(aliases)))
        for j, (alias, host) in enumerate(aliases.items()):
            struct.pack_into("<5I", data, values + 20 * j, 0, *put(alias), *put(host))
        prefix = len(contract.rsplit("-", 1)[0]) * 2
        struct.pack_into("<6I", data, 28 + 24 * index, 0, name, size, prefix, values, len(aliases))
    struct.pack_into("<7I", data, 0, 6, len(data), 0, len(entries), 28, 0, 0)
    return bytes(data)


def test_apiset_v6_revision_alias_and_unknown() -> None:
    schema = ApiSet(namespace({
        "ext-ms-onecore-demo-l1-2-7": {"": "base.dll", "special.dll": "alt.dll", "skip": ""},
        "api-ms-demo-l1-1-0": {"selected": "base.dll"},
    }))
    assert is_contract("ext-ms-onecore-demo-l1-2-0.dll")
    assert schema.entry("ext-ms-onecore-demo-l1-2-0.dll") == "ext-ms-onecore-demo-l1-2-7"
    assert schema.host("ext-ms-onecore-demo-l1-2-0.dll", "SPECIAL.DLL") == ("MAPPED_HOST", "alt.dll")
    assert schema.host("ext-ms-onecore-demo-l1-2-9.dll", "other.dll") == ("MAPPED_HOST", "base.dll")
    assert schema.host("ext-ms-onecore-demo-l1-2-7.dll", "skip.dll") == ("NOT_APPLICABLE", None)
    assert schema.host("api-ms-demo-l1-1-0.dll", "other.dll") == ("CONTRACT_PRESENT_UNMAPPED", None)
    assert schema.host("api-ms-demo-l1-9-0.dll", "other.dll") == ("UNKNOWN", None)


def test_apiset_ambiguous_revision_is_unknown_and_bad_bounds_rejected() -> None:
    raw = namespace({"api-ms-demo-l1-1-0": {"": "a.dll"}, "api-ms-demo-l1-1-1": {"": "b.dll"}})
    schema = ApiSet(raw)
    assert schema.host("api-ms-demo-l1-1-2.dll", "foo.dll") == ("UNKNOWN", None)
    assert schema.host("api-ms-demo-l1-1-0.dll", "foo.dll") == ("MAPPED_HOST", "a.dll")
    with pytest.raises(StaticError, match="APISET_HEADER_V6"):
        ApiSet(raw[:-2])


def pe_image() -> bytearray:
    data = bytearray(0x4000)
    data[:2] = b"MZ"
    struct.pack_into("<I", data, 60, 0x80)
    data[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", data, 0x84, 0x8664, 1, 0, 0, 0, 240, 0x2000)
    opt = 0x98
    struct.pack_into("<H", data, opt, 0x20B)
    struct.pack_into("<I", data, opt + 60, 0x200)
    struct.pack_into("<I", data, opt + 108, 16)
    for index, offset, size in ((0, 0x300, 0x140), (1, 0x210, 40), (13, 0x240, 64)):
        struct.pack_into("<II", data, opt + 112 + index * 8, offset + 0xe00, size)
    section = opt + 240
    data[section:section + 5] = b".data"
    struct.pack_into("<IIII", data, section + 8, 0x3e00, 0x1000, 0x3e00, 0x200)
    struct.pack_into("<5I", data, 0x210, 0x10c0, 0, 0, 0x10a0, 0)
    struct.pack_into("<8I", data, 0x240, 1, 0x10b0, 0, 0, 0x10d8, 0, 0, 0)
    data[0x2a0:0x2a8] = b"one.dll\0"
    data[0x2b0:0x2b8] = b"two.dll\0"
    struct.pack_into("<3Q", data, 0x2c0, 0x10f0, (1 << 63) | 7, 0)
    struct.pack_into("<2Q", data, 0x2d8, (1 << 63) | 4, 0)
    data[0x2f2:0x2f8] = b"Named\0"
    struct.pack_into("<IIHHIIIIIII", data, 0x300, 0, 0, 0, 0, 0, 3, 2, 1, 0x1140, 0x1150, 0x1158)
    struct.pack_into("<2I", data, 0x340, 0x1180, 0x1300)
    struct.pack_into("<I", data, 0x350, 0x1200)
    struct.pack_into("<H", data, 0x358, 0)
    data[0x380:0x389] = b"Other.#4\0"
    data[0x400:0x401 + 3865] = b"?" * 3865 + b"\0"
    return data


def test_pe_named_and_ordinal_direct_delay_and_long_forwarded_export() -> None:
    pe = PE(bytes(pe_image()))
    assert pe.imports() == [
        Import("DIRECT_STATIC", "one.dll", ("Named", 7)),
        Import("DELAY_IMPORT", "two.dll", (4,)),
    ]
    assert pe.exports() == {3: "Other.#4", 4: None, "?" * 3865: "Other.#4"}
    assert forward_target("Other.#4") == ("other.dll", 4)
    assert forward_target("Other.dll.Symbol") == ("other.dll", "Symbol")
    with pytest.raises(StaticError, match="MODULE_NAME"):
        forward_target(r"..\Other.Symbol")


def test_pe_rejects_unmapped_thunk() -> None:
    data = pe_image()
    struct.pack_into("<Q", data, 0x2c0, 0xffff0000)
    with pytest.raises(StaticError, match="RVA_UNBACKED"):
        PE(bytes(data)).imports()


def test_forward_cycle_and_wall_frontier(tmp_path: Path) -> None:
    pytest.importorskip("winreg")
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner23a_scoped_static import Closure

    (tmp_path / "a.dll").touch()
    (tmp_path / "b.dll").touch()
    audit = Closure({}, tmp_path, ApiSet(namespace({})), {}, time.monotonic() + 10)
    audit.modules = {"a.dll": {}, "b.dll": {}}
    audit.exports = {"a.dll": {"X": "b.Y"}, "b.dll": {"Y": "a.X"}}
    assert audit.resolve("root.exe", "a.dll", "X", 0)["status"] == "FORWARD_CYCLE"
    result = audit.resolve("root.exe", "a.dll", "X", 21)
    assert result["status"] == "ANALYSIS_BUDGET_EXHAUSTED"
    assert result["frontier"] == ["root.exe", "a.dll", "X"]
