"""Fail-closed audit of D2/D3 candidate-only Phase1 megawave packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


PHASE1_KEYS = [
    "blind_review_id", "text_naturalness", "local_internal_conflict", "self_containment",
    "ambiguous_referent", "meta_or_template_language", "issue_note",
]
PHASE1_ENUMS = {
    "text_naturalness": ["NATURAL", "MINOR_ISSUE", "UNNATURAL"],
    "local_internal_conflict": ["YES", "NO", "UNCERTAIN"],
    "self_containment": ["PASS", "FLAG", "UNCERTAIN"],
    "ambiguous_referent": ["YES", "NO", "UNCERTAIN"],
    "meta_or_template_language": ["YES", "NO", "UNCERTAIN"],
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_bytes())


def inspect(root: Path) -> dict[str, Any]:
    results: dict[str, Any] = {}
    failures: list[dict[str, Any]] = []
    for domain in ("D2", "D3"):
        release = root / domain.lower() / "domain_release_v1"
        acceptance = load(release / "domain_acceptance_matrix.json")
        manifest = load(release / "reviewer" / "package_manifest.json")
        schema_path = release / "reviewer" / f"PAPER1_CORE144_{domain}_PHASE1_IMPORT_SCHEMA_V1.json"
        schema = load(schema_path)
        corpus_path = release / "candidate_corpus_v1.jsonl"
        corpus = [json.loads(line) for line in corpus_path.read_text(encoding="utf-8").splitlines()]
        by_id = {row["blind_review_id"]: row for row in corpus}
        packets = {}
        for package in manifest["packages"]:
            packet_path = Path(package["package"])
            prompt_path = Path(package["prompt"])
            # The manifest stores repository-relative paths; do not accept a
            # path that escapes or points outside this exact release folder.
            if (packet_path.resolve().parent != (release / "reviewer").resolve()
                    or prompt_path.resolve().parent != (release / "reviewer").resolve()):
                failures.append({"domain": domain, "code": "REVIEWER_FILE_OUTSIDE_RELEASE"})
                continue
            packet = load(packet_path)
            reviewer = package["reviewer"]
            expected_provider = {"R3_GPT": "GPT", "R4_CODEX": "DOUBAO"}.get(reviewer)
            if package.get("actual_provider") != expected_provider or package.get("records") != 144:
                failures.append({"domain": domain, "reviewer": reviewer,
                                 "code": "REVIEWER_PROVENANCE_OR_COUNT_MANIFEST"})
            packets[reviewer] = packet
            ids = [row.get("blind_review_id") for row in packet]
            if len(packet) != 144 or len(set(ids)) != 144 or set(ids) != set(by_id):
                failures.append({"domain": domain, "reviewer": reviewer,
                                 "code": "COUNT_OR_ID_SET_MISMATCH"})
            if any(set(row) != {"blind_review_id", "candidate_text"} for row in packet):
                failures.append({"domain": domain, "reviewer": reviewer,
                                 "code": "HIDDEN_FIELD_IN_PACKET"})
            if any(row.get("candidate_text") != by_id[row["blind_review_id"]]["candidate_text"]
                   for row in packet if row.get("blind_review_id") in by_id):
                failures.append({"domain": domain, "reviewer": reviewer,
                                 "code": "CANDIDATE_TEXT_MISMATCH"})
            groups = [by_id[row["blind_review_id"]]["group_id"] for row in packet
                      if row.get("blind_review_id") in by_id]
            if any(groups[i] == groups[i + 1] for i in range(len(groups) - 1)):
                failures.append({"domain": domain, "reviewer": reviewer,
                                 "code": "TRIPLET_ADJACENCY"})
            if re.search(r"(?i)HKP[1-4]|S[1-3]-C[1-4]|EXPECTED|GROUND_TRUTH|CLEAN_CURRENT|HARD_NEGATIVE|POISON",
                         packet_path.read_text(encoding="utf-8")):
                failures.append({"domain": domain, "reviewer": reviewer,
                                 "code": "ROLE_OR_FACTOR_TEXT_LEAKAGE"})
            if sha(packet_path) != package["package_sha256"] or sha(prompt_path) != package["prompt_sha256"]:
                failures.append({"domain": domain, "reviewer": reviewer,
                                 "code": "PACKAGE_OR_PROMPT_SHA_MISMATCH"})
        if set(packets) != {"R3_GPT", "R4_CODEX"}:
            failures.append({"domain": domain, "code": "REVIEWER_SET_MISMATCH"})
        elif packets["R3_GPT"] == packets["R4_CODEX"]:
            failures.append({"domain": domain, "code": "REVIEWER_PERMUTATIONS_NOT_DISTINCT"})
        elif {r["blind_review_id"]: r["candidate_text"] for r in packets["R3_GPT"]} != {
            r["blind_review_id"]: r["candidate_text"] for r in packets["R4_CODEX"]
        }:
            failures.append({"domain": domain, "code": "REVIEWER_INFORMATION_NONPARITY"})
        if len(corpus) != 144 or len(by_id) != 144 or sha(corpus_path) != acceptance["candidate_sha256"]:
            failures.append({"domain": domain, "code": "CANDIDATE_CORPUS_SHA_OR_COUNT"})
        if not acceptance["all_internal_hard_gates_pass"] or not all(acceptance["gates"].values()):
            failures.append({"domain": domain, "code": "DOMAIN_INTERNAL_GATE_NOT_PASS"})
        if (manifest["external_execution_started"] or manifest["fallback_96_48_used"]
                or not manifest.get("information_equivalent") or not manifest.get("opaque_ids")
                or manifest.get("hidden_fields") != 0):
            failures.append({"domain": domain, "code": "EXTERNAL_OR_FALLBACK_STATE_WRONG"})
        unexpected_returns = [path.name for path in (release / "reviewer").iterdir()
                              if "RAW_RETURN" in path.name.upper() or "PHASE2" in path.name.upper()]
        if unexpected_returns:
            failures.append({"domain": domain, "code": "PREMATURE_REVIEWER_OUTPUT",
                             "files": unexpected_returns})
        if (schema.get("phase") != "PHASE1_CANDIDATE_ONLY"
                or schema.get("record_count") != 144
                or schema.get("keys") != PHASE1_KEYS
                or schema.get("enums") != PHASE1_ENUMS):
            failures.append({"domain": domain, "code": "PHASE1_SCHEMA_MISMATCH"})
        results[domain] = {"groups": acceptance["counts"]["groups"],
                           "candidates": len(corpus),
                           "candidate_sha256": sha(corpus_path),
                           "internal_gates": acceptance["gates"],
                           "reviewers": [{"reviewer": p["reviewer"],
                                          "actual_provider": p["actual_provider"],
                                          "package": p["package"], "package_sha256": p["package_sha256"],
                                          "prompt": p["prompt"], "prompt_sha256": p["prompt_sha256"]}
                                         for p in manifest["packages"]],
                           "schema": str(schema_path), "schema_sha256": sha(schema_path),
                           "external_execution_started": False}
    return {"domains": results, "failures": failures,
            "four_packages_ready": not failures,
            "fallback_96_48_used": False,
            "reviewer_outputs_created": False,
            "status": "STOP_EXTERNAL_REVIEW_REQUIRED" if not failures else "FAIL_CLOSED"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("Refusing to overwrite reviewer audit")
    result = inspect(args.root)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"ready": result["four_packages_ready"],
                      "failures": result["failures"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
