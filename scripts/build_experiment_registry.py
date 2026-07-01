from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    path = root / "experiments" / "registry.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    missing = []
    for experiment in registry["experiments"]:
        for field in ("code_entry", "deliverables"):
            value = experiment.get(field)
            if value and not (root / value).exists():
                missing.append(f"{experiment['stage_id']}:{field}:{value}")
    if missing:
        raise SystemExit("missing registry paths: " + ", ".join(missing))
    print(f"registry_entries={len(registry['experiments'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
