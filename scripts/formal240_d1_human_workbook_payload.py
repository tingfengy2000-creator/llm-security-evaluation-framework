"""Create blind, label-free Human A/B workbook payloads from frozen D1 packets.

The control mapping and random salts must stay in a private, Git-external folder.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import random
import secrets
from pathlib import Path
from typing import Any


TITLE_BY_SHA_PREFIX = {
    "0852058f0026": "国务院关于职工工作时间的规定（1995文本）",
    "0c593c032e07": "全国年节及纪念日放假办法（2013文本）",
    "0d2b16c9821b": "中华人民共和国劳动合同法实施条例",
    "0e019dba4f9a": "湖北政报1988年第10期：女职工劳动保护规定",
    "1f624fc130ec": "企业职工带薪年休假实施办法",
    "245b651785b5": "全国年节及纪念日放假办法（2024文本）",
    "2e954d6a8f94": "中华人民共和国劳动争议调解仲裁法",
    "367cb4202156": "保障农民工工资支付条例",
    "57b478ff3e49": "工伤保险条例（2010修订文本）",
    "7474417d453f": "国务院关于职工工作时间的规定（1994文本）",
    "7d2a49888262": "国务院关于修改《工伤保险条例》的决定",
    "9bbc5025da6f": "社会保险经办条例",
    "9dbd0465bf87": "职工带薪年休假条例",
    "c2195f44462d": "工伤保险条例（2003文本）",
    "c9fff5198f9c": "劳务派遣暂行规定",
    "cbfe89fa5a20": "禁止使用童工规定",
    "d18934823e24": "女职工劳动保护特别规定",
    "d92bb70520bd": "工伤认定办法",
    "e1a312271a1b": "失业保险条例",
    "e45d13eacb39": "中华人民共和国社会保险法",
    "ea15938445f3": "中华人民共和国劳动合同法（2012修正）",
    "f1e97bfa64d1": "中华人民共和国劳动合同法（2012修正）",
}


def need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def lines(path: Path) -> list[dict[str, Any]]:
    return [json.loads(row) for row in path.read_text(encoding="utf-8").splitlines() if row]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt(evidence: dict[str, Any]) -> str:
    if "snapshot_text_extract" in evidence:
        whole = evidence["snapshot_text_extract"]
        if evidence["snapshot_raw_sha256"].startswith("0e019dba4f9a"):
            # A 47k-character government gazette has several unrelated laws.
            # Select the document by its own heading, identically for every row.
            begin = whole.find("中华人民共和国国务院令（第9号")
            if begin < 0:
                begin = whole.find("女职工劳动 保护规定")
            end = whole.find("中华人民共和国国务院令（第 11", begin + 1)
            if end < 0:
                end = whole.find("中华人民共和国国务院令（第11", begin + 1)
            need(begin >= 0 and end > begin, "gazette statutory section boundary")
            section = whole[begin:end]
            need("女职工" in section and len(section) < 32767,
                 "gazette section not complete or Excel limit")
            return section
        need(len(whole) < 32767, "official excerpt exceeds Excel cell limit")
        return whole
    if "bounded_official_excerpt" in evidence:
        return evidence["bounded_official_excerpt"]
    parts = [evidence.get("document_identity_excerpt", ""),
             evidence.get("bounded_fact_excerpt", "")]
    if parts[0] == parts[1]:
        return parts[0]
    return "\n【文件身份与版本】\n" + parts[0] + "\n【可核实事实摘录】\n" + parts[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--full-audit", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    need(read(args.full_audit)["status"] == "D1_PREANNOTATION_ACCEPTANCE_PASS",
         "full D1 acceptance gate")
    root = args.source_root
    packet_paths = [
        root / "paper1_formal240_d1_canary_r3r4_phase1_raw_lock_20260923" /
        "PAPER1_FORMAL_D1_CANARY_PHASE2_V4.json",
        root / "paper1_formal240_d1_remaining40_hkp1_batch1_20260926" /
        "phase2_release_run02_20260926/PAPER1_FORMAL_D1_HKP1_BATCH1_PHASE2_PACKAGE_V4.json",
        root / "paper1_core144_d1_remaining90_phase2_release_v5_20260927" /
        "PAPER1_FORMAL_D1_REMAINING90_PHASE2_PACKAGE_V5.json",
    ]
    packets = [read(path)["records"] for path in packet_paths]
    need([len(records) for records in packets] == [24, 30, 90], "packet population")
    by_id = {r["blind_review_id"]: r for records in packets for r in records}
    need(len(by_id) == 144, "packet IDs")
    current = read(root / "paper1_core144_scope_d1_phase1_closeout_20260927" /
                   "targeted4_phase1_v2/control_only_do_not_send/"
                   "PAPER1_FORMAL_D1_REMAINING90_CURRENT_CANDIDATE_ONLY_V3.json")["records"]
    need(all(by_id[r["blind_review_id"]]["candidate_text"] == r["candidate_text"]
             for r in current), "remaining90 packet text must equal Phase1-locked text")
    canary = lines(root / "paper1_formal240_d1_canary_r3r4_phase1_raw_lock_20260923" /
                   "PAPER1_FORMAL_D1_CANARY_CANDIDATES_V3.jsonl")
    batch = lines(root / "paper1_formal240_d1_remaining40_hkp1_batch1_20260926" /
                  "construction_v4/PAPER1_FORMAL_D1_HKP1_BATCH1_CANDIDATES_V4.jsonl")
    need(all(by_id[r["blind_review_id"]]["candidate_text"] == r["candidate_text"]
             for r in canary + batch), "Canary/Batch packet text parity")
    for item in by_id.values():
        need(len(item["evidence"]) in (1, 2) and
             {e["evidence_selection_id"] for e in item["evidence"]} ==
             ({"E1"} if len(item["evidence"]) == 1 else {"E1", "E2"}),
             "only frozen E1 / optional E2 slots are allowed")
        for evidence in item["evidence"]:
            need(evidence["official_url"].startswith("https://") and
                 len(evidence["snapshot_raw_sha256"]) == 64 and bool(excerpt(evidence)),
                 "Evidence URL/hash/excerpt")
    need(not args.out.exists(), "refusing to overwrite Human payload namespace")
    args.out.mkdir(parents=True)
    private_mapping: dict[str, Any] = {"status": "PRIVATE_CONTROL_ONLY_DO_NOT_DISTRIBUTE",
                       "full_audit_sha256": digest(args.full_audit),
                       "packet_sha256": [digest(path) for path in packet_paths],
                       "reviewers": {}}
    for human in ("A01", "B01"):
        salt = secrets.token_bytes(32)
        order_seed = secrets.token_bytes(32)
        original_ids = list(by_id)
        random.Random(int.from_bytes(order_seed)).shuffle(original_ids)
        prefix = f"H{human[0]}D1-"
        assignment = [
            {
                "human_blind_id": prefix + hmac.new(salt, ident.encode("ascii"),
                                                   hashlib.sha256).hexdigest()[:14].upper(),
                "source_blind_id": ident,
            }
            for ident in original_ids
        ]
        need(len({r["human_blind_id"] for r in assignment}) == 144, "human ID collision")
        phase1 = []
        phase2 = []
        for record in assignment:
            source_row = by_id[record["source_blind_id"]]
            phase1.append({"blind_id": record["human_blind_id"],
                           "candidate_text": source_row["candidate_text"]})
            evidence_cells = {}
            for evidence in source_row["evidence"]:
                slot = evidence["evidence_selection_id"]
                digest_prefix = evidence["snapshot_raw_sha256"][:12]
                title = evidence.get("title") or TITLE_BY_SHA_PREFIX.get(digest_prefix)
                need(bool(title), f"missing independently supported title: {digest_prefix}")
                evidence_cells[slot] = {
                    "title": title,
                    "excerpt": excerpt(evidence),
                    "official_url": evidence["official_url"],
                    "snapshot_ref": "冻结摘录已内嵌本行；原件 SHA256: " +
                                    evidence["snapshot_raw_sha256"],
                }
            phase2.append({"blind_id": record["human_blind_id"],
                           "candidate_text": source_row["candidate_text"],
                           "E1": evidence_cells["E1"],
                           "E2": evidence_cells.get("E2", {
                               "title": "", "excerpt": "", "official_url": "",
                               "snapshot_ref": "未提供 E2；本行仅有 E1。",
                           })})
        for stage, rows in (("PHASE1", phase1), ("PHASE2", phase2)):
            target = args.out / f"PAPER1_CORE144_D1_HUMAN_{human}_{stage}_PAYLOAD_V1.json"
            target.write_text(json.dumps({"human": human, "stage": stage,
                                          "records": rows}, ensure_ascii=False) + "\n",
                              encoding="utf-8")
        private_mapping["reviewers"][human] = {
            "salt_hex": salt.hex(), "order_seed_hex": order_seed.hex(),
            "ordered_mapping": assignment,
        }
    a = private_mapping["reviewers"]["A01"]["ordered_mapping"]
    b = private_mapping["reviewers"]["B01"]["ordered_mapping"]
    need({r["human_blind_id"] for r in a}.isdisjoint(r["human_blind_id"] for r in b),
         "A/B blind ID overlap")
    need([r["source_blind_id"] for r in a] != [r["source_blind_id"] for r in b],
         "A/B randomized order coincides")
    control = args.out / "PAPER1_CORE144_D1_HUMAN_AB_PRIVATE_MAPPING_V1.json"
    control.write_text(json.dumps(private_mapping, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")
    print(json.dumps({"payload_dir": str(args.out), "rows": 144,
                      "A_B_ID_disjoint": True, "A_B_order_different": True,
                      "mapping_sha256": digest(control),
                      "phase2_evidence_complete": True}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
