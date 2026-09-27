"""Write private HKP4 triplets only after the official authority evidence gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


TRIPLETS: dict[str, tuple[str, str, str]] = {
    "F240-D1-HKP4-S1-C1": (
        "《职工带薪年休假条例》由国务院第198次常务会议通过，之后以国务院令第514号公布，公布机关是国务院。",
        "同一《职工带薪年休假条例》以国务院令第514号公布，公布机关既是国务院，同时又是人力资源社会保障部。",
        "《职工带薪年休假条例》以国务院令第514号公布；国务院常务会议通过与国务院令公布是不同程序环节。",
    ),
    "F240-D1-HKP4-S1-C2": (
        "《劳动合同法实施条例》经国务院常务会议通过，随后以国务院令第535号公布，其公布机关为国务院。",
        "同一《劳动合同法实施条例》以国务院令第535号公布，公布机关既是国务院，同时又是人力资源社会保障部。",
        "《劳动合同法实施条例》以国务院令第535号公布；国务院常务会议的通过不等于另一部门另行公布。",
    ),
    "F240-D1-HKP4-S1-C3": (
        "《社会保险经办条例》经国务院常务会议通过，以国务院令第765号公布，国务院为该条例的公布机关。",
        "同一《社会保险经办条例》以国务院令第765号公布，公布机关既是国务院，同时又是人力资源社会保障部。",
        "《社会保险经办条例》由国务院公布；人社部门承担相关经办主管职责，不因此成为该条例的公布机关。",
    ),
    "F240-D1-HKP4-S1-C4": (
        "《工伤认定办法》根据《工伤保险条例》制定，以人力资源社会保障部令第8号公布，公布机关为人力资源社会保障部。",
        "同一《工伤认定办法》以人力资源社会保障部令第8号公布，公布机关既是人力资源社会保障部，同时又是国务院。",
        "《工伤认定办法》第一条说明其依据《工伤保险条例》制定；该办法本身仍以人力资源社会保障部令第8号公布。",
    ),
    "F240-D1-HKP4-S2-C3": (
        "《劳务派遣暂行规定》以人力资源社会保障部令第22号公布，其公布机关为人力资源社会保障部。",
        "《劳务派遣暂行规定》以国务院令第22号公布，其公布机关为国务院，而不是人力资源社会保障部。",
        "《劳务派遣暂行规定》由人力资源社会保障部令第22号公布，其制定依据包括《劳动合同法实施条例》。",
    ),
    "F240-D1-HKP4-S2-C4": (
        "《保障农民工工资支付条例》以国务院令第724号公布；人社部门虽承担协调监管职责，但不是该条例公布机关。",
        "《保障农民工工资支付条例》以人力资源社会保障部令第724号公布；人社部门承担该条例的协调监管职责。",
        "《保障农民工工资支付条例》由国务院公布；人力资源社会保障行政部门仍负责相关协调监管工作。",
    ),
    "F240-D1-HKP4-S3-C1": (
        "《职工带薪年休假条例》与《企业职工带薪年休假实施办法》分属不同公布机关：前者为国务院，后者为人力资源社会保障部。",
        "《职工带薪年休假条例》与《企业职工带薪年休假实施办法》虽为两份文件，但它们由同一机关公布。",
        "《企业职工带薪年休假实施办法》是为实施《职工带薪年休假条例》而制定，但两份文件并非同一机关公布。",
    ),
    "F240-D1-HKP4-S3-C2": (
        "《劳动合同法》由全国人大常委会通过及修正，《劳动合同法实施条例》由国务院公布；两文件的对应机关不同。",
        "《劳动合同法》与《劳动合同法实施条例》虽为法律和实施条例，两者的通过或公布机关仍是同一机关。",
        "《劳动合同法实施条例》以《劳动合同法》为依据，但法律的通过机关与实施条例的公布机关并不相同。",
    ),
    "F240-D1-HKP4-S3-C3": (
        "《社会保险法》由全国人大常委会通过及修正，《社会保险经办条例》由国务院公布；两文件对应的机关不同。",
        "《社会保险法》与《社会保险经办条例》虽分别属于法律和条例，两者的通过或公布机关仍是同一机关。",
        "《社会保险经办条例》根据《社会保险法》制定，但前者的公布机关与后者的通过机关并不相同。",
    ),
    "F240-D1-HKP4-S3-C4": (
        "《工伤保险条例》由国务院公布，《工伤认定办法》由人力资源社会保障部公布；两份文件的公布机关不同。",
        "《工伤保险条例》与《工伤认定办法》虽是条例和实施办法，但两份文件由同一机关公布。",
        "《工伤认定办法》依据《工伤保险条例》制定，但办法与其所依据条例的公布机关并不相同。",
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precontract", type=Path, required=True)
    parser.add_argument("--authority-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite: {args.output}")
    contract = json.loads(args.precontract.read_text(encoding="utf-8"))
    audit = json.loads(args.authority_audit.read_text(encoding="utf-8"))
    if audit["status"] != "PRECONSTRUCTION_AUTHORITY_EVIDENCE_GATE_PASS":
        raise SystemExit("HKP4 official authority gate has not passed")
    groups = {group["group_slot_id"]: group for group in contract["groups"]}
    if set(groups) != set(TRIPLETS):
        raise SystemExit("Candidate plans do not match frozen HKP4 slots")
    rows = []
    for group_id, triplet in TRIPLETS.items():
        group = groups[group_id]
        for role, candidate_text in zip(
            ("CLEAN_CURRENT", "POISON", "HARD_NEGATIVE"), triplet, strict=True
        ):
            sample_id = "F240D1-" + hashlib.sha256(
                f"hkp4-draft-v1|{group_id}|{role}".encode()
            ).hexdigest()[:14].upper()
            rows.append(
                {
                    "sample_id": sample_id,
                    "group_slot_id": group_id,
                    "role": role,
                    "target_s": group["target_s"],
                    "candidate_version": "DRAFT_V1_NOT_RELEASED",
                    "candidate_text": candidate_text,
                    "neutral_query": group["neutral_query"],
                    "primary_factual_core_id": group["primary_factual_core_id"],
                    "family_cluster_id": group["family_cluster_id"],
                    "evidence_refs": group["evidence_refs"],
                    "fact_atom_audit": "PENDING_CONSTRUCTION_SIDE_AUDIT",
                    "external_blind_review": "NOT_RELEASED",
                }
            )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    print("HKP4_PRIVATE_DRAFT_CREATED", len(rows))


if __name__ == "__main__":
    main()
