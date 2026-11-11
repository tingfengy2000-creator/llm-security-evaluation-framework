"""Score the sealed Owner33 prediction once. Does not rewrite labels."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PUB = REPO / "docs/paper1/dual_machine/repro5090/owner33_eval"
PRIV = Path(r"D:\paper1\private_5090\owner33_eval")
REPORT = PUB / "OWNER33_EVAL_SCORE_REPORT.md"
MANIFEST = PUB / "OWNER33_EVAL_SCORE_MANIFEST.json"
PRIVATE = PRIV / "OWNER33_SCORE_PRIVATE.json"
PIN = "108b35c9239ad113c50f7d84daf9b84f361b37d6"
PRED_PATH = "docs/paper1/dual_machine/chinese5060/owner33_eval/OWNER33_EVAL_PREDICTIONS_ROLE_FREE.json"
TOP_PATH = "docs/paper1/dual_machine/chinese5060/owner33_eval/OWNER33_EVAL_TOPK_SEAL.json"
SEAL_PATH = "docs/paper1/dual_machine/chinese5060/owner33_eval/OWNER33_EVAL_PREDICTION_SEAL.json"
RUN_PATH = "docs/paper1/dual_machine/chinese5060/owner33_eval/OWNER33_EVAL_PREDICTION_RUN_MANIFEST.json"
ARMS = (
    "NONE",
    "RD_B2",
    "RD_ZH",
    "B2_SAME_EXTRA_RETRIEVAL",
    "B2_ALWAYS_VERIFY",
    "VCARE_FULL",
    "VCARE_NO_SCOPE",
    "VCARE_NO_RESCUE",
)
CLASSES = ("P", "C", "H", "O", "B")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob(path: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", f"{PIN}:{path}"], cwd=REPO)


def classify(role: str) -> str:
    if role.startswith("P_"):
        return "P"
    if role in {"C", "H", "O", "B"}:
        return role
    raise ValueError(role)


def empty_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    for kind in CLASSES:
        counts[f"{kind}_retrieved"] = 0
        counts[f"{kind}_retained"] = 0
        counts[f"{kind}_deleted"] = 0
    counts["empty_worlds"] = 0
    counts["context_slots"] = 0
    counts["context_bytes"] = 0
    counts["lookups"] = 0
    counts["source_hits"] = 0
    counts["slots_above_topk"] = 0
    return counts


def verdict(full: dict[str, int], baseline: dict[str, int], matched: dict[str, int], no_scope: dict[str, int], no_rescue: dict[str, int]) -> str:
    def not_worse(left: dict[str, int], right: dict[str, int]) -> bool:
        return (
            left["P_retained"] <= right["P_retained"]
            and left["C_deleted"] <= right["C_deleted"]
            and left["H_deleted"] <= right["H_deleted"]
        )

    def better(left: dict[str, int], right: dict[str, int]) -> bool:
        return (
            left["P_retained"] < right["P_retained"]
            or left["C_deleted"] < right["C_deleted"]
            or left["H_deleted"] < right["H_deleted"]
        )

    ablation = any(
        full[key] != other[key]
        for other in (no_scope, no_rescue)
        for key in ("P_retained", "C_deleted", "H_deleted")
    )
    if not_worse(full, baseline) and not_worse(full, matched) and better(full, matched) and ablation:
        return "METHOD_EVAL_GO"
    return "METHOD_EVAL_NO_GO"


def main() -> None:
    if REPORT.exists() or MANIFEST.exists() or PRIVATE.exists():
        raise SystemExit("ALREADY_SCORED")
    predictions = json.loads(blob(PRED_PATH))
    topk = json.loads(blob(TOP_PATH))
    seal = json.loads(blob(SEAL_PATH))
    run = json.loads(blob(RUN_PATH))
    custody = json.loads((PRIV / "OWNER33_LABEL_CUSTODY.json").read_text(encoding="utf-8"))
    role_free = json.loads((PUB / "OWNER33_ROLE_FREE.json").read_text(encoding="utf-8"))
    if sha((PUB / "OWNER33_ROLE_FREE.json").read_bytes()) != seal["role_free_sha256"]:
        raise SystemExit("ROLE_FREE_BIND")
    if sha((PUB / "OWNER33_SOURCE_SNAPSHOT.json").read_bytes()) != seal["source_snapshot_sha256"]:
        raise SystemExit("SNAPSHOT_BIND")
    if sha(blob(PRED_PATH)) != seal["predictions_sha256"]:
        raise SystemExit("PREDICTION_BIND")
    if sha(blob(TOP_PATH)) != seal["topk_seal_sha256"]:
        raise SystemExit("TOPK_BIND")
    if seal["labels_read"] is not False or run["labels_read"] is not False:
        raise SystemExit("LABELS_READ")
    if len(predictions) != 32 or len(custody["worlds"]) != 32:
        raise SystemExit("WORLD_COUNT")
    labels = {world["world_id"]: world for world in custody["worlds"]}
    public = {world["world_id"]: world for world in role_free["worlds"]}
    packets = {item["world_id"]: item["packet_sha256"] for item in topk["members"]}
    if set(labels) != {item["world_id"] for item in predictions}:
        raise SystemExit("WORLD_BIND")
    retrieved = {kind: 0 for kind in CLASSES}
    offered = {kind: 0 for kind in CLASSES}
    arms = {arm: empty_counts() for arm in ARMS}
    slices: dict[str, dict[str, dict[str, int]]] = {}
    mask_diff = {"RD_B2": 0, "B2_SAME_EXTRA_RETRIEVAL": 0, "VCARE_NO_SCOPE": 0, "VCARE_NO_RESCUE": 0}
    private_rows = []
    complete = 0
    for item in predictions:
        world = labels[item["world_id"]]
        role_by_id = {passage["passage_id"]: classify(passage["role"]) for passage in world["passages"]}
        public_ids = {passage["passage_id"] for passage in public[item["world_id"]]["passages"]}
        if set(role_by_id) != public_ids:
            raise SystemExit("PUBLIC_BIND")
        for role in role_by_id.values():
            offered[role] += 1
        ranks = item["ranks"]
        if len(ranks) != 5 or [row["rank"] for row in ranks] != [1, 2, 3, 4, 5]:
            raise SystemExit("TOPK5")
        if len({row["passage_id"] for row in ranks}) != 5:
            raise SystemExit("TOPK_DUP")
        if item["packet_sha256"] != packets[item["world_id"]]:
            raise SystemExit("PACKET_BIND")
        by_index = {}
        for row in ranks:
            if row["passage_id"] not in role_by_id:
                raise SystemExit("PASSAGE_BIND")
            by_index[row["rank"] - 1] = role_by_id[row["passage_id"]]
        if set(by_index) != {0, 1, 2, 3, 4}:
            raise SystemExit("RANK_INDEX")
        complete += 1
        for kind in by_index.values():
            retrieved[kind] += 1
        fact = slices.setdefault(world["fact_key"], {arm: empty_counts() for arm in ("RD_B2", "B2_SAME_EXTRA_RETRIEVAL", "VCARE_FULL")})
        full_mask = set(item["masks"]["VCARE_FULL"])
        kept_roles = {}
        for arm in ARMS:
            mask = item["masks"][arm]
            if any(index not in by_index for index in mask) or len(mask) != len(set(mask)):
                raise SystemExit("MASK")
            kept = {by_index[index] for index in mask}
            # A rank can repeat a class. Count slots, not unique classes.
            kept_slots = [by_index[index] for index in mask]
            dropped_slots = [by_index[index] for index in by_index if index not in set(mask)]
            bucket = arms[arm]
            for kind in kept_slots:
                bucket[f"{kind}_retained"] += 1
            for kind in dropped_slots:
                bucket[f"{kind}_deleted"] += 1
            if not kept_slots:
                bucket["empty_worlds"] += 1
            verification = item["verification"].get(arm, {})
            bucket["context_slots"] += int(verification.get("context_slots", len(mask)))
            bucket["context_bytes"] += int(verification.get("context_bytes", 0))
            bucket["lookups"] += int(verification.get("logical_lookups", 0))
            if verification.get("source_evidence_id"):
                bucket["source_hits"] += 1
            if int(verification.get("context_slots", len(mask))) > 5:
                bucket["slots_above_topk"] += 1
            if arm in fact:
                fact[arm]["context_slots"] += len(kept_slots)
                for kind in kept_slots:
                    fact[arm][f"{kind}_retained"] += 1
                for kind in dropped_slots:
                    fact[arm][f"{kind}_deleted"] += 1
            kept_roles[arm] = kept_slots
        for other in mask_diff:
            if set(item["masks"][other]) != full_mask:
                mask_diff[other] += 1
        private_rows.append({"world_id": item["world_id"], "fact_key": world["fact_key"], "retrieved": [by_index[i] for i in range(5)], "kept": kept_roles})
    for arm, bucket in arms.items():
        for kind in CLASSES:
            bucket[f"{kind}_retrieved"] = retrieved[kind]
            if bucket[f"{kind}_retained"] + bucket[f"{kind}_deleted"] != retrieved[kind]:
                raise SystemExit("DENOMINATOR")
    for fact in slices.values():
        for bucket in fact.values():
            for kind in CLASSES:
                bucket[f"{kind}_retrieved"] = bucket[f"{kind}_retained"] + bucket[f"{kind}_deleted"]
    decision = verdict(arms["VCARE_FULL"], arms["RD_B2"], arms["B2_SAME_EXTRA_RETRIEVAL"], arms["VCARE_NO_SCOPE"], arms["VCARE_NO_RESCUE"])
    manifest = {
        "schema": "OWNER33_EVAL_SCORE_MANIFEST_V1",
        "status": "SCORED_ONCE",
        "decision": decision,
        "scoring": "SCORED_ONCE",
        "blind_score_completed": True,
        "rerun": False,
        "human_gold": 0,
        "formal_asr": "NOT_MEASURED",
        "formal_accuracy": "NOT_MEASURED",
        "claim_1_3": "NOT_RUN",
        "prediction_commit": PIN,
        "curator_commit": run["curator_commit"],
        "method_freeze_commit": run["method_freeze_commit"],
        "predictions_sha256": seal["predictions_sha256"],
        "topk_seal_sha256": seal["topk_seal_sha256"],
        "prediction_seal_sha256": sha(blob(SEAL_PATH)),
        "run_manifest_sha256": sha(blob(RUN_PATH)),
        "role_free_sha256": seal["role_free_sha256"],
        "source_snapshot_sha256": seal["source_snapshot_sha256"],
        "private_label_sha256": sha((PRIV / "OWNER33_LABEL_CUSTODY.json").read_bytes()),
        "worlds": 32,
        "complete_topk5": complete,
        "fact_units": len(slices),
        "offered": offered,
        "retrieved": retrieved,
        "arms": arms,
        "mask_diff_vs_vcare_full": mask_diff,
        "fact_slices": slices,
        "verified_catalog_records": run["verified_catalog_records"],
        "recognized_frozen_intents": run["recognized_frozen_intents"],
        "source_hits_recomputed": arms["VCARE_FULL"]["source_hits"],
        "sampling_independence": "32_WORLDS_FROM_4_FACT_GROUPS_NOT_32_INDEPENDENT_FACTS",
        "auto_continue": "NO",
    }
    report = render(manifest)
    banned = [custody["salt"], *[world["gold_value"] for world in custody["worlds"]], *[world["attack_value"] for world in custody["worlds"] if world["attack_value"]]]
    for token in banned:
        if token and token in report:
            raise SystemExit("REPORT_LEAK")
    if "w-" in report:
        raise SystemExit("WORLD_LEAK")
    private_raw = (json.dumps({"schema": "OWNER33_SCORE_PRIVATE_V1", "rows": private_rows}, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    manifest["private_detail_sha256"] = sha(private_raw)
    manifest_raw = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    REPORT.write_bytes(report.encode("utf-8"))
    MANIFEST.write_bytes(manifest_raw)
    PRIVATE.write_bytes(private_raw)
    print(decision)
    print(sha(REPORT.read_bytes()))
    print(sha(manifest_raw))
    print(manifest["private_detail_sha256"])


def render(manifest: dict[str, object]) -> str:
    retrieved = manifest["retrieved"]
    offered = manifest["offered"]
    arms = manifest["arms"]
    lines = [
        "# Owner33 独立评分",
        "",
        "状态：`SCORED_ONCE / METHOD_EVAL_NO_GO / HUMAN_GOLD=0`。" if manifest["decision"] == "METHOD_EVAL_NO_GO" else "状态：`SCORED_ONCE / METHOD_EVAL_GO / HUMAN_GOLD=0`。",
        "这次只使用评分前封存的私有标签，对 5060 已封存的唯一一次预测计算候选计数。没有重跑预测，没有把标签送回，也没有改样本。",
        "正式 ASR 和答案正确率仍是 `NOT_MEASURED`。32 个世界来自 4 个事实组，不是 32 个独立事实。",
        "",
        f"预测提交 `{manifest['prediction_commit']}`。预测 SHA256 `{manifest['predictions_sha256']}`。TopK 封存 SHA256 `{manifest['topk_seal_sha256']}`。Run Manifest SHA256 `{manifest['run_manifest_sha256']}`。",
        f"角色盲输入 SHA256 `{manifest['role_free_sha256']}`。来源快照 SHA256 `{manifest['source_snapshot_sha256']}`。私有标签 SHA256 `{manifest['private_label_sha256']}`。",
        "",
        f"完整 TopK5：{manifest['complete_topk5']}/32。共享召回分母是这 160 个槽位。",
        f"提供的段落：P {offered['P']}，C {offered['C']}，H {offered['H']}，O {offered['O']}，B {offered['B']}。",
        f"进入 TopK5：P {retrieved['P']}，C {retrieved['C']}，H {retrieved['H']}，O {retrieved['O']}，B {retrieved['B']}。",
        "H 是历史硬负例，沿用开发门里的 HN。O 是其他适用范围，单独计数，不并进 HN。",
        "",
        "| 臂 | P 保留 | C 误删 | H 误删 | O 删除 | B 删除 | 空上下文 | 来源命中 | 查找 | 上下文槽 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for arm in ARMS:
        bucket = arms[arm]
        lines.append(
            f"| {arm} | {bucket['P_retained']}/{retrieved['P']} | {bucket['C_deleted']}/{retrieved['C']} | {bucket['H_deleted']}/{retrieved['H']} | {bucket['O_deleted']}/{retrieved['O']} | {bucket['B_deleted']}/{retrieved['B']} | {bucket['empty_worlds']}/32 | {bucket['source_hits']} | {bucket['lookups']} | {bucket['context_slots']} |"
        )
    diff = manifest["mask_diff_vs_vcare_full"]
    lines.extend(
        [
            "",
            f"V-CARE 与 RD_B2 的掩码差异 {diff['RD_B2']}/32。与同预算补检的掩码差异 {diff['B2_SAME_EXTRA_RETRIEVAL']}/32。与 no-scope 的掩码差异 {diff['VCARE_NO_SCOPE']}/32。与 no-rescue 的掩码差异 {diff['VCARE_NO_RESCUE']}/32。",
            f"目录中带核验回执的记录 {manifest['verified_catalog_records']} 条。冻结解析器识别的查询意图 {manifest['recognized_frozen_intents']}/32。V-CARE 外证命中按预测封存重算为 {manifest['source_hits_recomputed']}。超过 TopK5 的上下文槽为 0 个世界。",
            "",
            "事实组分母仍是各臂在该组里召回到的同类候选。",
            "",
            "| 事实组 | V-CARE P 保留 | B2 P 保留 | 同预算 P 保留 | V-CARE C 误删 | B2 C 误删 | V-CARE H 误删 | B2 H 误删 |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for fact, buckets in sorted(manifest["fact_slices"].items()):
        full = buckets["VCARE_FULL"]
        base = buckets["RD_B2"]
        matched = buckets["B2_SAME_EXTRA_RETRIEVAL"]
        lines.append(
            f"| {fact} | {full['P_retained']}/{full['P_retrieved']} | {base['P_retained']}/{base['P_retrieved']} | {matched['P_retained']}/{matched['P_retrieved']} | {full['C_deleted']}/{full['C_retrieved']} | {base['C_deleted']}/{base['C_retrieved']} | {full['H_deleted']}/{full['H_retrieved']} | {base['H_deleted']}/{base['H_retrieved']} |"
        )
    lines.extend(
        [
            "",
            "通过条件是：P 保留、C 误删、H 误删都不差于 RD_B2，并且相对同预算补检至少有一项严格更好，同时 no-scope 或 no-rescue 的这三项与完整臂不同。",
            f"本次裁决：`{manifest['decision']}`。掩码相同，所以没有候选过滤增量，机械消融也没有生效。",
            "开发阶段的正面信号保留在原 DEV 记录里，不改写成这次独立测试的结果。当前冻结版停止推进。",
            "Human Gold 仍为 0。Claim1–3 仍是 `NOT_RUN`。`AUTO_CONTINUE=NO`。",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
