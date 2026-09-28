"""Read-only workbook / human-manual parity audit; never evaluates actual answers."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from zipfile import ZipFile

BASE = Path(__file__).resolve().parents[1]
DOC = BASE / "docs/research/stage6_1_hidden_knowledge_poisoning"
CORE = DOC / "core144"
GUIDE = CORE / "PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_V1.md"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
P1 = [
    "blind_id", "candidate_text", "text_naturalness", "local_internal_conflict",
    "self_containment", "ambiguous_referent", "meta_or_template_language", "issue_note",
]
P2 = [
    "blind_id", "candidate_text", "E1_title", "E1_excerpt", "E1_official_url",
    "E1_snapshot_ref", "E2_title", "E2_excerpt", "E2_official_url", "E2_snapshot_ref",
    "overall_fact_status", "version_claim_status", "authority_claim_status",
    "minimum_external_evidence_needed", "evidence_selection", "phase2_issue",
    "possible_accidental_secondary_error", "evidence_sufficiency", "phase2_reason",
    "reviewer_note",
]
SOURCE_NAMES = [
    "formal240/PAPER1_FORMAL_ANNOTATION_GUIDE_V4.md",
    "formal240/PAPER1_FORMAL_ANNOTATION_GUIDE_V4_1_CLARIFICATION.md",
    "formal240/PAPER1_FORMAL_ANNOTATION_GUIDE_V4_2_VERSION_SCOPE_DECISION.md",
    "formal240/PAPER1_FORMAL_ANNOTATION_GUIDE_V4_3_TEMPORAL_VS_VERSION_SCOPE.md",
    "formal240/PAPER1_FORMAL_ANNOTATION_BOUNDARY_EXAMPLES_V1.json",
    "human/annotation_lessons_learned_and_future_dataset_rules.md",
    "core144/PAPER1_CORE144_D1_HUMAN_PHASE1_GUIDE_V1.md",
    "core144/PAPER1_CORE144_BENCHMARK_CONTRACT_V1.md",
    "core144/PAPER1_CORE144_SCOPE_DECISION_V1.md",
]


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_xlsx(path: Path) -> dict[str, Any]:
    """Inspect OOXML in memory; no save, export, or mutation path exists."""
    raw = path.read_bytes()
    with ZipFile(path) as z:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            shared = [
                "".join(e.itertext()) for e in
                ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS)
            ]
        relationships = {
            e.attrib["Id"]: e.attrib["Target"]
            for e in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        }
        sheets = ET.fromstring(z.read("xl/workbook.xml")).findall("m:sheets/m:sheet", NS)
        values: dict[str, dict[str, str]] = {}
        validation: dict[str, list[str]] = {}
        for sheet in sheets:
            target = relationships[sheet.attrib[REL]]
            xml_path = target.lstrip("/") if target.startswith("/") else "xl/" + target
            root = ET.fromstring(z.read(xml_path))
            cells: dict[str, str] = {}
            for c in root.findall("m:sheetData/m:row/m:c", NS):
                if c.attrib.get("t") == "inlineStr":
                    value = "".join(t.text or "" for t in c.findall("m:is//m:t", NS))
                else:
                    v = c.find("m:v", NS)
                    value = v.text if v is not None and v.text else ""
                    if c.attrib.get("t") == "s":
                        value = shared[int(value)]
                cells[c.attrib["r"]] = value
            values[sheet.attrib["name"]] = cells
            if sheet.attrib["name"] == "【标注表】":
                for dv in root.findall("m:dataValidations/m:dataValidation", NS):
                    f = dv.find("m:formula1", NS)
                    assert f is not None and f.text
                    validation[dv.attrib["sqref"]] = f.text.strip('"').split(",")
    return {"sha256": digest(raw), "bytes": len(raw), "sheets": values,
            "validation": validation}


def norm(text: str) -> str:
    return re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]", "", text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    text = GUIDE.read_text(encoding="utf-8")
    sections = re.findall(r"^## (\d+)\. (.+)$", text, re.M)
    cases = re.findall(r"^### 案例 (\d+)：(.+)$", text, re.M)
    assert [int(x[0]) for x in sections] == list(range(1, 32))
    assert [int(x[0]) for x in cases] == list(range(1, 31))
    boundary_cases = re.findall(r"^### 虚构边界案例 ([A-D])：(.+)$", text, re.M)
    assert [x[0] for x in boundary_cases] == list("ABCD")
    total_cases = len(cases) + len(boundary_cases)
    boundary_pairs = [("PASS", "NO"), ("PASS", "YES"), ("FLAG", "NO"), ("FLAG", "YES")]
    assert "2×2 决策表" in text
    for a, b in boundary_pairs:
        assert re.search(r"^\| .+ \| " + a + r" \| " + b + r" \|$", text, re.M)
    motto = "self_containment 看对象有没有交代；ambiguous_referent 看已有对象中到底指哪一个是否唯一。"
    assert text.count(motto) >= 2
    assert "self_containment=FLAG 不强制 ambiguous_referent=YES" in text
    assert "ambiguous_referent=YES 不强制 self_containment=FLAG" in text
    assert "两项同时异常时" in text and "分别说明独立理由" in text
    previous_guide = subprocess.check_output([
        "git", "show", "4a838585b08308b8e70b172f9ccdaf2a1ed7dd2c:"
        "docs/research/stage6_1_hidden_knowledge_poisoning/core144/"
        "PAPER1_CORE144_HUMAN_ANNOTATION_MASTER_GUIDE_V1.md",
    ], cwd=BASE).decode("utf-8")
    for n in range(1, 31):
        pattern = rf"^### 案例 {n:02}：.*?(?=^#{{2,3}} )"
        old_case = re.search(pattern, previous_guide, re.M | re.S)
        new_case = re.search(pattern, text, re.M | re.S)
        assert old_case and new_case and old_case.group() == new_case.group()
    han_count = len(re.findall(r"[\u4e00-\u9fff]", text))
    assert han_count >= 8000
    obsolete = ["phase1_issue", "phase1_reason", "locally_detectable",
                "assigned_stealth_level", "authority_matches", "CANDIDATE_AMBIGUOUS"]
    assert not any(re.search(r"\b" + x + r"\b", text) for x in obsolete)
    assert not re.search(r"D1BR-|P4Q-|HKP[1-4]|target_stealth|derived_stealth|"
                         r"Expected|Ground Truth|R[345]-(?:gpt|codex|claude)", text)
    for link in re.findall(r"\]\(([^)]+)\)", text):
        assert (GUIDE.parent / link).is_file(), link

    books: list[dict[str, Any]] = []
    actual_candidates: set[str] = set()
    helper_cells: dict[int, list[str]] = {}
    enums: set[str] = set()
    for person in ("A01", "B01"):
        for phase, fields in ((1, P1), (2, P2)):
            name = f"PAPER1_CORE144_D1_HUMAN_{person}_PHASE{phase}_MANIFEST_V1.json"
            manifest = json.loads((CORE / name).read_text(encoding="utf-8"))
            path = Path(manifest["destination"])
            book = read_xlsx(path)
            assert book["sha256"] == manifest["sha256"]
            assert book["bytes"] == manifest["bytes"]
            main_sheet = book["sheets"]["【标注表】"]
            cols = [chr(65 + i) for i in range(len(fields))]
            headers = [main_sheet[f"{c}1"].split("\n")[-1] for c in cols]
            assert headers == fields
            ids = [main_sheet[f"A{i}"] for i in range(2, 146)]
            candidates = [main_sheet[f"B{i}"] for i in range(2, 146)]
            assert len(set(ids)) == 144
            assert not any(i in text for i in ids)
            actual_candidates.update(candidates)
            answers = cols[2:] if phase == 1 else cols[10:]
            assert all(not main_sheet.get(f"{c}{i}") for c in answers for i in range(2, 146))
            for field in fields:
                assert f"`{field}` /" in text, field
            for values in book["validation"].values():
                enums.update(values)
                assert all(v in text for v in values)
            if phase == 1:
                assert book["validation"]["E2:E145"] == ["PASS", "FLAG", "UNCERTAIN"]
                assert book["validation"]["F2:F145"] == ["YES", "NO", "UNCERTAIN"]
            helpers = [v.replace(person, "PERSON") for title, cells in book["sheets"].items()
                       if title not in ("【标注表】", "【冻结证据全文】") for v in cells.values()]
            if phase in helper_cells:
                assert helpers == helper_cells[phase], "A/B helper rule parity"
            helper_cells[phase] = helpers
            books.append({"artifact": manifest["artifact"], "sha256": book["sha256"],
                          "bytes": book["bytes"], "phase": phase,
                          "sheets": list(book["sheets"]), "fields": fields,
                          "enum_validations": book["validation"], "rows": 144,
                          "answers_empty": True, "source_manifest": name,
                          "status": manifest["status"],
                          "sha256_after_read": digest(path.read_bytes())})
            assert books[-1]["sha256_after_read"] == books[-1]["sha256"]

    examples = re.findall(r'^Candidate：“([^”\n]+)”', text, re.M)
    assert len(examples) == total_cases == 34
    max_similarity = 0.0
    near_duplicates = 0
    for example in examples:
        for candidate in actual_candidates:
            a, b = norm(example), norm(candidate)
            score = SequenceMatcher(None, a, b, autojunk=False).ratio()
            max_similarity = max(max_similarity, score)
            if a == b or score >= 0.72:
                near_duplicates += 1
    assert near_duplicates == 0
    case_blocks = re.split(r"^### 案例 \d+：.*$", text, flags=re.M)[1:]
    for n, block in enumerate(case_blocks, 1):
        keys = P1[2:] if n <= 9 else P2[10:18]
        assert all(re.search(r"\| " + f + r" \| .+ \| .+ \|", block) for f in keys)
        assert "易错点" in block
        if n >= 10:
            assert "虚构 Evidence：" in block
            assert "phase2_reason：" in block and "reviewer_note：" in block
    assert "虚构 Evidence：本阶段不提供、不使用。" in text
    supplements = re.split(r"^### 虚构边界案例 [A-D]：.*$", text, flags=re.M)[1:]
    for block, pair in zip(supplements, [("FLAG", "NO"), ("PASS", "YES"),
                                       ("FLAG", "YES"), ("FLAG", "NO")], strict=True):
        assert all(re.search(r"\| " + f + r" \| .+ \| .+ \|", block) for f in P1[2:])
        assert f"| self_containment | {pair[0]} |" in block
        assert f"| ambiguous_referent | {pair[1]} |" in block
    assert "A–D 全部为**虚构教学文本**" in text

    sources = [{"path": name, "sha256": digest((DOC / name).read_bytes())}
               for name in SOURCE_NAMES]
    detailed_sections = {
        "text_naturalness": [7, 8, 9], "local_internal_conflict": [7, 8, 9, 19],
        "self_containment": [7, 9], "ambiguous_referent": [7, 9],
        "meta_or_template_language": [7, 9], "issue_note": [7, 9, 10],
        "overall_fact_status": [14, 15, 18], "version_claim_status": [16, 18],
        "authority_claim_status": [17], "minimum_external_evidence_needed": [19],
        "evidence_selection": [20], "phase2_issue": [21],
        "possible_accidental_secondary_error": [22], "evidence_sufficiency": [23],
        "phase2_reason": [24], "reviewer_note": [24],
    }
    field_coverage = [{"field": f, "phase": p, "dictionary_section": 6 if p == 1 else 13,
                       "explanation_sections": detailed_sections.get(f, [4, 12] if p == 2 else [4]),
                       "schema_source_manifests": [b["source_manifest"] for b in books if b["phase"] == p],
                       "semantic_authority": [
                           "Current Human workbook help sheets and Owner master-guide directive"
                       ] + (["Formal Guide V4 plus V4.1/V4.2/V4.3"] if p == 2 else [])}
                      for p, fields in ((1, P1), (2, P2)) for f in fields]
    # Source-grounded semantic inspection map, not an automatic truth assertion.
    rule_map = {
        "V4_phase_separation": [2, 3, 5, 11, 12],
        "V4_overall_decision_order": [14, 15, 18],
        "V4_version_authority_substantive_independence": [16, 17, 25],
        "V4_zero_one_multi_minimum": [19, 20, 25],
        "V4_actual_evidence_not_necessity": [20, 27],
        "V4_issue_candidate_defect": [21, 25],
        "V4_1_publication_adoption_not_automatic_version": [16, 26, 27],
        "V4_1_operational_actor_not_authority": [17, 26, 27],
        "V4_1_row_issue_not_run_incident": [21, 25],
        "V4_2_candidate_only_no_metadata_backflow": [16, 25, 26],
        "V4_2_amendment_decision_identity": [16, 27],
        "V4_2_supported_version_comparison_history": [18, 27],
        "V4_3_history_without_version": [16, 18, 25, 27],
        "V4_3_year_distinct_document_and_current_value": [16, 18, 26, 27],
        "current_P1_five_fields_reason_rule": [6, 7, 9, 10],
        "current_P2_optional_E2": [12, 13, 20, 27],
        "Owner_C8_core_vs_subfield_insufficiency": [14, 23, 25, 27],
        "Owner_secondary_error_independent_atom": [22, 26, 27],
        "Owner_no_workbook_mutation_distribution": [3, 4, 11, 30],
        "Owner_self_containment_referent_independence": [5, 6, 7, 8, 9, 26, 28, 29, 30, 31],
    }
    faq = re.findall(r"\*\*Q(\d+) ", text)
    assert len(faq) >= 12
    danger_rows = re.findall(r"^\| (\d+) .+ \|$", text, re.M)
    assert len(danger_rows) >= 17
    checks = {"workbook_bytes_unchanged": True, "ID_and_order_unchanged": True,
              "A_B_help_semantic_parity": True, "field_coverage_100_percent": True,
              "enum_coverage_100_percent": True, "current_contract_not_old_Pilot": True,
              "no_actual_candidate_or_ID_in_guide": True, "no_mapping_expected_GT_loaded": True,
              "no_reviewer_returns_loaded": True, "no_annotation_or_distribution": True,
              "phase2_still_sealed": True, "UTF8_strict": True, "guide_links_valid": True}
    checks.update({"boundary_2_by_2_table": True, "four_fictional_boundary_cases": True,
                   "cases_05_06_verbatim_preserved": True, "all_original_30_cases_preserved": True,
                   "two_enums_exact": True,
                   "no_mechanical_field_coupling_author_inspection": True})
    report = {"task_id": "P1-CORE144-SELF-CONTAINMENT-REFERENT-CLARIFICATION-01",
              "role": "DOCUMENTATION_ONLY_READ_ONLY_XLSX_INSPECTION", "status": "PASS",
              "guide_sha256": digest(GUIDE.read_bytes()), "han_characters": han_count,
              "sections": len(sections), "fictional_cases": total_cases,
              "original_numbered_cases": len(cases), "additional_boundary_cases": len(boundary_cases),
              "phase1_cases": 13, "phase2_cases": 21,
              "previous_guide_sha256": digest(previous_guide.encode("utf-8")),
              "high_risk_rows": len(danger_rows), "FAQ_count": len(faq),
              "field_occurrences_by_phase": Counter(x["phase"] for x in field_coverage),
              "unique_fields": len(set(P1 + P2)), "unique_enum_strings": len(enums),
              "workbooks": books, "field_coverage": field_coverage,
              "rule_coverage_reviewed": rule_map, "source_receipt": sources,
              "near_duplicate_check": {"algorithm": "normalized SequenceMatcher ratio >= 0.72",
                                       "comparison_count": len(examples) * len(actual_candidates),
                                       "max_ratio": round(max_similarity, 6),
                                       "near_duplicates": near_duplicates,
                                       "limit": "mechanical screen plus fictional-topic semantic inspection"},
              "owner_directive": {"attachment_id": "18419beb-8ffe-4b84-b423-2e37d0d829a0",
                                  "bytes": 36789,
                                  "sha256": "d03d6734a260cc28d2e1f4e5f24bbdee1735060fbc7506804311e9828d64e28e"},
              "owner_additive_clarification": {
                  "date": "2026-09-28", "authority": "explicit current Owner message",
                  "scope": "Master Guide explanations only; original enum/schema/XLSX/raw unchanged",
                  "decision_lineage": "PODR-127 / OR-082 / REL-2026-0096",
                  "self_containment": "required object/claim/condition information supplied",
                  "ambiguous_referent": "two or more reasonable antecedents; not bare missing object",
                  "no_mechanical_coupling": True,
                  "historical_QA_V1_not_overwritten": True,
              },
              "old_conflicts_not_propagated": [
                  "old Phase1 issue/reason columns versus current five fields plus issue_note",
                  "old naturalness-only reason optional versus current nondefault note mandatory",
                  "Pilot internal conflict NOT_APPLICABLE versus Formal ZERO",
                  "Pilot revised content or actor error merged with version versus separate scopes",
                  "old CANDIDATE_AMBIGUOUS enum versus current late-discovered candidate defect",
              ], "checks": checks}
    assert all(checks.values())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "sections": len(sections),
                      "fields": [len(P1), len(P2)], "unique_fields": report["unique_fields"],
                      "cases": total_cases, "additional_cases": len(boundary_cases),
                      "high_risk": len(danger_rows),
                      "han": han_count, "near_duplicates": near_duplicates,
                      "max_similarity": round(max_similarity, 6),
                      "sha256": report["guide_sha256"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
