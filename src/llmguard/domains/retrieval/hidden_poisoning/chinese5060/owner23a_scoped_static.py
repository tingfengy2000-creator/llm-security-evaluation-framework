
"""Owner23A fixed-input static audit. No network, DLL loading, or child process."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import time
import winreg
from collections import Counter, deque
from pathlib import Path
from typing import Any
from zipfile import ZipFile

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[5]))

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner22_acquisition import (  # noqa: E402
    ASSETS, ROOT, RUNTIME, safe, sha_file,
)
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner22_static_inspection import (  # noqa: E402
    deny_execution_and_network, member_info, validated_zip,
)
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner23a_pe import (  # noqa: E402
    PE, PE_CAP, ApiSet, Import, StaticError, forward_target, is_contract, module_name, require,
)

RUN = ROOT.parent / "owner23a-static-20261110-01"
SYSTEM = Path(r"C:\Windows\System32")
CLI = "llama-cli.exe"
ENTITY_CAP = 2048
DEPTH_CAP = 20
WALL_CAP = 120
DISK_RESERVE = 10 * 1024**3
OWNER22_ARCHIVE = "faa281e7e4a14f2bc11a292b6e42e94f42421c7a4152ec55f4212ad01a708247"
OWNER22_MANIFEST = "e333ee648ecb655a3e4ea5b5a9ff93bddd5442f4ab6cc554f2444fd48aaa7ea0"
OWNER21_ARCHIVE = "7895f7ef2c28e6b7411112bf71140b17cd6b1160b614fc6662b4b132ebf4a816"
OWNER21 = Path(r"D:\llmProject\.worktrees\paper1-chinese-defense-5060\experiments\paper1_chinese5060"
               r"\W1-5060-OWNER21-QWEN-GGUF-ADMISSION-20261110-01\READONLY_METADATA_PRIVATE.zip")
NOTICE_PINS = {
    "runtime_license.json": "94f29bbed6a22c35b992c5c6ebf0e7c92f13b836b90f36f461c9cf2f0f1d010d",
    "boringssl_license.json": "827c8d8fc207c2392794eef9e00fe246f9f61fdcc132556c275be3dd8c3cd97f",
    "llvm_openmp_license.json": "fdad1758a9e1f9d5a81e18879b3406772115edc92c24bfa36b70c654f325e8e4",
}
ENV_PATHS = (
    "TEMP", "TMP", "HF_HOME", "HF_HUB_CACHE", "HUGGINGFACE_HUB_CACHE", "LLAMA_CACHE",
    "XDG_CACHE_HOME", "USERPROFILE", "LOCALAPPDATA", "APPDATA", "PYTHONPYCACHEPREFIX",
)
VC_MODULES = ("vcruntime140.dll", "vcruntime140_1.dll", "msvcp140.dll", "ucrtbase.dll", "msvcrt.dll")


def safe_file(path: Path, limit: int) -> os.stat_result:
    safe(path)
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and 0 < info.st_size <= limit, "FILE_IDENTITY")
    return info


def read_pe(path: Path) -> tuple[PE, dict[str, Any]]:
    # Windows-serviced System32 files can legitimately be hard links to WinSxS.
    safe(path)
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and 0 < info.st_size <= PE_CAP, "PE_FILE_IDENTITY")
    data = path.read_bytes()
    require(info.st_size == len(data), "PE_SIZE_DRIFT")
    pe = PE(data)
    return pe, {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "machine": "AMD64",
                "subsystem_version": pe.subsystem_version}


def registry() -> tuple[dict[str, str], dict[str, str]]:
    flags = winreg.KEY_READ | winreg.KEY_WOW64_64KEY
    names = {}
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                        r"SYSTEM\CurrentControlSet\Control\Session Manager\KnownDLLs", 0, flags) as key:
        for index in range(winreg.QueryInfoKey(key)[1]):
            value, filename, kind = winreg.EnumValue(key, index)
            if isinstance(filename, str) and filename.lower().endswith(".dll") and kind == winreg.REG_SZ:
                names[module_name(filename)] = value
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", 0, flags) as key:
        version = {field: str(winreg.QueryValueEx(key, field)[0])
                   for field in ("CurrentBuildNumber", "UBR", "DisplayVersion", "InstallationType")}
    return names, version


def verify_inputs(manifest: Path) -> tuple[dict[str, Path], dict[str, Any]]:
    safe_file(manifest, 1024**2)
    require(sha_file(manifest) == OWNER22_MANIFEST, "OWNER22_MANIFEST_HASH")
    pins = json.loads(manifest.read_bytes())
    receipts = []
    for asset in ASSETS:
        path = ROOT / "download" / asset.filename
        require(safe_file(path, asset.size).st_size == asset.size and sha_file(path) == asset.sha256,
                "OWNER22_ASSET_HASH_OR_SIZE")
        receipts.append({"file": asset.filename, "bytes": asset.size, "sha256": asset.sha256})
    archive = ROOT / "seals" / "OWNER22_PRIVATE_AUDIT.zip"
    safe_file(archive, 1024**2)
    require(sha_file(archive) == OWNER22_ARCHIVE, "OWNER22_ARCHIVE_HASH")
    unpacked = ROOT / "unpacked"
    safe(unpacked)
    indexed = {}
    package = {}
    with ZipFile(ROOT / "download" / RUNTIME.filename) as bundle:
        rows = validated_zip(bundle)
        require(len(rows) == len(pins["zip_members"]) == 52, "OWNER22_MEMBER_COUNT")
        require(all(not i.is_dir() and Path(i.filename).name == i.filename for i in rows),
                "OWNER22_NON_FLAT_PACKAGE")
        require({p.name for p in unpacked.iterdir()} == {i.filename for i in rows}, "UNPACKED_MEMBERSHIP_DRIFT")
        for info, prior in zip(rows, pins["zip_members"], strict=True):
            row = member_info(info)
            require(all(prior[key] == row[key] for key in row), "OWNER22_ZIP_MEMBER_IDENTITY")
            with bundle.open(info) as stream:
                h = hashlib.sha256()
                while block := stream.read(1024**2):
                    h.update(block)
                digest = h.hexdigest()
            path = unpacked / info.filename
            require(safe_file(path, info.file_size).st_size == info.file_size and
                    sha_file(path) == digest == prior["sha256"], "OWNER22_EXTRACTED_MEMBER_HASH")
            indexed[info.filename] = {**row, "sha256": digest}
            if path.suffix.lower() in {".exe", ".dll"}:
                package[module_name(path.name)] = path
    require(len(package) == 51 and CLI in package, "OWNER22_PE_INVENTORY")
    staging = ROOT / "staging"
    old_qa = Path(r"D:\llmProject\experiments\owner22-checks-20261110")
    moved_qa = ROOT / "temp" / "initial-qa"
    safe(staging)
    safe(old_qa)
    safe(moved_qa)
    require(not any(staging.iterdir()) and not old_qa.exists() and moved_qa.is_dir(), "OWNER22_QA_RESIDUE")
    return package, {"assets": receipts, "owner22_manifest_sha256": OWNER22_MANIFEST,
                     "owner22_archive_sha256": OWNER22_ARCHIVE, "members": indexed,
                     "package_pe_count": len(package), "old_qa_outside_root_present": False,
                     "migrated_qa_present": True, "staging_files": 0}


class Closure:
    def __init__(self, package: dict[str, Path], system: Path, api: ApiSet, known: dict[str, str],
                 deadline: float) -> None:
        self.package = package
        self.system = system
        self.api = api
        self.known = known
        self.deadline = deadline
        self.modules: dict[str, dict[str, Any]] = {}
        self.imports: dict[str, list[Import]] = {}
        self.exports: dict[str, dict[str | int, str | None]] = {}
        self.mappings: dict[tuple[str, str], dict[str, Any]] = {}

    def budget(self, depth: int) -> bool:
        return depth <= DEPTH_CAP and time.monotonic() < self.deadline

    def locate(self, name: str, importer: str) -> tuple[str, str | None]:
        contract = is_contract(name)
        if contract:
            status, target = self.api.host(name, importer)
            host = target
            if target and target in self.package and target not in self.known:
                status, target = "UNKNOWN", None
            if target and not (self.system / target).is_file():
                status, target = "HOST_NOT_PRESENT", None
            self.mappings[(name, importer)] = {
                "contract": name, "importer": importer, "status": status, "host": host,
                "schema_entry": self.api.entry(name),
            }
            return status, target
        if name in self.package and name not in self.known:
            if (self.system / name).is_file():
                return "PACKAGE_SYSTEM32_COLLISION", None
            return "PACKAGE", name
        if (self.system / name).is_file():
            return ("KNOWN_DLL" if name in self.known else "SYSTEM32"), name
        return "NOT_FOUND_IN_FIXED_ROOTS", None

    def load(self, name: str) -> bool:
        if name in self.modules:
            return True
        if len(self.modules) >= ENTITY_CAP:
            return False
        kind = "PACKAGE" if name in self.package and name not in self.known else "SYSTEM32"
        path = self.package[name] if kind == "PACKAGE" else self.system / name
        self.modules[name] = {"origin": kind, "known_dll": name in self.known}
        try:
            pe, info = read_pe(path)
            self.modules[name].update(info)
            self.exports[name] = pe.exports()
            if kind == "PACKAGE":
                self.imports[name] = pe.imports()
        except (ValueError, OSError) as exc:
            self.modules[name]["parse_error"] = str(exc) if isinstance(exc, StaticError) else type(exc).__name__
        return True

    def resolve(self, importer: str, name: str, symbol: str | int, depth: int) -> dict[str, Any]:
        chain: list[dict[str, Any]] = []
        seen = set()
        while self.budget(depth + len(chain)):
            key = (importer, name, symbol)
            if key in seen:
                return {"status": "FORWARD_CYCLE", "chain": chain, "frontier": key}
            seen.add(key)
            kind, target = self.locate(name, importer)
            chain.append({"importer": importer, "requested": name, "target": target, "kind": kind,
                          "symbol": symbol})
            if target is None:
                return {"status": kind, "chain": chain}
            if not self.load(target):
                break
            exports = self.exports.get(target)
            if exports is None or "parse_error" in self.modules[target]:
                return {"status": "PE_PARSE_UNKNOWN", "chain": chain}
            if symbol not in exports:
                return {"status": "EXPORT_NOT_FOUND", "chain": chain}
            forward = exports[symbol]
            if forward is None:
                return {"status": "RESOLVED", "chain": chain}
            try:
                name, symbol = forward_target(forward)
            except StaticError:
                return {"status": "FORWARD_UNSUPPORTED", "chain": chain}
            importer = target
        return {"status": "ANALYSIS_BUDGET_EXHAUSTED", "chain": chain,
                "frontier": [importer, name, symbol]}

    def run(self, root: str) -> dict[str, Any]:
        queue = deque([(root, 0)])
        visited = set()
        imports: list[dict[str, Any]] = []
        frontier = []
        while queue:
            name, depth = queue.popleft()
            if name in visited:
                continue
            if not self.budget(depth) or not self.load(name):
                frontier.extend([name, *(pending for pending, _ in queue if pending not in visited)])
                break
            visited.add(name)
            if name not in self.imports:
                frontier.append(name)
                continue
            for item in self.imports[name]:
                origin, target = self.locate(item.module, name)
                bindings: list[dict[str, Any]] = [
                    {"symbol": s, **self.resolve(name, item.module, s, depth + 1)} for s in item.symbols
                ]
                # A forwarded export can enter a package DLL as well.
                package_targets = {step["target"] for binding in bindings for step in binding["chain"]
                                   if step["target"] in self.imports}
                if origin == "PACKAGE" and target is not None:
                    package_targets.add(target)
                queue.extend((target, depth + 1) for target in sorted(package_targets - visited))
                imports.append({"importer": name, "kind": item.kind, "module": item.module,
                                "origin": origin, "target": target, "bindings": bindings})
        counts = Counter(row["status"] for item in imports for row in item["bindings"])
        all_bound = bool(imports and counts and set(counts) == {"RESOLVED"} and not frontier
                         and all(item["bindings"] for item in imports))
        return {"root": root, "scope_status": "PASS" if all_bound else "UNKNOWN",
                "package_visited": sorted(visited), "package_frontier": sorted(set(frontier)),
                "dependency_edges": imports, "binding_status_counts": dict(sorted(counts.items()))}


def notices(package: dict[str, Path], members: dict[str, Any]) -> dict[str, Any]:
    safe_file(OWNER21, 2 * 1024**2)
    require(sha_file(OWNER21) == OWNER21_ARCHIVE, "OWNER21_METADATA_ARCHIVE_HASH")
    texts = {}
    links = {}
    with ZipFile(OWNER21) as archive:
        for name, digest in NOTICE_PINS.items():
            entry = archive.getinfo(name)
            require(entry.file_size <= 32 * 1024, "NOTICE_PIN_SIZE")
            source = json.loads(archive.read(entry))
            raw = source["text"].encode()
            require(hashlib.sha256(raw).hexdigest() == digest, "NOTICE_TEXT_PIN_HASH")
            texts[name] = raw.strip()
            links[name] = source.get("url") or source.get("source")
    cli_artifacts = ("llama.exe", "llama-connect.exe", CLI, "llama-cli-impl.dll", "llama-common.dll",
                     "llama-server-impl.dll", "ggml.dll", "ggml-base.dll", "ggml-cpu-haswell.dll",
                     "libomp.dll")
    embedded = {}
    for name in cli_artifacts:
        raw = package[name].read_bytes()
        embedded[name] = [key for key, value in texts.items() if value in raw]
    llvm = members["LICENSE-LLVM-OpenMP"]["sha256"] == NOTICE_PINS["llvm_openmp_license.json"]
    return {"owner21_metadata_archive_sha256": OWNER21_ARCHIVE, "notice_text_pins": NOTICE_PINS,
            "source_links": links, "whole_trimmed_notice_bytes_present": embedded,
            "llvm_notice_matches_shipped_file": llvm, "package_license": "UNKNOWN",
            "limits": ["Component-to-binary and redistributed notice coverage not closed for whole archive",
                       "Absence of a whole plaintext notice is not proof of component absence"]}


def write(path: Path, data: Any) -> None:
    safe(path)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(data, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")


def main() -> None:
    sys.addaudithook(deny_execution_and_network)
    start = time.monotonic()
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("--owner22-manifest", required=True, type=Path)
    args.add_argument("--attempt", required=True, type=Path)
    opts = args.parse_args()
    out: Path = opts.attempt
    safe(out)
    require(out.parent == RUN and out.is_dir(), "OWNER23A_OUTPUT_ROOT")
    for key in ENV_PATHS:
        path = Path(os.environ[key])
        safe(path)
        require(path.is_relative_to(RUN) and path.is_dir(), "OFF_D_ENV_PATH")
    require(shutil.disk_usage(RUN).free >= DISK_RESERVE, "D_DISK_RESERVE")
    require(opts.owner22_manifest == RUN / "owner22-public-manifest.json", "OWNER22_MANIFEST_PATH")
    package, inputs = verify_inputs(opts.owner22_manifest)
    write(out / "verified_inputs.json", inputs)
    schema_pe, schema_file = read_pe(SYSTEM / "apisetschema.dll")
    api = ApiSet(schema_pe.section(b".apiset"))
    known, version = registry()
    closure = Closure(package, SYSTEM, api, known, start + WALL_CAP)
    cli = closure.run(CLI)
    cli_mappings = list(closure.mappings.values())
    backends = {name: closure.run(name) for name in ("ggml-cpu-haswell.dll", "ggml-cpu-x64.dll")}
    for name in VC_MODULES:
        if closure.budget(0) and (SYSTEM / name).is_file() and name not in package:
            closure.load(name)
    findings = {
        "windows": version, "schema": {"version": 6, "contracts": len(api.contracts), **schema_file},
        "known_dll_registry_candidates": known, "cli": cli, "backend_candidates": backends,
        "package_cpu_inventory": sorted(k for k in package if k.startswith("ggml-cpu-")),
        "cli_api_set": cli_mappings, "all_api_set": list(closure.mappings.values()),
        "modules": closure.modules,
        "policy": {"entity_cap": ENTITY_CAP, "depth_cap": DEPTH_CAP, "wall_seconds": WALL_CAP,
                   "file_size_cap": PE_CAP, "scope": "package imports and necessary named OS exports/forwarders"},
        "vc_compat": "UNKNOWN", "dynamic_cpu_backend": "UNKNOWN", "actual_runtime_memory": "NOT_MEASURED",
    }
    write(out / "dependencies.json", findings)
    if not closure.budget(0):
        raise StaticError("ANALYSIS_BUDGET_EXHAUSTED")
    write(out / "license.json", notices(package, inputs["members"]))
    require(sha_file(ROOT / "seals" / "OWNER22_PRIVATE_AUDIT.zip") == OWNER22_ARCHIVE,
            "OWNER22_POST_ARCHIVE_DRIFT")
    require(closure.budget(0), "ANALYSIS_BUDGET_EXHAUSTED")
    write(out / "completion.json", {
        "elapsed_seconds": round(time.monotonic() - start, 3), "network_requests": 0, "downloads": 0,
        "runtime_executions": 0, "model_loads": 0, "inference_calls": 0, "scientific_trials": 0,
        "owner22_archive_unchanged": True, "auto_continue": False,
    })


if __name__ == "__main__":
    main()
