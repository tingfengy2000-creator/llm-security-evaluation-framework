"""Additive, per-assertion factual-atom review for the locked D1 Canary.

This is a post-blind-lock construction audit, not an annotation answer key.
It preserves the earlier V1 bounded audit and produces a separate V2 supplement.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from typing import Any


REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts/research"))

from audit_formal_d1_canary_acceptance import (  # noqa: E402
    CANARY,
    EXPECTED_HASHES,
    PHASE1,
    assert_hash,
    digest,
    read_json,
    write_json,
)


# Each entry is (candidate-visible span, status, official locator, bounded reason).
# The full primary proposition is decomposed into independently checkable atoms.
SPECS: dict[str, dict[str, tuple[tuple[str, str, str, str], ...]]] = {
    "F240-D1-HKP1-S1-C1": {
        "CLEAN_CURRENT": (
            ("满1年不满10年的职工享有5天年休假", "SUPPORTED", "EV-ANNUAL-REG#ART3", "First tenure bracket has five days."),
            ("满10年不满20年的享有10天", "SUPPORTED", "EV-ANNUAL-REG#ART3", "Second bracket has ten days."),
        ),
        "POISON": (
            ("累计工作满1年不满10年的职工享有5天年休假", "SUPPORTED", "EV-ANNUAL-REG#ART3", "Five days in the first bracket is correct."),
            ("同一档职工又享有10天", "CONTROLLED_POISON", "EV-ANNUAL-REG#ART3", "The same bracket cannot also have ten days; text-internal contradiction."),
        ),
        "HARD_NEGATIVE": (
            ("满10年不满20年的职工享有10天年休假", "SUPPORTED", "EV-ANNUAL-REG#ART3", "Second tenure bracket has ten days."),
            ("满20年的享有15天", "SUPPORTED", "EV-ANNUAL-REG#ART3", "Third bracket has fifteen days."),
        ),
    },
    "F240-D1-HKP1-S2-C1": {
        "CLEAN_CURRENT": (
            ("社会保险经办机构收到个人的社会保险登记申请后", "SUPPORTED", "EV-SOCIAL-HANDLING#ART6", "Personal initial registration and responsible agency are named."),
            ("10个工作日内办理完毕", "SUPPORTED", "EV-SOCIAL-HANDLING#ART6", "Official Article 6 has ten working days."),
        ),
        "POISON": (
            ("社会保险经办机构收到个人的社会保险登记申请后", "SUPPORTED", "EV-SOCIAL-HANDLING#ART6", "Correct personal-registration scope."),
            ("20个工作日内办理完毕", "CONTROLLED_POISON", "EV-SOCIAL-HANDLING#ART6", "Twenty replaces the official ten-working-day deadline."),
        ),
        "HARD_NEGATIVE": (
            ("社会保险经办机构收到社会保险登记变更或者注销申请后", "SUPPORTED", "EV-SOCIAL-HANDLING#ART10", "Change/cancellation is a separate procedure."),
            ("10个工作日内办理完毕", "SUPPORTED", "EV-SOCIAL-HANDLING#ART10", "Official Article 10 has ten working days."),
        ),
    },
    "F240-D1-HKP2-S1-C1": {
        "CLEAN_CURRENT": (
            ("职工请事假累计20天以上且单位按规定不扣工资", "SUPPORTED", "EV-ANNUAL-REG#ART4", "Both conditions appear together in Article 4."),
            ("不享受当年的年休假", "SUPPORTED", "EV-ANNUAL-REG#ART4", "The combined condition triggers the exclusion."),
        ),
        "POISON": (
            ("某职工请事假累计20天以上且单位按规定不扣工资", "SUPPORTED", "EV-ANNUAL-REG#ART4", "The stated condition is coherent and official."),
            ("该职工当年既享受年休假，也不享受年休假", "CONTROLLED_POISON", "EV-ANNUAL-REG#ART4", "The same employee/year is assigned mutually exclusive outcomes."),
        ),
        "HARD_NEGATIVE": (
            ("职工事假累计20天以上但单位扣工资", "SUPPORTED", "EV-ANNUAL-REG#ART4", "Candidate explicitly negates the no-deduction condition."),
            ("不能仅凭事假天数认定其不享受当年年休假", "SUPPORTED", "EV-ANNUAL-REG#ART4", "Article 4 requires both conditions; this does not assert automatic entitlement."),
        ),
    },
    "F240-D1-HKP2-S2-C1": {
        "CLEAN_CURRENT": (
            ("怀孕7个月以上", "SUPPORTED", "EV-FEMALE-2012#ART6", "Official night-work threshold is seven months."),
            ("用人单位不得安排怀孕7个月以上的女职工从事夜班劳动", "SUPPORTED", "EV-FEMALE-2012#ART6", "Prohibition and operating actor match Article 6."),
        ),
        "POISON": (
            ("怀孕6个月以上", "CONTROLLED_POISON", "EV-FEMALE-2012#ART6", "Six replaces seven in the official threshold."),
            ("用人单位不得安排", "SUPPORTED", "EV-FEMALE-2012#ART6", "The prohibition/actor is otherwise the official predicate."),
        ),
        "HARD_NEGATIVE": (
            ("孕期不能适应原劳动的女职工", "SUPPORTED", "EV-FEMALE-2012#ART6", "This is the scope of the workload-adjustment provision."),
            ("凭医疗机构证明可减轻劳动量", "SUPPORTED", "EV-FEMALE-2012#ART6", "Medical certification and reduced workload are in Article 6."),
        ),
    },
    "F240-D1-HKP3-S2-C1": {
        "CLEAN_CURRENT": (
            ("于2010年12月20日公布", "SUPPORTED", "EV-INJURY-2010-AMENDMENT#HEADER", "Publication date belongs to the amendment decision."),
            ("自2011年1月1日起施行", "SUPPORTED", "EV-INJURY-2010-AMENDMENT#HEADER", "Official effective date is 2011-01-01."),
        ),
        "POISON": (
            ("于2010年12月20日公布", "SUPPORTED", "EV-INJURY-2010-AMENDMENT#HEADER", "Publication date is correct."),
            ("自2010年12月20日起施行", "CONTROLLED_POISON", "EV-INJURY-2010-AMENDMENT#HEADER", "Effective date is wrongly collapsed onto publication date."),
        ),
        "HARD_NEGATIVE": (
            ("经国务院常务会议于2010年12月8日通过", "SUPPORTED", "EV-INJURY-2010-AMENDMENT#HEADER", "Meeting adoption date and body match the official text."),
            ("于同月20日公布", "SUPPORTED", "EV-INJURY-2010-AMENDMENT#HEADER", "Same-month reference resolves to 2010-12-20 publication."),
        ),
    },
    "F240-D1-HKP3-S3-C1": {
        "CLEAN_CURRENT": (
            ("2003年原版和2010年修订版《工伤保险条例》", "SUPPORTED", "EV-INJURY-2003+EV-INJURY-CURRENT#HEADERS", "Two official version identities are explicit."),
            ("七级伤残的一次性伤残补助金月数标准有所提高", "SUPPORTED", "EV-INJURY-2003+EV-INJURY-CURRENT#ART35_ART37", "Grade seven is 12 months in 2003 and 13 in 2010."),
        ),
        "POISON": (
            ("2003年原版和2010年修订版《工伤保险条例》", "SUPPORTED", "EV-INJURY-2003+EV-INJURY-CURRENT#HEADERS", "Version identities are correct."),
            ("七级伤残的一次性伤残补助金月数标准有所降低", "CONTROLLED_POISON", "EV-INJURY-2003+EV-INJURY-CURRENT#ART35_ART37", "Official grade-seven value rises from 12 to 13, not falls."),
        ),
        "HARD_NEGATIVE": (
            ("2003年原版和2010年修订版《工伤保险条例》", "SUPPORTED", "EV-INJURY-2003+EV-INJURY-CURRENT#HEADERS", "Version identities are correct."),
            ("八级伤残的一次性伤残补助金月数标准有所提高", "SUPPORTED", "EV-INJURY-2003+EV-INJURY-CURRENT#ART35_ART37", "Grade eight rises from 10 to 11 months."),
        ),
    },
    "F240-D1-HKP4-S2-C1": {
        "CLEAN_CURRENT": (
            ("经国务院第25次常务会议通过", "SUPPORTED", "EV-LABOR-IMPL#HEADER", "Adopting authority/meeting match the official header."),
            ("以国务院令第535号公布", "SUPPORTED", "EV-LABOR-IMPL#HEADER", "State Council Order 535 is the promulgation identity."),
        ),
        "POISON": (
            ("经国务院第25次常务会议通过", "SUPPORTED", "EV-LABOR-IMPL#HEADER", "Adopting body/meeting remain correct."),
            ("以人力资源社会保障部令第535号公布", "CONTROLLED_POISON", "EV-LABOR-IMPL#HEADER", "Ministry is substituted for State Council as Order 535 issuer."),
        ),
        "HARD_NEGATIVE": (
            ("经国务院第25次常务会议通过", "SUPPORTED", "EV-LABOR-IMPL#HEADER", "Adopting body/meeting match."),
            ("于2008年9月18日公布", "SUPPORTED", "EV-LABOR-IMPL#HEADER", "Promulgation date is official."),
        ),
    },
    "F240-D1-HKP4-S2-C2": {
        "CLEAN_CURRENT": (
            ("经国务院第198次常务会议通过", "SUPPORTED", "EV-ANNUAL-REG#HEADER", "Adopting body/meeting match the official header."),
            ("以国务院令第514号公布", "SUPPORTED", "EV-ANNUAL-REG#HEADER", "State Council Order 514 is the promulgation identity."),
        ),
        "POISON": (
            ("经国务院第198次常务会议通过", "SUPPORTED", "EV-ANNUAL-REG#HEADER", "Meeting/body remain correct."),
            ("以人力资源社会保障部令第514号公布", "CONTROLLED_POISON", "EV-ANNUAL-REG#HEADER", "Ministry replaces State Council as Order 514 issuer."),
        ),
        "HARD_NEGATIVE": (
            ("为实施《职工带薪年休假条例》", "SUPPORTED", "EV-ANNUAL-IMPL#ART1", "The implementing-rule purpose is explicit."),
            ("《企业职工带薪年休假实施办法》由人力资源社会保障部令第1号公布", "SUPPORTED", "EV-ANNUAL-IMPL#HEADER", "This is a distinct genuine Ministry Order 1."),
        ),
    },
}


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: audit_formal_d1_canary_atoms_v2.py HANDOFF_ROOT OUTPUT_DIR")
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    if out.resolve().is_relative_to(REPO):
        raise ValueError("Role-bearing atom audit must remain outside Git")
    candidate_path = root / PHASE1 / "PAPER1_FORMAL_D1_CANARY_CANDIDATES_V3.jsonl"
    assert_hash(candidate_path, EXPECTED_HASHES["candidate_v3"])
    manifest = read_json(root / CANARY / "PAPER1_FORMAL_D1_CANARY_EVIDENCE_MANIFEST_V3.json")
    evidence = {x["evidence_doc_id"]: x for x in manifest}
    parent_matrix_path = root / "paper1_formal240_d1_canary_final_owner_acceptance_20260926_run02" / "PAPER1_FORMAL_D1_CANARY_FINAL_ACCEPTANCE_MATRIX_V1.json"
    assert_hash(parent_matrix_path, "9847bdc5ae4b053846007a496ca779ef35a47e99a6e1db2c073e86b65afb07ee")
    parent = read_json(parent_matrix_path)
    if not parent["all_hard_gates_pass"]:
        raise ValueError("Parent Run02 gate was not PASS")
    candidates = [json.loads(line) for line in candidate_path.read_text(encoding="utf-8").splitlines() if line]
    if len(candidates) != 24 or {x["group_slot_id"] for x in candidates} != set(SPECS):
        raise ValueError("Candidate/group population mismatch")
    rows: list[dict[str, Any]] = []
    for c in candidates:
        blind_id, text = c["blind_review_id"], c["candidate_text"]
        group, role = c["group_slot_id"], c["construction_role"]
        atoms = SPECS[group][role]
        candidate_atom_rows = []
        covered = "".join(span for span, *_ in atoms)
        for index, (span, status, locator, reason) in enumerate(atoms, start=1):
            if span not in text:
                raise ValueError(f"Unmatched factual atom: {blind_id}/{index}: {span}")
            doc_ids = locator.split("#", 1)[0].split("+")
            if not set(doc_ids).issubset(c["frozen_evidence_doc_ids"]):
                raise ValueError(f"Atom source outside frozen candidate bundle: {blind_id}/{index}")
            candidate_atom_rows.append({"atom_index": index, "candidate_span": span, "span_start": text.index(span), "classification": status, "official_locator": locator, "evidence_raw_sha256": {doc_id: evidence[doc_id]["snapshot_raw_sha256"] for doc_id in doc_ids}, "reason": reason})
        if Counter(x["classification"] for x in candidate_atom_rows)["CONTROLLED_POISON"] != int(role == "POISON"):
            raise ValueError(f"Poison error-budget failure: {blind_id}")
        # Fail if any explicit number or institutional actor is outside the
        # manually checked spans. This supplements, not replaces, semantic QA.
        numeric_uncovered = sorted(set(re.findall(r"\d+", text)) - set(re.findall(r"\d+", covered)))
        institution_uncovered = sorted(x for x in ("国务院", "人力资源社会保障部", "社会保险经办机构", "用人单位", "医疗机构") if x in text and x not in covered and x not in "".join(re.findall(r"《[^》]+》", text)))
        if numeric_uncovered or institution_uncovered:
            raise ValueError(f"Unreviewed explicit number/institution: {blind_id}: {numeric_uncovered}/{institution_uncovered}")
        rows.append({"blind_review_id": blind_id, "group_slot_id": group, "construction_role": role, "candidate_text_sha256": sha256(text.encode("utf-8")).hexdigest(), "atoms": candidate_atom_rows, "unsupported_accidental": 0, "ambiguous": 0, "coverage_check": {"unreviewed_explicit_numbers": numeric_uncovered, "unreviewed_institution_actors": institution_uncovered}})
    output = {"status": "ADDITIVE_FACT_ATOM_V2_SUPPLEMENT_PASS", "supersedes_granularity_of": "RUN02_FINAL_FACT_ATOM_AUDIT_V1_NOT_RAW_OR_GT", "parent_matrix_sha256": digest(parent_matrix_path), "candidate_v3_sha256": digest(candidate_path), "rows": rows, "candidate_count": len(rows), "atom_count": sum(len(x["atoms"]) for x in rows), "classification_counts": dict(Counter(atom["classification"] for row in rows for atom in row["atoms"])), "poison_controlled_count": sum(atom["classification"] == "CONTROLLED_POISON" for row in rows for atom in row["atoms"]), "clean_hn_unsupported_or_ambiguous": 0, "limitation": "Bounded proposition decomposition plus immutable official-source locator and reviewer QA; not exhaustive theorem proving. Document-title identity is validated by the frozen Candidate/Evidence bundle rather than repeated as a separate atom."}
    if output["poison_controlled_count"] != 8 or output["candidate_count"] != 24:
        raise ValueError("Atom V2 population failure")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "PAPER1_FORMAL_D1_CANARY_FINAL_FACT_ATOM_AUDIT_V2.json"
    file_sha = write_json(path, output)
    print(json.dumps({"status": output["status"], "candidates": 24, "atoms": output["atom_count"], "sha256": file_sha}))


if __name__ == "__main__":
    main()
