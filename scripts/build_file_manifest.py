from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from codeguarder.stage5_paper.audit.fingerprints import (
    historical_files,
    sha256_file,
    write_sha256_manifest,
)


EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "xdg_cache",
    "xdg_config",
    "xdg_data",
    "tmp_create_test",
}


def is_candidate(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return not any(part in EXCLUDED_PARTS for part in relative.parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--historical", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.historical:
        files = historical_files(root)
        write_sha256_manifest(root, files, args.output)
    else:
        output_path = args.output.resolve()
        files = [
            path
            for path in root.rglob("*")
            if (
                path.is_file()
                and path.resolve() != output_path
                and is_candidate(path, root)
            )
        ]
        payload = [
            {
                "path": path.relative_to(root).as_posix(),
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
            for path in sorted(files, key=lambda item: item.relative_to(root).as_posix())
        ]
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    print(f"manifest_files={len(files)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
