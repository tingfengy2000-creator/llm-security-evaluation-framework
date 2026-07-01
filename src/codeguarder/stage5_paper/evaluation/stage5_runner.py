from __future__ import annotations

import argparse
import json
import shutil
import urllib.request
import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..attacks.loader import load_attack_matrix, load_benign_requests
from ..attacks.renderer import render_prompt
from ..audit.attempt_record import ExperimentConfig
from ..audit.canonical_log import write_canonical_attempts
from ..audit.fingerprints import attempt_id, experiment_fingerprint, sha256_file
from ..metrics.suite import compute_metrics
from ..proxy.http_api import running_proxy
from ..proxy.service import ProxyService
from ..reporting.architecture_figure import render_architecture_figures
from ..reporting.exporters import (
    heatmap_rows,
    metric_rows,
    taxonomy_result,
    write_csv,
    write_json,
    write_jsonl,
    write_summary,
)
from ..taxonomy.engine import classify_failure_types
from .providers import GroqProvider, MockProvider
from .validators import validate_output_only, validate_prompt_hash_parity


GUARD_MODES = {
    "P": "passthrough",
    "I": "input-only",
    "O": "output-only",
    "F": "full-guard",
}


def _post(url: str, payload: dict[str, Any], guard_code: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-CodeGuarder-Mode": guard_code,
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def _execution_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}-{uuid.uuid4().hex[:6]}"


def run_experiment(
    provider_name: str,
    data_root: Path,
    output_root: Path,
    include_benign: bool = True,
    seed: int = 42,
    model: str = "llama-3.1-8b-instant",
    attack_id: str | None = None,
) -> dict[str, Any]:
    data_root = Path(data_root)
    output_root = Path(output_root)
    attacks = load_attack_matrix(data_root)
    if attack_id:
        attacks = [sample for sample in attacks if sample.attack_id == attack_id]
    samples = attacks + (load_benign_requests(data_root) if include_benign else [])
    manifest_hash = sha256_file(data_root / "dataset_manifest.json")
    config = ExperimentConfig(
        schema_version="2.0",
        dataset_manifest_hash=manifest_hash,
        provider=provider_name,
        model=model,
        seed=seed,
        generation_config={"temperature": 0, "top_p": 1, "max_tokens": 160},
        detector_config=("garak", "stage5_pattern"),
        guard_version="stage4-rule-baseline",
    )
    fingerprint = experiment_fingerprint(config)
    execution_id = _execution_id()
    run_dir = output_root / "runs" / execution_id
    run_dir.mkdir(parents=True, exist_ok=False)
    provider = MockProvider() if provider_name == "mock" else GroqProvider()
    records: list[dict[str, Any]] = []
    measurements: list[dict[str, Any]] = []

    with running_proxy(ProxyService(provider)) as proxy:
        endpoint = proxy.url + "/v1/chat/completions"
        for sample in samples:
            rendered = render_prompt(sample.prompt)
            for guard_code, guard_mode in GUARD_MODES.items():
                payload = {
                    "model": model,
                    "messages": list(rendered.messages),
                    "seed": seed,
                    "_codeguarder": {"sample": asdict(sample)},
                }
                response = _post(endpoint, payload, guard_code)
                audit = response["_codeguarder"]
                aid = attempt_id(fingerprint, sample.sample_id, guard_code, 0)
                record = {
                    "schema_version": "2.0",
                    "experiment_fingerprint": fingerprint,
                    "attempt_id": aid,
                    "repetition_index": 0,
                    "sample_id": sample.sample_id,
                    "attack_id": sample.attack_id,
                    "threat_layer": sample.threat_layer,
                    "attack_family": sample.attack_family,
                    "variant": sample.variant,
                    "severity": sample.severity,
                    "benign_sample": sample.benign,
                    "guard_code": guard_code,
                    "guard_mode": guard_mode,
                    "model_provider": provider_name,
                    "model_name": model,
                    "seed": seed,
                    "prompt_hash": rendered.prompt_hash,
                    "turn_count": rendered.turn_count,
                    **{key: value for key, value in audit.items() if key != "latency_ms"},
                }
                record["failure_types"] = classify_failure_types(record)
                records.append(record)
                measurements.append(
                    {
                        "attempt_id": aid,
                        "execution_id": execution_id,
                        "latency_ms": audit["latency_ms"],
                        "retry_count": 0,
                    }
                )

    issues = [
        *validate_prompt_hash_parity(records),
        *validate_output_only(records),
    ]
    metrics = compute_metrics(
        [
            {
                **record,
                "latency_ms": next(
                    item["latency_ms"]
                    for item in measurements
                    if item["attempt_id"] == record["attempt_id"]
                ),
            }
            for record in records
        ]
    )
    status = "completed" if not issues else "invalid"
    result = {
        "schema_version": "2.0",
        "execution_id": execution_id,
        "experiment_fingerprint": fingerprint,
        "run_status": status,
        "provider": provider_name,
        "model": model,
        "sample_count": len(samples),
        "attempt_count": len(records),
        "prompt_hash_parity": not any(
            issue.code == "prompt_hash_parity" for issue in issues
        ),
        "validation_issues": [asdict(issue) for issue in issues],
        "metrics": metrics,
        "conclusion_scope": "当前攻击矩阵、当前模型与当前规则基线下",
    }

    write_canonical_attempts(run_dir / "canonical_attempts.jsonl", records)
    write_jsonl(run_dir / "measurements.jsonl", measurements)
    write_json(run_dir / "experiment_result.json", result)
    taxonomy = taxonomy_result(records)
    write_json(run_dir / "taxonomy_result.json", taxonomy)
    write_csv(run_dir / "metrics_summary.csv", metric_rows(metrics))
    write_csv(run_dir / "attack_heatmap.csv", heatmap_rows(records, "attack_id"))
    write_csv(
        run_dir / "threat_layer_heatmap.csv",
        heatmap_rows(records, "threat_layer"),
    )
    write_json(
        run_dir / "run_manifest.json",
        {
            "execution_id": execution_id,
            "experiment_config": config.canonical_dict(),
            "experiment_fingerprint": fingerprint,
            "canonical_log_sha256": sha256_file(
                run_dir / "canonical_attempts.jsonl"
            ),
        },
    )
    write_summary(
        run_dir / "run_summary.md",
        execution_id,
        fingerprint,
        status,
        len(records),
        metrics,
    )
    latest = output_root / "latest"
    latest.mkdir(parents=True, exist_ok=True)
    for name in (
        "experiment_result.json",
        "taxonomy_result.json",
        "metrics_summary.csv",
        "attack_heatmap.csv",
        "threat_layer_heatmap.csv",
    ):
        shutil.copy2(run_dir / name, latest / name)
    render_architecture_figures(output_root / "figures")
    return {
        **result,
        "run_dir": str(run_dir),
        "output_root": str(output_root),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage 5 Paper Dataset Runner")
    parser.add_argument("--provider", choices=("mock", "groq"), default="mock")
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--model", default="llama-3.1-8b-instant")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--attack-id", choices=("A1", "A2", "A3", "A4", "A5", "A6"))
    parser.add_argument("--include-benign", action="store_true")
    args = parser.parse_args()
    result = run_experiment(
        provider_name=args.provider,
        data_root=args.data_root,
        output_root=args.output_root,
        include_benign=args.include_benign,
        seed=args.seed,
        model=args.model,
        attack_id=args.attack_id,
    )
    print(f"execution_id={result['execution_id']}")
    print(f"run_status={result['run_status']}")
    print(f"attempt_count={result['attempt_count']}")
    return 0 if result["run_status"] == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
