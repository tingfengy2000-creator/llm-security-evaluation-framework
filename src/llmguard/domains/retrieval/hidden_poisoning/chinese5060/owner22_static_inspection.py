"""Owner22 offline byte inspection. PE modules and GGUF tensors are never loaded."""
from __future__ import annotations

import hashlib
import json
import re
import stat
import struct
import sys
import unicodedata
from collections import deque
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile, ZipInfo

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[5]))

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner22_acquisition import (  # noqa: E402
    ASSETS,
    CAP,
    CHUNK,
    MODEL,
    ROOT,
    RUNTIME,
    ZIP_CAP,
    check_disk,
    checked_environment,
    need,
    safe,
    sha_file,
    write_json,
)

HEADER_CAP = 32 * CHUNK
PE_CAP = 128 * CHUNK
DEVICES = re.compile(r"^(?:CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|COM[0-9¹²³]|LPT[0-9¹²³])(?:\.|$)", re.I)
DLL = re.compile(r"[A-Za-z0-9._-]{1,145}\.(?:dll|drv|exe|ocx|sys)", re.I)
FORMATS = {0: "B", 1: "b", 2: "H", 3: "h", 4: "I", 5: "i", 6: "f", 7: "?", 10: "Q", 11: "q", 12: "d"}


class GGUF:
    def __init__(self, stream: BinaryIO) -> None:
        self.stream = stream

    def data(self, count: int) -> bytes:
        need(0 <= count <= HEADER_CAP - self.stream.tell(), "GGUF_METADATA_BUDGET")
        raw = self.stream.read(count)
        need(len(raw) == count, "GGUF_SHORT_HEADER")
        return raw

    def number(self, fmt: str) -> Any:
        return struct.unpack("<" + fmt, self.data(struct.calcsize("<" + fmt)))[0]

    def string(self) -> bytes:
        size = self.number("Q")
        need(size <= CHUNK, "GGUF_STRING_BUDGET")
        return self.data(size)

    def value(self, kind: int) -> Any:
        if kind == 8:
            return self.string().decode()
        if kind != 9:
            need(kind in FORMATS, "GGUF_VALUE_TYPE")
            return self.number(FORMATS[kind])
        element, count = self.number("I"), self.number("Q")
        need(count <= 1_000_000 and (element in FORMATS or element == 8), "GGUF_ARRAY_BUDGET_OR_TYPE")
        h = hashlib.sha256()
        if element == 8:
            for _ in range(count):
                raw = self.string()
                raw.decode()
                h.update(struct.pack("<Q", len(raw)))
                h.update(raw)
        else:
            h.update(self.data(count * struct.calcsize("<" + FORMATS[element])))
        return {"element_type": element, "count": count, "encoded_elements_sha256": h.hexdigest()}


def inspect_gguf(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        data = GGUF(handle)
        need(data.data(4) == b"GGUF" and data.number("I") == 3, "GGUF_VERSION")
        tensors, entries = data.number("Q"), data.number("Q")
        need(0 < tensors <= 4096 and 0 < entries <= 1024, "GGUF_HEADER_COUNTS")
        values: dict[str, Any] = {}
        for _ in range(entries):
            key = data.string().decode()
            need(key not in values and bool(re.fullmatch(r"[A-Za-z0-9_.-]{1,256}", key)), "GGUF_METADATA_KEY")
            values[key] = data.value(data.number("I"))
        directory = {}
        for _ in range(tensors):
            name = data.string().decode()
            count = data.number("I")
            need(1 <= count <= 4 and name not in directory, "GGUF_TENSOR_DIMENSION")
            dims = [data.number("Q") for _ in range(count)]
            need(all(0 < d <= 1_000_000 for d in dims), "GGUF_TENSOR_DIMENSION")
            directory[name] = {"dims": dims, "type": data.number("I"), "offset": data.number("Q")}
        align = values.get("general.alignment", 32)
        need(type(align) is int and 32 <= align <= 4096 and align & (align - 1) == 0, "GGUF_ALIGNMENT")
        start = (handle.tell() + align - 1) // align * align
        offsets = {r["offset"] for r in directory.values()}
        need(len(offsets) == len(directory) and all(
            0 <= offset < path.stat().st_size - start and offset % align == 0 for offset in offsets
        ), "GGUF_TENSOR_OFFSETS")
    need(values.get("general.architecture") == "qwen2" and values.get("general.file_type") == 15 and
         values.get("qwen2.block_count") == 28 and values.get("qwen2.embedding_length") == 1536 and
         values.get("qwen2.attention.head_count") == 12 and values.get("qwen2.attention.head_count_kv") == 2,
         "GGUF_FIXED_ARCHITECTURE")
    tokenizer = {k: v for k, v in values.items() if k.startswith("tokenizer.")}
    template = tokenizer.pop("tokenizer.chat_template", None)
    need(isinstance(template, str) and bool(template) and isinstance(tokenizer.get("tokenizer.ggml.tokens"), dict)
         and tokenizer["tokenizer.ggml.tokens"]["count"] > 0 and bool(tokenizer.get("tokenizer.ggml.model")),
         "GGUF_EMBEDDED_TOKENIZER_OR_TEMPLATE")
    return {"status": "PASS", "gguf_version": 3, "tensor_count": tensors, "metadata_count": entries,
            "metadata_keys": sorted(values), "alignment": align, "tensor_data_start": start,
            "architecture": {k: v for k, v in values.items() if k.startswith(("general.", "qwen2."))},
            "tokenizer": tokenizer, "chat_template_bytes": len(template.encode()),
            "chat_template_sha256": hashlib.sha256(template.encode()).hexdigest(), "tensor_payload_parsed": False}


def validated_zip(bundle: ZipFile) -> list[ZipInfo]:
    infos = bundle.infolist()
    need(0 < len(infos) <= 2048 and sum(x.file_size for x in infos) <= ZIP_CAP, "ZIP_MEMBER_OR_UNPACK_CAP")
    tree: dict[str, str] = {}
    seen = set()
    for member in infos:
        raw = member.filename
        parts = raw.removesuffix("/").split("/")
        need(member.orig_filename == raw and bool(raw) and "\\" not in raw and len(raw) <= 200 and
             all(part and part not in {".", ".."} and not part.endswith((" ", ".")) and not DEVICES.match(part)
                 and not any(ord(c) < 32 or c in '<>:"|?*' for c in part) for part in parts), "ZIP_PATH")
        mode = member.external_attr >> 16
        attr = member.external_attr & 0xFFFF
        need(stat.S_IFMT(mode) in {0, stat.S_IFREG, stat.S_IFDIR} and
             not attr & stat.FILE_ATTRIBUTE_REPARSE_POINT and
             (member.is_dir() or stat.S_IFMT(mode) != stat.S_IFDIR), "ZIP_LINK_OR_SPECIAL_FILE")
        need(not member.flag_bits & 1 and member.compress_type in {ZIP_DEFLATED, ZIP_STORED} and
             member.file_size <= 200 * max(1, member.compress_size) and
             (not member.is_dir() or member.file_size == 0), "ZIP_COMPRESSION_GATE")
        for index in range(len(parts)):
            name = "/".join(parts[:index + 1])
            key = unicodedata.normalize("NFC", name).casefold()
            need(key not in tree or tree[key] == name, "ZIP_CASE_COLLISION")
            tree[key] = name
        key = unicodedata.normalize("NFC", raw.removesuffix("/")).casefold()
        need(key not in seen, "ZIP_DUPLICATE_MEMBER")
        seen.add(key)
    file_keys = {unicodedata.normalize("NFC", x.filename).casefold() for x in infos if not x.is_dir()}
    need(all(not any(str(parent).casefold() in file_keys for parent in PurePosixPath(name).parents)
             for name in tree), "ZIP_FILE_PARENT_COLLISION")
    return infos


def member_info(info: ZipInfo) -> dict[str, Any]:
    return {"path": info.filename, "bytes": info.file_size, "compressed_bytes": info.compress_size,
            "crc32": f"{info.CRC:08x}", "compression_ratio": round(info.file_size / max(1, info.compress_size), 3),
            "is_dir": info.is_dir()}


def unpack(path: Path) -> list[dict[str, Any]]:
    with ZipFile(path) as bundle:
        infos = validated_zip(bundle)
        records = [member_info(info) for info in infos]
        write_json("zip_validated_listing.json", records)
        check_disk(sum(i.file_size for i in infos) + CHUNK)
        for info, row in zip(infos, records, strict=True):
            target = ROOT / "unpacked" / Path(*PurePosixPath(info.filename).parts)
            safe(target)
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            safe(target)
            h = hashlib.sha256()
            actual = 0
            with bundle.open(info) as src, target.open("xb") as out:
                while block := src.read(CHUNK):
                    actual += len(block)
                    need(actual <= info.file_size, "ZIP_MEMBER_OVERFLOW")
                    out.write(block)
                    h.update(block)
            need(actual == info.file_size, "ZIP_MEMBER_TRUNCATED")
            row["sha256"] = h.hexdigest()
        return records


def pe(path: Path) -> dict[str, Any]:
    need(path.stat().st_size <= PE_CAP, "PE_SIZE_CAP")
    raw = path.read_bytes()

    def fields(fmt: str, offset: int) -> tuple[Any, ...]:
        need(0 <= offset <= len(raw) - struct.calcsize("<" + fmt), "PE_FIELD_BOUNDS")
        return struct.unpack_from("<" + fmt, raw, offset)

    need(raw[:2] == b"MZ", "PE_DOS_SIGNATURE")
    (header,) = fields("I", 60)
    need(raw[header:header + 4] == b"PE\0\0", "PE_SIGNATURE")
    machine, sections, _, _, _, opt_size, flags = fields("HHIIIHH", header + 4)
    opt = header + 24
    need(machine == 0x8664 and fields("H", opt)[0] == 0x20B and 0 < sections <= 96
         and 112 <= opt_size <= 4096, "PE_X64_LAYOUT")
    image_base = fields("Q", opt + 24)[0]
    table = opt + opt_size
    regions = [fields("IIII", table + 40 * idx + 8) for idx in range(sections)]
    directory_count = fields("I", opt + 108)[0]
    need(directory_count <= (opt_size - 112) // 8, "PE_DIRECTORY_BOUNDS")

    def directory(index: int) -> tuple[int, int]:
        if index >= directory_count:
            return 0, 0
        a, b = fields("II", opt + 112 + 8 * index)
        return a, b

    def location(rva: int, size: int) -> int:
        matches = [ptr + rva - va for _, va, span, ptr in regions if va <= rva and rva + size <= va + span]
        need(len(matches) == 1 and 0 <= matches[0] <= len(raw) - size, "PE_RVA_BOUNDS")
        return int(matches[0])

    def dll(rva: int) -> str:
        for size in range(1, 152):
            pos = location(rva, size)
            if raw[pos + size - 1] == 0:
                name = raw[pos:pos + size - 1].decode("ascii")
                need(bool(DLL.fullmatch(name)), "PE_DLL_NAME")
                return name.lower()
        raise ValueError("PE_DLL_STRING_BUDGET")

    def imports(index: int, width: int, name_slot: int) -> list[str]:
        rva, size = directory(index)
        if not rva and not size:
            return []
        need(rva > 0 and width <= size <= 64 * 1024, "PE_IMPORT_DIRECTORY")
        names: list[str] = []
        for off in range(0, size - width + 1, width):
            row = fields("I" * (width // 4), location(rva + off, width))
            if not any(row):
                return sorted(set(names))
            name_rva = row[name_slot]
            if index == 13 and not row[0] & 1:
                name_rva -= image_base
            names.append(dll(name_rva))
        raise ValueError("PE_IMPORT_TERMINATOR")

    cert, cert_size = directory(4)
    need((cert == cert_size == 0) or 0 < cert < cert + cert_size <= len(raw), "PE_CERTIFICATE_RANGE")
    return {"machine": "AMD64", "pe": "PE32+", "is_dll": bool(flags & 0x2000),
            "linker_version": list(fields("BB", opt + 2)), "os_version": list(fields("HH", opt + 40)),
            "subsystem_version": list(fields("HH", opt + 48)), "security_directory_bytes": cert_size,
            "authenticode_verified": False, "direct_imports": imports(1, 20, 3), "delay_imports": imports(13, 32, 1)}


def inspect_pe(rows: list[dict[str, Any]]) -> dict[str, Any]:
    package = {}
    for row in rows:
        path = Path(row["path"])
        if row["is_dir"] or path.suffix.lower() not in {".exe", ".dll"}:
            continue
        key = path.name.lower()
        need(key not in package, "PE_BASENAME_COLLISION")
        package[key] = {"relative_path": row["path"], **pe(ROOT / "unpacked" / path)}
    need("llama-cli.exe" in package, "LLAMA_CLI_NOT_IN_PACKAGE")
    queue = deque(sorted({name for row in package.values() for name in row["direct_imports"] + row["delay_imports"]}))
    system = Path(r"C:\Windows\System32")
    closure: dict[str, dict[str, Any]] = {}
    while queue:
        name = queue.popleft()
        if name in closure:
            continue
        need(len(closure) < 512, "PE_CLOSURE_NODE_BUDGET")
        if name in package:
            closure[name] = {"classification": "PACKAGE", "relative_path": package[name]["relative_path"]}
        elif name.startswith(("api-ms-win-", "ext-ms-win-")):
            closure[name] = {"classification": "WINDOWS_API_SET_CONTRACT_NOT_MAPPED"}
        else:
            path = system / name
            if not path.is_file():
                closure[name] = {"classification": "NOT_FOUND_IN_PACKAGE_OR_SYSTEM32"}
                continue
            safe(path)
            info = pe(path)
            closure[name] = {"classification": "SYSTEM32", "size": path.stat().st_size,
                             "sha256": sha_file(path), **info}
            queue.extend(info["direct_imports"] + info["delay_imports"])
    return {"package": package, "static_closure": closure, "runtime_minimum_vc": "UNKNOWN",
            "dynamic_backend_coverage": "UNKNOWN_NO_EXECUTION", "resolved_api_set_hosts": "NOT_CHECKED"}


def notices(rows: list[dict[str, Any]]) -> dict[str, Any]:
    documents = []
    for row in rows:
        p = Path(row["path"])
        if row["is_dir"] or not re.search(r"licen[cs]e|notice|copyright|copying|third.party", p.name, re.I):
            continue
        need(row["bytes"] <= 2 * CHUNK, "NOTICE_SIZE_CAP")
        raw = (ROOT / "unpacked" / p).read_bytes()
        text = raw.decode("utf-8-sig", errors="replace")
        documents.append({"path": row["path"], "sha256": row["sha256"], "bytes": len(raw),
                          "mentions_openmp_or_llvm": bool(re.search(r"OpenMP|LLVM", text, re.I)),
                          "mentions_boringssl": "BoringSSL" in text,
                          "matches_pinned_llvm_notice": row["sha256"] ==
                          "fdad1758a9e1f9d5a81e18879b3406772115edc92c24bfa36b70c654f325e8e4"})
    return {"documents": documents, "entire_package_license": "UNKNOWN_PENDING_COMPONENT_NOTICE_CLOSURE"}


def deny_execution_and_network(event: str, _args: tuple[Any, ...]) -> None:
    if event.startswith("socket.") or event in {"subprocess.Popen", "os.system", "os.startfile", "ctypes.dlopen"}:
        raise PermissionError("OWNER22_STATIC_PROCESS_ONLY")


def main() -> None:
    sys.addaudithook(deny_execution_and_network)
    checked_environment()
    transfer = json.loads((ROOT / "logs/transfer_complete.json").read_bytes())
    need(transfer["body_bytes"] == CAP and transfer["asset_count"] == 2 and transfer["retries"] == 0,
         "UNSEALED_TRANSFER")
    for asset in ASSETS:
        path = ROOT / "download" / asset.filename
        need(path.stat().st_size == asset.size and sha_file(path) == asset.sha256, "STATIC_INPUT_HASH")
    result = inspect_gguf(ROOT / "download" / MODEL.filename)
    write_json("gguf_static.json", result)
    rows = unpack(ROOT / "download" / RUNTIME.filename)
    write_json("zip_members_sha256.json", rows)
    write_json("notice_static.json", notices(rows))
    write_json("pe_static.json", inspect_pe(rows))
    check_disk(CHUNK)
    write_json("static_complete.json", {"gguf": "PASS", "zip": "PASS", "pe_inventory": "COMPLETE_STATIC",
                                       "executable_runs": 0, "model_loads": 0, "inference": 0})


if __name__ == "__main__":
    main()
