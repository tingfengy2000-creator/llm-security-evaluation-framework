from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from codeguarder.attacks.attack_schema import AttackSample
from codeguarder.attacks.hash_utils import sha256_text
from codeguarder.attacks.prompt_renderer import RenderedPrompt
from codeguarder.taxonomy.classifier import classify_risk


GUARD_MODES = {
    "passthrough": (False, False),
    "input-only": (True, False),
    "output-only": (False, True),
    "full-guard": (True, True),
}


def _load_historical_guard():
    workspace_root = Path(__file__).resolve().parents[3]
    scripts_dir = workspace_root / "llm-security-stage1" / "scripts"
    scripts_text = str(scripts_dir)
    if scripts_text not in sys.path:
        sys.path.insert(0, scripts_text)
    from guard_proxy import GuardEngine, REFUSAL_TEXT

    return GuardEngine, REFUSAL_TEXT


GuardEngine, REFUSAL_TEXT = _load_historical_guard()
ModelCallable = Callable[[tuple[dict[str, str], ...], str, int], str]


@dataclass(frozen=True)
class ServiceOutcome:
    record: dict
    final_output: str


class Stage5GuardService:
    def __init__(
        self,
        model_callable: ModelCallable,
        guard_mode: str,
        engine=None,
    ):
        if guard_mode not in GUARD_MODES:
            raise ValueError(f"unsupported guard mode: {guard_mode}")
        self.model_callable = model_callable
        self.guard_mode = guard_mode
        self.input_guard_enabled, self.output_guard_enabled = GUARD_MODES[guard_mode]
        self.engine = engine or GuardEngine()

    def process(
        self,
        sample: AttackSample,
        rendered: RenderedPrompt,
        model: str,
        seed: int,
    ) -> ServiceOutcome:
        started = time.perf_counter()
        prompt_text = "\n".join(message["content"] for message in rendered.messages)
        input_decision = self.engine.inspect_input(prompt_text)
        record = {
            "sample_id": sample.id,
            "category": sample.category,
            "variant": sample.variant,
            "severity": sample.severity,
            "benign_sample": sample.benign,
            "guard_mode": self.guard_mode,
            "input_guard_enabled": self.input_guard_enabled,
            "output_guard_enabled": self.output_guard_enabled,
            "prompt_hash": rendered.prompt_hash,
            "turn_count": len(rendered.messages),
            "seed": seed,
            "model": model,
            "input_matches": list(input_decision.matches),
            "input_blocked": False,
            "output_matches": [],
            "output_blocked": False,
            "upstream_called": False,
            "raw_model_output_hash": None,
            "raw_model_output_length": None,
            "raw_model_risk": False,
            "raw_risk_matches": [],
            "final_output_hash": None,
            "final_output_length": None,
            "final_risk": False,
            "final_risk_matches": [],
            "confidentiality_breach": False,
            "tool_call_intent": False,
            "would_execute_side_effect": False,
            "final_decision": None,
        }

        if self.input_guard_enabled and input_decision.blocked:
            final_output = REFUSAL_TEXT
            record["input_blocked"] = True
            record["final_decision"] = "input_block"
        else:
            record["upstream_called"] = True
            raw_output = self.model_callable(rendered.messages, model, seed)
            record["raw_model_output_hash"] = sha256_text(raw_output)
            record["raw_model_output_length"] = len(raw_output)
            raw_risk = classify_risk(
                raw_output,
                sample.expected_risk_patterns,
                sample.category,
            )
            record["raw_model_risk"] = raw_risk.risk
            record["raw_risk_matches"] = list(raw_risk.matches)
            record["confidentiality_breach"] = raw_risk.confidentiality_breach
            record["tool_call_intent"] = raw_risk.tool_call_intent
            record["would_execute_side_effect"] = raw_risk.would_execute_side_effect

            output_decision = self.engine.inspect_output(raw_output)
            record["output_matches"] = list(output_decision.matches)
            if self.output_guard_enabled and output_decision.blocked:
                final_output = REFUSAL_TEXT
                record["output_blocked"] = True
                record["final_decision"] = "output_block"
            else:
                final_output = raw_output
                record["final_decision"] = "allow"

        final_risk = classify_risk(
            final_output,
            sample.expected_risk_patterns,
            sample.category,
        )
        record["final_output_hash"] = sha256_text(final_output)
        record["final_output_length"] = len(final_output)
        record["final_risk"] = final_risk.risk
        record["final_risk_matches"] = list(final_risk.matches)
        record["latency_ms"] = round((time.perf_counter() - started) * 1000, 3)
        return ServiceOutcome(record=record, final_output=final_output)
