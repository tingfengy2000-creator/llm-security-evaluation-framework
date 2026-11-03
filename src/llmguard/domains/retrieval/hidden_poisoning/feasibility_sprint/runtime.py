"""Bounded orchestration. Runtime has no label path or evaluator import."""
from __future__ import annotations

import copy
import hashlib
from decimal import Decimal
from pathlib import Path
from typing import Any, Protocol

from ..method_engineering.llm_verification import parse_output
from .api import write_new
from .contracts import digest, empty_result, parse_structured, validate_runtime
from .prompts import messages

GAPS = {"scope_condition", "time_version", "source_role", "joint_evidence"}


class Client(Protocol):
    def call(self, messages: list[dict[str, str]], kind: str, max_output: int, probe: bool = False) -> dict[str, Any]: ...


class Engine:
    def __init__(self, client: Client):
        self.client = client
        self.unique_calls: list[dict[str, Any]] = []

    def invoke(self, row: dict[str, Any], kind: str, gaps: list[str] | None = None) -> dict[str, Any]:
        cap = {"direct": 1024, "internal": 2048, "structured": 4096, "followup": 4096}[kind]
        response = self.client.call(messages(row, kind, gaps), kind, cap)
        self.unique_calls.append({k: response[k] for k in ("call_id", "input_tokens", "output_tokens", "thinking_tokens", "latency", "estimated_cost")})
        if kind == "direct":
            # Reuse the frozen citation semantics without modifying L0 or its prompt.
            old = parse_output(response["content"], row)
            result = empty_result(old["error"])
            result.update(raw_model_verdict=old["model_verdict"], final_verdict=old["verdict"],
                          evidence_refs=old["citations"], missing_obligations=[old["insufficient_reason"]] if old["verdict"] == "INSUFFICIENT" else [])
            if old["verdict"] == "SUPPORT":
                result["supporting_spans"] = old["citations"]
            elif old["verdict"] == "CONTRADICT":
                result["conflicting_spans"] = old["citations"]
        else:
            result = parse_structured(response["content"], row, internal=kind == "internal")
        result.update(raw_output=response["content"], call_records=[{k: v for k, v in response.items() if k != "content"}], route_trace=[kind])
        return result

    def structured(self, row: dict[str, Any]) -> dict[str, Any]:
        first = self.invoke(row, "structured")
        gaps = sorted(GAPS & set(first["missing_obligations"]))
        # Never turn a JSON/quote error into a paid repair attempt.
        if first["parser_status"] != "OK" or first["final_verdict"] != "INSUFFICIENT" or not gaps:
            return first
        second = self.invoke(row, "followup", gaps)
        second["route_trace"] = first["route_trace"] + ["gap_check:" + ",".join(gaps)] + second["route_trace"]
        second["call_records"] = first["call_records"] + second["call_records"]
        second["prior_output"] = first
        return second

    @staticmethod
    def merge(front: dict[str, Any], external: dict[str, Any] | None) -> dict[str, Any]:
        result = copy.deepcopy(front if external is None else external)
        if external is not None:
            result["route_trace"] = front["route_trace"] + ["NO_INTERNAL_CERTIFICATE"] + external["route_trace"]
            result["call_records"] = front["call_records"] + external["call_records"]
            result["front_parser_status"] = front["parser_status"]
            result["front_raw_model_verdict"] = front["raw_model_verdict"]
            result["front_output"] = copy.deepcopy(front)
        else:
            result["route_trace"].append("INTERNAL_CONTRADICTION_CERTIFIED")
        return result

    def predict(self, row: dict[str, Any], e4: bool = False) -> dict[str, dict[str, Any]]:
        validate_runtime(row)
        front = self.invoke(row, "internal")
        direct = self.invoke(row, "direct")  # E1 always runs, including internal conflicts.
        certified = front.get("certificate_status") == "INTERNAL_CONTRADICTION_CERTIFIED"
        structured = self.structured(row) if not certified or e4 else None
        conditions = {"E1": direct, "E2": self.merge(front, None if certified else direct),
                      "E3": self.merge(front, None if certified else structured)}
        if e4:
            assert structured is not None
            conditions["E4"] = copy.deepcopy(structured)
        for condition, result in conditions.items():
            result.update(candidate_id=row["candidate_id"], condition=condition, input_sha256=digest(row))
            records = result["call_records"]
            result.update(input_tokens=sum(c["input_tokens"] for c in records), output_tokens=sum(c["output_tokens"] for c in records),
                          thinking_tokens=None if any(c["thinking_tokens"] is None for c in records) else sum(c["thinking_tokens"] for c in records),
                          latency=sum(c["latency"] for c in records),
                          estimated_cost=str(sum(Decimal(c["estimated_cost"]) for c in records)),
                          model_calls=len(records))
        return conditions


def predict_all(engine: Engine, rows: list[dict[str, Any]], run_dir: Path, config_sha: str, e4: bool = False) -> None:
    ids = [row["candidate_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("DUPLICATE_CANDIDATE_ID")
    predictions: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        outputs = engine.predict(row, e4=e4)
        write_new(run_dir / "raw" / f"candidate-{index:03d}.json", outputs)
        predictions.extend(outputs.values())
    write_new(run_dir / "PREDICTIONS.json", predictions)
    write_new(run_dir / "PREDICTION_LOCK.json", {"prediction_sha256": digest(predictions), "runtime_sha256": digest(rows),
               "config_lock_sha256": config_sha, "candidates": len(rows), "conditions": ["E1", "E2", "E3", "E4"] if e4 else ["E1", "E2", "E3"],
               "ids_sha256": digest(ids), "unique_call_costs": engine.unique_calls,
               "raw_files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((run_dir / "raw").glob("*.json"))},
               "not_formal_test": True, "sealed_before_labels": True})
