from __future__ import annotations

from collections.abc import Callable

from codeguarder.attacks.attack_schema import AttackSample
from codeguarder.attacks.prompt_renderer import render_prompt
from codeguarder.proxy.guard_proxy_stage5 import Stage5GuardService
from codeguarder.taxonomy.failure_taxonomy import classify_failure_types

from .garak_adapter import evaluate_final_text


GUARD_MODES = ("passthrough", "input-only", "output-only", "full-guard")


def run_sample_modes(
    sample: AttackSample,
    model_callable: Callable,
    model: str,
    seed: int,
) -> list[dict]:
    rendered = render_prompt(sample.prompt)
    records = []
    for mode in GUARD_MODES:
        service = Stage5GuardService(model_callable, mode)
        outcome = service.process(sample, rendered, model, seed)
        verdict = evaluate_final_text(outcome.final_output, sample)
        record = outcome.record
        record.update(
            {
                "garak_pass": verdict.garak_pass,
                "detector_source": verdict.detector_source,
                "detector_name": verdict.detector_name,
                "detector_matches": list(verdict.detector_matches),
            }
        )
        record["failure_types"] = classify_failure_types(record)
        records.append(record)
    return records
