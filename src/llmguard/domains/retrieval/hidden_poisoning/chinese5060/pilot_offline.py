"""Process-level offline and filesystem controls for the isolated CLI."""
from __future__ import annotations

import os
import shutil
import socket
import sys
import tempfile
from pathlib import Path
from typing import Any

from .pilot_admission import Stop

DISK_RESERVE = 20 * 1024**3
SDK_MODULES = frozenset({"dashscope", "openai", "requests", "httpx", "urllib3", "transformers", "tokenizers"})
CACHE_VARS = ("TEMP", "TMP", "TMPDIR", "XDG_CACHE_HOME", "HF_HOME", "HF_HUB_CACHE", "TRANSFORMERS_CACHE",
              "TORCH_HOME", "PIP_CACHE_DIR", "RUFF_CACHE_DIR", "MYPY_CACHE_DIR", "NUMBA_CACHE_DIR")


def local_de(path: Path) -> Path:
    absolute = path.absolute()
    if absolute.drive.upper() not in {"D:", "E:"} or not absolute.is_absolute():
        raise Stop("CONTROLLED_PATH_MUST_BE_LOCAL_D_OR_E")
    if absolute != absolute.resolve():
        raise Stop("CONTROLLED_PATH_REDIRECTED")
    return absolute


def require_space(path: Path) -> None:
    if shutil.disk_usage(path).free < DISK_RESERVE:
        raise Stop("DISK_20_GIB_RESERVE")


def prepare_output(path: Path, runs_root: Path) -> Path:
    root = local_de(runs_root)
    output = local_de(path)
    if output.parent != root or output.exists():
        raise Stop("OUTPUT_REQUIRES_NEW_DIRECT_CHILD_OF_RUNS_ROOT")
    require_space(Path(output.anchor))
    root.mkdir(parents=True, exist_ok=True)
    return output


def redirect_environment(output: Path) -> None:
    work = output / "local_scratch"
    work.mkdir()
    for key in CACHE_VARS:
        os.environ[key] = str(work)
    tempfile.tempdir = str(work)
    os.environ.update(PYTHONDONTWRITEBYTECODE="1", HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1",
                      HF_HUB_DISABLE_TELEMETRY="1", DO_NOT_TRACK="1")


def install_offline_barrier(output: Path, allowed_reads: set[Path]) -> None:
    if any(name.split(".")[0] in SDK_MODULES for name in sys.modules):
        raise Stop("OFFLINE_RUNTIME_PRELOADED_SDK")
    allowed_reads = {local_de(path) for path in allowed_reads}

    def output_path(raw: Any) -> bool:
        if not isinstance(raw, (str, bytes, os.PathLike)):
            return False
        path = Path(os.fsdecode(raw)).absolute()
        return path.is_relative_to(output) and path == path.resolve()

    def audit(event: str, args: tuple[Any, ...]) -> None:
        if event.startswith(("socket.", "subprocess.", "ctypes.")) or event in {
            "os.system", "os.startfile", "os.startfile/2", "os.exec", "os.spawn", "os.posix_spawn",
            "_winapi.CreateProcess",
        }:
            raise PermissionError("OFFLINE_PROCESS_EGRESS_DENIED")
        if event == "import" and args[0].split(".")[0] in SDK_MODULES:
            raise PermissionError("OFFLINE_SDK_IMPORT_DENIED")
        if event == "open":
            raw, _, flags = args
            writable = flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC)
            if not output_path(raw) and (writable or not isinstance(raw, (str, bytes, os.PathLike))
                                         or Path(os.fsdecode(raw)).absolute() not in allowed_reads):
                raise PermissionError("OFFLINE_FILE_ALLOWLIST_DENIED")
        if event == "os.mkdir" and not output_path(args[0]):
            raise PermissionError("OFFLINE_WRITE_ALLOWLIST_DENIED")
        if event in {"os.remove", "os.rmdir", "os.rename", "os.link", "os.symlink", "os.chmod",
                     "os.chown", "os.utime", "os.truncate"}:
            raise PermissionError("OFFLINE_MUTATION_DENIED")

    sys.addaudithook(audit)
    # Prove that the hook rejects the socket before any OS connection is attempted.
    try:
        with socket.socket():
            pass
    except PermissionError as exc:
        if str(exc) == "OFFLINE_PROCESS_EGRESS_DENIED":
            return
        raise
    raise Stop("OFFLINE_BARRIER_NOT_INSTALLED")
