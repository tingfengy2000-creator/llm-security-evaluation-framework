from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from pathlib import Path


FROZEN_ROOTS = (
    "deliverables/stage1",
    "deliverables/stage2",
    "deliverables/stage3",
    "deliverables/stage4",
    "deliverables/stage4_ablation",
    "deliverables/stage5",
    "data/stage5",
    "src/codeguarder",
    "tests/stage5",
    "llm-security-stage1/scripts",
    "llm-security-stage1/tests",
)

EXCLUDED_PARTS = {
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "xdg_cache",
    "xdg_config",
    "xdg_data",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def experiment_fingerprint(config) -> str:
    payload = asdict(config) if is_dataclass(config) else dict(config)
    canonical = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return sha256_text(canonical)


def attempt_id(
    fingerprint: str, sample_id: str, guard_code: str, repetition: int
) -> str:
    return sha256_text(f"{fingerprint}|{sample_id}|{guard_code}|{repetition}")


def _included(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return False
    if path.suffix.lower() in {".pyc", ".pyo"}:
        return False
    return relative.as_posix() != "src/codeguarder/stage5_paper" and not relative.as_posix().startswith(
        "src/codeguarder/stage5_paper/"
    )


def historical_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for relative_root in FROZEN_ROOTS:
        target = root / relative_root
        if target.is_file() and _included(target, root):
            files.append(target)
        elif target.is_dir():
            files.extend(
                path
                for path in target.rglob("*")
                if path.is_file() and _included(path, root)
            )
    return sorted(set(files), key=lambda path: path.relative_to(root).as_posix())


def write_sha256_manifest(root: Path, paths: list[Path], output: Path) -> None:
    lines = [
        f"{sha256_file(path)}  {path.relative_to(root).as_posix()}"
        for path in sorted(paths, key=lambda item: item.relative_to(root).as_posix())
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_sha256_manifest(path: Path) -> dict[str, str]:
    manifest: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, relative = line.split("  ", 1)
        manifest[relative] = digest
    return manifest


def verify_sha256_manifest(root: Path, manifest: dict[str, str]) -> list[str]:
    differences: list[str] = []
    for relative, expected in sorted(manifest.items()):
        path = root / Path(relative)
        if not path.is_file():
            differences.append(f"missing:{relative}")
        elif sha256_file(path) != expected:
            differences.append(f"changed:{relative}")
    return differences
