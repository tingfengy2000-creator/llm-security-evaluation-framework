"""Evidence-bound D2 QA, sealed before any construction-control-plane read.

The authored dispositions are inspectable judgements, not a factual classifier.
This command reads only released Candidate/Evidence and reviewer QA artifacts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PRIOR = Path("experiments/core144_d2_phase2_excerpt_v3_review_20261015")
TARGET = Path("experiments/core144_d2_targeted6_phase2_raw_lock_20261015")
GUIDES = Path("docs/research/stage6_1_hidden_knowledge_poisoning/formal240")
ROOT = Path("experiments/core144_d2_owner_qa_contract_audit_20261016")
INDEX_SHA = "524e8a7b91bec0b0776f55cdfe4ad5c979f8f31a225b19b6a7e0aa812665fcf5"
PACKET_SHA = "6795b7f7b04dabef28c5aa2283af4f922594a8f93687345637e75e61fb636564"
RAW_SHA = {
    "R3_GPT": "e83c3b0d8abbd5a3e00f18e2b47a99591cdebde399259789660838daf2e711cb",
    "R4_CODEX": "3085bdc7be45a061acef348d26baf0fbb0eeb1b3b9b4a7764c35cf1f12a829bf",
}
RULE_FILES = {
    "V4": "PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md",
    "V4.1": "PAPER1_FORMAL_ANNOTATION_GUIDE_V4_1_CLARIFICATION.md",
    "V4.2": "PAPER1_FORMAL_ANNOTATION_GUIDE_V4_2_VERSION_SCOPE_DECISION.md",
    "V4.3": "PAPER1_FORMAL_ANNOTATION_GUIDE_V4_3_TEMPORAL_VS_VERSION_SCOPE.md",
}

# Literal anchors in each assigned frozen excerpt. Context is retained, not normalized.
ANCHORS = {
    "EV-07C4CA04F10B4B54": ["第七条", "第九条"],
    "EV-4015E7A4BFF3703A": ["2024年12月25日第十四届", "第三十八条", "第三条", "第六条", "第十条"],
    "EV-B6D6F1EA5B179564": ["第826号", "已经2025年12月19日"],
    "EV-D66BFDEF9683B05F": ["1985年1月21日", "2024年6月28日"],
    "EV-87A7ADF4F7197B8A": ["中华人民共和国财政部 国家档案局令第79号", "第三十一条", "第十四条"],
    "EV-D6563B48D9E9D013": ["已经2008年11月5日", "第一条", "第二条", "第二十七条"],
    "EV-1969F20A5C935FDB": ["1993年12月12日国务院批准", "第四条"],
    "EV-4E061EBBCD574EB3": ["已经2020年11月26日", "第四条\u00a0财政部门"],
    "EV-1C71490FA3F80EA9": ["于2011年6月30日通过", "第一条 在中国境内"],
    "EV-F836E16995FE4888": ["2018年8月31日第十三届", "本决定自2019年1月1日起施行"],
    "EV-E99700B223F39438": ["2024年6月28日第十四届", "十、将第四十二条改为第四十条", "本决定自2024年7月1日起施行"],
    "EV-A430F122944BFE04": ["1999年10月31日第九届", "第四十二条", "第五十二条"],
    "EV-AAC6F8F667DC7CA3": ["2018年8月31日第十三届", "第一条"],
    "EV-6B5242D655FB681E": ["2007年3月16日第十届", "第九条", "第六十条"],
    "EV-BC4C417E9CC07388": ["2007年12月6日中华人民共和国国务院令", "根据2024年12月6日"],
    "EV-6501390238325B20": ["纳税人用于公益,救济性的捐赠"],
    "EV-BE1BBB1388D3A027": ["第二条"],
    "EV-0A252ED8ED9EFAFD": ["已经2023年11月24日", "第八条", "第六十条"],
}

# One independently reasoned disposition for every historical local proposal.
# Evidence anchors below are verified at execution; historical proposed values are
# compared, not automatically adopted. Construction role is deliberately absent.
# Authored case judgements live only in the private experiment namespace.


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: Path) -> Any:
    return json.loads(path.read_text("utf-8"))


def write_new(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()
    with path.open("xb") as stream:
        stream.write(data)


def verify_index(root: Path, expected: str | None = None) -> dict[str, Any]:
    path = root / "FINAL_EVIDENCE_INDEX_V1.json"
    if expected is not None and sha(path.read_bytes()) != expected:
        raise ValueError("Historical index identity changed")
    files = read(path)["files"]
    for name, entry in files.items():
        raw = (root / name).read_bytes()
        if sha(raw) != entry["sha256"] or len(raw) != entry["bytes"]:
            raise ValueError(f"Historical artifact changed: {name}")
    return {"root": root.name, "index_sha256": sha(path.read_bytes()), "files_verified": len(files)}


def witness(doc: dict[str, Any], anchor: str, after: int = 520) -> dict[str, Any]:
    text = doc["frozen_excerpt"]
    start = text.find(anchor)
    if start < 0:
        raise ValueError(f"Missing literal evidence anchor: {doc['evidence_id']} {anchor}")
    stop = min(len(text), start + after)
    return {"evidence_id": doc["evidence_id"], "title": doc["title"],
            "official_url": doc["official_url"], "snapshot_sha256": doc["snapshot_sha256"],
            "source_text_sha256": doc["source_text_sha256"],
            "excerpt_sha256": doc["frozen_excerpt_sha256"],
            "excerpt_char_start": start, "excerpt_char_end": stop, "literal_quote": text[start:stop],
            "quote_sha256": sha(text[start:stop].encode()),
            "original_source_character_ranges": doc["source_character_ranges"],
            "quote_is_direct_frozen_excerpt": True}


def seal_semantics(output: Path) -> dict[str, Any]:
    files = {p.relative_to(output).as_posix(): {"sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}
             for p in sorted(output.rglob("*")) if p.is_file()}
    lock = {"locked_at_utc": datetime.now(timezone.utc).isoformat(), "files": files,
            "construction_control_plane_loaded": False, "semantic_records_are_QA_not_GT": True,
            "post_lock_construction_must_not_change_semantic_judgement": True}
    write_new(output / "CANDIDATE_VISIBLE_SEMANTIC_LOCK_V1.json", lock)
    for p in output.rglob("*.json"):
        p.chmod(0o444)
    return {"sha256": sha((output / "CANDIDATE_VISIBLE_SEMANTIC_LOCK_V1.json").read_bytes()),
            "files_locked": len(files), "historical37_disposition": {"ACCEPT": 37, "REJECT": 0, "OWNER_DECISION_REQUIRED": 0}}


def validate_review_inventory(judgements: dict[str, Any], proposals: list[dict[str, Any]]) -> None:
    if len(proposals) != 37 or {r["blind_review_id"] for r in proposals} != set(judgements):
        raise ValueError("Historical37 inventory changed")
    if any(not isinstance(v, (list, tuple)) or len(v) != 2 or not all(isinstance(s, str) and s for s in v)
           for v in judgements.values()):
        raise ValueError("Each authored judgement needs substantive finding and independent reason")


def run(repo: Path, output: Path) -> dict[str, Any]:
    if output.exists():
        raise ValueError("Fresh semantic output required; never overwrite a seal")
    prior = repo / PRIOR
    authored = read(repo / ROOT / "AUTHORED_SEMANTIC_REVIEW_INPUT_V1.json")
    judgements = authored["37"]
    indices = [verify_index(prior, INDEX_SHA), verify_index(repo / TARGET),
               verify_index(repo / "experiments/core144_d2_phase2_raw_lock_20261015",
                            "940796ca4632a078ceb64ece728a109da19218c96d3856a2358b82dcf08ce3cf"),
               verify_index(repo / "experiments/core144_d2_d3_phase2_prep_20261007",
                            "2e92f682cbba6261381388f3c5b62b6cd5aa63e7c073609a4fc2ee581a03a4f9")]
    packet_path = prior / "output_v2/full144_archive/PAPER1_CORE144_D2_R3_GPT_PHASE2_PACKAGE_V3.json"
    if sha(packet_path.read_bytes()) != PACKET_SHA:
        raise ValueError("Released full144 V3 packet changed")
    packet = read(packet_path)
    docs = {d["evidence_id"]: d for d in packet["evidence_documents"]}
    records = {r["blind_review_id"]: r for r in packet["records"]}
    if len(records) != 144 or len(docs) != 25:
        raise ValueError("Visible population or corpus size changed")
    source_audit = read(prior / "output_v2/OFFICIAL_SOURCE_HASH_AUDIT_V1.json")
    for entry in source_audit:
        if sha((repo / entry["raw_path"]).read_bytes()) != entry["snapshot_sha256"]:
            raise ValueError("Official snapshot changed")
        raw_text = (repo / entry["text_path"]).read_bytes()
        if sha(raw_text) != entry["source_text_sha256"]:
            raise ValueError("Official extracted text changed")
        doc = docs[entry["evidence_id"]]
        sep = "\n\n[... noncontiguous frozen excerpt boundary ...]\n\n"
        original = raw_text.decode("utf-8")
        projection = sep.join(original[a:b] for a, b in doc["source_character_ranges"])
        if projection != doc["frozen_excerpt"] or sha(projection.encode()) != doc["frozen_excerpt_sha256"]:
            raise ValueError("Excerpt no longer exact source projection")
    rules = {k: {"file": name, "sha256": sha((repo / GUIDES / name).read_bytes())}
             for k, name in RULE_FILES.items()}
    schema = read(prior / "output_v2/reviewer_release/R3_GPT/PAPER1_CORE144_D2_TARGETED6_PHASE2_IMPORT_SCHEMA_V3.json")
    old = read(prior / "output_v2/BOUNDED43_RULE_REVIEW_PROPOSALS_V1.json")
    proposals = [r for r in old if r["disposition"] == "LOCAL_RULE_REVIEW_PROPOSAL"]
    validate_review_inventory(judgements, proposals)
    audit = []
    overlay = []
    for old_row in proposals:
        ident = old_row["blind_review_id"]
        row = records[ident]
        if row != old_row["candidate"]:
            raise ValueError("Historical proposal candidate/evidence assignment changed")
        for rule in old_row["rule_refs"]:
            if sha((repo / GUIDES / rule["file"]).read_bytes()) != rule["sha256"]:
                raise ValueError("Historical cited rule changed")
        fields = old_row["proposed_fields"]
        if "evidence_selection" in fields or any(v not in schema["enums"][k] for k, v in fields.items()):
            raise ValueError("Illegal QA field/value or process overwrite")
        evidence = [dict(witness(docs[docid], anchor), slot=slot)
                    for slot, docid in row["evidence"].items() for anchor in ANCHORS[docid]]
        issue, reason = judgements[ident]
        review = {"blind_review_id": ident, "candidate": row, "before": old_row["before"],
                  "historical_proposal": fields, "candidate_visible_evidence_spans": evidence,
                  "rule_refs": old_row["rule_refs"], "independent_review_reason": reason,
                  "proposal_legal_under_frozen_contract": True, "substantive_findings": issue,
                  "construction_defect_disposition": "NOT_IN_SCOPE_BEFORE_CONTROL_PLANE",
                  "disposition": "ACCEPT", "after_QA_fields_only": fields,
                  "human_GT": False, "raw_overwritten": False, "hidden_role_used": False,
                  "authority": "Owner authorized bounded independent review; not consensus-as-truth"}
        audit.append(review)
        overlay.append({"blind_review_id": ident, "origin": "HISTORICAL37_INDEPENDENT_DISPOSITION",
                        "before": old_row["before"], "after_QA_fields_only": fields,
                        "reason": reason, "evidence_spans": evidence,
                        "rule_refs": old_row["rule_refs"], "owner_lineage": "PODR-142 / OR-096",
                        "not_GT": True, "evidence_selection_preserved": True})
    targets = {}
    for reviewer, expected in RAW_SHA.items():
        path = repo / TARGET / "output_v1/raw" / (reviewer + ".json")
        if sha(path.read_bytes()) != expected:
            raise ValueError("Targeted6 raw changed")
        targets[reviewer] = {r["blind_review_id"]: r for r in read(path)}
    six = authored["six"]
    for ident, (fields, reason) in six.items():
        row = records[ident]
        if ident not in targets["R3_GPT"] or ident not in targets["R4_CODEX"]:
            raise ValueError("Missing targeted6 identity")
        evidence = []
        for slot, docid in row["evidence"].items():
            # Some non-primary companion documents have no material witness.
            for anchor in ANCHORS.get(docid, []):
                evidence.append(dict(witness(docs[docid], anchor), slot=slot))
        overlay.append({"blind_review_id": ident, "origin": "EXPLICIT_OWNER_SIX_DECISIONS_AND_CONDITIONAL_AUTHORITY_SCOPE_CHECK",
                        "candidate": row, "before": {r: values[ident] for r, values in targets.items()},
                        "after_QA_fields_only": fields, "reason": reason, "evidence_spans": evidence,
                        "rule_refs": list(rules.values()), "owner_lineage": "PODR-142 / OR-096",
                        "hidden_role_used": False, "not_GT": True, "evidence_selection_preserved": True})
    write_new(output / "INPUT_IDENTITY_AND_EVIDENCE_PROJECTION_CHECK_V1.json",
              {"historical_indices": indices, "visible_packet_sha256": PACKET_SHA,
               "targeted6_raw_sha256": RAW_SHA, "official_snapshots": len(source_audit),
               "exact_projection_verified": True, "rules": rules,
               "construction_control_plane_loaded": False})
    write_new(output / "HISTORICAL37_INDEPENDENT_DISPOSITIONS_V1.json", audit)
    write_new(output / "OWNER_QA_FIELD_OVERLAY_V1.json", overlay)
    write_new(output / "SEMANTIC_SCOPE_AND_AUTHORITY_DECISION_V1.json",
              {"carrier_id": "CBR-3FD51BC2D98A4D", "authority_scope": "INSTITUTIONAL_ROLE_NOT_ALL_CARRIER_CONTENT",
               "frozen_authority_rule_refs": [rules["V4"], rules["V4.1"]],
               "master_guide_sha256": sha((repo / GUIDES.parent / "core144/PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_V1.md").read_bytes()),
               "authority": "PRESENT_CORRECT", "overall": "INSUFFICIENT_EVIDENCE",
               "new_rules": 0, "modified_rules": 0, "guide_changed": False,
               "37_counts": dict(Counter(x["disposition"] for x in audit)),
               "37_accepted_fields": sum(len(x["after_QA_fields_only"]) for x in audit),
               "evidence_selection_is_process_not_QA_truth": True,
               "absence_of_carrier_evidence_is_not_proof_of_falsity": True,
               "Owner_directive_source": "current direct user message, 2026-10-16; PODR-142/OR-096",
               "candidate_repair_decision_pending_control_plane": True,
               "construction_control_plane_loaded": False, "GT_created": False})
    return seal_semantics(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.repo.resolve(), args.output or args.repo / ROOT / "semantic_lock_v1"), ensure_ascii=False))
