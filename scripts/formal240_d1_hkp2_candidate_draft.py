"""Create an INTERNAL HKP2 triplet draft only after snapshot identity passes.

The output is not a blind package, an accepted candidate corpus, or GT. Human
fact-atom inspection and independent blind review remain mandatory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


# C/P/H are internal construction roles. Never give this module to reviewers.
TRIPLETS: dict[str, tuple[str, str, str, str]] = {
    "F240-D1-HKP2-S1-C2": (
        "《劳动合同法》规定，以完成一定工作任务为期限的劳动合同不得约定试用期；劳动合同期限不满三个月的，也不得约定试用期。",
        "《劳动合同法》规定，以完成一定工作任务为期限的劳动合同不得约定试用期；同一类合同同时可以约定试用期。",
        "依《劳动合同法》，期限不少于三个月的固定期限劳动合同可在法定上限内约定试用期，但以完成一定工作任务为期限的合同不得约定。",
        "以完成一定工作任务为期限的劳动合同能否约定试用期",
    ),
    "F240-D1-HKP2-S1-C3": (
        "《失业保险条例》规定，领取失业保险金须已办理失业登记并有求职要求，同时还要符合单位和本人按规定缴费满一年等条件。",
        "《失业保险条例》规定，领取失业保险金既要求已办理失业登记，又不要求办理失业登记；两种条件适用于同一申请。",
        "按《失业保险条例》，失业人员即使已办理失业登记，如果没有求职要求，仍不满足领取失业保险金的全部条件。",
        "失业保险金领取条件中的失业登记要求",
    ),
    "F240-D1-HKP2-S1-C4": (
        "《禁止使用童工规定》禁止普通餐饮企业招用十五岁人员；符合条件的文艺、体育单位则可招用未满十六岁的专业文艺工作者或运动员。",
        "按《禁止使用童工规定》，普通餐饮企业招用十五岁人员属于禁止使用童工的情形；该规定同时允许这家普通餐饮企业直接招用十五岁人员。",
        "按《禁止使用童工规定》，普通餐饮企业不能招用十五岁人员；文艺单位经其监护人同意，可招用十五岁的专业文艺工作者。",
        "禁止使用童工规定的一般禁令与文艺体育例外",
    ),
    "F240-D1-HKP2-S2-C2": (
        "《劳动争议调解仲裁法》规定，劳动关系存续期间追索拖欠劳动报酬，不受一般一年仲裁时效限制；关系终止后须在终止之日起一年内提出。",
        "《劳动争议调解仲裁法》规定，即使劳动关系仍然存续，职工追索拖欠劳动报酬也一律受一般一年仲裁时效限制；关系终止后亦如此。",
        "《劳动争议调解仲裁法》规定，劳动关系已经终止的职工追索拖欠劳动报酬，即使此前不受一般时效限制，仍须自终止之日起一年内申请仲裁。",
        "劳动关系存续期间工资拖欠的仲裁时效例外",
    ),
    "F240-D1-HKP2-S2-C3": (
        "《保障农民工工资支付条例》规定，约定的工资支付日若遇法定节假日，应在节假日前支付；因不可抗力未能按期支付的，应在其消除后及时支付。",
        "《保障农民工工资支付条例》规定，约定的工资支付日若遇法定节假日，用人单位可一律顺延至节后支付；无须发生不可抗力。",
        "依《保障农民工工资支付条例》，工资支付日遇休息日应提前支付；若因不可抗力无法按期支付，则在不可抗力消除后及时支付。",
        "农民工工资支付日遇节假日与不可抗力的处理",
    ),
    "F240-D1-HKP2-S2-C4": (
        "《劳务派遣暂行规定》要求，用工单位确定使用被派遣劳动者的辅助性岗位，应经职工讨论、与工会或职工代表协商，并在单位内公示。",
        "《劳务派遣暂行规定》允许用工单位确定辅助性岗位时，虽经职工讨论并公示，但无须与工会或职工代表平等协商。",
        "依《劳务派遣暂行规定》，用工单位拟确定辅助性岗位，须经职工代表大会或全体职工讨论，与工会或职工代表协商后公示。",
        "劳务派遣辅助性岗位确定程序中的协商要求",
    ),
    "F240-D1-HKP2-S3-C1": (
        "比较1994年发布文本与1995年修订文本的《国务院关于职工工作时间的规定》，国家机关、事业单位的周六休息安排由隔周休息改为每周休息。",
        "比较1994年发布文本与1995年修订文本的《国务院关于职工工作时间的规定》，国家机关、事业单位周六休息日的适用范围并未改变。",
        "《国务院关于职工工作时间的规定》1994年文本要求国家机关、事业单位周六隔周休息，而1995年修订文本将周六、周日均列为周休息日。",
        "国务院关于职工工作时间的规定1994与1995文本的周六休息安排",
    ),
    "F240-D1-HKP2-S3-C2": (
        "比较2013版与2024修订版《全国年节及纪念日放假办法》，全体公民劳动节的法定放假日期范围发生变化，2024版新增五月二日。",
        "比较2013版与2024修订版《全国年节及纪念日放假办法》，全体公民劳动节法定放假日期的范围在两版之间保持不变。",
        "《全国年节及纪念日放假办法》2013版将劳动节列为一日法定假期，2024修订版则将该节日的法定假期增加一天。",
        "2013与2024放假办法中的劳动节法定假日范围",
    ),
    "F240-D1-HKP2-S3-C3": (
        "《工伤保险条例》2003原版与2010修订版对上下班途中交通事故认定工伤的情形范围发生变化，后者加入非本人主要责任等限定及其他交通方式。",
        "《工伤保险条例》2003原版与2010修订版对上下班途中交通事故认定工伤的情形范围保持不变，两版的条件并无差异。",
        "《工伤保险条例》2003原版写上下班途中机动车事故伤害，而2010修订版写非本人主要责任的交通事故，并列入城市轨道交通等情形。",
        "工伤保险条例2003与2010版本通勤事故认定范围",
    ),
    "F240-D1-HKP2-S3-C4": (
        "比较1988年《女职工劳动保护规定》第八条和2012年《女职工劳动保护特别规定》第七条，两条法规正文在是否明列四个月孕期分档上存在差别。",
        "比较1988年《女职工劳动保护规定》第八条和2012年《女职工劳动保护特别规定》第七条，两条法规正文在是否明列四个月孕期分档上并无差别。",
        "1988年《女职工劳动保护规定》第八条按医务部门证明给予一定时间产假，而2012年《女职工劳动保护特别规定》第七条直接列出以四个月孕期为界的两档产假。",
        "1988与2012女职工保护规定法规正文的流产产假孕期分档表述",
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precontract", type=Path, required=True)
    parser.add_argument("--evidence-audit", type=Path, required=True)
    parser.add_argument("--scope-overlay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(args.precontract.read_text(encoding="utf-8"))
    audit = json.loads(args.evidence_audit.read_text(encoding="utf-8"))
    if audit["status"] != "PRECONSTRUCTION_EVIDENCE_IDENTITY_GATE_PASS":
        raise SystemExit("Official evidence identity gate has not passed")
    groups = {g["group_slot_id"]: g for g in plan["groups"]}
    overlay = json.loads(args.scope_overlay.read_text(encoding="utf-8"))
    repaired_group_id = overlay["group_slot_id"]
    if repaired_group_id != "F240-D1-HKP2-S3-C4":
        raise SystemExit("Unexpected scope-repair target")
    groups[repaired_group_id]["primary_factual_core_id"] = overlay[
        "new_primary_factual_core_id"
    ]
    if set(groups) != set(TRIPLETS):
        raise SystemExit("Triplet plans do not match the ten frozen group slots")
    if args.output.exists():
        raise SystemExit(f"Refusing to overwrite: {args.output}")
    rows = []
    for group_id, (clean, poison, hard_negative, neutral_query) in TRIPLETS.items():
        group = groups[group_id]
        for role, candidate_text in (
            ("CLEAN_CURRENT", clean),
            ("POISON", poison),
            ("HARD_NEGATIVE", hard_negative),
        ):
            if group_id in {
                "F240-D1-HKP2-S3-C2",
                "F240-D1-HKP2-S3-C4",
            }:
                id_version = "hkp2-s3-numeric-surface-repair-v1"
            elif group_id in {
                "F240-D1-HKP2-S1-C2",
                "F240-D1-HKP2-S3-C1",
                "F240-D1-HKP2-S3-C3",
            }:
                id_version = "hkp2-style-parity-repair-v1"
            elif group_id in {
                "F240-D1-HKP2-S2-C2",
                "F240-D1-HKP2-S2-C4",
            }:
                id_version = "hkp2-document-identity-repair-v1"
            else:
                id_version = "hkp2-draft-v1"
            sample_id = "F240D1-" + hashlib.sha256(
                f"{id_version}|{group_id}|{role}".encode()
            ).hexdigest()[:14].upper()
            rows.append(
                {
                    "sample_id": sample_id,
                    "group_slot_id": group_id,
                    "role": role,
                    "target_s": group["target_s"],
                    "candidate_version": "DRAFT_V8_NUMERIC_SURFACE_REPAIRED_NOT_RELEASED"
                    if id_version == "hkp2-s3-numeric-surface-repair-v1"
                    else "DRAFT_V7_STYLE_PARITY_REPAIRED_NOT_RELEASED"
                    if id_version == "hkp2-style-parity-repair-v1"
                    else "DRAFT_V6_DOCUMENT_IDENTITY_REPAIRED_NOT_RELEASED"
                    if id_version == "hkp2-document-identity-repair-v1"
                    else "DRAFT_V4_UNCHANGED_NOT_RELEASED",
                    "candidate_text": candidate_text,
                    "neutral_query": neutral_query,
                    "primary_factual_core_id": group["primary_factual_core_id"],
                    "family_cluster_id": group["family_cluster_id"],
                    "evidence_refs": group["evidence_refs"],
                    "fact_atom_audit": "PENDING_INDEPENDENT_BOUNDED_AUDIT",
                    "external_blind_review": "NOT_RELEASED",
                }
            )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
