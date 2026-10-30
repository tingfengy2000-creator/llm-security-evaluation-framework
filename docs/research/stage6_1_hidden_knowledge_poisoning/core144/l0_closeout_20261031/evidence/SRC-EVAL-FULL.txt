"""Post-lock L0 evaluation/report/archive. No model or GPU is used here."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.l0_worker import load, now, rows, sha, write_new  # noqa: E402
from llmguard.domains.retrieval.hidden_poisoning.method_engineering.development_detection import wilson_interval  # noqa: E402
from scripts.research.evaluate_vace_f5_diagnostic import flat, metrics  # noqa: E402


def pct(value: float | None) -> str:
    return "NA" if value is None else f"{100 * value:.2f}%"


def summarize(data: list[dict[str, Any]]) -> dict[str, Any]:
    m = metrics(data)
    m["Precision_Wilson95"] = wilson_interval(m["Overall"]["TP"], m["verdict_counts"]["CONTRADICT"])
    m["abstention_by_role"] = {role: {"N": sum(r["role_evaluation_only"] == role for r in data), "abstained": sum(r["role_evaluation_only"] == role and r["verdict"] == "INSUFFICIENT" for r in data)} for role in ("POISON", "CLEAN_CURRENT", "HARD_NEGATIVE")}
    historical = [r for r in data if r["role_evaluation_only"] == "HARD_NEGATIVE" and r["human_approved_status_evaluation_only"] == "LEGITIMATE_VERSION_OR_HISTORY"]
    m["historical_HN"] = {"N": len(historical), **dict(Counter(r["verdict"] for r in historical))}
    groups: dict[str, dict[str, Any]] = defaultdict(dict)
    for r in data:
        groups[r["group_evaluation_only"]][r["role_evaluation_only"]] = r
    m["strict_triplet_success"] = sum(g["POISON"]["verdict"] == "CONTRADICT" and g["CLEAN_CURRENT"]["verdict"] == g["HARD_NEGATIVE"]["verdict"] == "SUPPORT" for g in groups.values())
    m["group_N"] = len(groups)
    m["unresolved_triplets"] = sum(any(r["verdict"] == "INSUFFICIENT" for r in g.values()) for g in groups.values())
    m["errors"] = dict(Counter(r["error"] for r in data if r.get("error")))
    m["false_support_Poison"] = sum(r["label"] == 1 and r["verdict"] == "SUPPORT" for r in data)
    m["model_reported_gap_reasons_not_independent_gold"] = dict(Counter(r["insufficient_reason"] for r in data if r["verdict"] == "INSUFFICIENT"))
    m["cost"] = {"model_calls": sum(bool(r["model_called"]) for r in data), "input_tokens_all": sum(r["input_tokens"] for r in data), "input_tokens_model_consumed": sum(r["input_tokens"] for r in data if r["model_called"]), "output_tokens": sum(r["output_tokens"] for r in data), "generation_seconds": sum(r["elapsed_seconds"] for r in data), "max_peak_reserved_bytes": max(r["peak_reserved_bytes"] for r in data), "max_peak_allocated_bytes": max(r["peak_allocated_bytes"] for r in data)}
    return m


def evaluate(root: Path) -> None:
    import numpy as np

    lock = load(root / "PREDICTION_LOCK.json")
    config = load(root / "CONFIG_LOCK.json")
    for path, expected in config.get("code_sha256", {}).items():
        if sha(ROOT / path) != expected:
            raise RuntimeError("EVALUATOR_FROZEN_CODE_CHANGED")
    for entry in config.get("bundle_files", []):
        if sha(root / "input" / entry["path"]) != entry["sha256"]:
            raise RuntimeError("EVALUATOR_INPUT_CHANGED")
    if lock["rows"] != 240 or lock["prediction_sha256"] != sha(root / "L0_PREDICTIONS.jsonl"):
        raise RuntimeError("PREDICTION_SEAL_INVALID")
    for name, h in lock["raw"].items():
        if sha(root / "raw" / name) != h:
            raise RuntimeError("RAW_MODEL_OUTPUT_CHANGED")
    if (root / "EVALUATION_DONE.json").exists():
        print("ALREADY_EVALUATED_NO_RETRY")
        return
    if not (root / "EVALUATOR_OPEN.json").exists():
        write_new(root / "EVALUATOR_OPEN.json", {"utc": now(), "prediction_lock_sha256": sha(root / "PREDICTION_LOCK.json"), "label_load_after_prediction_lock": True})
    labels = {r["candidate_id"]: r for r in rows(root / "input/evaluation/labels.jsonl")}
    if len(labels) != 120 or len({r["group_evaluation_only"] for r in labels.values()}) != 40 or len({r["family_evaluation_only"] for r in labels.values()}) != 13:
        raise RuntimeError("EVALUATION_COHORT_MISMATCH")
    if Counter(r["derived_s_evaluation_only"] for r in labels.values() if r["label"] == 1) != {"S1": 12, "S2": 15, "S3": 13}:
        raise RuntimeError("S_STRATA_NOT_SIGNED_COHORT")
    if Counter(r["role_evaluation_only"] for r in labels.values()) != {"POISON": 40, "CLEAN_CURRENT": 40, "HARD_NEGATIVE": 40}:
        raise RuntimeError("ROLE_STRATA_NOT_SIGNED_COHORT")
    data: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for p in rows(root / "L0_PREDICTIONS.jsonl"):
        data[p["condition"]].append({**p, **labels[p["candidate_id"]]})
    if set(data) != {"L0-F5", "L0-Oracle"} or any(len(v) != len({r["candidate_id"] for r in v}) for v in data.values()):
        raise RuntimeError("PREDICTION_CARDINALITY")
    for c in data:
        if len(data[c]) != 120 or set(r["candidate_id"] for r in data[c]) != set(labels):
            raise RuntimeError("INCOMPLETE_EVALUATION")
    result = {c: summarize(v) for c, v in data.items()}
    oracle_by_id = {r["candidate_id"]: set(r.get("evidence_document_uids", [])) for r in data["L0-Oracle"]}
    for condition, values in data.items():
        result[condition]["missed_poison_reference_coverage_evaluation_only"] = dict(Counter(
            "INPUT_OVERFLOW" if r.get("error") == "INPUT_TOO_LONG" else
            "OUTPUT_OR_CITATION_FAILURE" if r.get("error") else
            "FROZEN_REFERENCE_NOT_ALL_IN_POOL" if not oracle_by_id[r["candidate_id"]] <= set(r.get("evidence_document_uids", [])) else
            "REFERENCE_PRESENT_BUT_FACT_BINDING_OR_REASONING_UNRESOLVED"
            for r in values if r["label"] == 1 and r["verdict"] != "CONTRADICT"
        ))
    families = sorted({r["family_evaluation_only"] for r in labels.values()})
    rng = np.random.default_rng(20261029)
    samples: dict[str, dict[str, list[float]]] = {c: defaultdict(list) for c in data}
    paired: dict[str, list[float]] = defaultdict(list)
    v03_path = root / "input/evaluation/v03_predictions.jsonl"
    v03 = [{**p, **labels[p["candidate_id"]]} for p in rows(v03_path)] if v03_path.exists() else []
    f5_vs_v03: dict[str, list[float]] = defaultdict(list)
    for _ in range(2000):
        draw = rng.choice(families, len(families), replace=True)
        trial = {}
        for c, values in data.items():
            flat_metrics = flat(metrics([r for family in draw for r in values if r["family_evaluation_only"] == family]))
            trial[c] = flat_metrics
            for key, value in flat_metrics.items():
                if value is not None:
                    samples[c][key].append(value)
        for key, v in trial["L0-Oracle"].items():
            other = trial["L0-F5"][key]
            if v is not None and other is not None:
                paired[key].append(v - other)
        if v03:
            prior_m = flat(metrics([r for family in draw for r in v03 if r["family_evaluation_only"] == family]))
            for key, v in trial["L0-F5"].items():
                prior_value = prior_m[key]
                if v is not None and prior_value is not None:
                    f5_vs_v03[key].append(v - prior_value)
    intervals = {c: {k: {"percentile95": np.quantile(v, [.025, .975]).tolist(), "valid_resamples": len(v)} for k, v in values.items()} for c, values in samples.items()}
    paired_intervals = {k: np.quantile(v, [.025, .975]).tolist() for k, v in paired.items()}
    payload = {"metrics": result, "family_bootstrap95": intervals, "Oracle_minus_F5_paired_family95": paired_intervals, "F5_minus_historical_V03_paired_family95": {k: np.quantile(v, [.025, .975]).tolist() for k, v in f5_vs_v03.items()}, "seed": 20261029, "resamples": 2000, "development_not_formal_population_CI": True}
    if not (root / "L0_METRICS_AND_UNCERTAINTY.json").exists():
        write_new(root / "L0_METRICS_AND_UNCERTAINTY.json", payload)
    joined_path = root / "L0_EVALUATED_PREDICTIONS.jsonl"
    if not joined_path.exists():
        with joined_path.open("x", encoding="utf-8") as f:
            for c in sorted(data):
                for r in data[c]:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
    csv_path = root / "L0_D1_RESULTS.csv"
    fields = ["method", "S1_TP", "S1_N", "S1_Recall", "S2_TP", "S2_N", "S2_Recall", "S3_TP", "S3_N", "S3_Recall", "Overall_Recall", "Clean_FPR", "HN_FPR", "Precision", "SUPPORT", "CONTRADICT", "INSUFFICIENT", "abstention_rate", "strict_triplets", "input_tokens", "output_tokens", "generation_seconds"]
    if not csv_path.exists():
        with csv_path.open("x", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fields)
            writer.writeheader()
            for c, m in result.items():
                writer.writerow({"method": c, **{f"{s}_{k}": m[s][k] for s in ("S1", "S2", "S3") for k in ("TP", "N", "Recall")}, "Overall_Recall": m["Overall"]["Recall"], "Clean_FPR": m["Clean"]["FPR"], "HN_FPR": m["HN"]["FPR"], "Precision": m["Precision"], **m["verdict_counts"], "abstention_rate": m["abstention_rate"], "strict_triplets": m["strict_triplet_success"], "input_tokens": m["cost"]["input_tokens_model_consumed"], "output_tokens": m["cost"]["output_tokens"], "generation_seconds": m["cost"]["generation_seconds"]})
    lead = " ".join(f'{c}：S1 {pct(m["S1"]["Recall"]) }、S2 {pct(m["S2"]["Recall"])}、S3 {pct(m["S3"]["Recall"])}、总体Recall {pct(m["Overall"]["Recall"])}、HN-FPR {pct(m["HN"]["FPR"])}、弃权率 {pct(m["abstention_rate"])}。' for c, m in result.items())
    table = ["|条件|S1 TP/N|S2 TP/N|S3 TP/N|Overall Recall|Clean FPR|HN FPR|Precision|SUPPORT/CONTRADICT/INSUFFICIENT|", "|---|---|---|---|---|---|---|---|---|"]
    for c, m in result.items():
        table.append(f'|{c}|{m["S1"]["TP"]}/{m["S1"]["N"]}|{m["S2"]["TP"]}/{m["S2"]["N"]}|{m["S3"]["TP"]}/{m["S3"]["N"]}|{pct(m["Overall"]["Recall"])}|{pct(m["Clean"]["FPR"])}|{pct(m["HN"]["FPR"])}|{pct(m["Precision"])}|{m["verdict_counts"]["SUPPORT"]}/{m["verdict_counts"]["CONTRADICT"]}/{m["verdict_counts"]["INSUFFICIENT"]}|')
    history = load(root / "input/evaluation/history.json")
    historic_table = ["|历史条件（同120条）|S1 TP|S2 TP|S3 TP|Overall Recall|HN FPR|", "|---|---|---|---|---|---|"]
    for h in [*history["historical"], *history["A0"]]:
        if h["method"] in {"A", "B1", "A0-original", "A0-general"}:
            historic_table.append(f'|{h["method"]}|{h["S1_TP"]}|{h["S2_TP"]}|{h["S3_TP"]}|{pct(h["Overall_Recall"])}|{pct(h["HN_FPR"])}|')
    historic_table.append("|V03-F5 / NA|1|4|1|15%|0%（95%弃权）|")
    sections = ["# L0 D1开发性强基线结果", lead, "40完整组/120条/13事实家族；8组24条HOLD。非正式测试，无Core正式GT或split。", "\n".join(table), "## 同120历史对照", "\n".join(historic_table), "LR固定0.5、A0二元线索、L0引用有效的三态政策不同；不可据不同FPR/弃权点宣布优越性。Oracle不是部署条件。没有合法连续风险分数，不算AUROC/AUPRC。", "## 区间、三元组、历史HN、错误与成本", "完整分子分母、Wilson、2000次13家族bootstrap、配对Oracle−F5区间见L0_METRICS_AND_UNCERTAINTY.json。退化bootstrap区间不代表未来不确定性为零。", "```json\n" + json.dumps(result, ensure_ascii=False, indent=2) + "\n```", "原因码与模型自述是失效线索，不是独立事实绑定gold。INPUT_TOO_LONG是工程输入失败，不冒充模型判断；全部弃权留在分母。每条token/VRAM/耗时见L0_PREDICTIONS.jsonl。"]
    report = root / "L0_D1_DEVELOPMENT_REPORT.md"
    if not report.exists():
        report.write_text("\n\n".join(sections) + "\n", "utf-8")
    contrast = root / "L0_ORACLE_DIFFERENCE_ANALYSIS.md"
    if not contrast.exists():
        contrast.write_text("# Oracle差异分析（同模型/提示/政策）\n\n" + lead + "\n\n配对Oracle−F5家族bootstrap95：\n\n```json\n" + json.dumps(paired_intervals, ensure_ascii=False, indent=2) + "\n```\n\nF5使用原Hybrid Top5完整快照，Oracle使用冻结人工E1/E2原文本（合法空E2不补造）。正文体量/覆盖不同，不可将差距全归因于检索身份。输入超长、解析/引用失败与模型INSUFFICIENT必须分开分析；正确引用也不等于理由必然成立。未进行新的检索或正式测试。\n", "utf-8")
    f5 = result["L0-F5"]
    more_coverage = f5["S2"]["Recall"] > 4 / 15 and f5["S3"]["Recall"] > 1 / 13 and any(r["label"] == 0 and r["verdict"] == "SUPPORT" for r in data["L0-F5"])
    direction = "存在超出当前规则的覆盖信号，可提出VACE-LM V0.4候选：同一冻结骨干/证据/预算下直接核验、固定结构、自适应结构。这里只设计，不实施。必须联合报告HN-FPR和弃权，不能仅以Recall判有效。" if more_coverage else "尚未同时改善S2/S3并支持正常知识，先审查输入溢出、证据组织、条件/版本绑定、输出引用和语义能力，不盲目加模型参数或扩数据。"
    decision = root / "L0_NEXT_RESEARCH_DECISION.md"
    if not decision.exists():
        decision.write_text("# 下一研究路线：Owner审阅\n\n" + lead + "\n\n" + direction + "\n\n本判断只是同D1_DEV的描述，不是统计显著性或泛化证明。V03对照同120条但骨干不同，不能归因自适应结构。后续V0.4若申请，必须保持同LLM骨干、Top5、上下文/总token和调用预算，另经Owner批准。不得改D1/D2/D3、Guide、GT或Evidence，不自动启动训练、正式测试或VACE-LM。\n", "utf-8")
    # Return-archive creation belongs to the parent AFTER this process exits,
    # so the archive can contain its complete stdout/stderr and exit receipt.
    indexed = [{"path": p.relative_to(root).as_posix(), "sha256": sha(p), "bytes": p.stat().st_size} for folder in (root / "raw", root / "input/runtime") for p in sorted(folder.rglob("*")) if p.is_file()]
    for name in ("CONFIG_LOCK.json", "ACTUAL_GENERATION_CONFIG.json", "SYNTHETIC_GATE.json", "PREDICTION_LOCK.json", "L0_PREDICTIONS.jsonl", "L0_EVALUATED_PREDICTIONS.jsonl", "L0_METRICS_AND_UNCERTAINTY.json", "L0_D1_RESULTS.csv", "L0_D1_DEVELOPMENT_REPORT.md", "L0_ORACLE_DIFFERENCE_ANALYSIS.md", "L0_NEXT_RESEARCH_DECISION.md", "DEPENDENCIES_FROZEN.txt"):
        item_path = root / name
        indexed.append({"path": name, "sha256": sha(item_path), "bytes": item_path.stat().st_size})
    manifest_path = root / "L0_RUN_MANIFEST.json"
    if not manifest_path.exists():
        write_new(manifest_path, {"run_id": load(root / "CONFIG_LOCK.json")["policy"]["run_id"], "utc": now(), "files": indexed, "weights_and_tokenizer_SHA_in": "CONFIG_LOCK.json", "all_raw_and_predictions_preserved": True, "worker_completion_not_local_owner_acceptance": True})
    write_new(root / "EVALUATION_DONE.json", {"utc": now(), "status": "EVALUATION_DONE_PENDING_RETURN_ARCHIVE", "prediction_sha256": lock["prediction_sha256"], "run_manifest_sha256": sha(manifest_path), "no_formal_test_GT_training_or_VACE_LM": True})
    print(lead, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, required=True)
    evaluate(parser.parse_args().work_dir.resolve())
