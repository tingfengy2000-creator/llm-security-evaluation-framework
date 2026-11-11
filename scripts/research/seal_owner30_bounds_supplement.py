"""Seal the Owner30 V2 supplement without rewriting the V1 interval."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "docs/paper1/dual_machine/repro5090/owner30_eval"
PRIOR_REPORT = "bf622f8bb95b6ccefb77b0d8cf6c63bedfde294c9311bd8a4e982e1fd0232e32"
PRIOR_MANIFEST = "0d2fbe7308218a7aa78962859a4800c4f438b1fa8f733b0f7f78a24cdb7f4b25"
SCORE_REPORT = "3c05598a6ec65a6f224549232703e03e1ec8fdcac52621698b8acd6aee420715"
CUSTODY = "c4244e86fb2ecf1177cc3d2bb39b8791e1b789713fc3522bbfaa46b35b055595"
AUTHORITY = "W1-OD-20261111-PAPER1-OWNER30-ONE-DAY-AUTO-RAG-EVAL"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, code: str) -> None:
    if not condition:
        raise SystemExit(code)


def dumps(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def main() -> None:
    report_path = OUT / "OWNER30_FAST_TARGET_BOUNDS_SUPPLEMENT_V2.md"
    manifest_path = OUT / "OWNER30_FAST_TARGET_BOUNDS_SUPPLEMENT_V2_MANIFEST.json"
    prior_report = (OUT / "OWNER30_FAST_TARGET_BOUNDS_REPORT.md").read_bytes()
    prior_manifest = (OUT / "OWNER30_FAST_TARGET_BOUNDS_MANIFEST.json").read_bytes()
    old_score = (REPO / "docs/paper1/dual_machine/repro5090/owner28_eval/OWNER28_EVAL_INDEPENDENT_SCORE_REPORT.md").read_bytes()
    custody = Path(r"D:\paper1\private_5090\owner28_eval\EVAL_LABEL_CUSTODY.json").read_bytes()
    require(sha(prior_report) == PRIOR_REPORT, "PRIOR_REPORT")
    require(sha(prior_manifest) == PRIOR_MANIFEST, "PRIOR_MANIFEST")
    require(sha(old_score) == SCORE_REPORT, "OLD_SCORE")
    require(sha(custody) == CUSTODY, "CUSTODY")
    require(not manifest_path.exists(), "ALREADY_SEALED")
    report = report_path.read_bytes()
    text = report.decode("utf-8")
    require("[0, 6]/22" in text and "[0, 0]/22" in text, "INTERVAL_MISSING")
    require("SIX_VALUE_HANDOFF_NOT_FOUND" in text, "HANDOFF_STATUS")
    for token in ("四个子女", "四十四小时", "三十六小时", "二十年", "attack_atom", "gold_answer", "keep_ranks"):
        require(token not in text, "LEAK")
    for key in ("POP12", "POP23", "WORK", "PATENT"):
        require(re.search(rf"(?<![A-Za-z0-9_]){key}(?![A-Za-z0-9_])", text) is None, "FACT_KEY")
    manifest = {
        "schema": "OWNER30_FAST_TARGET_BOUNDS_SUPPLEMENT_V2_MANIFEST",
        "status": "SUPPLEMENT_ONLY / SIX_VALUE_HANDOFF_NOT_FOUND / PRIOR_INTERVAL_PRESERVED",
        "authority": AUTHORITY,
        "human_gold": 0,
        "formal_asr": "NOT_MEASURED",
        "formal_accuracy": "NOT_MEASURED",
        "diagnostic_version": "OWNER30_FAST_TARGET_BOUNDS_SUPPLEMENT_V2",
        "prior_report_sha256": PRIOR_REPORT,
        "prior_manifest_sha256": PRIOR_MANIFEST,
        "prior_interval": {"NONE": [0, 0, 22], "RD_B2": [0, 0, 22], "RD_ZH": [0, 6, 22]},
        "prior_files_modified": False,
        "attack_targets_modified": False,
        "handoff_status": "NOT_FOUND",
        "handoff_paths_checked": [
            "D:\\paper1\\private_5090\\owner30_eval",
            "161166a6228970c9a4c0728efca245365e37613a public tree",
        ],
        "world_id_verified": False,
        "raw_answer_sha_verified": False,
        "transfer_sha_verified": False,
        "six_values_read": False,
        "six_target_match": "TARGET_UNKNOWN",
        "scope_claim": "UNKNOWN",
        "scope_target_match": "UNKNOWN",
        "scope_cells": 6,
        "confirmed_wrong_answers": 0,
        "unresolved_answers": 68,
        "confirmed_reasonable_refusals": 0,
        "unjudged_abstentions": 27,
        "supplement_sha256": sha(report),
        "script_sha256": sha(Path(__file__).read_bytes()),
        "owner28_score_modified": False,
        "labels_in_git": False,
        "attack_targets_in_git": False,
        "fresh_generation_calls": 0,
        "judge_calls": 0,
        "claim1": "NOT_RUN",
        "claim2": "NOT_RUN",
        "claim3": "NOT_RUN",
        "auto_continue": "NO",
    }
    manifest_path.write_bytes(dumps(manifest))
    require(sha(prior_report) == PRIOR_REPORT, "PRIOR_CHANGED")
    print(sha(report))
    print(sha(manifest_path.read_bytes()))
    print(sha(Path(__file__).read_bytes()))


if __name__ == "__main__":
    main()
