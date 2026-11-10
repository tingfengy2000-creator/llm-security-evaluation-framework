
"""Bounded AMD64 PE and Windows API-set v6 byte parsers. No loader calls."""
from __future__ import annotations

import re
import struct
from dataclasses import dataclass
from typing import NamedTuple

PE_CAP = 128 * 1024**2
COUNT_CAP = 262_144
MODULE = re.compile(r"[a-z0-9][a-z0-9_.-]{0,144}\.(?:dll|exe|drv|ocx|sys)", re.ASCII)


class StaticError(ValueError):
    """A malformed or unsupported static structure."""


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise StaticError(reason)


def unpack(data: bytes, offset: int, fmt: str) -> tuple[int, ...]:
    fmt = "<" + fmt
    require(0 <= offset <= len(data) - struct.calcsize(fmt), "FIELD_BOUNDS")
    return tuple(struct.unpack_from(fmt, data, offset))


def module_name(name: str) -> str:
    name = name.lower()
    require(bool(MODULE.fullmatch(name)), "MODULE_NAME")
    return name


class Section(NamedTuple):
    name: bytes
    rva: int
    size: int
    offset: int


@dataclass(frozen=True)
class Import:
    kind: str
    module: str
    symbols: tuple[str | int, ...]


class PE:
    def __init__(self, data: bytes) -> None:
        self.data = data
        require(len(data) <= PE_CAP and data[:2] == b"MZ", "DOS_OR_SIZE")
        (header,) = unpack(data, 60, "I")
        require(data[header:header + 4] == b"PE\0\0", "PE_SIGNATURE")
        machine, nsections, _, _, _, size, _ = unpack(data, header + 4, "HHIIIHH")
        opt = header + 24
        require(machine == 0x8664 and unpack(data, opt, "H") == (0x20B,)
                and 0 < nsections <= 96 and 112 <= size <= 4096, "AMD64_PE32_PLUS")
        self.image_base, = unpack(data, opt + 24, "Q")
        self.subsystem_version = unpack(data, opt + 48, "HH")
        self.headers, = unpack(data, opt + 60, "I")
        count, = unpack(data, opt + 108, "I")
        require(count <= (size - 112) // 8 and opt + size + 40 * nsections <= self.headers <= len(data),
                "OPTIONAL_HEADER_BOUNDS")
        self.directories = [unpack(data, opt + 112 + idx * 8, "II") for idx in range(count)]
        self.sections = []
        for pos in range(opt + size, opt + size + 40 * nsections, 40):
            _, rva, span, raw = unpack(data, pos + 8, "IIII")
            require(not span or self.headers <= raw <= len(data) - span, "SECTION_BOUNDS")
            self.sections.append(Section(data[pos:pos + 8].rstrip(b"\0"), rva, span, raw))

    def directory(self, index: int) -> tuple[int, int]:
        if index >= len(self.directories):
            return 0, 0
        rva, size = self.directories[index]
        return rva, size

    def section(self, name: bytes) -> bytes:
        matches = [s for s in self.sections if s.name == name]
        require(len(matches) == 1, "SECTION_NAME")
        s = matches[0]
        return self.data[s.offset:s.offset + s.size]

    def locate(self, rva: int, length: int) -> tuple[int, int]:
        require(rva > 0 and length >= 0, "RVA_VALUE")
        if rva < self.headers and rva + length <= self.headers:
            return rva, self.headers - rva
        matches = [s for s in self.sections if s.rva <= rva < s.rva + s.size and
                   rva + length <= s.rva + s.size]
        require(len(matches) == 1, "RVA_UNBACKED_OR_OVERLAP")
        s = matches[0]
        return s.offset + rva - s.rva, s.rva + s.size - rva

    def values(self, rva: int, fmt: str) -> tuple[int, ...]:
        offset, _ = self.locate(rva, struct.calcsize("<" + fmt))
        return unpack(self.data, offset, fmt)

    def string(self, rva: int, limit: int = 8192) -> str:
        offset, available = self.locate(rva, 1)
        end = self.data.find(b"\0", offset, offset + min(available, limit))
        require(end > offset, "PE_STRING_BOUNDS")
        return self.data[offset:end].decode("ascii")

    def thunk(self, rva: int) -> tuple[str | int, ...]:
        symbols: list[str | int] = []
        offset, available = self.locate(rva, 8)
        for step in range(min(available // 8, COUNT_CAP)):
            value, = unpack(self.data, offset + step * 8, "Q")
            if value == 0:
                return tuple(symbols)
            if value >> 63:
                require(value == 1 << 63 | (value & 0xffff), "ORDINAL_ENCODING")
                symbols.append(value & 0xffff)
            else:
                require(value <= 0xffff_fffd, "THUNK_NAME_RVA")
                symbols.append(self.string(value + 2))
        raise StaticError("THUNK_TERMINATOR_OR_BUDGET")

    def imports(self) -> list[Import]:
        records = []
        for index, width, kind in ((1, 20, "DIRECT_STATIC"), (13, 32, "DELAY_IMPORT")):
            rva, size = self.directory(index)
            if rva == size == 0:
                continue
            require(width <= size <= 64 * 1024, "IMPORT_DIRECTORY_SIZE")
            for off in range(0, size - width + 1, width):
                row = self.values(rva + off, "I" * (width // 4))
                if not any(row):
                    break
                if index == 1:
                    name, thunk = row[3], row[0] or row[4]
                else:
                    require(row[0] in {0, 1}, "DELAY_ATTRIBUTES")
                    base = 0 if row[0] == 1 else self.image_base
                    name, thunk = row[1] - base, (row[4] or row[3]) - base
                records.append(Import(kind, module_name(self.string(name)), self.thunk(thunk)))
            else:
                raise StaticError("IMPORT_TERMINATOR")
        return records

    def exports(self) -> dict[str | int, str | None]:
        rva, size = self.directory(0)
        if rva == size == 0:
            return {}
        require(size >= 40, "EXPORT_DIRECTORY_SIZE")
        self.locate(rva, size)
        _, _, _, _, _, base, nfunc, nname, functions, names, ordinals = self.values(rva, "IIHHIIIIIII")
        require(0 <= nname <= COUNT_CAP and 0 <= nfunc <= COUNT_CAP, "EXPORT_COUNT")
        result: dict[str | int, str | None] = {}
        if nfunc:
            for i, pointer in enumerate(self.values(functions, f"{nfunc}I")):
                if pointer:
                    result[base + i] = (self.string(pointer, rva + size - pointer)
                                        if rva <= pointer < rva + size else None)
        if nname:
            indices = self.values(ordinals, f"{nname}H")
            for i, pointer in zip(indices, self.values(names, f"{nname}I"), strict=True):
                name = self.string(pointer)
                require(i < nfunc and base + i in result and name not in result, "EXPORT_NAME_OR_ORDINAL")
                result[name] = result[base + i]
        return result


def is_contract(name: str) -> bool:
    return name.startswith(("api-ms-", "ext-ms-"))


def contract_key(name: str) -> str:
    return name.lower().removesuffix(".dll")


class ApiSet:
    def __init__(self, data: bytes) -> None:
        version, size, _, count, entries, _, _ = unpack(data, 0, "7I")
        require(version == 6 and 28 <= size <= len(data) and count <= 8192, "APISET_HEADER_V6")
        data = data[:size]
        self.contracts: dict[str, dict[str, str]] = {}
        self.prefixes: dict[str, str | None] = {}

        def name_at(offset: int, length: int) -> str:
            require(length <= 512 and length % 2 == 0 and 0 <= offset <= size - length, "APISET_STRING_BOUNDS")
            return data[offset:offset + length].decode("utf-16-le").lower()

        for i in range(count):
            _, name_offset, name_size, hashed, values, nvalues = unpack(data, entries + i * 24, "6I")
            name = contract_key(name_at(name_offset, name_size))
            require(is_contract(name) and name not in self.contracts and hashed <= name_size
                    and hashed % 2 == 0 and nvalues <= 64, "APISET_ENTRY")
            hosts: dict[str, str] = {}
            for j in range(nvalues):
                _, alias_offset, alias_size, host_offset, host_size = unpack(data, values + j * 20, "5I")
                alias = contract_key(name_at(alias_offset, alias_size))
                host = name_at(host_offset, host_size)
                require(alias not in hosts, "APISET_ALIAS_DUPLICATE")
                hosts[alias] = module_name(host) if host else ""
            self.contracts[name] = hosts
            prefix, sep, revision = name.rpartition("-")
            # API-set v6 indexes the namespace without the final revision component.
            if sep and revision.isdecimal() and len(prefix) * 2 == hashed:
                self.prefixes[prefix] = None if prefix in self.prefixes else name

    def entry(self, contract: str) -> str | None:
        name = contract_key(contract)
        if name in self.contracts:
            return name
        prefix, sep, revision = name.rpartition("-")
        return self.prefixes.get(prefix) if sep and revision.isascii() and revision.isdecimal() else None

    def host(self, contract: str, importer: str) -> tuple[str, str | None]:
        entry = self.entry(contract)
        hosts = self.contracts.get(entry) if entry is not None else None
        if hosts is None:
            return "UNKNOWN", None
        target = hosts.get(contract_key(importer), hosts.get(""))
        if target is None:
            return "CONTRACT_PRESENT_UNMAPPED", None
        if not target:
            return "NOT_APPLICABLE", None
        return "MAPPED_HOST", target


def forward_target(value: str) -> tuple[str, str | int]:
    module, sep, symbol = value.rpartition(".")
    require(bool(sep and module and symbol), "EXPORT_FORWARD_SYNTAX")
    if not module.lower().endswith((".dll", ".exe", ".drv", ".ocx", ".sys")):
        module += ".dll"
    if symbol.startswith("#"):
        require(symbol[1:].isascii() and symbol[1:].isdecimal(), "EXPORT_FORWARD_ORDINAL")
        return module_name(module), int(symbol[1:])
    return module_name(module), symbol
