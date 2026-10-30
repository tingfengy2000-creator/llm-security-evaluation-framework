"""Offline audit of the sealed FULL01 run. Does not load a model or write into the run."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.l0_full01_offline_audit import (  # noqa: E402
    EXPECTED,
    VALIDATION_PASSED,
    classify_output,
    displayed_model_verdict,
    pair_class,
    select_cases,
    sha_file,
)
from llmguard.domains.retrieval.hidden_poisoning.method_engineering.llm_verification import sha_text  # noqa: E402

TASK = "P1-L0-FULL01-SEALED-OUTPUT-AUDIT-01"
RUN_ID = "VACE-L0-D1-20261030-FULL01"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def index_run(root: Path) -> list[dict]:
    indexed = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        relative = path.relative_to(root)
        if set(relative.parts) & {"cache", "temp"}:
            continue
        indexed.append({"path": relative.as_posix(), "bytes": path.stat().st_size, "sha256": sha_file(path)})
    return indexed


def write_csv(path: Path, header: list[str], records: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header)
        writer.writeheader()
        writer.writerows(records)


def allowed_label(row: dict) -> tuple[str, str]:
    role = row["role_evaluation_only"]
    if role not in {"POISON", "CLEAN_CURRENT", "HARD_NEGATIVE"}:
        raise RuntimeError("AUDIT_ROLE_OUTSIDE_AUTHORIZED_LABELS")
    if role != "POISON":
        return role, "NOT_APPLICABLE"
    stratum = row["derived_s_evaluation_only"]
    if stratum not in {"S1", "S2", "S3"}:
        raise RuntimeError("AUDIT_POISON_STRATUM_OUTSIDE_AUTHORIZED_LABELS")
    return role, stratum


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    run = args.run_dir.resolve()
    out = args.out_dir.resolve()
    if out == run or run in out.parents or out in run.parents:
        raise RuntimeError("AUDIT_DIRECTORY_MUST_STAY_OUTSIDE_THE_SEALED_RUN")
    if out.exists() and any(out.iterdir()):
        raise RuntimeError("AUDIT_DIRECTORY_ALREADY_HAS_OUTPUT")
    identities = {
        "CONFIG_LOCK.json": EXPECTED["config_lock"],
        "L0_PREDICTIONS.jsonl": EXPECTED["predictions"],
        "PREDICTION_LOCK.json": EXPECTED["prediction_lock"],
    }
    for name, expected in identities.items():
        if sha_file(run / name) != expected:
            raise RuntimeError("FULL01_IDENTITY_MISMATCH:" + name)
    config = load_json(run / "CONFIG_LOCK.json")
    if config.get("git_head") != EXPECTED["execution_commit"]:
        raise RuntimeError("FULL01_EXECUTION_COMMIT_MISMATCH")
    lock = load_json(run / "PREDICTION_LOCK.json")
    if lock.get("rows") != 240 or lock.get("prediction_sha256") != EXPECTED["predictions"] or len(lock.get("raw") or {}) != 240:
        raise RuntimeError("FULL01_PREDICTION_LOCK_MISMATCH")
    for name, digest in lock["raw"].items():
        if sha_file(run / "raw" / name) != digest:
            raise RuntimeError("FULL01_RAW_HASH_MISMATCH:" + name)
    before = index_run(run)
    out.mkdir(parents=True)
    labels = {row["candidate_id"]: allowed_label(row) for row in rows(run / "input/evaluation/labels.jsonl")}
    if len(labels) != 120:
        raise RuntimeError("FULL01_LABEL_CARDINALITY")
    runtime = {}
    for condition, filename in (("L0-F5", "f5.jsonl"), ("L0-Oracle", "oracle.jsonl")):
        for row in rows(run / "input/runtime" / filename):
            runtime[(condition, row["candidate_id"])] = row
    audited = []
    for prediction in rows(run / "L0_PREDICTIONS.jsonl"):
        key = (prediction["condition"], prediction["candidate_id"])
        source = runtime[key]
        if sha_text(json.dumps(source, ensure_ascii=False, sort_keys=True)) != prediction["input_sha256"]:
            raise RuntimeError("FULL01_INPUT_IDENTITY_MISMATCH")
        if prediction["evidence_uids"] != [doc["uid"] for doc in source["evidence"]]:
            raise RuntimeError("FULL01_EVIDENCE_UID_MISMATCH")
        classified = classify_output(prediction["raw_output"], source)
        if classified["parser_error"] != prediction["error"] or classified["final_verdict"] != prediction["verdict"] or classified["model_verdict"] != prediction["model_verdict"]:
            raise RuntimeError("FULL01_SEALED_PARSE_MISMATCH")
        role, stratum = labels[prediction["candidate_id"]]
        audited.append({
            "candidate_id": prediction["candidate_id"], "condition": prediction["condition"], "role": role, "stratum": stratum,
            "model_verdict": displayed_model_verdict(classified["model_verdict"]), "final_verdict": classified["final_verdict"],
            "parser_error": classified["parser_error"], "primary_category": classified["primary_category"],
            "diagnostic_tags": classified["diagnostic_tags"], "model_called": prediction["model_called"],
            "input_rejected": prediction.get("error") == "INPUT_TOO_LONG" or not prediction["model_called"],
            "raw_output": prediction["raw_output"], "source_row": source,
        })
    if len(audited) != 240:
        raise RuntimeError("FULL01_AUDIT_DENOMINATOR")
    by_candidate: dict[str, dict[str, dict]] = {}
    for item in audited:
        by_candidate.setdefault(item["candidate_id"], {})[item["condition"]] = item
    if any(set(pair) != {"L0-F5", "L0-Oracle"} for pair in by_candidate.values()):
        raise RuntimeError("FULL01_PAIR_CARDINALITY")
    for pair in by_candidate.values():
        f5, oracle = pair["L0-F5"], pair["L0-Oracle"]
        kind = pair_class(f5["primary_category"] != VALIDATION_PASSED, oracle["primary_category"] != VALIDATION_PASSED, f5["final_verdict"], oracle["final_verdict"])
        f5["pair_class"] = oracle["pair_class"] = kind
    metrics = load_json(run / "L0_METRICS_AND_UNCERTAINTY.json")
    count_check = []
    for condition in ("L0-F5", "L0-Oracle"):
        subset = [item for item in audited if item["condition"] == condition]
        verdicts = Counter(item["final_verdict"] for item in subset)
        errors = Counter(item["parser_error"] for item in subset if item["parser_error"])
        sealed = metrics["metrics"][condition]
        count_check.append({
            "condition": condition, "rows": len(subset), "verdicts": dict(verdicts),
            "sealed_verdicts": sealed["verdict_counts"], "verdicts_match": dict(verdicts) == sealed["verdict_counts"],
            "parser_errors": dict(errors), "sealed_errors": sealed["errors"], "errors_match": dict(errors) == sealed["errors"],
            "input_rejected": sum(item["input_rejected"] for item in subset),
            "validation_failures": sum(item["primary_category"] != VALIDATION_PASSED for item in subset),
            "model_insufficient_without_error": sum(item["final_verdict"] == "INSUFFICIENT" and item["parser_error"] is None for item in subset),
        })
    if any(not item["verdicts_match"] or not item["errors_match"] for item in count_check):
        (out / "COUNT_DIFFERENCE.json").write_text(json.dumps(count_check, ensure_ascii=False, indent=2), encoding="utf-8")
    breakdown = Counter((item["condition"], item["role"], item["stratum"], item["primary_category"]) for item in audited if item["primary_category"] != VALIDATION_PASSED)
    write_csv(out / "VALIDATION_ERROR_BREAKDOWN.csv", ["condition", "role", "stratum", "primary_category", "n"], [
        {"condition": key[0], "role": key[1], "stratum": key[2], "primary_category": key[3], "n": value}
        for key, value in sorted(breakdown.items())
    ])
    transitions = Counter((item["condition"], item["role"], item["stratum"], item["model_verdict"], item["final_verdict"], item["primary_category"]) for item in audited)
    write_csv(out / "RAW_VERDICT_TRANSITIONS.csv", ["condition", "role", "stratum", "model_verdict", "final_verdict", "primary_category", "n", "score_status"], [
        {"condition": key[0], "role": key[1], "stratum": key[2], "model_verdict": key[3], "final_verdict": key[4], "primary_category": key[5], "n": value, "score_status": "RAW_VERDICT_DIAGNOSTIC"}
        for key, value in sorted(transitions.items())
    ])
    paired = Counter((item["pair_class"], by_candidate[item["candidate_id"]]["L0-F5"]["model_verdict"], by_candidate[item["candidate_id"]]["L0-F5"]["final_verdict"], by_candidate[item["candidate_id"]]["L0-Oracle"]["model_verdict"], by_candidate[item["candidate_id"]]["L0-Oracle"]["final_verdict"]) for item in audited if item["condition"] == "L0-F5")
    write_csv(out / "PAIRED_OUTCOME_TRANSITIONS.csv", ["pair_class", "f5_model_verdict", "f5_final_verdict", "oracle_model_verdict", "oracle_final_verdict", "n"], [
        {"pair_class": key[0], "f5_model_verdict": key[1], "f5_final_verdict": key[2], "oracle_model_verdict": key[3], "oracle_final_verdict": key[4], "n": value}
        for key, value in sorted(paired.items())
    ])
    public_rows = []
    for item in audited:
        public_rows.append({k: item[k] for k in ("candidate_id", "condition", "role", "stratum", "model_verdict", "final_verdict", "parser_error", "primary_category", "diagnostic_tags", "model_called", "input_rejected", "pair_class")})
    (out / "AUDIT_ROWS.jsonl").write_text("".join(json.dumps(item, ensure_ascii=False) + "\n" for item in public_rows), encoding="utf-8")
    chosen = select_cases(public_rows)
    private = []
    for item in chosen:
        full = next(row for row in audited if row["condition"] == item["condition"] and row["candidate_id"] == item["candidate_id"])
        private.append({
            "selection_rule": item["selection_rule"], "candidate_id": item["candidate_id"], "condition": item["condition"],
            "role": item["role"], "stratum": item["stratum"], "model_verdict": item["model_verdict"], "final_verdict": item["final_verdict"],
            "parser_error": item["parser_error"], "primary_category": item["primary_category"], "diagnostic_tags": item["diagnostic_tags"],
            "pair_class": item["pair_class"], "mechanical_confirmation": "PARSER_CATEGORY_REPLAYED_FROM_SEALED_OUTPUT",
            "author_semantic_judgment": None, "uncertain": None, "candidate_text": full["source_row"]["candidate_text"],
            "evidence": [{k: doc[k] for k in ("uid", "document_uid", "title", "text")} for doc in full["source_row"]["evidence"]],
            "raw_output": full["raw_output"],
        })
    (out / "PRIVATE_CASE_REVIEW.jsonl").write_text("".join(json.dumps(item, ensure_ascii=False) + "\n" for item in private), encoding="utf-8")
    after = index_run(run)
    integrity = {"before_files": len(before), "after_files": len(after), "unchanged": before == after, "run_dir_read_only": True}
    (out / "ORIGINAL_RUN_INTEGRITY_CHECK.json").write_text(json.dumps(integrity, ensure_ascii=False, indent=2), encoding="utf-8")
    if before != after:
        raise RuntimeError("FULL01_RUN_CHANGED_DURING_AUDIT")
    summary = render_summary(count_check, audited, by_candidate, chosen)
    (out / "AUDIT_SUMMARY.md").write_text(summary, encoding="utf-8")
    produced = sorted(p for p in out.iterdir() if p.is_file() and p.name != "EVIDENCE_INDEX.json")
    evidence = {"files": [{"path": path.name, "sha256": sha_file(path), "bytes": path.stat().st_size} for path in produced]}
    (out / "EVIDENCE_INDEX.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest = {
        "task": TASK, "run_id": RUN_ID, "status": "FULL01_OFFLINE_OUTPUT_AUDIT_COMPLETE / OWNER_REVIEW_REQUIRED",
        "result_commit": EXPECTED["result_commit"], "execution_commit": EXPECTED["execution_commit"],
        "config_lock_sha256": EXPECTED["config_lock"], "predictions_sha256": EXPECTED["predictions"],
        "prediction_lock_sha256": EXPECTED["prediction_lock"], "rows": 240, "count_check": count_check,
        "case_selection_rules": [item["selection_rule"] for item in chosen],
        "case_ids_private": [{"condition": item["condition"], "candidate_id": item["candidate_id"], "rule": item["selection_rule"]} for item in chosen],
        "raw_verdict_is_not_a_replacement_score": True, "no_model_call": True, "no_parser_or_prompt_change": True,
    }
    (out / "AUDIT_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    evidence["files"].append({"path": "AUDIT_MANIFEST.json", "sha256": sha_file(out / "AUDIT_MANIFEST.json"), "bytes": (out / "AUDIT_MANIFEST.json").stat().st_size})
    (out / "EVIDENCE_INDEX.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    final_index = index_run(run)
    if final_index != before:
        raise RuntimeError("FULL01_RUN_CHANGED_DURING_AUDIT")
    print("FULL01_OFFLINE_OUTPUT_AUDIT_COMPLETE / OWNER_REVIEW_REQUIRED")


def blocked(items: list[dict], role: str | set[str], model: str) -> int:
    roles = {role} if isinstance(role, str) else role
    return sum(item["role"] in roles and item["model_verdict"] == model and item["final_verdict"] == "INSUFFICIENT" and item["primary_category"] != VALIDATION_PASSED for item in items)


def render_summary(count_check: list[dict], audited: list[dict], pairs: dict[str, dict[str, dict]], chosen: list[dict]) -> str:
    failure_counts = Counter((item["condition"], item["primary_category"]) for item in audited if item["primary_category"] != VALIDATION_PASSED)
    tag_counts = Counter(tag for item in audited if item["primary_category"] == "QUOTE_NOT_IN_FROZEN_TEXT" for tag in item["diagnostic_tags"])
    pair_counts = Counter(item["pair_class"] for item in audited if item["condition"] == "L0-F5")
    poison_pairs = [pairs[key] for key in pairs if pairs[key]["L0-F5"]["role"] == "POISON"]
    oracle_recovers_poison = [pair for pair in poison_pairs if pair["L0-F5"]["final_verdict"] != "CONTRADICT" and pair["L0-Oracle"]["final_verdict"] == "CONTRADICT"]
    recover_with_f5_failure = sum(pair["L0-F5"]["primary_category"] != VALIDATION_PASSED for pair in oracle_recovers_poison)
    passed_poison_support = sum(item["primary_category"] == VALIDATION_PASSED and item["role"] == "POISON" and item["final_verdict"] == "SUPPORT" for item in audited)
    passed_clean_contradict = sum(item["primary_category"] == VALIDATION_PASSED and item["role"] == "CLEAN_CURRENT" and item["final_verdict"] == "CONTRADICT" for item in audited)
    passed_hn_contradict = sum(item["primary_category"] == VALIDATION_PASSED and item["role"] == "HARD_NEGATIVE" and item["final_verdict"] == "CONTRADICT" for item in audited)
    lines = [
        "# FULL01 离线输出归因",
        "",
        "任务 P1-L0-FULL01-SEALED-OUTPUT-AUDIT-01。没有重新推理，没有修改 parser，也没有替换 FULL01 指标。",
        "引用前的 model_verdict 只记为 RAW_VERDICT_DIAGNOSTIC，不是新的有效分数。",
        "",
        "## 1. 计数和身份",
        "",
    ]
    for item in count_check:
        lines.append(
            f"{item['condition']}：{item['rows']} 条，判决 {item['verdicts']}，与封存指标一致：{item['verdicts_match']}。"
            f"parser 错误 {item['parser_errors']}，与封存指标一致：{item['errors_match']}。"
            f"输入拒绝 {item['input_rejected']}。输出失败 {item['validation_failures']}。无输出错误的模型 INSUFFICIENT {item['model_insufficient_without_error']}。"
        )
    lines.extend(["", "## 2. 输出失败主分类", ""])
    for key, value in sorted(failure_counts.items()):
        lines.append(f"- {key[0]} / {key[1]}：{value}")
    lines.extend(["", "引用失败的附加诊断标签不计入主分类。QUOTE_NOT_IN_FROZEN_TEXT 的标签计数：", ""])
    for key, value in sorted(tag_counts.items()):
        lines.append(f"- {key}：{value}")
    lines.extend([
        "",
        "## 3. 被校验拦截的原 CONTRADICT",
        "",
        "这里把 Poison 的原 CONTRADICT 称为检测意义上的正确方向，把 Clean/HN 的原 CONTRADICT 称为错误方向。这不是修复后的成绩。",
        f"Poison 原 CONTRADICT 被校验改成 INSUFFICIENT：F5 {blocked([i for i in audited if i['condition']=='L0-F5'], 'POISON', 'CONTRADICT')}，Oracle {blocked([i for i in audited if i['condition']=='L0-Oracle'], 'POISON', 'CONTRADICT')}。",
        f"Clean/HN 原 CONTRADICT 被校验改成 INSUFFICIENT：F5 {blocked([i for i in audited if i['condition']=='L0-F5'], {'CLEAN_CURRENT','HARD_NEGATIVE'}, 'CONTRADICT')}，Oracle {blocked([i for i in audited if i['condition']=='L0-Oracle'], {'CLEAN_CURRENT','HARD_NEGATIVE'}, 'CONTRADICT')}。",
        f"原 SUPPORT 被校验改成 INSUFFICIENT：F5 Poison {blocked([i for i in audited if i['condition']=='L0-F5'], 'POISON', 'SUPPORT')}，Clean {blocked([i for i in audited if i['condition']=='L0-F5'], 'CLEAN_CURRENT', 'SUPPORT')}，HN {blocked([i for i in audited if i['condition']=='L0-F5'], 'HARD_NEGATIVE', 'SUPPORT')}。",
        f"Oracle 对应为 Poison {blocked([i for i in audited if i['condition']=='L0-Oracle'], 'POISON', 'SUPPORT')}，Clean {blocked([i for i in audited if i['condition']=='L0-Oracle'], 'CLEAN_CURRENT', 'SUPPORT')}，HN {blocked([i for i in audited if i['condition']=='L0-Oracle'], 'HARD_NEGATIVE', 'SUPPORT')}。",
        "",
        "## 4. 校验通过后的事实判断",
        "",
        f"校验通过后 Poison 仍为 SUPPORT：F5 {sum(i['condition']=='L0-F5' and i['primary_category']==VALIDATION_PASSED and i['role']=='POISON' and i['final_verdict']=='SUPPORT' for i in audited)}，Oracle {sum(i['condition']=='L0-Oracle' and i['primary_category']==VALIDATION_PASSED and i['role']=='POISON' and i['final_verdict']=='SUPPORT' for i in audited)}。合计 {passed_poison_support}。",
        f"校验通过后 Clean 仍为 CONTRADICT：{passed_clean_contradict}。HN 仍为 CONTRADICT：{passed_hn_contradict}。",
        "",
        "## 5. 配对",
        "",
    ])
    for key, value in sorted(pair_counts.items()):
        lines.append(f"- {key}：{value}")
    lines.extend([
        "",
        f"Poison 上 Oracle 最终 CONTRADICT 而 F5 不是的配对数是 {len(oracle_recovers_poison)}。其中 F5 同时有输出失败的是 {recover_with_f5_failure}。",
        "两边的证据覆盖、正文长度、干扰和引用成功率可以同时变化，所以这些配对不能全部归因于检索召回。",
        "",
        "## 6. 案例选择",
        "",
        "选择规则按失败类别频数、Poison 与合法负例、校验通过后的事实错误，以及四类配对变化依次取第一条，最多 12 条。案例原文只在 PRIVATE_CASE_REVIEW.jsonl。",
        f"本轮选出 {len(chosen)} 条。作者语义判断仍待写入该私有文件，未写入本摘要。",
        "",
        "状态：FULL01_OFFLINE_OUTPUT_AUDIT_COMPLETE / OWNER_REVIEW_REQUIRED。",
        "",
    ])
    return "\n".join(lines)


if __name__ == "__main__":
    main()
