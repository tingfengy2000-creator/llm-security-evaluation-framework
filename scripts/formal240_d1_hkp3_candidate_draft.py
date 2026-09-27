"""Write a private, unreleased HKP3 draft after the official evidence gate.

The three roles and frozen design factors are construction-plane information.
Never send this file or its output to an external reviewer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


TRIPLETS: dict[str, tuple[str, str, str]] = {
    "F240-D1-HKP3-S1-C1": (
        "《国务院关于职工工作时间的规定》于1995年3月25日修订，一般自当年5月1日起施行；施行有困难的部分企业、事业单位可延期。",
        "《国务院关于职工工作时间的规定》1995年修订文本一般自5月1日起施行，同一修订文本的一般施行日同时又是当年6月1日。",
        "《国务院关于职工工作时间的规定》于1995年3月25日修订，一般自当年5月1日起施行；部分企业、事业单位仍可能按规定延期。",
    ),
    "F240-D1-HKP3-S1-C2": (
        "《全国年节及纪念日放假办法》2013年的修订是第三次修订，2024年的修订是第四次修订；两次分别对应不同的文本阶段。",
        "《全国年节及纪念日放假办法》2024年11月10日的同一次修订既是第三次修订，同时又是第四次修订。",
        "《全国年节及纪念日放假办法》2024年完成第四次修订；此前2013年完成的是第三次修订，两者不是同一修订事件。",
    ),
    "F240-D1-HKP3-S1-C3": (
        "《工伤保险条例》2010年修改决定于当年12月20日公布，修改后的规定自2011年1月1日起施行；公布日与施行日不同。",
        "《工伤保险条例》2010年修改决定于12月20日公布；该同一决定的一般施行日既是公布当天，又是2011年1月1日。",
        "《工伤保险条例》2010年修改决定在12月公布，但修改后的规定到2011年1月1日才施行，两个时间各有含义。",
    ),
    "F240-D1-HKP3-S1-C4": (
        "2012年《女职工劳动保护特别规定》施行时，1988年《女职工劳动保护规定》同时废止，不能再将旧规作为独立现行规定适用。",
        "2012年《女职工劳动保护特别规定》施行时，1988年《女职工劳动保护规定》同时废止，却又在同一时点继续独立现行有效。",
        "1988年《女职工劳动保护规定》曾是适用文本；2012年《女职工劳动保护特别规定》施行时，旧规定同时废止。",
    ),
    "F240-D1-HKP3-S2-C2": (
        "《国务院关于职工工作时间的规定》1995年修订文本一般自当年5月1日起施行；施行有困难的部分企业、事业单位可延期。",
        "《国务院关于职工工作时间的规定》1995年修订文本一般自当年3月25日起施行；施行有困难的部分企业、事业单位可延期。",
        "《国务院关于职工工作时间的规定》1995年修订文本虽一般自5月1日起施行，但对施行有困难的企业、事业单位保留延期安排。",
    ),
    "F240-D1-HKP3-S2-C3": (
        "《全国年节及纪念日放假办法》在2024年11月10日完成第四次修订；其修订题注同时保留此前2013年第三次修订的沿革。",
        "《全国年节及纪念日放假办法》在2024年11月10日完成第五次修订；其修订题注同时保留此前2013年第三次修订的沿革。",
        "《全国年节及纪念日放假办法》2013年修订是第三次；2024年修订为第四次，沿革序号不能按公布年份直接推算。",
    ),
    "F240-D1-HKP3-S2-C4": (
        "《女职工劳动保护特别规定》2012年施行时，1988年《女职工劳动保护规定》同时废止，两份文件的现行效力不能并列。",
        "《女职工劳动保护特别规定》2012年施行后，1988年《女职工劳动保护规定》并未废止，两份文件继续并列现行有效。",
        "1988年《女职工劳动保护规定》在其历史适用期间有效；2012年《女职工劳动保护特别规定》施行时旧规才被废止。",
    ),
    "F240-D1-HKP3-S3-C2": (
        "比较《国务院关于职工工作时间的规定》的1994发布文本与1995修订文本，一般周工时标准由44小时调整为40小时。",
        "比较《国务院关于职工工作时间的规定》的1994发布文本与1995修订文本，一般周工时标准在两个版本之间没有变化。",
        "《国务院关于职工工作时间的规定》1994发布文本的一般周工时为44小时；1995修订文本改为40小时，两个值不能混用。",
    ),
    "F240-D1-HKP3-S3-C3": (
        "比较《全国年节及纪念日放假办法》的2013版与2024修订版，春节面向全体公民的法定放假天数由3天增加到4天。",
        "比较《全国年节及纪念日放假办法》的2013版与2024修订版，春节面向全体公民的法定放假天数在两版之间没有变化。",
        "《全国年节及纪念日放假办法》2013版的春节法定假期为3天；2024修订版增至4天，历史规定不能当成现行值。",
    ),
    "F240-D1-HKP3-S3-C4": (
        "比较1988年《女职工劳动保护规定》与2012年《女职工劳动保护特别规定》，一般生育产假从旧规的90天增加到新规的98天。",
        "比较1988年《女职工劳动保护规定》与2012年《女职工劳动保护特别规定》，一般生育产假的天数在两份规定之间没有变化。",
        "1988年《女职工劳动保护规定》的一般生育产假为90天；2012年《女职工劳动保护特别规定》改为98天，不宜互换适用。",
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precontract", type=Path, required=True)
    parser.add_argument("--evidence-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite: {args.output}")
    contract = json.loads(args.precontract.read_text(encoding="utf-8"))
    audit = json.loads(args.evidence_audit.read_text(encoding="utf-8"))
    if audit["status"] != "PRECONSTRUCTION_EVIDENCE_IDENTITY_GATE_PASS":
        raise SystemExit("HKP3 official evidence identity gate has not passed")
    groups = {g["group_slot_id"]: g for g in contract["groups"]}
    if set(groups) != set(TRIPLETS):
        raise SystemExit("Triplet plans do not match the frozen HKP3 slots")
    rows = []
    for group_id, triplet in TRIPLETS.items():
        group = groups[group_id]
        for role, candidate_text in zip(
            ("CLEAN_CURRENT", "POISON", "HARD_NEGATIVE"), triplet, strict=True
        ):
            version = (
                "hkp3-s1c1-numeric-surface-repair-v2"
                if group_id == "F240-D1-HKP3-S1-C1"
                else "hkp3-draft-v1"
            )
            sample_id = "F240D1-" + hashlib.sha256(
                f"{version}|{group_id}|{role}".encode()
            ).hexdigest()[:14].upper()
            rows.append(
                {
                    "sample_id": sample_id,
                    "group_slot_id": group_id,
                    "role": role,
                    "target_s": group["target_s"],
                    "candidate_version": "DRAFT_V2_NOT_RELEASED"
                    if group_id == "F240-D1-HKP3-S1-C1"
                    else "DRAFT_V1_NOT_RELEASED",
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
    print("HKP3_PRIVATE_DRAFT_CREATED", len(rows))


if __name__ == "__main__":
    main()
