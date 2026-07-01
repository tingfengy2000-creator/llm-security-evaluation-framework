from __future__ import annotations

import argparse
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from codeguarder.attacks.attack_schema import AttackSample
from codeguarder.attacks.matrix_loader import (
    ATTACK_CATEGORIES,
    load_attack_matrix,
    load_benign_requests,
)
from codeguarder.reporting.csv_exporter import write_csv
from codeguarder.reporting.heatmap_exporter import write_heatmap
from codeguarder.reporting.json_report import write_json, write_jsonl
from codeguarder.reporting.markdown_report import write_run_summary

from .guard_mode_runner import run_sample_modes
from .result_collector import (
    collect_heatmap,
    collect_metrics,
    collect_overall,
    collect_taxonomy,
)
from .validators import (
    ValidationIssue,
    validate_no_secret_leak,
    validate_output_only,
    validate_prompt_hash_parity,
    validate_raw_output_hash_parity,
    validate_report_integrity,
)


DEFAULT_MODEL = "llama-3.1-8b-instant"


def _new_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{timestamp}-{uuid.uuid4().hex[:6]}"


def _mock_model_for(sample: AttackSample) -> Callable:
    if sample.benign:
        response = "This is a normal synthetic response."
    elif sample.variant == "delete_intent":
        response = "delete_file(path='synthetic.tmp')"
    elif sample.variant == "external_send_intent":
        response = "send_external(destination='example.invalid')"
    else:
        response = sample.expected_risk_patterns[0]

    def call(messages, model, seed):
        del messages, model, seed
        return response

    return call


def _groq_model() -> Callable:
    from openai import OpenAI

    credential = os.environ.get("GROQ_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not credential:
        raise RuntimeError("Groq credential environment variable is not configured")
    client = OpenAI(
        api_key=credential,
        base_url="https://api.groq.com/openai/v1",
        timeout=45,
        max_retries=3,
    )

    def call(messages, model, seed):
        response = client.chat.completions.create(
            model=model,
            messages=list(messages),
            temperature=0,
            top_p=1,
            max_tokens=160,
            seed=seed,
        )
        return response.choices[0].message.content or ""

    return call


def _issues_as_dicts(issues: list[ValidationIssue]) -> list[dict]:
    return [
        {"code": issue.code, "message": issue.message, "sample_id": issue.sample_id}
        for issue in issues
    ]


def run_experiment(
    provider: str,
    data_root: Path,
    output_root: Path,
    per_category: int = 2,
    include_benign: bool = True,
    category: str | None = None,
    delay_seconds: float = 0,
    model: str = DEFAULT_MODEL,
    seed: int = 42,
) -> dict:
    if provider not in {"mock", "groq"}:
        raise ValueError("provider must be mock or groq")
    if category is not None and category not in ATTACK_CATEGORIES:
        raise ValueError(f"unsupported category: {category}")

    attacks = load_attack_matrix(Path(data_root), per_category=per_category)
    if category:
        attacks = [sample for sample in attacks if sample.category == category]
    samples = attacks + (
        load_benign_requests(Path(data_root)) if include_benign else []
    )
    run_id = _new_run_id()
    run_dir = Path(output_root) / "logs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    shared_groq_model = _groq_model() if provider == "groq" else None
    records = []
    for index, sample in enumerate(samples):
        model_callable = shared_groq_model or _mock_model_for(sample)
        records.extend(run_sample_modes(sample, model_callable, model, seed))
        if delay_seconds > 0 and index + 1 < len(samples):
            time.sleep(delay_seconds)

    required_issues = []
    required_issues.extend(validate_prompt_hash_parity(records))
    required_issues.extend(validate_output_only(records))
    required_issues.extend(
        validate_report_integrity(records, {sample.id for sample in samples})
    )
    raw_hash_issues = validate_raw_output_hash_parity(records)
    metrics_rows = collect_metrics(records)
    heatmap_rows = collect_heatmap(records)
    taxonomy = collect_taxonomy(records)

    result = {
        "run_id": run_id,
        "run_status": "completed" if not required_issues else "invalid",
        "provider": provider,
        "model": model,
        "seed": seed,
        "sample_count": len(samples),
        "attempt_count": len(records),
        "conclusion_scope": "当前攻击矩阵和当前规则基线下",
        "detector_note": (
            "detector_source=stage5_pattern 是实验适配层，不等同于官方 garak 扫描。"
        ),
        "overall_metrics": collect_overall(records),
        "prompt_hash_parity": not any(
            issue.code == "prompt_hash_parity" for issue in required_issues
        ),
        "raw_output_hash_parity": not raw_hash_issues,
        "validation_issues": _issues_as_dicts(required_issues),
        "raw_hash_observations": _issues_as_dicts(raw_hash_issues),
        "attempts": records,
    }

    result_path = Path(output_root) / "attack_matrix_result.json"
    taxonomy_path = Path(output_root) / "failure_taxonomy_result.json"
    metrics_path = Path(output_root) / "metrics_summary.csv"
    heatmap_path = Path(output_root) / "attack_coverage_heatmap.csv"
    summary_path = run_dir / "run_summary.md"
    attempts_path = run_dir / "attempts.jsonl"
    manifest_path = run_dir / "run_manifest.json"
    run_result_path = run_dir / "attack_matrix_result.json"
    run_taxonomy_path = run_dir / "failure_taxonomy_result.json"
    run_metrics_path = run_dir / "metrics_summary.csv"
    run_heatmap_path = run_dir / "attack_coverage_heatmap.csv"

    write_json(result_path, result)
    write_json(run_result_path, result)
    write_json(taxonomy_path, {"run_id": run_id, **taxonomy})
    write_json(run_taxonomy_path, {"run_id": run_id, **taxonomy})
    write_csv(metrics_path, metrics_rows)
    write_csv(run_metrics_path, metrics_rows)
    write_heatmap(heatmap_path, heatmap_rows)
    write_heatmap(run_heatmap_path, heatmap_rows)
    write_jsonl(attempts_path, records)
    write_run_summary(
        summary_path,
        run_id,
        provider,
        result["run_status"],
        metrics_rows,
        result["validation_issues"],
    )
    write_json(manifest_path, {key: value for key, value in result.items() if key != "attempts"})

    artifact_paths = [
        result_path,
        taxonomy_path,
        metrics_path,
        heatmap_path,
        summary_path,
        attempts_path,
        manifest_path,
        run_result_path,
        run_taxonomy_path,
        run_metrics_path,
        run_heatmap_path,
    ]
    secret_issues = validate_no_secret_leak(artifact_paths)
    if secret_issues:
        result["run_status"] = "invalid"
        result["validation_issues"].extend(_issues_as_dicts(secret_issues))
        write_json(result_path, result)
        write_json(run_result_path, result)
        write_json(
            manifest_path,
            {key: value for key, value in result.items() if key != "attempts"},
        )
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Stage 5 attack matrix")
    parser.add_argument("--provider", choices=("mock", "groq"), default="mock")
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--per-category", type=int, default=2)
    parser.add_argument("--category", choices=ATTACK_CATEGORIES)
    parser.add_argument("--include-benign", action="store_true")
    parser.add_argument("--delay-seconds", type=float, default=0)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--seed", type=int, default=42)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = run_experiment(
        provider=args.provider,
        data_root=args.data_root,
        output_root=args.output_root,
        per_category=args.per_category,
        include_benign=args.include_benign,
        category=args.category,
        delay_seconds=args.delay_seconds,
        model=args.model,
        seed=args.seed,
    )
    print(f"run_id={result['run_id']}")
    print(f"run_status={result['run_status']}")
    print(f"attempt_count={result['attempt_count']}")
    return 0 if result["run_status"] == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
