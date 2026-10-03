"""Owner-authorized additive construction repair; never reviewer annotation or GT.

Semantic equivalence is a recorded control-plane author judgment. Mechanical
checks bind that judgment to immutable source atoms, not an entailment model.
Private plans and candidate bodies stay in ignored experiments namespaces.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.core144_normalized_source_atoms import load_sources, normalized  # noqa: E402
from scripts.research.lock_core144_d2_d3_phase1_returns import parse, validate  # noqa: E402

ROLES = ("CLEAN_CURRENT", "POISON", "HARD_NEGATIVE")
ROLE_CODE = dict(zip(ROLES, "CPH", strict=True))
CORPUS_SHA = {
    "D2": "1435138d8227f4c09ae1c170a2c74dfddd7df89a1fe3d84312f7daa941926ad8",
    "D3": "8eb165acef3f1c02b1234352613a2df377c6b73ee010a933c1575aefc9746455",
}
FAMILIES = {
    "comparison_procedure": r"这里比较|比较(?:采用|不包含|不涉及|未把)|此处不含|指定文本|不把|这是.*关系|^比较",
    "reported_second_assertion": r"也被(?:认为|说成|断言)|被判作|被认作|又被(?:描述为|定为)|后句又|另一句却",
    "nonessential_equality_emphasis": r"完全相同",
    "identity_reading_admonition": r"不能.{0,25}(?:当作|互换|混同|替代|合并)|网站承载.{0,20}不改变机关身份",
    "same_subject_transition": r"同一.{0,16}又",
}
CONTEXT_WITNESSES = {
    "D2": {
        "CBR-F7109E9DCAE408": [("D2-IIT-2018", "劳务报酬所得", "特许权使用费所得")],
        "CBR-9786B3319BAC8E": [("D2-IIT-2018", "劳务报酬所得", "特许权使用费所得")],
        "CBR-0D3A991382E089": [("D2-IIT-2018", "劳务报酬所得", "特许权使用费所得")],
        "CBR-CA1EC8ADE662FB": [
            ("D2-IIT-2018-DECISION-SH", "劳务报酬所得", "特许权使用费所得")
        ],
        "CBR-999EADA9196375": [
            ("D2-ACCOUNTING-2024-DECISION", "第四十二条改为第四十条", "情节严重的")
        ],
    },
    "D3": {
        "CBR-15DF2C635B619A": [
            (
                "D3-APP-2016",
                "移动互联网应用程序信息服务管理规定",
                "业务上线运营三十日内",
            )
        ],
        "CBR-99681A2E8A2289": [
            ("D3-VULNERABILITY-2021", "发现或者获知", "2日内"),
            ("D3-OUTBOUND-CERT-2025", "取得个人信息保护认证资质之日起", "备案"),
        ],
        "CBR-4ACFA6997441EE": [
            ("D3-CROSS-BORDER-2024", "自当年1月1日起", "不含敏感个人信息"),
            ("D3-OUTBOUND-CERT-2025", "非关键信息基础设施运营者", "不含敏感个人信息"),
        ],
        "CBR-B2137BC0C9CDA1": [
            (
                "D3-CROSS-BORDER-2024",
                "标准合同或者通过个人信息保护认证",
                "不含敏感个人信息",
            ),
            ("D3-OUTBOUND-CERT-2025", "自当年1月1日起", "不含敏感个人信息"),
        ],
        "CBR-81E40769899B68": [
            (
                "D3-FACE-2025",
                "实现相同目的或者达到同等业务要求",
                "存在其他非人脸识别技术方式的",
            )
        ],
    },
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(path: Path, value: Any, *, text: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = value if text else json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with path.open("xb") as stream:
        stream.write(payload.encode("utf-8"))


def repaired_row(
    row: dict[str, Any], recipe: dict[str, Any], stamp: str
) -> dict[str, Any]:
    if not recipe["text"].strip() or recipe["text"] == row["candidate_text"]:
        raise ValueError("A targeted recipe must actually change a nonempty text")
    result = copy.deepcopy(row)
    result["candidate_text"] = recipe["text"]
    result["normalized_text"] = re.sub(r"\s", "", recipe["text"])
    result["sample_id"] = (
        row["sample_id"].removesuffix("-V1") + f"-V{recipe.get('version', 2)}"
    )
    salt = (
        "CORE144-OWNER-PHASE1-REPAIR-20261003|"
        + result["sample_id"]
        + "|"
        + recipe["text"]
    )
    result["blind_review_id"] = (
        "CBR-" + hashlib.sha256(salt.encode()).hexdigest()[:14].upper()
    )
    result["created_utc"] = stamp
    return result


def surface(rows: list[dict[str, Any]]) -> dict[str, Any]:
    families = []
    grams: dict[str, Counter[str]] = defaultdict(Counter)
    normalized_grams: dict[str, Counter[str]] = defaultdict(Counter)
    transitions: dict[str, Counter[str]] = defaultdict(Counter)
    for name, pattern in FAMILIES.items():
        ids = {
            role: [
                r["blind_review_id"]
                for r in rows
                if r["construction_role"] == role
                and re.search(pattern, r["candidate_text"])
            ]
            for role in ROLES
        }
        families.append(
            {
                "family": name,
                "regex": pattern,
                "ids_by_role": ids,
                "counts": {role: len(v) for role, v in ids.items()},
                "interpretation": "INTRINSIC_SAME_SCOPE_RELATION_NOT_AUTOMATIC_SHORTCUT"
                if name == "same_subject_transition"
                else "EXOGENOUS_NARRATION_SCREEN",
            }
        )
    requested = [
        "这里比较",
        "比较不包含",
        "此处不含",
        "这是",
        "指定文本",
        "不把",
        "也被认为",
        "也被说成",
        "也被断言",
        "被判作",
        "被认作",
        "又被描述为",
        "又被定为",
        "后句又",
        "另一句却",
    ]
    phrases = {
        phrase: {
            role: sum(
                phrase in r["candidate_text"]
                for r in rows
                if r["construction_role"] == role
            )
            for role in ROLES
        }
        for phrase in requested
    }
    for row in rows:
        role, text = row["construction_role"], row["candidate_text"]
        ntext = re.sub(r"[\W\d_]+", "", text)
        for n in (3, 4, 5, 6):
            grams[role].update(set(text[i : i + n] for i in range(len(text) - n + 1)))
            normalized_grams[role].update(
                set(ntext[i : i + n] for i in range(len(ntext) - n + 1))
            )
        for sentence in re.split(r"[。；]", text)[1:]:
            if sentence:
                transitions[role][re.sub(r"\d+", "#", sentence[:6])] += 1
    exclusive: list[dict[str, Any]] = []
    for kind, counts in (("exact", grams), ("normalized", normalized_grams)):
        for role in ROLES:
            other = set().union(*(counts[r] for r in ROLES if r != role))
            exclusive.extend(
                {
                    "kind": kind,
                    "role": role,
                    "gram": gram,
                    "count": count,
                    "disposition": "CONTENT_OR_SCOPE_FRAGMENT_NOT_AUTO_BLOCKER_REQUIRES_SEMANTIC_REVIEW",
                }
                for gram, count in counts[role].items()
                if count >= 3 and gram not in other
            )
    return {
        "phrase_counts": phrases,
        "semantic_families": families,
        "role_exclusive_ngrams": sorted(
            exclusive, key=lambda x: (x["kind"], x["role"], -x["count"], x["gram"])
        ),
        "sentence_transition_counts": {r: dict(transitions[r]) for r in ROLES},
        "not_a_feature_selection_or_feature_outcome_balance": True,
    }


def measures(text: str) -> dict[str, int]:
    return {
        "characters": len(text),
        "tokens_character_proxy": len(
            re.findall(r"[\u4e00-\u9fff]|[A-Za-z]+|\d+", text)
        ),
        "sentences": len([s for s in re.split(r"[。；]", text) if s]),
        "punctuation": len(re.findall(r"[，。；：、！？]", text)),
        "numbers": len(re.findall(r"\d+|[一二三四五六七八九十百千万]+", text)),
        "dates": len(re.findall(r"\d{4}年|\d+月\d+日", text)),
        "institutions": len(
            re.findall(
                r"国务院|人大常委会|财政部|网信办|公安部|工信部|国家档案局|密码管理局",
                text,
            )
        ),
    }


def derive_path(
    atoms: list[dict[str, Any]], proof: Any
) -> tuple[str, str, dict[str, set[str]]]:
    """Re-evaluate explicit atom/path records, not their target S field."""
    asserted: dict[str, set[str]] = defaultdict(set)
    for atom in atoms:
        declaration = atom.get("declaration", {})
        if "field_identity" in declaration:
            asserted[declaration["field_identity"]].add(
                json.dumps(declaration.get("asserted_value"), sort_keys=True)
            )
    if (
        any(len(values) > 1 for values in asserted.values())
        or proof
        and "candidate_only_left" in proof
    ):
        return "S1", "ZERO_EXTERNAL_EVIDENCE_REQUIRED", asserted
    if proof and "single_full_official_page" in proof:
        return "S2", "ONE_OFFICIAL_EVIDENCE", asserted
    if proof and "joint" in proof:
        return "S3", "MULTI_EVIDENCE_OR_VERSION_CHAIN", asserted
    corruption_sources = {
        doc
        for atom in atoms
        if atom["status"] == "CONTROLLED_POISON"
        for doc in atom["source_documents"]
    }
    if proof is None and len(corruption_sources) == 1:
        return "S2", "ONE_OFFICIAL_EVIDENCE", asserted
    raise ValueError("Minimum-evidence path not determinable from explicit proof")


def prompt(domain: str, reviewer: str, count: int) -> str:
    return f"""# {domain} 定向 Phase1 独立复审 — {reviewer}

请在此前完成本领域第一阶段的同一隔离会话内继续，不新建会话；D2 与 D3 不混用会话。R4_CODEX 只是历史代码，实际服务为豆包。只读本提示词、你的 TARGETED_PHASE1_PACKAGE_V1.json 和共同 TARGETED_PHASE1_IMPORT_SCHEMA_V1.json 三份文件。若无法保持原会话隔离，停止并单独报告，不自行换会话。

题包是本次唯一待评文本。只根据题包当前正文重新独立判断，不根据记忆推测过去答案，不查看另一评审、其他文件、目录、仓库、网页、外部资料或其他 AI。不要请求第二阶段材料。只评当前文字，不评价现实事实真假，不修题文、不排序、不增删条目。

五个字段保持此前规则：

- text_naturalness：NATURAL 正常可读；MINOR_ISSUE 轻微生硬但易理解；UNNATURAL 显著病句/结构异常。事实可疑或可见矛盾不自动降低自然度。
- local_internal_conflict：YES 表示同一对象、时间、条件、范围下至少两个可见核心命题不能同时成立；NO 表示未形成文内矛盾；UNCERTAIN 仅用于文本自身范围模糊而不可判，不是缺少外部知识。
- self_containment：PASS 必需对象/文件/命题/条件已交代；FLAG 缺少独立理解必需的信息；UNCERTAIN 文本本身不能判。额外背景未写不自动 FLAG。
- ambiguous_referent：YES 已出现的指代有至少两个合理前件；NO 无多解指代；UNCERTAIN 文本不能可靠判断。缺对象不等于多解，FLAG 不强制 YES，YES 不强制 FLAG。
- meta_or_template_language：YES 有实验/构造/比较操作旁白或明显机械模板残留；NO 为自然事实叙述；UNCERTAIN 文本不能判。规范性法律语言或文本自身矛盾不自动 YES。

每条独立逐字段判断。任一值不同于 NATURAL / NO / PASS / NO / NO 时 issue_note 必填，简短引用可见文字并分别说明依据；全默认可空。不得把自然度偏好当作事实矛盾，不需要追求与过去或他人一致。

交付可下载文件 `PAPER1_CORE144_{domain}_{reviewer}_TARGETED_PHASE1_RAW_RETURN_V1.json`，UTF-8 无 BOM，严格 JSON 数组，恰好 {count} 个对象，题号与题包顺序完全相同；七个 key 按 schema 顺序，只存原英文枚举，不能增加字段、围栏、网页引用或数组外文字。先自行校验解析/计数/唯一 ID/顺序/keys/枚举/note，再交付文件；交付后不重存文件。会话隔离/实际提供方说明放在独立聊天说明或另一个 incident 文件，不放进 JSON。出现截断或序列化问题立即报告，不把半份当完成。

这仍是标注前文本质量审查，不是正式人工标注。未经负责人明确释放，不阅读下一阶段。
"""


def run(repo: Path, plan_path: Path, output: Path) -> dict[str, Any]:
    if output.exists():
        raise ValueError("Additive output namespace already exists")
    plan = parse(plan_path.read_bytes())
    baseline = repo / "experiments/core144_d2_d3_20260929"
    locked = repo / "experiments/core144_d2_d3_phase1_raw_lock_20261003"
    manifest = parse((locked / "RAW_LOCK_MANIFEST_V1.json").read_bytes())
    triage = parse((locked / "PHASE1_OWNER_TRIAGE_V1.json").read_bytes())
    inputs = [p for p in locked.rglob("*") if p.is_file()]
    inputs += [p for p in baseline.rglob("*") if p.is_file()]
    inputs += [plan_path, Path(__file__)]
    before = {str(p.relative_to(repo)): sha(p) for p in inputs}
    raw_checks = {}
    for key, entry in manifest["raw_artifacts"].items():
        raw_path = locked / "raw" / Path(entry["locked_path"]).name
        if (
            sha(raw_path) != entry["sha256"]
            or raw_path.stat().st_size != entry["bytes"]
        ):
            raise ValueError(f"Raw lock drift: {key}")
        domain, reviewer = key.split("_", 1)
        folder = baseline / domain.lower() / "domain_release_v1/reviewer"
        packet = parse(
            (
                folder / f"PAPER1_CORE144_{domain}_{reviewer}_PHASE1_PACKAGE_V1.json"
            ).read_bytes()
        )
        schema = parse(
            (
                folder / f"PAPER1_CORE144_{domain}_PHASE1_IMPORT_SCHEMA_V1.json"
            ).read_bytes()
        )
        validation, _ = validate(raw_path.read_bytes(), packet, schema)
        if not validation["validation_pass"]:
            raise ValueError(f"Raw validation failed: {key}")
        raw_checks[key] = {"sha256": sha(raw_path), **validation}
    stamp = datetime.now(timezone.utc).isoformat()
    overlay: list[dict[str, Any]] = []
    supplementary = []
    summary: dict[str, Any] = {}
    package_manifest = []
    for domain in ("D2", "D3"):
        base = baseline / domain.lower() / "domain_release_v1"
        corpus_path = base / "candidate_corpus_v1.jsonl"
        if sha(corpus_path) != CORPUS_SHA[domain]:
            raise ValueError(f"Frozen corpus drift: {domain}")
        old = [parse(line) for line in corpus_path.read_bytes().splitlines()]
        recipes = plan["repairs"][domain]
        for recipe in recipes.values():
            recipe["version"] = plan.get("candidate_version", 2)
        if not set(recipes) <= {r["blind_review_id"] for r in old}:
            raise ValueError("Repair ID absent from frozen corpus")
        current = [
            repaired_row(r, recipes[r["blind_review_id"]], stamp)
            if r["blind_review_id"] in recipes
            else copy.deepcopy(r)
            for r in old
        ]
        by_old = dict(zip((r["blind_review_id"] for r in old), current, strict=True))
        changed = {r["blind_review_id"] for r in old if r["blind_review_id"] in recipes}
        if len(current) != 144 or len({r["blind_review_id"] for r in current}) != 144:
            raise ValueError("Full domain identity/count collision")
        for original, revised in zip(old, current, strict=True):
            for field in (
                "group_id",
                "construction_role",
                "family_cluster_id",
                "pre_candidate_lock_utc",
            ):
                if original[field] != revised[field]:
                    raise ValueError(f"Frozen group/role/family/path changed: {field}")
        scope_ids = set()
        for item in triage["domains"][domain]["items"]:
            ident = item["blind_review_id"]
            scope_ids.add(ident)
            recipe = recipes.get(ident)
            if recipe is None:
                if item["different_fields"] != ["text_naturalness"] or {
                    item["r3"]["text_naturalness"],
                    item["r4"]["text_naturalness"],
                } != {"NATURAL", "MINOR_ISSUE"}:
                    raise ValueError(
                        f"Missing explicit non-naturalness disposition: {ident}"
                    )
                reason = "核心对象、范围与条件已明确；没有多解指代或选文操作旁白。纯 NATURAL/MINOR_ISSUE 表达偏好依 Owner 冻结默认原则非阻断，原值保留、不修不复审。"
                if ident == "CBR-48A10389C909A0":
                    reason += "主题相关不等于公布机关相同，是自然机关身份关系；不是本次选文或审读操作指令。"
                recipe = {
                    "classes": ["NATURALNESS_NONBLOCKING"],
                    "reason": reason,
                    "scope": "NONE",
                }
            overlay.append(
                {
                    "domain": domain,
                    "blind_review_id": ident,
                    "original_candidate": item["candidate_text"],
                    "disputed_fields": item["different_fields"],
                    "r3": item["r3"],
                    "r4": item["r4"],
                    "owner_primary_defect_class": recipe["classes"][0],
                    "owner_defect_classes": recipe["classes"],
                    "owner_decision": "REPAIR"
                    if ident in changed
                    else "NONBLOCKING_VARIANCE",
                    "repair_required": ident in changed,
                    "repair_reason": recipe["reason"],
                    "allowed_repair_scope": recipe["scope"],
                    "targeted_rereview_required": ident in changed,
                    "decision_authority": "CURRENT_OWNER_DIRECTIVE_DEFAULTS_APPLIED_BY_CONTROL_PLANE",
                    "not_an_owner_vote_or_final_annotation": True,
                }
            )
        for ident in sorted(changed - scope_ids):
            supplementary.append(
                {
                    "domain": domain,
                    "old_id": ident,
                    **recipes[ident],
                    "basis": "AUTHORIZED_FULL_DOMAIN_ROLE_CONDITIONED_AUDIT",
                }
            )
        sources = load_sources(baseline / domain.lower())
        paths = parse((base / "evidence_path_and_query_contract.json").read_bytes())
        paths_by_group = {p["group_id"]: p for p in paths}
        evidence_checks = []
        for path in paths:
            for unit in path["frozen_evidence_units"]:
                source = sources[unit["doc"]]
                if (
                    source["raw_sha256"] != unit["snapshot_sha256"]
                    or source["text_sha256"] != unit["text_sha256"]
                ):
                    raise ValueError("Source identity mismatch")
                for anchor in unit["anchors"]:
                    if normalized(anchor) not in normalized(source["text"]):
                        raise ValueError(
                            f"Missing evidence anchor: {unit['doc']}: {anchor}"
                        )
                evidence_checks.append(
                    {
                        "group": path["group_id"],
                        "doc": unit["doc"],
                        "raw_sha256": source["raw_sha256"],
                        "anchors_present": True,
                    }
                )
        lineage = []
        for row in old:
            ident = row["blind_review_id"]
            if ident not in changed:
                continue
            witnesses = []
            for doc, *anchors in CONTEXT_WITNESSES[domain].get(ident, []):
                source = sources[doc]
                if doc not in {
                    u["doc"]
                    for u in paths_by_group[row["group_id"]]["frozen_evidence_units"]
                }:
                    raise ValueError("Context expansion outside frozen group evidence")
                for anchor in anchors:
                    offset = normalized(source["text"]).find(normalized(anchor))
                    if offset < 0:
                        raise ValueError(f"Context witness absent: {doc}: {anchor}")
                    witnesses.append(
                        {
                            "doc": doc,
                            "anchor": anchor,
                            "normalized_offset": offset,
                            "raw_sha256": source["raw_sha256"],
                            "text_sha256": source["text_sha256"],
                        }
                    )
            lineage.append(
                {
                    "old_id": ident,
                    "new_id": by_old[ident]["blind_review_id"],
                    "old_sample_id": row["sample_id"],
                    "new_sample_id": by_old[ident]["sample_id"],
                    "group_id": row["group_id"],
                    "old_text": row["candidate_text"],
                    "new_text": recipes[ident]["text"],
                    "classes": recipes[ident]["classes"],
                    "reason": recipes[ident]["reason"],
                    "frozen_evidence_path": paths_by_group[row["group_id"]],
                    "scope_expansion_witnesses": witnesses,
                    "semantic_review": "EXPLICIT_AUTHOR_ATOM_EQUIVALENCE_REVIEW_EXTERNAL_TARGETED_PENDING",
                    "evidence_path_changed": False,
                    "factual_core_changed": False,
                    "independent_fact_added": False,
                }
            )
        atom_audit = parse((base / "fact_atom_audit.json").read_bytes())
        if atom_audit["blockers"]:
            raise ValueError("Frozen atom blockers must not be silently repaired")
        atom_rows = []
        for atom in atom_audit["records"]:
            matching = [
                r
                for r in old
                if r["group_id"].endswith(atom["group"])
                and ROLE_CODE[r["construction_role"]] == atom["role"]
            ]
            if len(matching) != 1 or atom["status"] not in (
                "SUPPORTED",
                "CONTROLLED_POISON",
            ):
                raise ValueError("Atom coverage or status gap")
            original = matching[0]
            revised = by_old[original["blind_review_id"]]
            atom_rows.append(
                {
                    "immutable_atom": atom,
                    "current_sample_id": revised["sample_id"],
                    "current_text_sha256": hashlib.sha256(
                        revised["candidate_text"].encode()
                    ).hexdigest(),
                    "same_atomic_claim_and_controlled_root": True,
                    "basis": "AUTHORIZED_SCOPE_RESTORATION"
                    if original["blind_review_id"] in changed
                    else "BYTE_IDENTICAL_TEXT_INHERITANCE",
                }
            )
        derivations = []
        for path in paths:
            poison = next(
                r
                for r in current
                if r["group_id"] == path["group_id"]
                and r["construction_role"] == "POISON"
            )
            atoms = [
                a["immutable_atom"]
                for a in atom_rows
                if a["current_sample_id"] == poison["sample_id"]
            ]
            roots = {
                a.get(
                    "controlled_root", a.get("declaration", {}).get("controlled_root")
                )
                for a in atoms
                if a["status"] == "CONTROLLED_POISON"
            }
            if len(roots) != 1 or None in roots:
                raise ValueError("Poison does not have exactly one corruption root")
            proof = path["derivation"]["full_source_ablation"]
            derived, minimum, asserted = derive_path(atoms, proof)
            if derived != path["derivation"]["target"]:
                raise ValueError("Evidence path changed derived S")
            if path["group_id"] == "F240-D3-HKP2-S1-C2":
                if "同一人已有这样的替代验证方式" not in poison["candidate_text"]:
                    raise ValueError("Same-condition hard semantic repair absent")
            derivations.append(
                {
                    "group_id": path["group_id"],
                    "current_poison_id": poison["blind_review_id"],
                    "derived": derived,
                    "minimum_external_evidence_after": minimum,
                    "unchanged_target": path["derivation"]["target"],
                    "proof": proof,
                    "same_field_incompatible_assertions": {
                        k: sorted(v) for k, v in asserted.items() if len(v) > 1
                    },
                    "review_basis": "AUTHOR_REASSESSMENT_OF_SAME_ATOMS_AND_MINIMUM_PATH_NOT_REVIEWER_VALUE_OVERRIDE",
                    "external_semantic_review_pending": True,
                }
            )
        before_surface, after_surface = surface(old), surface(current)
        permitted_scope = {"CBR-74A497B5718803"} if domain == "D2" else set()
        after_surface["explicit_scope_dispositions"] = [
            {
                "id": ident,
                "class": "VALID_SCOPE_DIFFERENCE",
                "decision": "KEEP_UNCHANGED",
                "reason": "Different payment regimes do not establish a wholesale replacement from dates alone. An epistemic scope qualification, not an instruction for selecting this comparison. One isolated occurrence is not the repeated role-exclusive identity-admonition family.",
            }
            for ident in sorted(permitted_scope)
        ]
        remaining = sum(
            len(set(ids) - permitted_scope)
            for f in after_surface["semantic_families"]
            if f["family"] != "same_subject_transition"
            for ids in f["ids_by_role"].values()
        )
        if remaining:
            raise ValueError("Known exogenous narration remains after repair")
        parity = []
        for group in paths_by_group:
            rows = [r for r in current if r["group_id"] == group]
            metrics = {
                r["construction_role"]: measures(r["candidate_text"]) for r in rows
            }
            sizes = [v["characters"] for v in metrics.values()]
            ratio = max(sizes) / min(sizes)
            parity.append(
                {
                    "group": group,
                    "metrics": metrics,
                    "length_ratio": ratio,
                    "construction_author_scope_review": "NO_EXOGENOUS_ROLE_TEMPLATE_AFTER_REPAIR",
                    "length_review_required": ratio > 1.4,
                }
            )
        if any(p["length_review_required"] for p in parity):
            raise ValueError("Triplet length review remains required")
        readiness = parse((base / "view_candidate_claim_readiness.json").read_bytes())
        primary = parse((base / "view_primary_readiness.json").read_bytes())
        sample_map = {
            r["sample_id"]: revised["sample_id"]
            for r, revised in zip(old, current, strict=True)
        }
        for record in readiness + primary:
            record["sample_id"] = sample_map[record["sample_id"]]
            if record.get("view") == "E" and "entity_claim_ir" in record:
                record["entity_claim_ir"] = [
                    a
                    for a in atom_rows
                    if a["current_sample_id"] == record["sample_id"]
                ]
        missingness = {
            role: {
                view: dict(
                    Counter(
                        r["status"]
                        for r in readiness
                        if r["construction_role"] == role and r["view"] == view
                    )
                )
                for view in "SEPTR"
            }
            for role in ROLES
        }
        query_checks = [
            {
                "group_id": p["group_id"],
                "query": p["neutral_query"],
                "C_P_H_shared": p["query_shared_C_P_H"],
                "hidden_control_token_leakage": bool(
                    re.search(
                        r"CBR-|HKP[1-4]|S[123]|POISON|HARD_NEGATIVE|Expected|ground_truth",
                        p["neutral_query"],
                    )
                ),
                "query_unchanged": True,
            }
            for p in paths
        ]
        if any(
            q["hidden_control_token_leakage"] or not q["C_P_H_shared"]
            for q in query_checks
        ):
            raise ValueError("Query isolation failed")
        folder = output / "private" / domain
        write_new(
            folder / f"candidate_corpus_v{plan.get('candidate_version', 2)}.jsonl",
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in current),
            text=True,
        )
        write_new(folder / "OLD_TO_NEW_LINEAGE_V1.json", lineage)
        write_new(
            folder / "FULL_DOMAIN_FACT_ATOM_AUDIT_V2.json",
            {
                "records": atom_rows,
                "derivations": derivations,
                "semantic_atom_count_changed": 0,
                "automatic_entailment_claimed": False,
                "external_targeted_pending": True,
            },
        )
        write_new(
            folder / "SURFACE_AUDIT_BEFORE_AFTER_V2.json",
            {
                "before": before_surface,
                "after": after_surface,
                "bounded_author_shortcut_audit": "PASS_KNOWN_EXOGENOUS_FAMILIES_REMOVED",
                "all_possible_shortcuts_ruled_out": False,
            },
        )
        write_new(folder / "FULL_DOMAIN_TRIPLET_PARITY_V2.json", parity)
        write_new(
            folder / "FULL_DOMAIN_READINESS_V2.json",
            {
                "primary": primary,
                "candidate_claim": readiness,
                "observability_only_not_signal_implementation": True,
                "optional_metadata_unknowns": parse(
                    (base / "metadata_unknowns.json").read_bytes()
                ),
            },
        )
        write_new(
            folder / "FULL_DOMAIN_MISSINGNESS_QUERY_FAMILY_V2.json",
            {
                "missingness_by_role": missingness,
                "primary": parse((base / "missingness_by_role.json").read_bytes())[
                    "rows"
                ],
                "query_audit": query_checks,
                "family_integrity": parse(
                    (base / "family_cluster_audit.json").read_bytes()
                ),
                "new_missing_inputs": 0,
                "split_executed": False,
            },
        )
        write_new(folder / "FROZEN_EVIDENCE_RECHECK_V1.json", evidence_checks)
        write_new(
            folder / "CANDIDATE_VISIBLE_AUTHOR_QA_V1.json",
            [
                {
                    "id": r["blind_review_id"],
                    "old_id": old_r["blind_review_id"],
                    "scope": "AUTHOR_CONSTRUCTION_RECHECK_NOT_EXTERNAL_ANNOTATION",
                    "self_containment_rechecked": True,
                    "referent_uniqueness_rechecked": True,
                    "material_naturalness_defect_found": False,
                    "external_targeted_required": old_r["blind_review_id"] in changed,
                }
                for old_r, r in zip(old, current, strict=True)
            ],
        )
        for reviewer in ("R3_GPT", "R4_CODEX"):
            reviewer_base = base / "reviewer"
            original_packet = parse(
                (
                    reviewer_base
                    / f"PAPER1_CORE144_{domain}_{reviewer}_PHASE1_PACKAGE_V1.json"
                ).read_bytes()
            )
            packet = [
                {
                    "blind_review_id": by_old[r["blind_review_id"]]["blind_review_id"],
                    "candidate_text": by_old[r["blind_review_id"]]["candidate_text"],
                }
                for r in original_packet
                if r["blind_review_id"] in changed
            ]
            if len(packet) != len(changed) or any(
                set(r) != {"blind_review_id", "candidate_text"} for r in packet
            ):
                raise ValueError("Targeted package scope/fields failed")
            dest = output / "reviewers" / domain / reviewer
            package_path = (
                dest
                / f"PAPER1_CORE144_{domain}_{reviewer}_TARGETED_PHASE1_PACKAGE_V1.json"
            )
            schema_path = (
                dest / f"PAPER1_CORE144_{domain}_TARGETED_PHASE1_IMPORT_SCHEMA_V1.json"
            )
            prompt_path = (
                dest
                / f"PAPER1_CORE144_{domain}_{reviewer}_TARGETED_PHASE1_PROMPT_V1.md"
            )
            schema = parse(
                (
                    reviewer_base
                    / f"PAPER1_CORE144_{domain}_PHASE1_IMPORT_SCHEMA_V1.json"
                ).read_bytes()
            )
            schema["record_count"] = len(packet)
            write_new(package_path, packet)
            write_new(schema_path, schema)
            write_new(prompt_path, prompt(domain, reviewer, len(packet)), text=True)
            if set(r["blind_review_id"] for r in packet) & set(by_old):
                raise ValueError("Old identities leaked into targeted package")
            package_manifest.append(
                {
                    "domain": domain,
                    "reviewer": reviewer,
                    "actual_provider": "GPT" if reviewer == "R3_GPT" else "DOUBAO",
                    "records": len(packet),
                    "package": str(package_path.relative_to(output)),
                    "package_sha256": sha(package_path),
                    "schema": str(schema_path.relative_to(output)),
                    "prompt": str(prompt_path.relative_to(output)),
                    "same_original_domain_session_required": True,
                    "hidden_fields": 0,
                    "return_received": False,
                }
            )
        summary[domain] = {
            "scope": len(scope_ids),
            "changed": len(changed),
            "changed_in_62": len(changed & scope_ids),
            "supplementary_changed": len(changed - scope_ids),
            "naturalness_nonblocking": len(scope_ids - changed),
            "hard_semantic": sum(
                "HARD_SEMANTIC_BLOCKER" in r["classes"] for r in recipes.values()
            ),
            "self_containment_ids": sorted(
                k
                for k, r in recipes.items()
                if "SELF_CONTAINMENT_BLOCKER" in r["classes"]
            ),
            "surface_ids": sorted(
                k for k, r in recipes.items() if "SURFACE_TEMPLATE_RISK" in r["classes"]
            ),
            "current_rows": len(current),
            "groups": len(paths),
            "roles": dict(Counter(r["construction_role"] for r in current)),
            "fact_status_counts": dict(
                Counter(a["immutable_atom"]["status"] for a in atom_rows)
            ),
            "max_length_ratio": max(p["length_ratio"] for p in parity),
            "phase1_accepted": False,
            "phase2_release_allowed": False,
            "targeted_review_pending": True,
        }
    if len(overlay) != 62:
        raise ValueError("Owner review scope must remain exactly 62")
    if any(sha(repo / name) != digest for name, digest in before.items()):
        raise ValueError("Immutable input changed during execution")
    write_new(
        output / "private/PAPER1_CORE144_D2_D3_PHASE1_OWNER_TRIAGE_OVERLAY_V1.json",
        {
            "records": overlay,
            "supplementary_full_domain_surface_cases": supplementary,
            "raw_overridden": False,
            "summary": summary,
        },
    )
    table = [
        "# Owner Phase1 triage — V1\n",
        "依据本轮 Owner 冻结默认原则逐条执行，不是人工最终标签或按票选择。原 raw 不改。\n",
        "| Domain | old ID | primary class | decision | reason |",
        "|---|---|---|---|---|",
    ]
    table += [
        f"| {r['domain']} | {r['blind_review_id']} | {r['owner_primary_defect_class']} | {r['owner_decision']} | {r['repair_reason']} |"
        for r in overlay
    ]
    table += ["\n## Full-domain supplemental cases\n"] + [
        f"- {r['domain']} / {r['old_id']}: {r['reason']}" for r in supplementary
    ]
    write_new(
        output / "private/PAPER1_CORE144_D2_D3_PHASE1_OWNER_TRIAGE_RECORD_V1.md",
        "\n".join(table) + "\n",
        text=True,
    )
    write_new(
        output / "RAW_PRESERVATION_AND_INPUT_MANIFEST_V1.json",
        {
            "input_hashes": before,
            "raw_revalidation": raw_checks,
            "original_session_isolation": "OWNER_ATTESTED_NOT_MACHINE_PROVEN",
            "immutable_inputs_after_check": True,
        },
    )
    write_new(
        output / "TARGETED_SEND_MANIFEST_V1.json",
        {
            "packages": package_manifest,
            "new_sessions_required": False,
            "domain_sessions_must_not_mix": True,
            "phase2_withheld": True,
        },
    )
    write_new(
        output / "GATE_AND_SUMMARY_V1.json",
        {
            "summary": summary,
            "unresolved_owner_choice": 0,
            "external_targeted_pending": 4,
            "phase2_withheld": True,
            "status": "STOP_EXTERNAL_TARGETED_REVIEW_REQUIRED",
            "no_gt_split_training_expected_model_feedback": True,
        },
    )
    index = {
        str(p.relative_to(output)): {"sha256": sha(p), "bytes": p.stat().st_size}
        for p in sorted(output.rglob("*"))
        if p.is_file()
    }
    write_new(
        output / "FINAL_EVIDENCE_INDEX_V1.json",
        {"files": index, "count": len(index), "task_id": plan["task_id"]},
    )
    for path in output.rglob("*"):
        if path.is_file():
            os.chmod(path, 0o444)
    return {
        "summary": summary,
        "files": len(index) + 1,
        "index_sha256": sha(output / "FINAL_EVIDENCE_INDEX_V1.json"),
        "status": "STOP_EXTERNAL_TARGETED_REVIEW_REQUIRED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            run(args.repo.resolve(), args.plan.resolve(), args.output.resolve()),
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
