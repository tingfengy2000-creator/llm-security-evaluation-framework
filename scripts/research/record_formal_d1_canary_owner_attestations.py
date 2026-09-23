"""Record the Owner's explicitly authorized, non-technical Phase1 isolation attestations."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-lock-root", type=Path, required=True)
    args = parser.parse_args()
    root: Path = args.raw_lock_root
    assert root.is_dir()
    common_basis = (
        "OWNER_ATTESTED only, via the 2026-09-23 direct Owner replies in the "
        "control-plane conversation. Owner confirmed that the two returns came "
        "from fresh independent Phase1 sessions, each receiving only the Phase1 "
        "V2 packet, import schema V2 and its own prompt; neither saw the project "
        "repository, old returns, Owner packet, labels/mapping or Phase2. Owner "
        "also confirmed neither used web or any other external search. The "
        "attachment-to-reviewer assignment was corrected: attachment 1 is "
        "R4-codex; attachment 2 is R3-gpt. Session URLs and system audit logs "
        "were not supplied; this is not machine-verified isolation."
    )
    specs = (
        (
            "R3-gpt",
            "GPT",
            "PAPER1_FORMAL_D1_CANARY_R3_GPT_PHASE1_RAW_V1.json",
            "R3_GPT_REVIEW_RUN_ATTESTATION_V1.json",
            "PAPER1_FORMAL_D1_R3_GPT_BLIND_REVIEWER_PROMPT_PHASE1_V4_1.md",
            "OWNER_ATTESTED_DISTINCT_R3_GPT_SESSION_20260923_NO_EXTERNAL_ID",
        ),
        (
            "R4-codex",
            "CODEX",
            "PAPER1_FORMAL_D1_CANARY_R4_CODEX_PHASE1_RAW_V1.json",
            "R4_CODEX_REVIEW_RUN_ATTESTATION_V1.json",
            "PAPER1_FORMAL_D1_R4_CODEX_BLIND_REVIEWER_PROMPT_PHASE1_V4_1.md",
            "OWNER_ATTESTED_DISTINCT_R4_CODEX_SESSION_20260923_NO_EXTERNAL_ID",
        ),
    )
    for reviewer, platform, raw_name, output_name, prompt, token in specs:
        raw = root / raw_name
        assert raw.is_file()
        evidence_basis = common_basis
        if reviewer == "R4-codex":
            evidence_basis += " Owner additionally confirmed a new projectless Codex task in an empty directory."
        data = {
            "reviewer_id": reviewer,
            "review_platform": platform,
            "phase": "PHASE1",
            "session_lineage_token": token,
            "fresh_session_confirmed": True,
            "repo_access_prohibited": True,
            "repo_access_occurred": False,
            "owner_packet_not_seen": True,
            "old_reviewer_returns_not_seen": True,
            "label_mapping_not_seen": True,
            "phase2_not_seen_before_phase1_lock": True,
            "external_search_not_used": True,
            "allowed_files": [
                "PAPER1_FORMAL_D1_BLIND_REVIEW_PACKAGE_PHASE1_V2.json",
                "PAPER1_FORMAL_D1_BLIND_REVIEW_IMPORT_SCHEMA_V2.json",
                prompt,
            ],
            "started_at": None,
            "phase1_raw_sha256": sha(raw),
            "prior_attestation_sha256": None,
            "attestation_status": "PASS",
            "evidence_basis": evidence_basis,
        }
        payload = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        output = root / output_name
        with output.open("xb") as stream:
            stream.write(payload)
        print(f"{reviewer}: owner-attested; attestation_sha256={sha(output)}")


if __name__ == "__main__":
    main()
