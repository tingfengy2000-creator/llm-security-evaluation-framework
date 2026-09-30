"""Lock explicitly interpreted official-source atoms, never labels or GT.

This checks witness identity and bytes. Semantic normalization is an explicit
construction-author operation, not an automated entailment or human verdict.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized(text: str) -> str:
    return re.sub(r"[\s,，]", "", text)


def load_sources(root: Path) -> dict[str, dict[str, Any]]:
    sources: dict[str, dict[str, Any]] = {}
    for registry in sorted(root.glob("source_capture_v*/snapshot_registry.json")):
        for record in json.loads(registry.read_bytes())["records"]:
            if record["capture_status"] != "CAPTURED_IDENTITY_ANCHORS_PRESENT":
                continue
            doc = record["evidence_doc_id"]
            raw_path = registry.parent / "raw" / f"{doc}.bin"
            text_path = registry.parent / "text" / f"{doc}.txt"
            if sha(raw_path.read_bytes()) != record["raw_sha256"]:
                raise ValueError(f"Raw snapshot changed: {doc}")
            text_bytes = text_path.read_bytes()
            if sha(text_bytes) != record["text_sha256"]:
                raise ValueError(f"Extracted text changed: {doc}")
            sources[doc] = {**record, "text": text_bytes.decode("utf-8")}
    return sources


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--definitions", type=Path, required=True)
    parser.add_argument("--captures", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("An existing normalized-atom lock may not be replaced")
    definitions_bytes = args.definitions.read_bytes()
    definitions = json.loads(definitions_bytes)
    sources = load_sources(args.captures)
    atoms = []
    for atom in definitions["atoms"]:
        source = sources[atom["doc"]]
        full = normalized(source["text"])
        witnesses = []
        for anchor in atom["anchors"]:
            needle = normalized(anchor)
            start = full.find(needle)
            if start < 0:
                raise ValueError(f"Missing quoted witness: {atom['id']}: {anchor}")
            witnesses.append({"anchor": anchor, "normalized_text_offset": start,
                              "context": full[max(0, start - 120):start + len(needle) + 180]})
        atoms.append({**atom, "witnesses": witnesses,
                      "snapshot_sha256": source["raw_sha256"],
                      "text_sha256": source["text_sha256"],
                      "snapshot_locked_utc": source["locked_utc"],
                      "official_url": source["official_url"]})
    ids = [atom["id"] for atom in atoms]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate normalized-source atom identity")
    result = {"domain": definitions["domain"], "atoms": atoms,
              "definitions_sha256": sha(definitions_bytes),
              "locked_utc": datetime.now(timezone.utc).isoformat(),
              "semantic_normalization_role": "SOURCE_BOUND_CONSTRUCTION_AUTHOR",
              "semantic_normalization_is_not_automatic_entailment": True,
              "not_expected_contract": True, "not_human_gt": True,
              "candidate_count": 0}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("xb") as stream:
        stream.write((json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode())
    print(json.dumps({"source_atoms": len(atoms), "candidate_count": 0}))


if __name__ == "__main__":
    main()
