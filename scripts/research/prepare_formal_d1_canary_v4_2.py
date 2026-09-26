"""Prepare the additive D1 Canary V4.2 Owner overlay and blind re-review packet.

Only the frozen reviewer-visible Phase2 packet, the public disagreement index,
and the Owner-approved V4.2 rule file are parsed. Hidden construction or GT
artifacts are deliberately outside this program's inputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
FORMAL = ROOT / "docs/research/stage6_1_hidden_knowledge_poisoning/formal240"
PACKET_REL = Path(
    "paper1_formal240_d1_canary_r3r4_phase1_raw_lock_20260923/"
    "PAPER1_FORMAL_D1_CANARY_PHASE2_V4.json"
)
PACKET_SHA = "2daf08286581cb8d28e70ab95ea844e5cdf41e2a6916980bf41b0a90a548ac38"
OWNER_DIRECTIVE_REL = Path(
    "paper1_formal240_d1_canary_v4_2_owner_semantic_freeze_20260926/OWNER_V4_2_DIRECTIVE_RAW_V1.txt"
)
OWNER_DIRECTIVE_SHA = "e6553e08cf05567ed1ab9598b5f18c3a08dfb17e50ca8e4954e10cc6a6554f39"
COMPARISON = FORMAL / "PAPER1_FORMAL_D1_CANARY_R3_R4_PHASE2_COMPARISON_V1.json"
RULES = FORMAL / "PAPER1_FORMAL_ANNOTATION_CONSISTENCY_RULES_V4_2.json"
OVERLAY = FORMAL / "PAPER1_FORMAL_D1_CANARY_PHASE2_OWNER_SEMANTIC_ADJUDICATION_OVERLAY_V1.json"
TARGETED = FORMAL / "PAPER1_FORMAL_D1_CANARY_PHASE2_15ITEM_TARGETED_REREVIEW_PACKAGE_V1.json"
RAW_DIR_REL = Path("paper1_formal240_d1_canary_phase2_r3r4_raw_lock_20260926")
RAW_SHAS = {
    "R3_GPT_PHASE2_VALID_REEXPORT.json": "29392396f705345e6213e50d5f457cc5881316ead52d706fc8d51d52024fd4fd",
    "R4_CODEX_PHASE2_RAW.json": "a1f8f4a50739d230770f7bb56920ea367a9171f1e581283105f33c9bd37c379d",
}
AMENDMENT_ID = "D1BR-89AF72FC0DA1"
HISTORY_GRADES = {"D1BR-EB126783B95E": "八级", "D1BR-F64D9CDAF252": "七级"}
VERSION_MARKERS = (
    "修订", "修改", "修正", "废止", "替代", "施行", "生效", "失效", "现行", "历史",
    "原版", "版本", "有效", "旧版", "新版", "前身", "后继", "沿革", "曾经",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def encoded(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write_or_check(path: Path, data: bytes, check: bool) -> None:
    if check:
        assert path.read_bytes() == data, f"generated artifact drift: {path}"
    else:
        with path.open("xb") as stream:
            stream.write(data)


def bare_rule(text: str) -> None:
    assert re.search(r"《[^》]+》.*第[一二三四五六七八九十]+条", text), text
    assert not any(marker in text for marker in VERSION_MARKERS), text


def history_rule(row: dict[str, Any], grade: str) -> str:
    claim = row["candidate_text"]
    assert "对照2003年原版和2010年修订版《工伤保险条例》" in claim
    assert grade in claim and "有所提高" in claim
    e1, e2 = row["evidence"]
    assert "2003原版" in e1["title"] and "2010修订" in e2["title"]
    pattern = rf"{grade}伤残为\s*(\d+)\s*个月"
    old = re.search(pattern, e1["bounded_official_excerpt"])
    new = re.search(pattern, e2["bounded_official_excerpt"])
    assert old is not None and new is not None
    assert int(new.group(1)) > int(old.group(1))
    return f"Frozen E1 2003 {grade}={old.group(1)} months; E2 2010 {grade}={new.group(1)} months; explicit comparison supported."


def amendment_rule(row: dict[str, Any]) -> str:
    claim = row["candidate_text"]
    assert "《国务院关于修改〈工伤保险条例〉的决定》" in claim
    assert "2010年12月8日通过" in claim and "同月20日公布" in claim
    e1, e2 = row["evidence"]
    assert "关于修改《工伤保险条例》的决定" in e1["title"]
    assert "2010年12月8日国务院第136次常务会议通过" in e1["bounded_official_excerpt"]
    assert "二○一○年十二月二十日" in e1["bounded_official_excerpt"]
    assert "2010-12-20公布" in e2["bounded_official_excerpt"]
    return "Candidate explicitly names the amendment decision; frozen E1 confirms identity, adoption and publication; E2 corroborates publication."


def build(handoff_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    packet_path = handoff_root / PACKET_REL
    raw_dir = handoff_root / RAW_DIR_REL
    assert sha(handoff_root / OWNER_DIRECTIVE_REL) == OWNER_DIRECTIVE_SHA
    assert sha(packet_path) == PACKET_SHA
    for filename, expected in RAW_SHAS.items():
        assert sha(raw_dir / filename) == expected, filename
    r3_raw = read_json(raw_dir / "R3_GPT_PHASE2_VALID_REEXPORT.json")
    r4_raw = read_json(raw_dir / "R4_CODEX_PHASE2_RAW.json")
    comparison = read_json(COMPARISON)
    rules = read_json(RULES)
    assert rules["rule_set_id"] == "PAPER1_FORMAL_ANNOTATION_CONSISTENCY_RULES_V4_2"
    assert rules["source_owner_directive_sha256"] == OWNER_DIRECTIVE_SHA
    assert {item["id"] for item in rules["rules"]} == {
        "RULE-VERSION-01", "RULE-VERSION-02", "RULE-VERSION-03", "RULE-VERSION-04", "RULE-OVERALL-01"
    }
    packet = read_json(packet_path)
    assert len(packet["records"]) == 24
    assert len(r3_raw) == len(r4_raw) == 24
    packet_order = [row["blind_review_id"] for row in packet["records"]]
    assert [row["blind_review_id"] for row in r3_raw] == packet_order
    assert [row["blind_review_id"] for row in r4_raw] == packet_order
    r3_by_id = {row["blind_review_id"]: row for row in r3_raw}
    r4_by_id = {row["blind_review_id"]: row for row in r4_raw}
    by_id = {row["blind_review_id"]: row for row in packet["records"]}
    assert len(by_id) == 24
    differences = comparison["differences"]
    assert len(differences) == 15
    assert len({d["blind_review_id"] for d in differences}) == 15
    for difference in differences:
        blind_id = difference["blind_review_id"]
        field = difference["field"]
        assert r3_by_id[blind_id][field] == difference["r3"]
        assert r4_by_id[blind_id][field] == difference["r4"]
    assert set(HISTORY_GRADES) | {AMENDMENT_ID} <= {d["blind_review_id"] for d in differences}
    differences_by_id = {d["blind_review_id"]: d for d in differences}
    cases: list[dict[str, Any]] = []
    targeted_rows: list[dict[str, Any]] = []
    category_counts = {"bare_substantive": 0, "amendment_decision": 0, "historical_comparison": 0}
    for row in packet["records"]:
        blind_id = row["blind_review_id"]
        if blind_id not in differences_by_id:
            continue
        difference = differences_by_id[blind_id]
        assert set(row) == {"blind_review_id", "candidate_text", "evidence"}
        assert [e["evidence_selection_id"] for e in row["evidence"]] == ["E1", "E2"]
        if blind_id in HISTORY_GRADES:
            assert difference["field"] == "overall_fact_status"
            evidence_basis = history_rule(row, HISTORY_GRADES[blind_id])
            decision = "LEGITIMATE_VERSION_OR_HISTORY"
            rule_ids = ["RULE-OVERALL-01"]
            category = "historical_comparison"
        elif blind_id == AMENDMENT_ID:
            assert difference["field"] == "version_claim_status"
            evidence_basis = amendment_rule(row)
            decision = "PRESENT_CORRECT"
            rule_ids = ["RULE-VERSION-03"]
            category = "amendment_decision"
        else:
            assert difference["field"] == "version_claim_status"
            bare_rule(row["candidate_text"])
            evidence_basis = "Candidate names a law/article and states only a substantive rule; E1/E2 version metadata cannot create a candidate claim."
            decision = "NOT_PRESENT"
            rule_ids = ["RULE-VERSION-01", "RULE-VERSION-02"]
            category = "bare_substantive"
        category_counts[category] += 1
        cases.append({
            "blind_review_id": blind_id,
            "target_field": difference["field"],
            "original_r3_value": difference["r3"],
            "original_r4_value": difference["r4"],
            "owner_semantic_value": decision,
            "case_category": category,
            "rule_ids": rule_ids,
            "candidate_text_sha256": hashlib.sha256(row["candidate_text"].encode("utf-8")).hexdigest(),
            "frozen_evidence_snapshot_sha256": [e["snapshot_raw_sha256"] for e in row["evidence"]],
            "evidence_basis": evidence_basis,
            "decision_authority": "OWNER_GLOBAL_SEMANTIC_CLARIFICATION_MECHANICALLY_APPLIED_NOT_REVIEWER_VOTE",
        })
        targeted_rows.append({
            "blind_review_id": blind_id,
            "candidate_text": row["candidate_text"],
            "evidence": row["evidence"],
            "target_field": difference["field"],
        })
    assert category_counts == {"bare_substantive": 12, "amendment_decision": 1, "historical_comparison": 2}
    assert len(cases) == len(targeted_rows) == 15
    overlay = {
        "artifact_id": "PAPER1_FORMAL_D1_CANARY_PHASE2_OWNER_SEMANTIC_ADJUDICATION_OVERLAY_V1",
        "status": "OWNER_SEMANTIC_QA_OVERLAY_NOT_GROUND_TRUTH",
        "owner_directive_sha256": rules["source_owner_directive_sha256"],
        "source_phase2_packet_sha256": PACKET_SHA,
        "source_comparison_sha256": sha(COMPARISON),
        "original_raw_sha256": RAW_SHAS,
        "case_counts": category_counts,
        "historical_raw_modified": False,
        "candidate_or_evidence_modified": False,
        "cases": cases,
    }
    targeted = {
        "artifact_id": "PAPER1_FORMAL_D1_CANARY_PHASE2_15ITEM_TARGETED_REREVIEW_PACKAGE_V1",
        "status": "TARGETED_RULE_CONFIRMATION_NOT_FRESH_INDEPENDENT_ANNOTATION",
        "source_frozen_phase2_packet_sha256": PACKET_SHA,
        "guide_id": "PAPER1_FORMAL_ANNOTATION_GUIDE_V4_2_VERSION_SCOPE_DECISION",
        "instruction": "Review only target_field under V4.2 using candidate text and the supplied frozen E1/E2. Return target value and a short reason; report a blocking evidence defect separately if found.",
        "records": targeted_rows,
    }
    assert set(overlay["case_counts"].values()) == {12, 1, 2}
    assert all(set(row) == {"blind_review_id", "candidate_text", "evidence", "target_field"} for row in targeted_rows)
    assert not any(key in encoded(targeted).decode("utf-8").lower() for key in ("expected_v3", "ground_truth", "owner_semantic_value", "original_r3_value", "original_r4_value", "hkp", "target_s"))
    return overlay, targeted


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--handoff-root", type=Path, required=True)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    overlay, targeted = build(args.handoff_root)
    write_or_check(OVERLAY, encoded(overlay), args.check_only)
    write_or_check(TARGETED, encoded(targeted), args.check_only)
    print(f"V4.2 {'CHECK' if args.check_only else 'PREPARE'} PASS: 15 cases, 12 bare, 1 amendment, 2 historical")
    print(f"overlay_sha256={sha(OVERLAY)}")
    print(f"targeted_sha256={sha(TARGETED)}")


if __name__ == "__main__":
    main()
